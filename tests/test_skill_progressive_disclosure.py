from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class SkillProgressiveDisclosureTests(unittest.TestCase):
    def test_harness_entrypoint_uses_progressive_disclosure(self) -> None:
        content = read_skill("using-harness")

        self.assertIn("Reference Map", content)
        self.assertIn("Use references only when their trigger applies", content)

    def test_knowledge_capture_uses_progressive_disclosure(self) -> None:
        content = read_skill("harness-knowledge-capture")

        self.assertIn("Reference Map", content)
        self.assertIn("references/completion-closeout-contract.md", content)
        self.assertIn("references/artifact-decision-matrix.md", content)
        self.assertIn("references/bugfix-attribution-and-patch-churn.md", content)

    def test_high_frequency_gates_use_progressive_disclosure(self) -> None:
        expected_refs = {
            "harness-start-gate": [
                "references/start-gate-decision-rules.md",
                "references/bug-intake-and-patch-churn.md",
            ],
            "harness-knowledge-retrieval": [
                "references/retrieval-order.md",
                "references/bug-retrieval-mode.md",
            ],
            "harness-readiness-dashboard": [
                "references/readiness-checks.md",
            ],
        }

        for skill, refs in expected_refs.items():
            content = read_skill(skill)
            self.assertIn("Reference Map", content)
            self.assertIn("Use references only when their trigger applies", content)
            for ref in refs:
                self.assertIn(ref, content)

    def test_script_resources_are_global_execute_first_contract(self) -> None:
        using_harness = read_skill("using-harness")
        capture = read_skill("harness-knowledge-capture")

        for content in [using_harness, capture]:
            self.assertIn("Execute bundled scripts; do not read script source", content)
            self.assertIn("unless debugging or editing that script", content)

    def test_verification_resources_are_run_first_contract(self) -> None:
        using_harness = read_skill("using-harness")
        capture = read_skill("harness-knowledge-capture")

        for content in [using_harness, capture]:
            self.assertIn("Run verification commands before reading verification source", content)
            self.assertIn("Do not read test files, validator scripts, or workflow files merely to verify", content)
            self.assertIn("Read them only when debugging a failure, editing them, reviewing them, or explaining their behavior", content)

    def test_referenced_harness_material_exists(self) -> None:
        expected = [
            SKILLS / "using-harness" / "references" / "routing.md",
            SKILLS / "using-harness" / "references" / "task-routing-fixtures.md",
            SKILLS
            / "harness-knowledge-capture"
            / "references"
            / "completion-closeout-contract.md",
            SKILLS
            / "harness-knowledge-capture"
            / "references"
            / "artifact-decision-matrix.md",
            SKILLS
            / "harness-knowledge-capture"
            / "references"
            / "bugfix-attribution-and-patch-churn.md",
            SKILLS
            / "harness-start-gate"
            / "references"
            / "start-gate-decision-rules.md",
            SKILLS
            / "harness-start-gate"
            / "references"
            / "bug-intake-and-patch-churn.md",
            SKILLS
            / "harness-knowledge-retrieval"
            / "references"
            / "retrieval-order.md",
            SKILLS
            / "harness-knowledge-retrieval"
            / "references"
            / "bug-retrieval-mode.md",
            SKILLS
            / "harness-readiness-dashboard"
            / "references"
            / "readiness-checks.md",
            SKILLS
            / "using-harness"
            / "assets"
            / "templates"
            / "CLOSEOUT_COMPACT.md",
        ]

        for path in expected:
            self.assertTrue(path.exists(), f"missing referenced file: {path}")

    def test_task_routing_fixtures_cover_common_workflows(self) -> None:
        content = (
            SKILLS
            / "using-harness"
            / "references"
            / "task-routing-fixtures.md"
        ).read_text(encoding="utf-8")

        for scenario in [
            "tiny bugfix",
            "non-tiny bugfix",
            "commit-only",
            "PR description",
            "skill edit",
            "artifact updated",
            "no artifact needed",
        ]:
            self.assertIn(scenario, content)

    def test_closeout_template_and_install_sync_are_discoverable(self) -> None:
        using_harness = read_skill("using-harness")
        capture = read_skill("harness-knowledge-capture")

        self.assertIn("assets/templates/CLOSEOUT_COMPACT.md", using_harness)
        self.assertIn("assets/templates/CLOSEOUT_COMPACT.md", capture)
        self.assertTrue((REPO_ROOT / "scripts" / "install.ps1").exists())
        self.assertTrue((REPO_ROOT / "scripts" / "install.sh").exists())


if __name__ == "__main__":
    unittest.main()
