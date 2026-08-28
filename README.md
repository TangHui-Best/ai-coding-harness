# AgentMentor

[English](README.en.md)

[![Knowledge checks](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml/badge.svg)](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml)

## 让每一次 AI 开发，
## 都留下下一次决策能用的工程事实。

AgentMentor 面向 Codex、Claude Code 等编码 Agent，为长期演进的代码库提供**可恢复、可解释、可验证的工程记忆**。

代码告诉我们系统现在是什么。

AgentMentor 保存代码无法可靠说明的另一部分事实：

- 这个功能要解决什么，边界在哪里；
- 当初为什么选择这个设计，又拒绝过哪些方案；
- 哪些失败已经发生过，今后不应再次重演；
- 哪些结论已经验证，验证范围和限制是什么。

下一位 Agent 不必从聊天记录、Git diff 和零散注释中猜测：

> 系统为什么这样设计？<br>
> 哪些方案已经被否定？<br>
> 这次改动真正验证过什么？

```text
Prompt 帮你表达一次需求。
工作流 Skill 帮你完成一次任务。
AgentMentor 让项目记住下一次开发仍然需要知道的事实。
```

---

## 为什么需要 AgentMentor

AI 编码模型已经很擅长实现局部需求。真正困难的是：项目经历多轮对话、多人协作、多次 review 和长期迭代后，关键判断会逐渐丢失。

测试通过，不等于做对了。

当目标已经漂移、旧规格已经失真、被拒绝的方案被重新提出，或者新的 Agent 无法理解上一位为什么这样设计时，代码和绿灯测试通常不会主动告诉你答案。

常见问题包括：

- 需求在多轮迭代中漂移，但测试仍然通过；
- 旧 Spec 或验收条件已经失效，Agent 仍然忠实执行；
- 同一功能不断补丁化，却没有人识别出原有抽象已经失效；
- Review 只看到 diff，看不到设计取舍、风险与被拒绝方案；
- Agent 宣称“已完成”，但没有可复核的验证事实；
- 新会话或新 Agent 无法恢复关键工程判断；
- 文档越来越多，却不知道哪些内容真正影响了后续开发决策。

AgentMentor 不是要求你为每个改动补齐文档。

它只在工程事实会影响未来判断时留下记录；也只在任务确实依赖历史时，召回少量直接相关的上下文。

---

## 它如何工作

```text
开发任务 + 已知改动路径
        │
        ▼
读取一次统一工程 Index
        │
        ├── Feature：目标、边界、规格、验收
        ├── ADR：设计取舍与被拒绝方案
        ├── Lesson：真实失败与预防措施
        └── Evidence：验证事实、范围与限制
        │
        ▼
模型自主规划、实现、测试与协作
        │
        ▼
仅在工程事件发生时，沉淀新的长期事实
```

AgentMentor 遵循两个原则：

1. **先精准找回，再自主工作**<br>
   对可能影响功能、规格、架构、接口、数据语义或验收的任务，主 Agent 读取一次统一 Index，并基于 Brief 自主选择需要阅读的正文，而不是扫描整套知识库。

2. **只在值得沉淀时写入**<br>
   普通小改动不需要创建文档。只有目标冲突、稳定决策、重复失败、关键交付声明等事件发生时，才记录可复用的工程事实。

Index 中没有相关条目是一个有效结果：它意味着项目历史没有必要干扰当前任务。

---

## 四类工程事实

| 文档 | 回答的问题 | 何时创建或更新 |
| --- | --- | --- |
| **Feature** | 要做什么、为什么做、边界是什么、如何验收？ | 功能需要明确规格或验收时 |
| **ADR** | 为什么选择这个方案？为什么不选其他方案？ | 决策会长期影响架构、接口、风险或成本时 |
| **Lesson** | 发生过什么失败？根因是什么？以后如何避免？ | 出现规格漂移、重复回归或可复用失败模式时 |
| **Evidence** | 哪个结论已被验证？验证了什么，尚未验证什么？ | 需要为完成、发布、交接或关键判断提供证据时 |

统一 Index 只承担轻量目录职责：它同时列出当前有效的 Feature 与已接受 ADR，帮助主 Agent 选择相关正文，而不替代正文。

---

## Feature 是功能级 SDD Spec

AgentMentor 不强制引入另一套独立的 Capability 或 Plan 文档。

在 AgentMentor 中，**Feature 就是功能级的 SDD Spec**，负责承载：

