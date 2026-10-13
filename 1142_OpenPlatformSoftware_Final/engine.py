import base64
import csv
import hashlib
import hmac
import json
import logging
import math
import os
import re
import sys
from datetime import datetime, timezone
from dataclasses import dataclass
from collections import Counter
from typing import Dict, List, Optional, Tuple, Union

import torch
import numpy as np
from openai import OpenAI
from pydantic import BaseModel
from sentence_transformers import CrossEncoder, util

# 全域 Reranker 實例
CROSS_ENCODER = None
try:
    from rapidfuzz import fuzz
except Exception:
    # Fallback using difflib when rapidfuzz isn't available.
    import difflib

    class _FuzzFallback:
        @staticmethod
        def WRatio(a: str, b: str) -> float:
            try:
                a = (a or "").lower()
                b = (b or "").lower()
                if not a or not b:
                    return 0.0
                return difflib.SequenceMatcher(None, a, b).ratio() * 100.0
            except Exception:
                return 0.0

        @staticmethod
        def token_set_ratio(a: str, b: str) -> float:
            try:
                a_tokens = sorted(set((a or "").lower().split()))
                b_tokens = sorted(set((b or "").lower().split()))
                a_join = " ".join(a_tokens)
                b_join = " ".join(b_tokens)
                return difflib.SequenceMatcher(None, a_join, b_join).ratio() * 100.0
            except Exception:
                return 0.0

        @staticmethod
        def partial_ratio(a: str, b: str) -> float:
            try:
                a = (a or "").lower()
                b = (b or "").lower()
                if len(a) == 0 or len(b) == 0:
                    return 0.0
                # approximate partial by comparing shorter to longer
                short, long = (a, b) if len(a) <= len(b) else (b, a)
                best = 0.0
                window = len(short)
                for i in range(0, len(long) - window + 1):
                    part = long[i : i + window]
                    best = max(best, difflib.SequenceMatcher(None, short, part).ratio())
                return best * 100.0
            except Exception:
                return 0.0

        @staticmethod
        def partial_token_sort_ratio(a: str, b: str) -> float:
            try:
                a_sorted = " ".join(sorted((a or "").lower().split()))
                b_sorted = " ".join(sorted((b or "").lower().split()))
                return _FuzzFallback.partial_ratio(a_sorted, b_sorted)
            except Exception:
                return 0.0

    fuzz = _FuzzFallback()

EMBEDDING_MODEL = "text-embedding-bge-m3"
DEBUG_CSV_PATH = os.getenv("DEBUG_CSV_PATH", "debug_candidates.csv").strip()

VECTOR_SEARCHER: Optional["VectorSearcher"] = None
BM25_INDEX: Optional["BM25Index"] = None
FAQ_RECORDS: List["FaqRecord"] = []


@dataclass
class FaqRecord:
    record_id: str
    category: str
    question: str
    answer: str
    updated: str
    search_text: str
    synonyms: str = ""


class KeywordOutput(BaseModel):
    primary_keywords: List[str]
    secondary_keywords: List[str]


class ScoreEntry(BaseModel):
    id: str
    reasoning: str
    score: float


class RerankOutput(BaseModel):
    scores: List[ScoreEntry]


class AlignmentOutput(BaseModel):
    reasoning_process: str
    is_concept_aligned: bool
    alignment_reason: str


class CoverageOutput(BaseModel):
    reasoning_process: str
    has_coverage: bool
    coverage_gap: str


class ContextualizeOutput(BaseModel):
    standalone_query: str

def contextualize_query(query: str, history: List[Dict[str, str]], client: Optional[OpenAI], model: str) -> str:
    if not client or not history:
        return query
    
    chat_history_str = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])
    
    system_instruction = """你是一個對話重寫助手。
任務：根據給定的對話歷史（Context）和使用者剛輸入的最新問題（Follow-up Input），將最新問題重寫為一個「獨立、完整且不依賴上下文就能理解」的問題。

限制：
- 不要回答該問題，只需要重寫問題。
- 如果最新問題本身已經很完整，不需要上下文即可理解，則逐字保留原問題。
- 保持問題原本的意圖與語言。"""

    user_prompt = f"對話歷史：\n{chat_history_str}\n\n最新問題：{query}\n\n獨立問題："
    
    res = llm_structured(
        client, model, user_prompt, ContextualizeOutput,
        system_instruction=system_instruction,
        max_output_tokens=128, temperature=0.0, log_tag="contextualize"
    )
    if res and res.standalone_query:
        logging.info("Contextualized Query: '%s' -> '%s'", query, res.standalone_query)
        return res.standalone_query
    return query


def normalize_text(text: str) -> str:
    text = text or ""
    text = text.strip().lower()
    return re.sub(r"\s+", " ", text)


def is_cjk(char: str) -> bool:
    code = ord(char)
    return (
        0x4E00 <= code <= 0x9FFF
        or 0x3400 <= code <= 0x4DBF
        or 0x20000 <= code <= 0x2A6DF
    )


def tokenize_bm25(text: str) -> List[str]:
    text = normalize_text(text)
    if not text:
        return []
    tokens = re.findall(r"[a-z0-9]+", text)
    # 找出所有連續的 CJK (中文) 片段，並在片段內部進行 Unigram 與 Bigram 斷詞
    cjk_pattern = r"[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df]+"
    cjk_chunks = re.findall(cjk_pattern, text)
    for chunk in cjk_chunks:
        # Unigram (單字)
        for char in chunk:
            tokens.append(char)
        # Bigram (雙字連詞)
        for i in range(len(chunk) - 1):
            tokens.append(chunk[i] + chunk[i + 1])
    return tokens





def load_faq(csv_path: str) -> List[FaqRecord]:
    records: List[FaqRecord] = []
    if not os.path.exists(csv_path):
        logging.warning("FAQ file missing: %s", csv_path)
        return records

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=1):
            category = (
                row.get("\u985e\u5225")
                or row.get("\u985e\u578b")
                or row.get("category")
                or ""
            ).strip()
            question = (
                row.get("\u984c\u76ee")
                or row.get("\u554f\u984c")
                or row.get("question")
                or ""
            ).strip()
            answer = (
                row.get("\u89e3\u7b54")
                or row.get("\u7b54\u6848")
                or row.get("answer")
                or ""
            ).strip()
            updated = (row.get("\u66f4\u65b0\u65e5\u671f") or row.get("updated") or "").strip()
            record_id = (row.get("\u9805\u6b21") or str(index)).strip()
            synonyms = (
                row.get("\u5ef6\u4f38\u554f\u984c")
                or row.get("synonyms")
                or ""
            ).strip()

            if not question or not answer:
                continue

            search_text = normalize_text(f"{question} {synonyms}" if synonyms else question)
            records.append(
                FaqRecord(
                    record_id=record_id,
                    category=category,
                    question=question,
                    answer=answer,
                    updated=updated,
                    search_text=search_text,
                    synonyms=synonyms,
                )
            )

    return records


def build_messages(system_instruction: str, user_prompt: str) -> List[Dict[str, str]]:
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})
    return messages


def get_message_text(response) -> str:
    if not response or not getattr(response, "choices", None):
        return ""
    message = response.choices[0].message
    return message.content or ""


def llm_structured(
    client: Optional[OpenAI],
    model: str,
    user_prompt: str,
    response_schema: type[BaseModel],
    *,
    system_instruction: Optional[str] = None,
    max_output_tokens: int = 512,
    temperature: float = 0.2,
    retries: int = 2,
    log_tag: str = "llm",
) -> Optional[BaseModel]:
    if not client:
        return None

    if system_instruction:
        full_system = f"{system_instruction.strip()}\n\n請注意：你同時也是一個專業的結構化輸出助手。請嚴格遵守提供的 Schema 格式進行輸出。"
    else:
        full_system = "你是一個專業的結構化輸出助手。請嚴格遵守提供的 Schema 格式進行輸出。"

    messages = build_messages(
        full_system,
        user_prompt,
    )
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "response_schema",
            "strict": True,
            "schema": response_schema.model_json_schema(),
        },
    }

    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature if attempt == 0 else 0.0,
                max_tokens=max_output_tokens,
                response_format=response_format,
                seed=42,
                user="default_user",
            )

            text = get_message_text(response)
            if not text:
                logging.warning("Structured output response empty (%s)", log_tag)
                continue
            try:
                cleaned_text = text.replace('\xa0', ' ').strip()
                parsed = response_schema.model_validate_json(cleaned_text)
                logging.info("LLM response (%s) parsed successfully", log_tag)
                return parsed
            except Exception:
                logging.exception("Structured output parsing failed (%s): %s", log_tag, text)

        except Exception:
            logging.exception("LLM request failed (attempt %d)", attempt + 1)
            continue

    logging.error("LLM failed to return valid structured output after retries")
    return None


