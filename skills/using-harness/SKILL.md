---
name: using-harness
description: Use when working in an AI-assisted engineering workflow that may need project memory, retrieval, gates, evidence, incident learning, change narrative, document lifecycle, handoff, ADRs, Lessons, Features, or durable completion records.
---

# Using Harness

## Purpose

Use this as the entrypoint for an AI coding harness. It routes engineering work toward the right harness skill so knowledge can survive across sessions, agents, reviewers, and teammates.

This skill does not create artifacts directly. It decides which harness skill should run, or whether no formal harness action is needed.

## Core Rule

If future sessions, agents, reviewers, teammates, or future you may need to understand what happened, why it happened, what was verified, or what should not be repeated, check the harness flow before closing the task.

Harness is not a documentation tax. The required behavior is checking whether shared project memory is needed; the correct result may be "no formal artifact needed."

## Routing

Use `harness-knowledge-retrieval` when the task needs existing project context before acting:

- Starting or resuming non-trivial work.
- Recovering context after a handoff or compacted conversation.
- Finding prior decisions, ADRs, Lessons, Features, specs, plans, or Evidence.
- Avoiding repeated mistakes by checking past incidents or rejected approaches.

Use `harness-doc-lifecycle` when document validity, archive state, supersession, or replacement links are in question:

- Cleaning active docs or archive docs.
- Handling stale, superseded, deprecated, invalidated, completed, or replaced documents.
- Deciding between `invalidates`, `updates`, and `superseded_by`.

Use `harness-incident-learning` after a bug, incident, outage, regression, or recurring failure is fixed or stabilized:

- Root cause and trigger analysis.
- Recurrence risk.
- Prevention through tests, gates, scripts, CI, permissions, ADRs, Lessons, or workflow changes.

Use `harness-vision-gate` before review, merge, done, acceptance, release, or handoff when original intent or user-goal alignment may have drifted:

- Product direction.
- UX or visual quality.
- User pain point.
- Acceptance criteria drift.
- Deliverable-goal fit.

Use `harness-change-narrative` when a compact explanation of a specific engineering change is needed:

- Commit messages.
- PR descriptions.
- Release notes.
- Progress summaries.
- Handoff notes.
- Root cause, rejected approaches, verification context, historical intent, workaround decisions, or future caution.

Use `harness-knowledge-capture` when the task may need durable project memory or completion gating:

- Before claiming work is complete, verified, reviewed, ready to commit, ready for PR, ready for handoff, or safely closed.
- Feature state changes.
- Evidence records.
- ADRs.
- Lessons.
- Backlog or handoff state.

## Routing Order

When multiple skills apply, prefer this order:

1. `harness-knowledge-retrieval` to read existing context.
2. `harness-doc-lifecycle` when document validity or replacement state matters.
3. `harness-incident-learning` when a bug or recurring failure was fixed or stabilized.
4. `harness-vision-gate` before acceptance or handoff when goal alignment may have drifted.
5. `harness-change-narrative` when a specific change needs a compact story.
6. `harness-knowledge-capture` last to decide durable artifacts, links, validation, Evidence, and final knowledge status.

For a simple commit, PR, or handoff with no incident, lifecycle, or vision-gate ambiguity, go directly to `harness-change-narrative`, then use `harness-knowledge-capture` only if durable project memory may be needed.

## Red Flags

| Thought | Reality |
| --- | --- |
| "This is done; I can just say completed." | Completion needs Evidence status, even if it stays in the final response. |
| "The next agent can infer intent from the diff." | Diffs show what changed, not why alternatives were rejected. |
| "This workaround is obvious." | Workarounds are exactly where future agents need context. |
| "We can write the ADR or Lesson later." | Later often means after the rationale is gone. |
| "This is just a PR description." | PR descriptions are one of the main change narrative surfaces. |
| "No formal artifact is needed, so no harness skill is needed." | The harness may conclude no artifact is needed; the check is still the gate. |

## Non-Goals

- Do not require a project-level `AGENTS.md` change to use Harness.
- Do not create Feature, ADR, Lesson, Evidence, or Backlog artifacts from this skill.
- Do not create documents for every small change.
- Use the smallest durable carrier that prevents repeated rediscovery, unverifiable completion, or repeated mistakes.
