#!/usr/bin/env python3
"""Validate AgentMentor skill metadata and trigger-surface health."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# Common UTF-8-as-GBK mojibake fragments seen when Chinese prose is damaged.
MOJIBAKE_PATTERNS = [
    "绠",
    "鏄",
    "锛",
    "寮",
    "闂",
    "涓",
    "浠",
    "鍙",
    "鐭",
    "浜",
    "瀹",
    "鎻",
    "褰",
    "澶",
    "鍓",
    "楠",
    "妫",
    "韪",
]

ENTRYPOINT_REQUIRED_TERMS = [
    "MUST use",
    "entrypoint",
    "non-trivial",
    "completion claim",
    "AgentMentor",
]

ROUTED_SKILLS = [
    "start-gate",
    "delegation-gate",
    "knowledge-retrieval",
    "doc-lifecycle",
    "incident-learning",
    "vision-gate",
    "readiness-dashboard",
    "change-narrative",
    "knowledge-capture",
    "project-rules",
]

USING_AGENTMENTOR_REQUIRED_RESOURCES = [
    Path("scripts/knowledge_check.py"),
    Path("scripts/closeout_check.py"),
    Path("scripts/skill_metadata_check.py"),
    Path("scripts/hook_diagnostics.py"),
    Path("hooks/agentmentor_hook.py"),
    Path("hooks/codex-hooks.example.json"),
    Path("hooks/claude-settings.example.json"),
    Path("hooks/opencode-plugin.example.ts"),
    Path("assets/templates/FEATURE.md"),
    Path("assets/templates/EVIDENCE.md"),
    Path("assets/templates/LESSON.md"),
    Path("assets/templates/ADR.md"),
    Path("assets/templates/AGENTS.md"),
    Path("assets/templates/CLOSEOUT_COMPACT.md"),
]


@dataclass
class Issue:
    level: str
    path: Path
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate AgentMentor skill frontmatter, encoding, and trigger metadata."
    )
    parser.add_argument("--root", default=".", help="Repository or project root.")
    parser.add_argument(
        "--skills-path",
        default="skills",
        help="Skills directory, relative to --root unless absolute.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings as well as errors.",
    )
    return parser.parse_args()


def frontmatter_block(content: str) -> str | None:
    normalized = content.lstrip("\ufeff").replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return None
    end = normalized.find("\n---\n", 4)
    if end == -1:
        return None
    return normalized[4:end]


def parse_frontmatter(block: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", stripped)
        if match:
            value = match.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            data[match.group(1)] = value
    return data


def read_utf8(path: Path) -> tuple[str | None, list[Issue]]:
    try:
        return path.read_text(encoding="utf-8"), []
    except UnicodeDecodeError as exc:
        return None, [Issue("error", path, f"File is not valid UTF-8: {exc}.")]
    except OSError as exc:
        return None, [Issue("error", path, f"Could not read file: {exc}.")]


def contains_mojibake(text: str) -> bool:
    return any(pattern in text for pattern in MOJIBAKE_PATTERNS)


def validate_skill(path: Path) -> list[Issue]:
    content, issues = read_utf8(path)
    if content is None:
        return issues

    block = frontmatter_block(content)
    if block is None:
        return [Issue("error", path, "Missing YAML frontmatter.")]

    metadata = parse_frontmatter(block)
    name = metadata.get("name", "").strip()
    description = metadata.get("description", "").strip()

    if not name:
        issues.append(Issue("error", path, "Missing frontmatter field: name."))
    elif name != path.parent.name:
        issues.append(
            Issue(
                "warning",
                path,
                f"Skill name '{name}' does not match directory '{path.parent.name}'.",
            )
        )

    if not description:
        issues.append(Issue("error", path, "Missing frontmatter field: description."))

    if contains_mojibake(block):
        issues.append(Issue("error", path, "Frontmatter contains likely mojibake text."))

    if contains_mojibake(content):
        issues.append(Issue("warning", path, "Body contains likely mojibake text."))

    if name == "using-agentmentor":
        for term in ENTRYPOINT_REQUIRED_TERMS:
            if term not in description:
                issues.append(
                    Issue("error", path, f"Entrypoint description is missing '{term}'.")
                )
        for routed_skill in ROUTED_SKILLS:
            if routed_skill not in content:
                issues.append(
                    Issue("error", path, f"Entrypoint body does not route to {routed_skill}.")
                )
        for heading in ["## Activation Contract", "## AgentMentor Presence Check"]:
            if heading not in content:
                issues.append(Issue("error", path, f"Entrypoint is missing {heading}."))
        for relative_resource in USING_AGENTMENTOR_REQUIRED_RESOURCES:
            resource_path = path.parent / relative_resource
            if not resource_path.exists():
                issues.append(
                    Issue(
                        "error",
                        resource_path,
                        "using-agentmentor is missing required bundled resource.",
                    )
                )
    elif name == "using-harness" or name.startswith("harness-"):
        issues.append(
            Issue(
                "error",
                path,
                "Legacy Harness skill slug was removed by the breaking rename; "
                "use `using-agentmentor` or a short semantic AgentMentor workflow slug.",
            )
        )
    elif name == "ai-coding-harness" or name.startswith("ai-coding-harness-"):
        issues.append(
            Issue(
                "error",
                path,
                "AI Coding Harness skill slug was removed by the AgentMentor rename; "
                "use `using-agentmentor` or a short semantic AgentMentor workflow slug.",
            )
        )

    return issues


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    skills_root = Path(args.skills_path)
    if not skills_root.is_absolute():
        skills_root = root / skills_root
    skills_root = skills_root.resolve()

    if not skills_root.exists():
        print(f"ERROR\t{skills_root}\tSkills path not found.", file=sys.stderr)
        return 1

    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    issues: list[Issue] = []
    for path in skill_files:
        issues.extend(validate_skill(path))

    for issue in issues:
        print(f"{issue.level.upper()}\t{issue.path}\t{issue.message}")

    errors = [issue for issue in issues if issue.level == "error"]
    warnings = [issue for issue in issues if issue.level == "warning"]
    print(
        f"Scanned {len(skill_files)} skill file(s). "
        f"Errors: {len(errors)}. Warnings: {len(warnings)}."
    )

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
