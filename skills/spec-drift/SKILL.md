---
name: spec-drift
description: MUST use when real cases, validation failures, user feedback, stale specs, outdated specs, acceptance criteria drift, SDD drift, or implementation follows spec but still wrong; triggers include old spec no longer trusted, spec vs reality conflict, repeated patches caused by wrong assumptions, 过期 Spec, 验收标准偏离, 真实案例推翻假设, or SDD 跑偏.
---

# Spec Drift

## Purpose

Use this gate when the current spec, plan, or acceptance criteria may no longer represent the real goal.

Spec Drift is a trust check on the source of truth. It decides whether the agent should keep implementing against the current spec, fix an implementation bug, revise the spec first, run Vision Gate, or record a higher-level decision.

This skill routes. It does not write specs, ADRs, Evidence, or code.

## Core Rule

Do not change code until this gate allows it.

When real cases, validation, or user feedback contradict an existing spec, treating the old spec as a command can turn local correctness into long-term system drift. First decide whether the spec is still trustworthy.

## When To Use

Use Spec Drift when any of these signals appear:

- A real case, production-like sample, manual validation, or user feedback contradicts the current spec.
- The implementation follows spec but still wrong behavior appears.
- Acceptance criteria drift, stale spec, outdated spec, SDD drift, or spec vs reality conflict is mentioned.
- Repeated patches are adding scenario-specific branches because the old assumption keeps failing.
- A reviewer says the code satisfies the written requirements but misses the real goal.
- The user asks whether an existing spec should be repaired before code changes.

Do not use Spec Drift for:

- A tiny implementation bug where the current expected behavior is still clear.
- Creating a new spec from scratch. Use `start-gate` to decide whether a spec is needed.
- Original-intent alignment when no stale spec signal exists. Use `vision-gate`.
- Stale, superseded, archived, or deprecated document lifecycle bookkeeping. Use `doc-lifecycle`.

## Workflow

1. Identify the current source: Feature page, spec, plan, acceptance criteria, ADR, test expectation, or user instruction.
2. Identify the contradicting signal: real case, validation failure, user feedback, review finding, repeated patch chain, or new domain constraint.
3. Compare source vs signal vs original goal. If original goal is missing or unclear, route to `vision-gate`.
4. Classify the drift using the smallest honest category.
5. Return exactly one Spec Drift Result before any code edit.

## Drift Categories

| Category | Meaning | Next action |
| --- | --- | --- |
| `spec valid` | The spec still represents the goal; the failure is outside spec drift. | Continue with normal implementation or bugfix flow. |
| `implementation bug` | The spec is still right; code or tests failed to implement it. | Fix code through the normal bug workflow. |
| `spec needs update` | Real cases changed or corrected the requirement; old spec would cause wrong work. | Update the owning spec/Feature before code. |
| `needs vision gate` | The original goal, user pain point, or non-goal is unclear. | Run `vision-gate` before implementation. |
| `needs ADR` | The contradiction changes a stable boundary, policy, architecture rule, or external contract. | Create or update an ADR before implementation. |
| `blocked` | The agent cannot decide from available evidence. | Ask targeted clarification questions. |

## Report Format

```text
Spec Drift Result: spec valid | implementation bug | spec needs update | needs vision gate | needs ADR | blocked
Current source:
- ...
Contradicting signal:
- ...
Original goal:
- known | unclear | missing
Drift category:
- ...
Required source update:
- none | Feature/spec/plan/ADR/doc-lifecycle needed
Allowed next action:
- ...
```

## Reference Map

Use references only when their trigger applies.

- `references/spec-drift-decision-rules.md`: read when category selection is unclear, evidence conflicts, or repeated patches may be caused by a stale assumption.

## Boundaries

- Do not mark a spec stale only because an implementation is inconvenient.
- Do not keep coding against a spec once real evidence shows the spec no longer describes the goal.
- Do not silently widen scope. Separate "old spec is wrong" from "new idea is attractive."
- Do not replace Vision Gate. Vision Gate protects original intent; Spec Drift owns stale spec classification.
- Do not replace ADRs. If the drift changes a durable architectural or policy boundary, route to `needs ADR`.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Treating the written spec as a permanent command. | Treat specs as current cognition snapshots that can be corrected by evidence. |
| Treating every bug as spec drift. | If the spec still describes the goal, it is an implementation bug. |
| Adding branches for every new sample. | Check whether the sample invalidates an upstream assumption. |
| Letting tests prove the spec is right. | Passing tests prove conformance to current expectations, not that those expectations are still true. |