def check_concept_alignment(query: str, best_record: FaqRecord, client: Optional[OpenAI], model: str) -> Tuple[bool, str]:
    if not client:
        return True, "無 LLM 預設切合"
    system_instruction = (
        """你是專利問答系統的「概念切合度守門員」(Agent 1)。
你的任務是核對 FAQ 條目是否在「核心概念與專利程序」上與用戶提問切合，防堵因檢索字面相似而導致的「關公戰張飛」錯誤（例如：用戶問「發明專利」，卻給出「新型專利」的答案）。

### 核心判斷原則（按優先級排序）

**原則 0 — 反誤殺優先（最高優先級）**：你的首要任務是避免 false negative（把正確的 FAQ 誤判為不切合）。只有在 FAQ 與用戶問題存在「不可調和的實質衝突」時，才能判定為不切合。若有疑慮，判定為切合。

**原則 1 — 寬容度原則**：如果 FAQ 的答案「正在回答」用戶的問題（無論答案是肯定、否定、還是有條件的），就必須判定為切合。FAQ 回答「不可以」「有條件可以」「需要注意某些限制」都是正確的回應方式。

**原則 2 — 雙向比對**：你不僅要看 FAQ 的「題目」，更要看 FAQ 的「答案」。有時候 FAQ 題目看起來相關，但答案中若明確寫出「本規定不適用於某某情況」，且用戶提問剛好屬於該被排除的情況，才能判定為不切合。

**原則 3 — 核心屬性核對**：僅在以下屬性發生「明確且不可調和的衝突」時判定不切合：
   - 專利類型衝突（用戶明確指定「發明」，FAQ 答案明確限定「僅新型」）
   - 關係人角色衝突（用戶問「申請人」，FAQ 答「代理人」的規定）
   - 程序類型衝突（用戶問「實體審查」，FAQ 答「形式審查」的規定）
**不屬於核心屬性衝突的情況**（禁止據此判定不切合）：
- 用戶假設「可以」但 FAQ 回答「不可以」（這是否定性回答，不是衝突）
- 用戶假設某方向（如紙本→電子），FAQ 回答相反方向（如僅電子→紙本）（這是限制性回答，不是衝突）
- FAQ 答案比用戶問題的涵蓋面更窄（這屬於覆蓋度問題，應由 Agent 2 判定）

### 常見誤判模式（以下情境必須判定為切合 true）
1. **有條件的答案 ≠ 不切合**：FAQ 回答「可以，但須滿足某條件」或「至少需一人相同」→ 切合。
2. **未指定類型 ≠ 不切合**：用戶未指定專利類型，FAQ 給出特定類型的通用答案 → 切合。
3. **適用範圍提醒 ≠ 不切合**：FAQ 末尾的「適用範圍提醒」是補充說明，不代表 FAQ 不適用於用戶的問題。
4. **絕對性提問 vs 條件式答案 ≠ 不切合**：用戶問「一定要嗎？」「每件都會嗎？」FAQ 答「不一定」「有例外」→ 正是正確回答 → 切合。
5. **否定性回答 ≠ 不切合**：FAQ 回答「不可以」「不行」正是對用戶問題的回答 → 切合。
6. **「不可以」即是回答 ≠ 不切合**：若用戶問「可以做 X 嗎？」，FAQ 回答「不可以做 X」、「有條件限制」或「僅限於 Y 情況」，這是對用戶問題最直接的回應 → 必須判定為切合。Agent 不應將「用戶預期與 FAQ 答案相反」解讀為衝突。常見觸發語境：「可以先填嗎？」→「不可以」、「可以退費嗎？」→「不可以」、「可以改回嗎？」→「不可以」。
7. **定義性提問的寬容**：若用戶詢問「什麼是X」或「X的申請資格」，只要 FAQ 內文有直接回答該定義或資格，即算切合。不可因為 FAQ 額外補充了其他資訊（如時程、例外）就認定未回應核心而誤判為不切合。
8. **嚴禁無中生有的腦補**：若用戶提問特定專有名詞（如「PPH」），請嚴格確認 FAQ 內文是否真的有針對該名詞給出指引。若 FAQ 完全未提及該名詞，且無法由通用概念合理推導，請勿自行腦補 FAQ 有涵蓋該名詞。

### 輸出規範 (Chain-of-Thought)
- `reasoning_process`：以 1-2 句話寫出你的比對分析（簡明扼要，控制在 100 字以內）。
- `is_concept_aligned`：判定是否切合 (true/false)。僅在存在不可調和的實質衝突時才設為 false。
- `alignment_reason`：若為 false，簡述哪裡發生實質衝突；若為 true，請以一句話 (30 字以內) 摘要該 FAQ 涵蓋了哪些核心概念，這將傳遞給後續的 Agent 作為對齊脈絡。"""
    )
    user_prompt = (
        f"用戶提問：{query}\n"
        f"FAQ 問題：{best_record.question}\n"
        f"FAQ 答案：{best_record.answer}"
    )
    res = llm_structured(client, model, user_prompt, AlignmentOutput, system_instruction=system_instruction, max_output_tokens=1024, temperature=0.0, log_tag="alignment")
    if res:
        logging.info("[Agent 1] Query: '%s' | Aligned: %s | Reason: %s", query, res.is_concept_aligned, res.alignment_reason)
        return res.is_concept_aligned, res.alignment_reason
    return True, "LLM 解析失敗，預設切合"


def check_coverage(query: str, best_record: FaqRecord, alignment_reason: str, client: Optional[OpenAI], model: str) -> Tuple[bool, str]:
    """判斷 reranker 選出的最佳 FAQ 條目，是否能單獨且完整地回答用戶的全部疑問。"""
    if not client:
        return True, ""  # 無 LLM 時保守預設：不觸發 RAG
    system_instruction = (
        """你是專利問答系統的「覆蓋判斷員」暨「RAG 守門員」(Agent 2)。
以下是系統檢索出最相關的單一 FAQ 條目。

**概念切合度前置 Context (Alignment Insights)：**
前置的概念守門員已判定本 FAQ 條目在以下核心領域與用戶提問完全切合：
『{alignment_reason}』

請您執行以下覆蓋度核對任務：
1. **信任核心對齊**：您無需重新審查上述已確認切合的核心概念。
2. **精準聚焦邊緣細節**：審核用戶問題，除了核心概念外，用戶是否還問了其他獨立子問題或實務邊界細節（例如：期限、特別文件、罰則或限制條件等）？
3. **口語修飾詞的寬容判定（防止誤判）**：若 FAQ 答案實質上已經涵蓋了該修飾詞所指向的實務資訊，就必須判定為完全覆蓋。例如：用戶問「最晚什麼時候」，FAQ 回「專利權期間內」，這已經涵蓋了時間資訊。

### 反過度推斷原則（必須嚴格遵守）
1. **口語修飾不構成獨立需求**：用戶改寫中的修飾語（如「具體」「到底」「在程序和文件上」「怎麼樣的」）不構成獨立的資訊需求。若 FAQ 已回答核心問題，不要因為這些口語修飾而判定未覆蓋。
2. **不要添加用戶沒問的問題**：只檢查 FAQ 是否回答了用戶「明確提出」的問題。不要要求 FAQ 額外回答用戶未問的延伸資訊（如費用、格式、期限、後續影響等）。
3. **同義改寫即為覆蓋**：若用戶的問題和 FAQ 的問題在核心語意上是同義改寫（只是措辭不同），直接判定 has_coverage=true。

### 輸出規範 (Chain-of-Thought)
- `reasoning_process`：以 1-2 句話寫出語意對比過程，對照 FAQ 解答是否無死角地涵蓋用戶所有次要細節（簡明扼要，控制在 100 字以內）。
- `has_coverage`：若無遺漏，判定為 true；若遺漏了關鍵細節，判定為 false。
- `coverage_gap`：若為 true，請留空或填寫 "None"；若為 false，請精確且簡短地條列「FAQ 缺漏了哪些具體資訊」，這將作為啟動 RAG 系統的救援指引。"""
    ).replace("{alignment_reason}", alignment_reason)
    
    user_prompt = (
        f"用戶提問：{query}\n"
        f"FAQ 問題：{best_record.question}\n"
        f"FAQ 答案：{best_record.answer}"
    )
    res = llm_structured(client, model, user_prompt, CoverageOutput, system_instruction=system_instruction, max_output_tokens=1024, temperature=0.0, log_tag="coverage")
    if res:
        logging.info("[Agent 2 Coverage CoT] Reasoning: %s | has_coverage: %s | gap: %s", 
                     res.reasoning_process, res.has_coverage, res.coverage_gap)
        return res.has_coverage, res.coverage_gap
    else:
        logging.info("[Agent 2 Coverage CoT] LLM returned empty response. Fallback to has_coverage = True")
        return True, ""


def get_embeddings(texts: List[str], client: Optional[OpenAI] = None, task_type: str = "") -> List[List[float]]:
    """
    取得文本的向量表示（embeddings）。
    說明：呼叫 LM Studio 的 embeddings 接口，忽略 task_type 參數。
    """
    if not texts:
        return []
    if not client:
        logging.warning("Embeddings client not available")
        return []
    try:
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
        return [item.embedding for item in response.data]
    except Exception:
        logging.exception("Failed to get embeddings from LM Studio")
        return []


