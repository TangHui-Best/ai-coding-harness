# AI Coding Harness

[English](README.md) | 简体中文

[![knowledge-check](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml/badge.svg)](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml)

一个面向 AI 辅助编码的轻量 Harness：把 Skill、项目记忆、门禁、证据和工程工作流组合成可复用的协作体系。

## 为什么需要它

AI coding assistant 已经可以很快地产出代码，但“写得快”并不等于“系统变强”。

在真实项目里，更棘手的问题通常不是“Agent 会不会写代码”，而是：

- Agent 是否知道项目长期规则？
- 新会话能否恢复上下文？
- 完成声明是否有 Evidence 支撑？
- 决策和被否决的方案是否被保留下来？
- 事故和缺陷是否会沉淀成可复用的防护？
- 人和 Agent、多 Agent 之间能否协作而不丢状态？

这个仓库探索的是一套轻量的 AI 辅助研发 Harness，用来把一次次协作经验沉淀为工程系统能力。

## 核心观点

```text
Prompt 解决单次表达。
Skill 解决单次流程。
Harness 解决长期工程系统行为。
```

AI Coding Harness 的目标不是让 Prompt 越写越长，而是把重复出现的协作经验沉淀为可复用的工作流、项目记忆、门禁和可追溯证据。

## 这个仓库提供什么

- 一个入口 Skill：`using-harness`
- 八个聚焦的 Harness Skill：开工门禁、检索、文档生命周期、事故学习、愿景校验、变更叙事、知识沉淀、项目规则晋升
- 可复用模板：Feature、ADR、Lesson、Evidence、AGENTS instructions
- 一个轻量校验脚本：`knowledge_check.py`
- 最小 Harness 和项目级 Harness 示例

## 仓库结构

```text
skills/       可复用的 Agent 工作流 Skill
docs/         概念、架构和工作流说明
templates/    可复用文档模板
examples/     最小 Harness 和项目级 Harness 示例
scripts/      轻量校验工具
```

## Harness 能力

- 非平凡实现前进行 Start Gate，判断是否需要澄清或前置知识锚点
- 非平凡任务开始前进行 Knowledge Retrieval
- 非平凡实现前，以及 Review、Merge、Release、Handoff 前进行 Vision Gate
- 完成声明前进行 Evidence Gate
- 为 Commit、PR、Handoff 编写 Change Narrative
- Bug 和 Regression 修复后进行 Incident Learning
- 管理过期、被替代、废弃或归档的文档生命周期
- 为长期项目沉淀可复用的工程记忆
- 将有来源支撑的行为约束晋升为 `AGENTS.md` 项目规则

## Skills

| Skill | 使用场景 |
| --- | --- |
| `using-harness` | 作为入口，判断当前工程任务应该进入哪个 Harness 工作流。 |
| `harness-start-gate` | 开始非平凡实现前，判断是否可以开工，或是否需要先澄清、检索、Vision Gate、Feature、spec、plan 或 ADR。 |
| `harness-knowledge-retrieval` | 在行动前恢复项目上下文、历史决策、Feature、ADR、Lesson 或 Evidence。 |
| `harness-doc-lifecycle` | 管理 stale、superseded、deprecated、archived 等文档生命周期。 |
| `harness-incident-learning` | Bug 或事故修复后，判断是否需要测试、门禁、Lesson、ADR 或 CI 防护。 |
| `harness-vision-gate` | 实现前，以及 Review、Merge、Done、Release 或 Handoff 前检查是否偏离原始目标。 |
| `harness-change-narrative` | 为 Commit、PR、Handoff、Release Note 或变更总结写清楚“改了什么、为什么改、为什么不选别的”。 |
| `harness-knowledge-capture` | 判断是否需要沉淀 Evidence、ADR、Lesson、Feature 状态或 Handoff 记忆。 |
| `harness-project-rules` | 判断有来源支撑的行为约束是否应该写入 `AGENTS.md` 或其他项目级 Agent 规则文件。 |

## 快速开始

对于最小项目，先复制：

```text
templates/AGENTS.md
```

然后定义三件事：

```text
1. Agent 必须遵守哪些项目规则？
2. 哪个命令可以证明项目仍然可用？
3. 完成证据应该记录在哪里？
```

对于会跨多个会话持续演进的项目，再增加：

```text
docs/BACKLOG.md
docs/features/
docs/decisions/
docs/lessons/
docs/evidence/
```

使用这些模板：

```text
templates/FEATURE.md
templates/ADR.md
templates/LESSON.md
templates/EVIDENCE.md
```

校验结构化 Harness 文档：

```bash
python scripts/knowledge_check.py --root . --docs-path docs
```

在 Review 或 CI Gate 中可以使用 strict 模式：

```bash
python scripts/knowledge_check.py --root . --docs-path docs --strict
```

## 最小采用路径

从最小闭环开始：

```text
AGENTS.md
  -> start gate
  -> verification command
    -> evidence record
      -> change narrative
        -> AGENTS.md 变更前的 project-rules gate
```

当项目复杂度上升时，再逐步加入：

```text
Feature pages
  -> ADRs
    -> Lessons
      -> document lifecycle
        -> knowledge check in CI
```

## 当前状态

项目处于早期公开整理阶段。当前目标是提供一套清晰、轻量、可复用的 Harness Skills、模板和示例。

## 设计原则

Harness 应该减少重复踩坑、重复检索和没有证据的完成声明。它不应该变成一种为每个小改动都制造文档的仪式。

## License

MIT
