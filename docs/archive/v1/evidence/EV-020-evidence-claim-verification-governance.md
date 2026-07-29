---
id: EV-020
doc_kind: evidence
scope: feature
feature_refs:
  - docs/features/F013-evidence-claim-verification-governance.md
created: 2026-06-27
---

# EV-020: Evidence Claim Verification Governance

## Supports Claim

F013 的 Evidence 新结构已经被模板、validator、测试、既有 Evidence 迁移和 Feature Index 校验共同验证。

## Verification Scope

覆盖：root/bundled Evidence 模板、root/bundled `knowledge_check.py`、Knowledge Capture 规则、artifact decision matrix、completion closeout contract、现有 Evidence 结构迁移、F013 Feature Index 本地条目。

不覆盖：未来真实任务中的 Evidence 写作质量、Evidence 长期复用率、Evidence 是否需要独立 Index。

## Checks

```text
rg -n "^## (Scope|Commands|Harness Validation|AgentMentor Validation|AI Coding Harness Validation)$" docs/evidence templates/EVIDENCE.md skills/using-agentmentor/assets/templates/EVIDENCE.md
python -m unittest tests.test_knowledge_check
python scripts/knowledge_check.py --root . --docs-path docs --strict
python scripts/knowledge_check.py --root . --docs-path docs --feature-index F013-evidence-claim-verification-governance
python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --feature-index F013-evidence-claim-verification-governance
python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict
git diff --check
```

## Results

- `rg -n "^## (Scope|Commands|Harness Validation|AgentMentor Validation|AI Coding Harness Validation)$" docs/evidence templates/EVIDENCE.md skills/using-agentmentor/assets/templates/EVIDENCE.md`: no matches; old Evidence headings are not present in Evidence docs or templates.
- `python -m unittest tests.test_knowledge_check`: passed, 35 tests.
- `python scripts/knowledge_check.py --root . --docs-path docs --strict`: passed, 60 markdown files scanned, 50 knowledge artifacts checked, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index F013-evidence-claim-verification-governance`: passed, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --feature-index F013-evidence-claim-verification-governance`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict`: passed, 12 skill files scanned, 0 errors, 0 warnings.
- `git diff --check`: passed.

## Artifacts

- `templates/EVIDENCE.md`
- `skills/using-agentmentor/assets/templates/EVIDENCE.md`
- `scripts/knowledge_check.py`
- `skills/using-agentmentor/scripts/knowledge_check.py`
- `tests/test_knowledge_check.py`
- `skills/knowledge-capture/SKILL.md`
- `skills/knowledge-capture/references/artifact-decision-matrix.md`
- `skills/knowledge-capture/references/completion-closeout-contract.md`
- `docs/evidence/`
- `docs/features/INDEX.md`
- `docs/features/F013-evidence-claim-verification-governance.md`
- `docs/evidence/EV-020-evidence-claim-verification-governance.md`

## Limitations

本 Evidence 证明结构、校验和迁移已经完成；不证明未来每份 Evidence 都会写出高质量的 `Supports Claim` 或 `Limitations`。真实质量仍需要后续任务中的写作和必要时的 validator 低线检查。

## Notes

本次治理刻意不把 Evidence 设计成高复用知识库。Evidence 的核心边界是约束完成声明：声明必须绑定可核验检查、结果、材料和限制。
