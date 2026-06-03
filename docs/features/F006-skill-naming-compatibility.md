---
id: F006
doc_kind: feature
status: completed
created: 2026-06-03
updated: 2026-06-03
---

# F006: AI Coding Harness Skill Rename

## Goal

通过硬切重命名，把 AI Coding Harness 的公开 skill slug 从 `using-harness` / `harness-*` 迁移到 `ai-coding-harness` / `ai-coding-harness-*`，消除项目内部 harness 概念冲突。

## Vision Anchor

- 原始请求或来源：用户指出很多项目内部也有 `harness` 功能，担心当前 `harness-*` skill 命名造成概念冲突；随后明确认可不保留兼容、卸载本机旧 skill 并重新安装新版本的硬切方案。
- 用户痛点或工程问题：裸 `harness-*` 容易被误解为项目测试夹具、运行容器或业务内部 harness，而不是 AI 辅助编码治理流程。
- 期望结果：正式系统名统一为 `AI Coding Harness`；入口 skill 为 `ai-coding-harness`；子 workflow skill 为 `ai-coding-harness-*`；skill 标题、agent display name、安装提示和 session recovery 输出不再以裸 `Harness` 作为公开入口；旧 `using-harness` / `harness-*` 目录从项目、本机独立 skills 安装和 Codex personal plugin 缓存中移除；personal plugin 入口硬切为 `ai-coding-harness@personal`。
- 非目标或边界：不保留 wrapper，不支持旧 slug 兼容；仍保留 `harness_hook.py`、`harness_closeout_check.py` 等内部脚本文件名，因为它们不是公开 skill slug。
- Exit Gate 对照来源：ADR-007、`ai-coding-harness` 命名边界、README/INSTALL/skill index、`skill_metadata_check.py` 严格校验结果、EV-009。

## Current Status

Done。本迭代从兼容策略升级为 breaking rename：仓库目录、frontmatter、显示标题、agent display name、安装提示和 session recovery 输出已迁移到 `AI Coding Harness` / `ai-coding-harness-*`；本机 `C:\Users\HUAWEI\.codex\skills` 已重新安装为 11 个 `ai-coding-harness*` 且 0 个旧 skill；旧 `harness@personal` 插件已移除，personal marketplace 已切到 `ai-coding-harness@personal`，Codex cache 已生成 `personal/ai-coding-harness/.../skills/ai-coding-harness-*`。

## Links

- [ADR-007 AI Coding Harness Skill Naming Compatibility](../decisions/ADR-007-ai-coding-harness-skill-naming-compatibility.md)
- [EV-009 Skill Naming Compatibility](../evidence/EV-009-skill-naming-compatibility.md)

## Acceptance Criteria

- [x] 文档明确 `AI Coding Harness` 是正式系统名，`Harness` 只是定义后的短称。
- [x] `skills/` 下只保留 `ai-coding-harness` 和 `ai-coding-harness-*` skill 目录。
- [x] 所有 skill frontmatter `name` 与新目录名一致。
- [x] 所有 skill 标题和 agent display name 使用 `AI Coding Harness` 前缀。
- [x] 文档、测试、validator 和 hook wrapper 路径全部引用新入口目录。
- [x] 本机旧 `using-harness` / `harness-*` skill 目录已卸载，并重新安装新版本。
- [x] Codex personal plugin 安装源和缓存链路不再重新生成旧 `personal/harness` 包。

## Patch History

| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |
| --- | --- | --- | --- | --- | --- | --- |
| F006.1 | 2026-06-03 | pending | 另一个 Codex 会话仍输出 `Harness Skill` 等旧称呼。 | `~/.codex/skills` 已是新版本，但 Codex personal plugin cache 由旧 `harness@personal` 源重新生成 `personal/harness/.../skills/harness-*`。 | 新增仓库 `.codex-plugin/plugin.json`，personal marketplace 切到 `ai-coding-harness@personal`，移除旧插件并重新安装新插件。 | closed |

## Evidence

[EV-009 Skill Naming Compatibility](../evidence/EV-009-skill-naming-compatibility.md)

## Next Step

重启 Codex，让当前会话之外的新会话加载 `ai-coding-harness@personal` 的 plugin metadata。
