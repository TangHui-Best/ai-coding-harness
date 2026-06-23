---
id: F010
doc_kind: feature
status: completed
created: 2026-06-18
updated: 2026-06-18
---

# F010: Goal-Driven Feature Flow

## Goal

让 AgentMentor 从默认逐 Feature 设计审批，收敛为 Goal 驱动执行：用户在开始前把需求、目标、边界和验收讲清楚后，Agent 可以在 Goal 范围内连续创建 Feature 记忆并推进实现；只有目标不清、范围越界、重大取舍、验收冲突或 patch churn 时才回问用户。

## Vision Anchor

- 原始请求或来源：用户指出一次项目会话要求“批准 F002 设计”，但该项目中没有 F002，也没有可审批设计；随后明确认可移除默认设计审批 gate，并要求完整落地到本机 Skill。
- 用户痛点或工程问题：逐 Feature 设计审批会打断 Goal 驱动的连续开发，还可能让 Agent 把“应该先创建 Feature/设计”误写成“已有设计等待审批”。
- 期望结果：默认移除 per-Feature design approval；Feature 是工程记忆而不是审批关卡；清晰 Goal 成为授权边界；closeout 门禁继续保留。
- 非目标或边界：不新增复杂状态机；不移除 closeout/knowledge-capture 完成门禁；不让 Hook 接管 Start Gate、Vision Gate 或 Feature ownership 判断。
- Exit Gate 对照来源：本 Feature、EV-013、`tests/test_goal_driven_feature_flow.py`、更新后的 `using-agentmentor` / `start-gate` / `knowledge-capture`。

## Feature Intake

- Original problem: Agent 在缺少 Feature 和设计产物时仍请求用户批准“F002 设计”，说明审批 gate 没有绑定真实 artifact。
- User pain point: 用户无法审批不存在或未展示的设计，而且逐 Feature 暂停会破坏 Codex Goal 下的连续开发体验。
- Capability promise: AgentMentor 明确 Goal 是授权边界，Feature 是工程记忆；默认不逐 Feature 设计审批，只在边界、风险或方向问题上回问用户。
- Non-goals: 不拆出一串新状态，不移除 closeout 门禁，不把 Feature 变成完整 spec/plan/log 容器。
- Acceptance source: 本 Feature、EV-013 和新增回归测试。
- Open questions: 是否后续需要把 Goal Intake 模板化为独立文档，等待真实使用反馈后再决定。

## Capability Contract

- 清晰 Goal 授权范围内，Agent 可以连续拆分和实现多个 Feature。
- 非平凡 Feature 仍必须创建或更新 Feature page，用于恢复、验收、Evidence 和 Patch History。
- 默认不要求用户逐 Feature 审批设计。
- 只有 Goal 缺失/模糊、Feature 越界、重大取舍、验收冲突或 patch churn 时才 ask user。
- closeout/knowledge-capture 门禁继续作为完成声明前的硬约束。

## Current Status

Done。核心 Skill 热路径已加入 Goal-Driven Feature Flow 和 Empty Approval Guard，新增回归测试和 Evidence。

## Links

- [EV-013 Goal Driven Feature Flow](../evidence/EV-013-goal-driven-feature-flow.md)
- [LL-003 Gate Outcomes Should Encode Next Action](../lessons/LL-003-gate-outcomes-encode-next-action.md)

## Acceptance Criteria

- [x] `using-agentmentor` 明确 Goal 是用户授权边界，Feature 是工程记忆，不默认逐 Feature 设计审批。
- [x] `start-gate` 明确 Goal 范围内创建 Feature 是记忆动作，不是用户审批 checkpoint。
- [x] `knowledge-capture` 保留 closeout/completion permission，同时说明 Feature 不是审批关卡。
- [x] 空审批被禁止：不得要求用户批准不存在或未展示的 Feature/design/plan。
- [x] 新增回归测试覆盖上述契约。

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| Goal 驱动替代默认逐 Feature 审批 | Skill 热路径和测试包含 Goal/Feature/approval guard 契约 | [EV-013](../evidence/EV-013-goal-driven-feature-flow.md) | completed |
| closeout 门禁保留 | Knowledge Capture closeout 文案未移除，测试仍覆盖 closeout convergence | [EV-013](../evidence/EV-013-goal-driven-feature-flow.md) | completed |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-06-18 | completed | User approved goal-driven flow and requested local sync | [EV-013](../evidence/EV-013-goal-driven-feature-flow.md) | 默认设计审批移除，Feature 作为记忆保留。 |

## Patch History

None yet

| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |
| --- | --- | --- | --- | --- | --- | --- |

## Evidence

[EV-013 Goal Driven Feature Flow](../evidence/EV-013-goal-driven-feature-flow.md)

## Recovery Snapshot

- Read first: this Feature page, then EV-013.
- Current capability state: completed; Goal-driven Feature execution is now documented in primary Skill text.
- Known risks: Goal Intake is still conversational, not a separate template or validator.
- Next safe action: observe real Goal-driven multi-Feature sessions; if agents still over-ask for approval, add a focused routing fixture or project rule.
- Unblock condition: not blocked.

## Next Step

在真实项目中观察是否仍出现“批准不存在的 Fxxx 设计”或“每个 Feature 都停下审批”的行为；若复发，优先补 routing fixture 和 skill tests，而不是新增状态机。
