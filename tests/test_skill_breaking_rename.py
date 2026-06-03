from __future__ import annotations

import re
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


FORMAL_SKILLS = [
    "ai-coding-harness",
    "ai-coding-harness-start-gate",
    "ai-coding-harness-delegation-gate",
    "ai-coding-harness-knowledge-retrieval",
    "ai-coding-harness-doc-lifecycle",
    "ai-coding-harness-incident-learning",
    "ai-coding-harness-vision-gate",
    "ai-coding-harness-readiness-dashboard",
    "ai-coding-harness-change-narrative",
    "ai-coding-harness-knowledge-capture",
    "ai-coding-harness-project-rules",
]

REMOVED_LEGACY_SKILLS = [
    "using-harness",
    "harness-start-gate",
    "harness-delegation-gate",
    "harness-knowledge-retrieval",
    "harness-doc-lifecycle",
    "harness-incident-learning",
    "harness-vision-gate",
    "harness-readiness-dashboard",
    "harness-change-narrative",
    "harness-knowledge-capture",
    "harness-project-rules",
]


def frontmatter_name(skill_file: Path) -> str:
    content = skill_file.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    if not match:
        raise AssertionError(f"missing name frontmatter: {skill_file}")
    return match.group(1).strip().strip("'\"")


class SkillBreakingRenameTests(unittest.TestCase):
    def test_formal_ai_coding_harness_skill_directories_exist(self) -> None:
        for skill in FORMAL_SKILLS:
            with self.subTest(skill=skill):
                skill_file = SKILLS / skill / "SKILL.md"
                self.assertTrue(skill_file.exists(), f"missing formal skill: {skill}")
                self.assertEqual(frontmatter_name(skill_file), skill)

    def test_legacy_harness_skill_directories_are_removed(self) -> None:
        for skill in REMOVED_LEGACY_SKILLS:
            with self.subTest(skill=skill):
                self.assertFalse((SKILLS / skill).exists(), f"legacy skill remains: {skill}")

    def test_display_headings_use_ai_coding_harness_prefix(self) -> None:
        expected_headings = {
            "ai-coding-harness": "# AI Coding Harness",
            "ai-coding-harness-start-gate": "# AI Coding Harness Start Gate",
            "ai-coding-harness-delegation-gate": "# AI Coding Harness Delegation Gate",
            "ai-coding-harness-knowledge-retrieval": "# AI Coding Harness Knowledge Retrieval",
            "ai-coding-harness-doc-lifecycle": "# AI Coding Harness Doc Lifecycle",
            "ai-coding-harness-incident-learning": "# AI Coding Harness Incident Learning",
            "ai-coding-harness-vision-gate": "# AI Coding Harness Vision Gate",
            "ai-coding-harness-readiness-dashboard": "# AI Coding Harness Readiness Dashboard",
            "ai-coding-harness-change-narrative": "# AI Coding Harness Change Narrative",
            "ai-coding-harness-knowledge-capture": "# AI Coding Harness Knowledge Capture",
            "ai-coding-harness-project-rules": "# AI Coding Harness Project Rules",
        }

        for skill, heading in expected_headings.items():
            with self.subTest(skill=skill):
                content = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(heading, content)
                if skill != "ai-coding-harness":
                    self.assertNotIn("# Harness ", content)

    def test_agent_display_names_use_ai_coding_harness_prefix(self) -> None:
        agent_file = (
            SKILLS
            / "ai-coding-harness-delegation-gate"
            / "agents"
            / "openai.yaml"
        )
        content = agent_file.read_text(encoding="utf-8")

        self.assertIn('display_name: "AI Coding Harness Delegation Gate"', content)
        self.assertNotIn('display_name: "Harness Delegation Gate"', content)


if __name__ == "__main__":
    unittest.main()