def answer_from_general_knowledge(query: str, client: Optional[OpenAI], model: str) -> str:
    if not client:
        return "無法回答：未配置 LLM 客戶端。"

    system_instruction = """你是一位嚴謹且專業的智慧財產權與專利實務專家。
當系統無法在官方常見問答庫中找到完全對應的資料時，你的任務是基於通用的專利法理與實務知識，為用戶提供方向性的解答。請根據您的通用專利知識回答實務問題。請提供詳細的說明與指引，並給予實質的專業建議。

### 答覆原則與護欄（極重要）
1. **免責聲明破題**：必須在回答的第一段明確告知用戶：「目前在常見問答庫中未檢索到針對您問題的特定說明，以下依據通用專利實務為您做初步解答：」（或類似語意），讓用戶清楚這不是官方標準答案。
2. **嚴禁捏造具體數據**：絕不可憑空捏造台灣智慧財產局 (TIPO) 的「精確規費金額」或「法定期限天數」。若回答涉及這些細節，請說明通用的實務原則，並強烈建議用戶「至經濟部智慧財產局官網查詢最新規定或致電確認」。
3. **提供實質但安全的建議**：給予具體可行的實務步驟與指引，但語氣必須保持客觀，避免提供具法律絕對約束力的背書。

### 排版與輸出規範
1. 一律使用繁體中文回答。
2. 嚴禁使用 Markdown 的標題語法（如 #, ##, ### 等），以免干擾系統前端的字體渲染。
3. 必須使用一般文字段落，並強烈建議搭配粗體 (**) 來標示關鍵字，以及條列式符號 (-) 來進行步驟說明，確保內容清晰易讀。"""

    user_prompt = f"用戶提問：{query}"
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=build_messages(
                system_instruction,
                user_prompt,
            ),
            temperature=0.7,
            max_tokens=1024,
            seed=42,
            user="default_user",
        )
        text = get_message_text(response)
        return text or "LLM 未能生成有效回答。"
    except Exception:
        logging.exception("Failed to get general knowledge answer")
        return "獲取通用知識回答時發生異常錯誤。"


def synthesize_answer_from_vector(
    query: str,
    top_candidates: List[Tuple[FaqRecord, float]],
    alignment_reason: str,
    coverage_gap: str,
    client: Optional[OpenAI],
    model: str,
) -> Tuple[str, List[str]]:
    if not client:
        return "無法回答：未配置 LLM 客戶端。", [rec.record_id for rec, _ in top_candidates]

    # 建立向量檢索的上下文內容
    context_parts = []
    for idx, (rec, score) in enumerate(top_candidates, start=1):
        context_parts.append(
            f"檢索到的 FAQ 條目 {idx} (相似度分數: {score:.4f})\n"
            f"條目ID: {rec.record_id}\n"
            f"類別: {rec.category}\n"
            f"問題: {rec.question}\n"
            f"答案: {rec.answer}\n"
        )
    context = "\n---\n".join(context_parts)

    system_instruction = ("""你是一位嚴謹、專業的智慧財產局專利諮詢專家。
你的任務是基於提供的 FAQ 檢索庫，提煉核心實務資訊來解答用戶提問。嚴禁編造任何未提及的規費、期限或法律效力。

### 答覆原則與結構
1. **直接破題**：不要使用「您好」、「很高興為您服務」等冗長開場白，第一句話直接給出核心結論。
2. **排版清晰**：善用 Markdown 的條列式符號 (-) 或粗體 (**) 來標示關鍵的「程序」、「期限」與「規費」，使內容易於掃視。
3. **邊界提醒**：若檢索結果與用戶問題的專利類型（如發明 vs 新型）有落差，必須在回答中明確標示本回答的適用範圍。

### 引用格式規範（極重要，嚴格遵守）
1. 當你的文字引用了 FAQ 內容時，必須在該段或該句結尾加上引用標記 [#ID]（ID 為條目的 record_id）。
2. 禁止使用非標準格式。不合格範例：[FAQ 2]、[2]。正確範例：應檢附委任書[#2]。
3. 若綜合了多個條目，請合併標示，例如 [#2][#261]。若同一段落反覆引用同一條目，僅需在段落結尾標示一次即可。

### 前置防錯與澄清洞察
前置審查 Agent 可能會提供概念對齊狀態與尚未覆蓋之缺口（見用戶輸入）。
**缺口處理動作**：請優先在提供的 FAQ 內容中尋找「尚未覆蓋之缺口」的答案並精確補足。若提供的 FAQ 內容中完全找不到該缺口的解答，請務必在回答中說明無法回答的原因（例如誠實聲明目前常見問答未有明確說明），切勿強行編造。

### 資訊衝突處理
若檢索到的多個 FAQ 條目在規費、期限等實務資訊上有互相衝突，請完整並陳兩者的說法，並建議用戶直接向智慧財產局確認，不得擅自決定何者為準。""")

    user_prompt = (
        f"用戶提問：{query}\n\n"
        f"### 前置審查資訊\n"
        f"概念對齊狀態：{alignment_reason}\n"
        f"尚未覆蓋之缺口：{coverage_gap}\n\n"
        f"### 檢索到的 FAQ 參考內容如下：\n"
        f"{context}\n"
    )

    candidate_ids = [rec.record_id for rec, _ in top_candidates]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=build_messages(system_instruction, user_prompt),
            temperature=0.2,
            max_tokens=2048,
            seed=42,
            user="default_user",
        )
        text = get_message_text(response)
        if not text:
            return "LLM 未能成功合成解答。", candidate_ids

        # 1. 抓取引用的 ID 標記 [#ID]
        raw_ids = re.findall(r'\[#\s*(\w+)\]', text)
        if not raw_ids:
            raw_ids = re.findall(r'\[(?:FAQ|條目|蝚)?\s*#?\s*(\w+)\]', text)

        used_ids = []
        for r_id in raw_ids:
            r_id = r_id.strip()
            if r_id and r_id not in used_ids:
                used_ids.append(r_id)

        # 過濾以確保引用 ID 在候選名單中
        used_ids = [uid for uid in used_ids if uid in candidate_ids]

        if not used_ids:
            logging.warning("[RAG] No valid citation tags found in LLM response. Fallback to all candidates.")
            used_ids = candidate_ids

        # 標準化回答中的引用標籤為 [#ID] 格式，供前端替換為行內按鈕
        clean_text = re.sub(r'\s*\[(?:FAQ|條目|蝚)?\s*#?\s*(\w+)\]', r' [#\1]', text)
        return clean_text, used_ids
    except Exception:
        logging.exception("Failed to synthesize answer from vector context")
        return "合成解答時發生錯誤。", candidate_ids


