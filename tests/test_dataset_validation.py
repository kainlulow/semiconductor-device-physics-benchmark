from pathlib import Path

import pytest

from scripts.validate_dataset import validate_dataset


def write_jsonl(path: Path, lines: list[str]) -> Path:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_valid_benchmark_validates(tmp_path: Path) -> None:
    path = write_jsonl(
        tmp_path / "questions.jsonl",
        [
            '{"question_id":"PN-01","topic":"PN junction","difficulty":"basic","skill":"conceptual reasoning","question":"What balances at equilibrium?","options":{"A":"A","B":"B","C":"C","D":"D"}}'
        ],
    )

    assert validate_dataset(path) == []


def test_malformed_json_raises_clear_error(tmp_path: Path) -> None:
    path = write_jsonl(tmp_path / "bad.jsonl", ['{"question_id":"PN-01"'])

    with pytest.raises(ValueError, match="invalid JSON"):
        validate_dataset(path)


def test_duplicate_question_ids_are_reported(tmp_path: Path) -> None:
    row = '{"question_id":"PN-01","topic":"PN junction","difficulty":"basic","skill":"conceptual reasoning","question":"Q?","options":{"A":"A","B":"B","C":"C","D":"D"}}'
    path = write_jsonl(tmp_path / "duplicate.jsonl", [row, row])

    assert any("duplicate id PN-01" in error for error in validate_dataset(path))


def test_invalid_options_are_reported(tmp_path: Path) -> None:
    path = write_jsonl(
        tmp_path / "invalid_options.jsonl",
        [
            '{"question_id":"PN-01","topic":"PN junction","difficulty":"basic","skill":"conceptual reasoning","question":"Q?","options":{"A":"A","B":"B","C":"C","E":"E"}}'
        ],
    )

    assert any("expected exactly A, B, C, and D" in error for error in validate_dataset(path))
