---
name: harness-knowledge-retrieval
description: MUST use when starting or resuming non-trivial work that may depend on project context, prior decisions, ADRs, Lessons, Features, specs, plans, Evidence, stale documents, rejected approaches, recovery context, 恢复上下文, 查历史决策, 查 ADR, 查 Lesson, 查 Feature, 查知识库, or 避免重复踩坑 before acting.
---

# Harness Knowledge Retrieval

## Purpose

Retrieve durable project knowledge before acting. Use this skill to rebuild context from structured project memory: Feature pages, ADRs, Lessons, specs, plans, Evidence, research, discussions, bug reports, and archive records.

Retrieval reads and judges existing knowledge. It does not build indexes, invent a knowledge service, or write durable memory. Route missing or stale durable memory to `harness-knowledge-capture`.

## When To Use

Use this before meaningful work when any of these apply:

- Starting or resuming non-trivial work.
- Recovering context after a handoff, compacted conversation, or interrupted session.
- Finding prior decisions, constraints, rejected approaches, incidents, or validation Evidence.
- Attributing a non-tiny bug, regression, accepted-behavior breakage, or validation failure to an existing Feature or prior fix chain before implementation.
- Searching ADR, Lesson, Feature, spec, plan, discussion, research, bug report, archive, or Evidence records.
- Avoiding repeated mistakes by checking historical failure modes first.

## When Not To Use

- Tiny local edits where existing project memory cannot change the outcome.
- Creating or updating ADRs, Lessons, Feature pages, Evidence, or handoff notes. Use `harness-knowledge-capture`.
- Designing a search index or CLI implementation. This skill tells the agent how to consume retrieval, not how to build it.

## Retrieval Order

1. Start with the repository's documented knowledge search if available, such as `knowledge search "<query>"`, `knowledge feature <id>`, or `knowledge open <doc-id>`.
2. If no knowledge search exists, use filesystem search against likely docs paths: `docs/ACTIVE.md`, `docs/BACKLOG.md`, `docs/features/`, `docs/specs/`, `docs/plans/`, `docs/discussions/`, `docs/research/`, `docs/decisions/`, `docs/bug-reports/`, `docs/lessons/`, `docs/evidence/`, and `docs/archive/`.
3. Read the Feature page first when a Feature ID or feature topic is found. Treat it as the delivery boundary and navigation entry, not as the owner of every related record.
4. Open linked or relevant ADR, Lesson, spec, plan, Evidence, research, discussion, bug report, PR, commit, and archive records as needed.
5. If a result is `stale`, `superseded`, `deprecated`, `invalidated`, or points to `superseded_by`, continue to the replacement or current document before relying on it.
6. Summarize what was read: paths, document kinds, status, feature IDs, current decisions, stale items, and open questions.

## Bug Retrieval Mode

Use this mode when Start Gate needs Feature attribution for a bugfix.

Search with the smallest useful set of terms:

- User symptom, expected behavior, error text, failing command, UI/workflow name, or validation message.
- Module, file, API, CLI command, screen, data model, or integration named by the report.
- Known Feature IDs, patch IDs such as `F010.2`, ADR IDs, Lesson IDs, and related PR or commit identifiers.
- Synonyms for the behavior, including `bug`, `regression`, `follow-up`, `validation`, `Patch History`, `Patch Churn Review`, and domain-specific nouns.

Then:

1. If a Feature is found, read it first and inspect `## Patch History`, `## Patch Churn Review`, related links, status, and Evidence.
2. Read linked or relevant Evidence, ADRs, Lessons, bug reports, discussions, and archive pointers before trusting a local code hypothesis.
3. Classify attribution as `existing Feature <id>`, `none found`, `ambiguous`, or `stale/superseded`.
4. If attribution is ambiguous, name the candidate Features and the missing fact needed to choose between them.
5. Return the attribution result to Start Gate or Knowledge Capture. Retrieval itself must not update Patch History.

If no Feature is found, say so explicitly. A negative retrieval result is still useful evidence; it tells later gates whether a new Feature anchor may be needed.

## Trust Rules

Search improves recall; Feature pages, frontmatter, ADRs, Lessons, archive status, and Evidence provide meaning and lifecycle.

Do not trust bare snippets without enough metadata to judge them. A trustworthy result should include, or be followed by opening a document that reveals:

| Field | Why it matters |
| --- | --- |
| `path` | Lets the agent read the source document instead of relying on a snippet. |
| `doc_kind` | Distinguishes ADR, Lesson, Feature, spec, plan, Evidence, draft, or archive material. |
| `status` | Shows whether the record is accepted, draft, active, completed, stale, deprecated, or superseded. |
| `feature_ids` | Connects the record to delivery scope without forcing false ownership. |
| `superseded_by` | Points to the current replacement when the result is old. |

If metadata is missing, open the source file and inspect frontmatter, headings, and links before treating the content as authoritative.

## Fallback Search Patterns

When no retrieval CLI exists:

- Search text for user terms plus synonyms: `ADR`, `Lesson`, `Feature`, `Evidence`, `decision`, `superseded`, `deprecated`, `stale`, `invalidates`, `updates`.
- For bugs, search symptoms and implementation nouns together with `bug`, `regression`, `follow-up`, `Patch History`, `Patch Churn Review`, `Evidence`, and likely Feature IDs.
- Search filenames for likely IDs: `F001`, `ADR-001`, feature slugs, incident names, plan/spec titles.
- Prefer structured docs over loose transcript snippets.
- If only loose snippets exist, mark confidence as low and state the limitation.
- Follow links and frontmatter relations such as `feature_ids`, `related`, `invalidates`, `updates`, and `superseded_by`.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Reading only the first search snippet. | Open the source path and inspect metadata/status. |
| Treating search rank as authority. | Authority comes from document kind, status, lifecycle, and links. |
| Stopping at a stale ADR or old plan. | Follow `superseded_by`, `updates`, or archive pointers to the current record. |
| Assuming Feature owns every record. | Feature expresses delivery boundary; ADR expresses decision boundary; Lesson expresses failure-mode boundary. |
| Debugging a non-tiny bug before attribution. | First establish whether it belongs to an existing Feature or prior fix chain, then debug with that context. |
| Writing new memory during retrieval. | Finish retrieval, then invoke `harness-knowledge-capture` for missing, stale, or newly discovered durable memory needs. |
