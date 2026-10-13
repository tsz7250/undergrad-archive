import csv
import os
import re
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ensure script and parent directory are on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import app
import engine

REPORT_COLUMNS = [
    "index",
    "record_id",
    "問題",
    "原本的問題",
    "預期答案",
    "現在答案",
    "matched_question",
    "matched_category",
    "score",
    "low_confidence",
    "retrieval_score",
    "retrieval_rank",
    "llm_score",
    "llm_rank",
    "final_score",
    "final_rank",
    "response_type",
    "exact_match",
    "fuzzy_match",
    "semantic_match",
    "bm25_match",
    "score_gap_ok",
    "primary_keywords",
    "secondary_keywords",
    "top2_question",
    "top2_score",
    "is_aligned",
    "has_coverage",
    "alignment_reason",
    "coverage_reason",
    "expected_retrieval_score",
    "expected_retrieval_rank",
    "expected_llm_score",
    "expected_llm_rank",
    "expected_final_score",
    "expected_final_rank",
    "error",
]


# Global storage for all FAQ records to keep full search scope.
ALL_RECORDS = []


# Paraphrase support removed: tests run using the original question from the
# FAQ (`db.csv`).


def normalize_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.strip())


def is_row_mismatch(row) -> bool:
    error = row.get("error", "")
    if error:
        return True
        
    expected_id = str(row.get("record_id", "")).strip()
    matched_id = str(row.get("matched_id", "")).strip()
    
    # 若檢索系統最終定位的 ID 就是預期的 ID (即使是 RAG 產生不同字串)，則視為正確
    if matched_id and expected_id and matched_id == expected_id:
        return False
        
    expected_norm = normalize_text(row.get("expected_answer", ""))
    actual_norm = normalize_text(row.get("actual_answer", ""))
    return bool(expected_norm != actual_norm)


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def run_single_stage_test(args, records, questions_map, client, model):
    """Run a single-stage test with all records."""
    total_tasks = len(records)
    results = []
    completed = 0
    concurrency = getattr(args, "concurrency", 1)

    if concurrency > 1:
        # Pre-initialize CrossEncoder in the main thread to avoid concurrent lazy-loading race conditions.
        if engine.CROSS_ENCODER is None:
            from sentence_transformers import CrossEncoder
            try:
                print("Initializing CrossEncoder in main thread before starting parallel pool...")
                engine.CROSS_ENCODER = CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=1024)
            except Exception as e:
                print(f"Failed to pre-initialize CrossEncoder: {e}")

        results_map = {}
        print_lock = threading.Lock()
        completed_lock = threading.Lock()

        def worker(index, record):
            nonlocal completed
            query_text = questions_map.get(record.record_id, "")
            result = run_one(
                index,
                record,
                query_text,
                records,
                client,
                model,
            )

            # Prepare log block
            display_query = query_text if query_text else record.question
            lines = [f"[{index + 1}/{total_tasks}] User asking: \"{display_query}\""]

            if result.get("error"):
                lines.append(f"  [ERROR] {result['error']}")
                lines.append(f"         +- 測試結果: 錯誤 (Error)")
            else:
                resp_type = result.get("response_type", "standard")
                ret_score = result.get("retrieval_score", "N/A")
                ret_rank = result.get("retrieval_rank", "N/A")
                llm_score = result.get("llm_score", "N/A")
                llm_rank = result.get("llm_rank", "N/A")
                fin_score = result.get("final_score", "N/A")
                lines.append(f"  [DONE] Answer received (Type: {resp_type})")
                lines.append(f"         | - Retrieval Score: {ret_score} (Rank: {ret_rank})")
                lines.append(f"         | - LLM Rerank Score: {llm_score} (Rank: {llm_rank})")
                lines.append(f"         | - Final Score: {fin_score}")
                status_str = "錯誤 (Mismatch)" if is_row_mismatch(result) else "正確 (Pass)"
                lines.append(f"         +- 測試結果: {status_str}")

            with completed_lock:
                completed += 1
                curr_completed = completed

            if curr_completed % 10 == 0 or curr_completed == total_tasks:
                lines.append(f"--- Progress: {curr_completed}/{total_tasks} ---")

            # Print atomically to prevent stdout interleaved outputs
            with print_lock:
                print("\n".join(lines))

            return index, result

        # Use ThreadPoolExecutor for concurrent execution
        print(f"Starting test runner with concurrency = {concurrency}...")
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(worker, idx, rec) for idx, rec in enumerate(records)]
            for future in as_completed(futures):
                try:
                    idx, result = future.result()
                    results_map[idx] = result
                except Exception as exc:
                    print(f"Thread execution failed: {exc}")

        # Reconstruct ordered results
        results = [results_map[i] for i in range(total_tasks) if i in results_map]
    else:
        for index, record in enumerate(records):
            query_text = questions_map.get(record.record_id, "")
            display_query = query_text if query_text else record.question
            print(f"[{index + 1}/{total_tasks}] User asking: \"{display_query}\"")

            result = run_one(
                index,
                record,
                query_text,
                records,
                client,
                model,
            )
            results.append(result)
            completed += 1

            # Check for error in result to provide immediate feedback
            if result.get("error"):
                print(f"  [ERROR] {result['error']}")
                print(f"         +- 測試結果: 錯誤 (Error)")
            else:
                resp_type = result.get("response_type", "standard")
                ret_score = result.get("retrieval_score", "N/A")
                ret_rank = result.get("retrieval_rank", "N/A")
                llm_score = result.get("llm_score", "N/A")
                llm_rank = result.get("llm_rank", "N/A")
                fin_score = result.get("final_score", "N/A")
                print(f"  [DONE] Answer received (Type: {resp_type})")
                print(f"         | - Retrieval Score: {ret_score} (Rank: {ret_rank})")
                print(f"         | - LLM Rerank Score: {llm_score} (Rank: {llm_rank})")
                print(f"         | - Final Score: {fin_score}")
                status_str = "錯誤 (Mismatch)" if is_row_mismatch(result) else "正確 (Pass)"
                print(f"         +- 測試結果: {status_str}")

            if completed % 10 == 0 or completed == total_tasks:
                print(f"--- Progress: {completed}/{total_tasks} ---")

    # 排序：錯誤的排在最前，正確的在後，各自照 index 排序
    sorted_results = sorted(results, key=lambda row: (0 if is_row_mismatch(row) else 1, row["index"]))

    write_report(args.report, sorted_results)

    mismatches = [row for row in sorted_results if is_row_mismatch(row)]
    total = len(sorted_results)
    mismatch_count = len(mismatches)
    error_count = sum(1 for row in mismatches if row.get("error"))
    rate = (mismatch_count / total * 100.0) if total else 0.0

    print(f"Total: {total}")
    print(f"Mismatches: {mismatch_count}")
    print(f"Errors: {error_count}")
    print(f"Mismatch rate: {rate:.2f}%")
    print(f"Report: {args.report}")

    return 0


