---
id: LL-007
doc_kind: lesson
status: active
scope: project
feature_refs: [docs/features/F005-session-recovery-hooks.md]
applies_to: [codex-plugin, hook-runtime, precompact, session-recovery, diagnostics]
created: 2026-05-31
updated: 2026-05-31
---

# LL-007: Hook Runtime Needs Lifecycle Evidence

## Pitfall

把“插件已安装”“Hook UI 能看到配置”“runner smoke 能手动写文件”误认为“平台生命周期事件一定会执行 hook”，会让 session recovery 看起来已经闭合，实际压缩后却没有任何 `.harness/session-recovery/` 材料。

## Root Cause

Hook 集成跨了三层不同事实：配置扫描、命令 runner、平台生命周期派发。前两层成立并不能证明第三层成立。Codex Desktop 中已经出现真实会话记录 `compacted/context_compacted`，但没有 Harness `PreCompact` 执行痕迹，也没有 recovery artifact。

后续还发现第四层风险：Codex 设置页能显示 Hook，不代表 runtime 会从预期的配置入口派发命令，也不代表直接命令里的相对路径会以插件根目录为工作目录执行。Codex 还需要用户配置启用 hook feature gates；UI 配置发现、信任 hash、命令执行是三件事。

## Trigger

出现以下任一信号时触发本 Lesson：

- session log 有 `compacted` 或 `context_compacted`，但项目下没有 `.harness/session-recovery/`。
- Hook UI 显示已刷新或已信任，但真实压缩后没有 recovery 文件。
- 手动运行 `harness_hook.py --event pre-compact` 成功，但平台自动压缩没有产物。
- 同一平台 hook 连续修改 matcher、schema、cache 或安装步骤仍无法得到真实触发证据。
- Hook UI 能显示事件，但 `.harness/hook-events/events.jsonl` 没有对应运行记录。

## Fix

补充 `using-harness/scripts/hook_diagnostics.py`，把诊断拆成两类证据：

- runner smoke：证明 Harness runner 在目标项目根目录可写 recovery snapshot。
- lifecycle evidence：扫描 Codex session logs，发现 `compacted/context_compacted` 但没有 recovery artifacts 时返回 warning。

同时让 `harness_hook.py` 在真实运行时写 `.harness/hook-events/events.jsonl`。这份 trace 只记录 event、platform、session id、decision、check、severity，不记录用户或 assistant 正文。

Codex plugin-bundled hook 配置同时保留 root-level `hooks.json` 和 `hooks/hooks.json`，并要求用户配置：

```toml
[features]
hooks = true
plugin_hooks = true
```

命令先进入插件内的 wrapper：

```text
"${CLAUDE_PLUGIN_ROOT}/hooks/run-harness-hook.cmd" stop
```

wrapper 再用自身所在目录反推插件根目录，并调用 `skills/using-harness/hooks/harness_hook.py`。不要让 `hooks.json` 直接调用 `python ./skills/...`，除非当前目标 runtime 已经用真实触发证据证明工作目录就是插件根目录。

Windows 上优先使用 `commandWindows` 和 `%PLUGIN_ROOT%`，不要假设 `cmd.exe` 会展开 `${PLUGIN_ROOT}` 或 `${CLAUDE_PLUGIN_ROOT}`。

## Protection

后续修改或安装 Codex hooks 后，先运行：

```bash
python <skills-root>/using-harness/scripts/hook_diagnostics.py codex --project-root <repo>
```

不要把 UI 可见、cache 文件存在、trusted hash 存在或 runner 手动成功当作 lifecycle proof。只有真实生命周期触发后产生预期 artifact、`.harness/hook-events/events.jsonl` 记录了对应事件，或诊断没有发现压缩缺产物，才把该 hook 标记为可依赖。

## Source

本 Lesson 来自 F005.4/F005.5。用户在 `E:\Work-Project\OtherWork\ScienceClaw` 的 2026-05-31 新会话中触发了 Codex context compaction，session log 确认存在 `compacted/context_compacted`，但项目下没有 `.harness/session-recovery/`。后续又确认 Codex 设置页能显示三个 Harness hooks，但 `Stop`、`PreCompact`、`SessionStart` 均没有可观察执行证据。

## Principle

Hook 能力的验收单位不是“配置存在”，而是“平台生命周期事件产生了可观察结果”。对 optional hook runtime，诊断应 fail open，但必须诚实暴露未被证明的自动化能力。
