#!/usr/bin/env python3
"""Repository command entrypoint for the bundled AgentMentor vNext validator."""

from pathlib import Path
import runpy
import sys


_script = Path(__file__).resolve().parents[1] / "skills" / "agentmentor" / "scripts" / "knowledge_check.py"
sys.path.insert(0, str(_script.parent))
runpy.run_path(
    _script,
    run_name="__main__",
)