- Goal：要达成的用户或业务目标；
- Scope：范围与明确的非目标；
- Specification：行为、规则、约束、接口与失败行为；
- Acceptance：可验证的 Given / When / Then 验收场景；
- Current State：当前实现与验证状态；
- Decision Context：修改功能前需要理解的历史取舍；
- Links：关联 ADR、Lesson、Evidence 与外部规格。

如果团队同时使用 OpenSpec、Superpowers 或其他规格工具，可以在 Feature 的 Links 中关联它们；但 AgentMentor 不依赖任何外部框架，也能独立工作。

---

## 默认支持 TDD，但不制造形式主义

对于可确定性验证的行为，AgentMentor 建议让 Feature 的验收场景直接驱动测试：

```text
Acceptance Scenario
        ↓
测试名称与断言
        ↓
Red → Green → Refactor
        ↓
最终验证结果记录为 Evidence
```

这意味着：

- 验收条件不是写完就遗忘的说明文字；
- 测试不是脱离需求的技术附属品；
- Evidence 只记录最终已知事实，不重复记录每一次临时尝试。

如果某项工作不适合 test-first，例如人工体验评估、外部系统联调或探索性验证，应在 Feature 的 `Verification Strategy` 中说明替代验证方式与限制。

---

## 六个 Skill，只在需要时介入

| Skill | 作用 | 触发时机 |
| --- | --- | --- |
| `agentmentor` | 执行一次有上限的项目上下文召回 | 开始或恢复依赖项目历史的工程工作 |
| `agentmentor-intent` | 处理真实的目标、范围或边界冲突 | 需求与既有 Feature、ADR、公开边界发生冲突时 |
| `agentmentor-decision` | 记录会影响未来的稳定设计取舍 | 架构、模块边界、接口、成本或风险决策形成时 |
| `agentmentor-learning` | 将重复失败转化为可执行预防措施 | 规格漂移、回归或重复失败确实发生时 |
| `agentmentor-evidence` | 为关键结论绑定可复核验证事实 | 完成、发布、交接或重要决策声明时 |
| `agentmentor-closeout` | 压缩本次任务的已知状态 | 暂停、交接或结束任务时 |

它们不是必须依次执行的流水线。

模型应自主完成常规的拆解、编码、测试、审查与协作；AgentMentor 只在项目记忆、边界、决策与证据真正需要介入时出现。

---

## 与 OpenSpec、Superpowers 的关系

AgentMentor 不试图取代所有开发方法，而是解决一个不同的问题：

> 让 AI 开发过程中的长期工程事实可恢复、可解释、可验证。

| 工具 | 主要关注点 | 适合的场景 |
| --- | --- | --- |
| **AgentMentor** | 工程记忆、功能规格、设计理由、失败经验、验证证据 | 希望项目能跨会话、跨 Agent 持续演进，并保留“为什么” |
| **OpenSpec** | 面向变更的规格、提案、设计与任务产物 | 希望用结构化变更提案推动规格驱动开发 |
| **Superpowers** | 由组合 Skill 构成的软件开发方法与执行流程 | 希望采用一套较完整的开发、测试、审查工作法 |

