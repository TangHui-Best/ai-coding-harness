from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

FORMAL_SKILLS = [
    "using-agentmentor",
    "start-gate",
    "delegation-gate",
    "knowledge-retrieval",
    "spec-drift",
    "doc-lifecycle",
    "incident-learning",
    "vision-gate",
    "readiness-dashboard",
    "change-narrative",
    "knowledge-capture",
    "project-rules",
]

LEGACY_SKILLS = [
    "using-harness",
    "harness-start-gate",
    "ai-coding-harness",
    "ai-coding-harness-start-gate",
]


def bash_is_usable() -> bool:
    if shutil.which("bash") is None:
        return False
    result = subprocess.run(
        ["bash", "--version"],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    return result.returncode == 0


@unittest.skipIf(not bash_is_usable(), "bash is not usable")
class BashInstallScriptTests(unittest.TestCase):
    def test_installs_to_overridden_destination_and_verifies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex = Path(tmp) / "codex-skills"
            claude = Path(tmp) / "claude-skills"
            for stale in LEGACY_SKILLS:
                (codex / stale).mkdir(parents=True)

            env = os.environ.copy()
            env["AGENTMENTOR_CODEX_SKILLS_DIR"] = str(codex)
            env["AGENTMENTOR_CLAUDE_SKILLS_DIR"] = str(claude)

            install = subprocess.run(
                ["bash", "scripts/install.sh", "codex"],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
            )

            self.assertEqual(install.returncode, 0, install.stderr)
            self.assertIn("Verification: passed", install.stdout)
            self.assertIn("Hooks are optional", install.stdout)
            for skill in FORMAL_SKILLS:
                self.assertTrue((codex / skill / "SKILL.md").exists(), skill)
            for stale in LEGACY_SKILLS:
                self.assertFalse((codex / stale).exists(), stale)
            self.assertFalse(claude.exists())

            verify = subprocess.run(
                ["bash", "scripts/install.sh", "--verify", "codex"],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
            )

            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertIn("Verify-only: no files were copied", verify.stdout)
            self.assertIn("Verification: passed", verify.stdout)


@unittest.skipIf(shutil.which("powershell") is None, "powershell is not available")
class PowerShellInstallScriptTests(unittest.TestCase):
    def test_installs_to_overridden_destination_and_verifies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex = Path(tmp) / "codex-skills"
            claude = Path(tmp) / "claude-skills"
            for stale in LEGACY_SKILLS:
                (claude / stale).mkdir(parents=True)

            env = os.environ.copy()
            env["AGENTMENTOR_CODEX_SKILLS_DIR"] = str(codex)
            env["AGENTMENTOR_CLAUDE_SKILLS_DIR"] = str(claude)

            install = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    ".\\scripts\\install.ps1",
                    "claude",
                ],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
            )

            self.assertEqual(install.returncode, 0, install.stderr)
            self.assertIn("Verification: passed", install.stdout)
            self.assertIn("Hooks are optional", install.stdout)
            for skill in FORMAL_SKILLS:
                self.assertTrue((claude / skill / "SKILL.md").exists(), skill)
            for stale in LEGACY_SKILLS:
                self.assertFalse((claude / stale).exists(), stale)
            self.assertFalse(codex.exists())

            verify = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    ".\\scripts\\install.ps1",
                    "-Verify",
                    "claude",
                ],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
            )

            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertIn("Verify-only: no files were copied", verify.stdout)
            self.assertIn("Verification: passed", verify.stdout)


if __name__ == "__main__":
    unittest.main()