class VectorSearcher:
    def __init__(self, records: List[FaqRecord], client: Optional[OpenAI], cache_path: str = "faq_embeddings_contextual.json"):
        self.records = records
        self.client = client
        self.cache_path = cache_path
        self.embeddings: Dict[str, List[float]] = {}
        if client and records:
            self._load_or_build_cache()

    def _load_or_build_cache(self):
        # 檢查快取檔案是否存在
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)
                
                # 檢查快取資料格式是否正確，並比對模型名稱是否一致
                if isinstance(cache_data, dict) and "model_name" in cache_data:
                    if cache_data.get("model_name") == EMBEDDING_MODEL:
                        self.embeddings = cache_data.get("embeddings", {})
                        # 檢查是否所有必要的 record_id_q 與 record_id_s 都已經有快取向量
                        all_cached = True
                        for r in self.records:
                            q_key = f"{r.record_id}_q"
                            s_key = f"{r.record_id}_s"
                            if q_key not in self.embeddings:
                                all_cached = False
                                break
                            if getattr(r, "synonyms", None) and s_key not in self.embeddings:
                                all_cached = False
                                break
                        if all_cached:
                            logging.info("Loaded FAQ embeddings from cache (%s).", EMBEDDING_MODEL)
                            return
                
                logging.warning("Cache version mismatch or incomplete. Rebuilding...")
            except Exception:
                logging.exception("Failed to load embeddings cache")

        logging.info("Building FAQ embeddings cache using %s...", EMBEDDING_MODEL)
        
        # [Embedding 設計標記 - 多向量最大相似度設計 (Multi-Vector Max Similarity)]
        # 為了提升檢索精準度，我們並未將「原始題目」與「延伸問題」（同義問句）直接字串拼接（避免前綴稀釋效應拉低相似度）。
        # 由於資料庫中約有 28.3% (202/713 筆) 的 FAQ 包含延伸問題，且長度廣泛分布（涵蓋極短句到長句，5 至 33+ 字不等），
        # 這些延伸問題提供了多樣的法律術語與正式表達方式。
        # 因此，我們將「原始題目」與「延伸問題」作為兩個獨立向量進行 Embedding 編碼，
        # 檢索時分別計算兩者與使用者提問的餘弦相似度，並取其最大值 (MAX) 作為該 FAQ 的向量分數。
        keys_to_embed = []
        texts_to_embed = []
        for r in self.records:
            keys_to_embed.append(f"{r.record_id}_q")
            texts_to_embed.append(f"[{r.category}] {r.question}")
            if getattr(r, "synonyms", None):
                keys_to_embed.append(f"{r.record_id}_s")
                texts_to_embed.append(f"[{r.category}] {r.synonyms}")

        all_values = get_embeddings(texts_to_embed, self.client)

        if len(all_values) == len(keys_to_embed):
            self.embeddings = {k: v for k, v in zip(keys_to_embed, all_values)}
            try:
                # 快取資料寫入檔案以供後續使用
                cache_to_save = {
                    "model_name": EMBEDDING_MODEL,
                    "embeddings": self.embeddings
                }

                with open(self.cache_path, "w", encoding="utf-8") as f:
                    json.dump(cache_to_save, f)
                logging.info("Saved FAQ embeddings to cache.")
            except Exception:
                logging.exception("Failed to save embeddings cache")

    def search(self, query: str) -> Optional[Tuple[FaqRecord, float]]:
        if not self.embeddings:
            return None

        query_vecs = get_embeddings([query], self.client)
        if not query_vecs:
            return None
        query_vec = query_vecs[0]

        query_vec_tensor = torch.tensor(query_vec)
        
        best_record = None
        best_score = -1.0

        for record in self.records:
            q_key = f"{record.record_id}_q"
            s_key = f"{record.record_id}_s"
            
            score_q = -1.0
            score_s = -1.0
            
            if q_key in self.embeddings:
                vec_q = torch.tensor(self.embeddings[q_key])
                score_q = util.cos_sim(query_vec_tensor, vec_q).item()
                
            if getattr(record, "synonyms", None) and s_key in self.embeddings:
                vec_s = torch.tensor(self.embeddings[s_key])
                score_s = util.cos_sim(query_vec_tensor, vec_s).item()
                
            score = max(score_q, score_s)

            if score > best_score:
                best_score = float(score)
                best_record = record

        return (best_record, best_score) if best_record else None

    def search_top_k(self, query: str, top_k: int = 3) -> List[Tuple[FaqRecord, float]]:
        if not self.embeddings:
            return []

        query_vecs = get_embeddings([query], self.client)
        if not query_vecs:
            return []
        query_vec = query_vecs[0]

        query_vec_tensor = torch.tensor(query_vec)
        
        results = []
        for record in self.records:
            q_key = f"{record.record_id}_q"
            s_key = f"{record.record_id}_s"
            
            score_q = -1.0
            score_s = -1.0
            
            if q_key in self.embeddings:
                vec_q = torch.tensor(self.embeddings[q_key])
                score_q = util.cos_sim(query_vec_tensor, vec_q).item()
                
            if getattr(record, "synonyms", None) and s_key in self.embeddings:
                vec_s = torch.tensor(self.embeddings[s_key])
                score_s = util.cos_sim(query_vec_tensor, vec_s).item()
                
            best_score = max(score_q, score_s)
            results.append((record, float(best_score)))

        results.sort(key=lambda item: item[1], reverse=True)
        return results[:top_k]


class BM25Index:
    def __init__(self, records: List[FaqRecord], k1: float = 1.5, b: float = 0.75):
        self.records = records
        self.k1 = k1
        self.b = b
        self.record_ids = [r.record_id for r in records]
        self.doc_count = len(records)
        self.doc_len: Dict[str, int] = {}
        self.term_freqs: Dict[str, Counter] = {}
        self.doc_freq: Dict[str, int] = {}
        self.avgdl = 0.0
        self._build()

    def matches(self, records: List[FaqRecord]) -> bool:
        if len(records) != len(self.record_ids):
            return False
        return self.record_ids == [r.record_id for r in records]

    def _build(self) -> None:
        total_len = 0
        for record in self.records:
            # 合併題目與延伸問題以建立更健壯的 BM25 詞彙索引
            text_to_tokenize = f"[{record.category}] {record.question}"
            if getattr(record, "synonyms", None):
                text_to_tokenize = f"[{record.category}] {record.question} {record.synonyms}"
            tokens = tokenize_bm25(text_to_tokenize)
            freq = Counter(tokens)
            self.term_freqs[record.record_id] = freq
            doc_len = sum(freq.values())
            self.doc_len[record.record_id] = doc_len
            total_len += doc_len
            for term in freq.keys():
                self.doc_freq[term] = self.doc_freq.get(term, 0) + 1

        self.avgdl = total_len / max(self.doc_count, 1)

    def score(self, query: str) -> Dict[str, float]:
        tokens = tokenize_bm25(query)
        if not tokens or self.doc_count == 0:
            return {}

        query_terms = Counter(tokens)
        scores: Dict[str, float] = {}
        avgdl = self.avgdl or 1.0

        for record_id, tf in self.term_freqs.items():
            dl = self.doc_len.get(record_id, 0)
            score = 0.0
            for term in query_terms.keys():
                df = self.doc_freq.get(term, 0)
                if df == 0:
                    continue
                idf = math.log(1.0 + (self.doc_count - df + 0.5) / (df + 0.5))
                freq = tf.get(term, 0)
                if freq == 0:
                    continue
                denom = freq + self.k1 * (1.0 - self.b + self.b * dl / avgdl)
                score += idf * (freq * (self.k1 + 1.0) / denom)

            if score > 0.0:
                scores[record_id] = score

        return scores


def fuzzy_similarity(text_a: str, text_b: str) -> float:
    if not text_a or not text_b:
        return 0.0
    return (
        0.3 * fuzz.WRatio(text_a, text_b)
        + 0.25 * fuzz.token_set_ratio(text_a, text_b)
        + 0.15 * fuzz.partial_ratio(text_a, text_b)
        + 0.3 * fuzz.partial_token_sort_ratio(text_a, text_b)
    )


def keyword_similarity(keywords: List[str], text: str) -> float:
    if not keywords:
        return 0.0
    scores = [fuzz.WRatio(keyword, text) for keyword in keywords if keyword]
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def keyword_hit_count(keywords: List[str], text: str) -> int:
    if not keywords:
        return 0
    hits = 0
    for keyword in keywords:
        if keyword and keyword in text:
            hits += 1
    return min(hits, 10)


def normalize_keywords(keywords: List[str]) -> List[str]:
    cleaned: List[str] = []
    for keyword in keywords:
        if not isinstance(keyword, str):
            continue
        normalized = normalize_text(keyword)
        if normalized:
            cleaned.append(normalized)
    return cleaned


def extract_keywords(
    query: str,
    client: Optional[OpenAI],
    model: str,
) -> Tuple[List[str], List[str], bool]:
    system_instruction = """你是一個來自經濟部智慧財產局(簡稱智慧局)、專門處理繁體中文專利 FAQ 系統的關鍵字提取專家。
你的任務是分析用戶查詢，提取核心專利實務概念，以供資料庫進行精確比對。

## 背景知識：專利基本術語
- 審查方案與管道：PPH (專利審查高速公路)、AEP (專利事由加速審查)、TW-SUPA、一般審查。
- 專利類型：發明專利、新型專利、設計專利。
- 申請主體與關係人：申請人、發明人、代理人、專利代理人、專利師、自然人、法人。
- 規費與程序：申請規費、年費、減免、退費、委任書。
- 文件與審查：說明書、申請書、摘要、圖式、實體審查、新型技術報告、補正、申復、答辯、面詢、優先權、分割。

## 關鍵字提取規則
1. Primary Keywords (主要關鍵字)：核心專利術語、類型與程序名稱（如：發明專利、規費減免、實體審查、AEP）。此類別需具備高度檢索區分度。
2. Secondary Keywords (次要關鍵字)：輔助說明屬性、時間或補充概念（如：期限、外文、金額、應檢附文件）。
3. 嚴格過濾無意義詞彙：絕對禁止提取「請問、我想知道、有沒有、是不是、可以嗎、怎麼辦、該如何、為什麼、何謂、什麼是」等口語問句或助詞。
4. 術語正規化 (同義轉換)：將口語詞彙精確對應至正式專利術語。
   - 機構稱呼轉換：若提及「你們」、「貴局」，請提取為「本局」；若提及「智慧財產局」，請提取為「智慧局」。
   - 「加速審查/快速審查」 -> 提取為「AEP」或「PPH」。
   - 「改名字/換人」 -> 依據上下文判斷，提取為「變更申請人」、「變更發明人」或「變更代理人」。
   - 「省錢/變便宜」 -> 提取為「規費減免」。

## 輸出格式規範
- 每一類關鍵字最多提取 5 個。
- 僅能輸出純 JSON 格式，嚴禁使用 Markdown 標記（如 ```json）、嚴禁加入任何解釋性文字。
- 必須嚴格符合以下 JSON 結構：
{"primary_keywords": ["詞1", "詞2"], "secondary_keywords": ["詞3", "詞4"]}

## 提取範例

【範例 1：定義型問題】
用戶提問：新型專利具體的法律定義到底是什麼？
預期輸出：{"primary_keywords": ["新型專利"], "secondary_keywords": ["定義", "法律"]}

【範例 2：時間型問題】
用戶提問：專利權人可以在什麼時候向智慧局申請專利權更正？
預期輸出：{"primary_keywords": ["專利權更正"], "secondary_keywords": ["時間", "申請", "何時"]}

【範例 3：口語與術語正規化】
用戶提問：如果不找人代辦，自己辦理發明專利，規費會不會比較便宜？
預期輸出：{"primary_keywords": ["發明專利", "規費減免"], "secondary_keywords": ["自辦", "規費"]}

【範例 4：機構稱呼正規化】
用戶提問：請問你們的地址在哪裡？
預期輸出：{"primary_keywords": ["本局", "地址"], "secondary_keywords": ["在哪裡"]} """

    user_prompt = f"用戶提問：{query}\n"

    data = llm_structured(
        client,
        model,
        user_prompt,
        KeywordOutput,
        system_instruction=system_instruction,
        max_output_tokens=512,
        temperature=0,
        log_tag="keywords",
    )
    if not data:
        return [], [], False

    primary = normalize_keywords(data.primary_keywords)[:5]
    secondary = normalize_keywords(data.secondary_keywords)[:5]
    has_keywords = bool(primary or secondary)
    return primary, secondary, has_keywords


