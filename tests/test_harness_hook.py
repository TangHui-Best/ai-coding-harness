from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK = REPO_ROOT / "skills" / "using-agentmentor" / "hooks" / "agentmentor_hook.py"


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

    import os

    env = os.environ.copy()
    env["AGENTMENTOR_HOOK_TRACE"] = "0"
    if extra_env:
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
        self.assertIn("AgentMentor closeout", output["reason"])

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

    def test_stop_writes_runtime_trace_without_message_body(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_hook(
                "stop",
                {
                    "session_id": "trace-session",
                    "cwd": str(root),
                    "last_assistant_message": "I found the relevant files and will continue.",
                },
                extra_env={"AGENTMENTOR_HOOK_TRACE": "1"},
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            trace_path = root / ".agentmentor" / "hook-events" / "events.jsonl"
            self.assertTrue(trace_path.exists())
            records = [
                json.loads(line)
                for line in trace_path.read_text(encoding="utf-8").splitlines()
            ]

        self.assertEqual([record["phase"] for record in records], ["start", "end"])
        self.assertEqual(records[0]["event"], "stop")
        self.assertEqual(records[0]["session_id"], "trace-session")
        self.assertEqual(records[1]["decision"], "allow")
        serialized = json.dumps(records, ensure_ascii=False)
        self.assertNotIn("I found the relevant files", serialized)

    def test_root_defaults_to_payload_cwd_for_runtime_trace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_hook(
                "stop",
                {
                    "session_id": "cwd-session",
                    "cwd": str(root),
                    "last_assistant_message": "I found the relevant files and will continue.",
                },
                extra_env={"AGENTMENTOR_HOOK_TRACE": "1"},
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(
                (root / ".agentmentor" / "hook-events" / "events.jsonl").exists()
            )

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
        self.assertIn("AgentMentor closeout", result.stderr)

    def test_post_tool_use_ignores_non_harness_paths(self) -> None:
        result = run_hook(
            "post-tool-use",
            {"tool_input": {"file_path": "src/example.py"}},
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = parsed_stdout(result)
        self.assertEqual(output["decision"], "allow")
        self.assertIn("no AgentMentor artifact paths", output["reason"])

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
                extra_env={"AGENTMENTOR_HOOK_STRICT_POST_TOOL_USE": "1"},
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

    def test_removed_session_recovery_events_are_not_accepted(self) -> None:
        for event in ["pre-compact", "session-start"]:
            result = run_hook(event, {})

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
