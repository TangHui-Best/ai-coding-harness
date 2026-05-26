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

This rule requires a decision, not automatic subagent use. A valid decision may be `not needed`, `ask user`, `authorized`, `declined`, `blocked`, or `conditional`, but it must be grounded in the task shape and recorded in the Start Gate report.

If Delegation Gate is skipped, the Start Gate outcome must be `blocked`, `needs clarification`, or another pre-work outcome instead of `ready`.

For `not needed`, include the concrete reason. Do not treat a missing Delegation decision as `not needed`; absence is a gate failure, not a decision.

## Bug Intake

For a non-tiny bug, regression, broken accepted behavior, or validation failure, decide whether existing project memory may affect the fix before code search or edits.

Tiny local edits where project memory cannot change the outcome may skip retrieval, such as a tiny typo in a test fixture or comment, but the Start Gate report must say why.

If ownership or prior history is unknown, return `needs retrieval` before code search or edits.

If an accepted or completed Feature owns the behavior, record which Feature should receive the Patch History row after the fix.

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
- not needed | ask user | authorized | declined | blocked | conditional
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
