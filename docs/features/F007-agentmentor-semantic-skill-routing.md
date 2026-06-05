---
id: F007
doc_kind: feature
status: completed
created: 2026-06-04
updated: 2026-06-04
---

# F007: AgentMentor Semantic Skill Routing

## Goal

把上一轮 `AI Coding Harness` 命名继续收敛为更宽、更少歧义的 `AgentMentor`：入口保留为 `using-agentmentor`，子 skill 改为短语义 slug，插件身份改为 `agentmentor@personal`，避免每个 workflow 都被 `ai-coding-harness-*` 前缀限制触发范围。

## Vision Anchor

- 原始请求或来源：用户观察到同一个项目进展评估问题在旧版 `harness-readiness-dashboard` 会触发，但重命名为 `ai-coding-harness-readiness-dashboard` 后没有稳定触发；随后明确认为 `ai-coding-harness` 太窄，当前 skill 不止服务于 coding。
- 用户痛点或工程问题：过长且过窄的 suite 前缀会让 discovery 更依赖“coding/harness”字面词，而 `readiness-dashboard`、`change-narrative`、`knowledge-capture` 等能力本质上面向 Agent 协作治理，不只面向写代码。
- 期望结果：正式品牌为 `AgentMentor`；公开插件身份为 `agentmentor@personal`；入口 skill 为 `using-agentmentor`；子 skill 为 `start-gate`、`readiness-dashboard` 等短语义名；活跃安装、hooks、脚本、文档和 validator 不再把 `ai-coding-harness-*` 当推荐命名。
- 非目标或边界：不保留旧 slug wrapper；不把项目内部通用词 `test harness`、`runtime harness` 机械替换掉；历史 F006/ADR-007/EV-009 可保留迁移背景。
- Exit Gate 对照来源：ADR-008、EV-010、`using-agentmentor` 入口、`skill_metadata_check.py --strict`、全量 unittest、安装后本机 skill/plugin 检查。

## Current Status

Done。仓库内 skill 目录、frontmatter、标题、routing、插件 manifest、hook runner、session recovery 目录和 metadata validator 已迁到 AgentMentor 目标形态；本机 Codex skills 已清理旧 `ai-coding-harness*` 并安装 11 个新 skill；personal plugin 源、marketplace、config 和 cache 已切到 `agentmentor@personal`。

## Links

- [ADR-008 AgentMentor Semantic Skill Routing](../decisions/ADR-008-agentmentor-semantic-skill-routing.md)
- [LL-008 Skill Naming Affects Discovery Scope](../lessons/LL-008-skill-naming-affects-discovery-scope.md)
- [EV-010 AgentMentor Semantic Skill Routing](../evidence/EV-010-agentmentor-semantic-skill-routing.md)

## Acceptance Criteria

- [x] `skills/` 下正式 skill 目录为 `using-agentmentor` 加 10 个短语义 workflow slug。
- [x] 子 skill 标题使用短语义 H1，不再重复 `AgentMentor` 或 `AI Coding Harness` 前缀。
- [x] `.codex-plugin/plugin.json` 使用 `agentmentor` / `AgentMentor` 身份。
- [x] `readiness-dashboard` description 覆盖 overall progress、distance to target、maturity、roadmap gap、整体进展、距离目标、还差多少、交付缺口等触发词。
- [x] `skill_metadata_check.py` 拒绝 `harness-*` 和 `ai-coding-harness-*`，允许短语义 workflow slug。
- [x] 本机 Codex skills 和 personal plugin 重新安装为 AgentMentor 最新版本，旧 `ai-coding-harness@personal` 不再启用。
- [x] 全量 tests、skill metadata、knowledge check、安装后 validator 均通过。
- [x] 命名迭代经验已沉淀为 Lesson，明确 `harness` 初始合理性和 `ai-coding-harness` 触发收窄风险。

## Patch History

None yet.

## Evidence

- [EV-010 AgentMentor Semantic Skill Routing](../evidence/EV-010-agentmentor-semantic-skill-routing.md)
- [LL-008 Skill Naming Affects Discovery Scope](../lessons/LL-008-skill-naming-affects-discovery-scope.md)

## Next Step

重启 Codex，让当前会话之外的新会话加载 `agentmentor@personal` 和新的 skill metadata。
