from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


def skill_text(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class HarnessBugfixRoutingContractTests(unittest.TestCase):
    def test_tiny_typo_fixture_does_not_require_retrieval(self) -> None:
        start_gate = skill_text("harness-start-gate")
        retrieval = skill_text("harness-knowledge-retrieval")

        self.assertIn("tiny typo", start_gate)
        self.assertIn("project memory cannot change the fix", start_gate)
        self.assertIn("If retrieval is not needed", start_gate)
        self.assertIn("Tiny local edits where existing project memory cannot change the outcome.", retrieval)

    def test_non_tiny_regression_fixture_requires_retrieval(self) -> None:
        using_harness = skill_text("using-harness")
        start_gate = skill_text("harness-start-gate")
        retrieval = skill_text("harness-knowledge-retrieval")

        self.assertIn("bug, regression, validation failure, or broken accepted behavior", using_harness)
        self.assertIn("non-tiny bug, regression, broken accepted behavior, or validation failure", start_gate)
        self.assertIn("return `needs retrieval` before code search or edits", start_gate)
        self.assertIn("Attributing a non-tiny bug, regression, accepted-behavior breakage", retrieval)

    def test_completed_feature_bugfix_fixture_updates_patch_history(self) -> None:
        start_gate = skill_text("harness-start-gate")
        capture = skill_text("harness-knowledge-capture")
        readiness = skill_text("harness-readiness-dashboard")

        self.assertIn("which Feature should receive the Patch History row after the fix", start_gate)
        self.assertIn("existing Feature <id>", capture)
        self.assertIn("update that Feature's `## Patch History`", capture)
        self.assertIn("existing completed Feature owners have an updated Patch History row", capture)
        self.assertIn("Patch History was not updated, readiness is `no` or `conditional`", readiness)


if __name__ == "__main__":
    unittest.main()
