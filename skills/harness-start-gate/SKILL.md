---
name: harness-start-gate
description: MUST use before starting non-trivial AI-assisted engineering work, multi-file bugfixes, behavior changes, refactors, or implementation after task intake to decide whether the agent may implement now or must first clarify scope, retrieve project knowledge, run Vision Gate, run Delegation Gate, or create/update a Feature, spec, plan, ADR, Backlog, or handoff anchor; triggers include development kickoff, pre-coding checks, implementation readiness, ambiguity checks, repeated patch chains, patch churn, Fxxx.n follow-ups, subagent/delegation decisions, 开发前检查, 开工门禁, 需求边界, 前置沉淀, 反复补丁, 归零审视, or 防止直接开工.
---

# Harness Start Gate

## Purpose

Use this gate before implementation. Decide whether the next action is safe to begin or whether the work first needs clarification, retrieval, alignment, or durable pre-work memory.

This skill is a routing gate. It does not write Feature pages, specs, plans, ADRs, Evidence, or code.

## Workflow

1. Classify the task.
2. Check risk triggers.
3. Check whether Delegation Gate is needed.
4. Choose exactly one primary outcome.
5. Route to the smallest required next action.
6. Report the gate result before implementation starts.

## Task Classes

Use the lightest class that honestly fits:

| Class | Meaning | Default gate pressure |
| --- | --- | --- |
| `tiny` | Local, reversible edit where project memory cannot change the outcome. | Usually `ready`. |
| `routine` | Bounded change with clear intent and known verification path. | Usually retrieval optional. |
| `non-trivial` | Feature work, refactor, behavior change, multi-file change, or unclear acceptance criteria. | Run retrieval or Vision Gate when triggered. |
| `high-risk` | Boundary, architecture, data model, security, cost, migration, or cross-feature decision. | Require durable pre-work anchor before implementation. |

## Risk Triggers

Check these before coding:

- The original goal, user pain point, acceptance criteria, non-goals, Vision Anchor, or owner boundary is unclear.
- The task spans multiple sessions, agents, modules, or delivery steps.
- The work changes public behavior, data shape, module boundaries, storage, infrastructure, permissions, or external contracts.
- The agent needs prior decisions, active Feature state, stale-doc status, Lessons, or Evidence to avoid repeating work.
- A future agent would need to know why this path was chosen before safely continuing.
- The proposed implementation path looks broader, costlier, or more complex than the user goal requires.
- The task may have separable workstreams, parallel exploration, independent verification, or enough scope that implementation subagents should be proposed.
- The only way to recover context later would be the chat transcript.
- The task is another fix in a repeated Feature patch chain, such as `Fxxx.n` follow-ups or multiple validation fixes after the Feature was considered done.
- The proposed fix adds scenario-specific rules, keywords, filters, fallback branches, or downstream cleanup instead of reducing the underlying invariant or boundary problem.
- Tests pass but manual validation keeps exposing related failures, suggesting the current abstraction may not explain the real user goal.

## Delegation Check

For `non-trivial` or `high-risk` work, run `harness-delegation-gate` in `implementation` mode before coding when the task may be split across subagents or parallel work could reduce latency, tunnel vision, or recovery risk.

Do not default to subagents. If Delegation Gate says `ask user`, ask a concise permission question and wait before spawning. If Delegation Gate says `not needed`, include the reason in the Start Gate report.

## Outcomes

Return exactly one primary outcome:

| Outcome | Use when | Required next action |
| --- | --- | --- |
| `ready` | Intent, scope, ownership, verification, and risk are clear enough for the task class. | Start implementation workflow. |
| `needs clarification` | Missing user intent or acceptance details could change the implementation. | Ask specific questions before coding. |
| `needs retrieval` | Existing Feature, ADR, Lesson, Evidence, stale-doc, or prior decision context may affect the work. | Use `harness-knowledge-retrieval`. |
| `needs vision gate` | The path may drift from the original goal or solve the wrong problem. | Use `harness-vision-gate` Entry Gate. |
| `needs feature` | The work changes or starts a delivery boundary that future sessions must recover, or non-trivial work lacks a durable Vision Anchor. | Use `harness-knowledge-capture` to create or update a Feature anchor. |
| `needs spec` | Requirements or acceptance criteria need a durable source before implementation. | Create or update a spec, then link it from the Feature when applicable. |
| `needs plan` | Execution order, decomposition, rollback, or multi-agent coordination needs a durable route. | Create or update a plan, then link it from the Feature when applicable. |
| `needs ADR` | A decision affects long-term architecture, interfaces, cost, security, operations, or likely future debate. | Use `harness-knowledge-capture` to create an ADR before coding. |
| `blocked` | Required context, permissions, environment, or decision owner is unavailable. | Stop and name the blocker. |

If multiple outcomes apply, choose the earliest blocker in this order:

```text
blocked -> needs clarification -> needs retrieval -> needs vision gate
  -> needs feature -> needs spec -> needs plan -> needs ADR -> ready
```

## Patch Churn Check

Before allowing another patch in a repeated Feature fix chain, answer:

1. Is this a new coherent change, or another patch in the same failure chain?
2. Does the patch reduce the underlying complexity, or add another scenario-specific branch?
3. Are failures moving upstream toward an invariant or boundary problem?
4. Has the Feature crossed a practical patch-churn threshold, such as 3+ follow-up fixes or equivalent repeated validation misses?

If patch churn is present and prior context may affect the answer, return `needs retrieval`. If the proposed path may preserve a wrong abstraction, return `needs vision gate`. If the decision changes architecture, boundary, cost, or long-term behavior, return `needs ADR`.

## Report Format

```text
Start Gate: ready | needs clarification | needs retrieval | needs vision gate | needs feature | needs spec | needs plan | needs ADR | blocked
Task class:
- tiny | routine | non-trivial | high-risk
Risk triggers:
- ...
Delegation decision:
- not needed | ask user | authorized | declined | blocked | conditional
Required pre-work:
- ...
Allowed next action:
- ...
```

## Boundaries

- Do not use this gate to create documents for every small task.
- Do not let a passing Start Gate replace verification, Evidence, or completion-time knowledge capture.
- Do not use Vision Gate to decide whether a Feature/spec/plan/ADR exists; Start Gate owns that intake decision.
- For non-trivial work, do not proceed with only chat history as the future Vision Gate source. Require a Feature, linked spec, or another durable Vision Anchor first.
- For repeated patch chains, do not proceed directly to another implementation patch until the Patch Churn Check is resolved.
- Do not skip Delegation Gate for medium or large work just because the user did not explicitly request subagents; the gate may conclude no delegation is needed, but the decision must be explicit.
- Do not expand scope during intake. Separate required pre-work from attractive follow-up ideas.
