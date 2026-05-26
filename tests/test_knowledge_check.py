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


def feature_doc_with_id(doc_id: str, extra_frontmatter: str = "", extra: str = "") -> str:
    return f"""---
id: {doc_id}
doc_kind: feature
status: active
created: 2026-05-18
updated: 2026-05-18
{extra_frontmatter}---

# {doc_id}: Export Reports

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


def evidence_doc(feature_refs: str) -> str:
    return f"""---
id: EV-010
doc_kind: evidence
scope: feature
feature_refs: {feature_refs}
created: 2026-05-18
---

# EV-010: Export Reports

## Commands

`python scripts/knowledge_check.py --root . --docs-path docs`

## Results

Passed.

## Artifacts

None.

## Notes

Feature relationship is expressed through feature_refs.
"""


def evidence_doc_with_frontmatter(feature_refs_frontmatter: str) -> str:
    return f"""---
id: EV-010
doc_kind: evidence
scope: feature
{feature_refs_frontmatter}
created: 2026-05-18
---

# EV-010: Export Reports

## Commands

`python scripts/knowledge_check.py --root . --docs-path docs`

## Results

Passed.

## Artifacts

None.

## Notes

Feature relationship is expressed through feature_refs.
"""


def run_check(docs: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(docs.parent),
            "--docs-path",
            docs.name,
            *extra_args,
        ],
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


class KnowledgeCheckFeatureRefsTests(unittest.TestCase):
    def test_allows_feature_refs_to_resolve_feature_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            evidence = docs / "evidence"
            features.mkdir(parents=True)
            evidence.mkdir(parents=True)
            (features / "F023-export-reports.md").write_text(
                feature_doc_with_id("F023"),
                encoding="utf-8",
            )
            (evidence / "EV-010-export-reports.md").write_text(
                evidence_doc("[docs/features/F023-export-reports.md]"),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_allows_feature_refs_to_resolve_feature_file_stem(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            evidence = docs / "evidence"
            features.mkdir(parents=True)
            evidence.mkdir(parents=True)
            (features / "F023-export-reports.md").write_text(
                feature_doc_with_id("F023"),
                encoding="utf-8",
            )
            (evidence / "EV-010-export-reports.md").write_text(
                evidence_doc("[F023-export-reports]"),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_completed_feature_closeout_accepts_evidence_via_path_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            evidence = docs / "evidence"
            features.mkdir(parents=True)
            evidence.mkdir(parents=True)
            (features / "F023-export-reports.md").write_text(
                feature_doc_with_id("F023").replace("status: active", "status: completed"),
                encoding="utf-8",
            )
            (evidence / "EV-010-export-reports.md").write_text(
                evidence_doc("[docs/features/F023-export-reports.md]"),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_allows_feature_refs_as_yaml_block_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            evidence = docs / "evidence"
            features.mkdir(parents=True)
            evidence.mkdir(parents=True)
            (features / "F023-export-reports.md").write_text(
                feature_doc_with_id("F023").replace("status: active", "status: completed"),
                encoding="utf-8",
            )
            (evidence / "EV-010-export-reports.md").write_text(
                evidence_doc_with_frontmatter(
                    "feature_refs:\n"
                    "  - docs/features/F023-export-reports.md\n"
                ),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_allows_duplicate_short_feature_ids_when_refs_use_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            evidence = docs / "evidence"
            features.mkdir(parents=True)
            evidence.mkdir(parents=True)
            (features / "F001-export-reports.md").write_text(
                feature_doc_with_id("F001"),
                encoding="utf-8",
            )
            (features / "F001-import-reports.md").write_text(
                feature_doc_with_id("F001"),
                encoding="utf-8",
            )
            (evidence / "EV-010-export-reports.md").write_text(
                evidence_doc("[docs/features/F001-export-reports.md]"),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_warns_for_bare_short_feature_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            evidence = docs / "evidence"
            features.mkdir(parents=True)
            evidence.mkdir(parents=True)
            (features / "F023-export-reports.md").write_text(
                feature_doc_with_id("F023"),
                encoding="utf-8",
            )
            (evidence / "EV-010-export-reports.md").write_text(
                evidence_doc("[F023]"),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Bare feature_ref 'F023' is ambiguous across branches", result.stdout)

    def test_rejects_ambiguous_bare_short_feature_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            evidence = docs / "evidence"
            features.mkdir(parents=True)
            evidence.mkdir(parents=True)
            (features / "F001-export-reports.md").write_text(
                feature_doc_with_id("F001"),
                encoding="utf-8",
            )
            (features / "F001-import-reports.md").write_text(
                feature_doc_with_id("F001"),
                encoding="utf-8",
            )
            (evidence / "EV-010-export-reports.md").write_text(
                evidence_doc("[F001]"),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Ambiguous bare feature_ref 'F001'", result.stdout)

    def test_rejects_unresolved_feature_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            evidence = docs / "evidence"
            evidence.mkdir(parents=True)
            (evidence / "EV-010-export-reports.md").write_text(
                evidence_doc("[docs/features/F023-missing-feature.md]"),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("References missing feature_ref", result.stdout)


class KnowledgeCheckPlacementTests(unittest.TestCase):
    def test_rejects_unsupported_doc_kind_outside_harness_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            specs = docs / "superpowers" / "specs"
            specs.mkdir(parents=True)
            (specs / "2026-05-25-public-hygiene-gate.md").write_text(
                """---
doc_kind: spec
status: active
created: 2026-05-25
feature_refs: []
---

# Public Hygiene Gate
""",
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported doc_kind 'spec'", result.stdout)

    def test_rejects_harness_artifact_outside_canonical_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            evidence = docs / "superpowers" / "evidence"
            evidence.mkdir(parents=True)
            (evidence / "2026-05-25-public-hygiene-gate.md").write_text(
                evidence_doc("[]"),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence artifact must live under docs/evidence/", result.stdout)


if __name__ == "__main__":
    unittest.main()
