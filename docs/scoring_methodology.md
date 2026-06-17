# Scoring Methodology

The scorer compares model `selected_option` values against a private answer key keyed by `question_id`.

## Metrics

- Accuracy: correct selected options divided by total keyed questions.
- Grouped accuracy: topic, difficulty, and skill slices when a question file is supplied.
- Mean confidence: average normalized confidence, where 100 becomes 1.0.
- Brier score: mean squared error between selected-option confidence and correctness.

Diagnostics include missing responses, duplicate response IDs, duplicate answer-key IDs, unknown response IDs, and malformed response rows.
