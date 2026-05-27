---
id: ADR-006
doc_kind: adr
status: accepted
scope: project
feature_refs: [docs/features/F002-canonical-harness-artifact-placement.md]
decision_area: harness-skill-design
created: 2026-05-27
updated: 2026-05-27
---

# ADR-006: Skill Progressive Disclosure Boundary

## Context

Harness skill 最近的迭代同时面对两个真实问题：

- Skill 文本过长会增加上下文成本，甚至被误认为导致会话卡住。
- Skill 文本过度瘦身会隐藏关键行为约束，让 Agent 在真实开发中走错路径。

2026-05-26 的 baseline 将大量细则拆到 `references/`，并新增 closeout convergence，方向是正确的：脚本默认执行而不读源码，细节按需加载，避免递归 closeout。但是后续真实使用发现，一些不可延迟的执行约束也被下沉了，例如 canonical Feature 路径、Entry/Exit Gate、Feature 创建触发条件、Patch Churn Check 等。

这导致 Agent 可能先沿用 Superpowers spec/plan 命名与路径，再靠 validator 暴露错误。Validator 能防止错误合入，但不能指导 Agent 在第一步做对。

## Decision

Harness skill 采用三层渐进式加载边界：

1. 主 `SKILL.md` 承载热路径约束。
   - 触发条件。
   - 阻塞条件。
   - 允许/禁止的下一步行动。
   - artifact canonical placement。
   - Entry Gate / Exit Gate 最低条件。
   - completion claim permission。
   - 非 tiny bugfix attribution 与 Patch History。
   - patch churn 的暂停与归零审视触发。

2. `references/` 承载细则和扩展判断。
   - 决策矩阵。
   - 完整检查表。
   - row-by-row readiness。
   - fallback search patterns。
   - 示例和 fixtures。
   - 边界案例。

3. `scripts/` 承载确定性校验。
   - Agent 默认知道如何执行脚本。
   - 不为了学习规则而读取脚本源码。
   - 只有在调试失败、编辑脚本、审查脚本行为或解释脚本行为时才读取源码。

对应约束：

- Progressive disclosure 只能延迟加载细节，不能延迟加载会改变第一行动的规则。
- Validator 是最后防线，不是写入期决策入口。
- 主 `SKILL.md` 可以短，但必须足够让 Agent 在不读取 reference 的情况下避免错误开始。

## Alternatives

- 全量回滚到长 Skill：拒绝。长文本会提高每次加载成本，也更容易让不同 gate 互相递归，重新引入 2026-05-26 试图解决的问题。
- 继续把所有细节都放进 reference：拒绝。真实任务中 Agent 不一定会打开 reference；关键规则会变成“失败后才知道”。
- 只依赖 `knowledge_check.py --strict`：拒绝。校验可以阻止错误合入，但不能替代 Start Gate 和 Knowledge Capture 的写入前判断。
- 把所有规则提升到 `AGENTS.md`：拒绝。`AGENTS.md` 应该只承载跨任务、项目级、行为性且值得注意力成本的规则。具体 Skill 分层属于 Harness 设计决策，优先由 ADR 和 Skill 自身承载。

## Consequences

收益：

- Agent 在真实开发中更容易第一步就做对，而不是靠后置校验纠偏。
- Skill 仍然保持 progressive disclosure，不需要每次加载完整矩阵和案例。
- 脚本继续保持 execute-first，避免把源码阅读变成默认成本。
- 未来 Skill 瘦身有明确判断标准：移走细节，不移走热路径约束。

代价：

- 主 `SKILL.md` 会比极限瘦身版本更长。
- 一些规则会在主 Skill 和 reference 中有意重复，但重复的是行为边界，不是长篇案例。
- 需要维护结构性测试，确保热路径约束不会在后续重构中消失。

## Evidence

- [LL-002 Skill Hot Path Constraints Must Stay Visible](../lessons/LL-002-skill-hot-path-constraints.md)
- [EV-004 Hot Path Harness Constraints](../evidence/EV-004-hot-path-harness-constraints.md)
- [EV-005 Skill Iteration Learning Docs](../evidence/EV-005-skill-iteration-learning-docs.md)
- `tests/test_skill_progressive_disclosure.py::test_hot_path_constraints_remain_in_primary_skill_text`
- Commit `a0b5411 fix: restore harness hot-path constraints`
