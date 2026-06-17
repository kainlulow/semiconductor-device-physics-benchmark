from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.common import VALID_OPTIONS, duplicate_ids, is_valid_question_id, read_jsonl


def _validate_canonical_question(row: dict[str, Any], path: Path, index: int) -> list[str]:
    """Validate one benchmark question row."""
    errors: list[str] = []
    required = ["question_id", "topic", "difficulty", "skill", "question", "options"]
    for key in required:
        if key not in row:
            errors.append(f"{path}:{index}:{key}: missing required property")

    if not is_valid_question_id(row.get("question_id")):
        errors.append(f"{path}:{index}:question_id: expected PN-##, MOSCAP-##, or MOSFET-##")
    if row.get("difficulty") not in {"basic", "intermediate", "advanced"}:
        errors.append(f"{path}:{index}:difficulty: expected basic, intermediate, or advanced")

    for key in ["topic", "skill", "question"]:
        if key in row and not isinstance(row[key], str):
            errors.append(f"{path}:{index}:{key}: expected string")
        elif key in row and not row[key].strip():
            errors.append(f"{path}:{index}:{key}: expected non-empty string")

    options = row.get("options")
    if not isinstance(options, dict):
        errors.append(f"{path}:{index}:options: expected object")
    elif set(options) != VALID_OPTIONS:
        errors.append(f"{path}:{index}:options: expected exactly A, B, C, and D")
    else:
        for option, text in options.items():
            if not isinstance(text, str) or not text.strip():
                errors.append(f"{path}:{index}:options.{option}: expected non-empty string")
    return errors


def _validate_chat_question(row: dict[str, Any], path: Path, index: int) -> list[str]:
    """Validate one chat-formatted benchmark row."""
    errors: list[str] = []
    if not is_valid_question_id(row.get("question_id")):
        errors.append(f"{path}:{index}:question_id: expected PN-##, MOSCAP-##, or MOSFET-##")

    messages = row.get("messages")
    if not isinstance(messages, list) or not messages:
        errors.append(f"{path}:{index}:messages: expected non-empty list")
        return errors

    for message_index, message in enumerate(messages, start=1):
        if not isinstance(message, dict):
            errors.append(f"{path}:{index}:messages[{message_index}]: expected object")
            continue
        if message.get("role") not in {"system", "user", "assistant"}:
            errors.append(f"{path}:{index}:messages[{message_index}].role: invalid role")
        if not isinstance(message.get("content"), str) or not message["content"].strip():
            errors.append(f"{path}:{index}:messages[{message_index}].content: expected non-empty string")
    return errors


def validate_dataset(path: Path) -> list[str]:
    """Validate a public benchmark JSONL file and return human-readable errors."""
    errors: list[str] = []
    rows = read_jsonl(path)

    for index, row in enumerate(rows, start=1):
        if "messages" in row:
            errors.extend(_validate_chat_question(row, path, index))
        else:
            errors.extend(_validate_canonical_question(row, path, index))

    for row_id in sorted(duplicate_ids(rows)):
        errors.append(f"{path}: duplicate id {row_id}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate benchmark JSONL questions.")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    paths: list[Path] = []
    for path in args.paths:
        if any(character in str(path) for character in "*?["):
            paths.extend(sorted(Path().glob(str(path))))
        else:
            paths.append(path)
    if not paths:
        print("no benchmark files matched")
        return 1

    errors: list[str] = []
    for path in paths:
        errors.extend(validate_dataset(path))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"validated {len(paths)} benchmark file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
