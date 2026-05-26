---
name: harness-knowledge-retrieval
description: MUST use when starting or resuming non-trivial work that may depend on project context, prior decisions, ADRs, Lessons, Features, specs, plans, Evidence, stale documents, rejected approaches, recovery context, 恢复上下文, 查历史决策, 查 ADR, 查 Lesson, 查 Feature, 查知识库, or 避免重复踩坑 before acting.
---

# Harness Knowledge Retrieval

## Purpose

Retrieve durable project knowledge before acting. Use this skill to rebuild context from structured project memory: Feature pages, ADRs, Lessons, specs, plans, Evidence, research, discussions, bug reports, and archive records.

Retrieval reads and judges existing knowledge. It does not build indexes, invent a knowledge service, or write durable memory. Route missing or stale durable memory to `harness-knowledge-capture`.

## When To Use

- Starting or resuming non-trivial work.
- Recovering context after handoff, compacted conversation, or interrupted session.
- Finding prior decisions, constraints, rejected approaches, incidents, or validation Evidence.
- Attributing a non-tiny bug, regression, accepted-behavior breakage, or validation failure to an existing Feature or prior fix chain before implementation.
- Searching ADR, Lesson, Feature, spec, plan, discussion, research, bug report, archive, or Evidence records.

## When Not To Use

- Tiny local edits where existing project memory cannot change the outcome.
- Creating or updating ADRs, Lessons, Feature pages, Evidence, or handoff notes. Use `harness-knowledge-capture`.
- Designing a search index or CLI implementation.

## Core Retrieval Flow

1. Start with direct `feature_refs` when present. Open path-like refs directly.
2. Prefer filename/path lookup before broad text search when a Feature path, stem, or unambiguous ID exists.
3. Read the Feature page first when found; treat it as the delivery boundary and navigation entry.
4. Open linked ADR, Lesson, spec, plan, Evidence, research, discussion, bug report, PR, commit, and archive records only as needed.
5. Follow `stale`, `superseded`, `deprecated`, `invalidated`, or `superseded_by` pointers before relying on old material.
6. Summarize what was read: paths, document kinds, status, feature IDs, decisions, stale items, confidence, and open questions.

## Bug Retrieval Mode

For bug attribution, classify the result as:

```text
existing Feature <path-or-stem> | none found | ambiguous | stale/superseded
```

If a Feature is found, inspect `## Patch History`, `## Patch Churn Review`, related links, status, and Evidence.

If no Feature is found, say so explicitly. A negative retrieval result is useful evidence.

Retrieval itself must not update Patch History.

## Reference Map

Use references only when their trigger applies.

- `references/retrieval-order.md`: read when search scope, source trust, stale document handling, or fallback search patterns are unclear.
- `references/bug-retrieval-mode.md`: read for non-tiny bugfix attribution, Feature ownership, Patch History, or ambiguous candidates.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Reading only the first search snippet. | Open the source path and inspect metadata/status. |
| Treating search rank as authority. | Authority comes from document kind, status, lifecycle, and links. |
| Stopping at a stale ADR or old plan. | Follow `superseded_by`, `updates`, or archive pointers to the current record. |
| Assuming Feature owns every record. | Feature expresses delivery boundary; ADR expresses decision boundary; Lesson expresses failure-mode boundary. |
| Debugging a non-tiny bug before attribution. | First establish whether it belongs to an existing Feature or prior fix chain, then debug with that context. |
