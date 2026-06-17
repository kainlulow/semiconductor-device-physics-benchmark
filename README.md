# Semiconductor Device Physics AI Benchmark

This repository provides a public benchmark for evaluating whether AI models understand foundational semiconductor-device physics before they are tested on more complex semiconductor failure-analysis cases.

The benchmark currently covers three device domains:

- PN junctions
- MOS capacitors
- MOSFETs

The intent is not to claim model performance. This repository supplies question sets, validation tools, response-format conventions, and scoring utilities. Benchmark results should be reported only when model outputs and scoring reports are actually supplied.

## Motivation

Failure analysis in semiconductor technology often requires careful reasoning about device electrostatics, transport, bias conditions, and measurement signatures. Before evaluating models on open-ended anomaly diagnosis, it is useful to test whether they can answer controlled questions about the underlying device physics. This benchmark is a first step toward that staged evaluation.

## Scope

The current release focuses on multiple-choice questions with short physics-based reasoning. Questions are grouped by topic, difficulty, and skill so that results can be analyzed beyond a single aggregate accuracy value.

Current public files:

- `benchmark/pn_junction_test.jsonl`
- `benchmark/mos_capacitor_test.jsonl`
- `benchmark/mosfet_test.jsonl`
- `benchmark/combined_test.jsonl`
- `benchmark/combined_chat_messages_test.jsonl`

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

The chat-message file contains the same scientific questions formatted as system/user messages for chat-completion evaluation.

## Question Taxonomy

- `topic`: device family, currently PN junction, MOS capacitor, or MOSFET.
- `difficulty`: `basic`, `intermediate`, or `advanced`.
- `skill`: the reasoning mode being tested, such as conceptual reasoning, quantitative calculation, bias interpretation, diagnostic reasoning, or failure diagnosis.

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

`confidence` is interpreted as a percentage from 0 to 100.

## Evaluation Procedure

From a clean clone with Python 3.11 or newer:

```powershell
python -m pip install -r requirements.txt
python scripts/validate_dataset.py benchmark/*.jsonl
python scripts/validate_responses.py examples/example_model_response.jsonl
pytest
```

To score model responses, keep the real answer key outside public version control and pass it explicitly:

```powershell
python scripts/score_responses.py path/to/model_responses.jsonl path/to/private_answer_key.jsonl --questions benchmark/combined_test.jsonl --output scoring_report.json
```

The real answer key should use:

```json
{"question_id":"PN-00","correct_option":"C"}
```

## Scoring Metrics

The scoring report is machine-readable JSON and includes:

- selected-option accuracy;
- results by topic, difficulty, and skill;
- mean normalized confidence;
- Brier score using the selected-option confidence;
- missing response IDs;
- duplicate response IDs;
- unknown response IDs;
- malformed response errors.

## Answer-Key Handling

Do not commit the full answer key. The `private/` directory is ignored by default except for `private/answer_key.example.jsonl`, which contains two illustrative non-benchmark records showing the expected format.

## Limitations

- The benchmark is multiple choice and does not fully measure open-ended derivation quality.
- The current domains are foundational device topics, not full process-integration or reliability workflows.
- The public question set may become known to models over time, so held-out private variants are recommended for high-stakes evaluation.
- The benchmark has not yet been validated against a broad panel of models in this repository.

## Roadmap

Planned extensions include:

- larger held-out answer-key management;
- expanded device families and reliability mechanisms;
- open-ended reasoning rubrics;
- anomaly-diagnosis cases based on electrical measurements;
- semiconductor failure-analysis scenarios that combine device physics, process knowledge, and measurement interpretation.

## Citation

Use the metadata in `CITATION.cff` when citing this repository. The software is MIT licensed. For benchmark question data, contributors are encouraged to use or recommend CC BY 4.0 so datasets can be reused with attribution.
