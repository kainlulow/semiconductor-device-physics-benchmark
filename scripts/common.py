from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

VALID_OPTIONS = {"A", "B", "C", "D"}
QUESTION_ID_PATTERN = re.compile(r"^(PN|MOSCAP|MOSFET)-\d{2,}$")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read a JSONL file and return object rows.

    Raises:
        ValueError: If a line is not valid JSON or is not a JSON object.
    """
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected JSON object")
            rows.append(value)
    return rows


def write_json(path: Path, payload: Any) -> None:
    """Write a stable, machine-readable JSON document."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def get_question_id(row: dict[str, Any]) -> str | None:
    """Return the canonical question ID field if present."""
    value = row.get("question_id")
    return value if isinstance(value, str) else None


def duplicate_ids(rows: Iterable[dict[str, Any]]) -> set[str]:
    """Return duplicate question IDs from an iterable of JSON objects."""
    seen: set[str] = set()
    duplicates: set[str] = set()
    for row in rows:
        row_id = get_question_id(row)
        if not row_id:
            continue
        if row_id in seen:
            duplicates.add(row_id)
        seen.add(row_id)
    return duplicates


def is_valid_question_id(value: Any) -> bool:
    """Return whether a value has the benchmark question-ID shape."""
    return isinstance(value, str) and bool(QUESTION_ID_PATTERN.fullmatch(value))


def normalize_confidence(value: Any) -> float | None:
    """Normalize a 0-100 confidence value to 0-1.

    Returns None if no confidence was supplied.
    """
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("confidence must be a number from 0 to 100")
    if not 0 <= float(value) <= 100:
        raise ValueError("confidence must be between 0 and 100")
    return float(value) / 100.0
