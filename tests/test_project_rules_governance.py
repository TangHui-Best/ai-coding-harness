from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class ProjectRulesGovernanceTests(unittest.TestCase):
    def test_project_rules_skill_requires_human_authorization(self) -> None:
        content = read_text(SKILLS / "project-rules" / "SKILL.md")

        self.assertIn("Human Authorization Boundary", content)
        self.assertIn("Agents MUST NOT edit `AGENTS.md`", content)
        self.assertIn("The user explicitly asks", content)
        self.assertIn("The user approves", content)
        self.assertIn("If authorization is missing", content)

    def test_project_rules_promotion_gate_is_hard_source_backed_and_budgeted(self) -> None:
        content = read_text(SKILLS / "project-rules" / "SKILL.md")

        self.assertIn("Hard constraint: The rule can be written as a MUST or MUST NOT", content)
        self.assertIn("Source-backed", content)
        self.assertIn("Human-authorized", content)
        self.assertIn("Length Budget", content)
        self.assertIn("Target: 100 lines or fewer", content)
        self.assertIn("Soft limit: 200 lines", content)
        self.assertIn("Hard limit: 300 lines", content)
        self.assertIn("Rules without a source reference", content)

    def test_project_rules_template_uses_source_backed_rule_shape(self) -> None:
        content = read_text(REPO_ROOT / "templates" / "AGENTS.md")
        bundled = read_text(
            SKILLS / "using-agentmentor" / "assets" / "templates" / "AGENTS.md"
        )

        self.assertEqual(content, bundled)
        self.assertIn("## Project Rules", content)
        self.assertIn("### Rule: 项目规则晋升门槛", content)
        for field in ["- Scope:", "- Requirement:", "- Source:", "- Rationale:"]:
            self.assertIn(field, content)
        self.assertIn("explicit user approval", content)
        self.assertNotIn("SHOULD", content)
        self.assertNotIn("PREFER", content)

    def test_artifact_decision_matrix_separates_agents_from_knowledge_archive(self) -> None:
        content = read_text(
            SKILLS / "knowledge-capture" / "references" / "artifact-decision-matrix.md"
        )

        self.assertIn("Repository-wide agent behavior constraint", content)
        self.assertIn("AGENTS.md is a high-attention control surface", content)
        self.assertIn("not a knowledge archive", content)
        self.assertIn("human-authorized MUST/MUST NOT rules", content)
        self.assertIn("target <=100 lines", content)


if __name__ == "__main__":
    unittest.main()
