---
id: ADR-010
doc_kind: adr
status: accepted
index_summary: 默认不运行 Gate 链；仅在工程事件发生时沉淀可复用的规格、决策、经验与证据。
feature_refs:
  - F017-agentmentor-vnext-gpt56-workflow
decision_area: agentmentor-vnext-architecture
applies_to_paths:
  - skills/
  - scripts/
  - templates/
trigger_terms:
  - AgentMentor vNext
  - event triggered
  - workflow orchestration
supersedes:
  - ADR-001
  - ADR-003
  - ADR-006
created: 2026-07-28
updated: 2026-07-29
---

# ADR-010: 采用事件触发的工程记忆层

## Context

GPT-5.6 能自主完成多数常规开发判断。旧版将开始、方向、委派、就绪与知识捕获串为默认 Gate，使小改动反复判断相近状态并重复读取项目文档。

## Decision

AgentMentor vNext 采用事件触发的工程记忆、Feature 级 SDD Spec 与验证约束层。运行期仅保留 `agentmentor`、`agentmentor-intent`、`agentmentor-decision`、`agentmentor-learning`、`agentmentor-evidence` 与 `agentmentor-closeout` 六个 Skill。

## Boundary

- 适用于 vNext 的 Skill 路由、模板、校验器、安装器、Hook 与测试。
- 不适用于 v1.0.0 GitHub Release 代表的历史版本，或外部工具自己的 Spec/Plan 能力。
- 项目规则的升级仍需人工授权，不随日常任务自动发生。

## Rejected Options

- 保留旧 12 Skill 并仅缩短文字：无法消除默认串行路由和重复判断。
- 合并为少数巨型 Skill：会把路由成本隐藏进更长的热路径提示词。
- 删除历史决策与证据：会让后续 Agent 只能从聊天记录或 diff 猜测原因。
- 同时解析旧/新 Schema：会引入双轨行为与运行时复杂度。

## Consequences

- 普通任务的流程负担降低，但 `agentmentor context` 必须通过真实样本证明没有关键漏召回。
- 文档收敛为可检索的规格、决策、经验与事实；历史 v1 资料归档，不进入热路径。
- closeout 保留为状态压缩，不得重启全套 Gate 或全量文档扫描。

## Revisit When

- 基准样本显示关键上下文漏召回。
- 新模型无法稳定完成原本交由其自主判断的常规工程动作。
- 有可证实、无法由事件触发模型解决的治理缺口。

## Links / Evidence

- [F017](../features/F017-agentmentor-vnext-gpt56-workflow.md)
- [vNext 重构计划](../proposals/2026-07-28-agentmentor-vnext-refactoring-plan.md)
- v1.0.0 baseline: `b7b2bec75bf4c91d644394b16b16e0a2fed91247`