OpenSpec 将规格保存在代码库中，并围绕变更组织 proposal、design、tasks 和 spec delta；Superpowers 提供从需求澄清、计划、TDD 到审查的组合式工作方法。[OpenSpec](https://openspec.dev/) · [Superpowers](https://github.com/obra/superpowers)

它们可以组合：

```text
OpenSpec / 其他工具
    └── 产出某次变更的提案或计划
                │
                ▼
AgentMentor Feature
    └── 保留长期有效的功能规格与边界
                │
                ├── ADR：长期设计取舍
                ├── Lesson：重复失败的预防
                └── Evidence：关键结论的验证事实
```

只安装 AgentMentor 也能独立工作：Feature、ADR、Lesson、Evidence 和一次精准召回已经构成完整的工程记忆闭环。

---

## 快速开始

### 1. 安装

克隆仓库：

```bash
git clone https://github.com/TangHui-Best/ai-coding-harness.git
cd ai-coding-harness
```

安装到 Codex：

```powershell
.\scripts\install.ps1 codex
.\scripts\install.ps1 -Verify codex
```

安装到 Claude Code：

```powershell
.\scripts\install.ps1 claude
.\scripts\install.ps1 -Verify claude
```

同时安装到两者：

```powershell
.\scripts\install.ps1 both
.\scripts\install.ps1 -Verify both
```

Bash 环境：

```bash
bash scripts/install.sh codex
bash scripts/install.sh --verify codex
```

安装完成后，请重启对应 Agent，使新的 Skill 元数据生效。

### 2. 从一个真实改动开始

当任务依赖项目历史、既有功能规格或设计决策时，让 Agent 使用 `agentmentor`：

```text
为“订单取消”增加库存回补。

已知可能受影响的路径：
- src/orders/
- src/inventory/
- tests/orders/
```

AgentMentor 会按以下顺序进行一次受限召回：

```text
已知路径
  → 读取统一 Index
  → 主 Agent 语义选择 0–3 个相关 Feature 与必要 ADR
  → 按需读取直接关联的 Lesson / Evidence
```

随后，模型自主完成实现和验证。

### 3. 只在事件发生时沉淀

例如：

- “订单取消是否允许已发货订单回补库存？”<br>
  如果这是长期规则取舍，记录 ADR。

- “该问题已经第三次因为异步消息重复投递而回归。”<br>
  如果形成可复用根因和防护措施，记录 Lesson。

- “此功能已通过指定集成测试，可以交付给 QA。”<br>
  如果需要让结论可复核，记录 Evidence。

无需一次性建立整套文档体系。可以从一个正在修改的 Feature 开始。

---

## AgentMentor 不做什么

AgentMentor 不会：

- 替你判断产品需求是否值得做；
- 强制每项任务进入固定的计划、委派、审查或收尾流程；
- 因为存在知识库就默认加载全部历史文档；
- 将每次聊天、每个 Git diff 或每个临时尝试都沉淀为项目记忆；
- 用文档替代测试、代码审查和真实验证；
- 用“流程完整”伪造“工程可靠”。

它只在模型无法从当前代码可靠推导、却会影响长期演进的地方，提供最小但可复用的工程事实。

---

## 校验

验证 Skill 元数据：

```powershell
python scripts\skill_metadata_check.py --root . --strict
```

验证 Index 是否已同步：

```powershell
python scripts\generate_index.py --root . --check
```

验证 AgentMentor 文档结构：

```powershell
python scripts\knowledge_check.py --root . --docs-path docs --strict
```

运行测试：

```powershell
pytest -q
```

---

## 设计演进：为什么新版选择更轻的编排

早期 AI 编程框架常用多层 Gate、预设子流程和大量系统规则，来补偿模型在任务拆分、验证和上下文保持方面的不足。

对更强的编码模型而言，重复的流程约束也会带来成本：

- 同一任务被不同 Gate 反复分类与重新判断；
- 同一批项目资料被重复读取；
- 规则之间相互重叠，挤占模型理解任务和验证代码的注意力；
- 默认工作流代替了模型本应自主完成的判断。

这不是“不要 Skill”，而是把 Skill 从**默认控制模型行为**转为**按事件提供高价值工程事实**。

Anthropic 在 Claude 5 代模型的上下文工程实践中，公开描述过将 Claude Code 系统提示词缩减超过 80%，且编码评测没有可测量损失；其方向是减少重复约束、给予模型判断空间，并通过渐进披露按需加载上下文。[The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)

验证并没有被移除。测试、lint、构建等确定性验证仍然关键；更合理的方式是在适用的任务边界触发专门能力，而不是将多个 Skill 串成每次必经的流程。[Building verification loops in Claude Code with skills](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills)

因此，AgentMentor 的选择是：

> 信任强模型处理常规推理与执行；<br>
> 把工程化约束集中在模型无法自行记住、却会影响长期演进的事实之上。

---

## 项目状态

- `v1.0.0`：旧版稳定基线，作为历史版本保留；
- `main`：承载不兼容的 AgentMentor v2 架构；
- 真实历史任务基准仍是后续质量评估工作；在完成前，不将其作为性能改善的证据。

---

## 文档

- [安装说明](INSTALL.md)
- [快速开始](docs/quickstart.md)
- [Skill 索引](docs/skill-index.md)
- [工程 Index](docs/INDEX.md)
- [新架构 Feature](docs/features/F017-agentmentor-vnext-gpt56-workflow.md)
- [核心架构决策 ADR](docs/decisions/ADR-010-agentmentor-vnext-event-triggered-memory-layer.md)

---

## License

MIT