# NOTE: two-stage testing removed — single-stage flow only.


# run_stage1 removed — single-stage processing uses `run_single_stage_test`.


# run_stage2 removed.


def run_one(index, record, query_text, records, client, model):
    # Use the original FAQ question as the query unless an explicit query_text
    # is provided (paraphrase support removed by default).
    try:
        query = query_text or record.question
        # Use ALL_RECORDS as the search database to ensure full coverage
        search_db = ALL_RECORDS if ALL_RECORDS else records
        result = engine.answer_query(query, search_db, client, model)
        
        # 預期條目的對比分數預設值
        expected_ret_score = "N/A"
        expected_ret_rank = "N/A"
        expected_llm_score = "N/A"
        expected_llm_rank = "N/A"
        expected_fin_score = "N/A"
        expected_fin_rank = "N/A"
        
        candidates_debug = result.get("candidates_debug", [])
        expected_id = str(record.record_id).strip()
        
        # 1. 搜尋預期條目的數據
        found_expected = False
        for cand in candidates_debug:
            cand_id = str(cand.get("record_id", "")).strip()
            if cand_id == expected_id:
                expected_ret_score = cand.get("total_score", "N/A")
                expected_ret_rank = cand.get("rank", "N/A")
                expected_llm_score = cand.get("llm_score", "N/A")
                expected_fin_score = cand.get("final_score", "N/A")
                found_expected = True
                break
                
        if not found_expected and candidates_debug:
            # 如果 Top-8 裡沒找到，說明跌出 Top-8
            expected_ret_rank = "未入圍"
            expected_fin_rank = "未入圍"
            
        # 計算預期 ID 在 Rerank 後的綜合排名與 LLM 排名
        if found_expected and candidates_debug:
            # 依照 final_score 排序計算 final_rank
            final_sorted = sorted(candidates_debug, key=lambda x: x.get("final_score", 0.0), reverse=True)
            for f_idx, cand in enumerate(final_sorted):
                if str(cand.get("record_id", "")).strip() == expected_id:
                    expected_fin_rank = f_idx + 1
                    break
            
            # 依照 llm_score 排序計算 llm_rank
            llm_candidates = [c for c in candidates_debug if c.get("llm_score") != "N/A" and c.get("llm_score") is not None]
            if llm_candidates:
                llm_sorted = sorted(llm_candidates, key=lambda x: x.get("llm_score", 0.0), reverse=True)
                for l_idx, cand in enumerate(llm_sorted):
                    if str(cand.get("record_id", "")).strip() == expected_id:
                        expected_llm_rank = l_idx + 1
                        break
                        
        # 如果剛好檢索正確 (Top-1 == expected_id)
        matched_id = str(result.get("record_id", "")).strip()
        if matched_id == expected_id:
            expected_ret_rank = 1
            expected_fin_rank = 1
            expected_ret_score = result.get("retrieval_score", "N/A")
            expected_llm_score = result.get("llm_score", "N/A")
            expected_fin_score = result.get("final_score", "N/A")

        return {
            "index": index,
            "record_id": record.record_id,
            "matched_id": matched_id,
            "問題": query,
            "原本的問題": record.question,
            "預期答案": record.answer,
            "現在答案": result.get("answer", ""),
            "question": record.question,
            "expected_answer": record.answer,
            "actual_answer": result.get("answer", ""),
            "matched_question": result.get("question", ""),
            "matched_category": result.get("category", ""),
            "score": result.get("score", ""),
            "low_confidence": result.get("low_confidence", ""),
            "retrieval_score": result.get("retrieval_score", ""),
            "retrieval_rank": result.get("retrieval_rank", ""),
            "llm_score": result.get("llm_score", ""),
            "llm_rank": result.get("llm_rank", ""),
            "final_score": result.get("final_score", ""),
            "final_rank": result.get("final_rank", ""),
            "response_type": result.get("response_type", ""),
            # 新增除錯欄位
            "exact_match": result.get("exact_match", "N/A"),
            "fuzzy_match": result.get("fuzzy_match", "N/A"),
            "semantic_match": result.get("semantic_match", "N/A"),
            "bm25_match": result.get("bm25_match", "N/A"),
            "score_gap_ok": result.get("score_gap_ok", "N/A"),
            "primary_keywords": result.get("primary_keywords", "N/A"),
            "secondary_keywords": result.get("secondary_keywords", "N/A"),
            "top2_question": result.get("top2_question", "N/A"),
            "top2_score": result.get("top2_score", "N/A"),
            "is_aligned": result.get("is_aligned", "N/A"),
            "has_coverage": result.get("has_coverage", "N/A"),
            "alignment_reason": result.get("alignment_reason", "N/A"),
            "coverage_reason": result.get("coverage_reason", "N/A"),
            # 新增預期對照欄位
            "expected_retrieval_score": expected_ret_score,
            "expected_retrieval_rank": expected_ret_rank,
            "expected_llm_score": expected_llm_score,
            "expected_llm_rank": expected_llm_rank,
            "expected_final_score": expected_fin_score,
            "expected_final_rank": expected_fin_rank,
            "error": "",
        }
    except Exception as exc:  # pragma: no cover - defensive for runtime issues
        return {
            "index": index,
            "record_id": record.record_id,
            "matched_id": "",
            "問題": query_text or record.question,
            "原本的問題": record.question,
            "預期答案": record.answer,
            "現在答案": "",
            "question": record.question,
            "expected_answer": record.answer,
            "actual_answer": "",
            "matched_question": "",
            "matched_category": "",
            "score": "",
            "low_confidence": "",
            "retrieval_score": "",
            "retrieval_rank": "",
            "llm_score": "",
            "llm_rank": "",
            "final_score": "",
            "final_rank": "",
            "response_type": "",
            "exact_match": "N/A",
            "fuzzy_match": "N/A",
            "semantic_match": "N/A",
            "bm25_match": "N/A",
            "score_gap_ok": "N/A",
            "primary_keywords": "N/A",
            "secondary_keywords": "N/A",
            "top2_question": "N/A",
            "top2_score": "N/A",
            "is_aligned": "N/A",
            "has_coverage": "N/A",
            "alignment_reason": "N/A",
            "coverage_reason": "N/A",
            "expected_retrieval_score": "N/A",
            "expected_retrieval_rank": "N/A",
            "expected_llm_score": "N/A",
            "expected_llm_rank": "N/A",
            "expected_final_score": "N/A",
            "expected_final_rank": "N/A",
            "error": repr(exc),
        }


