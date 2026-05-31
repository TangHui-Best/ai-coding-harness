---
name: harness-readiness-dashboard
description: MUST use before non-trivial review, merge, release, handoff, PR readiness, or completion claims when Codex needs to summarize Harness gate status, source documents, delegation and reviewer independence, evidence level, patch-churn risk, ADR/Lesson triggers, remaining blockers, ready 检查, 收尾前状态, 是否可以交付, 是否可以 review, 是否可以 handoff, 反复补丁, or 归零审视 without creating new artifacts.
---

# Harness Readiness Dashboard

## Purpose

Answer one question:

```text
Can this work safely move to review, release, handoff, or completion?
```

This is a status aggregation skill. It does not replace Start Gate, Vision Gate, Evidence, review, or knowledge capture, and it does not create official Feature, ADR, Lesson, or Evidence artifacts.

## Inputs

Gather only the smallest relevant set:

- Original request, Feature, spec, plan, or acceptance criteria.
- Latest Start Gate, Knowledge Retrieval, Vision Gate, review, and verification outputs if available.
- Evidence location or final verification commands.
- Bugfix attribution result and owning Feature Patch History for non-tiny bugfixes.
- Changed files, PR body, commit messages, or handoff note when present.
- ADR, Lesson, Backlog, or Feature status only when the current task may affect them.

If a source is missing, mark it as `missing`; do not invent status from memory.

## Core Rules

Use these status values:

```text
pass | missing | stale | not needed | pending | blocked
```

For `non-trivial` or `high-risk` work, mark `Delegation Gate` as `missing` when no explicit Delegation Gate decision is available.

Do not convert missing Delegation Gate evidence into self-review just because implementation is already finished. If delegation or independent review would have reduced risk but no explicit `single_agent`, `delegate`, or `blocked` decision exists, mark readiness as `conditional` or `blocked` and name the residual risk.

For non-tiny bugfixes, `Ready: yes` requires Bugfix Attribution to be `pass` or `not needed` with a reason. If an existing completed Feature owns the behavior and Patch History was not updated, readiness is `no` or `conditional`.

If a Feature has 3+ `## Patch History` rows or equivalent patch churn and no `## Patch Churn Review` is available, readiness must be `conditional` or `no`, not `yes`.

## Reference Map

Use references only when their trigger applies.

- `references/readiness-checks.md`: read when row-by-row readiness, reviewer policy, patch churn action, or the full output format is needed.

## Compact Output

```text
Harness Readiness Dashboard
Task class: tiny | routine | non-trivial | high-risk
Current stage: implementation | review | release | handoff | completion
Evidence Level: quick | standard | exhaustive
Delegation Gate: single_agent | delegate | missing | blocked
Bugfix Attribution: pass | missing | ambiguous | not needed
Ready: yes | no | conditional
Blockers:
- ...
Next action:
- ...
```

Use `conditional` only when the work can proceed with explicitly named residual risk.

## Boundaries

- Do not create new documents from this skill; route to `harness-knowledge-capture`.
- Do not re-run Vision Gate here; report whether it exists and whether it is needed.
- Do not treat passing tests as product alignment; that belongs to Vision Gate.
- Do not treat a dashboard as Evidence; it only points to Evidence.
