---
name: harness-start-gate
description: MUST use before starting non-trivial AI-assisted engineering work, multi-file bugfixes, behavior changes, refactors, or implementation after task intake to decide whether the agent may implement now or must first clarify scope, retrieve project knowledge, run Vision Gate, run Delegation Gate, or create/update a Feature, spec, plan, ADR, Backlog, or handoff anchor; triggers include development kickoff, pre-coding checks, implementation readiness, ambiguity checks, repeated patch chains, patch churn, Fxxx.n follow-ups, subagent/delegation decisions, 开发前检查, 开工门禁, 需求边界, 前置沉淀, 反复补丁, 归零审视, or 防止直接开工.
---

# Harness Start Gate

## Purpose

Use this gate before implementation. Decide whether the next action is safe to begin or whether the work first needs clarification, retrieval, alignment, delegation, or durable pre-work memory.

This skill routes. It does not write Feature pages, specs, plans, ADRs, Evidence, or code.

## Workflow

1. Classify the task as `tiny`, `routine`, `non-trivial`, or `high-risk`.
2. Check whether retrieval, Vision Gate, Delegation Gate, Feature, spec, plan, ADR, Backlog, or handoff anchor is needed.
3. Choose exactly one primary outcome.
4. Report the Start Gate result before implementation starts.

## Task Classes

Use the lightest class that honestly fits:

| Class | Meaning | Default gate pressure |
| --- | --- | --- |
| `tiny` | Local, reversible edit where project memory cannot change the outcome. | Usually `ready`. |
| `routine` | Bounded change with clear intent and known verification path. | Usually retrieval optional. |
| `non-trivial` | Feature work, refactor, behavior change, multi-file change, or unclear acceptance criteria. | Run retrieval or Vision Gate when triggered. |
| `high-risk` | Boundary, architecture, data model, security, cost, migration, cross-feature decision, or process rule change. | Require a durable pre-work anchor before implementation. |

## Risk Triggers

Check these before coding:

- Original goal, user pain point, acceptance criteria, non-goals, Vision Anchor, or owner boundary is unclear.
- Work spans multiple sessions, agents, modules, or delivery steps.
- Work changes public behavior, data shape, module boundaries, storage, infrastructure, permissions, external contracts, or Harness process rules.
- Prior decisions, active Feature state, stale-doc status, Lessons, Evidence, or patch history may affect the answer.
- The proposed path looks broader, costlier, or more complex than the user goal requires.
- The task may have separable workstreams, parallel exploration, independent verification, or enough scope that implementation subagents should be proposed.
- The only way to recover context later would be the chat transcript.
- Superpowers spec or plan paths are being used for work that needs official Harness Feature, ADR, Lesson, or Evidence memory.

## Core Outcomes

Return exactly one primary outcome:

```text
ready | needs clarification | needs retrieval | needs vision gate | needs feature | needs spec | needs plan | needs ADR | blocked
```

If multiple outcomes apply, choose the earliest blocker:

```text
blocked -> needs clarification -> needs retrieval -> needs vision gate
  -> needs feature -> needs spec -> needs plan -> needs ADR -> ready
```

## Delegation Decision Readiness Rule

Do not return `ready` for `non-trivial` or `high-risk` work until the report includes an explicit Delegation decision.

This rule requires a decision, not automatic subagent use. A valid decision must be `single_agent`, `delegate`, or `blocked`, grounded in the task shape and recorded in the Start Gate report.

If Delegation Gate is skipped, the Start Gate outcome must be `blocked`, `needs clarification`, or another pre-work outcome instead of `ready`.

For `single_agent`, include the concrete reason. Do not treat a missing Delegation decision as `single_agent`; absence is a gate failure, not a decision.

## Bug Intake

For a non-tiny bug, regression, broken accepted behavior, or validation failure, decide whether existing project memory may affect the fix before code search or edits.

Tiny local edits where project memory cannot change the outcome may skip retrieval, such as a tiny typo in a test fixture or comment, but the Start Gate report must say why.

If ownership or prior history is unknown, return `needs retrieval` before code search or edits.

If an accepted or completed Feature owns the behavior, record which Feature should receive the Patch History row after the fix.

## Patch Churn Check

Before allowing a bugfix or follow-up patch against an already completed or accepted Feature, retrieve the Feature page and inspect `## Patch History`.

Completed post-acceptance bugfixes are patch rows on the original Feature, using ids such as `F010.1`, `F010.2`, and `F010.3`. Do not create a new Feature only because a bug was found in an existing Feature.

If the Feature has 3+ Patch History rows, `Fxxx.n` patch slices, repeated validation misses, or growing scenario-specific rule branches and no `## Patch Churn Review`, do not return `ready`. Return `needs retrieval`, `needs vision gate`, or `needs ADR` depending on the missing context.

## Reference Map

Use references only when their trigger applies.

- `references/start-gate-decision-rules.md`: read when task class, outcome ordering, risk triggers, durable anchor requirements, or report details are unclear.
- `references/bug-intake-and-patch-churn.md`: read for non-tiny bugfixes, completed Feature follow-up fixes, `Fxxx.n` patches, repeated validation misses, or 3+ Patch History rows.

## Report Format

```text
Start Gate: ready | needs clarification | needs retrieval | needs vision gate | needs feature | needs spec | needs plan | needs ADR | blocked
Task class:
- tiny | routine | non-trivial | high-risk
Risk triggers:
- ...
Delegation decision:
- single_agent | delegate | blocked
Bug attribution:
- not triggered | existing Feature <id> | none found after retrieval | needs retrieval | needs feature
Required pre-work:
- ...
Allowed next action:
- ...
```

## Boundaries

- Do not create documents for every small task.
- Do not let a passing Start Gate replace verification, Evidence, or completion-time knowledge capture.
- Do not use Vision Gate to decide whether a Feature/spec/plan/ADR exists; Start Gate owns that intake decision.
- For non-trivial work, do not proceed with only chat history as the future Vision Gate source. Require a Feature, linked spec, or another durable Vision Anchor first.
- Absence of `docs/features/` is not a reason to skip Feature memory. When non-trivial work needs a durable Vision Anchor, create the first canonical Feature page under `docs/features/Fxxx-slug.md`.
- Treat `docs/superpowers/**` as legacy spec/plan material only. Do not place Harness Feature, ADR, Lesson, or Evidence artifacts there.
- For non-tiny bugfixes, do not skip Feature attribution silently. If retrieval is not needed, the Start Gate report must say why project memory cannot change the fix.
- Do not skip Delegation Gate for medium or large work just because the user did not explicitly request subagents; the gate may conclude no delegation is needed, but the decision must be explicit.
