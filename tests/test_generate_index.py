from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "agentmentor" / "scripts" / "generate_index.py"

FEATURE = """---
id: F001
doc_kind: feature
status: active
index_summary: Defines refund behavior; duplicate refunds are rejected.
created: 2026-08-27
updated: 2026-08-27
---
# F001: Payments
"""
DELIVERED_FEATURE = FEATURE.replace("F001", "F002").replace("active", "delivered").replace("Payments", "Settlement")
DRAFT_FEATURE = FEATURE.replace("status: active", "status: draft").replace("Payments", "Draft payments")
ADR = """---
id: ADR-001
doc_kind: adr
status: accepted
index_summary: Refunds are idempotent at the payment-provider boundary.
feature_refs: [F001]
decision_area: payments
supersedes: []
created: 2026-08-27
updated: 2026-08-27
---
# ADR-001: Refund idempotency
"""
PROPOSED_ADR = ADR.replace("status: accepted", "status: proposed").replace("Refund idempotency", "Future refund design")


class GenerateIndexTests(unittest.TestCase):
    def make_docs(self, root: Path) -> None:
        features = root / "docs" / "features"
        decisions = root / "docs" / "decisions"
        features.mkdir(parents=True)
        decisions.mkdir()
        (features / "F001-payments.md").write_text(FEATURE, encoding="utf-8")
        (features / "F002-settlement.md").write_text(DELIVERED_FEATURE, encoding="utf-8")
        (features / "F003-draft.md").write_text(DRAFT_FEATURE, encoding="utf-8")
        (decisions / "ADR-001-refunds.md").write_text(ADR, encoding="utf-8")
        (decisions / "ADR-002-proposed.md").write_text(PROPOSED_ADR.replace("ADR-001", "ADR-002"), encoding="utf-8")

    def run_generator(self, root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(root), *arguments], text=True, capture_output=True)

    def test_generates_one_compact_index_for_effective_features_and_adrs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_docs(root)
            result = self.run_generator(root)
            index = (root / "docs" / "INDEX.md").read_text(encoding="utf-8")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("| Document | Type | Brief |", index)
        self.assertIn("F001: Payments", index)
        self.assertIn("F002: Settlement", index)
        self.assertIn("ADR-001: Refund idempotency", index)
        self.assertNotIn("Draft payments", index)
        self.assertNotIn("Future refund design", index)
        self.assertNotIn("Status", index)

    def test_check_rejects_a_stale_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_docs(root)
            self.assertEqual(0, self.run_generator(root).returncode)
            (root / "docs" / "features" / "F001-payments.md").write_text(FEATURE.replace("duplicate refunds", "retries"), encoding="utf-8")
            result = self.run_generator(root, "--check")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Index is stale", result.stdout)
