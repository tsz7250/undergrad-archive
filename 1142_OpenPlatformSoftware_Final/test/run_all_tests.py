"""
批次執行 faq_regression_test 的 3 種設定，依序輪流執行。
"""
import os
import sys
import time

# Ensure script and parent directory are on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import app
import engine
import faq_regression_test as frt

BASE_CONFIGS = [
    # {
    #     "csv": "db.csv",
    #     "model": "qwen3.5-4b",
    #     "report": "test/reports/original_faq_mismatch.csv",
    #     "questions_csv": "",
    #     "test_only_mismatches": False,
    #     "concurrency": 1,
    # },
    # {
    #     "csv": "db.csv",
    #     "model": "qwen3.5-4b",
    #     "report": "test/reports/repara_faq_mismatch.csv",
    #     "questions_csv": "test/questions_reparaphrased.csv",
    #     "test_only_mismatches": False,
    #     "concurrency": 1,
    # },
    # {
    #     "csv": "db.csv",
    #     "model": "qwen3.5-4b",
    #     "report": "test/reports/repara_faq_mismatch_1.csv",
    #     "questions_csv": "test/questions_reparaphrased_1.csv",
    #     "test_only_mismatches": False,
    #     "concurrency": 1,
    # },
    # {
    #     "csv": "db.csv",
    #     "model": "qwen3.5-4b",
    #     "report": "test/reports/original_faq_mismatch.csv",
    #     "questions_csv": "test/reports/original_faq_mismatch.csv",
    #     "test_only_mismatches": True,
    # },
    { 
        "csv": "db.csv",
        "model": "qwen3.5-4b",
        "report": "test/reports/repara_faq_mismatch.csv",
        "questions_csv": "test/reports/repara_faq_mismatch.csv",
        "test_only_mismatches": True,
    },
    {
        "csv": "db.csv",
        "model": "qwen3.5-4b",
        "report": "test/reports/repara_faq_mismatch_1.csv",
        "questions_csv": "test/reports/repara_faq_mismatch_1.csv",
        "test_only_mismatches": True,
    }
]


CONFIGS = [dict(base) for base in BASE_CONFIGS]


def run_config(index, cfg):
    print("\n" + "=" * 70)
    print(f"[CONFIG {index}/{len(CONFIGS)}] Starting")
    for k, v in cfg.items():
        print(f"  {k} = {v!r}")
    print("=" * 70 + "\n")

    app.LLM_MODEL = cfg.get("model", app.LLM_MODEL)

    class Args:
        pass

    args = Args()
    for k, v in cfg.items():
        setattr(args, k, v)

    frt.ALL_RECORDS = engine.load_faq(args.csv)
    if not frt.ALL_RECORDS:
        print("No records loaded from CSV.")
        return 1

    engine.DEBUG_CSV_PATH = ""

    def load_questions(csv_path: str):
        import csv as csv_mod
        if not csv_path:
            return {}
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Questions file not found: {csv_path}")
        mapping = {}
        with open(csv_path, "r", encoding="utf-8-sig", newline="") as handle:
            reader = csv_mod.DictReader(handle)
            for row in reader:
                record_id = (row.get("record_id") or "").strip()
                q = (row.get("paraphrased_question") or row.get("問題") or "").strip()
                if record_id and q:
                    mapping[record_id] = q
        return mapping

    questions_map = load_questions(args.questions_csv)

    records = frt.ALL_RECORDS
    if args.test_only_mismatches and questions_map:
        records = [r for r in frt.ALL_RECORDS if r.record_id in questions_map]
        print(f"Filtered to run only {len(records)} mismatched records from {args.questions_csv}")

    if app.LLM_CLIENT is None:
        print("Warning: LLM client not configured or unavailable.")
        client = None
        model = ""
    else:
        client = app.LLM_CLIENT
        model = app.LLM_MODEL
    return frt.run_single_stage_test(args, records, questions_map, client, model)


def main():
    overall_start = time.time()
    exit_codes = []

    for i, cfg in enumerate(CONFIGS, start=1):
        t0 = time.time()
        code = run_config(i, cfg)
        elapsed = time.time() - t0
        exit_codes.append(code)
        print(f"\n[CONFIG {i}] Finished in {elapsed:.1f}s, exit code={code}")

    total = time.time() - overall_start
    print("\n" + "=" * 70)
    print(f"ALL CONFIGS DONE. Total elapsed: {total:.1f}s")
    for i, code in enumerate(exit_codes, start=1):
        status = "OK" if code == 0 else f"FAILED({code})"
        print(f"  Config {i}: {status}")
    print("=" * 70)

    return 0 if all(c == 0 for c in exit_codes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
