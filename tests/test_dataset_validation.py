from pathlib import Path

from scripts.validate_dataset import validate_dataset


def test_combined_dataset_validates() -> None:
    assert validate_dataset(Path("benchmark/combined_test.jsonl")) == []
