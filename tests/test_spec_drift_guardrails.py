from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_skill(name: str) -> str:
    return read(SKILLS / name / "SKILL.md")


class SpecDriftGuardrailTests(unittest.TestCase):
    def test_spec_drift_skill_exists_with_progressive_disclosure(self) -> None:
        content = read_skill("spec-drift")

        self.assertIn("name: spec-drift", content)
        self.assertIn("# Spec Drift", content)
        self.assertIn("Reference Map", content)
        self.assertIn("Use references only when their trigger applies", content)
        self.assertIn("references/spec-drift-decision-rules.md", content)
        self.assertTrue(
            (SKILLS / "spec-drift" / "references" / "spec-drift-decision-rules.md").exists()
        )

    def test_spec_drift_skill_covers_core_drift_signals(self) -> None:
        content = read_skill("spec-drift")

        for phrase in [
            "real cases",
            "validation failure",
            "user feedback",
            "stale spec",
            "acceptance criteria drift",
            "implementation follows spec but still wrong",
            "Spec Drift Result",
            "spec valid",
            "implementation bug",
            "spec needs update",
            "needs vision gate",
            "needs ADR",
            "Do not change code until this gate allows it",
        ]:
            self.assertIn(phrase, content)

    def test_entrypoint_routes_spec_drift_before_patch_work(self) -> None:
        content = read_skill("using-agentmentor")

        for phrase in [
            "spec-drift",
            "stale spec",
            "acceptance criteria drift",
            "implementation follows spec but still wrong",
            "real cases, validation, or user feedback contradict an existing spec",
        ]:
            self.assertIn(phrase, content)

    def test_start_gate_detects_spec_drift_without_doing_full_review(self) -> None:
        content = read_skill("start-gate")

        for phrase in [
            "Spec Drift Check",
            "spec-drift",
            "stale spec",
            "acceptance criteria drift",
            "real cases, validation, or user feedback contradict an existing spec",
            "Spec drift:",
            "needs spec-drift",
        ]:
            self.assertIn(phrase, content)

    def test_vision_gate_transfers_stale_spec_classification_to_spec_drift(self) -> None:
        content = read_skill("vision-gate")

        for phrase in [
            "Spec Drift",
            "spec-drift",
            "stale spec",
            "acceptance criteria drift",
            "Vision Gate protects original intent",
            "Spec Drift owns stale spec classification",
        ]:
            self.assertIn(phrase, content)

    def test_manual_agents_guidance_is_documented_without_auto_mutation(self) -> None:
        install = read(REPO_ROOT / "INSTALL.md")
        readme = read(REPO_ROOT / "README.en.md")

        for content in [install, readme]:
            for phrase in [
                "Optional Project Rules",
                "copy the bundled `AGENTS.md` template",
                "AgentMentor does not automatically modify",
                "Spec Drift before changing code",
                "repeated patches add scenario-specific branches",
            ]:
                self.assertIn(phrase, content)

            for forbidden in [
                "automatically writes AGENTS.md",
                "auto-merge AGENTS.md",
                "init-project",
            ]:
                self.assertNotIn(forbidden, content)


if __name__ == "__main__":
    unittest.main()
