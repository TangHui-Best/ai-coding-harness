#!/usr/bin/env python3
"""Validate the structural completeness of a Harness closeout block."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "Closeout verdict",
    "Completion claim allowed",
    "Entry Gate",
    "Vision Anchor",
    "Backlog/Handoff",
    "Plan lifecycle",
    "Readiness",
    "Vision Gate Exit",
    "Patch Churn Review",
    "Bugfix attribution",
    "ADR",
    "Lesson",
    "Evidence",
    "Evidence level",
    "Feature",
    "Check",
]

ALLOWED_VERDICTS = {"pass", "conditional", "blocked"}
ALLOWED_COMPLETION = {"yes", "no"}
ALLOWED_EVIDENCE_LEVELS = {"quick", "standard", "exhaustive"}
REASON_MARKERS = ("because", "since", "原因", "因为")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the structural completeness of a Harness closeout block."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Markdown or text file containing the Harness closeout block.",
    )
    return parser.parse_args()


def read_fields(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8-sig")
    fields: dict[str, str] = {}
    for line in content.splitlines():
        match = re.match(r"^([A-Za-z][A-Za-z /-]*):\s*(.*)$", line.strip())
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def first_token(value: str) -> str:
    parts = value.strip().split(maxsplit=1)
    if not parts:
        return ""
    return parts[0].strip().lower()


def normalized(value: str) -> str:
    return value.strip().lower()


def starts_with_status(value: str, status: str) -> bool:
    return normalized(value).startswith(status)


def has_reason(value: str) -> bool:
    text = normalized(value)
    return any(marker in text for marker in REASON_MARKERS)


def has_feature_record(value: str) -> bool:
    text = normalized(value)
    return bool(text) and not text.startswith("not triggered")


def has_dedicated_evidence_record(value: str) -> bool:
    return bool(
        re.search(r"\bEV-\d+\b", value)
        or re.search(r"(?:^|[\\/])docs[\\/]evidence(?:[\\/]|$)", value, re.IGNORECASE)
        or re.search(r"(?:^|[\\/])evidence[\\/]", value, re.IGNORECASE)
    )


def main() -> int:
    args = parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: closeout file not found: {path}", file=sys.stderr)
        return 2

    fields = read_fields(path)
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if not fields.get(field):
            errors.append(f"Missing or empty field: {field}")

    verdict = first_token(fields.get("Closeout verdict", ""))
    completion = first_token(fields.get("Completion claim allowed", ""))
    evidence_level = first_token(fields.get("Evidence level", ""))
    entry_gate = fields.get("Entry Gate", "")
    vision_anchor = fields.get("Vision Anchor", "")
    feature = fields.get("Feature", "")
    evidence = fields.get("Evidence", "")

    if verdict and verdict not in ALLOWED_VERDICTS:
        errors.append(
            "Closeout verdict must start with one of: "
            + ", ".join(sorted(ALLOWED_VERDICTS))
        )
    if completion and completion not in ALLOWED_COMPLETION:
        errors.append("Completion claim allowed must start with yes or no.")
    if evidence_level and evidence_level not in ALLOWED_EVIDENCE_LEVELS:
        errors.append(
            "Evidence level must start with one of: "
            + ", ".join(sorted(ALLOWED_EVIDENCE_LEVELS))
        )
    if completion == "yes" and verdict == "blocked":
        errors.append("Completion claim cannot be allowed when closeout is blocked.")
    if completion == "yes" and fields.get("Evidence", "").lower().startswith(
        "not triggered"
    ):
        errors.append("Completion claim requires an Evidence location.")
    if completion == "yes" and starts_with_status(entry_gate, "missing"):
        errors.append("Completion claim requires Entry Gate to be satisfied.")
    if (
        completion == "yes"
        and starts_with_status(vision_anchor, "not triggered")
        and not has_reason(vision_anchor)
    ):
        errors.append("Vision Anchor exemption must include a reason.")
    if (
        completion == "yes"
        and starts_with_status(entry_gate, "retroactive")
        and not (
            has_feature_record(feature) or has_dedicated_evidence_record(evidence)
        )
    ):
        errors.append(
            "Retroactive Entry Gate requires a Feature or dedicated Evidence recovery record."
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Harness closeout block structure: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
