---
name: harness-incident-learning
description: MUST use after a bug, incident, outage, regression, repeated process miss, recurring failure, repeated patch chain, patch churn, Fxxx.n follow-up sequence, or rule/keyword/filter growth has been fixed, stabilized, or grown enough to need root cause analysis, trigger analysis, recurrence-risk assessment, zero-base review, prevention, tests, gates, Lessons, ADRs, CI, scripts, permissions, durable Evidence, 事故复盘, bug 修完, 缺陷修复后, 反复补丁, 规则越补越多, 归零审视, 避免复发, 根因, or 以后别再出现.
---

# Harness Incident Learning

## Purpose

Use this as the post-fix learning gate for bugs, incidents, outages, regressions, and repeated failures.

A code fix stops the current bleeding; incident learning decides whether the system needs stronger immunity.

This skill does not create official Lesson, ADR, Evidence, Feature, or Backlog artifacts. It decides whether they are needed and routes to the owning skill.

## When To Use

Use after the current failure is fixed or stable enough to analyze, before closing, merging, handing off, or declaring the issue complete.

Use for:

- Bug, incident, outage, regression, or recurring failure follow-up.
- Repeated patch churn: multiple follow-up fixes on the same Feature, `Fxxx.n` patch slices recorded in `## Patch History`, manual validation repeatedly exposing related failures, or growing rule/keyword/filter branches without convergence.
- Harness process misses, such as skipped closeout, missing Evidence level, missing `knowledge_check.py` after artifact edits, skipped Start/Vision/Readiness Gate, or completion language used while closeout was incomplete.
- Requests about root cause, trigger, recurrence risk, or preventing recurrence.
- Decisions about adding tests, gates, skills, Lessons, ADRs, CI constraints, scripts, permissions, docs, or Evidence.

Do not use as:

- Active debugging before the failure is understood.
- Test-driven development for the fix itself.
- A change-summary workflow. Use `harness-change-narrative`.
- A formal artifact writer. Use `harness-knowledge-capture`.
- A ceremony for a one-off, low-risk typo with no transferable failure mode.

## Incident Learning Loop

1. Define the incident boundary: symptom, impact, trigger context, affected scope, current fix, and what evidence proves recovery.
2. Separate root cause from trigger: root cause explains why the defect was possible; trigger explains when it became visible.
3. Ask whether the same class of failure can recur in this project or another project.
4. Decide whether the current code fix is sufficient. If the answer depends on people remembering caution, it is not sufficient.
5. Choose the smallest protection mechanism that would have caught or prevented the failure.
6. Route durable knowledge only when useful: narrative to `harness-change-narrative`; Lesson, ADR, Evidence, Feature, or Backlog records to `harness-knowledge-capture`.

For repeated patch chains, inspect the trajectory before accepting another patch:

1. Read the original Feature page and its `## Patch History`; list the last 3+ fixes, or all known fixes if fewer, and the validation symptom each addressed.
2. Group symptoms by suspected shared root cause.
3. Identify whether fixes moved upstream toward the invariant boundary or downstream into presentation, filtering, keyword, fallback, or cleanup patches.
4. Ask whether the current abstraction can explain all observed failures.
5. If the answer is no, route to `harness-vision-gate` and consider ADR or Lesson before more implementation.

If `## Patch History` reaches 3 rows, route to `harness-knowledge-capture` to ensure a non-empty `## Patch Churn Review` is recorded before the next patch is closed.

For Harness process misses, also identify:

- Which required gate was skipped or downgraded.
- Whether the skipped gate was missing from the skill text, ignored by the agent, or unavailable as a deterministic check.
- Whether a script, CI check, project rule, or tighter final response contract would prevent recurrence.
- Whether the current task needs a Lesson before project-level rule promotion.

## Recurrence Decision

Treat recurrence risk as real when any answer is "yes":

- Did the failure expose a missing invariant, test, gate, permission boundary, CI check, or documented rule?
- Could another agent repeat the same path in a fresh session?
- Did a tool fail, return stale data, or get skipped without blocking progress?
- Did a Harness artifact exist while Exit Gate status, Evidence level, or check result was still missing?
- Did the final response use completion/readiness wording without the closeout categories required by `harness-knowledge-capture`?
- Is the fix local while the cause is process-level, architecture-level, or cross-module?
- Are rules, keywords, filters, fallbacks, or scenario-specific branches growing without convergence?
- Did tests pass while manual validation kept finding the same class of failure?
- Is the current patch local while the likely cause is an abstraction, invariant, or boundary problem?
- Would the only remaining advice be "be careful next time"?

If recurrence risk is low, record concise Evidence and close. If recurrence risk is medium or high, add a protection or route to capture a durable follow-up.

## Protection Options

| Protection | Use when | Good output |
| --- | --- | --- |
| Test | Behavior can be reproduced automatically. | Regression/unit/integration test that fails before the fix and passes after. |
| Gate | Work must not proceed without a condition. | Review, merge, done, or evidence gate with a concrete blocking rule. |
| Skill | Future agents need procedural judgment. | Cross-project skill trigger and concise workflow. |
| Lesson | A transferable failure mode needs a guardrail. | Lesson proposal with root cause, trigger, protection, and source anchor. |
| ADR | The fix makes or revises a durable decision. | Decision narrative with rejected alternatives and tradeoffs. |
| CI | Automation should block regressions. | Build, lint, test, schema, policy, or knowledge check in CI. |
| Script/check | Manual inspection is unreliable or repeated. | Deterministic command with clear pass/fail output. |
| Permission/sandbox | The incident involved unsafe access or missing authority boundaries. | Narrower permissions, approval point, or sandbox rule. |
| Docs/index | The issue came from missing, stale, or undiscoverable knowledge. | Updated source doc plus rebuilt/searchable index when the project uses one. |
| Evidence | Completion must be auditable. | Outcome, command output, environment/context, and trace or trajectory. |

## Evidence Requirements

Evidence must include enough detail to prove both result and path:

- Final outcome: what is fixed or recovered.
- Commands and output: tests, build, lint, validation, packaging, screenshots, or traces as appropriate.
- Environment/context: branch, paths, relevant config, tool failures, stale docs, or permission state.
- Trajectory: important failed attempts, skipped options, and why the selected protection is sufficient.
- For patch churn: the fix sequence, the symptoms each fix addressed, why another local patch is or is not sufficient, and whether the final protection moved upstream to the right invariant or boundary.

Scale Evidence to risk. Low-risk documentation work can report Evidence in the final response. Medium/high-risk incidents should route to `harness-knowledge-capture` for a durable Evidence record.

## Routing

Use `harness-change-narrative` when the root cause, trigger, fix rationale, rejected approaches, or PR/commit/handoff summary needs to be explained.

Use `harness-knowledge-capture` when the learning should become a Lesson, ADR, Evidence, Feature link, Backlog item, or another durable Harness artifact.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Stopping at "bug fixed." | Ask what would stop the same class of failure next time. |
| Writing "be careful." | Convert caution into a test, gate, skill, CI check, permission rule, or Lesson. |
| Calling every bug a Lesson. | Create durable memory only when recurrence or future confusion is plausible. |
| Treating trigger as root cause. | Record both: trigger is when it surfaced; root cause is why it was possible. |
| Creating artifacts directly. | Decide and route to `harness-knowledge-capture`. |
