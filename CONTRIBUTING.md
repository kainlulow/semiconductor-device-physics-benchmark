# Contributing

Contributions are welcome when they improve benchmark quality, validation, documentation, or reproducibility.

## Scientific Content

Preserve the scientific meaning of existing questions. Edit question text only to fix clear syntax, formatting, consistency, or ambiguity issues. If a change alters the intended physics, explain the reason in the pull request.

## Adding Questions

New public questions should:

- use a stable `question_id`;
- include topic, difficulty, skill, assumptions, question text, and options A through D;
- avoid ambiguous sign conventions;
- state ideality assumptions when they matter;
- keep real answer-key entries outside public version control.

## Validation

Run these commands before opening a pull request:

```powershell
python scripts/validate_dataset.py benchmark/*.jsonl
python scripts/validate_responses.py examples/example_model_response.jsonl
pytest
```

## Licensing

Software contributions are MIT licensed. Benchmark-data contributions should be compatible with CC BY 4.0 attribution.
