---
id: LL-006
doc_kind: lesson
status: active
scope: project
feature_refs: [docs/features/F005-session-recovery-hooks.md]
applies_to: [opencode-plugin, hook-runtime, session-recovery, precompact, platform-contracts]
created: 2026-05-31
updated: 2026-05-31
---

# LL-006: Platform Hooks Must Use Native Context Channels

## Pitfall

把不同 Agent 平台的 hook 事件按名字做一层简单映射，会制造“配置看起来完整、实际能力没有闭合”的假象。OpenCode 的 `experimental.session.compacting` 不是 Codex 式的 `PreCompact` + `SessionStart` 生命周期组合；它在同一个 hook 调用里通过 `output.context` 注入压缩上下文。

如果适配层只在 OpenCode compaction 时调用 `pre-compact`，它最多写出本地恢复快照，却不会把恢复材料交给 OpenCode 的压缩流程。用户会以为已经安装了 session recovery hook，但上下文压缩后仍然无法自动恢复。

## Root Cause

根因是把 Harness 的归一化事件模型误当成平台真实执行模型。归一化事件只适合作为内部 runner 的稳定接口，不应该覆盖平台自己的数据流边界。

OpenCode 的关键差异有两点：

- 会话标识字段是 `sessionID`，不是 `session_id` 或 `sessionId`。
- compaction 恢复上下文必须在 `experimental.session.compacting(input, output)` 里写入 `output.context`，而不是等待一个新会话的 `session.created` 再读取。

旧适配同时漏掉了这两点，导致 OpenCode 快照落回项目级 `latest.md`，并且没有任何自动注入路径。

## Trigger

出现以下信号时，先重新核对平台 hook contract，而不是继续调 runner 逻辑：

- 平台文档或源码提供了 `output` 参数、context push、prompt append、permission response 之类的原生返回通道。
- 适配代码只消费 `input`，没有消费平台要求的 `output` 或返回值。
- 平台字段命名不符合常见 camelCase 或 snake_case，例如 `sessionID`。
- 适配把启动事件当作恢复事件使用，可能让新独立会话读取旧会话上下文。
- 手动运行 runner 通过，但真实平台流程没有出现预期上下文。

## Fix

F005.2 对 OpenCode 适配做了收口：

- `harness_hook.py` 的 `session_id_from_payload` 识别 `sessionID`、`conversationID`、`threadID`。
- `opencode-plugin.example.ts` 移除 `session.created` 恢复映射，避免新会话污染。
- `experimental.session.compacting(input, output)` 先调用 `pre-compact` 保存同 session 快照，再调用 `session-start` 读取同 session 快照。
- 当 `session-start` 返回 `additional_context` 时，把内容写入 OpenCode 原生 `output.context.push(...)`。
- 插件示例对命令失败和 JSON 解析失败 fail open，仅在 runner 明确返回 `decision=block` 时阻断。

F005.6 补充修正 OpenCode Stop 适配：

- `session.idle` 是 SDK 全局事件类型，应通过插件 `event(input)` 入口过滤 `input.event.type`。
- 不要把 `"session.idle"` 注册成直接 hook key；当前 `@opencode-ai/plugin` `Hooks` 类型只把 `experimental.session.compacting` 这类触发器暴露为直接 hook。
- `session.idle` 只提供 `sessionID`，Stop closeout 检查还需要最后的 assistant 文本；适配层应通过 `client.session.messages` 读取最近消息并传入 `last_assistant_message`。

## Protection

新增保护测试：

```text
tests/test_harness_hook.py::HarnessHookTests::test_pre_compact_accepts_opencode_session_id_shape
tests/test_skill_progressive_disclosure.py::SkillProgressiveDisclosureTests::test_opencode_hook_example_uses_compaction_context_output
tests/test_skill_progressive_disclosure.py::SkillProgressiveDisclosureTests::test_opencode_stop_uses_event_hook_for_session_idle
tests/test_skill_progressive_disclosure.py::SkillProgressiveDisclosureTests::test_opencode_stop_fetches_latest_assistant_message
```

后续新增或修改平台 hook 适配时，至少要验证：

1. 平台实际事件名、文件位置、schema 和 matcher。
2. 平台输入字段命名，尤其 session/thread/conversation id。
3. 平台是否要求通过 `output` 参数、返回值或特定 JSON shape 注入上下文。
4. 启动事件、恢复事件、压缩事件是否属于同一生命周期，不能只按名字猜测。
5. 安装失败、运行失败、解析失败是否 fail open；明确规则失败才允许 block。

## Source

本 Lesson 来自 F005.2 的 OpenCode 适配复审。用户在 Codex hook 经多次修复才生效后，要求重新审视 OpenCode 适配。复审发现旧示例未使用 OpenCode 官方 `experimental.session.compacting` 的 `output.context` 通道，也没有识别 OpenCode 的 `sessionID` 字段。

相关记录：

- [F005 Session Recovery Hooks](../features/F005-session-recovery-hooks.md)
- [EV-008 Session Recovery Hooks](../evidence/EV-008-session-recovery-hooks.md)

## Principle

Harness 可以有归一化 runner，但平台适配必须尊重平台自己的上下文通道。hook 能力是否成立，不看事件名是否能映射，而看平台在真实生命周期里是否消费了我们写入的内容。
