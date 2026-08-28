---
id: EV-016
doc_kind: evidence
scope: feature
feature_refs:
  - docs/features/F009-feature-intake-governance.md
created: 2026-06-26
---

# EV-016: Feature Index Local Governance

## Supports Claim

This Evidence supports the completion or validation claim for EV-016: Feature Index Local Governance.


## Verification Scope

This Evidence covers the checks and results recorded below.

## Checks
```text
python -m unittest tests.test_knowledge_check
python scripts/knowledge_check.py --root . --docs-path docs --strict
python scripts/knowledge_check.py --root . --docs-path docs --feature-index F009-feature-intake-governance
python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --feature-index F009-feature-intake-governance
python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict
```

## Results

- Unit tests: Pass, 23 tests passed.
- Root strict knowledge check: Pass, scanned 52 markdown files, checked 42 knowledge artifacts, 0 errors, 0 warnings.
- Root local Feature Index check for `F009-feature-intake-governance`: Pass, 0 errors, 0 warnings.
- Root explicit global Feature Index audit: Pass, 0 errors, 0 warnings.
- Bundled strict knowledge check: Pass, scanned 52 markdown files, checked 42 knowledge artifacts, 0 errors, 0 warnings.
- Bundled local Feature Index check for `F009-feature-intake-governance`: Pass, 0 errors, 0 warnings.
- Bundled skill metadata check: Pass, scanned 12 skill files, 0 errors, 0 warnings.

## Artifacts

- `scripts/knowledge_check.py`
- `skills/using-agentmentor/scripts/knowledge_check.py`
- `skills/using-agentmentor/SKILL.md`
- `skills/knowledge-retrieval/SKILL.md`
- `skills/knowledge-capture/SKILL.md`
- `tests/test_knowledge_check.py`
- `docs/features/INDEX.md`
- `docs/features/F009-feature-intake-governance.md`
- `docs/evidence/EV-016-feature-index-local-governance.md`

## Limitations

This Evidence does not prove behavior outside the verification scope recorded above.

## Notes
本次治理把 Feature Index 的一致性检查拆成两个层级：默认只检查当前关联 Feature 的 Index 入口是否存在、唯一且可用于粗召回；全局机械审计只在用户显式要求时触发，避免普通任务收尾因为全量扫描而变长。
