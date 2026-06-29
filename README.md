# AgentMentor

简体中文 | [English](README.en.md)

[![knowledge-check](https://github.com/TangHui-Best/using-agentmentor/actions/workflows/knowledge-check.yml/badge.svg)](https://github.com/TangHui-Best/using-agentmentor/actions/workflows/knowledge-check.yml)

AgentMentor 是一套面向 **Codex / Claude Code / OpenCode** 的 Agent 工程治理 Skill 套件。它的目标不是让 Agent 写更多代码，而是让 AI 辅助研发在多轮会话、多 Agent、多次 review 和长期迭代中保持可恢复、可验证、可追溯、可防复发。

```text
确认真实目标 -> 检索项目记忆 -> 做最小可验证变更 -> 用证据和知识沉淀收尾
```

## 为什么需要 AgentMentor

AI coding assistant 已经很会写代码。真正的风险通常不是“写不出来”，而是：

- 目标在多轮迭代后漂移，但测试仍然变绿。
- 旧 spec 或验收标准已经失真，Agent 仍然忠实执行。
- 同一个 Feature 反复补丁化，抽象失效却没有被识别。
- Review 只看到 diff，看不到决策、风险和被拒绝方案。
- Agent 自信宣布完成，但没有 Evidence 支撑。
- 上下文压缩或新会话后，关键工程判断无法恢复。
- 文档越写越多，却不知道哪些真正改变了后续 Agent 的判断。

AgentMentor 的核心判断是：

```text
Prompt 解决一次表达。
Skill 解决一次工作流。
AgentMentor 解决长期工程治理闭环。
```

它不是文档形式主义。真正要治理的是 Agent 时代的失控：需求是否真实、边界是否清晰、结果是否可验收、过程是否可追溯、失败后是否可恢复。

## 核心机制

AgentMentor 把长期软件工程里的关键判断拆成 Agent 可触发、可执行、可检查的控制点：

- **Gate**：在开工、实现、review、release、handoff 或完成声明前判断是否可以继续。
- **Knowledge**：从 Feature、ADR、Lesson、Evidence、AGENTS.md 中恢复历史上下文。
- **Evidence**：把完成声明绑定到可复核的验证命令、结果和限制。
- **Lifecycle**：判断旧文档是否 active、completed、superseded、deprecated 或 archived。
- **Narrative**：为 commit、PR、handoff 和 release note 说明为什么这样改。
- **Project Rules**：只把有证据、跨任务有效、会改变未来 Agent 行为的经验晋升到 `AGENTS.md`。
- **Usage Telemetry**：只记录真实影响判断或叙事的文档使用，不记录普通 read log。

## 设计原则

- Agent 时代的瓶颈不是写代码慢，而是目标漂移、虚假完成、上下文丢失、失败复发和控制面膨胀。
- AgentMentor 的价值不是制造形式文档，而是让 Agent 开发可治理、可恢复、可验证、可防复发。
- 文档的价值不在数量，而在被召回、被判断、被用于闭环。
- 代码承载“现在如何运行”；文档承载“为什么这样运行，以及未来修改时不能忘记什么”。
- 不可靠或收益不稳定的自动化，应降级为显式流程或直接删除。

## 这个仓库提供什么

- `using-agentmentor`：高召回入口 Skill，用于判断当前任务是否需要 AgentMentor 介入。
- 十一个聚焦 workflow Skills：覆盖 Start Gate、Vision Gate、Spec Drift、Delegation Gate、Knowledge Retrieval、Doc Lifecycle、Incident Learning、Readiness Dashboard、Change Narrative、Knowledge Capture、Project Rules。
- `AGENTS.md`、Feature、ADR、Lesson、Evidence 模板。
- `knowledge_check.py` / `closeout_check.py`：随 `using-agentmentor` 安装，用于校验结构化 AgentMentor 文档和 closeout block。
- 可选 Stop-only Hook Runtime 示例：Codex、Claude Code 和 OpenCode 的 Stop 示例位于 `using-agentmentor/hooks/`。
- Codex Desktop personal plugin 包：`.codex-plugin/plugin.json`、插件级 `hooks.json` / `hooks/hooks.json`、`hooks/run-agentmentor-hook.cmd`、`hook_diagnostics.py` 和 `.agentmentor/hook-events/events.jsonl` 运行痕迹；插件身份为 `agentmentor@personal`。
- `usage_record.py`：记录真实影响判断的文档 usage 事件。
- `skill_metadata_check.py`：校验 Skill metadata、触发表面和必需 bundled resources。
- 最小示例和项目级示例，方便从轻量规则逐步升级为可恢复的工程记忆。

## 12 个 Skill

| Skill | 用途 |
| --- | --- |
| `using-agentmentor` | 判断当前任务是否需要 AgentMentor，并路由到合适 workflow。 |
| `start-gate` | 在非平凡工作开始前判断能否开工，或是否需要澄清、检索、Feature、spec、plan、ADR。 |
| `vision-gate` | 校验局部实现、review、merge、done、release 或 handoff 是否仍贴合原始目标。 |
| `knowledge-retrieval` | 在行动前恢复项目上下文、历史决策、Evidence 和相关 Lesson。 |
| `doc-lifecycle` | 判断旧文档是否仍可信，或是否已 superseded、deprecated、archived。 |
| `spec-drift` | 当真实案例、验证失败或用户反馈推翻旧 spec 时，先修正认知再改代码。 |
| `delegation-gate` | 判断是否需要实现 subagent 或独立 reviewer。 |
| `readiness-dashboard` | 在 review、release、handoff 或完成前汇总 readiness、progress、maturity、blocker 和 gap。 |
| `change-narrative` | 为 commit、PR、handoff、release note 或进展说明解释改了什么、为什么这样改。 |
| `knowledge-capture` | 完成声明前判断是否需要 Feature、ADR、Lesson、Evidence 或 handoff 记忆。 |
| `incident-learning` | 把 bug、事故、补丁震荡转化成可复发防护。 |
| `project-rules` | 判断某条经验是否值得晋升为 `AGENTS.md` 等项目级 Agent 规则。 |

更多细节见 [docs/skill-index.md](docs/skill-index.md)。

## 最小安装

克隆仓库：

```bash
git clone https://github.com/TangHui-Best/using-agentmentor.git
cd using-agentmentor
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

安装后重启对应 Agent。第一次使用时，从 `using-agentmentor` 开始；它会在需要时路由到更小的 workflow Skills。

更多安装方式见 [INSTALL.md](INSTALL.md)。

## Optional Project Rules

AgentMentor 不会自动修改全局或项目级 `AGENTS.md`。当项目需要仓库级规则时，可以手动复制 bundled 模板：

```bash
cp ~/.codex/skills/using-agentmentor/assets/templates/AGENTS.md /path/to/your-project/AGENTS.md
```

Windows PowerShell：

```powershell
Copy-Item "$HOME\.codex\skills\using-agentmentor\assets\templates\AGENTS.md" "C:\path\to\your-project\AGENTS.md"
```

先定义三件事：

```text
1. Agent 必须遵守哪些项目规则？
2. 哪个命令可以证明项目仍然可用？
3. 完成证据应该记录在哪里？
```

建议长期演进项目把这些规则加入复制后的 `AGENTS.md`：

```text
- Run Start Gate before non-trivial implementation.
- If real cases, validation, or user feedback contradict an existing spec, run Spec Drift before changing code.
- If repeated patches add scenario-specific branches, pause and run Patch Churn Review before continuing.
```

再逐步增加：

```text
docs/BACKLOG.md
docs/features/
docs/decisions/
docs/lessons/
docs/evidence/
```

## 典型工作流

```text
收到任务
  -> using-agentmentor 判断是否触发 AgentMentor
  -> start-gate 判断能否开工
  -> 需要时运行 retrieval / spec drift / vision gate / delegation gate
  -> 建立或更新 Feature、spec、plan、ADR 等必要前置记忆
  -> 执行最小可验证变更
  -> 运行验证并记录 Evidence
  -> 需要交付时使用 readiness-dashboard 汇总 progress、maturity、blocker、gap
  -> 用 change-narrative 解释变更
  -> 用 knowledge-capture 判断是否允许完成声明
```

不是每个任务都要完整走一遍。AgentMentor 的目标是选择足够轻的流程，保护未来真的需要恢复、验证或解释的上下文。

## Hook 边界

Hooks 是可选增强，Skills-only 安装是基线。

当前默认 hook 示例只启用 **Stop-time completion check**：当 Agent 准备说 done、fixed、verified、ready 等完成类表达时，检查 closeout 和 Evidence 状态。

AgentMentor 不再默认提供 `pre-compact` / `session-start` 自动恢复 hook。平台 compaction 交给平台本身；如果需要交接，应显式要求 Agent 写 handoff。

Codex hook 安装或更新后，可以运行诊断：

```powershell
python "$HOME\.codex\skills\using-agentmentor\scripts\hook_diagnostics.py" codex --project-root "C:\path\to\your-project"
```

如果诊断提示 Stop runner warning，说明该机器上的可选 Stop hook 尚未被证明；继续使用 Skills-only closeout 即可。

## 与 Superpowers / OpenSpec 的区别

| 方案 | 主要解决的问题 | 更像什么 |
| --- | --- | --- |
| Superpowers | 让 Agent 在单次任务中遵守更好的工作方法 | 工作流纪律层 |
| OpenSpec | 让需求变更围绕 spec、proposal、tasks、archive 被组织 | 规格治理层 |
| AgentMentor | 让目标、证据、决策、失败、恢复和规则形成长期闭环 | 工程治理层 |

Superpowers 让 Agent 更会按流程做事。OpenSpec 让需求变化更有结构。AgentMentor 关心的是：这些流程、规格、证据和失败经验是否能改变未来 Agent 的判断。

## 仓库结构

```text
skills/       可安装的 Agent workflow Skills，其中 using-agentmentor 携带 bundled scripts/templates
hooks/        Codex 插件级 Stop hook wrapper 和示例配置
docs/         概念、架构、Feature、ADR、Lesson、Evidence
templates/    可复用文档模板
examples/     最小 AgentMentor 和项目级治理示例
scripts/      轻量校验和 usage 记录工具
```

## 校验

校验 Skill metadata：

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills
```

校验结构化治理文档：

```bash
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs
```

准备更严格的 review 或 CI gate 时：

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills --strict
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs --strict
```

## 示例

- [最小示例](examples/minimal-harness/README.md)：只保留最小规则、验证和 Evidence 习惯。
- [项目级示例](examples/project-harness/README.md)：展示 Feature、ADR、Lesson、Evidence 如何协作。

## 文章

- [AgentMentor：把 AI Agent 纳入可治理的软件开发流程](docs/articles/agentmentor-governable-ai-agent-development-flow.md)

## 当前状态

AgentMentor 仍处于快速塑形阶段。当前重点是把 AI 辅助开发从“靠长 Prompt 维持秩序”推进到“靠 Gate、Evidence、Knowledge 和 Lifecycle 持续治理”的工程系统。

## License

MIT
