---
id: EV-026
doc_kind: evidence
feature_refs:
  - F017-agentmentor-vnext-gpt56-workflow
scope: Agent-selected unified engineering Index implementation
created: 2026-08-27
---

# EV-026: 主 Agent 选择的统一工程 Index 实现验证

## Supports Claim

统一 `docs/INDEX.md`、由 Feature/ADR 元数据生成的目录、主 Agent 语义选择契约、Schema 校验、安装资源和自动化测试已在仓库中实现。规则型 `context.py`、路径/关键词评分与 Top-1 自动路由不再属于 vNext 运行时表面。

## Verification Scope

覆盖 Index 生成与过期检测、有效 Feature/已接受 ADR 的收录规则、草稿/提案的排除、`index_summary` Schema、Skill 文本契约、安装资源、仓库级知识校验与 Python 测试。未覆盖真实 Agent 在真实历史任务中的语义选择质量。

## Checks

```text
python -m compileall -q scripts skills\agentmentor\scripts
python scripts\generate_index.py --root . --check
python scripts\knowledge_check.py --root . --docs-path docs --strict
python scripts\skill_metadata_check.py --root . --strict
pytest -q
git diff --check
```

## Results

Pass：Python 编译通过；统一 Index 为当前生成结果；vNext 文档与 Skill 元数据校验均为 0 errors；自动化测试 8 项通过；diff 空白检查通过。

## Artifacts

- `docs/INDEX.md`
- `docs/decisions/ADR-011-agent-selected-engineering-index.md`
- `skills/agentmentor/SKILL.md`
- `skills/agentmentor/scripts/generate_index.py`
- `skills/agentmentor/scripts/knowledge_check.py`
- `tests/test_generate_index.py`
- `tests/test_knowledge_check.py`

## Limitations

这不是主 Agent 语义选择质量或端到端性能 Evidence。尚未以 10–20 个真实历史变更检验关键 Feature/ADR 漏读、无关文档读取、Index 规模与端到端开发体验；在该基准完成前，不应宣称统一 Index 已提升召回质量或开发速度。
