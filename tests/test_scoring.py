from pathlib import Path

from scripts.score_responses import score_responses


def write_jsonl(path: Path, rows: list[str]) -> Path:
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def test_missing_and_unknown_question_ids_are_reported(tmp_path: Path) -> None:
    responses = write_jsonl(
        tmp_path / "responses.jsonl",
        [
            '{"question_id":"PN-01","selected_option":"A","confidence":90}',
            '{"question_id":"MOSFET-99","selected_option":"B","confidence":20}',
        ],
    )
    answer_key = write_jsonl(
        tmp_path / "answer_key.jsonl",
        [
            '{"question_id":"PN-01","correct_option":"A"}',
            '{"question_id":"PN-02","correct_option":"B"}',
        ],
    )

    report = score_responses(responses, answer_key)

    assert report["diagnostics"]["missing_response_ids"] == ["PN-02"]
    assert report["diagnostics"]["unknown_question_ids"] == ["MOSFET-99"]


def test_accuracy_and_brier_score_are_correct(tmp_path: Path) -> None:
    questions = write_jsonl(
        tmp_path / "questions.jsonl",
        [
            '{"question_id":"PN-01","topic":"PN junction","difficulty":"basic","skill":"conceptual reasoning","question":"Q?","options":{"A":"A","B":"B","C":"C","D":"D"}}',
            '{"question_id":"MOSCAP-01","topic":"MOS capacitor","difficulty":"advanced","skill":"diagnostic reasoning","question":"Q?","options":{"A":"A","B":"B","C":"C","D":"D"}}',
        ],
    )
    responses = write_jsonl(
        tmp_path / "responses.jsonl",
        [
            '{"question_id":"PN-01","selected_option":"A","confidence":80}',
            '{"question_id":"MOSCAP-01","selected_option":"B","confidence":30}',
        ],
    )
    answer_key = write_jsonl(
        tmp_path / "answer_key.jsonl",
        [
            '{"question_id":"PN-01","correct_option":"A"}',
            '{"question_id":"MOSCAP-01","correct_option":"C"}',
        ],
    )

    report = score_responses(responses, answer_key, questions)

    assert report["overall"]["total"] == 2
    assert report["overall"]["correct"] == 1
    assert report["overall"]["accuracy"] == 0.5
    assert abs(report["overall"]["brier_score"] - 0.065) < 1e-12
    assert report["by_topic"]["PN junction"]["accuracy"] == 1.0
    assert report["by_topic"]["MOS capacitor"]["accuracy"] == 0.0
