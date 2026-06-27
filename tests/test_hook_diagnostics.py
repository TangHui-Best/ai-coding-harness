from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = REPO_ROOT / "skills" / "using-agentmentor" / "scripts" / "hook_diagnostics.py"


def run_diagnostic(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(DIAGNOSTIC), *args],
        text=True,
        capture_output=True,
        cwd=REPO_ROOT,
    )


class HookDiagnosticsTests(unittest.TestCase):
    def test_skip_runner_smoke_reports_not_applicable_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            codex_home = Path(tmp) / "codex-home"
            root.mkdir()
            codex_home.mkdir()

            result = run_diagnostic(
                "codex",
                "--codex-home",
                str(codex_home),
                "--project-root",
                str(root),
                "--format",
                "json",
                "--skip-runner-smoke",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["status"], "pass")
        self.assertEqual(output["checks"]["runner_smoke"]["status"], "not_applicable")
        self.assertNotIn("codex_compaction_triggers", output["checks"])

    def test_runner_smoke_passes_when_stop_hook_runner_can_inspect_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            codex_home = Path(tmp) / "codex-home"
            root.mkdir()
            codex_home.mkdir()

            result = run_diagnostic(
                "codex",
                "--codex-home",
                str(codex_home),
                "--project-root",
                str(root),
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["checks"]["runner_smoke"]["status"], "pass")
        self.assertIn("Stop runner", output["checks"]["runner_smoke"]["reason"])


if __name__ == "__main__":
    unittest.main()
