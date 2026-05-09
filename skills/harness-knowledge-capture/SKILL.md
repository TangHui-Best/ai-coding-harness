---
name: harness-knowledge-capture
description: Use before claiming engineering work is complete, verified, reviewed, ready to commit, ready for PR, ready for handoff, or safely closed; use when preserving Evidence, changing Feature state, linking specs or plans, resolving incidents, recording ADRs or Lessons, or deciding whether durable Harness project memory is needed.
---

# Harness Knowledge Capture

## Purpose

Use this skill to turn completed engineering work into durable project memory without creating documentation tax.

Core boundary:

```text
Skill is the knowledge-capture entry point.
Scripts and gates are the reliability layer.
```

This skill does not build the whole Harness. Use it to capture the smallest durable knowledge artifact after work, review, handoff, or incident learning.

Do not write documents just to look disciplined. Capture only the smallest artifact that prevents future confusion, repeated mistakes, or unverifiable completion claims.

Treat Markdown documents as the source of truth. Treat search indexes, summaries, and retrieval databases as compiled outputs.

## Trigger Discipline

If you are about to say work is done, complete, verified, reviewed, ready to commit, ready for PR, ready for handoff, or safely closed, stop and use this skill first.

This skill may conclude "no formal artifact needed." The required behavior is checking Evidence, ADR, Lesson, Feature, Backlog, and Handoff status before completion claims.

## Workflow

1. Read the current task, changed files, verification output, user constraints, `AGENTS.md`, `docs/BACKLOG.md`, active Feature pages, recent commits, and existing ADR/Lesson/Evidence docs when present.
2. Identify the smallest knowledge boundary that matters: active work state, handoff, Feature delivery, decision, failure mode, evidence, or none.
3. Use the Artifact Decision Matrix, then run the trigger checklist below.
4. Create or update only the lightest durable artifact that fits the risk.
5. Link ADR, Lesson, and Evidence artifacts from the Feature page when a Feature is involved.
6. Update `docs/BACKLOG.md` or a handoff note when active work state changes.
7. Run `scripts/knowledge_check.py` against the target docs directory when dedicated Harness artifacts were created or updated.
8. Report Backlog/Handoff, ADR, Lesson, Evidence, Feature, and Check status explicitly.

## Integration

Use this skill as the closeout around other workflow skills:

| Upstream event | Knowledge-capture action |
| --- | --- |
| Brainstorming writes a spec | Link spec from the Feature page; add Feature linkback when ownership is clear. |
| Planning writes a plan | Link plan from the Feature page; update next step and BACKLOG if active work changed. |
| Implementation or verification finishes | Record Evidence in the lightest durable place. |
| Code review or PR preparation starts | Check Feature, ADR, Lesson, Evidence, and handoff status before claiming readiness. |
| Bug, incident, or repeated failure is resolved | Consider Lesson, Evidence, and stronger gates before closing. |
| Architecture or process decision is made | Consider ADR before the rationale is lost. |

Use `harness-change-narrative` as the change-level narrative layer when commit, PR, merge, release, handoff, non-trivial bugfix, rejected-option, or history-aware context needs to be explained first.

## Artifact Decision Matrix

Choose the smallest durable carrier that matches the knowledge boundary:

| Boundary | Preferred carrier | Rule |
| --- | --- | --- |
| Current active work, next step, recovery context | `docs/BACKLOG.md` or handoff note | Update only when future sessions need this state. |
| Delivery boundary, status, acceptance criteria, related links | Feature page | Create or update when the task advances a Feature. |
| Detailed requirement or scope | Spec linked from Feature | Link it; do not copy the spec into the Feature page. |
| Execution route or task breakdown | Plan linked from Feature | Link it; update Feature status and next step if they changed. |
| Decision conversation, issue thread, review thread | Discussion linked from Feature | Link it when it explains current state or open questions. |
| Defect reproduction, impact, expected behavior | Bug report linked from Feature | Link it; create a Lesson only if the failure mode can recur. |
| Exploration before a decision | Research linked from Feature or ADR | Link it; create an ADR only when a decision is made. |
| Why this option, why not alternatives | ADR | Create a dedicated ADR when the decision will be questioned later. |
| Recurring failure mode and protection | Lesson | Create a dedicated Lesson when caution must become a guardrail. |
| Proof of completion | Evidence location or Evidence doc | Record proof every time; create an Evidence doc only when retrieval or audit matters. |

Feature pages are indexes, not containers for all material. Prefer linking spec, plan, discussion, bug report, and research documents over copying their content.

## Trigger Checklist

### Backlog or Handoff

Update `docs/BACKLOG.md` or write a handoff note when the task changes current active work state.

