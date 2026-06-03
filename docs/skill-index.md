# Skill Index

This repository is an **AI Coding Harness Skill suite**. Each directory under `skills/` contains one installable Skill with a `SKILL.md` entrypoint. `ai-coding-harness` is the high-recall entrypoint; it routes to the smallest specific workflow that protects the project from lost context, unverifiable completion, repeated incidents, or unclear handoff.

Formal naming: use `AI Coding Harness` when introducing the system or when a project has its own test harness, runtime harness, evaluation harness, or business concept named harness. The formal skill slugs are `ai-coding-harness` and `ai-coding-harness-*`; pre-rename names were removed by the breaking rename documented in ADR-007.

## Skills

| Skill | Responsibility |
| --- | --- |
| `ai-coding-harness` | Route the current task to the right harness workflow. |
| `ai-coding-harness-start-gate` | Decide whether non-trivial work may start or needs clarification, retrieval, Vision Gate, patch-churn review, Feature, spec, plan, or ADR first. |
| `ai-coding-harness-delegation-gate` | Decide whether to ask for implementation subagents or independent reviewers. |
| `ai-coding-harness-knowledge-retrieval` | Recover project context before acting. |
| `ai-coding-harness-doc-lifecycle` | Interpret stale, superseded, deprecated, or archived documents. |
| `ai-coding-harness-incident-learning` | Turn fixed failures and repeated patch chains into prevention. |
| `ai-coding-harness-vision-gate` | Check original intent and abstraction fit before implementation and before review, merge, done, release, or handoff. |
| `ai-coding-harness-readiness-dashboard` | Summarize gate, reviewer, evidence, patch-churn, and knowledge status before review, release, handoff, or completion. |
| `ai-coding-harness-change-narrative` | Explain a specific change for commits, PRs, handoffs, and release notes. |
| `ai-coding-harness-knowledge-capture` | Decide whether durable memory is needed and record the smallest useful artifact. |
| `ai-coding-harness-project-rules` | Decide whether source-backed Harness memory should become a project-level agent rule. |

## Typical Flow

```text
Start work
  -> ai-coding-harness-start-gate
  -> ai-coding-harness-delegation-gate, when implementation subagents or independent review may reduce risk
  -> ai-coding-harness-knowledge-retrieval
  -> ai-coding-harness-vision-gate, when intent or scope may drift before implementation
  -> pre-work artifact, when Start Gate requires Feature, spec, plan, or ADR
  -> implementation workflow
  -> verification
  -> ai-coding-harness-vision-gate, when deliverable-goal drift is possible
  -> ai-coding-harness-readiness-dashboard, when a status rollup or blocker list is needed
  -> ai-coding-harness-change-narrative, when the change needs explanation
  -> ai-coding-harness-knowledge-capture, before completion or handoff
  -> ai-coding-harness-project-rules, before editing AGENTS.md or project agent rules
```

Not every task needs every skill. The point is to choose the lightest workflow that preserves what future work will need.

## Proposals

- [Patch Churn 与归零审视：AI Coding Harness Skill 迭代方案](proposals/2026-05-15-patch-churn-zero-base-review.md)
