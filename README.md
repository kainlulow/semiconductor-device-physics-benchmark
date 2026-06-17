# Semiconductor Device Physics Benchmark

A benchmark for evaluating model answers to semiconductor device physics questions across PN junctions, MOS capacitors, and MOSFETs.

## Repository Layout

- `benchmark/`: public JSONL benchmark questions.
- `private/`: private answer-key template. Keep real answer keys out of public commits.
- `schemas/`: JSON Schemas for questions and model responses.
- `scripts/`: validation, scoring, calibration, and report-generation utilities.
- `examples/`: sample model response and scoring report.
- `prompts/`: evaluation prompts for model runs and reasoning review.
- `tests/`: pytest coverage for validation and scoring behavior.
- `docs/`: benchmark design, taxonomy, scoring, and contribution guidance.

## Quick Start

```powershell
python -m pip install -r requirements.txt
python scripts/validate_dataset.py benchmark/combined_test.jsonl
python scripts/validate_responses.py examples/example_model_response.jsonl
python scripts/score_responses.py examples/example_model_response.jsonl private/answer_key.example.jsonl
pytest
```

## Data Format

Each benchmark row is one JSON object per line. Questions include a stable `id`, a `domain`, topic metadata, a prompt, choices, and optional tags. Responses include the same `id`, a selected answer, optional confidence, and optional reasoning.

## License

See `LICENSE`.
