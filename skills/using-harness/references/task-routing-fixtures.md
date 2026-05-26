# Task Routing Fixtures

Use this reference when a common workflow route is unclear. These examples are regression fixtures for expected Harness behavior, not a replacement for judgment.

## tiny bugfix

Shape: one local typo, fixture text, comment, or mechanical correction where project memory cannot change the fix.

Expected route:

- `using-harness`: triggered only if Harness is mentioned or repo policy requires it.
- `harness-start-gate`: may return `ready` with `Task class: tiny`.
- `harness-knowledge-retrieval`: not triggered because project memory cannot change the fix.
- Verification: run the smallest relevant test/command.
- Closeout: compact closeout is enough.

## non-tiny bugfix

Shape: regression, validation failure, broken accepted behavior, public workflow bug, cross-module bug, or bug likely owned by an existing Feature.

Expected route:

- `harness-start-gate`: return `needs retrieval` when ownership or prior history is unknown.
- `harness-knowledge-retrieval`: establish Feature attribution before code search or edits.
- `harness-knowledge-capture`: record Evidence and Bugfix attribution; update Patch History when an existing completed Feature owns the behavior.

## commit-only

Shape: user asks to commit already-finished local changes.

Expected route:

- `harness-change-narrative`: use for commit message and compact change rationale.
- `harness-knowledge-capture`: use only if durable memory, Evidence, or completion readiness is still missing.
- Verification: run staged/diff checks relevant to the commit; do not read tests merely to verify.

## PR description

Shape: user asks for PR body or publish-ready summary.

Expected route:

- `harness-change-narrative`: owns PR narrative.
- `harness-readiness-dashboard`: use when readiness or blockers need a concise rollup.
- `harness-knowledge-capture`: use if completion, Evidence, or durable artifact state must be claimed.

## skill edit

Shape: editing Harness or another skill.

Expected route:

- Use `skill-creator` when skill structure, progressive disclosure, scripts, references, or assets are being changed.
- Use focused tests before editing implementation.
- Execute validation scripts; read script source only when debugging or editing scripts.
- Sync installed skills with repository install scripts when the user needs local behavior updated.

## artifact updated

Shape: Feature, ADR, Lesson, Evidence, Backlog, template, or Harness docs changed.

Expected route:

- `harness-knowledge-capture`: record Evidence level and closeout state.
- Run `knowledge_check.py` when Harness knowledge artifacts changed.
- Run `skill_metadata_check.py` when skill metadata or bundled resources changed.

## no artifact needed

Shape: routine or tiny work where durable memory cannot improve recovery, traceability, or future decisions.

Expected route:

- Explicitly say why no artifact is needed.
- Still record Evidence location/level in the final closeout when making completion claims.
- Do not create documents for performative discipline.
