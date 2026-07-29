---
id: F017
doc_kind: feature
status: active
created: 2026-07-27
updated: 2026-07-29
owned_paths:
  - skills/
  - scripts/
  - templates/
  - docs/features/
trigger_terms:
  - AgentMentor vNext
  - GPT-5.6
  - workflow cost
  - context retrieval
  - engineering memory
---

# F017: AgentMentor vNext 工作流

## Goal

将 AgentMentor 从默认串行 Gate 编排器重构为面向 GPT-5.6 的工程记忆、Feature 级 SDD Spec 与验证约束层：普通开发只获得一次精确上下文，其余规划、实现、测试和协作由模型自主完成。

## Scope

### In Scope

- 六个事件触发 Skill 与一次性 `agentmentor context` 召回。
- Feature、ADR、Lesson、Evidence、Feature Index 的 vNext Schema。
- 独立于 OpenSpec、Superpowers 的 SDD 与 TDD 闭环。
- 轻量 closeout，以及仅在明确证据边界执行的校验。

### Non-goals

- 不维护旧 Gate、旧模板或旧 Schema 的运行时兼容层。
- 不把减少 Skill 数量本身当作性能结论。
- 不依赖外部编排框架才能运行。

## Specification

### Behavior

- 开始或恢复有项目上下文依赖的任务时，`agentmentor` 只执行一次 `context`。
- 召回按路径精确匹配、Feature Index 粗筛、Feature 正文、直接关联的 ADR/Lesson/Evidence 的顺序进行，默认最多返回三份正文文档。
- 仅在意图冲突、稳定取舍、规格漂移/重复失败、关键声明或任务暂停时，分别触发 intent、decision、learning、evidence、closeout。

### Rules and Constraints

- Feature 是 Feature 级 SDD Spec；ADR 记录取舍；Lesson 记录真实失败与防护；Evidence 记录验证事实。
- 无高置信命中时返回 `no relevant context`，不得扩大为全量扫描。
- closeout 只能压缩本轮已有事实，不能重新检索、扫描文档或强制创建产物。
- 历史 v1 文档位于 `docs/archive/v1/`，仅作人工追溯来源，不进入 vNext 热路径。

## Acceptance

- AC-01：给定包含已知路径或触发词的任务，`agentmentor context` 最多返回三份正文文档，并说明每份命中原因。
  - 自动化验证：`tests/test_context.py`。
- AC-02：给定无关联任务，`agentmentor context` 返回明确的 `no relevant context`，不读取归档或全量文档。
  - 自动化验证：`tests/test_context.py`。
- AC-03：给定一个新 vNext 文档，严格校验器接受新 Schema；缺失关键字段、章节或 superseded 指针时拒绝。
  - 自动化验证：`tests/test_knowledge_check.py`。
- AC-04：安装产物只暴露六个 vNext Skill，不含旧的默认 Gate Skill。
  - 自动化验证：`tests/test_install_scripts.py`、`tests/test_skill_metadata_check.py`。

## Current State

第一实现切片已完成：Schema、模板、六个 Skill、一次性召回器、安装器与替换后的行为测试均已落地。仍需以 10–20 个真实历史变更完成召回质量与端到端效率基准，之后才能将本 Feature 标记为 delivered 或宣称性能改善。

## Decision Context

### Why

GPT-5.6 已具备常规任务拆分、验证选择与协作判断能力；当前真正稀缺的是项目专属历史、可执行规格与可验证事实。

### Why Not

不保留“缩短文字的旧 12 Skill”，因为默认串行路由和重复状态判断仍会留在热路径；也不将能力压成几个巨型 Skill，以免把同样成本藏进更长的提示词。

### If Modifying This Area, Check

- [ADR-010](../decisions/ADR-010-agentmentor-vnext-event-triggered-memory-layer.md)
- `docs/proposals/2026-07-28-agentmentor-vnext-refactoring-plan.md`
- `tests/test_context.py` 与 `tests/test_knowledge_check.py`

## Links

### ADRs

- [ADR-010](../decisions/ADR-010-agentmentor-vnext-event-triggered-memory-layer.md)

### Lessons

- None.

### Evidence

- [EV-025 vNext 初始实现验证](../evidence/EV-025-agentmentor-vnext-initial-implementation.md)

### Related Features

- None.

### External Context

- [vNext 重构计划](../proposals/2026-07-28-agentmentor-vnext-refactoring-plan.md)
- [GPT-5.6 后工作流成本分析](../proposals/2026-07-27-agentmentor-vnext-gpt56-workflow-cost-analysis.md)
