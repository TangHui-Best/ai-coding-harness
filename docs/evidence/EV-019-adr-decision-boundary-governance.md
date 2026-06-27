---
id: EV-019
doc_kind: evidence
scope: feature
feature_refs:
  - docs/features/F012-adr-decision-boundary-governance.md
created: 2026-06-27
---

# EV-019: ADR Decision Boundary Governance

## Commands

```text
rg -n "^## Alternatives" docs/decisions templates/ADR.md skills/using-agentmentor/assets/templates/ADR.md
python -m unittest tests.test_knowledge_check
python scripts/knowledge_check.py --root . --docs-path docs --strict
python scripts/knowledge_check.py --root . --docs-path docs --feature-index F012-adr-decision-boundary-governance
python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --feature-index F012-adr-decision-boundary-governance
python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict
git diff --check
```

## Results

- `rg -n "^## Alternatives" docs/decisions templates/ADR.md skills/using-agentmentor/assets/templates/ADR.md`: no matches; old ADR heading is not present in ADR docs or templates.
- `python -m unittest tests.test_knowledge_check`: passed, 31 tests.
- `python scripts/knowledge_check.py --root . --docs-path docs --strict`: passed, 58 markdown files scanned, 48 knowledge artifacts checked, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index F012-adr-decision-boundary-governance`: passed, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --feature-index F012-adr-decision-boundary-governance`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict`: passed, 12 skill files scanned, 0 errors, 0 warnings.
- `git diff --check`: passed.

## Artifacts

- `templates/ADR.md`
- `skills/using-agentmentor/assets/templates/ADR.md`
- `scripts/knowledge_check.py`
- `skills/using-agentmentor/scripts/knowledge_check.py`
- `tests/test_knowledge_check.py`
- `skills/knowledge-capture/SKILL.md`
- `skills/knowledge-capture/references/artifact-decision-matrix.md`
- `skills/incident-learning/SKILL.md`
- `docs/decisions/ADR-001-start-gate-before-implementation.md`
- `docs/decisions/ADR-002-chinese-prose-for-knowledge-artifacts.md`
- `docs/decisions/ADR-003-explicit-delegation-decision-before-complex-work.md`
- `docs/decisions/ADR-004-feature-identity-and-refs-protocol.md`
- `docs/decisions/ADR-005-canonical-harness-artifact-placement.md`
- `docs/decisions/ADR-006-skill-progressive-disclosure-boundary.md`
- `docs/decisions/ADR-007-ai-coding-harness-skill-naming-compatibility.md`
- `docs/decisions/ADR-008-agentmentor-semantic-skill-routing.md`
- `docs/decisions/ADR-009-adr-decision-boundary-structure.md`
- `docs/features/INDEX.md`
- `docs/features/F012-adr-decision-boundary-governance.md`
- `docs/evidence/EV-019-adr-decision-boundary-governance.md`

## Notes

本次治理把 ADR 定位为长期决策边界控制器：它记录被接受方案、适用边界、非适用边界、已拒绝方案、后果和修改前检查。ADR 文件名承担轻量召回职责，但不新增 ADR Index。
