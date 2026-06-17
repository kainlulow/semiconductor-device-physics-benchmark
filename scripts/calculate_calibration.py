from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.score_responses import score_responses


def calibration_bins(report: dict[str, Any], bins: int = 10) -> list[dict[str, Any]]:
    """Calculate accuracy by confidence bucket from a scoring report."""
    buckets = [{"count": 0, "correct": 0, "confidence_sum": 0.0} for _ in range(bins)]
    for item in report["items"]:
        confidence = item.get("confidence")
        if confidence is None:
            continue
        index = min(int(float(confidence) * bins), bins - 1)
        buckets[index]["count"] += 1
        buckets[index]["correct"] += int(bool(item["correct"]))
        buckets[index]["confidence_sum"] += float(confidence)

    result = []
    for index, bucket in enumerate(buckets):
        count = bucket["count"]
        result.append(
            {
                "bin": index,
                "lower": index / bins,
                "upper": (index + 1) / bins,
                "count": count,
                "accuracy": bucket["correct"] / count if count else None,
                "mean_confidence": bucket["confidence_sum"] / count if count else None,
            }
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate confidence calibration bins.")
    parser.add_argument("responses", type=Path)
    parser.add_argument("answer_key", type=Path)
    parser.add_argument("--questions", type=Path)
    parser.add_argument("--bins", type=int, default=10)
    args = parser.parse_args()

    import json

    report = score_responses(args.responses, args.answer_key, args.questions)
    print(json.dumps(calibration_bins(report, args.bins), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
