---
id: LL-005
doc_kind: lesson
status: active
scope: project
feature_refs: [docs/features/F005-session-recovery-hooks.md]
applies_to: [session-recovery, hook-runtime, precompact, sessionstart, context-isolation, codex-plugin]
created: 2026-05-31
updated: 2026-05-31
---

# LL-005: Session Recovery Must Be Session-Scoped

## Pitfall

把 `PreCompact` 保存的恢复材料建模成项目级 `latest.md`，再让 `SessionStart` 无条件读取，会让“同一会话压缩后恢复”和“同一项目中新开独立会话”混在一起。

这会制造隐蔽的上下文污染：用户新开一个会话想做独立任务时，Agent 可能自动读入上一个会话的 handoff，从而把旧目标、旧约束或旧判断带进新任务。

## Root Cause

根因是恢复状态的隔离边界选错了。

`PreCompact` / `SessionStart` 配合解决的是会话生命周期内的上下文丢失，而不是项目级记忆恢复。项目级记忆应该来自 canonical Harness docs，例如 Feature、ADR、Lesson、Evidence；压缩恢复材料只是 runtime context。

旧实现把恢复入口固定为：

```text
.harness/session-recovery/latest.md
```

这只有项目维度，没有会话维度，也没有区分 `SessionStart` 的来源。结果是 `startup`、`resume`、`clear` 和 `compact` 都可能读取同一份旧材料。

## Trigger

出现以下信号时，应怀疑 session recovery 的隔离边界错误：

- `SessionStart(startup)` 会读取压缩前的 handoff。
- 新开独立会话时，Agent 自动带入上一个任务的目标或约束。
- 恢复文件路径只有 `latest.md`，没有 `session_id`。
- hook matcher 覆盖 `startup|resume|clear|compact`，但 runner 内没有 source 检查。
- 测试只验证“有 snapshot 就能读”，没有验证“不同 session 不能读”。

## Fix

F005.1 将自动注入恢复改为同会话 compact 专用：

- `PreCompact` 写入：

```text
.harness/session-recovery/by-session/<session_id>.md
```

- `latest.md` 仍可更新，但只作为人工排查入口，不参与自动注入。
- `SessionStart` 只有在 `source=compact` 时才尝试恢复。
- `SessionStart(compact)` 只读取当前 `session_id` 对应的 snapshot。
- Codex `SessionStart` 输出改为官方 `hookSpecificOutput.additionalContext` 结构。
- Codex `SessionStart` matcher 收窄为 `compact`，减少无意义触发。

## Protection

以后设计恢复类 hook 时，必须同时验证三条边界：

1. **生命周期边界**：恢复只服务于中断/压缩后的同一会话，不默认服务于新任务启动。
2. **身份边界**：自动注入必须绑定 `session_id` 或等价会话标识。
3. **来源边界**：只有 `source=compact` 这类明确恢复来源才允许注入 runtime context。

已新增/更新的保护测试覆盖：

- `PreCompact` 写入 `by-session/<session_id>.md`。
- `SessionStart(compact)` 读取同一 session snapshot。
- `SessionStart(startup)` 不读取旧 `latest.md`。
- `SessionStart(compact)` 不读取其他 session snapshot。
- Codex 输出 `hookSpecificOutput.additionalContext`。
- Codex `SessionStart` matcher 必须是 `compact`。

## Source

本 Lesson 来自 F005.1 修复：

- 用户明确指出：上下文压缩后会继续当前会话，而新开独立会话不能读取旧会话压缩材料。
- 旧实现存在项目级 `latest.md` 污染风险。
- 修复记录在 [F005 Session Recovery Hooks](../features/F005-session-recovery-hooks.md) 的 Patch History。
- 验证记录在 [EV-008 Session Recovery Hooks](../evidence/EV-008-session-recovery-hooks.md)。

## Principle

Runtime recovery 不是项目记忆。项目记忆可以按项目共享，runtime recovery 必须按会话隔离。能帮助“恢复当前会话”的材料，如果无条件带入“新任务启动”，就会从恢复能力变成上下文污染源。
