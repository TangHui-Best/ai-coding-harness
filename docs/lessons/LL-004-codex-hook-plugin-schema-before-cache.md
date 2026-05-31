---
id: LL-004
doc_kind: lesson
status: active
scope: project
feature_refs: [docs/features/F003-optional-harness-hook-runtime.md, docs/features/F005-session-recovery-hooks.md]
applies_to: [codex-plugin, hook-runtime, hook-installation, local-plugin-cache, session-recovery, stop-hook]
created: 2026-05-31
updated: 2026-05-31
---

# LL-004: Verify Codex Hook Schema Before Reinstalling Plugin Cache

## Pitfall

把 Codex hook 安装失败误判为“插件没有刷新”或“缓存没有更新”，会导致反复重装插件但 UI 仍然显示未找到钩子。

本次问题连续经历了几轮修复才成功，原因不是 hook runner 本身不可用，而是没有先归零确认 Codex 实际读取的 hook 配置 contract。我们先后修了路径、事件名、cachebuster，最后才发现真正的 schema 入口还缺少顶层 `hooks` 字段。

## Root Cause

根因是把三层不同的配置形态混在了一起：

- Skill 内资源：`skills/using-harness/hooks/codex-hooks.example.json` 只是安装示例，默认不会自动成为 Codex Desktop 的 hook 配置。
- Plugin-bundled hooks：Codex 插件内的 hook 入口必须放在插件根目录的 `hooks/hooks.json`。
- Codex hook schema：文件顶层必须是 `{ "hooks": { ... } }`，事件名位于 `hooks` 对象内部，例如 `SessionStart`、`PreCompact`、`Stop`。

第一次修复只把文件放进了插件根目录，第二次修复只把事件名改成了 Codex 官方事件名，但仍然遗漏了顶层 `hooks`。因此插件可以安装、cache 中也能看到文件，但 Codex Hooks UI 仍然不识别。

## Trigger

出现以下信号时，应优先怀疑 hook schema 或扫描入口，而不是继续重装：

- `codex plugin list` 显示插件已安装启用，但 Codex Desktop Hooks 页面仍显示未找到钩子。
- 插件 cache 目录中存在 `hooks.json`，但路径不是 `hooks/hooks.json`。
- `hooks/hooks.json` 中能看到 `SessionStart`、`PreCompact`、`Stop`，但这些事件名位于 JSON 顶层，而不是 `hooks` 对象下。
- 手动运行 hook runner smoke test 通过，但 UI 仍不展示 hook。
- 修改本地插件后没有更新 cachebuster，导致 Desktop 继续读取旧插件 cache。

## Fix

本次修复采取了四步：

1. 在插件根目录新增 `hooks/hooks.json`，作为 Codex 插件自动扫描的入口。
2. 将 Codex 事件名改为官方事件名：`SessionStart`、`PreCompact`、`Stop`。
3. 将 hook 配置改为 Codex schema：

```json
{
  "hooks": {
    "SessionStart": [],
    "PreCompact": [],
    "Stop": []
  }
}
```

4. 使用 `update_plugin_cachebuster.py` 更新插件版本，再执行 `codex plugin add harness@personal`，确保 Desktop 读取新 cache。

最终安装成功的版本为 `harness@personal 0.1.0+codex.20260531003837`。

## Protection

以后修改 Codex plugin hook 时，按以下顺序验证，不要跳步：

1. 先查平台 contract：确认 hook 文件位置、顶层 schema、事件名、matcher、平台变量。
2. 校验 JSON 结构：Codex hook 文件必须有顶层 `hooks` 字段。
3. 区分路径变量：
   - Skill 示例使用 `HARNESS_SKILL_ROOT`。
   - Plugin-bundled hooks 使用 `PLUGIN_ROOT`。
4. 本地插件更新必须执行 cachebuster，而不是只改源目录。
5. 重装后读取 cache 目录中的最终文件，确认 Desktop 实际会消费的内容。
6. 不把 CLI 插件安装成功当成 hook 安装成功；hook 成功需要 UI 可见或真实 hook 触发证据。
7. 对 schema 增加自动化测试，避免未来再次把事件名放回 JSON 顶层。

已新增保护测试：

```text
tests/test_skill_progressive_disclosure.py::SkillProgressiveDisclosureTests::test_codex_hook_example_uses_codex_schema
```

该测试固定要求 `codex-hooks.example.json` 包含顶层 `hooks`，且 `hooks` 下包含 `SessionStart`、`PreCompact`、`Stop`。

## Source

本 Lesson 来自 Harness plugin 本机安装验证过程：

- 目标：在 Codex Desktop Hooks 页面展示并启用 Harness Stop / SessionStart / PreCompact hooks。
- 失败表现：插件已安装启用、cache 中存在 hook 文件，但 Hooks 页面仍显示未找到钩子。
- 最终根因：Codex hook JSON 缺少顶层 `hooks` schema。
- 相关 Feature：
  - [F003 Optional Harness Hook Runtime](../features/F003-optional-harness-hook-runtime.md)
  - [F005 Session Recovery Hooks](../features/F005-session-recovery-hooks.md)

## Principle

平台集成失败时，先验证平台 contract，再验证缓存与安装流程。不要把“文件存在”“插件安装成功”“runner 可手动执行”误认为“平台已识别 hook”。Hook 集成至少要同时满足：正确扫描路径、正确 schema、正确事件名、正确缓存版本，以及 UI 或真实触发证据。
