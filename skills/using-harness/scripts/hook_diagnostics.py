#!/usr/bin/env python3
"""Diagnose optional Harness hook installation and runtime evidence."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose optional Harness hook runtime wiring.")
    subparsers = parser.add_subparsers(dest="platform", required=True)
    codex = subparsers.add_parser("codex", help="Diagnose Codex plugin hook wiring.")
    codex.add_argument("--codex-home", default=str(Path.home() / ".codex"))
    codex.add_argument("--project-root", default=".")
    codex.add_argument("--format", choices=["text", "json"], default="text")
    codex.add_argument(
        "--skip-runner-smoke",
        action="store_true",
        help="Skip the local runner smoke test and only inspect stored evidence.",
    )
    return parser.parse_args()


def check(status: str, reason: str, **extra: Any) -> dict[str, Any]:
    result: dict[str, Any] = {"status": status, "reason": reason}
    result.update(extra)
    return result


def normalize(path: Path) -> str:
    try:
        return str(path.resolve()).casefold()
    except OSError:
        return str(path).casefold()


def first_json_line(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    parsed = json.loads(line)
                except json.JSONDecodeError:
                    return None
                return parsed if isinstance(parsed, dict) else None
    except OSError:
        return None
    return None


def session_cwd(path: Path) -> str | None:
    first = first_json_line(path)
    payload = first.get("payload") if isinstance(first, dict) else None
    if not isinstance(payload, dict):
        return None
    cwd = payload.get("cwd")
    return cwd if isinstance(cwd, str) else None


def has_compaction_event(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if '"type":"compacted"' in line or '"type": "compacted"' in line:
                    return True
                if "context_compacted" in line:
                    return True
    except OSError:
        return False
    return False


def recovery_artifacts(project_root: Path) -> list[Path]:
    recovery_root = project_root / ".harness" / "session-recovery"
    if not recovery_root.exists():
        return []
    try:
        return [path for path in recovery_root.rglob("*.md") if path.is_file()]
    except OSError:
        return []


def scan_codex_compactions(codex_home: Path, project_root: Path) -> dict[str, Any]:
    sessions_root = codex_home / "sessions"
    if not sessions_root.exists():
        return check("not_applicable", f"Codex sessions directory not found: {sessions_root}")

    project_key = normalize(project_root)
    matching_logs: list[str] = []
    compacted_logs: list[str] = []
    for session_log in sessions_root.rglob("*.jsonl"):
        cwd = session_cwd(session_log)
        if cwd is None or normalize(Path(cwd)) != project_key:
            continue
        matching_logs.append(str(session_log))
        if has_compaction_event(session_log):
            compacted_logs.append(str(session_log))

    if not compacted_logs:
        return check(
            "not_applicable",
            "no Codex compacted/context_compacted events found for this project root",
            matching_session_logs=len(matching_logs),
        )

    artifacts = recovery_artifacts(project_root)
    if artifacts:
        return check(
            "pass",
            "Codex compaction events and Harness recovery artifacts were both found",
            matching_session_logs=len(matching_logs),
            compaction_logs=compacted_logs,
            recovery_artifacts=[str(path) for path in artifacts],
            compactions_without_hook_evidence=0,
        )

    return check(
        "warning",
        "Codex compacted/context_compacted events were found, but no Harness session recovery artifact exists",
        matching_session_logs=len(matching_logs),
        compaction_logs=compacted_logs,
        recovery_artifacts=[],
        compactions_without_hook_evidence=len(compacted_logs),
    )


def run_runner_smoke(project_root: Path) -> dict[str, Any]:
    hook_runner = Path(__file__).resolve().parents[1] / "hooks" / "harness_hook.py"
    if not hook_runner.exists():
        return check("warning", f"Harness hook runner not found: {hook_runner}")

    recovery_path = ".tmp/harness-hook-diagnostic/latest.md"
    payload = {
        "session_id": "harness-hook-diagnostic",
        "source": "manual",
        "summary": "Diagnostic smoke test for optional Harness pre-compact runner.",
    }
    command = [
        sys.executable,
        str(hook_runner),
        "--event",
        "pre-compact",
        "--platform",
        "generic",
        "--root",
        str(project_root),
        "--recovery-path",
        recovery_path,
    ]
    try:
        result = subprocess.run(
            command,
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return check("warning", f"runner smoke could not execute: {exc}")

    cleanup_root = project_root / ".tmp" / "harness-hook-diagnostic"
    try:
        if cleanup_root.exists() and normalize(cleanup_root).startswith(normalize(project_root / ".tmp")):
            shutil.rmtree(cleanup_root)
    except OSError:
        pass

    if result.returncode != 0:
        return check(
            "warning",
            "runner smoke exited non-zero",
            returncode=result.returncode,
            stderr=result.stderr.strip(),
        )

    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        return check("warning", "runner smoke did not return JSON", stdout=result.stdout[:1000])

    if output.get("decision") == "allow" and "recovery_path" in output:
        return check("pass", "Harness pre-compact runner can write a recovery snapshot")

    return check("warning", "runner smoke did not report a recovery snapshot", output=output)


def overall_status(checks: dict[str, dict[str, Any]]) -> str:
    statuses = {item["status"] for item in checks.values()}
    if "fail" in statuses:
        return "fail"
    if "warning" in statuses:
        return "warning"
    return "pass"


def render_text(output: dict[str, Any]) -> str:
    lines = [
        f"Harness hook diagnostics: {output['status']}",
        f"Generated: {output['generated_at']}",
        f"Platform: {output['platform']}",
        f"Project root: {output['project_root']}",
    ]
    for name, result in output["checks"].items():
        lines.append("")
        lines.append(f"[{result['status']}] {name}")
        lines.append(str(result["reason"]))
        if result.get("compaction_logs"):
            lines.append("Compaction logs:")
            for path in result["compaction_logs"]:
                lines.append(f"- {path}")
        if result.get("recovery_artifacts"):
            lines.append("Recovery artifacts:")
            for path in result["recovery_artifacts"]:
                lines.append(f"- {path}")
    return "\n".join(lines)


def run_codex(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root).resolve()
    codex_home = Path(args.codex_home).resolve()
    checks: dict[str, dict[str, Any]] = {}
    checks["runner_smoke"] = (
        check("not_applicable", "runner smoke skipped")
        if args.skip_runner_smoke
        else run_runner_smoke(project_root)
    )
    checks["codex_compaction_triggers"] = scan_codex_compactions(codex_home, project_root)
    return {
        "status": overall_status(checks),
        "generated_at": datetime.now(UTC).isoformat(),
        "platform": "codex",
        "project_root": str(project_root),
        "codex_home": str(codex_home),
        "checks": checks,
    }


def main() -> int:
    args = parse_args()
    output = run_codex(args)
    if args.format == "json":
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(render_text(output))
    return {"pass": 0, "warning": 1, "fail": 2}[output["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
