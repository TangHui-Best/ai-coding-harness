from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


def skill_text(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class GoalDrivenFeatureFlowTests(unittest.TestCase):
    def test_using_agentmentor_defines_goal_as_authorization_boundary(self) -> None:
        content = skill_text("using-agentmentor")

        self.assertIn("Goal-Driven Feature Flow", content)
        self.assertIn("Goal is the user authorization boundary", content)
        self.assertIn("Feature pages are engineering memory, not approval gates", content)
        self.assertIn("Do not require default per-Feature design approval", content)

    def test_start_gate_continues_with_feature_memory_inside_goal(self) -> None:
        content = skill_text("start-gate")

        self.assertIn("Goal-Driven Feature Flow", content)
        self.assertIn(
            "When a clear Goal authorizes a multi-Feature effort, creating or updating the Feature page is required memory, not a user approval checkpoint.",
            content,
        )
        self.assertIn(
            "Return `ready` when the next Feature slice is inside the approved Goal",
            content,
        )

    def test_start_gate_only_asks_user_for_goal_boundary_or_risk(self) -> None:
        content = skill_text("start-gate")

        for phrase in [
            "Goal is missing or ambiguous",
            "proposed Feature exceeds the approved Goal",
            "architecture, data model, security, cost, migration, or external contract",
            "acceptance criteria conflict",
            "patch churn suggests the direction may be wrong",
        ]:
            self.assertIn(phrase, content)

    def test_knowledge_capture_preserves_closeout_but_not_design_approval(self) -> None:
        content = skill_text("knowledge-capture")

        self.assertIn("Feature pages are engineering memory, not approval gates", content)
        self.assertIn("Do not require default per-Feature design approval", content)
        self.assertIn("This skill owns closeout and completion permission.", content)

    def test_empty_design_approval_requests_are_forbidden(self) -> None:
        using_agentmentor = skill_text("using-agentmentor")
        start_gate = skill_text("start-gate")

        for content in [using_agentmentor, start_gate]:
            self.assertIn("Empty Approval Guard", content)
            self.assertIn("Do not ask the user to approve a Feature, design, or plan that has not been created or shown.", content)
            self.assertIn("If the artifact is missing, the next action belongs to the agent", content)


if __name__ == "__main__":
    unittest.main()
