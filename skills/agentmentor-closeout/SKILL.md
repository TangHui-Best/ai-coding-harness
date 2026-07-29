---
name: agentmentor-closeout
description: Use when pausing, handing off, or finishing an engineering task and a compact recoverable state is useful. Compress only facts already established in the current task; do not run retrieval, dashboards, global scans, or mandatory document creation.
---

# AgentMentor Closeout

Create a short state compression, not an exit gate.

1. Reuse the current task's implementation state, checks, limitations, and next safe action.
2. Return exactly one status: `done`, `partial`, or `blocked`.
3. Use `assets/templates/CLOSEOUT_COMPACT.md` when a visible handoff block is useful.
4. Route to evidence, decision, or learning only when an already observed event independently warrants durable memory.

Do not repeat context retrieval, document validation, readiness assessment, or task classification.
