#!/usr/bin/env python3
"""Generate the compact AgentMentor engineering index from vNext documents."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


INDEXABLE_STATUS = {"feature": {"active", "delivered"}, "adr": {"accepted"}}
KIND_DIR = {"feature": "features", "adr": "decisions"}


@dataclass(frozen=True)
class IndexRecord:
    path: Path
    kind: str
    doc_id: str
    title: str
    brief: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--docs-path", default="docs")
    parser.add_argument("--check", action="store_true", help="Fail when docs/INDEX.md is stale.")
    return parser.parse_args()


def frontmatter(content: str) -> dict[str, str] | None:
    content = content.lstrip("\ufeff").replace("\r\n", "\n")
    if not content.startswith("---\n"):
        return None
    end = content.find("\n---\n", 4)
    if end < 0:
        return None
    result: dict[str, str] = {}
    for line in content[4:end].splitlines():
        matched = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line.strip())
        if matched:
            result[matched.group(1)] = matched.group(2).strip().strip("'\"")
    return result


def heading(content: str) -> str | None:
    matched = re.search(r"^#\s+(.+?)\s*$", content, re.MULTILINE)
    return matched.group(1).strip() if matched else None


def collect(docs_root: Path) -> tuple[list[IndexRecord], list[str]]:
    records: list[IndexRecord] = []
    errors: list[str] = []
    for kind, directory in KIND_DIR.items():
        base = docs_root / directory
        for path in sorted(base.glob("*.md")) if base.exists() else []:
            content = path.read_text(encoding="utf-8")
            fields = frontmatter(content)
            if fields is None or fields.get("doc_kind") != kind:
                continue
            if fields.get("status") not in INDEXABLE_STATUS[kind]:
                continue
            doc_id, title, brief = fields.get("id", ""), heading(content), fields.get("index_summary", "")
            if not doc_id or not title or not brief:
                errors.append(f"{path}: indexable {kind} requires id, title, and index_summary.")
                continue
            if "\n" in brief or len(brief) > 120:
                errors.append(f"{path}: index_summary must be one line and at most 120 characters.")
                continue
            records.append(IndexRecord(path, kind, doc_id, title, brief))
    return sorted(records, key=lambda record: (record.kind, record.doc_id, record.path.name)), errors


def render(docs_root: Path) -> tuple[str, list[str]]:
    records, errors = collect(docs_root)
    lines = [
        "# AgentMentor Index",
        "",
        "用于帮助 Agent 判断当前任务需要阅读哪些工程事实。它不是正文，不是规则引擎，也不替代 Feature 或 ADR。",
        "",
        "仅收录当前有效的 Feature 与已接受的 ADR；草稿、归档和已替代文档不进入此目录。",
        "",
        "| Document | Type | Brief |",
        "| --- | --- | --- |",
    ]
    for record in records:
        relative = record.path.relative_to(docs_root).as_posix()
        lines.append(f"| [{record.title}]({relative}) | {record.kind} | {record.brief} |")
    return "\n".join(lines) + "\n", errors


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    docs_root = (root / args.docs_path).resolve()
    target = docs_root / "INDEX.md"
    rendered, errors = render(docs_root)
    if errors:
        for error in errors:
            print(f"ERROR\t{error}")
        return 1
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != rendered:
            print(f"ERROR\t{target}\tIndex is stale. Run generate_index.py without --check.")
            return 1
        print(f"Index is current: {target}")
        return 0
    target.write_text(rendered, encoding="utf-8")
    print(f"Wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
