from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.common import read_jsonl, write_json


def score_responses(response_path: Path, answer_key_path: Path) -> dict[str, Any]:
    responses = {row["id"]: row for row in read_jsonl(response_path)}
    answer_key = {row["id"]: row for row in read_jsonl(answer_key_path)}
    items: list[dict[str, Any]] = []

    for row_id, key in sorted(answer_key.items()):
        response = responses.get(row_id)
        predicted = response.get("answer") if response else None
        correct = predicted == key["answer"]
        items.append(
            {
                "id": row_id,
                "answer": key["answer"],
                "prediction": predicted,
                "correct": correct,
                "confidence": response.get("confidence") if response else None,
            }
        )

    total = len(items)
    correct_count = sum(1 for item in items if item["correct"])
    return {
        "total": total,
        "correct": correct_count,
        "accuracy": correct_count / total if total else 0.0,
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score model responses against an answer key.")
    parser.add_argument("responses", type=Path)
    parser.add_argument("answer_key", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = score_responses(args.responses, args.answer_key)
    if args.output:
        write_json(args.output, report)
    else:
        import json

        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
