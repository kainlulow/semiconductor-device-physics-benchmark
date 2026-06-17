from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def generate_summary(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Scoring Summary",
            "",
            f"- Total questions: {report['total']}",
            f"- Correct answers: {report['correct']}",
            f"- Accuracy: {report['accuracy']:.3f}",
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
