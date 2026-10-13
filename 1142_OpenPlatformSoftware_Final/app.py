import base64
import csv
import hashlib
import hmac
import json
import logging
import os
import re
import sys
import random
import sqlite3
from typing import Dict, List, Optional, Tuple, Union

import requests
from flask import Flask, abort, jsonify, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
from linebot.v3.messaging import ApiClient, Configuration, MessagingApi, ShowLoadingAnimationRequest

# 導入核心檢索與 AI 引擎
import engine

load_dotenv()

app = Flask(__name__)

# 設定/配置 root logger 以便將日誌正常輸出到 stdout
for h in logging.root.handlers[:]:
    logging.root.removeHandler(h)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.root.addHandler(stdout_handler)
logging.root.setLevel(logging.INFO)


def verify_line_signature(body: bytes, signature: str, channel_secret: str) -> bool:
    if not body or not signature or not channel_secret:
        return False
    digest = hmac.new(channel_secret.encode("utf-8"), body, hashlib.sha256).digest()
    computed = base64.b64encode(digest).decode("utf-8")
    return hmac.compare_digest(computed, signature)


def reply_line_message(reply_token: str, text: str, access_token: str) -> None:
    if not reply_token or not access_token:
        return
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": text,
            }
        ],
    }
    try:
        requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=payload, timeout=10)
    except Exception:
        logging.exception("LINE reply failed")


def show_line_loading_animation(chat_id: str, loading_seconds: int = 60) -> None:
    if not chat_id or not LINE_MESSAGING_CONFIGURATION:
        return
    try:
        with ApiClient(LINE_MESSAGING_CONFIGURATION) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.show_loading_animation(
                ShowLoadingAnimationRequest(
                    chat_id=chat_id,
                    loading_seconds=loading_seconds,
                )
            )
    except Exception:
        logging.exception("LINE loading animation failed")


# LINE credentials - read from environment if available (empty string fallback)
LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "").strip()
LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET", "").strip()
LINE_MESSAGING_CONFIGURATION = Configuration(access_token=LINE_ACCESS_TOKEN) if LINE_ACCESS_TOKEN else None

# LMStudio settings
LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
LLM_MODEL = "qwen3.5-4b"
LLM_CLIENT = OpenAI(base_url=LMSTUDIO_BASE_URL)
logging.info("Using LM Studio OpenAI SDK at %s with model %s", LMSTUDIO_BASE_URL, LLM_MODEL)

# 初始化核心引擎中的全域檢索與快取變數
engine.FAQ_RECORDS = engine.load_faq("db.csv")
engine.VECTOR_SEARCHER = engine.VectorSearcher(engine.FAQ_RECORDS, LLM_CLIENT)
engine.BM25_INDEX = engine.BM25Index(engine.FAQ_RECORDS) if engine.FAQ_RECORDS else None

