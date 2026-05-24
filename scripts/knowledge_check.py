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
CANONICAL_FEATURE_ID_PATTERN = r"F\d{3}"
DRAFT_FEATURE_ID_PATTERN = r"FP-\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*"
FEATURE_REF_PATTERN = rf"(?:{CANONICAL_FEATURE_ID_PATTERN}|{DRAFT_FEATURE_ID_PATTERN})"

REQUIRED_FIELDS = {
    "feature": ["id", "doc_kind", "status", "created", "updated"],
    "adr": [
        "id",
        "doc_kind",
        "status",
        "scope",
        "feature_refs",
        "decision_area",
        "created",
        "updated",
    ],
    "lesson": [
        "id",
        "doc_kind",
        "status",
        "scope",
        "feature_refs",
        "applies_to",
        "created",
        "updated",
    ],
    "evidence": ["id", "doc_kind", "scope", "feature_refs", "created"],
}

ALLOW_EMPTY_FIELDS = {
    "adr": {"feature_refs"},
    "lesson": {"feature_refs", "applies_to"},
    "evidence": {"feature_refs"},
}

REQUIRED_SECTIONS = {
    "feature": [
        "Goal",
        "Vision Anchor",
        "Current Status",
        "Links",
        "Acceptance Criteria",
        "Patch History",
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


def is_canonical_feature_id(value: str) -> bool:
    return bool(re.fullmatch(CANONICAL_FEATURE_ID_PATTERN, value))


def is_draft_feature_id(value: str) -> bool:
    return bool(re.fullmatch(DRAFT_FEATURE_ID_PATTERN, value))


def is_feature_ref(value: str) -> bool:
    return bool(re.fullmatch(FEATURE_REF_PATTERN, value))


def feature_refs(record: Record) -> list[str]:
    return parse_list(record.frontmatter.get("feature_refs"))


def normalized_status(value: str | None) -> str:
    return (value or "").strip().lower().replace(" ", "-")


def section_content(content: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$"
        rf"(?P<body>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(content)
    if not match:
        return None
    return match.group("body").strip()


def markdown_table_cells(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def is_table_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def patch_history_rows(content: str) -> list[list[str]]:
    body = section_content(content, "Patch History")
    if body is None:
        return []

    rows: list[list[str]] = []
    for line in body.splitlines():
        cells = markdown_table_cells(line)
        if not cells or is_table_separator(cells):
            continue
        if cells[0].lower() == "patch":
            continue
        rows.append(cells)
    return rows


def has_nonempty_section(content: str, heading: str) -> bool:
    body = section_content(content, heading)
    return body is not None and bool(body.strip())


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
        if not is_feature_ref(doc_id):
            issues.append(
                Issue(
                    "error",
                    path,
                    f"Feature id '{doc_id}' must match FNNN or FP-YYYY-MM-DD-slug.",
                )
            )
        elif not re.match(rf"^{re.escape(doc_id)}(\b|-|_)", path.stem):
            issues.append(
                Issue(
                    "warning",
                    path,
                    f"Feature id '{doc_id}' is not reflected in the file name.",
                )
            )
        if frontmatter.get("canonicalized_at") and not parse_list(
            frontmatter.get("aliases")
        ):
            issues.append(
                Issue(
                    "error",
                    path,
                    "Canonicalized Feature must keep its draft identity in aliases.",
                )
            )

    return Record(path, kind, doc_id, frontmatter, content), issues


def validate_feature_patch_history(records: list[Record]) -> list[Issue]:
    issues: list[Issue] = []

    for feature in records:
        if feature.kind != "feature":
            continue

        rows = patch_history_rows(feature.content)
        valid_patch_count = 0
        expected_prefix = f"{feature.doc_id}."

        for row in rows:
            if len(row) < 7:
                issues.append(
                    Issue(
                        "error",
                        feature.path,
                        "Patch History row must include Patch, Date, Commit, Symptom, "
                        "Root Cause, Protection, and Status columns.",
                    )
                )
                continue

            patch_id = row[0]
            if not re.fullmatch(r"F\d{3}\.\d+", patch_id) or not patch_id.startswith(
                expected_prefix
            ):
                issues.append(
                    Issue(
                        "error",
                        feature.path,
                        f"Patch History row uses invalid patch id: {patch_id}. "
                        f"Expected {feature.doc_id}.N.",
                    )
                )
                continue
            valid_patch_count += 1

        if valid_patch_count >= 3 and not has_nonempty_section(
            feature.content, "Patch Churn Review"
        ):
            issues.append(
                Issue(
                    "error",
                    feature.path,
                    f"Feature {feature.doc_id} has {valid_patch_count} Patch History "
                    "entries but no ## Patch Churn Review section.",
                )
            )

    return issues


def validate_relationships(records: list[Record]) -> list[Issue]:
    issues: list[Issue] = []
    feature_ref_targets = build_feature_ref_targets(records, issues)

    for record in records:
        for ref in feature_refs(record):
            if not is_feature_ref(ref):
                issues.append(
                    Issue(
                        "error",
                        record.path,
                        f"Invalid feature_ref '{ref}'. Expected FNNN or FP-YYYY-MM-DD-slug.",
                    )
                )
            elif ref not in feature_ref_targets:
                issues.append(
                    Issue("error", record.path, f"References missing feature_ref: {ref}.")
                )

        if record.kind in {"adr", "lesson", "evidence"}:
            has_scope = "scope" in record.frontmatter
            has_feature_refs = bool(feature_refs(record))
            if not (has_scope or has_feature_refs):
                issues.append(
                    Issue(
                        "warning",
                        record.path,
                        "Knowledge artifact has no scope or feature relationship.",
                    )
                )

    return issues


def build_feature_ref_targets(
    records: list[Record], issues: list[Issue]
) -> dict[str, Record]:
    feature_ref_targets: dict[str, Record] = {}

    for record in records:
        if record.kind != "feature":
            continue

        refs = [record.doc_id, *parse_list(record.frontmatter.get("aliases"))]
        for ref in refs:
            if not ref:
                continue
            if not is_feature_ref(ref):
                issues.append(
                    Issue(
                        "error",
                        record.path,
                        f"Invalid feature ref '{ref}'. Expected FNNN or FP-YYYY-MM-DD-slug.",
                    )
                )
                continue
            existing = feature_ref_targets.get(ref)
            if existing is not None:
                issues.append(
                    Issue(
                        "error",
                        record.path,
                        f"Duplicate feature ref '{ref}' also appears in {existing.path.name}.",
                    )
                )
                continue
            feature_ref_targets[ref] = record

    return feature_ref_targets


def feature_ref_canonical_ids(records: list[Record]) -> dict[str, str]:
    canonical_ids: dict[str, str] = {}

    for record in records:
        if record.kind != "feature":
            continue
        for ref in [record.doc_id, *parse_list(record.frontmatter.get("aliases"))]:
            if ref and ref not in canonical_ids:
                canonical_ids[ref] = record.doc_id

    return canonical_ids


def validate_feature_links(records: list[Record]) -> list[Issue]:
    issues: list[Issue] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
    scheme_pattern = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
    feature_records = {record.doc_id: record for record in records if record.kind == "feature"}
    ref_to_canonical_id = feature_ref_canonical_ids(records)
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
        feature_ids = [
            ref_to_canonical_id.get(feature_ref, feature_ref)
            for feature_ref in feature_refs(record)
        ]

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


def validate_draft_feature_path_links(records: list[Record]) -> list[Issue]:
    issues: list[Issue] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
    scheme_pattern = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")

    for record in records:
        for match in link_pattern.finditer(record.content):
            target = match.group(1)
            if target.startswith("#") or scheme_pattern.match(target):
                continue
            target_name = Path(target).name
            if re.match(rf"{DRAFT_FEATURE_ID_PATTERN}.*\.md$", target_name):
                issues.append(
                    Issue(
                        "warning",
                        record.path,
                        "Markdown links should not target draft Feature paths; "
                        "use feature_refs for machine relationships and link canonical "
                        "FNNN files after mainline acceptance.",
                    )
                )

    return issues


def validate_completed_feature_closeout(records: list[Record]) -> list[Issue]:
    issues: list[Issue] = []
    evidence_by_feature_id: dict[str, list[Record]] = defaultdict(list)
    ref_to_canonical_id = feature_ref_canonical_ids(records)

    for record in records:
        if record.kind == "evidence":
            for feature_ref in feature_refs(record):
                feature_id = ref_to_canonical_id.get(feature_ref, feature_ref)
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
                        "(`knowledge_check.py` command path and result) when Harness "
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
    issues.extend(validate_draft_feature_path_links(records))
    issues.extend(validate_feature_patch_history(records))
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
