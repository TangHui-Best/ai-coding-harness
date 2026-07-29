from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "knowledge_check.py"

VALID_FEATURE = """---
id: F001
doc_kind: feature
status: active
created: 2026-07-29
updated: 2026-07-29
owned_paths: [src/example/]
trigger_terms: [example]
---
# F001: Example
## Goal
Goal.
## Scope
### In Scope
### Non-goals
## Specification
### Behavior
### Rules and Constraints
## Acceptance
- AC-01.
## Current State
Active.
## Links
### ADRs
- None.
### Lessons
- None.
### Evidence
- None.
### Related Features
- None.
### External Context
- None.
"""


class KnowledgeCheckTests(unittest.TestCase):
    def make_docs(self, root: Path, feature: str = VALID_FEATURE) -> None:
        features = root / "docs" / "features"
        features.mkdir(parents=True)
        (features / "F001-example.md").write_text(feature, encoding="utf-8")
        (features / "INDEX.md").write_text(
            "| Feature | Status | Trigger Terms | Owned Paths | Read When |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| [F001 Example](F001-example.md) | active | example | `src/example/` | Example work. |\n",
            encoding="utf-8",
        )

    def run_check(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(root), "--docs-path", "docs", "--strict"], text=True, capture_output=True)

    def test_accepts_vnext_schema_and_ignores_archive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_docs(root)
            archive = root / "docs" / "archive" / "v1" / "features"
            archive.mkdir(parents=True)
            (archive / "F999-legacy.md").write_text("not a vNext artifact", encoding="utf-8")
            result = self.run_check(root)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_rejects_missing_feature_specification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_docs(root, VALID_FEATURE.replace("## Specification\n### Behavior\n### Rules and Constraints\n", ""))
            result = self.run_check(root)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Missing required section: ## Specification.", result.stdout)

