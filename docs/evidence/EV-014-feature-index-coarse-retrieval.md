---
id: EV-014
doc_kind: evidence
scope: feature
feature_refs:
  - docs/features/F009-feature-intake-governance.md
created: 2026-06-23
---

# EV-014: Feature Index Coarse Retrieval

## Commands

```text
python -m unittest ai-coding-harness.tests.test_knowledge_check
python -m unittest ai-coding-harness.tests.test_skill_progressive_disclosure
python ai-coding-harness/scripts/knowledge_check.py --root ai-coding-harness --docs-path docs --strict
python ai-coding-harness/skills/using-agentmentor/scripts/knowledge_check.py --root ai-coding-harness --docs-path docs --strict
python ai-coding-harness/scripts/skill_metadata_check.py --root ai-coding-harness --skills-path skills --strict
```

## Results

- `python -m unittest ai-coding-harness.tests.test_knowledge_check`: passed, 18 tests.
- `python -m unittest ai-coding-harness.tests.test_skill_progressive_disclosure`: passed, 21 tests.
- `python ai-coding-harness/scripts/knowledge_check.py --root ai-coding-harness --docs-path docs --strict`: passed on target main; scanned 50 markdown files, checked 40 knowledge artifacts, errors 0, warnings 0.
- `python ai-coding-harness/skills/using-agentmentor/scripts/knowledge_check.py --root ai-coding-harness --docs-path docs --strict`: passed on target main; scanned 50 markdown files, checked 40 knowledge artifacts, errors 0, warnings 0.
- `python ai-coding-harness/scripts/skill_metadata_check.py --root ai-coding-harness --skills-path skills --strict`: passed; scanned 12 skill files, errors 0, warnings 0.

## Artifacts

- `docs/features/INDEX.md` is the coarse Feature recall index.
- `skills/knowledge-retrieval/SKILL.md` now routes no-ref retrieval through the Feature Index or filename fallback.
- `skills/using-agentmentor/SKILL.md` now documents the coarse recall rule in the hot path.
- `templates/FEATURE.md` and bundled Feature template now include the filename recall rule.
- `knowledge_check.py` and the bundled copy now skip `docs/features/INDEX.md` as a non-artifact index.

## Notes

This iteration intentionally does not add Feature frontmatter recall fields, task-type recall intensity, vector-search schema, or key-section-only reading. The goal is to improve recall before Feature opening with naming, a lightweight index, and a coarse retrieval rule.
