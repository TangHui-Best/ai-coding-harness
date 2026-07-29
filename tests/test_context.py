from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "agentmentor" / "scripts" / "context.py"

FEATURE = """---
id: F001
doc_kind: feature
status: active
created: 2026-07-29
updated: 2026-07-29
owned_paths: [src/payments/]
trigger_terms: [payment, refund]
---
# F001: Payments
## Goal
Provide payment behavior.
## Scope
### In Scope
### Non-goals
## Specification
### Behavior
### Rules and Constraints
## Acceptance
- AC-01: refund is idempotent.
## Current State
Active.
## Links
### ADRs
- [ADR-001](../decisions/ADR-001-payment-idempotency.md)
### Lessons
- None.
### Evidence
- None.
### Related Features
- None.
### External Context
- None.
"""
ADR = """---
id: ADR-001
doc_kind: adr
status: accepted
feature_refs: [F001-payments]
decision_area: payments
applies_to_paths: [src/payments/]
trigger_terms: [refund]
created: 2026-07-29
updated: 2026-07-29
---
# ADR-001: Idempotency
## Context
## Decision
## Boundary
## Rejected Options
## Consequences
## Revisit When
## Links / Evidence
"""


class ContextTests(unittest.TestCase):
    def make_docs(self, root: Path) -> None:
        (root / "docs" / "features").mkdir(parents=True)
        (root / "docs" / "decisions").mkdir()
        (root / "docs" / "archive" / "v1" / "features").mkdir(parents=True)
        (root / "docs" / "features" / "F001-payments.md").write_text(FEATURE, encoding="utf-8")
        (root / "docs" / "decisions" / "ADR-001-payment-idempotency.md").write_text(ADR, encoding="utf-8")
        (root / "docs" / "archive" / "v1" / "features" / "F999-legacy.md").write_text("legacy refund history", encoding="utf-8")
        (root / "docs" / "features" / "INDEX.md").write_text(
            "| Feature | Status | Trigger Terms | Owned Paths | Read When |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| [F001 Payments](F001-payments.md) | active | payment, refund | `src/payments/` | Change payments. |\n",
            encoding="utf-8",
        )

    def run_context(self, root: Path, *arguments: str, task: str = "fix refund behavior") -> dict[str, object]:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), "--task", task, *arguments],
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(completed.stdout)

    def test_path_match_returns_feature_and_direct_adr_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_docs(root)
            result = self.run_context(root, "--path", "src/payments/refund.py")
        self.assertEqual("context", result["result"])
        self.assertEqual(["feature", "adr"], [item["kind"] for item in result["documents"]])
        self.assertLessEqual(len(result["documents"]), 3)
        self.assertNotIn("archive", "\n".join(item["path"] for item in result["documents"]))

    def test_no_match_exits_without_documents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_docs(root)
            result = self.run_context(root, "--path", "src/catalog/product.py", task="edit catalog metadata")
        self.assertEqual("no relevant context", result["result"])
        self.assertEqual([], result["documents"])
