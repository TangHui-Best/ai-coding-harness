from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = REPO_ROOT / "skills" / "using-harness" / "scripts" / "hook_diagnostics.py"


def run_diagnostic(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(DIAGNOSTIC), *args],
        text=True,
        capture_output=True,
        cwd=REPO_ROOT,
    )


class HookDiagnosticsTests(unittest.TestCase):
    def test_reports_codex_compaction_without_precompact_hook_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            codex_home = Path(tmp) / "codex-home"
            session_dir = codex_home / "sessions" / "2026" / "05" / "31"
            session_dir.mkdir(parents=True)
            root.mkdir()
            session_log = session_dir / "rollout-2026-05-31T14-42-27-session.jsonl"
            session_log.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "timestamp": "2026-05-31T06:42:27.501Z",
                                "type": "session_meta",
                                "payload": {
                                    "id": "session-123",
                                    "cwd": str(root),
                                    "originator": "Codex Desktop",
                                },
                            }
                        ),
                        json.dumps(
                            {
                                "timestamp": "2026-05-31T10:30:04.695Z",
                                "type": "compacted",
                                "payload": {"message": ""},
                            }
                        ),
                        json.dumps(
                            {
                                "timestamp": "2026-05-31T10:30:04.796Z",
                                "type": "event_msg",
                                "payload": {"type": "context_compacted"},
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

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

        self.assertEqual(result.returncode, 1, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["status"], "warning")
        compact_check = output["checks"]["codex_compaction_triggers"]
        self.assertEqual(compact_check["status"], "warning")
        self.assertEqual(compact_check["compactions_without_hook_evidence"], 1)
        self.assertIn("context_compacted", compact_check["reason"])

    def test_runner_smoke_passes_when_hook_runner_can_write_recovery_snapshot(self) -> None:
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
        self.assertEqual(output["checks"]["codex_compaction_triggers"]["status"], "not_applicable")


if __name__ == "__main__":
    unittest.main()
