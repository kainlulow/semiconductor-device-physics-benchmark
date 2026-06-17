from pathlib import Path

from scripts.validate_responses import validate_responses


def test_example_response_validates() -> None:
    assert validate_responses(Path("examples/example_model_response.jsonl")) == []
