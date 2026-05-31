---
id: LL-003
doc_kind: lesson
status: active
scope: project
feature_refs: [docs/features/F004-delegation-gate-three-outcomes.md]
applies_to: [harness-skills, gate-design, hook-design, delegation-gate, start-gate, readiness-dashboard, session-recovery]
created: 2026-05-30
updated: 2026-05-30
---

# LL-003: Gate Outcomes Should Encode Next Action

## Pitfall

设计 gate 或 hook 时，Agent 容易把主结果枚举做成流程状态机，把权限状态、建议强度、执行阶段、失败解释和残余风险都塞进同一个 outcome。这样看似信息更完整，实际会让判断面变宽，降低命中准确性。

Delegation Gate 原先把 `not needed`、`ask user`、`authorized`、`declined`、`required`、`blocked`、`conditional` 混在同一层。这里面有些是主 Agent 的下一步行动，有些是权限来源，有些是风险说明，有些是收尾状态。结果是 Agent 很难稳定回答最关键的问题: 我现在应该自己做、委托做，还是停下。

## Root Cause

根因是没有区分两类信息:

- 主决策: 下一步行动是否改变。
- 附属字段: 为什么这样判断、权限来自哪里、目标是谁、残余风险是什么、是否需要在平台上请求授权。

当这些信息混在同一个 outcome 里，gate 会被迫同时承担路由、授权、解释、审计和 readiness 汇总。枚举越多，主 Agent 越容易在语义相近的值之间摇摆，也越容易把缺失决策误判成“可以继续”。

## Trigger

出现以下信号时，应怀疑 gate 或 hook 的 outcome 设计正在膨胀:

- outcome 超过 3-4 个，并且多个值不会真正改变下一步行动。
- outcome 同时包含动词状态和解释状态，例如 ask、authorized、declined、required、conditional。
- 缺失信息需要用一个业务 outcome 伪装，而不是由聚合层显式报告 `missing`。
- 用户或平台权限被建模为主决策，而不是 `delegate` 或同类主决策之后的执行约束。
- readiness、closeout、hook 和 skill 各自发明相近但不一致的状态词。

## Fix

F004 将 Delegation Gate 收口为三个主 Agent 决策:

- `single_agent`: 主 Agent 明确决定独立完成，并给出具体理由。
- `delegate`: 主 Agent 判断应该使用实现 subagent、独立 reviewer 或两者。
- `blocked`: 需要的 delegation、review、permission、context 或 platform support 不可用。

权限来源、触发原因、delegation target、用户约束和残余风险被移到独立字段。这样主 outcome 只回答“下一步行动是什么”，而不是试图承载整段执行故事。

## Protection

- 主 outcome 只保留会改变下一步行动的值，默认收口到 3 个，最多 4 个。
- 授权、来源、原因、对象、残余风险、证据等级和执行细节使用独立字段，不进入主 outcome。
- `missing` 只能用于 Readiness Dashboard 这类聚合/检查层，表示没有证据；不能把缺失证据降级成 `single_agent` 或其他业务决策。
- 对关键 gate 写结构性测试，固定主 outcome 集合，防止未来回流成授权状态机。
- 当新增 Hook 或 Gate 时，先问“这个值是否会改变 Agent 下一步行动”。如果不会，它应该是字段、note、risk 或 Evidence，而不是 outcome。

## Source

本 Lesson 来自 F004 的 Delegation Gate 收口:

- [F004 Delegation Gate Three Outcomes](../features/F004-delegation-gate-three-outcomes.md)
- [ADR-003 Explicit Delegation Decision Before Complex Work](../decisions/ADR-003-explicit-delegation-decision-before-complex-work.md)
- [EV-007 Delegation Gate Three Outcomes](../evidence/EV-007-delegation-gate-three-outcomes.md)

## Principle

Gate outcome 不是日志字段，也不是权限状态机。它应该表达主 Agent 的下一步行动判断。会改变行动的东西进入 outcome；只解释行动的东西进入字段。
