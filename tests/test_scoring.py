from pathlib import Path

from scripts.score_responses import score_responses


def test_example_scoring_is_perfect() -> None:
    report = score_responses(
        Path("examples/example_model_response.jsonl"),
        Path("private/answer_key.example.jsonl"),
    )
    assert report["total"] == 3
    assert report["correct"] == 3
    assert report["accuracy"] == 1.0
