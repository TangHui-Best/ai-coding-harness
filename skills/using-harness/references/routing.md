# Harness Routing Reference

Use this reference only when `using-harness/SKILL.md` is not enough to choose the next Harness skill.

## Start Gate

Use `harness-start-gate` before non-trivial implementation starts.

Examples:

- Development kickoff, task intake, or pre-coding readiness checks.
- Deciding whether implementation may start now.
- Deciding whether clarification, retrieval, Vision Gate, Feature, spec, plan, ADR, Backlog, or handoff anchor is required first.
- Preventing direct coding when task boundaries, acceptance criteria, or durable pre-work memory are missing.

For non-trivial or high-risk implementation work, Start Gate must produce an explicit Delegation Gate decision before implementation may begin.

## Delegation Gate

Use `harness-delegation-gate` when implementation subagents, parallel work, or independent review may be useful.

- Before coding non-trivial or high-risk work that has separable workstreams, cross-module scope, parallel exploration, or tunnel-vision risk.
- If the user describes a long-running or unattended task, route to Delegation Gate early.
- Before review, merge, release, handoff, acceptance, or completion when independent code review or independent Vision Gate review may reduce risk.

## Knowledge Retrieval

Use `harness-knowledge-retrieval` when the task needs existing project context before acting.

- Starting or resuming non-trivial work.
- Recovering context or finding prior decisions.
- Checking ADRs, Lessons, Features, specs, plans, or Evidence.
- Before non-tiny bugfixes where the bug may be a regression, accepted-Feature follow-up, repeated validation miss, or prior fix-chain symptom.

## Document Lifecycle

Use `harness-doc-lifecycle` when document validity, archive state, supersession, or replacement links are in question.

Examples: archived docs, stale docs, superseded ADRs, completed plans, invalidated research, old specs, and active docs directory cleanup.

## Incident Learning

Use `harness-incident-learning` after a bug, incident, outage, regression, recurring failure, repeated patch chain, or Harness process miss is fixed or stabilized.

It decides whether root cause, trigger, recurrence risk, prevention, Lesson, ADR, CI, tests, gates, or project rules are needed.

## Vision Gate

Use `harness-vision-gate` when original intent, acceptance criteria, scope, user pain point, product direction, or deliverable fit may drift.

Run before implementation for scope-sensitive work and before review, merge, done, acceptance, release, or handoff when alignment may have changed.

## Readiness Dashboard

Use `harness-readiness-dashboard` when a concise status rollup is needed before review, merge, release, handoff, PR readiness, or completion.

It summarizes gate status, source documents, reviewer independence, Evidence level, ADR/Lesson triggers, remaining blockers, and completion risk.

## Change Narrative

Use `harness-change-narrative` when the requested output needs the compact story of a specific engineering change.

Examples: commit message, PR description, merge note, release note, progress summary, handoff note, root cause, rejected paths, verification context, historical intent, workaround, fallback, shim decision, or future caution.

## Knowledge Capture

Use `harness-knowledge-capture` last for durable Harness memory and completion gating.

It owns Evidence, Feature/Backlog consistency, ADR/Lesson decisions, closeout verdict, and completion-claim permission.

## Project Rules

Use `harness-project-rules` only when deciding whether a source-backed behavior constraint belongs in `AGENTS.md` or another project-level agent rule file.
