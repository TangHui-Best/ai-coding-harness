#!/usr/bin/env python3
"""Validate Harness knowledge-capture Markdown artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


ALLOWED_DOC_KINDS = {"feature", "adr", "lesson", "evidence"}
HARNESS_DIRS = {"features", "decisions", "lessons", "evidence"}

REQUIRED_FIELDS = {
    "feature": ["id", "doc_kind", "status", "created", "updated"],
    "adr": [
        "id",
        "doc_kind",
        "status",
        "scope",
        "feature_ids",
        "decision_area",
        "created",
        "updated",
    ],
    "lesson": [
        "id",
        "doc_kind",
        "status",
        "scope",
        "source_feature_ids",
        "applies_to",
        "created",
        "updated",
    ],
    "evidence": ["id", "doc_kind", "scope", "feature_ids", "created"],
}

ALLOW_EMPTY_FIELDS = {
    "adr": {"feature_ids"},
    "lesson": {"source_feature_ids", "applies_to"},
    "evidence": {"feature_ids"},
}

REQUIRED_SECTIONS = {
    "feature": [
        "Goal",
        "Vision Anchor",
        "Current Status",
        "Links",
        "Acceptance Criteria",
        "Evidence",
        "Next Step",
    ],
    "adr": ["Context", "Decision", "Alternatives", "Consequences", "Evidence"],
    "lesson": [
        "Pitfall",
        "Root Cause",
        "Trigger",
        "Fix",
        "Protection",
        "Source",
        "Principle",
    ],
    "evidence": ["Commands", "Results", "Artifacts", "Notes"],
}


@dataclass
class Issue:
    level: str
    path: Path
    message: str


@dataclass
class Record:
    path: Path
    kind: str
    doc_id: str
    frontmatter: dict[str, str]
    content: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Harness knowledge-capture Markdown artifacts."
    )
    parser.add_argument("--root", default=".", help="Repository or project root.")
    parser.add_argument(
        "--docs-path",
        default="docs",
        help="Docs directory, relative to --root unless absolute.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings as well as errors.",
    )
    parser.add_argument(
        "--all-markdown",
        action="store_true",
        help="Require every Markdown file under docs to be a valid knowledge artifact.",
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


def parse_frontmatter(text: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", stripped)
        if match:
            data[match.group(1)] = match.group(2).strip()
    return data


def is_missing_value(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip() == ""


def parse_list(value: str | None) -> list[str]:
    if value is None:
        return []
    text = value.strip()
    if not text:
        return []
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [
            item.strip().strip("'\"")
            for item in inner.split(",")
            if item.strip().strip("'\"")
        ]
    return [text]


def normalized_status(value: str | None) -> str:
    return (value or "").strip().lower().replace(" ", "-")


def linked_markdown_targets(record: Record) -> list[Path]:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
    scheme_pattern = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
    targets: list[Path] = []
    for match in link_pattern.finditer(record.content):
        target = match.group(1)
        if target.startswith("#") or scheme_pattern.match(target):
            continue
        targets.append((record.path.parent / target).resolve())
    return targets


def parse_linked_frontmatter(path: Path) -> dict[str, str]:
    if not path.exists() or path.suffix.lower() != ".md":
        return {}
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    block = frontmatter_block(content)
    if block is None:
        return {}
    return parse_frontmatter(block)


def is_in_harness_dir(path: Path, docs_root: Path) -> bool:
    try:
        relative = path.relative_to(docs_root)
    except ValueError:
        return False
    return bool(relative.parts) and relative.parts[0] in HARNESS_DIRS


def should_check_file(path: Path, docs_root: Path, content: str, all_markdown: bool) -> bool:
    if all_markdown or is_in_harness_dir(path, docs_root):
        return True
    block = frontmatter_block(content)
    if block is None:
        return False
    return parse_frontmatter(block).get("doc_kind") in ALLOWED_DOC_KINDS


def validate_file(
    path: Path, docs_root: Path, all_markdown: bool
) -> tuple[Record | None, list[Issue]]:
    content = path.read_text(encoding="utf-8")
    if not should_check_file(path, docs_root, content, all_markdown):
        return None, []

    issues: list[Issue] = []
    block = frontmatter_block(content)
    if block is None:
        issues.append(Issue("error", path, "Missing YAML frontmatter."))
        return None, issues

    frontmatter = parse_frontmatter(block)
    kind = frontmatter.get("doc_kind")
    if not kind:
        issues.append(Issue("error", path, "Missing required field: doc_kind."))
        return None, issues

    if kind not in ALLOWED_DOC_KINDS:
        issues.append(
            Issue(
                "error",
                path,
                f"Unsupported doc_kind '{kind}'. "
                f"Allowed: {', '.join(sorted(ALLOWED_DOC_KINDS))}.",
            )
        )
        return None, issues

    for field in REQUIRED_FIELDS[kind]:
        if field not in frontmatter:
            issues.append(Issue("error", path, f"Missing required field: {field}."))
        elif field not in ALLOW_EMPTY_FIELDS.get(kind, set()) and is_missing_value(
            frontmatter[field]
        ):
            issues.append(Issue("error", path, f"Required field is empty: {field}."))

    for section in REQUIRED_SECTIONS[kind]:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", content, re.MULTILINE):
            issues.append(Issue("error", path, f"Missing required section: ## {section}."))

    doc_id = frontmatter.get("id", "")
    if kind == "feature" and doc_id:
        if not re.match(rf"^{re.escape(doc_id)}(\b|-|_)", path.stem):
            issues.append(
                Issue(
                    "warning",
                    path,
                    f"Feature id '{doc_id}' is not reflected in the file name.",
                )
            )

    return Record(path, kind, doc_id, frontmatter, content), issues


def validate_relationships(records: list[Record]) -> list[Issue]:
    issues: list[Issue] = []
    feature_ids = {record.doc_id: record.path for record in records if record.kind == "feature"}

    for record in records:
        if record.kind in {"adr", "evidence"}:
            for feature_id in parse_list(record.frontmatter.get("feature_ids")):
                if feature_id not in feature_ids:
                    issues.append(
                        Issue("error", record.path, f"References missing feature_id: {feature_id}.")
                    )
        if record.kind == "lesson":
            for feature_id in parse_list(record.frontmatter.get("source_feature_ids")):
                if feature_id not in feature_ids:
                    issues.append(
                        Issue(
                            "error",
                            record.path,
                            f"References missing source_feature_id: {feature_id}.",
                        )
                    )

        if record.kind in {"adr", "lesson", "evidence"}:
            has_scope = "scope" in record.frontmatter
            has_feature_ids = bool(parse_list(record.frontmatter.get("feature_ids")))
            has_source_feature_ids = bool(
                parse_list(record.frontmatter.get("source_feature_ids"))
            )
            if not (has_scope or has_feature_ids or has_source_feature_ids):
                issues.append(
                    Issue(
                        "warning",
                        record.path,
                        "Knowledge artifact has no scope or feature relationship.",
                    )
                )

    return issues


def validate_feature_links(records: list[Record]) -> list[Issue]:
    issues: list[Issue] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
    scheme_pattern = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
    feature_records = {record.doc_id: record for record in records if record.kind == "feature"}
    linked_paths_by_feature_id: dict[str, set[Path]] = defaultdict(set)

    for record in records:
        if record.kind != "feature":
            continue
        for match in link_pattern.finditer(record.content):
            target = match.group(1)
            if target.startswith("#") or scheme_pattern.match(target):
                continue
            target_path = (record.path.parent / target).resolve()
            if not target_path.exists():
                issues.append(
                    Issue("error", record.path, f"Feature page links to missing file: {target}.")
                )
            else:
                linked_paths_by_feature_id[record.doc_id].add(target_path)

    for record in records:
        if record.kind in {"adr", "evidence"}:
            feature_ids = parse_list(record.frontmatter.get("feature_ids"))
        elif record.kind == "lesson":
            feature_ids = parse_list(record.frontmatter.get("source_feature_ids"))
        else:
            feature_ids = []

        for feature_id in feature_ids:
            if feature_id not in feature_records:
                continue
            if record.path.resolve() not in linked_paths_by_feature_id[feature_id]:
                issues.append(
                    Issue(
                        "warning",
                        feature_records[feature_id].path,
                        f"Feature {feature_id} does not link related {record.kind} "
                        f"{record.doc_id}: {record.path.name}.",
                    )
                )

    return issues


def validate_completed_feature_closeout(records: list[Record]) -> list[Issue]:
    issues: list[Issue] = []
    evidence_by_feature_id: dict[str, list[Record]] = defaultdict(list)

    for record in records:
        if record.kind == "evidence":
            for feature_id in parse_list(record.frontmatter.get("feature_ids")):
                evidence_by_feature_id[feature_id].append(record)

    for feature in records:
        if feature.kind != "feature":
            continue
        if normalized_status(feature.frontmatter.get("status")) != "completed":
            continue

        linked_targets = linked_markdown_targets(feature)
        linked_evidence = [
            target
            for target in linked_targets
            if parse_linked_frontmatter(target).get("doc_kind") == "evidence"
        ]

        if not evidence_by_feature_id.get(feature.doc_id) and not linked_evidence:
            issues.append(
                Issue(
                    "error",
                    feature.path,
                    f"Completed feature {feature.doc_id} has no linked Evidence record.",
                )
            )

        for target in linked_targets:
            frontmatter = parse_linked_frontmatter(target)
            if frontmatter.get("doc_kind") == "plan" and normalized_status(
                frontmatter.get("status")
            ) == "active":
                issues.append(
                    Issue(
                        "error",
                        feature.path,
                        f"Completed feature {feature.doc_id} links to active plan: {target.name}.",
                    )
                )

        related_evidence = list(evidence_by_feature_id.get(feature.doc_id, []))
        linked_evidence_paths = {path.resolve() for path in linked_evidence}
        for record in records:
            if (
                record.kind == "evidence"
                and record.path.resolve() in linked_evidence_paths
                and record not in related_evidence
            ):
                related_evidence.append(record)

        for evidence in related_evidence:
            if "knowledge_check" not in evidence.content:
                issues.append(
                    Issue(
                        "error",
                        evidence.path,
                        "Evidence for a completed feature must record Harness validation "
                        "(`scripts/knowledge_check.py` command and result) when Harness "
                        "artifacts changed.",
                    )
                )

    return issues


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    docs_root = Path(args.docs_path)
    if not docs_root.is_absolute():
        docs_root = root / docs_root
    docs_root = docs_root.resolve()

    if not docs_root.exists():
        print(f"ERROR\t{docs_root}\tDocs path not found.", file=sys.stderr)
        return 1

    records: list[Record] = []
    issues: list[Issue] = []
    markdown_files = sorted(docs_root.rglob("*.md"))

    for path in markdown_files:
        record, file_issues = validate_file(path, docs_root, args.all_markdown)
        issues.extend(file_issues)
        if record is not None:
            records.append(record)

    issues.extend(validate_relationships(records))
    issues.extend(validate_feature_links(records))
    issues.extend(validate_completed_feature_closeout(records))

    for issue in issues:
        print(f"{issue.level.upper()}\t{issue.path}\t{issue.message}")

    errors = [issue for issue in issues if issue.level == "error"]
    warnings = [issue for issue in issues if issue.level == "warning"]
    print(
        f"Scanned {len(markdown_files)} markdown file(s). "
        f"Checked {len(records)} knowledge artifact(s). "
        f"Errors: {len(errors)}. Warnings: {len(warnings)}."
    )

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
