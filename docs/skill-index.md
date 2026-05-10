# Skill Index

This repository uses `using-harness` as the entrypoint. The entrypoint routes to the smallest specific workflow that protects the project from lost context, unverifiable completion, repeated incidents, or unclear handoff.

## Skills

| Skill | Responsibility |
| --- | --- |
| `using-harness` | Route the current task to the right harness workflow. |
| `harness-start-gate` | Decide whether non-trivial work may start or needs clarification, retrieval, Vision Gate, Feature, spec, plan, or ADR first. |
| `harness-knowledge-retrieval` | Recover project context before acting. |
| `harness-doc-lifecycle` | Interpret stale, superseded, deprecated, or archived documents. |
| `harness-incident-learning` | Turn fixed failures into prevention. |
| `harness-vision-gate` | Check original intent before implementation and before review, merge, done, release, or handoff. |
| `harness-change-narrative` | Explain a specific change for commits, PRs, handoffs, and release notes. |
| `harness-knowledge-capture` | Decide whether durable memory is needed and record the smallest useful artifact. |
| `harness-project-rules` | Decide whether source-backed Harness memory should become a project-level agent rule. |

## Typical Flow

```text
Start work
  -> harness-start-gate
  -> harness-knowledge-retrieval
  -> harness-vision-gate, when intent or scope may drift before implementation
  -> pre-work artifact, when Start Gate requires Feature, spec, plan, or ADR
  -> implementation workflow
  -> verification
  -> harness-vision-gate, when deliverable-goal drift is possible
  -> harness-change-narrative, when the change needs explanation
  -> harness-knowledge-capture, before completion or handoff
  -> harness-project-rules, before editing AGENTS.md or project agent rules
```

Not every task needs every skill. The point is to choose the lightest workflow that preserves what future work will need.
