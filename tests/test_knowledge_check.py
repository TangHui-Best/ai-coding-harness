from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "knowledge_check.py"


def feature_doc(extra: str = "") -> str:
    return f"""---
id: F010
doc_kind: feature
status: active
created: 2026-05-18
updated: 2026-05-18
---

# F010: Export Reports

## Goal

Keep export reports reliable.

## Vision Anchor

- Original request or source: test fixture.
- User pain point or engineering problem: exports regress after completion.
- Desired outcome: patch history is visible and reviewable.
- Non-goals or boundaries: no new export subsystem.
- Exit Gate source: this Feature page.

## Current Status

Active.

## Links

None.

## Acceptance Criteria

- [ ] Export regressions are tracked.

## Patch History

{extra}

## Evidence

Final response or linked Evidence.

## Next Step

Continue only after gate checks pass.
"""


def run_check(docs: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(docs.parent), "--docs-path", docs.name],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class KnowledgeCheckPatchHistoryTests(unittest.TestCase):
    def test_rejects_patch_history_row_without_feature_patch_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            (features / "F010-export-reports.md").write_text(
                feature_doc(
                    "| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |\n"
                    "| --- | --- | --- | --- | --- | --- | --- |\n"
                    "| bugfix | 2026-05-18 | abc123 | export failed | missing invariant | test | closed |\n"
                ),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Patch History row uses invalid patch id", result.stdout)

    def test_rejects_three_patch_rows_without_patch_churn_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            (features / "F010-export-reports.md").write_text(
                feature_doc(
                    "| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |\n"
                    "| --- | --- | --- | --- | --- | --- | --- |\n"
                    "| F010.1 | 2026-05-18 | abc123 | first failure | root one | test | closed |\n"
                    "| F010.2 | 2026-05-18 | def456 | second failure | root two | test | closed |\n"
                    "| F010.3 | 2026-05-18 | ghi789 | third failure | root three | test | active |\n"
                ),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("has 3 Patch History entries but no ## Patch Churn Review", result.stdout)

    def test_allows_three_patch_rows_with_patch_churn_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            (features / "F010-export-reports.md").write_text(
                feature_doc(
                    "| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |\n"
                    "| --- | --- | --- | --- | --- | --- | --- |\n"
                    "| F010.1 | 2026-05-18 | abc123 | first failure | root one | test | closed |\n"
                    "| F010.2 | 2026-05-18 | def456 | second failure | root two | test | closed |\n"
                    "| F010.3 | 2026-05-18 | ghi789 | third failure | root three | Vision Gate | active |\n"
                    "\n"
                    "## Patch Churn Review\n"
                    "\n"
                    "Three follow-up fixes triggered review. The next action is Vision Gate.\n"
                ),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
