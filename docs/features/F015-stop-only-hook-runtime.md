---
id: F015
doc_kind: feature
status: completed
created: 2026-06-27
updated: 2026-06-27
invalidates:
  - F005
---

# F015: Stop Only Hook Runtime

## Goal

将 AgentMentor optional hook runtime 收敛为 Stop-only completion-claim guard，移除默认 `pre-compact` / `session-start` session recovery 能力。

## Vision Anchor

- 原始请求或来源：用户指出当前 pre-compact 只能从平台 payload / transcript tail 被动提取文本，和 Codex、Claude Code 等平台自带上下文压缩能力重叠，价值不稳定。
- 用户痛点或工程问题：session recovery hook 牵涉多个平台适配、诊断、文档和测试，但不能生成 Agent 主动判断后的高质量结构化 handoff，容易成为复杂控制面。
- 期望结果：默认 hook 示例和 runner 只保留 Stop completion-claim checking；session recovery 相关事件、恢复文件和 compaction diagnostics 从当前能力中移除。
- 非目标或边界：不移除 Stop hook；不删除历史 Feature、Evidence、Lesson；不禁止用户显式要求 handoff；不把平台 compaction 纳入 AgentMentor 默认 hook 责任。
- Exit Gate 对照来源：本 Feature、EV-022、hook runner tests、diagnostics tests、progressive disclosure tests、strict knowledge check。

## Feature Intake

- Original problem: pre-compact/session-start recovery 不能产生比平台 compact 更高质量的恢复材料。
- User pain point: 默认启用一条收益不稳定的 runtime recovery 路径，会增加平台适配和维护复杂度。
- Capability promise: AgentMentor optional hook runtime 默认只负责 Stop-time completion claim guard。
- Non-goals: 不移除 explicit handoff 概念；不删除历史 session recovery 经验；不把 Stop hook 改成唯一完成门禁。
- Acceptance source: 用户确认移除 pre-compact/session-start 相关功能的当前请求。
- Open questions: 是否未来彻底移除 Stop hook，暂不处理。

## Capability Contract

- `agentmentor_hook.py` 只接受 `stop` 和实验性的 `post-tool-use` 事件，不再接受 `pre-compact` 或 `session-start`。
- Codex、Claude Code、OpenCode hook examples 默认只 wire Stop。
- Root `hooks.json` 和 nested `hooks/hooks.json` 只声明 Codex Stop hook。
- `hook_diagnostics.py` 只做 Stop runner smoke，不再扫描 Codex compaction logs 或 `.agentmentor/session-recovery` artifact。
- README、INSTALL、quickstart 和 `using-agentmentor` 不再宣传 default session recovery hooks。
- F005 标记为 superseded，并指向 F015。

## Decision Context

### Why

AgentMentor hook runtime 的高价值边界是完成声明约束：Agent 如果说完成，就必须有 closeout 和 Evidence 状态。相比之下，pre-compact/session-start recovery 当前只能搬运平台 payload 或 transcript tail，不能让 Agent 在压缩前主动生成结构化 handoff，因此不能稳定提供比平台 compaction 更好的决策恢复材料。

### Why Not

没有继续优化 pre-compact handoff，因为 hook runner 不是 Agent 本体，不能可靠触发 Agent 在压缩前重新判断目标、下一步、风险和证据。没有删除 Stop hook，因为 Stop hook 的完成声明检查是可验证、低语义裁量、与 AgentMentor 第一性原理高度一致的边界。

### If Modifying This Area, Check

- 检查 `agentmentor_hook.py` 的 event choices 是否仍然不包含 `pre-compact` / `session-start`。
- 检查 Codex、Claude Code、OpenCode 示例是否只 wire Stop。
- 检查 root `hooks.json` 和 `hooks/hooks.json` 是否保持一致。
- 检查 README、INSTALL、quickstart、`using-agentmentor` 是否没有把 session recovery 作为现役默认能力宣传。
- 运行 hook tests、diagnostics tests、progressive disclosure tests、strict knowledge check 和 F015 Feature Index 本地校验。

## Current Status

Completed。默认 optional hook runtime 已收敛为 Stop-only，session recovery hooks 被 F015 替代并从当前 runner、配置、诊断、文档和测试中移除。

## Links

### Evidence

- [EV-022 Stop Only Hook Runtime](../evidence/EV-022-stop-only-hook-runtime.md)

### Decisions / ADRs

- None.

### Lessons

- [LL-005 Session Recovery Must Be Session-Scoped](../lessons/LL-005-session-recovery-must-be-session-scoped.md)
- [LL-006 Platform Hooks Must Use Native Context Channels](../lessons/LL-006-platform-hooks-native-context-channels.md)
- [LL-007 Hook Runtime Needs Lifecycle Evidence](../lessons/LL-007-hook-runtime-needs-lifecycle-evidence.md)

### Specs / Plans

- None.

### Related Features

- [F003 Optional Harness Hook Runtime](F003-optional-harness-hook-runtime.md)
- [F005 Session Recovery Hooks](F005-session-recovery-hooks.md)

### External Context

- [README](../../README.md)
- [INSTALL](../../INSTALL.md)
- [Quickstart](../quickstart.md)

## Acceptance Criteria

- [x] Hook runner no longer accepts `pre-compact` or `session-start`.
- [x] Codex, Claude Code, and OpenCode examples wire Stop only.
- [x] Root and nested Codex hook configs wire Stop only and remain identical.
- [x] Hook diagnostics no longer checks compaction recovery artifacts.
- [x] Current user-facing docs no longer describe session recovery hooks as default capability.
- [x] F005 is marked superseded by F015.

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| Hook runtime is Stop-only by default | Hook examples and Codex plugin configs contain Stop only | [EV-022](../evidence/EV-022-stop-only-hook-runtime.md) | completed |
| Removed events are not supported | `agentmentor_hook.py` rejects `pre-compact` and `session-start` choices | [EV-022](../evidence/EV-022-stop-only-hook-runtime.md) | completed |
| Session recovery is no longer current capability | F005 status is superseded and current docs point to Stop-only behavior | [EV-022](../evidence/EV-022-stop-only-hook-runtime.md) | completed |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-06-27 | completed | Stop-only hook runtime narrowing | [EV-022](../evidence/EV-022-stop-only-hook-runtime.md) | Session recovery hooks removed from current default runtime. |

## Patch History

None yet.

## Evidence

- [EV-022 Stop Only Hook Runtime](../evidence/EV-022-stop-only-hook-runtime.md)

## Recovery Snapshot

- Read first: this Feature page, then EV-022 and F003.
- Current capability state: completed; default optional hooks are Stop-only.
- Known risks: historical docs and lessons still mention session recovery; treat those as historical unless they point to F015.
- Next safe action: if changing hook runtime again, preserve Stop closeout guard and justify any new default hook against runtime complexity.
- Unblock condition: not blocked.

## Next Step

Sync installed local skills after validation so Codex loads the Stop-only hook definitions.
