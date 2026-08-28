---
id: EV-025
doc_kind: evidence
feature_refs:
  - F017-agentmentor-vnext-gpt56-workflow
scope: AgentMentor vNext initial implementation slice
created: 2026-07-29
---

# EV-025: AgentMentor vNext 初始实现验证

## Supports Claim

截至 2026-07-29，vNext 的六个 Skill 表面、一次性有界 `context`、当时的文档 Schema、安装器和替换后的行为测试已在仓库中实现；旧 12 Skill 与旧默认 Hook 不再属于运行时表面。该初始召回器随后被 ADR-011 的统一 Index 方案替代。

## Verification Scope

覆盖 Skill 元数据、vNext 文档校验、Context 的路径命中/无命中边界、临时安装目标以及 Python 测试套件。未覆盖真实历史任务的 Top-3 召回率或端到端耗时比较。

## Checks

```text
python -m compileall -q scripts skills\agentmentor\scripts
pytest -q
python scripts/skill_metadata_check.py --root . --strict
python scripts/knowledge_check.py --root . --docs-path docs --strict
git diff --check
```

## Results

Pass：8 项测试通过；Skill 元数据校验通过；两份 vNext 知识文档严格校验通过；编译与 diff 空白检查通过。

## Artifacts

- 历史实现提交：`ce295d9`
- `skills/agentmentor/scripts/knowledge_check.py`
- 历史测试：`tests/test_context.py`
- `tests/test_knowledge_check.py`
- `tests/test_install_scripts.py`
- `tests/test_skills.py`

## Limitations

这不是性能 Evidence，也不证明当前统一 Index 实现。当前测试使用合成的最小文档夹，仅证明当时召回器的有界行为与基本路径；尚未建立 10–20 个真实历史变更的关键召回、误召回、文本量、工具调用数和端到端时间基准。
