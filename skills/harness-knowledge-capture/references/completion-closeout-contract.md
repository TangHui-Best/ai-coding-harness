# Completion Closeout Contract

Use this reference when the compact closeout block is not enough, when a category is blocked or conditional, or when review/release/handoff readiness matters.

## Completion Closeout Gate

Run this gate before claiming a Feature, non-trivial change, review, release, handoff, or completion is ready.

| Check | Required action |
| --- | --- |
| Entry Gate | Record whether Start Gate was `ready`, `not triggered because ...`, `satisfied by ...`, `retroactive ...`, or `missing`. If it is missing, completion claims are blocked. |
| Vision Anchor | Record the Feature, spec, Evidence, ADR, discussion, or other durable source that lets future agents recover original intent. Use `not triggered because ...` only when project memory cannot change the outcome. |
| Backlog/Handoff | Record whether active state changed or why no handoff state is needed. |
| Plan lifecycle | If linked plans were executed, set them to `completed`, archive them, or explicitly record why they remain `active`. |
| Readiness | For non-trivial review, release, handoff, or readiness claims, use `harness-readiness-dashboard` or record why it was not triggered. |
| Vision Gate Exit | For non-trivial, user-facing, architecture, scope-sensitive, or behavior-changing work, use `harness-vision-gate` in Exit Gate mode or record why it was not triggered. |
| Patch Churn Review | If 3+ Patch History rows or equivalent repeated misses exist, record whether review passed, routed, or blocked. |
| Bugfix attribution | For non-tiny bugfixes, record existing Feature, none found, ambiguous, not triggered, or blocked. |
| Feature and Backlog consistency | Ensure Feature status, Backlog state, Evidence links, ADR/Lesson links, and next step describe the same state. |
| Evidence validation | Record verification commands and results. When Harness artifacts changed, include the `knowledge_check.py` command path and actual result. |
| Completion verdict | Set `Closeout verdict` to `pass`, `conditional`, or `blocked`; set `Completion claim allowed` to `yes` only when no required item is missing. |

## Full Final Response Contract

Use the full block when any category is newly updated, non-trivial, conditional, blocked, or requested by the user:

```text
Closeout verdict: pass / conditional / blocked
Completion claim allowed: yes / no
Entry Gate: ready / not triggered because ... / satisfied by ... / retroactive ... / missing
Vision Anchor: Feature Fxxx / spec ... / ADR ... / Evidence ... / not triggered because ...
Backlog/Handoff: not triggered / updated ...
Plan lifecycle: not triggered / updated ... / intentionally active because ...
Readiness: not triggered / dashboard pass / dashboard conditional ... / blocked ...
Vision Gate Exit: not triggered / pass / needs follow-up / blocked ...
Patch Churn Review: not triggered / pass / routed to Vision Gate / routed to ADR / routed to Lesson / blocked ...
Bugfix attribution: not triggered / existing Feature <id> updated / none found after retrieval / ambiguous ... / blocked ...
ADR: not triggered / written ADR-xxx
Lesson: not triggered / written LL-xxx
Evidence: recorded in ...
Evidence level: quick / standard / exhaustive
Feature: updated ... / not triggered
Check: passed / not run because ... / failed because ...
```

If a trigger was deliberately not satisfied, explain the reason briefly. Do not leave a category blank.

## Verdicts

| Verdict | Meaning | Completion language |
| --- | --- | --- |
| `pass` | Required closeout items are satisfied for the task risk level. | Completion/readiness claims are allowed. |
| `conditional` | Work can move to a named next stage with explicit residual risk. | Use conditional wording only. |
| `blocked` | Required Evidence, gate, decision, artifact validation, or recovery context is missing. | Completion/readiness claims are not allowed. |

`Completion claim allowed: yes` is valid only when:

- `Closeout verdict` is `pass`, or the claim is explicitly limited to the conditional stage.
- `Entry Gate` is present and is not `missing`.
- `Vision Anchor` is present; if it is `not triggered`, it includes a reason explaining why no durable anchor is needed.
- Evidence location and Evidence level are present.
- Required verification commands and outcomes are recorded in Evidence or final response.
- `Check` records the actual `knowledge_check.py` result when Harness artifacts were created or updated.
- Required Readiness and Vision Gate Exit checks are satisfied or explicitly not triggered with a reason.
- Non-tiny bugfixes have Bugfix attribution status.
