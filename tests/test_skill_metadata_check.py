from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "skill_metadata_check.py"


class SkillMetadataCheckTests(unittest.TestCase):
    def test_using_agentmentor_requires_optional_hook_resources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(REPO_ROOT / "skills", root / "skills")
            missing = (
                root
                / "skills"
                / "using-agentmentor"
                / "hooks"
                / "codex-hooks.example.json"
            )
            missing.unlink()

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--skills-path",
                    "skills",
                ],
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("using-agentmentor is missing required bundled resource", result.stdout)
        self.assertIn("codex-hooks.example.json", result.stdout)

    def test_legacy_harness_skill_name_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(REPO_ROOT / "skills", root / "skills")
            skill_dir = root / "skills" / "harness-new-workflow"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: harness-new-workflow\n"
                "description: MUST use when testing a future workflow name.\n"
                "---\n\n"
                "# Harness New Workflow\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--skills-path",
                    "skills",
                ],
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Legacy Harness skill slug was removed", result.stdout)
        self.assertIn("harness-new-workflow", result.stdout)

    def test_ai_coding_harness_skill_name_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(REPO_ROOT / "skills", root / "skills")
            skill_dir = root / "skills" / "ai-coding-harness-new-workflow"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: ai-coding-harness-new-workflow\n"
                "description: MUST use when testing a future workflow name.\n"
                "---\n\n"
                "# AI Coding Harness New Workflow\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--skills-path",
                    "skills",
                    "--strict",
                ],
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("AI Coding Harness skill slug was removed", result.stdout)
        self.assertIn("ai-coding-harness-new-workflow", result.stdout)

    def test_short_semantic_agentmentor_skill_name_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(REPO_ROOT / "skills", root / "skills")
            skill_dir = root / "skills" / "workflow-check"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: workflow-check\n"
                "description: Use when testing a future semantic workflow name.\n"
                "---\n\n"
                "# Workflow Check\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--skills-path",
                    "skills",
                    "--strict",
                ],
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
