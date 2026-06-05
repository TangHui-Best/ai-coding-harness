# Retrieval Order

Use this reference when retrieval scope or source trust is unclear.

## Source Order

1. Direct path-like `feature_refs`.
2. Feature filename/stem lookup in `docs/features/`.
3. Structured docs paths:
   - `docs/ACTIVE.md`
   - `docs/BACKLOG.md`
   - `docs/features/`
   - `docs/specs/`
   - `docs/plans/`
   - `docs/discussions/`
   - `docs/research/`
   - `docs/decisions/`
   - `docs/bug-reports/`
   - `docs/lessons/`
   - `docs/evidence/`
   - `docs/archive/`
4. Linked records from the Feature, ADR, Lesson, Evidence, or archive pointers.

## Trust Rules

Search improves recall; metadata and lifecycle provide authority.

A trustworthy result should expose:

- `path`
- `doc_kind`
- `status`
- `feature_refs`
- `superseded_by` when old

If metadata is missing, open the source file and inspect frontmatter, headings, and links before treating content as authoritative.

## Fallback Search Patterns

When no retrieval CLI exists:

- Search user terms plus `ADR`, `Lesson`, `Feature`, `Evidence`, `decision`, `superseded`, `deprecated`, `stale`, `invalidates`, `updates`.
- Search filenames for likely IDs: `F001`, `ADR-001`, feature slugs, incident names, plan/spec titles.
- Prefer structured docs over loose transcript snippets.
- If only loose snippets exist, mark confidence as low.