def write_report(report_path: str, sorted_results):
    ensure_parent_dir(report_path)
    with open(report_path, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REPORT_COLUMNS)
        writer.writeheader()
        
        has_written_mismatch = False
        has_written_separator = False
        
        for row in sorted_results:
            is_mism = is_row_mismatch(row)
            if not is_mism and has_written_mismatch and not has_written_separator:
                sep_row = {key: "" for key in REPORT_COLUMNS}
                sep_row["record_id"] = "--- 以下為正確回答 / Below are correct answers ---"
                writer.writerow(sep_row)
                has_written_separator = True
                
            if is_mism:
                has_written_mismatch = True
                
            writer.writerow({key: row.get(key, "") for key in REPORT_COLUMNS})


def main() -> int:
    global ALL_RECORDS
    class Args:
        csv = "db.csv"  # FAQ CSV 檔案的路徑。
        report = "test/reports/repara_faq_mismatch_new.csv"  # 不匹配報告 CSV 檔案的路徑。
        questions_csv = "test/reports/repara_faq_mismatch.csv"  # 選用的 CSV 檔案（record_id, paraphrased_question 或 問題），用作查詢以取代原始 FAQ 問題。
        test_only_mismatches = True  # 若為 True 且已指定 questions_csv，則只測試該檔案中列出的記錄。

    args = Args()

    ALL_RECORDS = engine.load_faq(args.csv)
    if not ALL_RECORDS:
        print("No records loaded from CSV.")
        return 1

    # Disable debug CSV to avoid concurrent writes.
    engine.DEBUG_CSV_PATH = ""

    # Optional: load alternate question CSV (merged human paraphrases).
    def load_questions(csv_path: str):
        if not csv_path:
            return {}
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Questions file not found: {csv_path}")
        mapping = {}
        with open(csv_path, "r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                record_id = (row.get("record_id") or "").strip()
                q = (row.get("paraphrased_question") or row.get("問題") or "").strip()
                if record_id and q:
                    mapping[record_id] = q
        return mapping

    questions_map = load_questions(args.questions_csv)

    records = ALL_RECORDS
    if args.test_only_mismatches and questions_map:
        records = [r for r in ALL_RECORDS if r.record_id in questions_map]
        print(f"Filtered to run only {len(records)} mismatched records from {args.questions_csv}")

    # Single-stage test only
    if app.LLM_CLIENT is None:
        print("Warning: LLM client not configured or unavailable. Running in non-LLM fallback mode.")
        client = None
        model = ""
    else:
        client = app.LLM_CLIENT
        model = app.LLM_MODEL

    return run_single_stage_test(args, records, questions_map, client, model)


if __name__ == "__main__":
    raise SystemExit(main())
