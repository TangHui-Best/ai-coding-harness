---
name: harness-readiness-dashboard
description: MUST use before non-trivial review, merge, release, handoff, PR readiness, or completion claims when Codex needs to summarize Harness gate status, source documents, delegation and reviewer independence, evidence level, patch-churn risk, ADR/Lesson triggers, remaining blockers, ready 检查, 收尾前状态, 是否可以交付, 是否可以 review, 是否可以 handoff, 反复补丁, or 归零审视 without creating new artifacts.
---

# Harness Readiness Dashboard

## Purpose

Use this skill to answer one question:

```text
Can this work safely move to review, release, handoff, or completion?
```

This is a status aggregation skill. It does not replace Start Gate, Vision Gate, Evidence, review, or knowledge capture, and it does not create official Feature, ADR, Lesson, or Evidence artifacts.

## Inputs

Gather only the smallest relevant set:

- Original request, Feature, spec, plan, or acceptance criteria.
- Latest Start Gate, Knowledge Retrieval, Vision Gate, review, and verification outputs if available.
- Evidence location or final verification commands.
- Changed files, PR body, commit messages, or handoff note when present.
- ADR, Lesson, Backlog, or Feature status only when the current task may affect them.

If a source is missing, mark it as `missing`; do not invent status from memory.

## Status Rules

Use these status values:

| Status | Meaning |
| --- | --- |
| `pass` | Required for this task and satisfied. |
| `missing` | Required for this task but not found. |
| `stale` | Found, but likely no longer matches the current diff, intent, or HEAD. |
| `not needed` | Not required for this task class or risk level. |
| `pending` | Required, but not completed yet. |
| `blocked` | Required context, evidence, decision, or reviewer is unavailable. |

Do not upgrade `missing` to `pass` because the change looks simple. Downgrade the task class instead only when the work is truly tiny or routine.

## Readiness Checks

Evaluate these rows:

| Row | Check |
| --- | --- |
| Task class | `tiny`, `routine`, `non-trivial`, or `high-risk`. |
| Source docs | Whether the original intent is anchored in a request, Feature, spec, plan, or acceptance criteria. |
| Start Gate | Required for non-trivial or high-risk work before implementation. |
| Knowledge Retrieval | Required when prior decisions, Feature state, ADRs, Lessons, stale docs, or Evidence may affect the work. |
| Vision Gate Entry | Required when implementation may drift from the original goal before coding. |
| Vision Gate Exit | Required before review, merge, release, handoff, or completion when deliverable-goal drift is plausible. |
| Delegation Gate | Required for non-trivial or high-risk work when implementation subagents or independent review may reduce risk, latency, or tunnel vision. |
| Reviewer policy | `self allowed`, `independent recommended`, or `independent required`. |
| Evidence level | `quick`, `standard`, or `exhaustive`; see `harness-knowledge-capture`. |
| Evidence status | Whether proof is recorded and fresh enough for the current outcome. |
| ADR | `present`, `needed`, or `not triggered`. |
| Lesson | `present`, `needed`, or `not triggered`. |
| Patch Churn | Whether `## Patch History` has 3+ rows, repeated fixes, `Fxxx.n` follow-ups, rule growth, or recurring manual-validation failures require zero-base review before readiness. |
| Knowledge Capture | Whether completion-time memory and Evidence status have been checked. |
| Release/Handoff readiness | Whether unresolved blockers remain before the requested transition. |

For `non-trivial` or `high-risk` work, mark `Delegation Gate` as `missing` when no explicit Delegation Gate decision is available.

Do not convert missing Delegation Gate evidence into self-review just because implementation is already finished. If delegation or independent review would have reduced risk but authorization was unavailable, mark readiness as `conditional` or `blocked` and name the residual risk.

## Reviewer Policy

Use the lightest honest policy:

| Task/risk | Policy |
| --- | --- |
| Tiny or routine, low-risk | `self allowed`. |
| Non-trivial feature, refactor, user-facing change, or unclear scope | `independent recommended`. |
| High-risk architecture, data model, security, migration, release, major UX, or external contract | `independent required` unless unavailable. |

If an independent reviewer is required but unavailable, mark readiness as `blocked` or `conditional` and name the risk.

Use `harness-delegation-gate` in `review` mode when the dashboard would otherwise report `independent recommended` or `independent required` without an explicit decision to ask, self-review, block, or proceed conditionally.

## Output Format

```text
Harness Readiness Dashboard

Task class: tiny | routine | non-trivial | high-risk
Current stage: implementation | review | release | handoff | completion

Source docs: pass | missing | stale | not needed
Start Gate: pass | missing | stale | not needed
Knowledge Retrieval: pass | missing | stale | not needed
Vision Gate Entry: pass | missing | stale | not needed
Vision Gate Exit: pass | missing | stale | not needed
Delegation Gate: pass | missing | not needed | blocked | conditional
Reviewer Policy: self allowed | independent recommended | independent required
Reviewer Status: pass | missing | not needed | blocked
Evidence Level: quick | standard | exhaustive
Evidence Status: pass | missing | stale | pending
Knowledge Capture: pass | pending | not needed
ADR: present | needed | not triggered
Lesson: present | needed | not triggered
Patch Churn: not triggered | low | medium | high
Patch Churn Action: none | Vision Gate | Incident Learning | ADR | Lesson | blocked
Release/Handoff Readiness: pass | blocked | not needed

Ready: yes | no | conditional
Blockers:
- ...
Next action:
- ...
```

Use `conditional` only when the work can proceed with explicitly named residual risk, such as "review can start, but release is blocked until Evidence is recorded."

If a Feature has 3+ `## Patch History` rows or equivalent patch churn and no `## Patch Churn Review` is available, readiness must be `conditional` or `no`, not `yes`.

## Boundaries

- Do not create new documents from this skill; route to `harness-knowledge-capture`.
- Do not re-run Vision Gate here; report whether it exists and whether it is needed.
- Do not treat passing tests as product alignment; that belongs to Vision Gate.
- Do not treat a dashboard as Evidence; it only points to Evidence.
