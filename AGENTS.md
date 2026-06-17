# Agent Instructions

This repository stores a public benchmark scaffold for semiconductor device physics evaluation.

## Working Rules

- Keep public benchmark questions in `benchmark/`.
- Do not commit real private answer keys. Use `private/answer_key.example.jsonl` only as a schema example.
- Validate changed JSONL files before committing.
- Prefer small, reviewable changes with stable question IDs.
- Keep scoring code deterministic and covered by tests.

## Validation

Run these checks before publishing changes:

```powershell
python scripts/validate_dataset.py benchmark/combined_test.jsonl
python scripts/validate_responses.py examples/example_model_response.jsonl
python scripts/score_responses.py examples/example_model_response.jsonl private/answer_key.example.jsonl
pytest
```
