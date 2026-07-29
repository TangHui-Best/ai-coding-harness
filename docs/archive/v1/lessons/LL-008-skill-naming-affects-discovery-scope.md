---
id: LL-008
doc_kind: lesson
status: active
scope: project
feature_refs: [docs/features/F007-agentmentor-semantic-skill-routing.md]
applies_to: [skill-design, naming, discovery, trigger-surface, agentmentor]
created: 2026-06-05
updated: 2026-06-05
---

# LL-008: Skill Naming Affects Discovery Scope

## Case

F006 到 F007 的命名迭代经历了三步：

```text
harness-* -> ai-coding-harness-* -> AgentMentor + short semantic workflow slugs
```

`harness-*` 在早期并不是错误命名，当时系统主要为 AI coding 过程提供门禁、Evidence、ADR、closeout 等工程护栏。真正的问题是：能力后来扩展到进展评估、交接、知识沉淀、事故学习、项目规则、roadmap gap 等非纯 coding 场景，但命名没有同步复核。

`ai-coding-harness-*` 解决了项目内部 test/runtime/evaluation harness 的概念冲突，却让 `readiness-dashboard` 这类泛化能力更难被“整体进展 / 距离目标 / 还差多少模块 / 当前成熟度”这类自然语言问题命中。

## Resolution

采用两层命名：

```text
Suite / plugin identity: AgentMentor
Entrypoint:              using-agentmentor
Workflow skills:         start-gate, readiness-dashboard, knowledge-capture, ...
```

这让归属和能力分离：

- `AgentMentor` 表达系统身份和温度，比 `AI Coding Harness` 更能覆盖 Agent 协作治理。
- `using-agentmentor` 作为入口保留 suite 召回和命名边界。
- 短语义 workflow slug 让能力词成为 discovery 主体，避免每个 skill 都被 suite 前缀绑住。
- `readiness-dashboard` description 显式覆盖整体进展、距离目标、成熟度、交付缺口和 roadmap gap。

## Pitfall

把 skill 名称当成“展示标签”而不是“触发面的一部分”，会低估命名对 Agent discovery 的影响。尤其是 suite 级前缀如果过窄，可能让一个已经泛化的能力重新被限制在前缀表达的场景里。

本次命名演进经历了三步：

```text
harness-* -> ai-coding-harness-* -> AgentMentor + short semantic workflow slugs
```

`harness-*` 在早期并不是错误命名。当时这个系统主要为 AI coding 过程提供门禁、Evidence、ADR、closeout 等工程护栏，用 `harness` 表达“约束和验证环节”是合理的。真正的问题是：能力后来扩展到了进展评估、交接、知识沉淀、事故学习、项目规则、roadmap gap 等非纯 coding 场景，而命名没有同步复核。

`ai-coding-harness-*` 解决了项目内部 test/runtime/evaluation harness 的概念冲突，却引入了新的触发收窄：`coding` 和长 suite 前缀让 `readiness-dashboard` 这类泛化能力更难被“整体进展 / 距离目标 / 还差多少模块 / 当前成熟度”这类自然语言问题命中。

## Root Cause

Skill discovery 同时受到至少三层文字影响：

- plugin 或 skill suite 的显示名，负责建立系统身份。
- skill slug 和 H1，负责暴露能力语义。
- frontmatter description，负责匹配具体触发场景。

F006 的 `ai-coding-harness-*` 把 suite 身份、领域边界和 workflow 能力压进同一个 slug。这样做能减少裸 `harness` 歧义，但代价是每个 workflow 的核心能力词都被长前缀稀释，并被 `coding` 场景框住。

从第一性原理看，入口和子技能承担的职责不同：

- 入口 skill 应负责 suite 身份、命名边界和路由。
- 子 skill 应负责能力语义，例如 `readiness-dashboard`、`knowledge-capture`、`change-narrative`。
- 插件命名空间应负责 UI 归属，不应要求每个子 skill 重复 suite 前缀。

## Protection

后续新增或重命名 skill 时先做命名复核：

1. 判断这是 suite 身份、入口行为，还是 workflow 能力。
2. 如果是 workflow 能力，优先使用短语义 slug，不重复 suite 前缀。
3. 检查名称是否过窄：不要把已经泛化的 Agent 协作能力命名成只适合 coding 的能力。
4. 保留用户真实会问的问题作为触发词，而不是只写内部术语。
5. 用测试锁定命名边界：旧 slug 应报错，新短语义 slug 应允许。

`skill_metadata_check.py` 应继续拒绝 `harness-*` 和 `ai-coding-harness-*` 作为新公开 skill slug，允许短语义 workflow slug。

## Source

本 Lesson 来自 F006 到 F007 的命名迭代。用户指出：一开始命名为 harness 是合理的，因为当时没有预期这套 skill 会泛化到非 coding 场景；但 `ai-coding-harness` 导致触发范围缩小，这一点值得稳定沉淀。

相关证据：

- [F007 AgentMentor Semantic Skill Routing](../features/F007-agentmentor-semantic-skill-routing.md)
- [ADR-008 AgentMentor Semantic Skill Routing](../decisions/ADR-008-agentmentor-semantic-skill-routing.md)
- [EV-010 AgentMentor Semantic Skill Routing](../evidence/EV-010-agentmentor-semantic-skill-routing.md)

## Principle

Skill 名称不是装饰，它是触发系统的一部分。suite 名称负责身份，workflow 名称负责能力；当能力泛化时，命名也必须重新接受验收。
