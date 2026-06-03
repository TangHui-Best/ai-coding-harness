---
id: F006
doc_kind: feature
status: active
created: 2026-06-03
updated: 2026-06-03
---

# F006: AI Coding Harness Skill Rename

## Goal

通过硬切重命名，把 AI Coding Harness 的公开 skill slug 从 `using-harness` / `harness-*` 迁移到 `ai-coding-harness` / `ai-coding-harness-*`，消除项目内部 harness 概念冲突。

## Vision Anchor

- 原始请求或来源：用户指出很多项目内部也有 `harness` 功能，担心当前 `harness-*` skill 命名造成概念冲突；随后明确认可不保留兼容、卸载本机旧 skill 并重新安装新版本的硬切方案。
- 用户痛点或工程问题：裸 `harness-*` 容易被误解为项目测试夹具、运行容器或业务内部 harness，而不是 AI 辅助编码治理流程。
- 期望结果：正式系统名统一为 `AI Coding Harness`；入口 skill 为 `ai-coding-harness`；子 workflow skill 为 `ai-coding-harness-*`；skill 标题、agent display name、安装提示和 session recovery 输出不再以裸 `Harness` 作为公开入口；旧 `using-harness` / `harness-*` 目录从项目和本机独立 skills 安装中移除。Codex personal plugin 缓存需要由插件包发布/卸载链路单独收口，不能只靠 `scripts/install.ps1 codex` 保证。
- 非目标或边界：不保留 wrapper，不支持旧 slug 兼容；仍保留 `harness_hook.py`、`harness_closeout_check.py` 等内部脚本文件名，因为它们不是公开 skill slug。
- Exit Gate 对照来源：ADR-007、`ai-coding-harness` 命名边界、README/INSTALL/skill index、`skill_metadata_check.py` 严格校验结果、EV-009。

## Current Status

Repo/local-skills done, plugin-cache follow-up open。本迭代从兼容策略升级为 breaking rename：仓库目录、frontmatter、显示标题、agent display name、安装提示和 session recovery 输出已迁移到 `AI Coding Harness` / `ai-coding-harness-*`；本机 `C:\Users\HUAWEI\.codex\skills` 已重新安装为 11 个 `ai-coding-harness*` 且 0 个旧 skill。后续验证发现 Codex personal plugin cache 可能由旧插件安装源重新生成 `personal/harness/.../skills/harness-*`，因此 UI/新会话是否完全切换还取决于插件包卸载或重新发布。

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
- [ ] Codex personal plugin 安装源或缓存链路不再重新生成旧 `personal/harness` 包。

## Patch History

| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |
| --- | --- | --- | --- | --- | --- | --- |
| F006.1 | 2026-06-03 | pending | 另一个 Codex 会话仍输出 `Harness Skill` 等旧称呼。 | `~/.codex/skills` 已是新版本，但 Codex personal plugin cache 可由旧插件包重新生成 `personal/harness/.../skills/harness-*`。 | 将插件缓存链路列为独立后续项，不再把一次性删除 cache 作为完成证据。 | open |

## Evidence

[EV-009 Skill Naming Compatibility](../evidence/EV-009-skill-naming-compatibility.md)

## Next Step

处理 Codex personal plugin 包：卸载旧 `harness` personal plugin，或重新发布/安装插件包，使插件缓存中的 skills 也变为 `ai-coding-harness-*`，再重启 Codex 验证 UI。
