#!/usr/bin/env python3
"""Append AgentMentor document usage events."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


DOC_TYPES = {"feature", "adr", "lesson", "evidence", "agents", "other"}
IMPACTS = {
    "changed_scope",
    "changed_design",
    "changed_fix_direction",
    "changed_verification_gate",
    "supported_completion_claim",
    "prevented_repeat_failure",
    "shaped_change_narrative",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append one AgentMentor doc-used event to .agentmentor/usage/events/<git-user>.jsonl."
    )
    parser.add_argument("--root", default=".", help="Repository root. Defaults to cwd.")
    parser.add_argument("--doc", required=True, help="Document path relative to --root.")
    parser.add_argument("--doc-type", required=True, choices=sorted(DOC_TYPES))
    parser.add_argument("--task", required=True, help="Short current task description.")
    parser.add_argument("--impact", required=True, choices=sorted(IMPACTS))
    parser.add_argument(
        "--actor",
        help="Override actor filename stem. Defaults to git config user.name.",
    )
    return parser.parse_args()


def run_git_user_name(root: Path) -> str:
    result = subprocess.run(
        ["git", "config", "user.name"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise ValueError("git config user.name is required to choose the usage event file")
    return result.stdout.strip()


def actor_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip().lower()).strip(".-_")
    if not slug:
        raise ValueError("actor name produced an empty usage filename")
    return slug


def validate_relative_doc(root: Path, doc: str) -> str:
    doc_path = Path(doc)
    if doc_path.is_absolute():
        raise ValueError("--doc must be relative to --root")
    normalized = doc_path.as_posix()
    if normalized.startswith("../") or "/../" in normalized or normalized == "..":
        raise ValueError("--doc must stay inside --root")
    resolved = (root / doc_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("--doc must stay inside --root") from exc
    if not resolved.exists():
        raise ValueError(f"--doc does not exist: {normalized}")
    return normalized


def append_event(root: Path, doc: str, doc_type: str, task: str, impact: str, actor: str) -> Path:
    if not task.strip():
        raise ValueError("--task must not be empty")
    event = {
        "ts": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "doc": validate_relative_doc(root, doc),
        "doc_type": doc_type,
        "task": task.strip(),
        "impact": impact,
    }
    target_dir = root / ".agentmentor" / "usage" / "events"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{actor_slug(actor)}.jsonl"
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
    return target


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: --root does not exist: {root}", file=sys.stderr)
        return 2
    try:
        actor = args.actor or run_git_user_name(root)
        target = append_event(root, args.doc, args.doc_type, args.task, args.impact, actor)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"usage event appended: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
