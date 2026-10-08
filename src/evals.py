"""Minimal eval harness: golden Q&A pairs scored by keyword recall.

Run:  python -m src.evals
Extend data/golden.json with your own questions as the knowledge base grows.
"""
import json
from pathlib import Path

from .rag import answer

GOLDEN = Path(__file__).resolve().parent.parent / "data" / "golden.json"


def run() -> None:
    cases = json.loads(GOLDEN.read_text(encoding="utf-8"))
    passed = 0
    for case in cases:
        text, _sources = answer(case["question"])
        hit = all(kw.lower() in text.lower() for kw in case["keywords"])
        print(("PASS" if hit else "FAIL"), "-", case["question"])
        if not hit:
            print("   expected keywords:", case["keywords"])
        passed += hit
    print(f"{passed}/{len(cases)} passed")


if __name__ == "__main__":
    run()
