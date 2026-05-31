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
    def test_using_harness_requires_optional_hook_resources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(REPO_ROOT / "skills", root / "skills")
            missing = (
                root
                / "skills"
                / "using-harness"
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
        self.assertIn("using-harness is missing required bundled resource", result.stdout)
        self.assertIn("codex-hooks.example.json", result.stdout)


if __name__ == "__main__":
    unittest.main()
