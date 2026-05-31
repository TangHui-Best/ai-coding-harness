#!/usr/bin/env python3
"""Optional Harness hook runner.

This runner is intentionally platform-neutral. Agent-specific hook configs can
call it and translate the generic decision shape when a platform needs a
different wire format. The runner must fail open for runtime/configuration
errors so a broken hook install never breaks the Skill-only Harness workflow.
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
    parser = argparse.ArgumentParser(description="Run optional Harness hook checks.")
    parser.add_argument(
        "--event",
        required=True,
        choices=["post-tool-use", "stop", "pre-compact", "session-start"],
        help="Normalized Harness hook event name.",
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
    parser.add_argument(
        "--recovery-path",
        default=".harness/session-recovery/latest.md",
        help="Session recovery snapshot path relative to --root.",
    )
    return parser.parse_args()


def load_payload() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {"_harness_hook_invalid_json": raw[:1000]}
    return payload if isinstance(payload, dict) else {"value": payload}


def decision(status: str, reason: str, **extra: Any) -> dict[str, Any]:
    output: dict[str, Any] = {"decision": status, "reason": reason}
    output.update(extra)
    return output


def strict_post_tool_use_enabled() -> bool:
    value = os.environ.get("HARNESS_HOOK_STRICT_POST_TOOL_USE", "")
    return value.strip().lower() in {"1", "true", "yes", "on"}


def emit(output: dict[str, Any], platform: str, event: str) -> int:
    if platform == "claude" and output.get("decision") == "block":
        print(output.get("reason", "Harness hook blocked this action."), file=sys.stderr)
        return 2
    if platform == "claude" and event == "session-start" and output.get("additional_context"):
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "SessionStart",
                        "additionalContext": output["additional_context"],
                    }
                },
                ensure_ascii=False,
            )
        )
        return 0
    if platform == "claude":
        return 0

    if platform == "codex" and event == "session-start" and output.get("additional_context"):
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "SessionStart",
                        "additionalContext": output["additional_context"],
                    }
                },
                ensure_ascii=False,
            )
        )
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
        return decision("allow", "no Harness artifact paths found in tool event")

    docs_root = (root / docs_path).resolve()
    if not docs_root.exists():
        return decision(
            "allow",
            f"docs path not found; fail-open for optional Harness hook: {docs_root}",
            paths=[str(path) for path in paths],
        )

    checker = script_path("knowledge_check.py")
    if not checker.exists():
        return decision(
            "allow",
            f"knowledge_check.py not found; fail-open for optional Harness hook: {checker}",
            paths=[str(path) for path in paths],
        )

    try:
        result = run_knowledge_check(root, docs_path)
    except OSError as exc:
        return decision(
            "allow",
            f"knowledge_check.py could not run; fail-open for optional Harness hook: {exc}",
            paths=[str(path) for path in paths],
        )

    if result.returncode != 0:
        reason = "knowledge_check.py failed after Harness artifact edit"
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
        "knowledge_check.py passed after Harness artifact edit",
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
    script = script_path("harness_closeout_check.py")
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

    checker = script_path("harness_closeout_check.py")
    if not checker.exists():
        return decision(
            "allow",
            f"harness_closeout_check.py not found; fail-open for optional Harness hook: {checker}",
        )

    try:
        result = run_closeout_check(message)
    except OSError as exc:
        return decision(
            "allow",
            f"harness_closeout_check.py could not run; fail-open for optional Harness hook: {exc}",
        )

    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip()
        reason = "Completion claim needs a valid Harness closeout block"
        if details:
            reason = f"{reason}: {details[:1200]}"
        return decision("block", reason, check="harness_closeout_check.py")

    return decision(
        "allow",
        "closeout check passed for completion claim",
        check="harness_closeout_check.py",
    )


def recovery_snapshot_path(root: Path, recovery_path: str) -> Path:
    path = Path(recovery_path)
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def session_recovery_root(root: Path, recovery_path: str) -> Path:
    return recovery_snapshot_path(root, recovery_path).parent


def safe_session_id(session_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", session_id.strip())
    cleaned = cleaned.strip(".-")
    return cleaned[:120] if cleaned else ""


def session_snapshot_path(root: Path, recovery_path: str, session_id: str) -> Path | None:
    safe_id = safe_session_id(session_id)
    if not safe_id:
        return None
    return (session_recovery_root(root, recovery_path) / "by-session" / f"{safe_id}.md").resolve()


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
            "conversation_id",
            "conversationId",
            "thread_id",
            "threadId",
        ],
    )


def session_start_source(payload: dict[str, Any]) -> str:
    return first_payload_text(
        payload,
        [
            "source",
            "session_start_source",
            "sessionStartSource",
            "hook_event_source",
            "hookEventSource",
        ],
    ).lower()


def transcript_tail(payload: dict[str, Any], root: Path) -> str:
    transcript = first_payload_text(payload, ["transcript_path", "transcriptPath"])
    if not transcript:
        return ""

    path = normalize_path(transcript, root)
    if path is None or not path.exists() or not path.is_file():
        return f"Transcript path: {transcript}"

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return f"Transcript path could not be read: {path} ({exc})"

    tail = text[-6000:].strip()
    if not tail:
        return f"Transcript path: {path}"
    return f"Transcript tail from {path}:\n\n{tail}"


def recovery_payload_text(payload: dict[str, Any], root: Path) -> str:
    direct = first_payload_text(
        payload,
        [
            "summary",
            "compact_summary",
            "compactSummary",
            "handoff",
            "recovery_context",
            "recoveryContext",
            "last_assistant_message",
            "assistant_message",
            "message",
        ],
    )
    transcript = transcript_tail(payload, root)
    custom = first_payload_text(payload, ["custom_instructions", "customInstructions", "instructions"])

    parts = []
    if direct:
        parts.append(direct)
    if custom:
        parts.append(f"Instructions:\n{custom}")
    if transcript:
        parts.append(transcript)

    if parts:
        return "\n\n".join(parts)

    strings = strings_from(payload)
    joined = "\n".join(item.strip() for item in strings if item.strip())
    return joined[-6000:] if joined else "No textual recovery payload was provided."


def handle_pre_compact(payload: dict[str, Any], root: Path, recovery_path: str) -> dict[str, Any]:
    latest_path = recovery_snapshot_path(root, recovery_path)
    session_id = session_id_from_payload(payload)
    path = session_snapshot_path(root, recovery_path, session_id) or latest_path
    visible_session_id = session_id or "unknown"
    source = first_payload_text(payload, ["hook_event_name", "hookEventName", "source"]) or "pre-compact"
    cwd = first_payload_text(payload, ["cwd", "directory"]) or str(root)
    generated = datetime.now(UTC).replace(microsecond=0).isoformat()
    body = recovery_payload_text(payload, root)

    content = "\n".join(
        [
            "# Harness Session Recovery",
            "",
            f"- Generated: {generated}",
            f"- Event: {source}",
            f"- Session: {visible_session_id}",
            f"- Project root: {root}",
            f"- CWD: {cwd}",
            "",
            "## Recovery Context",
            "",
            body[:12000],
            "",
            "## Resume Instruction",
            "",
            "At session start, load `using-harness`, treat this file as recovery context, then run the smallest needed Harness gate before acting.",
            "",
        ]
    )

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        latest_path.parent.mkdir(parents=True, exist_ok=True)
        latest_path.write_text(content, encoding="utf-8")
    except OSError as exc:
        return decision(
            "allow",
            f"session recovery snapshot could not be written; fail-open for optional Harness hook: {exc}",
            recovery_path=str(path),
            severity="warning",
        )

    return decision(
        "allow",
        "session recovery snapshot written",
        recovery_path=str(path),
        latest_recovery_path=str(latest_path),
    )


def handle_session_start(payload: dict[str, Any], root: Path, recovery_path: str) -> dict[str, Any]:
    source = session_start_source(payload)
    if source != "compact":
        return decision(
            "allow",
            "not a compact recovery event; skip session recovery to avoid cross-session context pollution",
            source=source or "unknown",
        )

    session_id = session_id_from_payload(payload)
    path = session_snapshot_path(root, recovery_path, session_id)
    if path is None:
        return decision(
            "allow",
            "no session id found for compact recovery; skip session recovery to avoid cross-session context pollution",
            recovery_root=str(session_recovery_root(root, recovery_path)),
        )

    if not path.exists():
        return decision(
            "allow",
            "no session recovery snapshot found",
            recovery_path=str(path),
        )

    try:
        context = path.read_text(encoding="utf-8", errors="replace")[:12000]
    except OSError as exc:
        return decision(
            "allow",
            f"session recovery snapshot could not be read; fail-open for optional Harness hook: {exc}",
            recovery_path=str(path),
            severity="warning",
        )

    return decision(
        "allow",
        "session recovery snapshot found",
        recovery_path=str(path),
        additional_context=context,
    )


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve() if args.root else Path.cwd().resolve()
    payload = load_payload()

    if "_harness_hook_invalid_json" in payload:
        return emit(
            decision("allow", "invalid hook JSON; fail-open for optional Harness hook"),
            args.platform,
            args.event,
        )

    try:
        if args.event == "post-tool-use":
            output = handle_post_tool_use(payload, root, args.docs_path)
        elif args.event == "stop":
            output = handle_stop(payload)
        elif args.event == "pre-compact":
            output = handle_pre_compact(payload, root, args.recovery_path)
        else:
            output = handle_session_start(payload, root, args.recovery_path)
    except Exception as exc:  # noqa: BLE001 - hooks must never break Skill-only use.
        output = decision(
            "allow",
            f"unexpected Harness hook error; fail-open for optional hook: {exc}",
        )

    return emit(output, args.platform, args.event)


if __name__ == "__main__":
    raise SystemExit(main())
