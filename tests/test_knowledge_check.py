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

## Feature Intake

- Original problem: export reliability needs a durable owner.
- User pain point: completed exports can regress without attribution.
- Capability promise: export regressions are tracked through this Feature.
- Non-goals: no new export subsystem.
- Acceptance source: this Feature page.
- Open questions: none.

## Capability Contract

- Export report behavior has a durable recovery and patch attribution entrypoint.

## Decision Context

### Why

Export behavior needs a durable owner because regressions can appear after completion.

### Why Not

Do not create a new Feature for each export regression because patch attribution belongs to the owning Feature.

### If Modifying This Area, Check

- Check linked Evidence and Patch History before changing export behavior.

## Current Status

Active.

## Links

### Evidence

- Final response or linked Evidence.

### Decisions / ADRs

- None.

### Lessons

- None.

### Specs / Plans

- None.

### Related Features

- None.

### External Context

- None.

## Acceptance Criteria

- [ ] Export regressions are tracked.

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| Export regressions are tracked | Patch history rows identify follow-up fixes | Final response or linked Evidence | active |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-05-18 | active | test fixture | Final response | Initial state |

## Patch History

{extra}

## Evidence

Final response or linked Evidence.

## Recovery Snapshot

- Read first: this Feature page.
- Current capability state: active test fixture.
- Known risks: none.
- Next safe action: continue only after gate checks pass.
- Unblock condition: not blocked.

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

## Feature Intake

- Original problem: export reliability needs a durable owner.
- User pain point: completed exports can regress without attribution.
- Capability promise: export regressions are tracked through this Feature.
- Non-goals: no new export subsystem.
- Acceptance source: this Feature page.
- Open questions: none.

## Capability Contract

- Export report behavior has a durable recovery and patch attribution entrypoint.

## Decision Context

### Why

Export behavior needs a durable owner because regressions can appear after completion.

### Why Not

Do not create a new Feature for each export regression because patch attribution belongs to the owning Feature.

### If Modifying This Area, Check

- Check linked Evidence and Patch History before changing export behavior.

## Current Status

Active.

## Links

### Evidence

- Final response or linked Evidence.

### Decisions / ADRs

- None.

### Lessons

- None.

### Specs / Plans

- None.

### Related Features

- None.

### External Context

- None.

## Acceptance Criteria

- [ ] Export regressions are tracked.

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| Export regressions are tracked | Patch history rows identify follow-up fixes | Final response or linked Evidence | active |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-05-18 | active | test fixture | Final response | Initial state |

## Patch History

{extra}

## Evidence

Final response or linked Evidence.

## Recovery Snapshot

- Read first: this Feature page.
- Current capability state: active test fixture.
- Known risks: none.
- Next safe action: continue only after gate checks pass.
- Unblock condition: not blocked.

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


def lesson_doc() -> str:
    return """---
id: LL-010
doc_kind: lesson
status: active
scope: project
feature_refs: []
applies_to: [exports, reports]
created: 2026-05-18
updated: 2026-05-18
---

# LL-010: Export Report Protection

## Case

Export report validation failed after a completed workflow changed.

## Resolution

The report validation path was stabilized and documented.

## Pitfall

Do not treat repeated export report failures as unrelated local bugs.

## Root Cause

The owning Feature and prior validation evidence were not checked first.

## Protection

Run the owning Feature retrieval and linked Evidence checks before changing export report behavior.

## Source

Final response or linked Evidence.

## Principle

Repeated failures should be attributed before patching.
"""


def adr_doc() -> str:
    return """---
id: ADR-010
doc_kind: adr
status: accepted
scope: project
feature_refs: []
decision_area: test-decision
created: 2026-05-18
updated: 2026-05-18
---

# ADR-010: Test Decision Boundary

## Context

A durable test decision needs a recoverable rationale.

## Decision

Use the accepted test decision.

## Decision Boundary

### Applies To

- Test ADR validation fixtures.

### Does Not Apply To

- Production runtime behavior.

## Rejected Options

- Keep the old structure: rejected because it does not capture decision boundaries.

## Consequences

Future readers can see the accepted tradeoff and its cost.

## Before Changing This Decision

Check the linked Feature, Evidence, validator expectations, and affected ADR docs.

## Evidence

Final response or linked Evidence.
"""


