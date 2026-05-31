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

## Trigger

出现以下任一信号时触发本 Lesson：

- session log 有 `compacted` 或 `context_compacted`，但项目下没有 `.harness/session-recovery/`。
- Hook UI 显示已刷新或已信任，但真实压缩后没有 recovery 文件。
- 手动运行 `harness_hook.py --event pre-compact` 成功，但平台自动压缩没有产物。
- 为同一平台 hook 连续修改 matcher、schema、cache 或安装步骤仍无法得到真实触发证据。

## Fix

补充 `using-harness/scripts/hook_diagnostics.py`，把诊断拆成两类证据：

- runner smoke：证明 Harness runner 在目标项目根目录可写 recovery snapshot。
- lifecycle evidence：扫描 Codex session logs，发现 `compacted/context_compacted` 但没有 recovery artifacts 时返回 warning。

这不是让 hook 变成强依赖；诊断 warning 只说明 optional runtime 未被证明，Skills-only Harness 仍然可用。

## Protection

后续修改或安装 Codex hooks 后，先运行：

```bash
python <skills-root>/using-harness/scripts/hook_diagnostics.py codex --project-root <repo>
```

不要把 UI 可见、cache 文件存在、trusted hash 存在或 runner 手动成功当作 lifecycle proof。只有真实生命周期触发后产生预期 artifact，或者诊断没有发现压缩缺产物，才把该 hook 标记为可依赖。

## Source

本 Lesson 来自 F005.4。用户在 `E:\Work-Project\OtherWork\ScienceClaw` 的 2026-05-31 新会话中触发了 Codex context compaction，session log 确认存在 `compacted/context_compacted`，但项目下没有 `.harness/session-recovery/`。手动 runner smoke 可写入 `.tmp`，排除了文件权限和 runner 本身故障。

## Principle

Hook 能力的验收单位不是“配置存在”，而是“平台生命周期事件产生了可观察结果”。对 optional hook runtime，诊断应 fail open 但必须诚实暴露未被证明的自动化能力。
