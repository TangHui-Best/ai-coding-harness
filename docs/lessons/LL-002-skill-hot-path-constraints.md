---
id: LL-002
doc_kind: lesson
status: active
scope: project
feature_refs: [docs/features/F002-canonical-harness-artifact-placement.md]
applies_to: [harness-skills, skill-design, progressive-disclosure, knowledge-capture, start-gate, using-harness]
created: 2026-05-27
updated: 2026-05-27
---

# LL-002: Skill Hot Path Constraints Must Stay Visible

## Pitfall

在优化 Skill 体积和会话稳定性时，Agent 容易把规则拆得过细，把“会改变第一步行动”的硬约束一起下沉到 `references/`、validator 或后置校验里。这样主 `SKILL.md` 看起来更轻，但真实开发时 Agent 可能已经按旧路径开始行动，直到校验失败才发现写入位置、Feature 归属或完成声明条件错了。

这次 Harness skill 迭代中，`docs/features/Fxxx-slug.md` 的 canonical Feature 规则虽然存在于 `using-harness`、ADR 和 validator 中，但 `harness-knowledge-capture`、`harness-start-gate` 等写入期热路径弱化后，Agent 仍可能沿用 Superpowers 的 `docs/superpowers/**` spec/plan 习惯，把“设计/计划文件”误当成 Harness Feature memory。

## Root Cause

根因不是 progressive disclosure 本身，而是分层标准不够明确。我们把“脚本默认不读源码”“reference 延迟加载”“主 Skill 保持轻量”这三条最佳实践机械合并，缺少一条反向约束：

热路径约束不能延迟加载。

只要某条规则会改变以下任一行为，它就必须留在主 `SKILL.md` 中：

- 是否可以开始实现。
- 是否必须停下来澄清、检索、建 Feature、建 ADR 或跑 Gate。
- 官方 artifact 应该写到哪里。
- 是否允许使用完成、ready、verified、handoff 等声明。
- 非 tiny bugfix 是否需要 Feature attribution 和 Patch History。
- 重复补丁是否必须触发 Patch Churn Review 或 Vision Gate。

## Trigger

出现以下信号时，应怀疑 Skill 瘦身过度：

- Agent 在真实任务中遵守了 validator，但写入前没有主动选择正确 artifact 路径。
- 主 `SKILL.md` 只说“读取 reference”，但没有写清楚阻塞条件和写入位置。
- 规则只有失败后才暴露，例如 `knowledge_check.py --strict` 才发现官方 Harness artifact 写进了 legacy 路径。
- 同一个约束在 ADR、Evidence、测试里存在，但写入期 Skill 没有直接提醒。
- 为了避免会话卡住，删除了 Entry Gate / Exit Gate / completion permission 这类行为边界。

## Fix

保留 2026-05-26 引入的 progressive disclosure 和 closeout convergence，但把以下规则恢复到主 Skill 热路径：

- `using-harness/SKILL.md`：Entry Gate、Exit Gate、Core Rule、Superpowers spec/plan 与 Harness artifact 的边界。
- `harness-knowledge-capture/SKILL.md`：Artifact Placement、Templates、Stable IDs、Feature page 创建/更新触发条件。
- `harness-start-gate/SKILL.md`：Task Classes、Risk Triggers、Patch Churn Check。
- `FEATURE.md` 模板：保存路径提示，防止复制模板时丢失位置约束。

同时新增 `tests/test_skill_progressive_disclosure.py::test_hot_path_constraints_remain_in_primary_skill_text`，防止未来再次把这些热路径约束完全藏进 reference。

## Protection

- 任何 Skill 瘦身都必须先分类：热路径约束、细则矩阵、案例、脚本执行说明、脚本源码。
- 热路径约束留在主 `SKILL.md`；细则矩阵和案例放到 `references/`；脚本源码默认不读，只保留执行命令和失败时读取源码的规则。
- 如果某条规则的缺失会让 Agent 写错路径、跳过 Gate、误用完成声明或错过 Feature attribution，它不能只存在于 reference、ADR、Evidence 或 validator。
- 对关键热路径约束写结构性测试，测试目标不是文本长度，而是防止行为边界消失。
- validator 只能作为最后防线，不能替代写入前的 Skill 决策。

## Source

该 Lesson 来自 F002 的后续修复：

- [F002 Canonical Harness Artifact Placement](../features/F002-canonical-harness-artifact-placement.md)
- [ADR-005 Canonical Harness Artifact Placement](../decisions/ADR-005-canonical-harness-artifact-placement.md)
- [EV-004 Hot Path Harness Constraints](../evidence/EV-004-hot-path-harness-constraints.md)
- Commit `a0b5411 fix: restore harness hot-path constraints`

## Principle

Progressive disclosure 降低的是上下文成本，不是行为约束的可见性。凡是会改变 Agent 第一行动、写入位置、Gate 阻塞、完成声明权限或验收边界的规则，都必须在主 `SKILL.md` 热路径中可见。
