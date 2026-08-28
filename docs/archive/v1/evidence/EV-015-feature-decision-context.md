---
id: EV-015
doc_kind: evidence
scope: feature
feature_refs:
  - docs/features/F009-feature-intake-governance.md
created: 2026-06-24
---

# EV-015: Feature Decision Context

## Supports Claim

This Evidence supports the completion or validation claim for EV-015: Feature Decision Context.


## Verification Scope

This Evidence covers the checks and results recorded below.

## Checks
```text
python -m unittest ai-coding-harness.tests.test_knowledge_check
python ai-coding-harness/scripts/knowledge_check.py --root ai-coding-harness --docs-path docs --strict
python ai-coding-harness/skills/using-agentmentor/scripts/knowledge_check.py --root ai-coding-harness --docs-path docs --strict
python ai-coding-harness/scripts/skill_metadata_check.py --root ai-coding-harness --skills-path skills --strict
```

## Results

- `python -m unittest ai-coding-harness.tests.test_knowledge_check`: passed, 19 tests.
- `python ai-coding-harness/scripts/knowledge_check.py --root ai-coding-harness --docs-path docs --strict`: passed; scanned 51 markdown files, checked 41 knowledge artifacts, errors 0, warnings 0.
- `python ai-coding-harness/skills/using-agentmentor/scripts/knowledge_check.py --root ai-coding-harness --docs-path docs --strict`: passed; scanned 51 markdown files, checked 41 knowledge artifacts, errors 0, warnings 0.
- `python ai-coding-harness/scripts/skill_metadata_check.py --root ai-coding-harness --skills-path skills --strict`: passed; scanned 12 skill files, errors 0, warnings 0.

## Artifacts

- `templates/FEATURE.md`
- `skills/using-agentmentor/assets/templates/FEATURE.md`
- `scripts/knowledge_check.py`
- `skills/using-agentmentor/scripts/knowledge_check.py`
- `tests/test_knowledge_check.py`
- `skills/knowledge-capture/SKILL.md`
- `docs/features/F001` through `F010` updated with `Decision Context`

## Limitations

This Evidence does not prove behavior outside the verification scope recorded above.

## Notes
This iteration keeps the structure intentionally small: `Why`, `Why Not`, and `If Modifying This Area, Check`. It does not add `Last Accepted Decision`, separate `Fragile Boundary`, separate `Before Modifying`, scoring, vector-search fields, or complex content quality checks.
