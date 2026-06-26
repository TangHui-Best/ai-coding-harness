---
id: EV-017
doc_kind: evidence
scope: feature
feature_refs:
  - docs/features/F009-feature-intake-governance.md
created: 2026-06-26
---

# EV-017: Typed Links And Artifact Boundaries

## Commands

```text
python -m unittest tests.test_knowledge_check
python scripts/knowledge_check.py --root . --docs-path docs --strict
python scripts/knowledge_check.py --root . --docs-path docs --feature-index F009-feature-intake-governance
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --feature-index F009-feature-intake-governance
python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict
```

## Results

- Unit tests: Pass, 24 tests passed.
- Root strict knowledge check: Pass, scanned 53 markdown files, checked 43 knowledge artifacts, 0 errors, 0 warnings.
- Root local Feature Index check for `F009-feature-intake-governance`: Pass, 0 errors, 0 warnings.
- Bundled strict knowledge check: Pass, scanned 53 markdown files, checked 43 knowledge artifacts, 0 errors, 0 warnings.
- Bundled local Feature Index check for `F009-feature-intake-governance`: Pass, 0 errors, 0 warnings.
- Bundled skill metadata check: Pass, scanned 12 skill files, 0 errors, 0 warnings.

## Artifacts

- `templates/FEATURE.md`
- `skills/using-agentmentor/assets/templates/FEATURE.md`
- `scripts/knowledge_check.py`
- `skills/using-agentmentor/scripts/knowledge_check.py`
- `skills/knowledge-capture/SKILL.md`
- `skills/knowledge-capture/references/artifact-decision-matrix.md`
- `tests/test_knowledge_check.py`
- `docs/features/INDEX.md`
- `docs/features/F009-feature-intake-governance.md`
- `docs/features/F001-closeout-entry-anchor-validation.md`
- `docs/features/F002-canonical-harness-artifact-placement.md`
- `docs/features/F003-optional-harness-hook-runtime.md`
- `docs/features/F004-delegation-gate-three-outcomes.md`
- `docs/features/F005-session-recovery-hooks.md`
- `docs/features/F006-skill-naming-compatibility.md`
- `docs/features/F007-agentmentor-semantic-skill-routing.md`
- `docs/features/F008-spec-drift-guardrails.md`
- `docs/features/F010-goal-driven-feature-flow.md`
- `docs/evidence/EV-017-typed-links-and-artifact-boundaries.md`

## Notes

本次治理让 Feature 打开后的链接从自由列表变成分类入口：Evidence、Decisions / ADRs、Lessons、Specs / Plans、Related Features、External Context。Feature / ADR / Lesson 的写入边界进入 Knowledge Capture 和 artifact decision matrix，避免后续 Agent 把所有内容都塞进 Feature，或把决策、失败模式、验证事实混成同一种文档。
