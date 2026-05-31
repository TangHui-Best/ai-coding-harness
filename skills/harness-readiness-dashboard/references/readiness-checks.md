# Readiness Checks

Use this reference when the compact readiness dashboard is not enough.

## Rows

Evaluate these rows:

| Row | Check |
| --- | --- |
| Task class | `tiny`, `routine`, `non-trivial`, or `high-risk`. |
| Source docs | Whether original intent is anchored in a request, Feature, spec, plan, or acceptance criteria. |
| Start Gate | Required for non-trivial or high-risk work before implementation. |
| Knowledge Retrieval | Required when prior decisions, Feature state, ADRs, Lessons, stale docs, or Evidence may affect work. |
| Bugfix Attribution | Required for non-tiny bugfixes to show whether the bug belongs to an existing Feature, no Feature was found, or ownership remains ambiguous. |
| Vision Gate Entry | Required when implementation may drift from original goal before coding. |
| Vision Gate Exit | Required before review, merge, release, handoff, or completion when deliverable-goal drift is plausible. |
| Delegation Gate | Required for non-trivial or high-risk work when subagents or independent review may reduce risk, latency, or tunnel vision. |
| Reviewer policy | `single_agent`, `delegate`, or `blocked`. |
| Evidence level | `quick`, `standard`, or `exhaustive`. |
| Evidence status | Whether proof is recorded and fresh enough. |
| ADR | `present`, `needed`, or `not triggered`. |
| Lesson | `present`, `needed`, or `not triggered`. |
| Patch Churn | Whether repeated fixes require zero-base review before readiness. |
| Knowledge Capture | Whether completion-time memory and Evidence status have been checked. |
| Release/Handoff readiness | Whether unresolved blockers remain before transition. |

## Reviewer Policy

| Task/risk | Policy |
| --- | --- |
| Tiny or routine, low-risk | `single_agent`. |
| Non-trivial feature, refactor, user-facing change, or unclear scope | Usually `delegate`; use `single_agent` only with a concrete reason. |
| High-risk architecture, data model, security, migration, release, major UX, or external contract | `delegate`; use `blocked` if unavailable. |

If an independent reviewer is needed but unavailable, mark readiness as `blocked` or `conditional` and name the risk.

Use `harness-delegation-gate` in `review` mode when the dashboard would otherwise need independent review without an explicit decision.

## Full Output

```text
Harness Readiness Dashboard

Task class: tiny | routine | non-trivial | high-risk
Current stage: implementation | review | release | handoff | completion

Source docs: pass | missing | stale | not needed
Start Gate: pass | missing | stale | not needed
Knowledge Retrieval: pass | missing | stale | not needed
Bugfix Attribution: pass | missing | ambiguous | not needed
Vision Gate Entry: pass | missing | stale | not needed
Vision Gate Exit: pass | missing | stale | not needed
Delegation Gate: single_agent | delegate | missing | blocked
Reviewer Policy: single_agent | delegate | blocked
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
