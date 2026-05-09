# Skill Index

This repository uses `using-harness` as the entrypoint. The entrypoint routes to the smallest specific workflow that protects the project from lost context, unverifiable completion, repeated incidents, or unclear handoff.

## Skills

| Skill | Responsibility |
| --- | --- |
| `using-harness` | Route the current task to the right harness workflow. |
| `harness-knowledge-retrieval` | Recover project context before acting. |
| `harness-doc-lifecycle` | Interpret stale, superseded, deprecated, or archived documents. |
| `harness-incident-learning` | Turn fixed failures into prevention. |
| `harness-vision-gate` | Check original intent before review, merge, done, release, or handoff. |
| `harness-change-narrative` | Explain a specific change for commits, PRs, handoffs, and release notes. |
| `harness-knowledge-capture` | Decide whether durable memory is needed and record the smallest useful artifact. |

## Typical Flow

```text
Start work
  -> harness-knowledge-retrieval
  -> implementation workflow
  -> verification
  -> harness-vision-gate, when intent drift is possible
  -> harness-change-narrative, when the change needs explanation
  -> harness-knowledge-capture, before completion or handoff
```

Not every task needs every skill. The point is to choose the lightest workflow that preserves what future work will need.
