from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from jsonschema import Draft202012Validator
except ModuleNotFoundError:  # pragma: no cover - exercised in minimal runtimes.
    Draft202012Validator = None

from scripts.common import duplicate_ids, read_jsonl


def _fallback_errors(row: dict, path: Path, index: int) -> list[str]:
    errors: list[str] = []
    required = ["id", "domain", "topic", "question", "choices", "answer_type", "difficulty"]
    for key in required:
        if key not in row:
            errors.append(f"{path}:{index}:{key}: missing required property")

    if row.get("domain") not in {"pn_junction", "mos_capacitor", "mosfet"}:
        errors.append(f"{path}:{index}:domain: invalid domain")
    if row.get("answer_type") != "multiple_choice":
        errors.append(f"{path}:{index}:answer_type: invalid answer type")
    if row.get("difficulty") not in {"introductory", "intermediate", "advanced"}:
        errors.append(f"{path}:{index}:difficulty: invalid difficulty")

    choices = row.get("choices")
    if not isinstance(choices, dict):
        errors.append(f"{path}:{index}:choices: expected object")
    elif set(choices) != {"A", "B", "C", "D"}:
        errors.append(f"{path}:{index}:choices: expected choices A, B, C, and D")
    return errors


def validate_dataset(path: Path, schema_path: Path = Path("schemas/question.schema.json")) -> list[str]:
    errors: list[str] = []
    rows = read_jsonl(path)

    if Draft202012Validator is None:
        for index, row in enumerate(rows, start=1):
            errors.extend(_fallback_errors(row, path, index))
    else:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for index, row in enumerate(rows, start=1):
            for error in validator.iter_errors(row):
                location = ".".join(str(part) for part in error.path) or "<root>"
                errors.append(f"{path}:{index}:{location}: {error.message}")

    for row_id in sorted(duplicate_ids(rows)):
        errors.append(f"{path}: duplicate id {row_id}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate benchmark JSONL questions.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--schema", type=Path, default=Path("schemas/question.schema.json"))
    args = parser.parse_args()

    errors = validate_dataset(args.path, args.schema)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"validated {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
