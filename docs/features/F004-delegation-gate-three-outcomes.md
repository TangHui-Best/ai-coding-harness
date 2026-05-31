---
id: F004
doc_kind: feature
status: completed
created: 2026-05-30
updated: 2026-05-30
---

# F004: Delegation Gate Three Outcomes

## Goal

将 Delegation Gate 从授权状态机收口为主 Agent 的三值决策：`single_agent`、`delegate`、`blocked`。

## Vision Anchor

- Original request or source: 用户指出 Delegation Gate 不应围绕授权状态展开，而应由主 Agent 判断是否需要 subagent；除非用户明确要求不用或明确要求使用。
- User pain point or engineering problem: 原有取值过多，把授权、建议、要求、条件状态混在主决策里，容易降低判断准确性，也让 Start Gate 和 Readiness Dashboard 难以区分“已决定单 Agent”与“缺失决策”。
- Desired outcome: Delegation Gate 只表达主 Agent 下一步判断；是否需要请求权限是 `delegate` 之后的执行细节，不再作为主要枚举。
- Non-goals or boundaries: 不新增多 Agent runtime，不自动 spawn subagent，不改变 Stop hook 作为唯一默认 Hook 的策略。
- Exit Gate source: Delegation Gate skill、Start Gate readiness rule、Readiness Dashboard compact output、ADR-003 更新、EV-007 验证结果。

## Current Status

Done. Delegation Gate、Start Gate、Vision Gate、Readiness Dashboard 和 using-harness routing 已统一到三值决策模型。

## Links

- [ADR-003 Explicit Delegation Decision Before Complex Work](../decisions/ADR-003-explicit-delegation-decision-before-complex-work.md)
- [LL-003 Gate Outcomes Should Encode Next Action](../lessons/LL-003-gate-outcomes-encode-next-action.md)
- [EV-007 Delegation Gate Three Outcomes](../evidence/EV-007-delegation-gate-three-outcomes.md)
- [F005 Session Recovery Hooks](F005-session-recovery-hooks.md)

## Acceptance Criteria

- [x] Delegation Gate 只输出 `single_agent`、`delegate`、`blocked` 三个主决策。
- [x] `single_agent` 表示主 Agent 明确决定独立完成，并必须给出具体理由。
- [x] `delegate` 表示主 Agent 判断应该使用实现 subagent、独立 reviewer 或两者；用户或平台权限只是后续执行约束。
- [x] `blocked` 表示必要的 delegation/review/permission/context/platform support 不可用。
- [x] Start Gate 不再接受旧授权式枚举作为有效 Delegation decision。
- [x] Readiness Dashboard 保留 `missing`，用于表达复杂任务没有显式 Delegation Gate 决策，避免把缺失证据降级成 self-review。

## Patch History

None yet

| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |
| --- | --- | --- | --- | --- | --- | --- |

## Evidence

[EV-007 Delegation Gate Three Outcomes](../evidence/EV-007-delegation-gate-three-outcomes.md)

## Next Step

Done in F005: SessionStart / PreCompact recovery hooks use a small action surface and keep permission/source/recovery details outside the main hook outcome.
