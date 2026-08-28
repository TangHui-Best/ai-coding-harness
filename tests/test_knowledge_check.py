from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "knowledge_check.py"
GENERATOR = REPO_ROOT / "scripts" / "generate_index.py"

VALID_FEATURE = """---
id: F001
doc_kind: feature
status: active
index_summary: Defines example behavior and its explicit boundary.
created: 2026-08-27
updated: 2026-08-27
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
        result = subprocess.run([sys.executable, str(GENERATOR), "--root", str(root)], text=True, capture_output=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def run_check(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(root), "--docs-path", "docs", "--strict"], text=True, capture_output=True)

    def test_accepts_schema_and_ignores_archive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_docs(root)
            archive = root / "docs" / "archive" / "v1" / "features"
            archive.mkdir(parents=True)
            (archive / "F999-legacy.md").write_text("not a vNext artifact", encoding="utf-8")
            result = self.run_check(root)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_rejects_missing_index_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_docs(root)
            (root / "docs" / "features" / "F001-example.md").write_text(
                VALID_FEATURE.replace("index_summary: Defines example behavior and its explicit boundary.\n", ""),
                encoding="utf-8",
            )
            result = self.run_check(root)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Missing required field: index_summary.", result.stdout)
