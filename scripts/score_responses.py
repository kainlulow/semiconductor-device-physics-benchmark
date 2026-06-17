from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.common import VALID_OPTIONS, duplicate_ids, is_valid_question_id, normalize_confidence, read_jsonl, write_json
from scripts.validate_responses import validate_responses


def _index_by_question_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {row["question_id"]: row for row in rows if isinstance(row.get("question_id"), str)}


def _answer_from_key(row: dict[str, Any]) -> str:
    answer = row.get("correct_option", row.get("selected_option"))
    if answer not in VALID_OPTIONS:
        raise ValueError(f"answer key row {row.get('question_id', '<unknown>')}: expected correct_option A, B, C, or D")
    return str(answer)


def _summarize(items: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(items)
    correct = sum(1 for item in items if item["correct"])
    confidences = [item["confidence"] for item in items if item["confidence"] is not None]
    brier_values = [item["brier"] for item in items if item["brier"] is not None]
    return {
        "total": total,
        "correct": correct,
        "accuracy": correct / total if total else None,
        "mean_confidence": sum(confidences) / len(confidences) if confidences else None,
        "brier_score": sum(brier_values) / len(brier_values) if brier_values else None,
    }


def _group_by(items: list[dict[str, Any]], field: str) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        groups[str(item.get(field, "unknown"))].append(item)
    return {name: _summarize(group_items) for name, group_items in sorted(groups.items())}


def score_responses(response_path: Path, answer_key_path: Path, question_path: Path | None = None) -> dict[str, Any]:
    """Score selected-option responses against a private answer key.

    The answer key is expected to contain `question_id` and `correct_option`.
    If a benchmark question file is supplied, topic, difficulty, and skill are
    copied into per-item and grouped metrics.
    """
    response_errors = validate_responses(response_path)
    if response_errors:
        raise ValueError("response validation failed:\n" + "\n".join(response_errors))

    response_rows = read_jsonl(response_path)
    key_rows = read_jsonl(answer_key_path)
    question_rows = read_jsonl(question_path) if question_path else []
    responses = _index_by_question_id(response_rows)
    questions = _index_by_question_id(question_rows)
    key_ids = [row.get("question_id") for row in key_rows]
    malformed_key_ids = [value for value in key_ids if not is_valid_question_id(value)]
    if malformed_key_ids:
        raise ValueError(f"answer key contains malformed question IDs: {malformed_key_ids}")

    answer_key = _index_by_question_id(key_rows)
    items: list[dict[str, Any]] = []
    duplicate_response_ids = sorted(duplicate_ids(response_rows))
    duplicate_key_ids = sorted(duplicate_ids(key_rows))
    unknown_question_ids = sorted(set(responses) - set(answer_key))
    missing_response_ids = sorted(set(answer_key) - set(responses))

    for row_id, key in sorted(answer_key.items()):
        response = responses.get(row_id)
        metadata = questions.get(row_id, {})
        prediction = response.get("selected_option") if response else None
        correct_option = _answer_from_key(key)
        correct = prediction == correct_option
        confidence = normalize_confidence(response.get("confidence")) if response else None
        target = 1.0 if correct else 0.0
        brier = (confidence - target) ** 2 if confidence is not None else None
        items.append(
            {
                "question_id": row_id,
                "topic": metadata.get("topic", key.get("topic", "unknown")),
                "difficulty": metadata.get("difficulty", key.get("difficulty", "unknown")),
                "skill": metadata.get("skill", key.get("skill", "unknown")),
                "correct_option": correct_option,
                "selected_option": prediction,
                "correct": correct,
                "confidence": confidence,
                "brier": brier,
            }
        )

    return {
        "overall": _summarize(items),
        "by_topic": _group_by(items, "topic"),
        "by_difficulty": _group_by(items, "difficulty"),
        "by_skill": _group_by(items, "skill"),
        "diagnostics": {
            "missing_response_ids": missing_response_ids,
            "duplicate_response_ids": duplicate_response_ids,
            "duplicate_answer_key_ids": duplicate_key_ids,
            "unknown_question_ids": unknown_question_ids,
            "malformed_response_errors": response_errors,
        },
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score model responses against an answer key.")
    parser.add_argument("responses", type=Path)
    parser.add_argument("answer_key", type=Path)
    parser.add_argument("--questions", type=Path, help="Optional benchmark question JSONL for topic/difficulty/skill grouping.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = score_responses(args.responses, args.answer_key, args.questions)
    if args.output:
        write_json(args.output, report)
    else:
        import json

        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
