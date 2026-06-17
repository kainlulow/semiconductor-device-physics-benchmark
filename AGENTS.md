# Agent Instructions

## Layout

- `benchmark/`: public JSONL question sets.
- `schemas/`: JSON Schema documentation for questions and responses.
- `scripts/`: validation, scoring, calibration, and summary utilities.
- `prompts/`: evaluation and reasoning-review prompts.
- `examples/`: example response and report artifacts.
- `tests/`: pytest coverage.
- `docs/`: design, taxonomy, scoring, and contribution notes.
- `private/`: ignored private material. Only `answer_key.example.jsonl` may be committed.
- `.github/workflows/`: CI validation.

## Scientific-Content Rules

Preserve every question's scientific meaning unless there is a clear syntax, formatting, consistency, or ambiguity error. Do not change answer choices or physics claims casually. Flag any uncertain device-physics issue for expert review.

## Commands

Validate public benchmark files:

```powershell
python scripts/validate_dataset.py benchmark/*.jsonl
```

Validate example model responses:

```powershell
python scripts/validate_responses.py examples/example_model_response.jsonl
```

Run tests:

```powershell
pytest
```

Score a private run:

```powershell
python scripts/score_responses.py path/to/model_responses.jsonl path/to/private_answer_key.jsonl --questions benchmark/combined_test.jsonl --output scoring_report.json
```

## Coding Conventions

Use Python 3.11 or newer, standard-library features where practical, type hints, docstrings for public helpers, `pathlib`, deterministic JSON output, and clear error messages. Avoid unnecessary dependencies.

## Pull-Request Completion Criteria

- Public JSONL benchmark files validate.
- Tests pass.
- No real answer key is committed.
- README or docs are updated when formats or procedures change.
- Any scientific-content changes are explicitly described.
