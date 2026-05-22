---
id: F001
doc_kind: feature
status: completed
created: 2026-05-22
updated: 2026-05-22
---

# F001: Closeout Entry And Vision Anchor Validation

## Goal

让 Harness closeout 检查成为稳定的完成声明闸门：任何非平凡工程工作在声明完成前，都必须显式说明入口门禁状态和可恢复的 Vision Anchor，避免 Agent 只在事后补文档或依赖聊天记录恢复目标。

## Vision Anchor

- 原始请求或来源：用户要求从全局视角优化 Harness，优先把 `harness_closeout_check.py` 变成机器可拦截的稳定机制，而不是针对特定场景补关键词。
- 用户痛点或工程问题：Agent 可能调用了部分 Harness skill，但没有让入口门禁和 Vision Anchor 约束行动，导致缺少 Feature/Evidence 时仍然进入实现或完成声明。
- 期望结果：closeout block 必须包含通用的 `Entry Gate` 和 `Vision Anchor` 状态；脚本在完成声明被允许时阻断缺失、空洞、retroactive 未补救、或未说明原因的情况。
- 非目标或边界：不让脚本推断具体任务类型、不写死 runner/CLI/资产生命周期等场景关键词、不用脚本替代 Start Gate 的人工判断。
- Exit Gate 对照来源：本 Feature 的 Acceptance Criteria、更新后的 `harness_closeout_check.py` 测试、`harness-knowledge-capture` final response contract。

## Current Status

Done。closeout checker 已经对 Entry Gate、Vision Anchor、Patch Churn Review 做结构化阻断，root 脚本与 bundled skill 脚本保持一致，技能契约已同步。

## Links

- [ADR-001 Start Gate Before Implementation](../decisions/ADR-001-start-gate-before-implementation.md)
- [EV-001 Closeout Entry Anchor Validation](../evidence/EV-001-closeout-entry-anchor-validation.md)

## Acceptance Criteria

- [x] `harness_closeout_check.py` 要求 closeout block 包含 `Entry Gate` 和 `Vision Anchor` 字段。
- [x] 当 `Completion claim allowed: yes` 时，`Entry Gate` 不能是 `missing`，`Vision Anchor` 不能缺失或空洞。
- [x] `Vision Anchor: not triggered` 必须带有明确原因，允许 tiny/routine 场景显式豁免。
- [x] `Entry Gate: retroactive` 必须有 Feature 或 Evidence 补救记录，不能静默通过。
- [x] `harness-knowledge-capture` 的 Final Response Contract 与脚本字段保持一致。
- [x] 测试覆盖通过、Harness knowledge artifacts 通过校验。

## Patch History

None yet

| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |
| --- | --- | --- | --- | --- | --- | --- |

## Evidence

[EV-001 Closeout Entry Anchor Validation](../evidence/EV-001-closeout-entry-anchor-validation.md)

## Next Step

无。后续若发现 closeout block 仍能绕过关键完成声明，可在本 Feature 的 Patch History 中记录补丁并评估是否需要 Lesson。
