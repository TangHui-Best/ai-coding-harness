---
id: F001
doc_kind: feature
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

<!-- Save as docs/features/F001-slug.md. Do not place official Harness Features under docs/superpowers/**. -->
<!-- Filename recall rule: use Fxxx-<domain>-<capability>-<trigger>.md, usually 4-7 English words. The filename should carry domain, capability, and likely trigger terms without becoming a sentence; extra recall hints belong in docs/features/INDEX.md. -->

# F001: <Name>

## Goal

用中文说明这个 Feature 要解决的用户问题或工程问题。

## Vision Anchor

- 原始请求或来源：
- 用户痛点或工程问题：
- 期望结果：
- 非目标或边界：
- Exit Gate 对照来源：

## Feature Intake

创建或重大更新 Feature 前，必须先回答这些问题；若无法回答，Agent 应先反问而不是写入长期记忆。

- Original problem:
- User pain point:
- Capability promise:
- Non-goals:
- Acceptance source:
- Open questions:

## Capability Contract

用中文列出这个 Feature 当前承诺提供的能力边界。只写能力，不写实施流水。

- 

## Current Status

使用稳定状态值：Draft | In Progress | Blocked | Done | Archived。必要时用中文补充当前状态说明。

## Links

链接相关 spec、plan、discussion、ADR、Lesson、Evidence、PR 或 commit。链接路径和文件名保持原样。

## Acceptance Criteria

- [ ] 用中文写清楚可验收标准

## Acceptance Map

把能力声明、验收标准和证据连起来。`ready_for_review`、`done` 或 `completed` 状态不得留下 `TBD`、`None` 或空 Evidence。

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
|  |  |  |  |

## State Timeline

记录状态变化，不要覆盖掉关键历史。详细日志放 Evidence 或 Handoff。

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| YYYY-MM-DD | draft | Feature created | This Feature | Initial state |

## Patch History

记录 Feature 被认为完成或验收后的 follow-up fixes。Patch id 使用 `F001.1`、`F001.2`、`F001.3` 这类格式。若暂时没有后续修复，写 `None yet`。

| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |
| --- | --- | --- | --- | --- | --- | --- |

<!-- 当本表达到 3 行时，继续补丁前必须新增 `## Patch Churn Review`。 -->

## Evidence

用中文记录能证明当前状态的验证证据，命令、日志和路径保持原文。

## Recovery Snapshot

给未来 Agent 的最短恢复入口。它应该能让下一个会话在不读完整聊天记录的情况下继续判断。

- Read first:
- Current capability state:
- Known risks:
- Next safe action:
- Unblock condition:

## Next Step

用中文写下一步最小可行动作。
