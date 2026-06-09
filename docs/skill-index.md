# Skill Index

This repository is an **AgentMentor Skill suite**. Each directory under `skills/` contains one installable Skill with a `SKILL.md` entrypoint. `using-agentmentor` is the high-recall entrypoint; it routes to the smallest specific workflow that protects the project from lost context, unverifiable completion, repeated incidents, or unclear handoff.

Formal naming: use `AgentMentor` when introducing the system or when a project has its own test harness, runtime harness, evaluation harness, or business concept named harness. The formal skill slugs are `using-agentmentor` plus short semantic workflow slugs such as `start-gate` and `readiness-dashboard`; pre-rename names were removed by the breaking rename documented in ADR-008.

## Skills

| Skill | Responsibility |
| --- | --- |
| `using-agentmentor` | Route the current task to the right AgentMentor workflow. |
| `start-gate` | Decide whether non-trivial work may start or needs clarification, retrieval, Spec Drift, Vision Gate, patch-churn review, Feature, spec, plan, or ADR first. |
| `delegation-gate` | Decide whether to ask for implementation subagents or independent reviewers. |
| `knowledge-retrieval` | Recover project context before acting. |
| `spec-drift` | Decide whether a current spec or acceptance criteria is still trustworthy before changing code. |
| `doc-lifecycle` | Interpret stale, superseded, deprecated, or archived documents. |
| `incident-learning` | Turn fixed failures and repeated patch chains into prevention. |
| `vision-gate` | Check original intent and abstraction fit before implementation and before review, merge, done, release, or handoff. |
| `readiness-dashboard` | Summarize gate, reviewer, evidence, patch-churn, and knowledge status before review, release, handoff, or completion. |
| `change-narrative` | Explain a specific change for commits, PRs, handoffs, and release notes. |
| `knowledge-capture` | Decide whether durable memory is needed and record the smallest useful artifact. |
| `project-rules` | Decide whether source-backed AgentMentor memory should become a project-level agent rule. |

## Typical Flow

```text
Start work
  -> start-gate
  -> delegation-gate, when implementation subagents or independent review may reduce risk
  -> knowledge-retrieval
  -> spec-drift, when real cases or validation contradict an existing spec
  -> vision-gate, when intent or scope may drift before implementation
  -> pre-work artifact, when Start Gate requires Feature, spec, plan, or ADR
  -> implementation workflow
  -> verification
  -> vision-gate, when deliverable-goal drift is possible
  -> readiness-dashboard, when a status rollup or blocker list is needed
  -> change-narrative, when the change needs explanation
  -> knowledge-capture, before completion or handoff
  -> project-rules, before editing AGENTS.md or project agent rules
```

Not every task needs every skill. The point is to choose the lightest workflow that preserves what future work will need.

## Proposals

- [Patch Churn 与归零审视：AgentMentor Skill 迭代方案](proposals/2026-05-15-patch-churn-zero-base-review.md)

## Articles

- [AgentMentor: 把 AI Agent 纳入可治理的软件开发流程](articles/agentmentor-governable-ai-agent-development-flow.md)