def feature_index(*rows: str) -> str:
    return (
        "# Feature Index\n\n"
        "Use this file as the coarse recall entry before opening Feature pages.\n\n"
        "| Feature | Domain | Trigger Terms | Owned Paths | Read When |\n"
        "| --- | --- | --- | --- | --- |\n"
        + "".join(rows)
    )


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


class KnowledgeCheckFeatureGovernanceTests(unittest.TestCase):
    def test_allows_feature_index_without_artifact_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            (features / "INDEX.md").write_text(
                "# Feature Index\n\n| Feature | Domain |\n| --- | --- |\n",
                encoding="utf-8",
            )
            (features / "F010-export-reports.md").write_text(
                feature_doc(),
                encoding="utf-8",
            )

            result = run_check(docs, "--all-markdown")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Checked 1 knowledge artifact(s)", result.stdout)

    def test_rejects_feature_without_feature_intake(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            content = feature_doc().replace(
                "## Feature Intake\n\n"
                "- Original problem: export reliability needs a durable owner.\n"
                "- User pain point: completed exports can regress without attribution.\n"
                "- Capability promise: export regressions are tracked through this Feature.\n"
                "- Non-goals: no new export subsystem.\n"
                "- Acceptance source: this Feature page.\n"
                "- Open questions: none.\n\n",
                "",
            )
            (features / "F010-export-reports.md").write_text(content, encoding="utf-8")

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required section: ## Feature Intake", result.stdout)

    def test_rejects_feature_without_decision_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            start = feature_doc().index("## Decision Context")
            end = feature_doc().index("## Current Status")
            content = feature_doc()[:start] + feature_doc()[end:]
            (features / "F010-export-reports.md").write_text(content, encoding="utf-8")

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required section: ## Decision Context", result.stdout)

    def test_rejects_feature_intake_missing_required_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            content = feature_doc().replace(
                "- Open questions: none.\n",
                "",
            )
            (features / "F010-export-reports.md").write_text(content, encoding="utf-8")

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Feature Intake must answer Open questions", result.stdout)

    def test_rejects_ready_feature_acceptance_map_without_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            content = (
                feature_doc()
                .replace("status: active", "status: ready_for_review")
                .replace(
                    "| Export regressions are tracked | Patch history rows identify follow-up fixes | Final response or linked Evidence | active |",
                    "| Export regressions are tracked | Patch history rows identify follow-up fixes | TBD | ready_for_review |",
                )
            )
            (features / "F010-export-reports.md").write_text(content, encoding="utf-8")

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "ready-for-review feature F010 has Acceptance Map row without Evidence",
            result.stdout,
        )

    def test_rejects_blocked_feature_without_unblock_condition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            content = (
                feature_doc()
                .replace("status: active", "status: blocked")
                .replace("- Unblock condition: not blocked.\n", "")
            )
            (features / "F010-export-reports.md").write_text(content, encoding="utf-8")

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("blocked feature F010 Recovery Snapshot must include Unblock condition", result.stdout)

    def test_rejects_feature_links_without_required_categories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            start = feature_doc().index("## Links")
            end = feature_doc().index("## Acceptance Criteria")
            content = (
                feature_doc()[:start]
                + "## Links\n\n- [EV-010](../evidence/EV-010-export-reports.md)\n\n"
                + feature_doc()[end:]
            )
            (features / "F010-export-reports.md").write_text(content, encoding="utf-8")

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Links must include category: ### Evidence", result.stdout)


