---
id: ADR-004
doc_kind: adr
status: accepted
scope: project
feature_refs: []
decision_area: harness-knowledge-model
created: 2026-05-24
updated: 2026-05-24
---

# ADR-004: Feature Identity And Refs Protocol

## Context

`F001`, `F002`, and similar Feature IDs are useful because they show the mainline delivery sequence. In multi-branch or multi-contributor work, using those IDs at creation time creates coordination conflicts: two branches may claim the same next number, and branch-local creation order is not the same as mainline knowledge order.

The old relationship fields (`feature_ids` and `source_feature_ids`) also tied relationship validation to canonical IDs only. That made draft Features hard to reference before they received a mainline number.

## Decision

Use a two-stage Feature identity model.

New branch-local Features use draft IDs in the form `FP-YYYY-MM-DD-slug`. When accepted into mainline knowledge, they receive a canonical `FNNN` ID and keep the draft ID in `aliases`.

Use `feature_refs` as the machine-readable relationship field for ADR, Lesson, and Evidence artifacts. A `feature_refs` entry may reference either a Feature `id` or one of its `aliases`; validation normalizes aliases to the canonical Feature when possible.

Markdown links remain human navigation only. They are not the source of truth for Feature relationships.

## Alternatives

- Allocate `FNNN` when a branch starts: rejected because it turns Feature creation into a shared lock and still cannot express mainline order under concurrent development.
- Replace `FNNN` with UUIDs: rejected because it removes the readable mainline sequence that makes Harness iteration history understandable.
- Keep Markdown links as the relationship source: rejected because agents and scripts would need to open and interpret every linked page, and path renames would break relationship meaning.
- Keep `feature_ids` and add draft-only exceptions: rejected because it preserves the wrong mental model that relationships only target canonical IDs.

## Consequences

Feature IDs now have clearer semantics:

- `FP-YYYY-MM-DD-slug` means branch-local or draft Feature identity.
- `FNNN` means accepted mainline Feature sequence.
- `aliases` preserve identity continuity after canonicalization.
- `feature_refs` is the relationship source for tools and agents.

The trade-off is stricter validation. `knowledge_check.py` must validate Feature ID formats, alias uniqueness, `feature_refs` resolution, canonical Feature filenames, draft Feature filenames, and draft-path Markdown links.

## Evidence

- `docs/evidence/EV-002-feature-identity-and-refs-protocol.md`
- `scripts/knowledge_check.py`
- `templates/FEATURE.md`
- `templates/ADR.md`
- `templates/LESSON.md`
- `templates/EVIDENCE.md`
- `tests/test_knowledge_check.py`
