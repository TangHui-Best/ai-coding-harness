# Architecture

The harness is organized around a small set of durable capabilities:

- Workflow: reusable task procedures
- Knowledge: recoverable project memory
- Gate: explicit checks before risky transitions, including Start Gate before non-trivial implementation
- Readiness: concise status rollups before review, release, handoff, or completion
- Evidence: verifiable completion records
- Narrative: compact explanations of what changed and why
- Lifecycle: document freshness, supersession, and archive rules
- Project rules: source-backed behavior constraints that belong in `AGENTS.md`

These capabilities can start as lightweight Markdown conventions and gradually move into scripts, CI checks, indexes, and runtime enforcement.
