# Architecture

The harness is organized around a small set of durable capabilities:

- Workflow: reusable task procedures
- Knowledge: recoverable project memory
- Gate: explicit checks before risky transitions
- Evidence: verifiable completion records
- Narrative: compact explanations of what changed and why
- Lifecycle: document freshness, supersession, and archive rules

These capabilities can start as lightweight Markdown conventions and gradually move into scripts, CI checks, indexes, and runtime enforcement.
