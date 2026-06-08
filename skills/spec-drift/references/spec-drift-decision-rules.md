# Spec Drift Decision Rules

Use this reference only when the primary Spec Drift workflow cannot classify the situation quickly.

## Decision Matrix

| Evidence pattern | Likely result | Why |
| --- | --- | --- |
| Code fails an explicit, still-valid requirement. | `implementation bug` | The source is trustworthy; execution is wrong. |
| A real case contradicts an assumption the spec made implicitly. | `spec needs update` | The source omitted or misstated a real boundary. |
| User feedback says the accepted output is technically correct but not useful. | `needs vision gate` or `spec needs update` | First recover original intent; then update the source if needed. |
| Repeated patch rows add scenario-specific branches around the same behavior. | `spec needs update` or `needs ADR` | The patch chain may be preserving a wrong abstraction. |
| The change would alter module ownership, architecture policy, external contracts, data shape, or compatibility stance. | `needs ADR` | The drift is no longer only a spec wording problem. |
| Evidence is anecdotal, incomplete, or conflicts with the original goal. | `blocked` | Clarification beats guessing. |

## Minimal Evidence To Gather

- Current source: Feature, spec, plan, acceptance criteria, ADR, test, or user instruction.
- Contradiction: real case, validation failure, user feedback, review finding, or patch history.
- Original goal: user pain point, non-goal, Vision Anchor, or the best available durable intent source.
- Scope impact: implementation-only, spec wording, product intent, module boundary, or architecture decision.

## Browser SOP To Playwright Example

In an RPA Agent project, a `SkillCompiler` module may translate browser operation SOPs into Playwright scripts. Early work can predict broad interaction types: click, input, select, wait, file upload, iframe, popup, and date controls.

That does not mean the first spec can foresee every vendor widget, timing condition, nested frame, or business exception. The healthy path is:

1. Keep the early spec focused on variation boundaries and invariants.
2. When a new real case fails, decide whether it is an implementation bug or a missing interaction model.
3. If the new case changes the model, update the spec or Feature first.
4. Then implement the smallest change that follows the repaired source.

The unhealthy path is repeatedly adding branches like "if this page has this exact dropdown shape" without revisiting the interaction abstraction. That is patch churn caused by spec drift.

## Escalation Rules

- Use `vision-gate` when original intent is unclear, when acceptance criteria may be a lossy compression, or when the user pain point is missing.
- Use `doc-lifecycle` when the issue is document status: stale, archived, superseded, deprecated, invalidated, or replaced.
- Use `knowledge-capture` after the decision when a Feature/spec/ADR/Evidence update is required.
- Use `project-rules` only after a source-backed rule proves it should become a project-level agent rule.
