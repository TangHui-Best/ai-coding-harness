---
id: ADR-010
doc_kind: adr
status: accepted
scope: project
feature_refs:
  - F017-agentmentor-vnext-gpt56-workflow
decision_area: agentmentor-vnext-architecture
created: 2026-07-28
updated: 2026-07-28
---

# ADR-010: AgentMentor vNext 采用事件触发的工程记忆层

## Context

GPT-5.6 已能够自主完成多数常规开发任务的拆分、实施、测试选择和协作判断。现有 AgentMentor 将 Start、Vision、Delegation、Readiness、Capture 等判断串成默认 Gate 流程，导致模型在小改动中重复解释相近状态、重复检索项目文档，并将流程遵从成本放大为开发延迟。

AgentMentor 仍必须独立保留 Feature 级 SDD Spec、历史取舍、失败防复发、验证证据和任务状态恢复能力；不能依赖 OpenSpec 或 Superpowers 才能工作。

## Decision

AgentMentor vNext 从默认开发编排器重构为事件触发的工程记忆、SDD Spec 与验证约束层。

- 默认路径只执行一次 `agentmentor context`，随后由模型自主计划、TDD/实施和验证。
- 仅在意图冲突、稳定设计取舍、规格漂移或重复失败、关键完成/发布/交接声明、任务结束或暂停时，触发对应的 intent、decision、learning、evidence 或 closeout 能力。
- vNext 只保留 `agentmentor`、`agentmentor-intent`、`agentmentor-decision`、`agentmentor-learning`、`agentmentor-evidence`、`agentmentor-closeout` 六个 Skill。
- Feature、ADR、Lesson、Evidence、Feature Index 继续作为唯一长期文档体系；Feature 是 AgentMentor 自己的 Feature 级 SDD Spec。
- vNext 不保留旧 Skill、旧 Schema 或旧 Gate 的运行时兼容层；v0 由 GitHub Release `v0.2.0` 固定为可回退基线。

## Decision Boundary

### Applies To

- AgentMentor vNext 的 Skill 路由、模板、校验器、安装脚本、Hook 和测试。
- 以 GPT-5.6 或后续具备同等自主工程能力的模型为主要使用环境。

### Does Not Apply To

- v0.2.0 的 Git 标签与 GitHub Release 所代表的历史版本。
- 外部工具自身的 Spec、Plan 或任务执行能力。
- 人工授权的项目规则维护；此类规则不因日常任务自动生成。

## Rejected Options

- 保留 12 个旧 Skill 并仅缩短文字：无法消除默认串行路由与重复状态判断。
- 将全部能力合并成 4 个大型 Skill：会把路由成本隐藏进更长的热路径提示词，并丢失意图与收尾的独立边界。
- 删除历史检索、ADR、Lesson 或 Evidence：会让未来 Agent 只能依赖聊天记录和 diff 猜测设计理由。
- 保留 v0/vNext 双轨解析：增加运行时复杂度，并使两个版本的触发语义相互干扰。

## Consequences

- 普通任务的流程负担降低，但 vNext 必须用真实样本证明 `agentmentor context` 没有关键漏召回。
- 文档 Schema 必须从流程日志收敛为可检索的规格、决定、经验与事实。
- closeout 仍存在，但只能压缩已有状态，不能重新触发全套 Gate 或文档扫描。
- 旧文档保留为归档来源；只精炼仍会影响未来决策的内容进入 vNext 基线。

## Before Changing This Decision

- 阅读 F017 和 vNext 重构计划。
- 检查 `agentmentor context` 的真实历史任务基准，特别是关键上下文漏召回与无关文档加载。
- 检查 vNext 是否仍保留 Feature 级 SDD、可测试验收条件、ADR 的拒绝方案、Lesson 的可执行防护、Evidence 的范围和限制。
- 若重新引入默认 Gate 或运行时兼容层，必须新建 ADR 并说明其不可由事件触发模型解决的具体问题。

## Evidence

- [F017: AgentMentor vNext GPT-5.6 Workflow](../features/F017-agentmentor-vnext-gpt56-workflow.md)
- [AgentMentor vNext 重构计划](../proposals/2026-07-28-agentmentor-vnext-refactoring-plan.md)
- GitHub tag: `v0.2.0` at `1a3fa2a57bd394e9a866e8f5b110392bf7620aa6`
