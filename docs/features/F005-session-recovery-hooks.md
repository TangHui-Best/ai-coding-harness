---
id: F005
doc_kind: feature
status: completed
created: 2026-05-30
updated: 2026-05-31
---

# F005: Session Recovery Hooks

## Goal

Add the second default Harness hook capability: lightweight `SessionStart` / `PreCompact` context recovery that reduces manual handoff work without making hooks mandatory.

## Vision Anchor

- Original request or source: The user approved keeping `Stop` as the only hard default boundary and adding a second hook focused on session recovery.
- User pain point or engineering problem: Long Harness iterations can lose context after compaction or session restarts, forcing manual handoff prompts even when the project already has a clear current goal.
- Desired outcome: `pre-compact` writes a local recovery snapshot scoped to the current session and `session-start` exposes that snapshot only when the same session resumes from `compact` and the platform supports contextual hook output.
- Non-goals or boundaries: Do not reintroduce default `PostToolUse`; do not move Start Gate, Vision Gate, ADR, Lesson, or Feature ownership judgment into hook code; do not make recovery snapshots canonical docs.
- Exit Gate source: Hook runner tests, example hook configs, install docs, LL-003, and EV-008.

## Current Status

Done. The optional hook runner supports `pre-compact` and `session-start`, default examples wire session recovery hooks, same-session compact recovery can inject context, and missing, unreadable, or cross-session recovery state fails open.
OpenCode compaction recovery now uses OpenCode's native `output.context` channel instead of treating `session.created` as a recovery event.

## Links

- [F003 Optional Harness Hook Runtime](F003-optional-harness-hook-runtime.md)
- [F004 Delegation Gate Three Outcomes](F004-delegation-gate-three-outcomes.md)
- [LL-003 Gate Outcomes Should Encode Next Action](../lessons/LL-003-gate-outcomes-encode-next-action.md)
- [LL-004 Verify Codex Hook Schema Before Reinstalling Plugin Cache](../lessons/LL-004-codex-hook-plugin-schema-before-cache.md)
- [LL-005 Session Recovery Must Be Session-Scoped](../lessons/LL-005-session-recovery-must-be-session-scoped.md)
- [LL-006 Platform Hooks Must Use Native Context Channels](../lessons/LL-006-platform-hooks-native-context-channels.md)
- [EV-008 Session Recovery Hooks](../evidence/EV-008-session-recovery-hooks.md)

## Acceptance Criteria

- [x] `pre-compact` writes `.harness/session-recovery/by-session/<session_id>.md` with deterministic recovery context from hook payload or transcript tail, and updates `latest.md` only for manual inspection.
- [x] `session-start` reads only the same-session compact recovery snapshot and returns additional context for platforms that can consume it.
- [x] Missing, invalid, or unreadable recovery state returns `allow` with a warning or no-context reason instead of blocking Skills-only work.
- [x] Codex, Claude Code, and OpenCode examples wire `session-start`, `pre-compact`, and `stop` while still excluding default `PostToolUse`.
- [x] Recovery snapshots remain local runtime state under `.harness/`, not canonical Harness knowledge under `docs/`.

## Patch History

| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |
| --- | --- | --- | --- | --- | --- | --- |
| F005.1 | 2026-05-31 | pending | 新开独立会话可能读取同项目旧 `latest.md`，Codex `SessionStart` 输出也未使用官方 `hookSpecificOutput.additionalContext` 结构。 | 恢复快照按项目级 `latest.md` 建模，缺少 session/source 约束；Codex 分支输出复用了 generic 结构。 | 改为 `by-session/<session_id>.md`，仅 `source=compact` 且同一 session 时注入；新增污染防护和 Codex 输出结构测试。 | done |
| F005.2 | 2026-05-31 | pending | OpenCode compaction could write a snapshot but not inject recovery context; OpenCode `sessionID` payloads also fell back to project-level `latest.md`. | The adapter copied the Codex/Claude `SessionStart` mental model instead of using OpenCode's `experimental.session.compacting(input, output)` contract and native `output.context` channel. | Recognize `sessionID`, remove `session.created` recovery wiring, inject same-session recovery context during `experimental.session.compacting`, and add regression tests for OpenCode's context output contract. | done |

## Evidence

[EV-008 Session Recovery Hooks](../evidence/EV-008-session-recovery-hooks.md)

## Next Step

Trial the recovery hook examples in real Codex, Claude Code, and OpenCode sessions and tighten platform adapters only where actual hook output behavior requires it.