DB_PATH = "sessions.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT, 
                role TEXT, 
                content TEXT, 
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS semantic_cache (
                query_hash TEXT PRIMARY KEY, 
                query TEXT, 
                embedding JSON, 
                response JSON, 
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

def get_session_history(session_id: str) -> List[Dict[str, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT role, content FROM sessions 
            WHERE session_id = ? 
            ORDER BY timestamp DESC LIMIT 10
        ''', (session_id,))
        rows = cursor.fetchall()
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

def save_session_message(session_id: str, role: str, content: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sessions (session_id, role, content) 
            VALUES (?, ?, ?)
        ''', (session_id, role, content))
        conn.commit()


def clear_session_history(session_id: str) -> None:
    if not session_id:
        return
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
        conn.commit()


def is_reset_command(message: str) -> bool:
    normalized = (message or "").strip().lower()
    return normalized == "/reset"

def process_message(message: str, session_id: Optional[str]) -> Dict:
    message = message.strip()
    if not message:
        return {"error": "Empty message"}
        
    history = []
    if session_id:
        history = get_session_history(session_id)
        
    # Contextualize Query
    if history:
        contextualized_query = engine.contextualize_query(message, history, LLM_CLIENT, LLM_MODEL)
    else:
        contextualized_query = message
        
    # Semantic Cache Logic Layer 1: Exact Match
    query_hash = hashlib.sha256(contextualized_query.encode("utf-8")).hexdigest()
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT response FROM semantic_cache WHERE query_hash = ?', (query_hash,))
        row = cursor.fetchone()
        if row:
            logging.info("Semantic Cache Layer 1 (Exact Match) hit for query: %s", contextualized_query)
            result = json.loads(row[0])
            if session_id:
                save_session_message(session_id, "user", message)
                save_session_message(session_id, "assistant", result.get("full_answer", ""))
            return result
            
        # Semantic Cache Layer 2: Semantic Match
        query_vecs = engine.get_embeddings([contextualized_query], LLM_CLIENT)
        query_vec = None
        if query_vecs:
            query_vec = query_vecs[0]
            cursor.execute('SELECT query_hash, embedding, response FROM semantic_cache')
            all_caches = cursor.fetchall()
            
            import torch
            from sentence_transformers import util
            query_tensor = torch.tensor(query_vec)
            
            best_sim = -1.0
            best_response = None
            for chash, cemb_str, cresp_str in all_caches:
                cemb = json.loads(cemb_str)
                cemb_tensor = torch.tensor(cemb)
                sim = util.cos_sim(query_tensor, cemb_tensor).item()
                if sim > best_sim:
                    best_sim = sim
                    best_response = cresp_str
            
            if best_sim >= 0.95 and best_response:
                logging.info("Semantic Cache Layer 2 (Semantic Match) hit with sim %.4f for query: %s", best_sim, contextualized_query)
                result = json.loads(best_response)
                if session_id:
                    save_session_message(session_id, "user", message)
                    save_session_message(session_id, "assistant", result.get("full_answer", ""))
                return result
                
    # Fallback to normal RAG if cache misses
    result = engine.answer_query(contextualized_query, engine.FAQ_RECORDS, LLM_CLIENT, LLM_MODEL)
    
    # Save to Cache & Session
    if session_id:
        save_session_message(session_id, "user", message)
        save_session_message(session_id, "assistant", result.get("full_answer", ""))
        
    if query_vec:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO semantic_cache (query_hash, query, embedding, response) 
                VALUES (?, ?, ?, ?)
            ''', (query_hash, contextualized_query, json.dumps(query_vec), json.dumps(result)))
            conn.commit()

    return result




@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")
    session_id = payload.get("session_id", "")
    result = process_message(message, session_id)
    return jsonify(result)

@app.route("/api/chat/clear", methods=["POST"])
def api_chat_clear():
    payload = request.get_json(silent=True) or {}
    session_id = payload.get("session_id")
    if session_id:
        clear_session_history(session_id)
    return jsonify({"status": "ok"})


@app.route("/api/faq/<record_id>", methods=["GET"])
def api_get_faq_detail(record_id):
    record = next((r for r in engine.FAQ_RECORDS if r.record_id == record_id), None)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return jsonify({
        "record_id": record.record_id,
        "category": record.category,
        "question": record.question,
        "answer": record.answer,
        "updated": record.updated
    })


@app.route("/api/faq/random", methods=["GET"])
def api_faq_random():
    try:
        limit = int(request.args.get("limit", 4))
    except ValueError:
        limit = 4
        
    # 隨機挑選長度在 8 到 35 字之間的常見問題，以確保展示在介面上的效果最佳
    valid_records = [
        r for r in engine.FAQ_RECORDS 
        if r.question and 8 <= len(r.question) <= 35
    ]
    if not valid_records:
        valid_records = engine.FAQ_RECORDS
        
    sampled = random.sample(valid_records, min(len(valid_records), limit))
    return jsonify([{
        "record_id": r.record_id,
        "category": r.category,
        "question": r.question
    } for r in sampled])


@app.route("/api/db/categories", methods=["GET"])
def api_db_categories():
    categories = sorted(list(set(r.category for r in engine.FAQ_RECORDS if r.category)))
    return jsonify(categories)


@app.route("/api/db/search", methods=["GET"])
def api_db_search():
    query = request.args.get("query", "").strip().lower()
    categories_raw = request.args.get("categories", "").strip()
    field = request.args.get("field", "all").strip().lower()
    
    try:
        page = int(request.args.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
        
    try:
        page_size = int(request.args.get("pageSize", 20))
        if page_size < 1:
            page_size = 20
    except ValueError:
        page_size = 20
    
    selected_categories = [c.strip() for c in categories_raw.split(",") if c.strip()]
    
    filtered = engine.FAQ_RECORDS
    if selected_categories:
        filtered = [r for r in filtered if r.category in selected_categories]
        
    if query:
        if field == "question":
            filtered = [r for r in filtered if query in r.question.lower()]
        elif field == "answer":
            filtered = [r for r in filtered if query in r.answer.lower()]
        else:
            filtered = [
                r for r in filtered
                if query in r.question.lower() or query in r.answer.lower()
            ]
        
    total_matches = len(filtered)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    results = filtered[start_idx:end_idx]
    
    return jsonify({
        "total": total_matches,
        "page": page,
        "pageSize": page_size,
        "results": [{
            "record_id": r.record_id,
            "category": r.category,
            "question": r.question,
            "updated": r.updated
        } for r in results]
    })


@app.route("/callback", methods=["POST"])
def webhook():
    body = request.get_data()
    signature = request.headers.get("x-line-signature", "")
    if not verify_line_signature(body, signature, LINE_SECRET):
        abort(400)

    payload = request.get_json(silent=True) or {}
    events = payload.get("events", [])

    for event in events:
        if event.get("type") != "message":
            continue
        message = event.get("message", {})
        if message.get("type") != "text":
            continue

        reply_token = event.get("replyToken")
        user_text = message.get("text", "")
        source = event.get("source", {})
        session_id = source.get("userId")

        if session_id and is_reset_command(user_text):
            clear_session_history(session_id)
            reply_line_message(reply_token, "已清除對話歷史，現在開始新對話。", LINE_ACCESS_TOKEN)
            continue

        if source.get("type") == "user" and session_id:
            show_line_loading_animation(session_id, 60)
        
        result = process_message(user_text, session_id)
        reply_line_message(reply_token, result.get("full_answer", ""), LINE_ACCESS_TOKEN)

    return "OK"


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
