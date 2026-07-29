from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class InstallScriptTests(unittest.TestCase):
    def test_powershell_install_copies_vnext_and_removes_legacy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            (destination / "start-gate").mkdir(parents=True)
            environment = os.environ | {"AGENTMENTOR_CODEX_SKILLS_DIR": str(destination)}
            result = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "scripts/install.ps1", "codex"], cwd=REPO_ROOT, text=True, capture_output=True, env=environment)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue((destination / "agentmentor" / "SKILL.md").exists())
            self.assertFalse((destination / "start-gate").exists())

