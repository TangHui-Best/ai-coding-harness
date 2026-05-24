---
id: EV-002
doc_kind: evidence
scope: project
feature_refs: []
created: 2026-05-24
---

# EV-002: Feature Identity And Refs Protocol

## Commands

```text
python -m unittest tests.test_knowledge_check
python -m unittest discover -s tests
python scripts\knowledge_check.py --root . --docs-path docs --strict
python skills\using-harness\scripts\knowledge_check.py --root examples\project-harness --docs-path docs --strict
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
```

## Results

```text
python -m unittest tests.test_knowledge_check
Ran 7 tests in 0.767s
OK

python -m unittest discover -s tests
Ran 23 tests in 1.978s
OK

python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 14 markdown file(s). Checked 8 knowledge artifact(s). Errors: 0. Warnings: 0.

python skills\using-harness\scripts\knowledge_check.py --root examples\project-harness --docs-path docs --strict
Scanned 4 markdown file(s). Checked 4 knowledge artifact(s). Errors: 0. Warnings: 0.

python scripts\skill_metadata_check.py --root . --skills-path skills --strict
Scanned 11 skill file(s). Errors: 0. Warnings: 0.
```

## Artifacts

- `scripts/knowledge_check.py`
- `skills/using-harness/scripts/knowledge_check.py`
- `templates/FEATURE.md`
- `templates/ADR.md`
- `templates/LESSON.md`
- `templates/EVIDENCE.md`
- `skills/using-harness/assets/templates/`
- `docs/decisions/ADR-004-feature-identity-and-refs-protocol.md`
- `tests/test_knowledge_check.py`

## Notes

The red phase intentionally failed because `knowledge_check.py` still required `feature_ids` and did not understand `feature_refs` or Feature aliases. The green phase made `feature_refs` the relationship field, allowed references through `aliases`, rejected duplicate Feature refs, and warned on Markdown links to draft `FP-*` Feature paths.
