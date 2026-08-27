#!/usr/bin/env python3
"""Validate AgentMentor vNext knowledge artifacts and their generated index."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from generate_index import render


KIND_DIR = {"feature": "features", "adr": "decisions", "lesson": "lessons", "evidence": "evidence"}
REQUIRED_FIELDS = {
    "feature": ("id", "doc_kind", "status", "index_summary", "created", "updated"),
    "adr": ("id", "doc_kind", "status", "index_summary", "feature_refs", "decision_area", "supersedes", "created", "updated"),
    "lesson": ("id", "doc_kind", "status", "feature_refs", "applies_to_paths", "trigger_terms", "created", "updated"),
    "evidence": ("id", "doc_kind", "feature_refs", "scope", "created"),
}
REQUIRED_SECTIONS = {
    "feature": ("Goal", "Scope", "Specification", "Acceptance", "Current State", "Links"),
    "adr": ("Context", "Decision", "Boundary", "Rejected Options", "Consequences", "Revisit When", "Links / Evidence"),
    "lesson": ("Signal / Case", "Root Cause", "Resolution", "Protection", "Applies When / Not", "Links"),
    "evidence": ("Supports Claim", "Verification Scope", "Checks", "Results", "Artifacts", "Limitations"),
}
STATUS = {
    "feature": {"draft", "active", "delivered", "archived", "superseded"},
    "adr": {"proposed", "accepted", "superseded"},
    "lesson": {"active", "superseded"},
}
ID_PATTERN = {"feature": r"F\d{3}", "adr": r"ADR-\d{3}", "lesson": r"LL-\d{3}", "evidence": r"EV-\d{3}"}


@dataclass
class Issue:
    path: Path
    message: str


@dataclass
class Record:
    path: Path
    kind: str
    doc_id: str
    fields: dict[str, str]
    content: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--docs-path", default="docs")
    parser.add_argument("--strict", action="store_true", help="Reserved for CI compatibility; all vNext violations are errors.")
    return parser.parse_args()


def frontmatter(content: str) -> dict[str, str] | None:
    content = content.lstrip("\ufeff").replace("\r\n", "\n")
    if not content.startswith("---\n"):
        return None
    end = content.find("\n---\n", 4)
    if end < 0:
        return None
    result: dict[str, str] = {}
    list_key: str | None = None
    values: list[str] = []

    def flush() -> None:
        nonlocal list_key, values
        if list_key is not None:
            result[list_key] = "[" + ", ".join(values) + "]"
        list_key, values = None, []

    for line in content[4:end].splitlines():
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        if list_key is not None and item.startswith("- "):
            values.append(item[2:].strip().strip("'\""))
            continue
        flush()
        matched = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", item)
        if matched:
            key, value = matched.groups()
            if value.strip():
                result[key] = value.strip().strip("'\"")
            else:
                list_key = key
    flush()
    return result


def list_value(value: str | None) -> list[str]:
    if not value:
        return []
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [part.strip().strip("'\"") for part in value[1:-1].split(",") if part.strip()]
    return [value]


def section(content: str, heading: str) -> str | None:
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$.*?(?=^##\s+|\Z)", content, re.MULTILINE | re.DOTALL)
    return match.group(0) if match else None


def has_subheading(content: str, heading: str) -> bool:
    return bool(re.search(rf"^###\s+{re.escape(heading)}\s*$", content, re.MULTILINE))


def markdown_files(docs_root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory in KIND_DIR.values():
        base = docs_root / directory
        if base.exists():
            paths.extend(path for path in base.glob("*.md") if path.name != "INDEX.md")
    return sorted(paths)


def validate_record(path: Path, docs_root: Path) -> tuple[Record | None, list[Issue]]:
    content = path.read_text(encoding="utf-8")
    fields = frontmatter(content)
    if fields is None:
        return None, [Issue(path, "Missing YAML frontmatter.")]
    kind = fields.get("doc_kind", "")
    issues: list[Issue] = []
    if kind not in KIND_DIR:
        return None, [Issue(path, f"Unsupported doc_kind '{kind}'.")]
    expected_dir = docs_root / KIND_DIR[kind]
    if path.parent.resolve() != expected_dir.resolve():
        issues.append(Issue(path, f"{kind} artifact must live under docs/{KIND_DIR[kind]}/."))
    for key in REQUIRED_FIELDS[kind]:
        if key not in fields or not fields[key].strip():
            issues.append(Issue(path, f"Missing required field: {key}."))
    doc_id = fields.get("id", "")
    if doc_id and not re.fullmatch(ID_PATTERN[kind], doc_id):
        issues.append(Issue(path, f"Invalid {kind} id '{doc_id}'."))
    status = fields.get("status")
    if kind in STATUS and status not in STATUS[kind]:
        issues.append(Issue(path, f"Invalid {kind} status '{status}'."))
    if kind in {"feature", "adr"}:
        summary = fields.get("index_summary", "")
        if "\n" in summary or len(summary) > 120:
            issues.append(Issue(path, "index_summary must be one line and at most 120 characters."))
    for heading in REQUIRED_SECTIONS[kind]:
        if section(content, heading) is None:
            issues.append(Issue(path, f"Missing required section: ## {heading}."))
    if kind == "feature":
        scope = section(content, "Scope") or ""
        spec = section(content, "Specification") or ""
        for heading in ("In Scope", "Non-goals"):
            if not has_subheading(scope, heading):
                issues.append(Issue(path, f"Scope must include ### {heading}."))
        for heading in ("Behavior", "Rules and Constraints"):
            if not has_subheading(spec, heading):
                issues.append(Issue(path, f"Specification must include ### {heading}."))
        links = section(content, "Links") or ""
        for heading in ("ADRs", "Lessons", "Evidence", "Related Features", "External Context"):
            if not has_subheading(links, heading):
                issues.append(Issue(path, f"Links must include ### {heading}."))
    if fields.get("status") == "superseded" and not fields.get("superseded_by"):
        issues.append(Issue(path, "superseded artifact must declare superseded_by."))
    return Record(path, kind, doc_id, fields, content), issues


def validate_relationships(records: list[Record], docs_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    features = {record.doc_id: record for record in records if record.kind == "feature"}
    features.update({record.path.stem: record for record in records if record.kind == "feature"})
    for record in records:
        if record.kind == "feature":
            continue
        for ref in list_value(record.fields.get("feature_refs")):
            if ref and ref not in features:
                issues.append(Issue(record.path, f"References missing feature_ref: {ref}."))
    expected, generation_errors = render(docs_root)
    for error in generation_errors:
        issues.append(Issue(docs_root / "INDEX.md", error))
    index_path = docs_root / "INDEX.md"
    if not index_path.exists():
        issues.append(Issue(index_path, "AgentMentor Index is missing."))
    elif index_path.read_text(encoding="utf-8") != expected:
        issues.append(Issue(index_path, "AgentMentor Index is stale. Run generate_index.py."))
    return issues


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    docs_root = Path(args.docs_path)
    docs_root = (root / docs_root if not docs_root.is_absolute() else docs_root).resolve()
    if not docs_root.exists():
        print(f"ERROR\t{docs_root}\tDocs path not found.", file=sys.stderr)
        return 1
    records: list[Record] = []
    issues: list[Issue] = []
    files = markdown_files(docs_root)
    for path in files:
        record, file_issues = validate_record(path, docs_root)
        issues.extend(file_issues)
        if record is not None:
            records.append(record)
    issues.extend(validate_relationships(records, docs_root))
    for issue in issues:
        print(f"ERROR\t{issue.path}\t{issue.message}")
    print(f"Scanned {len(files)} vNext markdown file(s). Checked {len(records)} knowledge artifact(s). Errors: {len(issues)}.")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
