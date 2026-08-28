---
id: F017
doc_kind: feature
status: active
index_summary: 以统一工程 Index 供主 Agent 语义选择 Feature 与 ADR，替代规则型 Top-1 召回。
created: 2026-07-27
updated: 2026-08-27
---

# F017: AgentMentor vNext 工作流

## Goal

将 AgentMentor 从默认串行 Gate 编排器重构为面向 GPT-5.6 的工程记忆、Feature 级 SDD Spec 与验证约束层：普通开发只获得一次精确上下文，其余规划、实现、测试和协作由模型自主完成。

## Scope

### In Scope

- 六个事件触发 Skill 与一次统一工程 Index 阅读。
- Feature、ADR、Lesson、Evidence 与统一 Index 的 vNext Schema。
- 独立于 OpenSpec、Superpowers 的 SDD 与 TDD 闭环。
- 轻量 closeout，以及仅在明确证据边界执行的校验。

### Non-goals

- 不维护旧 Gate、旧模板或旧 Schema 的运行时兼容层。
- 不把减少 Skill 数量本身当作性能结论。
- 不依赖外部编排框架才能运行。

## Specification

### Behavior

- 对可能改变功能行为、规格、架构边界、接口契约、数据语义或验收条件的任务，`agentmentor` 提示主 Agent 读取一次 `docs/INDEX.md`。
- Index 合并当前有效 Feature 与已接受 ADR；主 Agent 基于 Brief 自主选择默认 0–3 个 Feature，按需直接选择 ADR 或展开一跳关联的 ADR/Lesson/Evidence。
- 仅在意图冲突、稳定取舍、规格漂移/重复失败、关键声明或任务暂停时，分别触发 intent、decision、learning、evidence、closeout。

### Rules and Constraints

- Feature 是 Feature 级 SDD Spec；ADR 记录取舍；Lesson 记录真实失败与防护；Evidence 记录验证事实。
- Index 是工程目录而不是路由规则；不得按路径、关键词评分替主 Agent 选定唯一正文，也不得自动展开全部链接或递归搜索历史。
- closeout 只能压缩本轮已有事实，不能重新检索、扫描文档或强制创建产物。
- 历史 v1 文档位于 `docs/archive/v1/`，仅作人工追溯来源，不进入 vNext 热路径。

## Acceptance

- AC-01：`docs/INDEX.md` 仅包含当前有效的 Feature 与已接受 ADR，且每行只有 Document、Type、Brief。
  - 自动化验证：`tests/test_generate_index.py`。
- AC-02：生成器与严格校验器拒绝过期的 Index、失效链接、缺失 `index_summary` 或不应收录的状态。
  - 自动化验证：`tests/test_generate_index.py`、`tests/test_knowledge_check.py`。
- AC-03：给定一个新 vNext 文档，严格校验器接受新 Schema；缺失关键字段、章节或 superseded 指针时拒绝。
  - 自动化验证：`tests/test_knowledge_check.py`。
- AC-04：安装产物只暴露六个 vNext Skill，不含旧的默认 Gate Skill。
  - 自动化验证：`tests/test_install_scripts.py`、`tests/test_skill_metadata_check.py`。

## Current State

统一 Index 的实现已完成：规则型 `context.py` 已被替换为 Index 生成、校验与主 Agent 语义选择契约。仍需以 10–20 个真实历史变更完成选择质量与端到端体验基准，之后才能将本 Feature 标记为 delivered 或宣称性能改善。

## Decision Context

### Why

GPT-5.6 已具备常规任务拆分、验证选择与协作判断能力；当前真正稀缺的是项目专属历史、可执行规格与可验证事实。

### Why Not

不保留“缩短文字的旧 12 Skill”，因为默认串行路由和重复状态判断仍会留在热路径；也不将能力压成几个巨型 Skill，以免把同样成本藏进更长的提示词。

### If Modifying This Area, Check

- [ADR-010](../decisions/ADR-010-agentmentor-vnext-event-triggered-memory-layer.md)
- [ADR-011](../decisions/ADR-011-agent-selected-engineering-index.md)
- `docs/proposals/2026-07-28-agentmentor-vnext-refactoring-plan.md`
- `tests/test_generate_index.py` 与 `tests/test_knowledge_check.py`

## Links

### ADRs

- [ADR-010](../decisions/ADR-010-agentmentor-vnext-event-triggered-memory-layer.md)
- [ADR-011](../decisions/ADR-011-agent-selected-engineering-index.md)

### Lessons

- None.

### Evidence

- [EV-025 vNext 初始实现验证](../evidence/EV-025-agentmentor-vnext-initial-implementation.md)
- [EV-026 主 Agent 选择的统一工程 Index 实现验证](../evidence/EV-026-agent-selected-engineering-index-implementation.md)

### Related Features

- None.

### External Context

- [vNext 重构计划](../proposals/2026-07-28-agentmentor-vnext-refactoring-plan.md)
- [GPT-5.6 后工作流成本分析](../proposals/2026-07-27-agentmentor-vnext-gpt56-workflow-cost-analysis.md)
