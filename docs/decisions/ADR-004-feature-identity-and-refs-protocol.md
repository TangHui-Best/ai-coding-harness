---
id: ADR-004
doc_kind: adr
status: accepted
scope: project
feature_refs: []
decision_area: harness-knowledge-model
created: 2026-05-24
updated: 2026-05-25
---

# ADR-004: Path-Based Feature References

## Context

Harness needs a cheap and reliable way to connect ADR, Lesson, and Evidence records back to Feature pages.

The earlier draft identity protocol introduced `FP-YYYY-MM-DD-slug`, canonical `FNNN` IDs, and `aliases`. That reduced branch-number conflicts, but it made bug attribution more expensive: agents had to reason about aliases, canonicalization, Markdown links, and Feature filenames before opening the right source document.

In this project, that indirection is a higher cost than occasional branch-local `F001` collisions. A Feature filename already carries the short id and the meaningful slug, and `created` / `updated` preserve the timeline.

## Decision

Keep `feature_refs` as the single relationship field for ADR, Lesson, and Evidence artifacts, but make the reference value path-oriented.

Preferred values are:

- `docs/features/F001-feature-slug.md`
- `F001-feature-slug`

Bare short ids such as `F001` remain accepted only as a compatibility form. They produce a warning because they can become ambiguous across branches. If multiple Feature files share the same short id, a bare short-id reference is an error and the author must use a full Feature path or file stem.

Feature pages use simple short ids again:

```yaml
id: F001
doc_kind: feature
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

Do not require `FP-*`, `aliases`, `canonicalized_at`, or a separate Feature registry for the default workflow.

## Alternatives

- Keep the `FP-* -> FNNN + aliases` protocol: rejected because it pushed too much identity-resolution work into ordinary retrieval and bug attribution.
- Maintain a separate Feature registry: rejected for now because it creates another source that must be kept in sync.
- Use only bare `FNNN` references: rejected because duplicate branch-local short ids are acceptable, but ambiguous machine references are not.
- Fully revert to `feature_ids` / `source_feature_ids`: rejected because a single `feature_refs` field is still simpler across ADR, Lesson, and Evidence records.

## Consequences

Agents can open the referenced Feature directly when `feature_refs` uses a path or file stem. This should reduce broad Feature/Evidence/ADR searches during bug attribution.

The trade-off is that Feature renames require updating references. That cost is acceptable because Feature files are durable knowledge anchors and should not be renamed casually.

`knowledge_check.py` validates path and file-stem references, warns on unambiguous bare short ids, errors on ambiguous bare short ids, and no longer validates alias/canonicalization rules.

## Evidence

- `docs/evidence/EV-002-feature-identity-and-refs-protocol.md`
- `scripts/knowledge_check.py`
- `templates/FEATURE.md`
- `templates/ADR.md`
- `templates/LESSON.md`
- `templates/EVIDENCE.md`
- `tests/test_knowledge_check.py`
