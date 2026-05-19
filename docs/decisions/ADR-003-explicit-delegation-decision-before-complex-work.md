---
id: ADR-003
doc_kind: adr
status: accepted
scope: project
feature_ids: []
decision_area: harness-workflow
created: 2026-05-19
updated: 2026-05-19
---

# ADR-003: Explicit Delegation Decision Before Complex Work

## Context

当前 Harness 已经有 `harness-delegation-gate`，但它的触发语义偏软：复杂任务只有在用户显式提到 subagent、parallel agents 或 independent review 时才稳定触发。对于长时间、跨模块、可拆分或高风险任务，这会让 Agent 默默退回单 Agent 工作，直到中途遇到授权问题才停住。

真正需要强化的不是“默认派 subagent”，而是“复杂任务开始前必须显式判断是否需要 delegation”。平台仍然可能要求用户授权才能实际 spawn subagent，因此 Harness 不能把 gate 本身当成授权。

## Decision

对 `non-trivial` 或 `high-risk` 工作，Start Gate 在返回 `ready` 前必须包含明确的 Delegation decision。

Delegation Gate 默认产生显式决策，而不是默认派发 subagent。有效决策可以是 `not needed`、`ask user`、`authorized`、`declined`、`blocked` 或 `conditional`，但不能把缺失决策当作 `not needed`。

当用户描述长时间或 unattended 任务时，`using-harness` 必须提前路由到 Delegation Gate，在任务中途卡住前请求必要预授权。

Readiness Dashboard 在收尾时反向检查：如果复杂任务没有明确 Delegation Gate 决策，应标记 `missing`，不能因为实现已经完成就默默降级为 self-review。

## Alternatives

- 默认自动 spawn subagent：拒绝。平台和用户授权边界仍然存在，而且并非所有复杂任务都能有效并行。
- 只在用户明确说 subagent 时触发：拒绝。这正是当前失效点，会让复杂任务默认滑向单 Agent。
- 把规则写进 `AGENTS.md`：暂不采用。本次目标是修复 Harness skill 自身的触发约束；项目级规则可以作为后续建议，但不属于 skill 包本身。
- 新增完整 runtime 编排：拒绝。当前缺口是 gate 语义，而不是多 Agent runtime。

## Consequences

复杂任务的开工成本会略微增加，因为 Agent 必须先说明 delegation 决策。但这能减少长任务中途等待授权、复杂任务无独立审视、以及收尾阶段才发现缺少 reviewer 记录的问题。

这项决策保持了两个边界：Harness 强制“做决策”，但不强制“派 subagent”；实际 subagent 使用仍以用户授权和平台能力为准。

## Evidence

- `skills/harness-start-gate/SKILL.md`
- `skills/harness-delegation-gate/SKILL.md`
- `skills/using-harness/SKILL.md`
- `skills/harness-readiness-dashboard/SKILL.md`
- `tests/test_delegation_gate_policy.py`
