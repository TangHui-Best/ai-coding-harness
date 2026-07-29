#!/usr/bin/env python3
"""Return one bounded AgentMentor vNext context package."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Candidate:
    path: Path
    score: int
    reasons: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--docs-path", default="docs")
    parser.add_argument("--task", required=True)
    parser.add_argument("--path", action="append", default=[], dest="paths")
    parser.add_argument("--format", choices=("json", "text"), default="json")
    return parser.parse_args()


def normalize(value: str) -> str:
    return value.replace("\\", "/").strip().lower().strip("`")


def tokens(value: str) -> set[str]:
    return {part for part in re.findall(r"[a-z0-9][a-z0-9._/-]*", normalize(value)) if len(part) > 1}


def parse_table(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    headers: list[str] | None = None
    rows: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        lowered = [cell.lower() for cell in cells]
        if headers is None and "feature" in lowered:
            headers = lowered
        elif headers is not None and len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def linked_target(cell: str) -> str | None:
    matched = re.search(r"\[[^]]+\]\(([^)#]+)", cell)
    return matched.group(1) if matched else None


def frontmatter(content: str) -> dict[str, str]:
    if not content.startswith("---\n"):
        return {}
    end = content.find("\n---\n", 4)
    if end < 0:
        return {}
    data: dict[str, str] = {}
    active: str | None = None
    items: list[str] = []

    def flush() -> None:
        nonlocal active, items
        if active is not None:
            data[active] = "[" + ", ".join(items) + "]"
        active, items = None, []

    for line in content[4:end].splitlines():
        value = line.strip()
        if active is not None and value.startswith("- "):
            items.append(value[2:].strip().strip("'\""))
            continue
        flush()
        matched = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", value)
        if matched:
            key, raw = matched.groups()
            if raw.strip():
                data[key] = raw.strip().strip("'\"")
            else:
                active = key
    flush()
    return data


def markdown_links(content: str, source: Path) -> list[Path]:
    targets: list[Path] = []
    for matched in re.finditer(r"\[[^]]+\]\(([^)#]+)", content):
        target = matched.group(1)
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
            continue
        path = (source.parent / target).resolve()
        if path.suffix == ".md" and path.exists():
            targets.append(path)
    return targets


def score_row(row: dict[str, str], task: str, known_paths: list[str]) -> Candidate | None:
    target = linked_target(row.get("feature", ""))
    if target is None:
        return None
    task_tokens = tokens(task)
    trigger_tokens = tokens(row.get("trigger terms", ""))
    owned_paths = [normalize(value) for value in re.findall(r"`([^`]+)`", row.get("owned paths", ""))]
    if not owned_paths:
        owned_paths = [normalize(value) for value in row.get("owned paths", "").split(",") if value.strip()]
    score, reasons = 0, []
    for known in known_paths:
        for owned in owned_paths:
            if known == owned or known.startswith(owned.rstrip("/") + "/"):
                score += 100
                reasons.append(f"path:{owned}")
                break
    overlap = task_tokens & trigger_tokens
    if overlap:
        score += min(30, len(overlap) * 10)
        reasons.append("terms:" + ",".join(sorted(overlap)))
    if not score:
        return None
    return Candidate(Path(target), score, reasons)


def document_payload(path: Path, docs_root: Path, reason: str) -> dict[str, object]:
    content = path.read_text(encoding="utf-8")
    fields = frontmatter(content)
    return {
        "path": path.relative_to(docs_root.parent).as_posix(),
        "kind": fields.get("doc_kind", "unknown"),
        "id": fields.get("id", path.stem),
        "reason": reason,
        "content": content,
    }


def retrieve(root: Path, docs_root: Path, task: str, paths: list[str]) -> dict[str, object]:
    rows = parse_table(docs_root / "features" / "INDEX.md")
    known_paths = [normalize(path) for path in paths]
    candidates: list[Candidate] = []
    for row in rows:
        candidate = score_row(row, task, known_paths)
        if candidate is not None:
            candidate.path = (docs_root / "features" / candidate.path).resolve()
            if candidate.path.exists():
                candidates.append(candidate)
    if not candidates:
        return {"result": "no relevant context", "documents": [], "reason": "no path or trigger-term match in Feature Index"}
    candidates.sort(key=lambda item: (-item.score, item.path.name))
    selected = candidates[0]
    documents = [document_payload(selected.path, docs_root, "; ".join(selected.reasons))]
    linked_paths: set[Path] = set()
    for linked in markdown_links(documents[0]["content"], selected.path):
        if linked in linked_paths:
            continue
        linked_paths.add(linked)
        fields = frontmatter(linked.read_text(encoding="utf-8"))
        if fields.get("doc_kind") not in {"adr", "lesson", "evidence"}:
            continue
        documents.append(document_payload(linked, docs_root, f"direct link from {selected.path.stem}"))
        if len(documents) == 3:
            break
    return {"result": "context", "documents": documents, "reason": "bounded Feature-first retrieval"}


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    docs_root = Path(args.docs_path)
    docs_root = (root / docs_root if not docs_root.is_absolute() else docs_root).resolve()
    result = retrieve(root, docs_root, args.task, args.paths)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["result"])
        print(result["reason"])
        for document in result["documents"]:
            print(f"- {document['path']} ({document['kind']}): {document['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
