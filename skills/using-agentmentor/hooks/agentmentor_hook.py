#!/usr/bin/env python3
"""Optional AgentMentor hook runner.

This runner is intentionally platform-neutral. Agent-specific hook configs can
call it and translate the generic decision shape when a platform needs a
different wire format. The runner must fail open for runtime/configuration
errors so a broken hook install never breaks the Skill-only AgentMentor workflow.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


HARNESS_ARTIFACT_PARTS = {
    ("docs", "features"),
    ("docs", "decisions"),
    ("docs", "lessons"),
    ("docs", "evidence"),
}

COMPLETION_PATTERNS = [
    r"\bdone\b",
    r"\bcomplete(?:d|ion)?\b",
    r"\bfixed\b",
    r"\bverified\b",
    r"\bready\b",
    r"\bimplemented\b",
    r"完成",
    r"修复",
    r"已验证",
    r"交付",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run optional AgentMentor hook checks.")
    parser.add_argument(
        "--event",
        required=True,
        choices=["post-tool-use", "stop"],
        help="Normalized AgentMentor hook event name.",
    )
    parser.add_argument(
        "--platform",
        default="generic",
        choices=["generic", "codex", "claude", "opencode"],
        help="Output compatibility mode. Generic JSON is the stable core format.",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Project root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--docs-path",
        default="docs",
        help="Docs directory relative to --root.",
    )
    return parser.parse_args()


def load_payload() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {"_agentmentor_hook_invalid_json": raw[:1000]}
    return payload if isinstance(payload, dict) else {"value": payload}


def root_from_args_or_payload(root_arg: str | None, payload: dict[str, Any]) -> Path:
    if root_arg:
        return Path(root_arg).resolve()
    for key in ["cwd", "project_root", "projectRoot", "workspace", "workspaceRoot"]:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            try:
                return Path(value).resolve()
            except (OSError, ValueError):
                break
    return Path.cwd().resolve()


def decision(status: str, reason: str, **extra: Any) -> dict[str, Any]:
    output: dict[str, Any] = {"decision": status, "reason": reason}
    output.update(extra)
    return output


def write_hook_trace(
    root: Path,
    event: str,
    platform: str,
    payload: dict[str, Any],
    output: dict[str, Any] | None = None,
) -> None:
    """Best-effort runtime trace; never let diagnostics break hook behavior."""

    if os.environ.get("AGENTMENTOR_HOOK_TRACE", "1").strip().lower() in {"0", "false", "no", "off"}:
        return

    try:
        trace_dir = root / ".agentmentor" / "hook-events"
        trace_dir.mkdir(parents=True, exist_ok=True)
        record: dict[str, Any] = {
            "timestamp": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "event": event,
            "platform": platform,
            "session_id": session_id_from_payload(payload),
        }
        if output is None:
            record["phase"] = "start"
        else:
            record.update(
                {
                    "phase": "end",
                    "decision": output.get("decision"),
                    "reason": output.get("reason"),
                    "check": output.get("check"),
                    "severity": output.get("severity"),
                }
            )
        with (trace_dir / "events.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        return


def strict_post_tool_use_enabled() -> bool:
    value = os.environ.get("AGENTMENTOR_HOOK_STRICT_POST_TOOL_USE", "")
    return value.strip().lower() in {"1", "true", "yes", "on"}


def emit(output: dict[str, Any], platform: str, event: str) -> int:
    if platform == "claude" and output.get("decision") == "block":
        print(output.get("reason", "AgentMentor hook blocked this action."), file=sys.stderr)
        return 2
    if platform == "claude":
        return 0

    if platform == "codex" and output.get("decision") != "block":
        print("{}")
        return 0

    print(json.dumps(output, ensure_ascii=False))
    return 0


def strings_from(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, str):
        found.append(value)
    elif isinstance(value, dict):
        for item in value.values():
            found.extend(strings_from(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(strings_from(item))
    return found


def normalize_path(text: str, root: Path) -> Path | None:
    if not text or "\n" in text or len(text) > 500:
        return None

    candidate = text.strip().strip('"').strip("'")
    if not candidate:
        return None

    try:
        path = Path(candidate)
        if not path.is_absolute():
            path = root / path
        return path.resolve()
    except (OSError, ValueError):
        return None


def is_harness_artifact_path(path: Path, root: Path) -> bool:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False

    parts = tuple(part.lower() for part in relative.parts)
    for marker in HARNESS_ARTIFACT_PARTS:
        if len(parts) >= len(marker) and parts[: len(marker)] == marker:
            return True
    return False


def extracted_harness_paths(payload: dict[str, Any], root: Path) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for text in strings_from(payload):
        path = normalize_path(text, root)
        if path is None or not is_harness_artifact_path(path, root):
            continue
        if path not in seen:
            seen.add(path)
            paths.append(path)
    return paths


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def script_path(name: str) -> Path:
    return skill_root() / "scripts" / name


def run_knowledge_check(root: Path, docs_path: str) -> subprocess.CompletedProcess[str]:
    script = script_path("knowledge_check.py")
    return subprocess.run(
        [
            sys.executable,
            str(script),
            "--root",
            str(root),
            "--docs-path",
            docs_path,
            "--strict",
        ],
        text=True,
        capture_output=True,
    )


def handle_post_tool_use(payload: dict[str, Any], root: Path, docs_path: str) -> dict[str, Any]:
    paths = extracted_harness_paths(payload, root)
    if not paths:
        return decision("allow", "no AgentMentor artifact paths found in tool event")

    docs_root = (root / docs_path).resolve()
    if not docs_root.exists():
        return decision(
            "allow",
            f"docs path not found; fail-open for optional AgentMentor hook: {docs_root}",
            paths=[str(path) for path in paths],
        )

    checker = script_path("knowledge_check.py")
    if not checker.exists():
        return decision(
            "allow",
            f"knowledge_check.py not found; fail-open for optional AgentMentor hook: {checker}",
            paths=[str(path) for path in paths],
        )

    try:
        result = run_knowledge_check(root, docs_path)
    except OSError as exc:
        return decision(
            "allow",
            f"knowledge_check.py could not run; fail-open for optional AgentMentor hook: {exc}",
            paths=[str(path) for path in paths],
        )

    if result.returncode != 0:
        reason = "knowledge_check.py failed after AgentMentor artifact edit"
        details = (result.stderr or result.stdout).strip()
        if details:
            reason = f"{reason}: {details[:1200]}"
        if not strict_post_tool_use_enabled():
            return decision(
                "allow",
                reason,
                severity="warning",
                paths=[str(path) for path in paths],
                check="knowledge_check.py",
            )
        return decision(
            "block",
            reason,
            paths=[str(path) for path in paths],
            check="knowledge_check.py",
        )

    return decision(
        "allow",
        "knowledge_check.py passed after AgentMentor artifact edit",
        paths=[str(path) for path in paths],
        check="knowledge_check.py",
    )


def latest_message(payload: dict[str, Any]) -> str:
    for key in [
        "last_assistant_message",
        "assistant_message",
        "message",
        "response",
        "content",
    ]:
        value = payload.get(key)
        if isinstance(value, str):
            return value
    return "\n".join(strings_from(payload))


def has_completion_claim(message: str) -> bool:
    return any(re.search(pattern, message, re.IGNORECASE) for pattern in COMPLETION_PATTERNS)


def run_closeout_check(message: str) -> subprocess.CompletedProcess[str]:
    script = script_path("closeout_check.py")
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", suffix=".md", delete=False
    ) as handle:
        handle.write(message)
        temp_path = Path(handle.name)

    try:
        return subprocess.run(
            [sys.executable, str(script), "--file", str(temp_path)],
            text=True,
            capture_output=True,
        )
    finally:
        temp_path.unlink(missing_ok=True)


def handle_stop(payload: dict[str, Any]) -> dict[str, Any]:
    message = latest_message(payload)
    if not has_completion_claim(message):
        return decision("allow", "no completion claim detected")

    checker = script_path("closeout_check.py")
    if not checker.exists():
        return decision(
            "allow",
            f"closeout_check.py not found; fail-open for optional AgentMentor hook: {checker}",
        )

    try:
        result = run_closeout_check(message)
    except OSError as exc:
        return decision(
            "allow",
            f"closeout_check.py could not run; fail-open for optional AgentMentor hook: {exc}",
        )

    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip()
        reason = "Completion claim needs a valid AgentMentor closeout block"
        if details:
            reason = f"{reason}: {details[:1200]}"
        return decision("block", reason, check="closeout_check.py")

    return decision(
        "allow",
        "closeout check passed for completion claim",
        check="closeout_check.py",
    )


def first_payload_text(payload: dict[str, Any], keys: list[str]) -> str:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def session_id_from_payload(payload: dict[str, Any]) -> str:
    return first_payload_text(
        payload,
        [
            "session_id",
            "sessionId",
            "sessionID",
            "conversation_id",
            "conversationId",
            "conversationID",
            "thread_id",
            "threadId",
            "threadID",
        ],
    )


def main() -> int:
    args = parse_args()
    payload = load_payload()
    root = root_from_args_or_payload(args.root, payload)
    write_hook_trace(root, args.event, args.platform, payload)

    if "_agentmentor_hook_invalid_json" in payload:
        output = decision("allow", "invalid hook JSON; fail-open for optional AgentMentor hook")
        write_hook_trace(root, args.event, args.platform, payload, output)
        return emit(output, args.platform, args.event)

    try:
        if args.event == "post-tool-use":
            output = handle_post_tool_use(payload, root, args.docs_path)
        else:
            output = handle_stop(payload)
    except Exception as exc:  # noqa: BLE001 - hooks must never break Skill-only use.
        output = decision(
            "allow",
            f"unexpected AgentMentor hook error; fail-open for optional hook: {exc}",
        )

    write_hook_trace(root, args.event, args.platform, payload, output)
    return emit(output, args.platform, args.event)


if __name__ == "__main__":
    raise SystemExit(main())
