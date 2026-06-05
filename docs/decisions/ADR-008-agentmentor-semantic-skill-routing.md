---
id: ADR-008
doc_kind: adr
status: accepted
scope: project
feature_refs: [docs/features/F007-agentmentor-semantic-skill-routing.md]
decision_area: skill-naming-and-discovery
created: 2026-06-04
updated: 2026-06-04
---

# ADR-008: AgentMentor Semantic Skill Routing

## Context

F006 解决了裸 `harness-*` 和项目内部 harness 概念冲突，但新的 `ai-coding-harness-*` 又暴露两个问题：第一，`coding` 过窄，当前套件还覆盖进展评估、交接、知识沉淀、事故学习、项目规则沉淀等 Agent 协作治理场景；第二，每个 workflow 都带同一个长前缀，会稀释 `readiness-dashboard` 这类能力词在 skill discovery 中的权重。

同一个“整体进展 / 距离目标 / 还差多少模块”问题在旧版 readiness skill 下更容易触发，而在 `ai-coding-harness-readiness-dashboard` 下触发表现变弱。虽然不能把触发完全归因于 slug 名称，但从第一性原理看，公开命名应该服务于 discovery：入口负责 suite 身份，子 skill 名称负责能力语义。

## Decision

采用 `AgentMentor` 作为正式品牌和插件显示名。

公开命名采用两层结构：

```text
Entrypoint: using-agentmentor
Plugin:     agentmentor@personal
Workflows:  start-gate, readiness-dashboard, knowledge-capture, ...
```

不再推荐 `ai-coding-harness-*`、`agentmentor-*` 或每个 skill 都带 suite 前缀。插件命名空间和入口 skill 负责表达归属；子 skill slug 和标题保持短语义，提升自然语言任务到具体 workflow 的匹配概率。

hooks 和可见运行状态也硬切到 AgentMentor：`run-agentmentor-hook.cmd`、`agentmentor_hook.py`、`closeout_check.py`、`.agentmentor/session-recovery`、`.agentmentor/hook-events`。不保留旧 wrapper。

## Alternatives

- 回退到 F006 前的 `harness-*`：拒绝。它恢复了部分触发优势，但重新带回项目内部 harness 概念冲突。
- 保持 `ai-coding-harness-*` 并只加强 description：拒绝。description 可以缓解，但无法改变 suite 前缀过窄和过长的问题。
- 使用 `agent-harness-*` 或 `agentmentor-*` 前缀：拒绝。它仍然让每个子 skill 承担 suite 身份，降低能力词本身的检索权重。
- 只改插件名，不改 skill slug：拒绝。Codex skill discovery 仍会看到旧 slug，核心触发问题不能闭环。

## Consequences

收益：

- `readiness-dashboard`、`change-narrative`、`knowledge-capture` 等能力词成为公开 slug 主体，更贴近用户自然语言请求。
- `AgentMentor` 比 `AI Coding Harness` 更宽，覆盖 coding 之外的 Agent 协作、恢复、复盘和治理。
- 旧命名策略由 validator 和 tests 明确拒绝，避免后续新增 workflow 又回到 suite 前缀。

代价：

- 这是第二次 breaking rename，需要重新安装本机 skills 和 personal plugin。
- 历史文档中仍会出现 `Harness` / `AI Coding Harness` 迁移背景；这些保留为历史事实，不作为当前推荐命名。
- 用户若口头说 “harness skill”，入口仍需能识别为 AgentMentor 相关请求，并在必要时澄清项目内部 harness 与 AgentMentor 的区别。

## Evidence

- [F007 AgentMentor Semantic Skill Routing](../features/F007-agentmentor-semantic-skill-routing.md)
- [EV-010 AgentMentor Semantic Skill Routing](../evidence/EV-010-agentmentor-semantic-skill-routing.md)
- `tests/test_skill_breaking_rename.py`
- `tests/test_skill_metadata_check.py`
- `tests/test_skill_progressive_disclosure.py`
