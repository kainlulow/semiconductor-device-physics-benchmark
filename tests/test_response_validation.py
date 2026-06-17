from pathlib import Path

from scripts.validate_responses import validate_responses


def test_example_response_validates() -> None:
    assert validate_responses(Path("examples/example_model_response.jsonl")) == []


def test_invalid_selected_option_is_reported(tmp_path: Path) -> None:
    path = tmp_path / "responses.jsonl"
    path.write_text('{"question_id":"PN-01","selected_option":"E","confidence":50}\n', encoding="utf-8")

    assert any("selected_option" in error for error in validate_responses(path))