def rerank_candidates(
    query: str,
    candidates: List[Dict],
    client: Optional[OpenAI],
    model: str,
) -> Optional[Dict[str, float]]:
    if not candidates:
        return None

    global CROSS_ENCODER
    if CROSS_ENCODER is None:
        logging.info("Initializing CrossEncoder 'BAAI/bge-reranker-v2-m3' locally...")
        try:
            # 預設 bge-reranker-v2-m3 支援最高 8192 tokens，但考量 VRAM 消耗，我們設定 1024 通常已足夠涵蓋所有 FAQ 內容。
            CROSS_ENCODER = CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=1024)
        except Exception as e:
            logging.exception("Failed to initialize CrossEncoder: %s", e)
            return None

    logging.info("Reranking %d candidates for query: %s", len(candidates), query)

    texts = [[query, item["record"].question + "\n" + item["record"].answer] for item in candidates]
    
    try:
        # 由於 top-k=12，為避免 1024 長度下的 OOM，設定 batch_size=1 分批推論
        raw_scores = CROSS_ENCODER.predict(texts, batch_size=1)
        if isinstance(raw_scores, float):
            raw_scores = [raw_scores]
        # numpy array => list
        if hasattr(raw_scores, "tolist"):
            raw_scores = raw_scores.tolist()
    except Exception as e:
        logging.exception("CrossEncoder predict failed: %s", e)
        return None

    scores = {}
    for idx, raw_score in enumerate(raw_scores):
        # BGE Reranker 回傳 logit，需進行 sigmoid 轉換映射至 0-100
        prob = 1.0 / (1.0 + math.exp(-raw_score))
        mapped_score = prob * 100.0
        scores[candidates[idx]["record"].record_id] = max(0.0, min(100.0, mapped_score))

    return scores


def compute_candidates(
    query: str,
    records: List[FaqRecord],
    client: Optional[OpenAI],
    model: str,
) -> Tuple[List[Dict], List[str], List[str]]:
    query_norm = normalize_text(query)
    global BM25_INDEX
    bm25_scores: Dict[str, float] = {}
    bm25_ranks: Dict[str, int] = {}
    bm25_rank_scores: Dict[str, float] = {}
    if records:
        if BM25_INDEX is None or not BM25_INDEX.matches(records):
            BM25_INDEX = BM25Index(records)
        bm25_scores = BM25_INDEX.score(query)
        if bm25_scores:
            # 只有當 BM25 原始分數顯著大於等於 0.5 時，才列入排名計算，過濾低分噪聲
            valid_scores = {rid: sc for rid, sc in bm25_scores.items() if sc >= 0.5}
            if valid_scores:
                sorted_bm25 = sorted(valid_scores.items(), key=lambda item: item[1], reverse=True)
                rank_scale = max(len(sorted_bm25) - 1, 1)
                for rank, (record_id, score) in enumerate(sorted_bm25, start=1):
                    bm25_ranks[record_id] = rank
                    bm25_rank_scores[record_id] = 100.0 - (rank - 1) * (100.0 / rank_scale)
    primary_keywords, secondary_keywords, keyword_ready = extract_keywords(query, client, model)
    all_keywords = primary_keywords + secondary_keywords

    # 計算向量檢索相似度 (使用多向量最大相似度設計)
    vector_scores: Dict[str, float] = {}
    vector_ranks: Dict[str, int] = {}
    if VECTOR_SEARCHER and VECTOR_SEARCHER.embeddings:
        query_vecs = get_embeddings([query], client)
        if query_vecs:
            query_vec_tensor = torch.tensor(query_vecs[0])
            for record in records:
                q_key = f"{record.record_id}_q"
                s_key = f"{record.record_id}_s"
                
                score_q = -1.0
                score_s = -1.0
                
                if q_key in VECTOR_SEARCHER.embeddings:
                    vec_tensor = torch.tensor(VECTOR_SEARCHER.embeddings[q_key])
                    score_q = util.cos_sim(query_vec_tensor, vec_tensor).item()
                    
                if getattr(record, "synonyms", None) and s_key in VECTOR_SEARCHER.embeddings:
                    vec_tensor_s = torch.tensor(VECTOR_SEARCHER.embeddings[s_key])
                    score_s = util.cos_sim(query_vec_tensor, vec_tensor_s).item()
                    
                best_score = max(score_q, score_s)
                vector_scores[record.record_id] = float(best_score) * 100.0
                
            if vector_scores:
                sorted_vec = sorted(vector_scores.items(), key=lambda item: item[1], reverse=True)
                for rank, (record_id, score) in enumerate(sorted_vec, start=1):
                    vector_ranks[record_id] = rank

    candidates: List[Dict] = []
    for record in records:
        base_text = normalize_text(record.question)
        base_score = fuzzy_similarity(query_norm, base_text)
        if getattr(record, "synonyms", None):
            # 對於延伸同義問題，計算 query 與每個同義句的 fuzzy ratio，取最大值以防止短題目被嚴重壓分
            synonym_list = [s.strip() for s in record.synonyms.split("；") if s.strip()]
            for syn in synonym_list:
                syn_score = fuzzy_similarity(query_norm, normalize_text(syn))
                if syn_score > base_score:
                    base_score = syn_score
        vec_score = vector_scores.get(record.record_id, 0.0)
        vec_rank = vector_ranks.get(record.record_id, 1000)
        bm25_score = bm25_scores.get(record.record_id, 0.0)
        bm25_rank = bm25_ranks.get(record.record_id, 1000)
        bm25_rank_score = bm25_rank_scores.get(record.record_id, 0.0)
        
        rrf_score = 0.0
        if vec_score > 0 or bm25_score > 0:
            rrf_score = (1.0 / (60.0 + vec_rank)) + (1.0 / (60.0 + bm25_rank))
        rrf_normalized = (rrf_score / 0.03278688) * 100.0

        # 長度與字元重疊補償 (Length & Character Overlap Compensation)
        # 較短的 FAQ 題目在口語改寫後容易被更長的相關 FAQ 壓過，給予漸進式補償。
        # Tier 1 (≤6 字)：原始高補償，解決極短關鍵字匹配問題。
        # Tier 2 (7-15 字)：中等補償，解決短題目被長題目壓過的問題。
        q_len = len(record.question)
        length_compensation = 0.0
        if q_len <= 15:
            q_chars = set(c for c in query if c.isalnum())
            faq_chars = set(c for c in record.question if c.isalnum())
            if faq_chars:
                overlap_ratio = len(faq_chars & q_chars) / len(faq_chars)
                if q_len <= 6 and overlap_ratio >= 0.5:
                    length_compensation = (8.0 - q_len) * 1.5
                elif overlap_ratio >= 0.6:
                    length_compensation = max(0.0, (16.0 - q_len) * 0.8)

        if keyword_ready:
            primary_score = keyword_similarity(primary_keywords, record.search_text)
            secondary_score = keyword_similarity(secondary_keywords, record.search_text)
            hit_count = keyword_hit_count(all_keywords, record.search_text)
            
            # 主要關鍵字在題目中的精確命中次數加成 (Primary Keyword Exact Hits Boost)
            primary_exact_hits = sum(1 for kw in primary_keywords if kw and kw in record.question)
            
            # [NEW] 主要關鍵字在答案中的精確命中加分 (Answer Keyword Hit Bonus)
            # 用途：LLM 萃取的關鍵字常為「答案特徵」（如問專利種類→提取出發明/新型/設計），
            # 這些詞在短題目中不存在，但在正確 FAQ 的答案中會出現。
            # 限制：僅計算 primary_keywords，且以低權重 (1.5) 加入，避免通用詞過度加分。
            answer_hit_bonus = sum(
                1 for kw in primary_keywords
                if kw and kw not in record.question and kw in record.answer
            ) * 1.5
            
            # 計算綜合檢索評分 (RRF + Heuristics)
            # 註：額外加上 0.10 * bm25_rank_score 是為了補償 RRF 非線性倒數排名 (1/(60+rank)) 抹平前幾名分數差距的副作用，
            # 保障當專利關鍵字「字面精確命中 (Exact Match)」時，BM25 絕對第一名的線性分數優勢能被保留，防止被語意擦邊球壓過。
            total_score = (
                0.20 * rrf_normalized
                + 0.50 * vec_score
                + 0.25 * base_score
                + 0.10 * bm25_rank_score
                + 0.25 * primary_score
                + 0.05 * secondary_score
                + hit_count
                + (primary_exact_hits * 3.0)
                + answer_hit_bonus
                + length_compensation
            )
        else:
            primary_score = None
            secondary_score = None
            hit_count = None
            answer_hit_bonus = 0.0
            # 額外加上 0.10 * bm25_rank_score 以補償 RRF 抹平前幾名名次差距的副作用，保留字面精準命中的線性優勢
            total_score = 0.20 * rrf_normalized + 0.50 * vec_score + 0.25 * base_score + 0.10 * bm25_rank_score + length_compensation

        candidates.append(
            {
                "record": record,
                "base_score": base_score,
                "vector_score": vec_score,
                "bm25_score": bm25_score,
                "bm25_rank": bm25_rank,
                "bm25_rank_score": bm25_rank_score,
                "primary_score": primary_score,
                "secondary_score": secondary_score,
                "hit_count": hit_count,
                "answer_hit_bonus": answer_hit_bonus,
                "total_score": total_score,
                "keyword_ready": keyword_ready,
                "length_compensation": length_compensation,
            }
        )

    candidates.sort(key=lambda item: item["total_score"], reverse=True)
    return candidates, primary_keywords, secondary_keywords


