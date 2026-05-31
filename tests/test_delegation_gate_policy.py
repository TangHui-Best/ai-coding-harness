from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


def skill_text(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class DelegationGatePolicyTests(unittest.TestCase):
    def test_start_gate_requires_explicit_delegation_decision_before_ready(self) -> None:
        content = skill_text("harness-start-gate")

        self.assertIn("Delegation Decision Readiness Rule", content)
        self.assertIn(
            "Do not return `ready` for `non-trivial` or `high-risk` work until the report includes an explicit Delegation decision.",
            content,
        )
        self.assertIn(
            "If Delegation Gate is skipped, the Start Gate outcome must be `blocked`, `needs clarification`, or another pre-work outcome instead of `ready`.",
            content,
        )

    def test_delegation_gate_defaults_to_decision_not_subagents(self) -> None:
        content = skill_text("harness-delegation-gate")

        self.assertIn("Default to an explicit delegation decision for non-trivial or high-risk work.", content)
        self.assertIn("Do not default to spawning subagents.", content)
        self.assertIn("Delegation Gate: single_agent | delegate | blocked", content)
        self.assertIn("Delegation target:", content)
        self.assertIn("long-running or unattended", content)

    def test_delegation_gate_uses_three_primary_outcomes(self) -> None:
        content = skill_text("harness-delegation-gate")

        self.assertIn("Return exactly one decision:", content)
        self.assertIn("`single_agent`", content)
        self.assertIn("`delegate`", content)
        self.assertIn("`blocked`", content)

        for old_status in [
            "`not needed`",
            "`ask user`",
            "`authorized`",
            "`declined`",
            "`required`",
            "`conditional`",
        ]:
            self.assertNotIn(old_status, content)

    def test_using_harness_routes_long_running_work_to_delegation_gate_early(self) -> None:
        content = skill_text("using-harness")

        self.assertIn(
            "If the user describes a long-running or unattended task, route to Delegation Gate early",
            content,
        )
        self.assertIn(
            "Start Gate must produce an explicit Delegation Gate decision before implementation may begin",
            content,
        )

    def test_readiness_dashboard_marks_missing_delegation_for_complex_work(self) -> None:
        content = skill_text("harness-readiness-dashboard")

        self.assertIn(
            "For `non-trivial` or `high-risk` work, mark `Delegation Gate` as `missing` when no explicit Delegation Gate decision is available.",
            content,
        )
        self.assertIn(
            "Do not convert missing Delegation Gate evidence into self-review just because implementation is already finished.",
            content,
        )
        self.assertIn("Delegation Gate: single_agent | delegate | missing | blocked", content)


if __name__ == "__main__":
    unittest.main()
