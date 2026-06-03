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
OpenCode compaction recovery now uses OpenCode's native `output.context` channel instead of treating `session.created` as a recovery event. OpenCode Stop checking now listens through the plugin `event` hook for the global `session.idle` event, fetches recent session messages, and passes the latest assistant text to the normalized `stop` runner instead of registering `session.idle` as a direct trigger hook.

## Links

- [F003 Optional Harness Hook Runtime](F003-optional-harness-hook-runtime.md)
- [F004 Delegation Gate Three Outcomes](F004-delegation-gate-three-outcomes.md)
- [LL-003 Gate Outcomes Should Encode Next Action](../lessons/LL-003-gate-outcomes-encode-next-action.md)
- [LL-004 Verify Codex Hook Schema Before Reinstalling Plugin Cache](../lessons/LL-004-codex-hook-plugin-schema-before-cache.md)
- [LL-005 Session Recovery Must Be Session-Scoped](../lessons/LL-005-session-recovery-must-be-session-scoped.md)
- [LL-006 Platform Hooks Must Use Native Context Channels](../lessons/LL-006-platform-hooks-native-context-channels.md)
- [LL-007 Hook Runtime Needs Lifecycle Evidence](../lessons/LL-007-hook-runtime-needs-lifecycle-evidence.md)
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

| F005.3 | 2026-05-31 | pending | Codex context compaction in `E:\Self-Project\Multi-Agent-Assi` produced session log events but no `.harness/session-recovery/` file. | The plugin-bundled `PreCompact` matcher used `auto|manual`; current Codex Desktop emitted `compacted/context_compacted` with no Harness hook execution evidence, so the matcher was too narrow or not interpreted as intended. | Set Codex `PreCompact` matcher to empty so all pre-compaction triggers run, while keeping `SessionStart` narrowed to `compact`; add a regression assertion for the matcher. | done |
| F005.4 | 2026-05-31 | pending | A new Codex Desktop session in `E:\Work-Project\OtherWork\ScienceClaw` still recorded `compacted/context_compacted` without `.harness/session-recovery/` artifacts. | UI visibility, trusted hook config, and runner smoke were insufficient lifecycle proof; Codex did not provide observable evidence that plugin `PreCompact` executed for the real compaction event. | Add `hook_diagnostics.py` to run runner smoke and scan Codex session logs for compactions missing recovery artifacts; document Codex PreCompact as unproven when diagnostics warn. | done |
| F005.5 | 2026-05-31 | pending | Codex Settings displayed all three Harness hooks, but new sessions still showed no observable `Stop`, `PreCompact`, or `SessionStart` execution. | The plugin-bundled config relied on unproven runtime assumptions: missing `[features].hooks` / `[features].plugin_hooks`, `hooks/hooks.json` versus root `hooks.json` discovery, direct `python ./skills/...` commands, and Unix-style environment expansion on Windows. UI config discovery was mistaken for command execution proof. | Enable Codex hook feature gates, keep both Codex hook config locations, route commands through `hooks/run-harness-hook.cmd` so the wrapper resolves the plugin root, use `commandWindows` with `%PLUGIN_ROOT%`, and add `.harness/hook-events/events.jsonl` runtime trace from the hook runner. | in progress |
| F005.6 | 2026-06-03 | pending | OpenCode example wired `session.idle` as a direct hook key, so Stop closeout checks were not supported by the current `@opencode-ai/plugin` `Hooks` contract; even a dispatched idle event only carries `sessionID`, not the final assistant text needed by the closeout checker. | The adapter conflated OpenCode's global event stream event `session.idle` with direct trigger hooks such as `experimental.session.compacting`, then treated lifecycle metadata as if it were a Stop payload. Current plugin types expose global events through `event(input)`, while `session.idle` appears only as an SDK event payload type. | Route OpenCode Stop checks through `event: async (input)`, filter `input.event.type === "session.idle"`, fetch recent session messages through `client.session.messages`, pass the latest assistant text as `last_assistant_message`, and add regression assertions for both the event entry and message extraction. | done |

## Patch Churn Review

F005 has accumulated three platform-adapter follow-ups in one day, so the failure pattern is no longer isolated implementation noise. The shared root cause is treating hook integration as a small config mapping instead of a platform contract with independently verified trigger evidence, payload fields, matcher semantics, and output channels.

The fixes have moved progressively upstream:

- F005.1 corrected the recovery isolation invariant: automatic runtime recovery must be same-session and compact-sourced.
- F005.2 corrected OpenCode's native context channel: compaction recovery has to flow through `output.context`.
- F005.3 corrected Codex trigger breadth: `PreCompact` must run on observed compaction variants, while `SessionStart` remains narrowed to `compact`.
- F005.4 corrected the verification boundary: Codex hook recovery is not considered proven by config or smoke alone; it needs lifecycle evidence or a diagnostic warning.
- F005.5 corrected the command execution assumption: Codex hook UI discovery is not enough; hook config must cover both observed discovery locations, command paths must avoid current-working-directory assumptions, and actual execution must produce trace evidence.
- F005.6 corrected the OpenCode event contract: global lifecycle events must enter through `event(input)`, while direct trigger hooks remain limited to names present in the OpenCode `Hooks` interface.

The next adapter change should not add another local patch until it first captures a real trigger sample or platform contract for the affected hook. If another Codex/Claude/OpenCode hook issue appears, run `hook_diagnostics.py` or add a small adapter verification note/test fixture that records the observed event shape before changing matcher, payload, or output behavior.

## Evidence

[EV-008 Session Recovery Hooks](../evidence/EV-008-session-recovery-hooks.md)

## Next Step

Use `hook_diagnostics.py` after Codex hook installation or update. Treat Codex `PreCompact` recovery as optional and unproven on machines where diagnostics find compaction events without recovery artifacts.
