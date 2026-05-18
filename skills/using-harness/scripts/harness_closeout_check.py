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
    "Backlog/Handoff",
    "Plan lifecycle",
    "Readiness",
    "Vision Gate Exit",
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

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Harness closeout block structure: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
