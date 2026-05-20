import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "harness_closeout_check.py"


BASE_CLOSEOUT = """\
Closeout verdict: pass
Completion claim allowed: yes
Backlog/Handoff: not triggered
Plan lifecycle: not triggered
Readiness: not triggered
Vision Gate Exit: not triggered
Patch Churn Review: not triggered
ADR: not triggered
Lesson: not triggered
Evidence: recorded in final response
Evidence level: quick
Feature: not triggered
Check: not run because no Harness artifacts changed
"""


class HarnessCloseoutCheckTests(unittest.TestCase):
    def run_check(self, content: str) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", suffix=".md", delete=False
        ) as handle:
            handle.write(textwrap.dedent(content))
            path = Path(handle.name)

        try:
            return subprocess.run(
                [sys.executable, str(SCRIPT), "--file", str(path)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
            )
        finally:
            path.unlink(missing_ok=True)

    def test_requires_bugfix_attribution_field(self):
        result = self.run_check(BASE_CLOSEOUT)

        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing or empty field: Bugfix attribution", result.stderr)

    def test_accepts_closeout_with_bugfix_attribution_field(self):
        result = self.run_check(
            BASE_CLOSEOUT
            + "Bugfix attribution: not triggered because documentation-only change\n"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Harness closeout block structure: pass", result.stdout)


if __name__ == "__main__":
    unittest.main()
