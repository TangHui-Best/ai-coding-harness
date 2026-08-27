from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = {"agentmentor", "agentmentor-intent", "agentmentor-decision", "agentmentor-learning", "agentmentor-evidence", "agentmentor-closeout"}


class SkillSurfaceTests(unittest.TestCase):
    def test_only_six_vnext_skills_exist(self) -> None:
        found = {path.name for path in (REPO_ROOT / "skills").iterdir() if path.is_dir()}
        self.assertEqual(SKILLS, found)

    def test_metadata_check_passes(self) -> None:
        result = subprocess.run([sys.executable, "scripts/skill_metadata_check.py", "--root", ".", "--strict"], cwd=REPO_ROOT, text=True, capture_output=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_hot_path_uses_the_index_without_default_gates(self) -> None:
        content = (REPO_ROOT / "skills" / "agentmentor" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("docs/INDEX.md", content)
        self.assertIn("zero to three Feature", content)
        self.assertIn("Do not invoke a Start Gate", content)
        self.assertNotIn("context.py", content)
