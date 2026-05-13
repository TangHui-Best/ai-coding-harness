# AI Coding Harness

[English](README.md) | 简体中文

[![knowledge-check](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml/badge.svg)](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml)

AI Coding Harness 是一个面向 **Codex / Claude Code 的 Skill 套件**，用于把 AI 辅助研发中的门禁、项目记忆、验证证据、变更叙事、事故学习和交接流程沉淀成可复用工作流。

如果你是在 GitHub 上第一次看到这个仓库，最快路径是：

```text
安装 Skills -> 复制 AGENTS.md 模板 -> 运行一次校验命令
```

Codex 和 Claude Code 的安装命令见 [INSTALL.md](INSTALL.md)。

## 30 秒安装

克隆仓库：

```bash
git clone https://github.com/TangHui-Best/ai-coding-harness.git
cd ai-coding-harness
```

安装到 Codex：

```bash
bash scripts/install.sh codex
```

安装到 Claude Code：

```bash
bash scripts/install.sh claude
```

Windows PowerShell：

```powershell
.\scripts\install.ps1 both
```

安装后重启对应 Agent。入口 Skill 是 `using-harness`，它会在需要时路由到更小的 `harness-*` Skills。

## 为什么需要它

AI coding assistant 已经可以很快地产出代码，但“写得快”不等于“系统变强”。

真实项目里，更棘手的问题通常不是“Agent 会不会写代码”，而是：

- Agent 是否知道项目长期规则？
- 新会话能否恢复上下文？
- 完成声明是否有 Evidence 支撑？
- 决策和被否决的方案是否被保留下来？
- 事故和缺陷是否会沉淀成可复用的防护？
- 人和 Agent、多 Agent 之间能否协作而不丢状态？

这个仓库提供的是一套轻量 AI 辅助研发 Harness，让重复出现的协作经验变成可安装、可验证、可迭代的 Skill 和工程记忆。

## 核心观点

```text
Prompt 解决单次表达。
Skill 解决单次工作流。
Harness 解决长期工程系统行为。
```

Harness 不是文档形式主义，而是一个控制回路：

```text
Run -> Trace -> Diagnose -> Patch Harness -> Eval -> Deploy -> Learn
```

真正的问题是：每一次 AI 辅助任务结束后，工程系统是否变得更可恢复、更可验证，并且更不容易重复踩坑。

## 这个仓库提供什么

- 一个入口 Skill：`using-harness`
- 十个聚焦的 Harness Skills：开工门禁、委派决策、知识检索、文档生命周期、事故学习、愿景校验、就绪状态面板、变更叙事、知识沉淀、项目规则晋升
- Feature、ADR、Lesson、Evidence、AGENTS 指令模板
- `knowledge_check.py`：校验结构化 Harness 文档
- `skill_metadata_check.py`：校验 Skill metadata 和触发表面
- 最小示例和项目级示例

## 仓库结构

```text
skills/       可安装的 Agent 工作流 Skills
docs/         概念、架构和工作流说明
templates/    可复用文档模板
examples/     最小 Harness 和项目级 Harness 示例
scripts/      轻量校验工具
```

## Skill 激活模型

Harness Skills 面向渐进式加载设计。Agent 在决定是否加载完整 `SKILL.md` 前，往往只能看到 Skill 名称和 description，所以触发关键规则既写在 frontmatter description 里，也写在 Skill 正文里。

`using-harness` 是高召回入口，用于非平凡工程任务、多文件 bugfix、行为变更、commit、PR、handoff 和完成声明。它会先运行轻量 Harness Presence Check；如果当前任务不需要 Harness，就明确退出。聚焦的 `harness-*` Skills 也带有独立触发描述，因此当任务边界很明确时可以直接激活。

## 快速开始

先安装 Skill 套件。然后把 Agent 规则模板复制到你的项目：

```bash
cp templates/AGENTS.md /path/to/your-project/AGENTS.md
```

Windows PowerShell：

```powershell
Copy-Item ".\templates\AGENTS.md" "C:\path\to\your-project\AGENTS.md"
```

然后在 `AGENTS.md` 中定义三件事：

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

校验 Skill metadata：

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills
```

校验结构化 Harness 文档：

```bash
python scripts/knowledge_check.py --root . --docs-path docs
```

## 设计原则

Harness 应该减少重复检索、重复踩坑和没有证据的完成声明。它不应该变成一种为每个小改动都制造文档的仪式。

先知识沉淀，再任务编排。先门禁，再自动化。先治理，再扩大规模。

## License

MIT
