from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.common import VALID_OPTIONS, duplicate_ids, is_valid_question_id, normalize_confidence, read_jsonl


def _validate_response(row: dict[str, Any], path: Path, index: int) -> list[str]:
    """Validate one model response row."""
    errors: list[str] = []
    if not is_valid_question_id(row.get("question_id")):
        errors.append(f"{path}:{index}:question_id: expected PN-##, MOSCAP-##, or MOSFET-##")
    if row.get("selected_option") not in VALID_OPTIONS:
        errors.append(f"{path}:{index}:selected_option: expected A, B, C, or D")
    try:
        normalize_confidence(row.get("confidence"))
    except ValueError as exc:
        errors.append(f"{path}:{index}:confidence: {exc}")
    if "reasoning" in row and not isinstance(row["reasoning"], str):
        errors.append(f"{path}:{index}:reasoning: expected string")
    if "equation_used" in row and row["equation_used"] is not None and not isinstance(row["equation_used"], str):
        errors.append(f"{path}:{index}:equation_used: expected string or null")
    return errors


def validate_responses(path: Path) -> list[str]:
    """Validate a model-response JSONL file and return human-readable errors."""
    errors: list[str] = []
    rows = read_jsonl(path)

    for index, row in enumerate(rows, start=1):
        errors.extend(_validate_response(row, path, index))

    for row_id in sorted(duplicate_ids(rows)):
        errors.append(f"{path}: duplicate response id {row_id}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate model response JSONL.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    errors = validate_responses(args.path)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"validated {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
