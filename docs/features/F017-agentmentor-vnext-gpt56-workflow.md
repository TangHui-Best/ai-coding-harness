---
id: F017
doc_kind: feature
status: active
created: 2026-07-27
updated: 2026-07-28
---

# F017: AgentMentor vNext GPT-5.6 Workflow

## Goal

为 AgentMentor 大版本升级建立可恢复的分析入口：在不依赖 OpenSpec 的前提下，重新界定 GPT-5.6 时代 AgentMentor 应保留的长期记忆能力，以及应退出默认开发热路径的编排职责。

## Vision Anchor

- 原始请求或来源：用户明确指出 GPT-5.6 下，使用 AgentMentor 开发小改动明显变慢，并将后续迭代视为大版本升级。
- 用户痛点或工程问题：当前 Skill 可能把模型已具备的规划、委派、验证和收尾判断重复固化为多层 Gate，消耗模型推理而非解决实际工程问题。
- 期望结果：先形成不包含历史文档格式问题的原因分析材料，再以可验证的方式确定 vNext 工作流。
- 非目标或边界：本 Feature 当前不实施 vNext、不修改现有 Skill、不创建兼容层，也不将任何未批准方案写成已接受 ADR。
- Exit Gate 对照来源：本 Feature、关联分析材料、严格知识校验；未来实施另行建立 Evidence。

## Feature Intake

- Original problem: AgentMentor 的默认多 Gate 流水线与 GPT-5.6 的原生工程编排能力重叠，导致小改动的流程推理成本不成比例。
- User pain point: 开发节奏被路由、前置判断和收尾状态反复打断，无法确定慢来自模型、Skill 还是项目文档质量。
- Capability promise: 提供一份边界清楚的升级前分析，并为后续 vNext 的召回基准、职责取舍和 ADR 提供恢复入口。
- Non-goals: 不把本分析当作性能基准结果；不根据主观体感直接删除 Skill；不引入对 OpenSpec 的运行时依赖。
- Acceptance source: 用户确认的分析范围，以及 `docs/proposals/2026-07-27-agentmentor-vnext-gpt56-workflow-cost-analysis.md`。
- Open questions: vNext 的 Capability 元数据、`agentmentor context` CLI 形态、基准样本及最终保留的 Skill 表面尚未决定。

## Capability Contract

- 本 Feature 为 vNext 的问题定义、历史决策检查和后续实施提供单一入口。
- 分析必须把“已观察到的现象”“由现行规则支持的机制”和“尚待基准验证的推断”分开。
- 历史设计理由、拒绝方案、失败经验和验证证据仍是 vNext 必须保留的长期知识；优化对象是默认编排成本，不是记忆本身。

## Decision Context

### Why

GPT-5.6 的模型能力边界已改变。现有 Start、Vision、Delegation、Readiness 和 Capture 链路曾用于补偿模型遗漏，但现在可能与模型原生推理重复。大版本升级必须先明确这种错位，避免继续在旧流水线上做局部补丁。

### Why Not

不直接删除现有 12 个 Skill，因为缺少对召回准确性、无关文档加载和端到端开发时间的基准，粗暴删减会丢失真正有价值的长期知识能力。也不把全部能力合并为少数更长 Skill，因为那只会把重复路由藏进更大的热路径提示词。

### If Modifying This Area, Check

- 阅读关联分析材料及 ADR-001、ADR-003、ADR-006。
- 区分“模型应自主判断的常规开发动作”与“必须长期保存的工程知识”。
- 对 `agentmentor context` 先建立真实历史改动基准，再宣称召回更快或更准。
- 在创建替代 ADR 前，不修改现行 Gate、Feature、Evidence 或 closeout 语义。

## Current Status

Active。升级问题分析材料已形成；vNext 的目标结构、基准和实施范围尚未决策。

## Links

### Evidence

- None yet.

### Decisions / ADRs

- [ADR-001 Start Gate Before Implementation](../decisions/ADR-001-start-gate-before-implementation.md)
- [ADR-003 Explicit Delegation Decision Before Complex Work](../decisions/ADR-003-explicit-delegation-decision-before-complex-work.md)
- [ADR-006 Skill Progressive Disclosure Boundary](../decisions/ADR-006-skill-progressive-disclosure-boundary.md)
- [ADR-010 AgentMentor vNext 采用事件触发的工程记忆层](../decisions/ADR-010-agentmentor-vnext-event-triggered-memory-layer.md)

### Lessons

- [LL-002 Skill Hot Path Constraints](../lessons/LL-002-skill-hot-path-constraints.md)
- [LL-003 Gate Outcomes Encode Next Action](../lessons/LL-003-gate-outcomes-encode-next-action.md)

### Specs / Plans

- [GPT-5.6 后 AgentMentor 小改动变慢的原因分析](../proposals/2026-07-27-agentmentor-vnext-gpt56-workflow-cost-analysis.md)
- [AgentMentor vNext 重构计划](../proposals/2026-07-28-agentmentor-vnext-refactoring-plan.md)

### Related Features

- [F009 Feature Intake Governance](F009-feature-intake-governance.md)
- [F010 Goal-Driven Feature Flow](F010-goal-driven-feature-flow.md)

### External Context

- [Current workflow](../workflow.md)
- [Current skill index](../skill-index.md)

## Acceptance Criteria

- [x] 形成一份仅分析 GPT-5.6 能力变化与 Skill 设计成本的升级前材料，明确排除历史文档格式问题。
- [x] 材料明确区分已观察事实、设计推断和仍需基准验证的结论。
- [ ] 基于真实历史改动完成 `agentmentor context` 的召回与端到端基准。
- [ ] 经用户确认 vNext 的职责边界后，创建替代旧编排决策的 ADR 和实施计划。

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| vNext 有可恢复的问题定义 | 分析材料说明范围、根因、非结论及设计要求 | [分析材料](../proposals/2026-07-27-agentmentor-vnext-gpt56-workflow-cost-analysis.md) | completed |
| vNext 的性能结论可验证 | 使用真实历史改动建立召回与端到端基准 | None yet | pending |
| vNext 的流程变更有明确授权 | 用户确认取舍后再建立 ADR 与实施计划 | None yet | pending |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-07-27 | active | 用户将此次迭代定义为大版本升级 | [分析材料](../proposals/2026-07-27-agentmentor-vnext-gpt56-workflow-cost-analysis.md) | 完成升级前问题分析，尚未实施。 |

## Patch History

None yet.

## Evidence

本阶段的可验证产物是升级前分析材料与严格知识校验通过；它们证明问题定义已沉淀，不证明 vNext 已实现或性能已改善。

## Recovery Snapshot

- Read first: 本 Feature，然后阅读关联分析材料、ADR-001、ADR-003、ADR-006。
- Current capability state: 已完成问题定义；当前 AgentMentor 行为未变。
- Known risks: 将“减少 Skill 数量”误当作目标，或以缺少基准的数据支持的主观体感替代性能结论。
- Next safe action: 选取 10–20 个真实历史改动，定义 context 召回与端到端开发基准。
- Unblock condition: 用户确认 vNext 设计方向和实施范围。

## Next Step

先设计并验证 `agentmentor context` 的最小召回基准；基准结果出来后，再决定哪些 Gate 删除、合并或降级为按事件触发的能力。