Trigger on:

- A Feature starts, pauses, unblocks, ships, or changes next step.
- Important recovery context would be lost in a new session.
- There are unresolved risks, open decisions, or follow-up commands.
- The work spans multiple sessions, agents, or collaborators.

Do not update BACKLOG for a one-off low-risk task with no future recovery value.

### ADR

Write an ADR when the task makes a decision future agents are likely to question.

Trigger on:

- High-cost rollback technical choices.
- Changes to module boundaries, data models, or interface contracts.
- New frameworks, infrastructure, storage, or messaging mechanisms.
- Rejected alternatives that are likely to be proposed again.
- Decisions affecting multiple Features or long-term evolution.
- Security, performance, cost, compliance, or operational tradeoffs.

Decision sentence:

```text
If a future person or agent is likely to ask "why did we choose this?", write an ADR.
```

### Lesson

Write a Lesson when a failure mode can recur and needs a protection mechanism.

Trigger on:

- Similar issues may recur or have already recurred.
- A bug exposes a process gap, missing rule, or weak gate.
- Future agents are likely to repeat the same error.
- Code changes alone cannot fully prevent recurrence.
- The only post-fix guidance would otherwise be "be careful next time."
- The fix requires tests, gates, CI, permissions, docs, or workflow rules.

Decision sentence:

```text
If the fix ends with "be careful next time", write a Lesson and turn caution into protection.
```

### Evidence

Evidence is required as proof for every completion claim. A dedicated Evidence document is optional.

Scale storage location to risk:

- Low risk: final response, commit message, or manual inspection note.
- Medium risk: Feature page, PR body, tests, build, lint, and key diff summary.
- High risk: dedicated Evidence document, tests, build, E2E or screenshot, trace, reviewer record, and rollback note.

Evidence should include final outcome, command output, environment or diff context, and trace or trajectory when relevant.

### Feature Page

Create or update a Feature page when:

- A Feature status changes.
- A spec, plan, discussion, bug report, research, ADR, Lesson, or Evidence artifact is added.
- Acceptance criteria change.
- New constraints are discovered.
- The task advances a Feature.

Feature pages express delivery boundaries. ADRs express decision boundaries. Lessons express failure-mode boundaries. Evidence expresses proof of completion.

## Artifact Placement

Prefer these paths unless the project already has a stronger convention:

```text
docs/BACKLOG.md
docs/features/Fxxx-slug.md
docs/decisions/ADR-xxx-slug.md
docs/lessons/LL-xxx-slug.md
docs/evidence/EV-xxx-slug.md
```

## Templates

Copy the matching template and fill every required field and section:

- Feature: `templates/FEATURE.md`
- ADR: `templates/ADR.md`
- Lesson: `templates/LESSON.md`
- Evidence: `templates/EVIDENCE.md`

Use stable IDs:

- Feature: `F001`
- ADR: `ADR-001`
- Lesson: `LL-001`
- Evidence: `EV-001`

Keep titles specific enough to scan in search results.

## Check Script

Run:

```bash
python scripts/knowledge_check.py --root <repo> --docs-path docs
```

Optional:

```bash
python scripts/knowledge_check.py --root <repo> --docs-path docs --strict
python scripts/knowledge_check.py --root <repo> --docs-path docs --all-markdown --strict
```

The script checks Harness knowledge artifacts for Markdown frontmatter, allowed `doc_kind`, required fields, required sections, Feature ID/file-name consistency, Feature references, Feature links, and missing Feature backlinks for ADR/Lesson/Evidence documents that declare Feature relationships.

## Final Response Contract

Always include this knowledge-capture status before claiming readiness or completion:

```text
Backlog/Handoff: not triggered / updated ...
ADR: not triggered / written ADR-xxx
Lesson: not triggered / written LL-xxx
Evidence: recorded in ...
Feature: updated ... / not triggered
Check: passed / not run because ... / failed because ...
```

If a trigger was deliberately not satisfied, explain the reason briefly. Do not leave a category blank.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Claiming work is done without Evidence status. | Record where Evidence lives, even if it is only the final response. |
| Creating a new artifact when an existing one should be updated. | Prefer updating current Feature, ADR, Lesson, or Evidence records. |
| Copying spec/plan content into a Feature page. | Link source artifacts and summarize only the status or next step. |
| Writing a Lesson that only says to be careful. | Turn caution into a test, gate, CI check, permission rule, or skill. |
| Writing an ADR without rejected alternatives or tradeoffs. | Include alternatives and consequences. |
| Treating a search index as source of truth. | Markdown source artifacts own truth; indexes are compiled outputs. |
