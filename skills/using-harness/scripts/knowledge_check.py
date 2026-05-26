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
CANONICAL_KIND_DIR = {
    "feature": "features",
    "adr": "decisions",
    "lesson": "lessons",
    "evidence": "evidence",
}
FEATURE_ID_PATTERN = r"F\d{3}"

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


@dataclass
class FeatureRefIndex:
    by_key: dict[str, Record]
    by_id: dict[str, list[Record]]


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
    current_list_key: str | None = None
    current_list_items: list[str] = []

    def flush_list() -> None:
        nonlocal current_list_key, current_list_items
        if current_list_key is not None:
            data[current_list_key] = "[" + ", ".join(current_list_items) + "]"
            current_list_key = None
            current_list_items = []

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if current_list_key is not None and stripped.startswith("- "):
            item = stripped[2:].strip().strip("'\"")
            if item:
                current_list_items.append(item)
            continue
        flush_list()
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", stripped)
        if match:
            key = match.group(1)
            value = match.group(2).strip()
            if not value:
                current_list_key = key
                current_list_items = []
            else:
                data[key] = value
    flush_list()
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


def is_feature_id(value: str) -> bool:
    return bool(re.fullmatch(FEATURE_ID_PATTERN, value))


def feature_refs(record: Record) -> list[str]:
    return parse_list(record.frontmatter.get("feature_refs"))


def normalized_ref(value: str) -> str:
    return value.strip().strip("'\"").replace("\\", "/")


def is_feature_stem_ref(value: str) -> bool:
    return bool(re.fullmatch(r"F\d{3}-[A-Za-z0-9][A-Za-z0-9._-]*", value))


def is_feature_path_ref(value: str) -> bool:
    ref = normalized_ref(value)
    return ref.endswith(".md") and ("/features/" in f"/{ref}" or ref.startswith("features/"))


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
    return "doc_kind" in parse_frontmatter(block)


def validate_artifact_path(path: Path, docs_root: Path, kind: str) -> Issue | None:
    expected_dir = CANONICAL_KIND_DIR[kind]
    try:
        relative = path.relative_to(docs_root)
    except ValueError:
        return None

    if not relative.parts or relative.parts[0] != expected_dir:
        return Issue(
            "error",
            path,
            f"{kind} artifact must live under {docs_root.name}/{expected_dir}/.",
        )
    return None


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

    artifact_path_issue = validate_artifact_path(path, docs_root, kind)
    if artifact_path_issue is not None:
        issues.append(artifact_path_issue)

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
        if not is_feature_id(doc_id):
            issues.append(
                Issue(
                    "error",
                    path,
                    f"Feature id '{doc_id}' must match FNNN.",
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


def validate_relationships(records: list[Record], docs_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    feature_ref_index = build_feature_ref_index(records, docs_root)

    for record in records:
        for ref in feature_refs(record):
            resolve_feature_ref(ref, record.path, feature_ref_index, issues)

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


def add_feature_key(targets: dict[str, Record], key: str, record: Record) -> None:
    normalized = normalized_ref(key)
    if normalized and normalized not in targets:
        targets[normalized] = record


def build_feature_ref_index(records: list[Record], docs_root: Path) -> FeatureRefIndex:
    by_key: dict[str, Record] = {}
    by_id: dict[str, list[Record]] = defaultdict(list)
    for record in records:
        if record.kind != "feature":
            continue

        by_id[record.doc_id].append(record)
        add_feature_key(by_key, record.path.stem, record)
        try:
            docs_relative = record.path.resolve().relative_to(docs_root)
        except ValueError:
            continue
        add_feature_key(by_key, docs_relative.as_posix(), record)
        add_feature_key(by_key, f"{docs_root.name}/{docs_relative.as_posix()}", record)

    return FeatureRefIndex(by_key, by_id)


def resolve_feature_ref(
    ref: str,
    source_path: Path,
    index: FeatureRefIndex,
    issues: list[Issue],
) -> Record | None:
    normalized = normalized_ref(ref)
    if normalized in index.by_key:
        return index.by_key[normalized]

    if is_feature_id(normalized):
        matches = index.by_id.get(normalized, [])
        if len(matches) == 1:
            issues.append(
                Issue(
                    "warning",
                    source_path,
                    f"Bare feature_ref '{normalized}' is ambiguous across branches; "
                    "prefer docs/features/<feature-file>.md or the feature file stem.",
                )
            )
            return matches[0]
        if len(matches) > 1:
            issues.append(
                Issue(
                    "error",
                    source_path,
                    f"Ambiguous bare feature_ref '{normalized}' matches multiple Feature files; "
                    "use a full Feature path or file stem.",
                )
            )
            return None

    if is_feature_path_ref(normalized) or is_feature_stem_ref(normalized) or is_feature_id(normalized):
        issues.append(Issue("error", source_path, f"References missing feature_ref: {ref}."))
    else:
        issues.append(
            Issue(
                "error",
                source_path,
                f"Invalid feature_ref '{ref}'. Expected a Feature path, file stem, or FNNN.",
            )
        )
    return None


def validate_feature_links(records: list[Record], docs_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
    scheme_pattern = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
    feature_ref_index = build_feature_ref_index(records, docs_root)
    linked_paths_by_feature_path: dict[Path, set[Path]] = defaultdict(set)

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
                linked_paths_by_feature_path[record.path.resolve()].add(target_path)

    for record in records:
        related_features = [
            resolved
            for feature_ref in feature_refs(record)
            if (resolved := resolve_feature_ref(feature_ref, record.path, feature_ref_index, []))
            is not None
        ]

        for feature in related_features:
            if record.path.resolve() not in linked_paths_by_feature_path[feature.path.resolve()]:
                issues.append(
                    Issue(
                        "warning",
                        feature.path,
                        f"Feature {feature.path.stem} does not link related {record.kind} "
                        f"{record.doc_id}: {record.path.name}.",
                    )
                )

    return issues


def validate_completed_feature_closeout(records: list[Record], docs_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    evidence_by_feature_path: dict[Path, list[Record]] = defaultdict(list)
    feature_ref_index = build_feature_ref_index(records, docs_root)

    for record in records:
        if record.kind == "evidence":
            for feature_ref in feature_refs(record):
                feature = resolve_feature_ref(feature_ref, record.path, feature_ref_index, [])
                if feature is not None:
                    evidence_by_feature_path[feature.path.resolve()].append(record)

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

        if not evidence_by_feature_path.get(feature.path.resolve()) and not linked_evidence:
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

        related_evidence = list(evidence_by_feature_path.get(feature.path.resolve(), []))
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

    issues.extend(validate_relationships(records, docs_root))
    issues.extend(validate_feature_links(records, docs_root))
    issues.extend(validate_feature_patch_history(records))
    issues.extend(validate_completed_feature_closeout(records, docs_root))

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