def format_answer(record: FaqRecord, low_confidence: bool) -> str:
    lines = [
        f"Category: {record.category}",
        f"Question: {record.question}",
        "",
        record.answer,
    ]
    return "\n".join(lines).strip()


def build_debug_rows(
    query: str,
    candidates: List[Dict],
    best_id: str,
    llm_scores: Optional[Dict[str, float]],
    primary_keywords: List[str],
    secondary_keywords: List[str],
) -> List[Dict]:
    timestamp = datetime.now(timezone.utc).isoformat()
    rows: List[Dict] = []

    def format_score(value: Optional[float]) -> Union[str, float]:
        if value is None:
            return ""
        return round(value, 4)

    def format_keywords(values: List[str]) -> str:
        if not values:
            return ""
        return ", ".join(values)

    primary_text = format_keywords(primary_keywords)
    secondary_text = format_keywords(secondary_keywords)

    for rank, item in enumerate(candidates, start=1):
        record = item["record"]
        llm_score = ""
        if llm_scores and record.record_id in llm_scores:
            llm_score = round(llm_scores[record.record_id], 4)
        rows.append(
            {
                "timestamp": timestamp,
                "query": query,
                "stage": "final",
                "rank": rank,
                "record_id": record.record_id,
                "category": record.category,
                "question": record.question,
                "primary_keywords": primary_text,
                "secondary_keywords": secondary_text,
                "base_score": round(item.get("base_score", 0.0), 4) if item.get("base_score") is not None else "",
                "vector_score": round(item.get("vector_score", 0.0), 4) if item.get("vector_score") is not None else "",
                "primary_score": format_score(item.get("primary_score")),
                "secondary_score": format_score(item.get("secondary_score")),
                "hit_count": "" if item.get("hit_count") is None else item.get("hit_count"),
                "total_score": round(item.get("total_score", 0.0), 4),
                "llm_score": llm_score,
                "final_score": round(item.get("final_score", 0.0), 4),
                "selected": "yes" if record.record_id == best_id else "",
            }
        )

    return rows


def append_debug_rows(rows: List[Dict], csv_path: str) -> None:
    if not rows or not csv_path:
        return

    columns = [
        "timestamp",
        "query",
        "stage",
        "rank",
        "record_id",
        "category",
        "question",
        "primary_keywords",
        "secondary_keywords",
        "base_score",
        "vector_score",
        "primary_score",
        "secondary_score",
        "hit_count",
        "total_score",
        "llm_score",
        "final_score",
        "selected",
    ]

    directory = os.path.dirname(csv_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in columns})


