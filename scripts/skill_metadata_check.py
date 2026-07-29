#!/usr/bin/env python3
"""Validate the six AgentMentor vNext Skill entrypoints and core resources."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


FORMAL_SKILLS = {
    "agentmentor",
    "agentmentor-intent",
    "agentmentor-decision",
    "agentmentor-learning",
    "agentmentor-evidence",
    "agentmentor-closeout",
}
LEGACY_SKILLS = {
    "using-agentmentor", "start-gate", "delegation-gate", "knowledge-retrieval",
    "spec-drift", "doc-lifecycle", "incident-learning", "vision-gate",
    "readiness-dashboard", "change-narrative", "knowledge-capture", "project-rules",
}
CORE_RESOURCES = (
    "scripts/context.py", "scripts/knowledge_check.py",
    "assets/templates/FEATURE.md", "assets/templates/ADR.md",
    "assets/templates/LESSON.md", "assets/templates/EVIDENCE.md",
    "assets/templates/CLOSEOUT_COMPACT.md",
)


@dataclass
class Issue:
    path: Path
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--skills-path", default="skills")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def frontmatter(content: str) -> dict[str, str] | None:
    if not content.startswith("---\n"):
        return None
    end = content.find("\n---\n", 4)
    if end < 0:
        return None
    values: dict[str, str] = {}
    for line in content[4:end].splitlines():
        matched = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line.strip())
        if matched:
            values[matched.group(1)] = matched.group(2).strip().strip("'\"")
    return values


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    skills_root = Path(args.skills_path)
    skills_root = (root / skills_root if not skills_root.is_absolute() else skills_root).resolve()
    issues: list[Issue] = []
    present = {path.name for path in skills_root.iterdir() if path.is_dir()} if skills_root.exists() else set()
    for name in sorted(FORMAL_SKILLS - present):
        issues.append(Issue(skills_root / name, "Missing required vNext Skill directory."))
    for name in sorted(LEGACY_SKILLS & present):
        issues.append(Issue(skills_root / name, "Legacy default-Gate Skill must not exist in vNext."))
    for name in sorted(FORMAL_SKILLS & present):
        path = skills_root / name / "SKILL.md"
        if not path.exists():
            issues.append(Issue(path, "Missing SKILL.md."))
            continue
        content = path.read_text(encoding="utf-8")
        fields = frontmatter(content)
        if fields is None:
            issues.append(Issue(path, "Missing YAML frontmatter."))
        elif fields.get("name") != name:
            issues.append(Issue(path, f"Frontmatter name must be '{name}'."))
        elif not fields.get("description"):
            issues.append(Issue(path, "Missing frontmatter description."))
    agentmentor_root = skills_root / "agentmentor"
    for relative in CORE_RESOURCES:
        path = agentmentor_root / relative
        if not path.exists():
            issues.append(Issue(path, "Missing required AgentMentor resource."))
    for issue in issues:
        print(f"ERROR\t{issue.path}\t{issue.message}")
    print(f"Scanned {len(FORMAL_SKILLS)} required vNext Skill(s). Errors: {len(issues)}.")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
