from __future__ import annotations

import re
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


FORMAL_SKILLS = [
    "using-agentmentor",
    "start-gate",
    "delegation-gate",
    "knowledge-retrieval",
    "doc-lifecycle",
    "incident-learning",
    "vision-gate",
    "readiness-dashboard",
    "change-narrative",
    "knowledge-capture",
    "project-rules",
]

REMOVED_LEGACY_SKILLS = [
    "using-harness",
    "ai-coding-harness",
    "harness-start-gate",
    "ai-coding-harness-start-gate",
    "harness-delegation-gate",
    "ai-coding-harness-delegation-gate",
    "harness-knowledge-retrieval",
    "ai-coding-harness-knowledge-retrieval",
    "harness-doc-lifecycle",
    "ai-coding-harness-doc-lifecycle",
    "harness-incident-learning",
    "ai-coding-harness-incident-learning",
    "harness-vision-gate",
    "ai-coding-harness-vision-gate",
    "harness-readiness-dashboard",
    "ai-coding-harness-readiness-dashboard",
    "harness-change-narrative",
    "ai-coding-harness-change-narrative",
    "harness-knowledge-capture",
    "ai-coding-harness-knowledge-capture",
    "harness-project-rules",
    "ai-coding-harness-project-rules",
]


def frontmatter_name(skill_file: Path) -> str:
    content = skill_file.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    if not match:
        raise AssertionError(f"missing name frontmatter: {skill_file}")
    return match.group(1).strip().strip("'\"")


class SkillBreakingRenameTests(unittest.TestCase):
    def test_formal_agentmentor_skill_directories_exist(self) -> None:
        for skill in FORMAL_SKILLS:
            with self.subTest(skill=skill):
                skill_file = SKILLS / skill / "SKILL.md"
                self.assertTrue(skill_file.exists(), f"missing formal skill: {skill}")
                self.assertEqual(frontmatter_name(skill_file), skill)

    def test_legacy_harness_skill_directories_are_removed(self) -> None:
        for skill in REMOVED_LEGACY_SKILLS:
            with self.subTest(skill=skill):
                self.assertFalse((SKILLS / skill).exists(), f"legacy skill remains: {skill}")

    def test_display_headings_use_semantic_agentmentor_names(self) -> None:
        expected_headings = {
            "using-agentmentor": "# Using AgentMentor",
            "start-gate": "# Start Gate",
            "delegation-gate": "# Delegation Gate",
            "knowledge-retrieval": "# Knowledge Retrieval",
            "doc-lifecycle": "# Doc Lifecycle",
            "incident-learning": "# Incident Learning",
            "vision-gate": "# Vision Gate",
            "readiness-dashboard": "# Readiness Dashboard",
            "change-narrative": "# Change Narrative",
            "knowledge-capture": "# Knowledge Capture",
            "project-rules": "# Project Rules",
        }

        for skill, heading in expected_headings.items():
            with self.subTest(skill=skill):
                content = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(heading, content)
                if skill != "using-agentmentor":
                    self.assertNotIn("# AgentMentor ", content)
                self.assertNotIn("# Harness ", content)

    def test_agent_display_names_use_agentmentor_identity(self) -> None:
        agent_file = (
            SKILLS
            / "delegation-gate"
            / "agents"
            / "openai.yaml"
        )
        content = agent_file.read_text(encoding="utf-8")

        self.assertIn('display_name: "AgentMentor Delegation Gate"', content)
        self.assertNotIn('display_name: "AI Coding Harness Delegation Gate"', content)
        self.assertNotIn('display_name: "Harness Delegation Gate"', content)


if __name__ == "__main__":
    unittest.main()
