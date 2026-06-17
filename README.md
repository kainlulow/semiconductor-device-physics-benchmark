# Semiconductor Device Physics AI Benchmark

This repository provides a public benchmark for evaluating whether AI models understand foundational semiconductor-device physics before they are tested on more complex semiconductor failure-analysis cases.

The benchmark currently covers three device domains:

- PN junctions
- MOS capacitors
- MOSFETs

The repository supplies question sets, validation tools, response-format conventions, and scoring utilities. It does not claim model performance. Report benchmark results only when the model outputs, answer key provenance, and generated scoring reports are actually supplied.

## Motivation

Semiconductor failure analysis often requires careful reasoning about electrostatics, carrier transport, bias conditions, measurement signatures, and non-ideal device behavior. Before evaluating models on open-ended anomaly diagnosis, it is useful to test whether they can answer controlled questions about the underlying device physics. This benchmark is a staged first step toward that broader evaluation.

## Repository Layout

```text
benchmark/            Public JSONL question sets
schemas/              JSON Schema documentation for questions and responses
scripts/              Validation, scoring, calibration, and summary utilities
prompts/              Evaluation and reasoning-review prompts
examples/             Non-benchmark example response/report files
tests/                Pytest tests for validators and scorer behavior
docs/                 Design notes, taxonomy, scoring, and contribution notes
private/              Ignored private material, except answer_key.example.jsonl
.github/workflows/   CI validation workflow
```

## Benchmark Scope

The current release focuses on multiple-choice questions with short physics-based reasoning. Questions are grouped by topic, difficulty, and skill so results can be analyzed beyond one aggregate accuracy value.

Public benchmark files:

- `benchmark/pn_junction_test.jsonl`
- `benchmark/mos_capacitor_test.jsonl`
- `benchmark/mosfet_test.jsonl`
- `benchmark/combined_test.jsonl`
- `benchmark/combined_chat_messages_test.jsonl`

Use the domain-specific files when evaluating one topic at a time. Use `combined_test.jsonl` for aggregate evaluation. Use `combined_chat_messages_test.jsonl` when an evaluation harness expects chat-style `system` and `user` messages.

## Dataset Structure

Canonical benchmark rows are JSONL records with this shape:

```json
{
  "question_id": "PN-01",
  "topic": "PN junction",
  "difficulty": "basic",
  "skill": "conceptual reasoning",
  "assumptions": "Assume silicon devices at T = 300 K...",
  "question": "At thermal equilibrium...",
  "options": {
    "A": "...",
    "B": "...",
    "C": "...",
    "D": "..."
  },
  "response_schema": {
    "question_id": "string",
    "selected_option": "A|B|C|D",
    "confidence": "integer from 0 to 100",
    "reasoning": "brief physics-based explanation",
    "equation_used": "equation or null"
  }
}
```

The chat-message JSONL variant contains the same scientific questions formatted as:

```json
{
  "question_id": "PN-01",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ]
}
```

## Question Taxonomy

- `topic`: device family, currently PN junction, MOS capacitor, or MOSFET.
- `difficulty`: `basic`, `intermediate`, or `advanced`.
- `skill`: reasoning mode being tested, such as conceptual reasoning, quantitative calculation, bias interpretation, diagnostic reasoning, mechanism discrimination, or failure diagnosis.

Question IDs use stable prefixes:

- `PN-##`
- `MOSCAP-##`
- `MOSFET-##`

## Response Format

Model responses should be one JSON object per line:

```json
{
  "question_id": "PN-00",
  "selected_option": "C",
  "confidence": 82,
  "reasoning": "Example reasoning for a non-benchmark illustrative record.",
  "equation_used": null
}
```

`selected_option` must be `A`, `B`, `C`, or `D`. `confidence` is interpreted as a percentage from 0 to 100 and is normalized to 0-1 for calibration and Brier-score calculations.

## Quick Start

From a clean clone with Python 3.11 or newer:

```powershell
python -m pip install -r requirements.txt
python scripts/validate_dataset.py benchmark/*.jsonl
python scripts/validate_responses.py examples/example_model_response.jsonl
pytest
```

The dataset validator supports canonical question files and the chat-message file. On shells that do not expand `benchmark/*.jsonl`, the script expands the glob internally.

## Scoring A Model Run

Keep the real answer key outside public version control and pass it explicitly:

```powershell
python scripts/score_responses.py path/to/model_responses.jsonl path/to/private_answer_key.jsonl --questions benchmark/combined_test.jsonl --output scoring_report.json
```

The real answer key should use one JSON object per line:

```json
{"question_id":"PN-00","correct_option":"C"}
```

The `--questions` argument is optional but recommended. It lets the scorer attach topic, difficulty, and skill metadata to each scored item and produce grouped metrics.

## Scoring Report

The scoring report is machine-readable JSON with these top-level fields:

- `overall`: total count, correct count, accuracy, mean confidence, and Brier score.
- `by_topic`: metrics grouped by device topic.
- `by_difficulty`: metrics grouped by difficulty.
- `by_skill`: metrics grouped by tested reasoning skill.
- `diagnostics`: missing response IDs, duplicate response IDs, duplicate answer-key IDs, unknown question IDs, and malformed response errors.
- `items`: per-question scoring records.

The Brier score uses the model's confidence in its selected option. For a correct selected option the target is 1.0; for an incorrect selected option the target is 0.0.

## Answer-Key Handling

Do not commit the full answer key. The `private/` directory is ignored by default except for `private/answer_key.example.jsonl`, which contains two illustrative non-benchmark records showing the expected format.

Public question files should not contain answer labels. The examples use `-00` IDs so they demonstrate format without revealing labels for benchmark questions.

## Continuous Integration

The GitHub Actions workflow runs on every push and pull request. It installs the Python test dependency, validates all public benchmark JSONL files, validates the example response file, and runs pytest.

## Contributing

See `CONTRIBUTING.md` and `docs/contributing_questions.md`. In brief:

- preserve the scientific meaning of existing questions unless fixing a clear syntax, consistency, or ambiguity issue;
- keep answer-key material private;
- validate changed JSONL files;
- run tests before opening a pull request;
- explain any physics-content change explicitly.

## Limitations

- The benchmark is multiple choice and does not fully measure open-ended derivation quality.
- The current domains are foundational device topics, not full process-integration or reliability workflows.
- The public question set may become known to models over time, so held-out private variants are recommended for high-stakes evaluation.
- The repository has not yet published broad model-evaluation results.
- Expert review is still recommended for any scientific-content change.

## Roadmap

Planned extensions include:

- larger held-out answer-key management;
- expanded device families and reliability mechanisms;
- open-ended reasoning rubrics;
- anomaly-diagnosis cases based on electrical measurements;
- semiconductor failure-analysis scenarios that combine device physics, process knowledge, and measurement interpretation.

## Licensing And Citation

The software in this repository is MIT licensed. For benchmark question data, contributors are encouraged to use or recommend CC BY 4.0 so datasets can be reused with attribution.

Use the metadata in `CITATION.cff` when citing this repository.
