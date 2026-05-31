from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK = REPO_ROOT / "skills" / "using-harness" / "hooks" / "harness_hook.py"


VALID_CLOSEOUT = """\
Closeout verdict: pass
Completion claim allowed: yes
Entry Gate: ready
Vision Anchor: Feature F003
Backlog/Handoff: not triggered
Plan lifecycle: not triggered
Readiness: not triggered
Vision Gate Exit: not triggered because no release transition
Patch Churn Review: not triggered
Bugfix attribution: not triggered because hook runtime is not a bugfix
ADR: not triggered
Lesson: not triggered
Evidence: recorded in final response
Evidence level: standard
Feature: F003
Check: knowledge_check.py passed
"""


def run_hook(
    event: str,
    payload: dict,
    root: Path | None = None,
    platform: str = "generic",
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        str(HOOK),
        "--event",
        event,
        "--platform",
        platform,
    ]
    if root is not None:
        command.extend(["--root", str(root)])

    env = None
    if extra_env:
        import os

        env = os.environ.copy()
        env.update(extra_env)

    return subprocess.run(
        command,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=REPO_ROOT,
        env=env,
    )


def parsed_stdout(result: subprocess.CompletedProcess[str]) -> dict:
    return json.loads(result.stdout)


class HarnessHookTests(unittest.TestCase):
    def test_stop_allows_non_completion_message_without_closeout(self) -> None:
        result = run_hook(
            "stop",
            {"last_assistant_message": "I found the relevant files and will continue."},
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "allow")
        self.assertIn("no completion claim", output["reason"])

    def test_stop_blocks_completion_claim_without_closeout(self) -> None:
        result = run_hook(
            "stop",
            {"last_assistant_message": "Done. The hook runtime is implemented."},
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "block")
        self.assertIn("Harness closeout", output["reason"])

    def test_stop_allows_completion_claim_with_valid_closeout(self) -> None:
        result = run_hook(
            "stop",
            {
                "last_assistant_message": (
                    "Implementation done.\n\n"
                    + VALID_CLOSEOUT
                )
            },
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "allow")
        self.assertIn("closeout check passed", output["reason"])

    def test_codex_allow_output_uses_empty_json_object(self) -> None:
        result = run_hook(
            "stop",
            {"last_assistant_message": "I found the relevant files and will continue."},
            platform="codex",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(parsed_stdout(result), {})

    def test_claude_block_output_uses_exit_code_two(self) -> None:
        result = run_hook(
            "stop",
            {"last_assistant_message": "Done. The hook runtime is implemented."},
            platform="claude",
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("Harness closeout", result.stderr)

    def test_post_tool_use_ignores_non_harness_paths(self) -> None:
        result = run_hook(
            "post-tool-use",
            {"tool_input": {"file_path": "src/example.py"}},
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "allow")
        self.assertIn("no Harness artifact paths", output["reason"])

    def test_post_tool_use_warns_on_invalid_intermediate_harness_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs" / "features"
            docs.mkdir(parents=True)
            bad_feature = docs / "F010-bad.md"
            bad_feature.write_text(
                textwrap.dedent(
                    """\
                    ---
                    id: F010
                    doc_kind: feature
                    status: active
                    created: 2026-05-30
                    updated: 2026-05-30
                    ---

                    # F010: Bad Feature
                    """
                ),
                encoding="utf-8",
            )

            result = run_hook(
                "post-tool-use",
                {"tool_input": {"file_path": str(bad_feature)}},
                root=root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "allow")
        self.assertIn("knowledge_check.py failed", output["reason"])
        self.assertEqual(output["severity"], "warning")

    def test_post_tool_use_strict_mode_blocks_invalid_harness_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs" / "features"
            docs.mkdir(parents=True)
            bad_feature = docs / "F010-bad.md"
            bad_feature.write_text(
                textwrap.dedent(
                    """\
                    ---
                    id: F010
                    doc_kind: feature
                    status: active
                    created: 2026-05-30
                    updated: 2026-05-30
                    ---

                    # F010: Bad Feature
                    """
                ),
                encoding="utf-8",
            )

            result = run_hook(
                "post-tool-use",
                {"tool_input": {"file_path": str(bad_feature)}},
                root=root,
                extra_env={"HARNESS_HOOK_STRICT_POST_TOOL_USE": "1"},
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "block")
        self.assertIn("knowledge_check.py failed", output["reason"])

    def test_post_tool_use_fails_open_when_docs_root_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_hook(
                "post-tool-use",
                {"tool_input": {"file_path": str(root / "docs" / "features" / "F010.md")}},
                root=root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "allow")
        self.assertIn("docs path not found", output["reason"])

    def test_pre_compact_writes_session_recovery_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_hook(
                "pre-compact",
                {
                    "session_id": "session-123",
                    "hook_event_name": "PreCompact",
                    "cwd": str(root),
                    "summary": "Current goal: add SessionStart and PreCompact recovery hooks.",
                    "custom_instructions": "Preserve Harness context.",
                },
                root=root,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            output = parsed_stdout(result)
            recovery_path = Path(output["recovery_path"])

            self.assertEqual(output["decision"], "allow")
            self.assertIn("recovery snapshot written", output["reason"])
            self.assertEqual(
                recovery_path,
                root / ".harness" / "session-recovery" / "by-session" / "session-123.md",
            )
            self.assertTrue(recovery_path.exists())
            content = recovery_path.read_text(encoding="utf-8")
            self.assertIn("# Harness Session Recovery", content)
            self.assertIn("session-123", content)
            self.assertIn("Current goal: add SessionStart", content)
            self.assertIn("Preserve Harness context", content)
            self.assertTrue((root / ".harness" / "session-recovery" / "latest.md").exists())

    def test_pre_compact_accepts_opencode_session_id_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_hook(
                "pre-compact",
                {
                    "sessionID": "ses_opencode_123",
                    "source": "compact",
                    "summary": "Continue the OpenCode compaction recovery review.",
                },
                root=root,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            output = parsed_stdout(result)
            recovery_path = Path(output["recovery_path"])

            self.assertEqual(
                recovery_path,
                root / ".harness" / "session-recovery" / "by-session" / "ses_opencode_123.md",
            )
            self.assertTrue(recovery_path.exists())

    def test_session_start_compact_returns_same_session_recovery_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            recovery_dir = root / ".harness" / "session-recovery" / "by-session"
            recovery_dir.mkdir(parents=True)
            recovery_file = recovery_dir / "session-456.md"
            recovery_file.write_text(
                "# Harness Session Recovery\n\nContinue F005 from EV-008.\n",
                encoding="utf-8",
            )

            result = run_hook(
                "session-start",
                {"session_id": "session-456", "source": "compact"},
                root=root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "allow")
        self.assertIn("recovery snapshot found", output["reason"])
        self.assertIn("Continue F005", output["additional_context"])

    def test_session_start_startup_does_not_read_previous_latest_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            recovery_dir = root / ".harness" / "session-recovery"
            recovery_dir.mkdir(parents=True)
            (recovery_dir / "latest.md").write_text(
                "# Harness Session Recovery\n\nPrevious unrelated task.\n",
                encoding="utf-8",
            )

            result = run_hook(
                "session-start",
                {"session_id": "new-session", "source": "startup"},
                root=root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "allow")
        self.assertIn("not a compact recovery event", output["reason"])
        self.assertNotIn("additional_context", output)

    def test_session_start_compact_does_not_read_other_session_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            recovery_dir = root / ".harness" / "session-recovery" / "by-session"
            recovery_dir.mkdir(parents=True)
            (recovery_dir / "old-session.md").write_text(
                "# Harness Session Recovery\n\nOld session context.\n",
                encoding="utf-8",
            )

            result = run_hook(
                "session-start",
                {"session_id": "new-session", "source": "compact"},
                root=root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "allow")
        self.assertIn("no session recovery snapshot", output["reason"])
        self.assertNotIn("additional_context", output)

    def test_session_start_allows_when_recovery_snapshot_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_hook(
                "session-start",
                {"session_id": "session-789", "source": "compact"},
                root=root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "allow")
        self.assertIn("no session recovery snapshot", output["reason"])

    def test_claude_session_start_emits_additional_context_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            recovery_dir = root / ".harness" / "session-recovery" / "by-session"
            recovery_dir.mkdir(parents=True)
            (recovery_dir / "session-claude.md").write_text(
                "# Harness Session Recovery\n\nUse the F005 Vision Anchor.\n",
                encoding="utf-8",
            )

            result = run_hook(
                "session-start",
                {"session_id": "session-claude", "source": "compact"},
                root=root,
                platform="claude",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("Use the F005 Vision Anchor", output["hookSpecificOutput"]["additionalContext"])

    def test_codex_session_start_emits_additional_context_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            recovery_dir = root / ".harness" / "session-recovery" / "by-session"
            recovery_dir.mkdir(parents=True)
            (recovery_dir / "session-codex.md").write_text(
                "# Harness Session Recovery\n\nUse the Codex compact snapshot.\n",
                encoding="utf-8",
            )

            result = run_hook(
                "session-start",
                {"session_id": "session-codex", "source": "compact"},
                root=root,
                platform="codex",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("Use the Codex compact snapshot", output["hookSpecificOutput"]["additionalContext"])


if __name__ == "__main__":
    unittest.main()
