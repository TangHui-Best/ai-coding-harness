# AI Coding Harness

简体中文 | [English](README.en.md)

[![knowledge-check](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml/badge.svg)](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml)

AI Coding Harness 是一套面向 **Codex / Claude Code** 的 Skill 与工程协作模板。它要解决的不是“让 Agent 多写一点代码”，而是让 AI 辅助研发在多轮会话、多 Agent、多人协作中仍然可追溯、可验收、可恢复。

如果你第一次打开这个仓库，可以把它理解成一套给 AI 编程工作的“工程护栏”：

```text
先确认目标 -> 再读取上下文 -> 再执行最小变更 -> 最后用证据收尾
```

它帮助 Agent 在关键节点停一下：需求是否真实？边界是否清晰？结果如何证明？失败后能不能恢复？经验是否沉淀成下一次不会再踩的机制？

## 适合谁

- 正在用 Codex、Claude Code 或类似 Agent 做真实项目开发的人
- 希望 AI 不只是“会写代码”，还要能记住项目规则、交接上下文、说明变更原因的团队
- 已经遇到过这些问题的人：会话一换就丢上下文、完成声明缺少证据、PR 解释不清、同类问题反复修补、多 Agent 协作难以收敛

如果你的项目只是一次性实验，可能只需要其中的少量 Skill。  
如果你的项目会持续演进，Harness 会更有价值。

## 为什么需要 Harness

AI coding assistant 的代码产出速度已经很快。真正的瓶颈通常不再是“能不能写”，而是：

- Agent 是否知道这个项目长期有效的规则？
- 新会话能否恢复上一次为什么这么做？
- 完成声明是否有实际验证证据？
- 决策、否定方案和风险是否被保留下来？
- Bug 或事故修复后，是否形成可复用的防护？
- 人、Agent、多 Agent 是否能协作而不丢状态？

Harness 的核心判断是：

```text
Prompt 解决一次表达。
Skill 解决一次工作流。
Harness 解决长期工程系统行为。
```

它不是文档形式主义，而是一套轻量控制回路：

```text
Run -> Trace -> Diagnose -> Patch Harness -> Eval -> Deploy -> Learn
```

每一次 AI 辅助任务结束后，系统都应该比开始时更可恢复、更可验证，也更不容易重复踩坑。

## 这个仓库提供什么

- `using-harness`：高召回入口 Skill，用于判断当前任务是否需要 Harness 介入
- 十个聚焦的 `harness-*` Skills：覆盖开工门禁、委派决策、知识检索、文档生命周期、事故学习、愿景校验、就绪状态、变更叙事、知识沉淀、项目规则晋升
- `AGENTS.md`、Feature、ADR、Lesson、Evidence bundled 模板
- `knowledge_check.py` / `harness_closeout_check.py`：随 `using-harness` 安装，用于校验结构化 Harness 文档和 closeout block
- `skill_metadata_check.py`：校验 Skill metadata、触发表面和必需 bundled resources
- 最小示例和项目级示例，方便从轻量使用逐步升级

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

安装后重启对应 Agent。第一次使用时，从 `using-harness` 开始；它会在需要时路由到更小的 `harness-*` Skills。

更多安装方式见 [INSTALL.md](INSTALL.md)。

## 最小使用路径

先把项目规则模板复制到你的项目：

```bash
cp ~/.codex/skills/using-harness/assets/templates/AGENTS.md /path/to/your-project/AGENTS.md
```

Windows PowerShell：

```powershell
Copy-Item "$HOME\.codex\skills\using-harness\assets\templates\AGENTS.md" "C:\path\to\your-project\AGENTS.md"
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

使用 `using-harness/assets/templates/` 中的 bundled 模板：

```text
using-harness/assets/templates/FEATURE.md
using-harness/assets/templates/ADR.md
using-harness/assets/templates/LESSON.md
using-harness/assets/templates/EVIDENCE.md
```

## 典型工作流

```text
收到任务
  -> using-harness 判断是否触发 Harness
  -> harness-start-gate 判断能否开工
  -> 需要时检索项目知识、澄清目标或建立 Feature / spec / plan / ADR
  -> 执行最小可验证变更
  -> 运行验证命令并记录 Evidence
  -> 需要交付、Review 或交接时生成 readiness / change narrative / knowledge capture
```

这条链路不是每个任务都完整走一遍。Harness 的目标是选择足够轻的流程，保护那些未来真的需要恢复、验证或解释的上下文。

## Skills 一览

| Skill | 用途 |
| --- | --- |
| `using-harness` | 判断当前任务是否需要 Harness，并路由到合适的工作流。 |
| `harness-start-gate` | 在非平凡工作开始前判断是否需要澄清、检索、愿景校验、Feature、spec、plan 或 ADR。 |
| `harness-delegation-gate` | 判断是否需要请求实现子 Agent 或独立 Reviewer。 |
| `harness-knowledge-retrieval` | 在行动前恢复项目上下文、历史决策和相关证据。 |
| `harness-doc-lifecycle` | 处理 stale、superseded、deprecated、archived 等文档生命周期状态。 |
| `harness-incident-learning` | 把 Bug、事故和补丁震荡转化为可复用防护。 |
| `harness-vision-gate` | 在实现、Review、Merge、Done 或 Handoff 前校验是否仍然贴合原始目标。 |
| `harness-readiness-dashboard` | 在 Review、Release、Handoff 或完成声明前汇总门禁、证据、风险和阻塞项。 |
| `harness-change-narrative` | 为 commit、PR、交接、发布说明或变更总结写清楚“改了什么，为什么这么改”。 |
| `harness-knowledge-capture` | 判断是否需要沉淀 Feature、ADR、Lesson、Evidence 或 Handoff 记忆。 |
| `harness-project-rules` | 判断某条经验或约束是否应该晋升到 `AGENTS.md` 等项目级 Agent 规则。 |

更多说明见 [docs/skill-index.md](docs/skill-index.md)。

## 仓库结构

```text
skills/       可安装的 Agent 工作流 Skills，其中 using-harness 携带 bundled scripts/templates
docs/         概念、架构和工作流说明
templates/    可复用文档模板
examples/     最小 Harness 和项目级 Harness 示例
scripts/      轻量校验工具
```

## 校验

校验 Skill metadata：

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills
```

校验结构化 Harness 文档：

```bash
python skills/using-harness/scripts/knowledge_check.py --root . --docs-path docs
```

准备更严格的 Review 或 CI gate 时：

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills --strict
python skills/using-harness/scripts/knowledge_check.py --root . --docs-path docs --strict
```

## 示例

- [最小 Harness 示例](examples/minimal-harness/README.md)：只保留最小规则、验证和 Evidence 习惯
- [项目级 Harness 示例](examples/project-harness/README.md)：展示 Feature、ADR、Lesson、Evidence 如何协作

## 设计原则

Harness 应该减少重复检索、重复踩坑和没有证据的完成声明。它不应该变成一种为每个小改动都制造文档的仪式。

先知识沉淀，再任务编排。  
先门禁，再自动化。  
先治理，再扩大规模。

## 状态

这个项目仍处于早期公开塑形阶段。当前目标是提供一个清晰、最小、可复用的 Harness Skill 套件和模板，让更多 AI 辅助研发实践可以从“靠一段长 Prompt 撑住”走向“靠工程机制持续演进”。

## License

MIT