def answer_query(
    query: str,
    records: List[FaqRecord],
    client: Optional[OpenAI],
    model: str,
) -> Dict:
    # 說明：低置信度閾值 (60.0) 是結合檢索相似度與 LLM 評估分數的綜合評定基準。
    # 若綜合評分低於此值，則代表檢索結果不夠精確，系統將啟動 RAG 或通用知識回答機制。
    low_confidence_threshold = 60.0
    top_k = 12
    score_gap_threshold = 8.0

    # 初始化除錯輸出參數
    exact_match = "N/A"
    fuzzy_match = "N/A"
    semantic_match = "N/A"
    bm25_match = "N/A"
    score_gap_ok = "N/A"
    is_aligned = "N/A"
    primary_keywords_str = "N/A"
    secondary_keywords_str = "N/A"
    top2_question = "N/A"
    top2_score = "N/A"
    has_coverage_val = "N/A"
    candidates_debug = []

    if query:
        # 清除查詢字串中的不間斷空格 (\xa0) 與全形空格 (\u3000)，以避免影響 LLM 解析與 JSON 輸出格式。
        query = query.replace('\xa0', ' ').replace('\u3000', ' ').strip()

    if not query or not query.strip():
        return {
            "answer": "Please enter a question.",
            "full_answer": "Please enter a question.",
            "category": "",
            "question": "",
            "score": 0.0,
            "low_confidence": True,
            "response_type": "standard",
            "alignment_reason": "N/A (Empty Query)",
            "coverage_reason": "N/A (Empty Query)",
            "bm25_match": "N/A",
            "is_aligned": "N/A",
        }

    if not records:
        return {
            "answer": "FAQ data not available.",
            "full_answer": "FAQ data not available.",
            "category": "",
            "question": "",
            "score": 0.0,
            "low_confidence": True,
            "response_type": "standard",
            "alignment_reason": "N/A (No Data)",
            "coverage_reason": "N/A (No Data)",
            "bm25_match": "N/A",
            "is_aligned": "N/A",
        }

    candidates, primary_keywords, secondary_keywords = compute_candidates(
        query,
        records,
        client,
        model,
    )

    if candidates:
        if primary_keywords:
            primary_keywords_str = ", ".join(primary_keywords)
        if secondary_keywords:
            secondary_keywords_str = ", ".join(secondary_keywords)
        if len(candidates) > 1:
            top2_question = candidates[1]["record"].question
            top2_score = round(candidates[1]["total_score"], 2)

        for idx, item in enumerate(candidates[:8]):
            candidates_debug.append({
                "record_id": item["record"].record_id,
                "question": item["record"].question,
                "total_score": round(item.get("total_score", 0.0), 2),
                "llm_score": "N/A",
                "final_score": round(item.get("total_score", 0.0), 2),
                "rank": idx + 1
            })

        query_norm = normalize_text(query)
        top_candidate = candidates[0]
        second_score = candidates[1]["total_score"] if len(candidates) > 1 else None
        score_gap_ok = (
            True
            if second_score is None
            else (top_candidate["total_score"] - second_score) >= score_gap_threshold
        )
        top_question_norm = normalize_text(top_candidate["record"].question)
        exact_match = bool(query_norm and top_question_norm and query_norm == top_question_norm)
        fuzzy_match = False
        if not exact_match and query_norm and top_question_norm:
            fuzzy_match = fuzzy_similarity(query_norm, top_question_norm) >= 88.0

        # 定義語意匹配 (Semantic Match) 的高置信度判定基準
        # 使用 text-embedding-bge-m3 模型時，若檢索向量分數 >= 85.0 且與第二名的差距足夠大，則視為語意匹配。
        semantic_match = False
        if not exact_match and not fuzzy_match:
            if top_candidate["vector_score"] >= 88.0 and score_gap_ok:
                semantic_match = True

        bm25_match = False
        bm25_gap_ok = False
        bm25_rank = top_candidate.get("bm25_rank")
        bm25_top = top_candidate.get("bm25_score", 0.0)
        bm25_second = candidates[1].get("bm25_score", 0.0) if len(candidates) > 1 else None
        if bm25_rank == 1 and bm25_top >= 1.5:
            if bm25_second is None:
                bm25_gap_ok = True
            else:
                bm25_gap_ok = bm25_top >= (bm25_second + 0.001) * 1.5
            if bm25_gap_ok:
                bm25_match = True

        # 優化快速鎖定防禦網，若第二名分數 >= 75.0 (雙峰警戒水位)，不允許語意/詞頻 bypass，強制送 Reranker
        if (exact_match or 
            (score_gap_ok and (fuzzy_match or 
            (semantic_match and (second_score is None or second_score < 75.0)) or 
            (bm25_match and (second_score is None or second_score < 75.0))))):
            for item in candidates:
                item["final_score"] = item["total_score"]

            best = candidates[0]
            low_confidence = best["final_score"] < low_confidence_threshold
            debug_rows = build_debug_rows(
                query,
                candidates,
                best["record"].record_id,
                None,
                primary_keywords,
                secondary_keywords,
            )
            append_debug_rows(debug_rows, DEBUG_CSV_PATH)

            logging.info(
                "[Guardrail] Exact/near match locked (response_type: standard): %s (Score: %.2f)",
                best["record"].question,
                best["final_score"],
            )
            return {
                "answer": best["record"].answer,
                "full_answer": format_answer(best["record"], low_confidence),
                "category": best["record"].category,
                "question": best["record"].question,
                "record_id": best["record"].record_id,
                "score": round(best["final_score"], 2),
                "low_confidence": low_confidence,
                "response_type": "standard",
                "retrieval_score": round(best["total_score"], 2),
                "retrieval_rank": 1,
                "llm_score": "N/A",
                "llm_rank": "N/A",
                "final_score": round(best["final_score"], 2),
                "final_rank": 1,
                # 除錯元數據
                "exact_match": exact_match,
                "fuzzy_match": fuzzy_match,
                "semantic_match": semantic_match,
                "bm25_match": bm25_match,
                "score_gap_ok": score_gap_ok,
                "primary_keywords": primary_keywords_str,
                "secondary_keywords": secondary_keywords_str,
                "top2_question": top2_question,
                "top2_score": top2_score,
                "has_coverage": "N/A",
                "is_aligned": "N/A",
                "alignment_reason": "N/A (Guardrail Lock)",
                "coverage_reason": "N/A (Guardrail Lock)",
                "candidates_debug": candidates_debug,
            }

    # Reranking
    top_candidates = candidates[:top_k]
    llm_scores: Optional[Dict[str, float]] = None
    is_na = False

    llm_scores = rerank_candidates(query, top_candidates, client, model)

    # 一致性抑制 (Consistency Damping)：當向量檢索的第一名被 Reranker 翻轉時，進行置信度調整。
    # 用以避免 Reranker 在檢索分數差距極大時，因為細微的字面理解偏差而做出錯誤的翻轉。
    # 我們引入「檢索置信度引力」(Retrieval Confidence Gravity)：若向量檢索的第一名與第二名差距顯著（例如 >= 3.0 分），
    # 代表檢索結果相當確定，此時將對 Reranker 的翻轉施加懲罰，限制其隨意翻轉的幅度；若差距巨大（如 >= 10.0），則極難被翻轉。
    if llm_scores and len(top_candidates) >= 2:
        ret_top1_id = top_candidates[0]["record"].record_id
        llm_top1_id = max(llm_scores, key=llm_scores.get)

        if ret_top1_id != llm_top1_id and ret_top1_id in llm_scores:
            llm_gap = llm_scores[llm_top1_id] - llm_scores[ret_top1_id]

            if llm_gap > 0:
                ret_top1_score = top_candidates[0]["total_score"]
                ret_selected_score = next((cand["total_score"] for cand in top_candidates if cand["record"].record_id == llm_top1_id), 0.0)
                ret_diff = ret_top1_score - ret_selected_score

                if ret_diff >= 3.0:
                    # 依據 LLM 評估差距與檢索差距進行 Damping 計算
                    damping = 2.0 + min(llm_gap * 0.6, 12.0) + (ret_diff - 3.0) * 0.8
                elif ret_diff < 1.5:
                    damping = 0.0
                else:
                    damping = min(llm_gap * 0.3, 3.0)

                if damping > 0:
                    llm_scores[llm_top1_id] -= damping
                logging.info(
                    "[Consistency Damping] Reranker flipped retrieval Top-1: "
                    "ret_top1=%s, llm_top1=%s, llm_gap=%.1f, ret_diff=%.2f, damping=%.2f",
                    ret_top1_id, llm_top1_id, llm_gap, ret_diff, damping,
                )

    for item in candidates:
        record_id = item["record"].record_id
        if llm_scores and record_id in llm_scores:
            item["final_score"] = 0.5 * item["total_score"] + 0.5 * llm_scores[record_id]
        else:
            item["final_score"] = item["total_score"]

        # 同步更新除錯輸出中的綜合評估數據
        for c_db in candidates_debug:
            if c_db["record_id"] == record_id:
                if llm_scores and record_id in llm_scores:
                    c_db["llm_score"] = round(llm_scores[record_id], 2)
                c_db["final_score"] = round(item["final_score"], 2)

    candidates.sort(key=lambda item: item.get("final_score", 0.0), reverse=True)
    best = candidates[0]

    # Alignment Bypass：對 Reranker 選出的最佳條目進行高置信度檢查，
    # 若 Reranker Top-1 與用戶查詢有精確或模糊匹配，則跳過 Agent 1 避免 false negative。
    best_q_norm = normalize_text(best["record"].question)
    best_is_exact = bool(query_norm and best_q_norm and query_norm == best_q_norm)
    best_is_fuzzy = bool(
        not best_is_exact and query_norm and best_q_norm
        and fuzzy_similarity(query_norm, best_q_norm) >= 88.0
    )

    alignment_bypass = False
    if best_is_exact or best_is_fuzzy:
        is_aligned = True
        alignment_reason = "N/A (High-confidence match bypass)"
        alignment_bypass = True
        logging.info(
            "[Alignment Bypass] Reranker top-1 exact/fuzzy match detected, skipping Agent 1 & 2: %s",
            best["record"].question,
        )
    else:
        # 執行 Agent 1 概念切合度審查
        is_aligned, alignment_reason = check_concept_alignment(query, best["record"], client, model)
    # ==========================================
    # 擴充救援機制 (Dual-Rescue) 準備階段
    # 目的：當加權計算後的最佳條目 (best) 未能通過後續的防護網審查時，
    # 系統不應直接放棄並降級為 RAG，而應給予其他高潛力候選人一次補考機會。
    # ==========================================
    rescue_candidates = []
    
    # 救援順位 1：原始向量檢索的第一名 (retrieval_top1)
    # 說明：有時 Reranker 會過度偏好某些條目，導致真正切合的檢索第一名被擠下。
    retrieval_top1 = max(candidates, key=lambda x: x["total_score"])
    if retrieval_top1["record"].record_id != best["record"].record_id:
        rescue_candidates.append(retrieval_top1)
    
    # 救援順位 2：LLM 評分的第一名 (llm_top1)
    # 說明：有時 Reranker 其實精準命中了正確答案，但由於向量分數落後，
    # 在 50/50 權重相加後被數學公式誤殺。此機制負責撈回這些遺珠。
    if llm_scores:
        llm_top1_id = max(llm_scores, key=llm_scores.get)
        llm_top1 = next((c for c in candidates if c["record"].record_id == llm_top1_id), None)
        if llm_top1 and llm_top1["record"].record_id != best["record"].record_id and llm_top1["record"].record_id != retrieval_top1["record"].record_id:
            rescue_candidates.append(llm_top1)

    coverage_gap_val = ""

    if not is_aligned:
        # 概念或程序不切合！進行 Alignment Rescue (切合度救援)
        logging.info("[Guardrail] Agent 1 Concept Misalignment detected. Attempting Alignment Rescue...")
        rescued = False
        for rescue_cand in rescue_candidates:
            logging.info("[Alignment Rescue] Trying candidate ID=%s", rescue_cand["record"].record_id)
            rescue_aligned, rescue_reason = check_concept_alignment(query, rescue_cand["record"], client, model)
            if rescue_aligned:
                # 若 Agent 1 救援成功，接著驗證 Agent 2
                rescue_coverage, rescue_gap = check_coverage(query, rescue_cand["record"], rescue_reason, client, model)
                if rescue_coverage:
                    logging.info("[Alignment Rescue] Rescue successful! Using ID=%s", rescue_cand["record"].record_id)
                    best = rescue_cand
                    is_aligned = True
                    has_coverage_val = True
                    alignment_reason = rescue_reason
                    coverage_gap_val = "N/A (Rescue Passed)"
                    rescued = True
                    break
        
        if not rescued:
            logging.info("[Guardrail] Alignment Rescue failed. Short-circuit to RAG.")
            has_coverage_val = False
            coverage_gap_val = "N/A (Skipped due to misalignment)"
            is_na = True
    else:
        # 覆蓋度判定優化 (Coverage Bypass)
        best_vector_score = best["vector_score"]
        best_record_id = best["record"].record_id
        best_rerank_score = llm_scores.get(best_record_id, 0.0) if llm_scores else 0.0

        if alignment_bypass:
            # Alignment Bypass 已觸發（精確/模糊匹配）→ 同時跳過 Agent 2
            has_coverage_val = True
            coverage_gap_val = "N/A (High-confidence match bypass)"
            logging.info("[Coverage Bypass] Alignment bypass active, skipping coverage check.")
        elif (
            ((best_rerank_score >= 92.0 and best_vector_score >= 82.0) or
             (best_rerank_score >= 88.0 and best_vector_score >= 85.0))
            and score_gap_ok
        ):
            # 極致安全雙門檻策略
            has_coverage_val = True
            coverage_gap_val = "N/A (Bypassed Coverage Check)"
            logging.info(
                "[Coverage Bypass] Ultra-Safe Dual-Threshold met: rerank=%.2f, vector=%.2f. Bypassing check_coverage.",
                best_rerank_score, best_vector_score
            )
        else:
            has_coverage_val, coverage_gap_val = check_coverage(query, best["record"], alignment_reason, client, model)
            if has_coverage_val:
                coverage_gap_val = "N/A (Aligned and Covered)"

        if not has_coverage_val:
            logging.info("[Coverage] Top-1 cannot fully answer. Attempting Coverage Rescue...")
            rescued = False
            for rescue_cand in rescue_candidates:
                logging.info("[Coverage Rescue] Trying candidate ID=%s", rescue_cand["record"].record_id)
                rescue_aligned, rescue_reason = check_concept_alignment(query, rescue_cand["record"], client, model)
                if rescue_aligned:
                    rescue_coverage, rescue_gap = check_coverage(query, rescue_cand["record"], rescue_reason, client, model)
                    if rescue_coverage:
                        logging.info("[Coverage Rescue] Rescue successful! Using ID=%s", rescue_cand["record"].record_id)
                        best = rescue_cand
                        has_coverage_val = True
                        alignment_reason = rescue_reason
                        coverage_gap_val = "N/A (Rescue Passed)"
                        rescued = True
                        break
            if not rescued:
                is_na = True

    if is_na:
        logging.info("[Coverage/Rerank] No single FAQ can fully answer. Falling back to Vector Search.")
        # 第一階段降級：進行向量庫檢索與 RAG 合成回答
        if VECTOR_SEARCHER:
            top_vec_res = VECTOR_SEARCHER.search_top_k(query, top_k=5)
            valid_res = [res for res in top_vec_res if res[1] >= 0.45]

            if valid_res:
                best_rec, best_score = valid_res[0]
                logging.info("Vector Search Top-1 Score: %.4f, Question: %s", best_score, best_rec.question)

                logging.info("Vector Search hit %d relevant items. Synthesizing answer with LLM...", len(valid_res))
                synthesized_answer, used_ids = synthesize_answer_from_vector(query, valid_res, alignment_reason, coverage_gap_val, client, model)
                debug_rows = build_debug_rows(
                    query,
                    [{"record": r, "total_score": s*100, "final_score": s*100} for r, s in valid_res],
                    best_rec.record_id,
                    None,
                    primary_keywords,
                    secondary_keywords
                )
                append_debug_rows(debug_rows, DEBUG_CSV_PATH)
                logging.info("[RAG] Vector Search + LLM Synthesis used. Best score: %.2f%%, Reference IDs: %s", best_score * 100, used_ids)
                return {
                    "answer": synthesized_answer,
                    "full_answer": synthesized_answer,
                    "category": "智慧搜尋結果",
                    "question": query,
                    "score": round(best_score * 100, 2),
                    "low_confidence": False,
                    "reference_ids": used_ids,
                    "response_type": "rag",
                    "retrieval_score": round(best_score * 100, 2),
                    "retrieval_rank": 1,
                    "llm_score": "N/A",
                    "llm_rank": "N/A",
                    "final_score": round(best_score * 100, 2),
                    "final_rank": 1,
                    # 除錯元數據
                    "exact_match": exact_match,
                    "fuzzy_match": fuzzy_match,
                    "semantic_match": semantic_match,
                    "bm25_match": bm25_match,
                    "score_gap_ok": score_gap_ok,
                    "primary_keywords": primary_keywords_str,
                    "secondary_keywords": secondary_keywords_str,
                    "top2_question": top2_question,
                    "top2_score": top2_score,
                    "is_aligned": is_aligned,
                    "has_coverage": has_coverage_val,
                    "alignment_reason": alignment_reason,
                    "coverage_reason": coverage_gap_val,
                    "candidates_debug": candidates_debug,
                }

        # 第二階段降級：降級至使用通用專利知識回答
        logging.info("Vector Search failed or score too low. Falling back to General Knowledge.")
        gen_answer = answer_from_general_knowledge(query, client, model)
        logging.info("[General Knowledge] LLM used to answer from general knowledge.")
        return {
            "answer": gen_answer,
            "full_answer": gen_answer,
            "category": "通用專利知識",
            "question": query,
            "score": 0.0,
            "low_confidence": True,
            "response_type": "general_knowledge",
            "retrieval_score": 0.0,
            "retrieval_rank": "N/A",
            "llm_score": "N/A",
            "llm_rank": "N/A",
            "final_score": 0.0,
            "final_rank": "N/A",
            # 除錯元數據
            "exact_match": exact_match,
            "fuzzy_match": fuzzy_match,
            "semantic_match": semantic_match,
            "bm25_match": bm25_match,
            "score_gap_ok": score_gap_ok,
            "primary_keywords": primary_keywords_str,
            "secondary_keywords": secondary_keywords_str,
            "top2_question": top2_question,
            "top2_score": top2_score,
            "is_aligned": is_aligned,
            "has_coverage": has_coverage_val,
            "alignment_reason": alignment_reason,
            "coverage_reason": coverage_gap_val,
            "candidates_debug": candidates_debug,
        }

    low_confidence = best["final_score"] < low_confidence_threshold

    debug_rows = build_debug_rows(
        query,
        candidates,
        best["record"].record_id,
        llm_scores,
        primary_keywords,
        secondary_keywords,
    )
    append_debug_rows(debug_rows, DEBUG_CSV_PATH)

    # 搜尋最佳條目在原始檢索結果中的相似度與排名
    retrieval_score = 0.0
    retrieval_rank = "N/A"
    for r_idx, cand in enumerate(top_candidates):
        if cand["record"].record_id == best["record"].record_id:
            retrieval_score = cand["total_score"]
            retrieval_rank = r_idx + 1
            break
    if retrieval_rank == "N/A" and best in candidates:
        retrieval_score = best["total_score"]
        retrieval_rank = candidates.index(best) + 1

    # 計算並記錄 LLM Rerank 之後的排名與分數
    llm_score = "N/A"
    llm_rank = "N/A"
    if llm_scores:
        rec_id = best["record"].record_id
        if rec_id in llm_scores:
            llm_score = llm_scores[rec_id]
            
            # 根據 LLM 分數對候選條目進行排序，以計算最佳條目在 Reranker 中的排名
            llm_sorted = sorted(
                [cand for cand in top_candidates if cand["record"].record_id in llm_scores],
                key=lambda x: llm_scores.get(x["record"].record_id, 0.0),
                reverse=True
            )
            for l_idx, cand in enumerate(llm_sorted):
                if cand["record"].record_id == rec_id:
                    llm_rank = l_idx + 1
                    break

    logging.info("[Standard] Selected final answer from FAQ (response_type: standard): %s (Final Score: %.2f)", best["record"].question, best["final_score"])
    return {
        "answer": best["record"].answer,
        "full_answer": format_answer(best["record"], low_confidence),
        "category": best["record"].category,
        "question": best["record"].question,
        "record_id": best["record"].record_id,
        "score": round(best["final_score"], 2),
        "low_confidence": low_confidence,
        "response_type": "standard",
        "retrieval_score": round(retrieval_score, 2),
        "retrieval_rank": retrieval_rank,
        "llm_score": round(llm_score, 2) if isinstance(llm_score, (int, float)) else llm_score,
        "llm_rank": llm_rank,
        "final_score": round(best["final_score"], 2),
        "final_rank": 1,
        # 除錯元數據
        "exact_match": exact_match,
        "fuzzy_match": fuzzy_match,
        "semantic_match": semantic_match,
        "bm25_match": bm25_match,
        "score_gap_ok": score_gap_ok,
        "primary_keywords": primary_keywords_str,
        "secondary_keywords": secondary_keywords_str,
        "top2_question": top2_question,
        "top2_score": top2_score,
        "is_aligned": is_aligned,
        "has_coverage": has_coverage_val,
        "alignment_reason": alignment_reason,
        "coverage_reason": coverage_gap_val,
        "candidates_debug": candidates_debug,
    }
