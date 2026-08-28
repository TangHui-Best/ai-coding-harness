#!/usr/bin/env python3
"""Repository command entrypoint for the bundled AgentMentor index generator."""

from pathlib import Path
import runpy


runpy.run_path(
    Path(__file__).resolve().parents[1] / "skills" / "agentmentor" / "scripts" / "generate_index.py",
    run_name="__main__",
)
