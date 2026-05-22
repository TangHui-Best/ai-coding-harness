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
Entry Gate: ready
Vision Anchor: Feature F001
Backlog/Handoff: not triggered
Plan lifecycle: not triggered
Readiness: not triggered
Vision Gate Exit: not triggered
Patch Churn Review: not triggered
Bugfix attribution: not triggered because closeout contract change is not a bugfix
ADR: not triggered
Lesson: not triggered
Evidence: recorded in final response
Evidence level: quick
Feature: updated F001
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
        result = self.run_check(
            BASE_CLOSEOUT.replace(
                "Bugfix attribution: not triggered because closeout contract change is not a bugfix\n",
                "",
            )
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing or empty field: Bugfix attribution", result.stderr)

    def test_requires_entry_gate_field(self):
        result = self.run_check(BASE_CLOSEOUT.replace("Entry Gate: ready\n", ""))

        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing or empty field: Entry Gate", result.stderr)

    def test_requires_vision_anchor_field(self):
        result = self.run_check(BASE_CLOSEOUT.replace("Vision Anchor: Feature F001\n", ""))

        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing or empty field: Vision Anchor", result.stderr)

    def test_requires_patch_churn_review_field(self):
        result = self.run_check(
            BASE_CLOSEOUT.replace("Patch Churn Review: not triggered\n", "")
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing or empty field: Patch Churn Review", result.stderr)

    def test_rejects_completion_with_missing_entry_gate(self):
        result = self.run_check(
            BASE_CLOSEOUT.replace("Entry Gate: ready\n", "Entry Gate: missing\n")
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Completion claim requires Entry Gate to be satisfied", result.stderr)

    def test_rejects_completion_with_unexplained_vision_anchor_exemption(self):
        result = self.run_check(
            BASE_CLOSEOUT.replace(
                "Vision Anchor: Feature F001\n",
                "Vision Anchor: not triggered\n",
            )
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Vision Anchor exemption must include a reason", result.stderr)

    def test_rejects_retroactive_entry_gate_without_recovery_artifact(self):
        result = self.run_check(
            BASE_CLOSEOUT.replace("Entry Gate: ready\n", "Entry Gate: retroactive\n")
            .replace("Feature: updated F001\n", "Feature: not triggered because routine check\n")
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "Retroactive Entry Gate requires a Feature or dedicated Evidence recovery record",
            result.stderr,
        )

    def test_accepts_closeout_with_entry_gate_and_vision_anchor_fields(self):
        result = self.run_check(BASE_CLOSEOUT)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Harness closeout block structure: pass", result.stdout)


if __name__ == "__main__":
    unittest.main()
