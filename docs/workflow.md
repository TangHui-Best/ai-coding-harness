# Workflow

The recommended harness loop:

1. Run Start Gate before non-trivial implementation.
2. Retrieve relevant project context when the gate or task risk requires it.
3. Clarify the user goal, constraints, and acceptance criteria.
4. Create only the required pre-work anchor: Feature, spec, plan, ADR, Backlog, or handoff note.
5. Execute the smallest coherent change.
6. Verify with concrete evidence.
7. Use the readiness dashboard when review, release, handoff, or completion needs a status rollup.
8. Capture durable knowledge only when future work would benefit.
9. Write a compact change narrative for review, handoff, or history.
10. Run the project-rules gate before promoting any source-backed constraint into `AGENTS.md`.

The loop should stay lightweight. Harness is not a documentation tax; it is a way to prevent repeated rediscovery and unverifiable completion.
