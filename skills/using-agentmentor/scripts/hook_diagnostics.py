#!/usr/bin/env python3
"""Diagnose optional AgentMentor hook installation and runtime evidence."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose optional AgentMentor hook runtime wiring.")
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


def run_runner_smoke(project_root: Path) -> dict[str, Any]:
    hook_runner = Path(__file__).resolve().parents[1] / "hooks" / "agentmentor_hook.py"
    if not hook_runner.exists():
        return check("warning", f"AgentMentor hook runner not found: {hook_runner}")

    payload = {
        "session_id": "agentmentor-hook-diagnostic",
        "last_assistant_message": "I am inspecting the repository and will continue.",
    }
    command = [
        sys.executable,
        str(hook_runner),
        "--event",
        "stop",
        "--platform",
        "generic",
        "--root",
        str(project_root),
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

    if output.get("decision") == "allow" and "no completion claim" in output.get("reason", ""):
        return check("pass", "AgentMentor Stop runner can inspect a non-completion message")

    return check("warning", "runner smoke did not report the expected Stop allow result", output=output)


def overall_status(checks: dict[str, dict[str, Any]]) -> str:
    statuses = {item["status"] for item in checks.values()}
    if "fail" in statuses:
        return "fail"
    if "warning" in statuses:
        return "warning"
    return "pass"


def render_text(output: dict[str, Any]) -> str:
    lines = [
        f"AgentMentor hook diagnostics: {output['status']}",
        f"Generated: {output['generated_at']}",
        f"Platform: {output['platform']}",
        f"Project root: {output['project_root']}",
    ]
    for name, result in output["checks"].items():
        lines.append("")
        lines.append(f"[{result['status']}] {name}")
        lines.append(str(result["reason"]))
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
