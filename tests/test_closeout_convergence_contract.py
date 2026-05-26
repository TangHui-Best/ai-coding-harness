from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


def skill_text(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class CloseoutConvergenceContractTests(unittest.TestCase):
    def test_using_harness_defines_terminal_closeout_and_no_reentry(self) -> None:
        content = skill_text("using-harness")

        self.assertIn("Closeout Convergence Protocol", content)
        self.assertIn("Do not re-enter `using-harness`", content)
        self.assertIn("closeout is terminal", content)
        self.assertIn("Do not route a normal final response to `harness-change-narrative`", content)

    def test_knowledge_capture_owns_completion_verdict(self) -> None:
        content = skill_text("harness-knowledge-capture")

        self.assertIn("Completion Verdict Ownership", content)
        self.assertIn("This skill owns the completion verdict", content)
        self.assertIn("A `pass` or permitted `conditional` verdict is terminal", content)
        self.assertIn("consume that evidence instead of re-running equivalent checks", content)

    def test_terminal_closeout_still_requires_visible_status(self) -> None:
        content = skill_text("harness-knowledge-capture")

        self.assertIn("Terminal Closeout Output", content)
        self.assertIn("Terminal means no recursion, not invisible", content)
        self.assertIn("visible closeout status", content)
        self.assertIn("A structural `harness_closeout_check.py` pass is not a substitute", content)
        self.assertIn("compact closeout block", content)

    def test_change_narrative_does_not_trigger_on_normal_final_response(self) -> None:
        content = skill_text("harness-change-narrative")

        self.assertIn("Normal Final Response Boundary", content)
        self.assertIn("does not by itself trigger this skill", content)
        self.assertIn("Do not re-enter `harness-knowledge-capture`", content)


if __name__ == "__main__":
    unittest.main()
