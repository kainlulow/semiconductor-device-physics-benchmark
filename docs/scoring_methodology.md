# Scoring Methodology

The default scorer compares each model response against an answer key by question ID.

## Metrics

- Accuracy: correct answers divided by total scored questions.
- Per-item correctness: selected answer equals the key answer.
- Calibration bins: optional confidence analysis when responses include confidence values.

Reasoning quality can be evaluated separately with the prompt in `prompts/reasoning_evaluation_prompt.txt`.
