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
- The user reports a non-tiny bug, regression, broken accepted behavior, or validation failure and the owning Feature or prior fix history is not yet known.
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

## Delegation Decision Readiness Rule

Do not return `ready` for `non-trivial` or `high-risk` work until the report includes an explicit Delegation decision.

This rule requires a decision, not automatic subagent use. A valid decision may be `not needed`, `ask user`, `authorized`, `declined`, `blocked`, or `conditional`, but it must be grounded in the task shape and recorded in the Start Gate report.

If Delegation Gate is skipped, the Start Gate outcome must be `blocked`, `needs clarification`, or another pre-work outcome instead of `ready`.

For `not needed`, include the concrete reason: for example, the work is tightly coupled, has no useful independent verification path, or coordination overhead clearly exceeds the value of delegation. Do not use generic phrases such as "single-agent is enough" without tying them to the current task.

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

## Bug Intake And Feature Attribution

Before implementation-oriented debugging for a non-tiny bugfix, decide whether the bug may belong to an existing Feature or prior fix chain.

Ask:

1. Is this a tiny local defect, such as a tiny typo, where project memory cannot change the fix?
2. Does the symptom mention an existing Feature ID, accepted behavior, prior fix, regression, validation miss, user workflow, module boundary, or error already likely to appear in docs?
3. Could fixing this without reading prior Feature, Evidence, ADR, or Lesson records cause another local patch against the wrong boundary?
4. If this belongs to a completed or accepted Feature, which Feature should receive the Patch History row after the fix?

If the answer to question 1 is no and Feature ownership or prior history is unknown, return `needs retrieval` before code search or edits. Retrieval may conclude no relevant Feature exists; record that result and then proceed according to the remaining risk.

Do not create a new Feature only because the owner is unknown. First attempt retrieval and attribution. If no existing Feature fits and the bugfix is non-trivial enough to need a durable Vision Anchor, return `needs feature`.

## Patch Churn Check

Before allowing a bugfix or follow-up patch against an already completed or accepted Feature, retrieve the Feature page and its Evidence, then inspect `## Patch History`.

Record completed-post-acceptance bugfixes as patch rows on the original Feature, using ids such as `F010.1`, `F010.2`, and `F010.3`. Do not create a new Feature only because a bug was found in an existing Feature.

Before allowing another patch in a repeated Feature fix chain, answer:

1. Is this a new coherent change, or another patch in the same failure chain?
2. Does the patch reduce the underlying complexity, or add another scenario-specific branch?
3. Are failures moving upstream toward an invariant or boundary problem?
4. Has `## Patch History` reached 3+ rows, or is there equivalent evidence of repeated validation misses?

If the Feature has 3+ Patch History rows and no `## Patch Churn Review`, do not return `ready`; return `needs vision gate`, `needs ADR`, or `needs retrieval` depending on the missing context. If patch churn is present and prior context may affect the answer, return `needs retrieval`. If the proposed path may preserve a wrong abstraction, return `needs vision gate`. If the decision changes architecture, boundary, cost, or long-term behavior, return `needs ADR`.

## Report Format

```text
Start Gate: ready | needs clarification | needs retrieval | needs vision gate | needs feature | needs spec | needs plan | needs ADR | blocked
Task class:
- tiny | routine | non-trivial | high-risk
Risk triggers:
- ...
Delegation decision:
- not needed | ask user | authorized | declined | blocked | conditional
Bug attribution:
- not triggered | existing Feature <id> | none found after retrieval | needs retrieval | needs feature
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
- For non-tiny bugfixes, do not skip Feature attribution silently. If retrieval is not needed, the Start Gate report must say why project memory cannot change the fix.
- For repeated patch chains, do not proceed directly to another implementation patch until the Patch Churn Check is resolved.
- Do not skip Delegation Gate for medium or large work just because the user did not explicitly request subagents; the gate may conclude no delegation is needed, but the decision must be explicit.
- Do not treat a missing Delegation decision as `not needed`; absence is a gate failure, not a decision.
- Do not expand scope during intake. Separate required pre-work from attractive follow-up ideas.
