---
id: EV-021
doc_kind: evidence
scope: feature
feature_refs:
  - docs/features/F014-project-rules-human-authorized-governance.md
created: 2026-06-27
---

# EV-021: Project Rules Human Authorized Governance

## Supports Claim

F014 的 Project Rules / AGENTS 治理已经落地：规则晋升必须经过人类授权，必须 source-backed、可验证、可写成 MUST/MUST NOT，并受 AGENTS 长度预算约束。

## Verification Scope

覆盖：`skills/project-rules/SKILL.md`、root/bundled AGENTS starter templates、artifact decision matrix、Project Rules governance tests、F014 Feature Index 本地条目。

不覆盖：当前仓库根目录 `AGENTS.md` 创建或修改、未来真实项目中每条规则的质量、大型既有 AGENTS.md 的瘦身迁移工具。

## Checks

```text
python -m unittest tests.test_project_rules_governance
python -m unittest tests.test_knowledge_check tests.test_project_rules_governance tests.test_skill_progressive_disclosure
python scripts/knowledge_check.py --root . --docs-path docs --strict
python scripts/knowledge_check.py --root . --docs-path docs --feature-index F014-project-rules-human-authorized-governance
python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --feature-index F014-project-rules-human-authorized-governance
python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict
git diff --check
```

## Results

- `python -m unittest tests.test_project_rules_governance`: passed, 4 tests.
- `python -m unittest tests.test_knowledge_check tests.test_project_rules_governance tests.test_skill_progressive_disclosure`: passed, 62 tests.
- `python scripts/knowledge_check.py --root . --docs-path docs --strict`: passed, 62 markdown files scanned, 52 knowledge artifacts checked, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index F014-project-rules-human-authorized-governance`: passed, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --feature-index F014-project-rules-human-authorized-governance`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict`: passed, 12 skill files scanned, 0 errors, 0 warnings.
- `git diff --check`: passed.

## Artifacts

- `skills/project-rules/SKILL.md`
- `templates/AGENTS.md`
- `skills/using-agentmentor/assets/templates/AGENTS.md`
- `skills/knowledge-capture/references/artifact-decision-matrix.md`
- `tests/test_project_rules_governance.py`
- `docs/features/INDEX.md`
- `docs/features/F014-project-rules-human-authorized-governance.md`
- `docs/evidence/EV-021-project-rules-human-authorized-governance.md`

## Limitations

本 Evidence 证明规则晋升机制、模板和校验已经落地；不证明未来每个项目都会正确选择规则，也不证明已有大型 AGENTS.md 已完成瘦身。

## Notes

本次迭代刻意没有创建或修改当前项目根目录 `AGENTS.md`。AGENTS.md 的修改必须由用户明确请求、批准，或由仓库既有流程授权。
