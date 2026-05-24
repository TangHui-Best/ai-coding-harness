---
name: harness-doc-lifecycle
description: "MUST use when governing Harness document lifecycle: archive docs, stale docs, superseded docs, deprecated docs, invalidates, updates, superseded_by, old ADRs, old plans, old specs, old research, resolved discussions, fixed bug reports, completed Features, oversized active docs directories, 文档归档, 过期文档, 旧文档, 被替代, 废弃, or 生命周期."
---

# Harness Doc Lifecycle

## Purpose

Use this skill to decide whether Harness documents should stay visible in active knowledge paths, move toward archive, or be linked as replaced or updated.

Core rule:

```text
Retrieval is not governance.
```

A search hit must be interpreted through document kind, status, ownership, and replacement links before it can be trusted.

This skill governs lifecycle metadata and placement only. If the lifecycle change also changes durable project knowledge, route to `harness-knowledge-capture`.

## When To Use

Use for:

- Cleaning active docs, archive docs, or an active directory that is too large.
- Old ADR, plan, spec, research, discussion, bug report, or Feature documents whose current validity is unclear.
- Stale, superseded, deprecated, completed, or archived Harness documents.
- Choosing between `invalidates`, `updates`, and `superseded_by`.

Do not use for:

- Writing all knowledge capture from scratch. Use `harness-knowledge-capture`.
- Deciding product or architecture truth without reading the related current Feature, ADR, Evidence, or Lesson.
- Deleting old documents. Archive is not delete.

## Lifecycle States

Use states according to document kind. Do not force every state onto every document.

| State | Meaning | Typical document kinds |
| --- | --- | --- |
| `draft` | Work in progress, not yet reliable as a decision source. | spec, plan, research, discussion |
| `review` | Ready for human or agent review, not accepted yet. | spec, plan, ADR |
| `accepted` | Approved decision or direction. | ADR, spec |
| `active` | Current reusable knowledge or current working document. | Feature, Lesson, active spec, current plan |
| `completed` | Work finished; useful historically, not an active task. | plan, bug report, research |
| `superseded` | Fully replaced by another document. | ADR, spec, plan, research |
| `deprecated` | Historically useful but should not guide new work. | ADR, Lesson, API note, process note |
| `archived` | Removed from active directories for history and audit. | completed, superseded, deprecated, or resolved docs |

Keep Feature status on the Feature aggregate page. Do not copy Feature state into every spec, plan, or discussion; otherwise one Feature change creates many stale edits.

## Archive Triggers

Move a document out of active paths when its operational purpose is finished and it is no longer the best entry point:

- Bug fixed.
- Discussion resolved or converged.
- Plan executed.
- Research conclusion landed.
- Feature completed.

Archive into a dated archive path such as:

```text
docs/archive/2026-05/
```

Set `status: archived` only when the document is no longer meant to appear in active browsing. If it was replaced, set `status: superseded` first and preserve replacement links before or during archival.

## Supersession Rules

Do not treat "new" as correct or "old" as wrong automatically. Decide the relationship.

For full replacement, the new document points backward with `invalidates`, and the old document points forward with `superseded_by`:

```yaml
# New document
invalidates:
  - ADR-003
```

```yaml
# Old document
status: superseded
superseded_by: ADR-012
```

For partial replacement, use `updates` and specify the affected section and reason:

```yaml
updates:
  - doc: ADR-003
    section: Session Strategy
    reason: Updates session handoff strategy only; storage isolation remains valid.
```

Use `deprecated` when a document should no longer guide new work but has not been fully replaced by a specific successor.

## Retrieval Safety

When search finds old or stale docs:

1. Read frontmatter before relying on body content.
2. Check `status`, `updated`, `superseded_by`, `invalidates`, `updates`, `references`, `feature_refs`, and `doc_kind`.
3. If `superseded_by` exists, read the successor first.
4. If `updates` exists, preserve the unaffected parts of the older document.
5. If status is missing or ambiguous, classify the document before using it as evidence.

Search can recall related content; it cannot decide which document is the current source of truth.

## Routing

Route to `harness-knowledge-capture` when a lifecycle change affects any durable knowledge entry:

- Feature status or Feature aggregation.
- ADR acceptance, invalidation, or replacement.
- Lesson creation, retirement, or applicability.
- Evidence index, proof of verification, or bug-fix record.
- Backlog item creation, completion, or cancellation.

Use this skill to choose lifecycle state and links; use capture to record substantive project memory.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Archiving by age alone. | Archive because purpose is complete, replaced, deprecated, or no longer active. |
| Moving a replaced doc without links. | Add `invalidates` on the successor and `superseded_by` on the old document. |
| Treating a discussion as a decision. | Promote or link the accepted outcome; mark the discussion completed or archived. |
| Letting active directories grow indefinitely. | Archive completed plans, resolved discussions, landed research, fixed bug reports, and completed Feature support docs. |
| Using search rank as truth. | Follow lifecycle metadata and replacement links before relying on content. |
