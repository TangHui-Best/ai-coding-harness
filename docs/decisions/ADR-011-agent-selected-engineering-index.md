---
id: ADR-011
doc_kind: adr
status: accepted
index_summary: 统一 Index 提供当前有效的 Feature 与 ADR 目录，由主 Agent 语义选择需要阅读的工程事实。
feature_refs:
  - F017-agentmentor-vnext-gpt56-workflow
decision_area: agentmentor-vnext-retrieval
supersedes: []
created: 2026-08-27
updated: 2026-08-27
---

# ADR-011: 采用主 Agent 选择的统一工程 Index

## Context

旧 vNext 召回器以 `owned_paths` 与 `trigger_terms` 对 Feature Index 行评分，并自动选择唯一 Feature。该机制把跨 Feature、跨架构的语义判断压缩为规则匹配，可能漏掉关键上下文；已接受 ADR 也只能经由 Feature 的链接被间接发现。

## Decision

以 `docs/INDEX.md` 取代 `docs/features/INDEX.md`。统一 Index 只包含当前有效的 Feature 与已接受 ADR，每行只记录可点击的 Document、Type 与 Brief。主 Agent 在任务可能影响行为、规格、架构、接口、数据语义或验收时读取一次 Index，并基于任务语义自主选择默认 0–3 个 Feature，必要时直接读取 ADR，再按需展开一跳关联的 Lesson、Evidence 或 ADR。

## Boundary

- Index 是目录和工程地图，不是规则引擎、向量数据库或后台检索服务。
- 纯机械、局部、无行为语义的改动可以跳过 Index；用户明确指定 Feature 时可直接读取该 Feature。
- `0–3` 是默认 Feature 阅读策略，不是 Hook 或运行时强制上限；关联文档按是否改变当前判断决定。
- `docs/archive/v1/`、草稿、归档与已替代文档不进入 Index。

## Rejected Options

- 保留路径/关键词评分并优化权重：仍然是规则替主 Agent 路由，无法解决语义关联与跨 Feature 场景。
- 将 Feature 与 ADR 分成两个常驻 Index：增加主 Agent 的入口判断与目录维护成本。
- 用异步小模型、向量检索或 Hook 选择正文：增加模型调用、延迟与不可解释性，超出当前问题所需复杂度。
- 将 Lesson 与 Evidence 也加入常驻 Index：会稀释 Feature/ADR 的地图作用并扩大默认上下文。

## Consequences

- Feature 与 ADR 必须维护简短的 `index_summary`；Index 由生成器派生并在 CI 校验。
- 主 Agent 获得跨 Feature 与架构语义选择权，但选择质量必须通过真实历史任务基准验证。
- 规则型 `context.py` 被移除；不恢复默认 Gate、Stop Hook 或全库递归检索。

## Revisit When

- 真实样本显示主 Agent 系统性漏读关键 Feature 或 ADR。
- Index 规模无法保持为可快速阅读的高信息密度目录。
- 有证据表明额外检索机制在召回质量上显著优于主 Agent 选择，且成本与可解释性可接受。

## Links / Evidence

- [F017](../features/F017-agentmentor-vnext-gpt56-workflow.md)
- [ADR-010](ADR-010-agentmentor-vnext-event-triggered-memory-layer.md)
- 实现验证将在本次改造完成后记录为新的 Evidence。
