from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def generate_summary(report: dict[str, Any]) -> str:
    """Generate a concise Markdown summary from a machine-readable report."""
    overall = report["overall"]
    return "\n".join(
        [
            "# Scoring Summary",
            "",
            f"- Total questions: {overall['total']}",
            f"- Correct answers: {overall['correct']}",
            f"- Accuracy: {overall['accuracy']:.3f}",
            f"- Mean confidence: {overall['mean_confidence']:.3f}" if overall["mean_confidence"] is not None else "- Mean confidence: n/a",
            f"- Brier score: {overall['brier_score']:.3f}" if overall["brier_score"] is not None else "- Brier score: n/a",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Markdown summary from a scoring report.")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.report.read_text(encoding="utf-8"))
    print(generate_summary(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