class KnowledgeCheckFeatureIndexTests(unittest.TestCase):
    def test_feature_index_local_check_accepts_current_feature_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            (features / "INDEX.md").write_text(
                feature_index(
                    "| [F010](F010-export-reports.md) | exports | export, reports, regression | `exports/` | read when export reports change |\n"
                ),
                encoding="utf-8",
            )
            (features / "F010-export-reports.md").write_text(feature_doc(), encoding="utf-8")

            result = run_check(docs, "--feature-index", "F010-export-reports")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_feature_index_local_check_rejects_missing_current_feature_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            (features / "INDEX.md").write_text(
                feature_index(
                    "| [F011](F011-import-reports.md) | imports | import, reports | `imports/` | read when import reports change |\n"
                ),
                encoding="utf-8",
            )
            (features / "F010-export-reports.md").write_text(feature_doc(), encoding="utf-8")
            (features / "F011-import-reports.md").write_text(
                feature_doc_with_id("F011"),
                encoding="utf-8",
            )

            result = run_check(docs, "--feature-index", "F010-export-reports")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Feature Index missing local Feature entry: F010-export-reports", result.stdout)

    def test_feature_index_local_check_rejects_duplicate_current_feature_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            (features / "INDEX.md").write_text(
                feature_index(
                    "| [F010](F010-export-reports.md) | exports | export, reports | `exports/` | read when export reports change |\n"
                    "| [F010 again](F010-export-reports.md) | exports | regression | `exports/` | read when regressions appear |\n"
                ),
                encoding="utf-8",
            )
            (features / "F010-export-reports.md").write_text(feature_doc(), encoding="utf-8")

            result = run_check(docs, "--feature-index", "F010-export-reports")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Feature Index has duplicate local Feature entry: F010-export-reports", result.stdout)

    def test_feature_index_global_audit_is_explicit_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            features = docs / "features"
            features.mkdir(parents=True)
            (features / "INDEX.md").write_text(
                feature_index(
                    "| [F010](F010-export-reports.md) | exports | export, reports | `exports/` | read when export reports change |\n"
                ),
                encoding="utf-8",
            )
            (features / "F010-export-reports.md").write_text(feature_doc(), encoding="utf-8")
            (features / "F011-import-reports.md").write_text(
                feature_doc_with_id("F011"),
                encoding="utf-8",
            )

            default_result = run_check(docs)
            global_result = run_check(docs, "--feature-index-all")

        self.assertEqual(default_result.returncode, 0, default_result.stdout + default_result.stderr)
        self.assertNotEqual(global_result.returncode, 0)
        self.assertIn("Feature Index missing active/completed Feature entry: F011-import-reports", global_result.stdout)


class KnowledgeCheckLessonGovernanceTests(unittest.TestCase):
    def test_allows_lesson_case_resolution_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            lessons = docs / "lessons"
            lessons.mkdir(parents=True)
            (lessons / "LL-010-export-report-protection.md").write_text(
                lesson_doc(),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_lesson_without_case(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            lessons = docs / "lessons"
            lessons.mkdir(parents=True)
            content = lesson_doc().replace(
                "## Case\n\nExport report validation failed after a completed workflow changed.\n\n",
                "",
            )
            (lessons / "LL-010-export-report-protection.md").write_text(
                content,
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required section: ## Case", result.stdout)

    def test_rejects_lesson_without_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            lessons = docs / "lessons"
            lessons.mkdir(parents=True)
            content = lesson_doc().replace(
                "## Resolution\n\nThe report validation path was stabilized and documented.\n\n",
                "",
            )
            (lessons / "LL-010-export-report-protection.md").write_text(
                content,
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required section: ## Resolution", result.stdout)


class KnowledgeCheckAdrGovernanceTests(unittest.TestCase):
    def test_allows_adr_decision_boundary_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            decisions = docs / "decisions"
            decisions.mkdir(parents=True)
            (decisions / "ADR-010-test-decision-boundary.md").write_text(
                adr_doc(),
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_adr_without_decision_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            decisions = docs / "decisions"
            decisions.mkdir(parents=True)
            start = adr_doc().index("## Decision Boundary")
            end = adr_doc().index("## Rejected Options")
            content = adr_doc()[:start] + adr_doc()[end:]
            (decisions / "ADR-010-test-decision-boundary.md").write_text(
                content,
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required section: ## Decision Boundary", result.stdout)

    def test_rejects_adr_without_rejected_options(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            decisions = docs / "decisions"
            decisions.mkdir(parents=True)
            content = adr_doc().replace(
                "## Rejected Options\n\n"
                "- Keep the old structure: rejected because it does not capture decision boundaries.\n\n",
                "",
            )
            (decisions / "ADR-010-test-decision-boundary.md").write_text(
                content,
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required section: ## Rejected Options", result.stdout)

    def test_rejects_adr_without_before_changing_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            decisions = docs / "decisions"
            decisions.mkdir(parents=True)
            content = adr_doc().replace(
                "## Before Changing This Decision\n\n"
                "Check the linked Feature, Evidence, validator expectations, and affected ADR docs.\n\n",
                "",
            )
            (decisions / "ADR-010-test-decision-boundary.md").write_text(
                content,
                encoding="utf-8",
            )

            result = run_check(docs)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required section: ## Before Changing This Decision", result.stdout)


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
