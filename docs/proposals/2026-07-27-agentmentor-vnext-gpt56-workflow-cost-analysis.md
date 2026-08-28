# GPT-5.6 后 AgentMentor 小改动变慢的原因分析

## 文档定位

这是一份 AgentMentor 大版本升级前的**问题分析材料**，用于解释当前工作流为什么在 GPT-5.6 上产生明显的开发摩擦，并为 vNext 的范围取舍提供依据。

它不是已经生效的架构决策，不修改现行 workflow，也不承诺兼容旧版 Skill 或知识文档。

## 分析范围与非范围

本材料只分析两类因素：

- GPT-5.6 的原生推理、规划、验证与任务编排能力提升；
- 当前 AgentMentor Skill 的默认路由、Gate 与上下文加载设计。

明确不纳入本次归因：

- 项目历史文档的格式质量、缺字段或迁移问题；
- Markdown 扫描、Python 校验脚本或磁盘 I/O 的原始执行耗时；
- 可选 Hook 的性能影响。当前默认 Hook 设计本就不应在每次工具调用后运行全量知识校验。

因此，本文讨论的是**模型推理与流程编排的成本**，而不是文档治理质量问题。

## 结论

AgentMentor 的原始价值是为能力有限的模型补齐工程控制：任务拆解、历史检索、方向校验、委派判断、完成声明和经验沉淀。

GPT-5.6 已能原生完成其中相当大一部分判断。问题不是模型变慢，而是 Skill 仍把这些判断串成默认且强约束的流水线。模型的推理与遵从能力越强，越会认真完成每一层的条件判断、解释和前置动作；一次很小的代码改动因而被放大为一次完整的流程自审。

```text
小改动
  → 阅读入口规则并判断是否触发 AgentMentor
  → Start Gate 分类与风险判断
  → 检索、Vision、Delegation、Feature/ADR 等前置判断
  → 实现与验证
  → Readiness、Evidence、Knowledge Capture、Narrative 等收尾判断
```

真正消耗时间的不是“改代码”，而是模型反复回答“我现在是否还需要进入下一道流程”。

## 原始设计为什么曾经合理

现行架构将 AgentMentor 定义为工作流、知识、Gate、Readiness、Evidence、Narrative、Lifecycle 和项目规则的组合。`docs/workflow.md` 也明确规定：非平凡实现先过 Start Gate，按风险检索上下文，必要时建立前置锚点，完成后再进入验证、Readiness、知识沉淀和叙事。

在较弱模型阶段，这套设计有效解决了几个真实问题：

- 模型会直接编码而不澄清目标或检索历史；
- 模型不会稳定判断何时需要 Feature、ADR 或证据；
- 模型容易遗漏验证、交接和失败复盘；
- 复杂任务可能未经判断就默认单 Agent 执行。

例如 ADR-001 引入 Start Gate，正是为了在代码修改前明确“能否开始”；ADR-003 要求复杂任务在 Start Gate 返回 `ready` 前给出 Delegation decision；ADR-006 则要求把会改变第一步行为的规则保留在 Skill 热路径中。这些决策在当时是对模型遗漏和失控风险的直接补偿。

## GPT-5.6 带来的设计错位

GPT-5.6 的提升并不意味着不需要工程治理，而是改变了治理最应放置的位置。

模型现在通常能够在正常开发循环中自行完成：

- 根据目标和代码范围拆分任务；
- 判断是否应该查找历史设计；
- 判断是否需要并行、独立复核或保持单 Agent；
- 选择验证方式并解释验证边界；
- 判断某次改动是否形成了值得沉淀的设计决策或失败模式。

但现有 AgentMentor 仍要求模型先显式证明自己做过这些判断。于是产生两层决策：模型原生决策一次，Skill 流程再要求决策一次。

```text
模型原生：这个改动是否需要检索、拆分、验证？
Skill 规则：请先证明是否需要检索、Vision、Delegation、Feature、Evidence……
```

这不是更高的工程质量，而是同一类认知工作被重复记账。

## 造成小改动变慢的具体设计问题

### 1. 默认路径是串行 Gate，而不是按事件触发的治理

`using-agentmentor` 将非平凡工作定义为 Entry Gate 和 Exit Gate 协议。Start Gate 又将检索、Spec Drift、Vision Gate、Feature、spec、plan、ADR、Backlog、handoff 等列为可能的前置结果；对 `non-trivial` 和 `high-risk` 工作，必须先给出明确的 Delegation decision。

这使“修改代码”天然成为“启动治理状态机”的入口。即使最终结论是无需正式产物，模型仍需先证明它为何无需这些产物。

更合适的关系应是：

```text
开发任务
  → 默认：模型直接计划、实现、验证
  → 仅在出现决策、失败复盘、交接、发布或长期证据需求时，触发治理动作
```

治理事件应触发记忆，而不是让每个开发任务先穿过完整治理链。

### 2. 多个 Skill 对同一状态进行重复判断

当前模块在单独看时边界清晰，但串联后判断对象高度重叠：

| Skill / Gate | 原始目的 | 与 GPT-5.6 原生能力或其他 Gate 的重叠 |
| --- | --- | --- |
| Start Gate | 判断能否开始 | 与正常任务理解、计划和风险判断重叠 |
| Vision Gate | 防止偏离用户意图 | 与需求理解、实施前计划校验重叠 |
| Delegation Gate | 判断是否委派 | 与模型的任务拆分和并行判断重叠 |
| Readiness Dashboard | 汇总交付状态 | 与常规验证结果整理、Knowledge Capture 部分重叠 |
| Change Narrative | 解释取舍与历史 | 与普通开发汇报不应绑定，只适合提交、PR、交接 |
| Knowledge Capture | 保存长期知识 | 有保留价值，但不应把每次改动都升级为完整 closeout |

典型重复是：Start Gate 先要求 Delegation decision，Readiness 在收尾时再检查该决策是否缺失；入口、检索、Feature 和收尾规则又分别要求模型判断历史知识是否影响当前任务。每一次判断都需要读取规则、回忆任务状态、生成解释，且很难复用前一层的自然语言结论。

### 3. 自然语言路由把 Skill 变成高成本状态机

AgentMentor 的关键控制不是一个确定性命令，而是大量自然语言条件，例如“non-trivial”“可能影响未来恢复”“可能需要委派”“可能发生意图漂移”。

这类规则必须由模型解释。GPT-5.6 的高遵从性会让它倾向于采取更保守的路径：只要任务有一点跨文件、行为变化或历史关联的可能，就会认真考虑进入下一层 Gate，而不是快速视为例外。

结果是每个 Skill 都需要重新建立状态：

```text
当前任务是什么？
它属于什么风险等级？
前一层是否已完成？
下一层是否仍然需要？
我是否有资格声明完成？
```

流程的成本因此主要是推理轮次和上下文注意力，而不是脚本运行时间。

### 4. 入口 Skill 的职责过重，启动即加载治理框架

`using-agentmentor` 名义上是轻量路由器，但其热路径同时承载：触发判定、Entry/Exit Gate、十一类路由顺序、文档放置规则、收尾收敛、Hook 边界、校验入口和多条禁止规则。

ADR-006 选择把会改变第一步行为的约束保留在热路径，这降低了弱模型遗漏关键约束的风险；但在 GPT-5.6 下，热路径已从“必要护栏”膨胀为“每次开发都需要理解的治理框架”。

因此，哪怕最终判断为小改动，模型也先支付了理解整个路由体系的成本。

### 5. 上下文检索仍是模型主导的流程选择，而不是确定性服务

历史设计理由、放弃方案和失败经验仍然是 AgentMentor 必须保留的价值，不能因为模型变强而删除。

问题在于，当前检索顺序是：模型先判断是否需要历史，再依据 Feature、文件名、链接和文本搜索选择候选文档；之后不同 Gate 还可能再次要求关联 Feature、ADR、Lesson 或 Evidence。

这造成两种重复：

- 重复判断“是否需要检索”；
- 重复阅读“哪些历史资料真正改变当前决策”。

vNext 应把检索收敛为一个一次性、可度量的 `agentmentor context`：输入任务语义和已知改动路径，按“路径匹配 → 当前 Capability → 直接关联 ADR / Lesson / Evidence → 一跳历史链接”的顺序返回最多 3 份上下文。模型随后直接开发，而不是在多道 Gate 中重新猜测搜索范围。

### 6. 把“需要沉淀的事件”误建模为“每次开发都要收尾的步骤”

ADR、Lesson、Evidence 和 Narrative 的价值没有消失，但它们适用于不同事件：

- 发生稳定且可复用的架构取舍时，记录 ADR；
- 修复了可复发失败模式时，记录 Lesson；
- 需要支撑发布、交接或完成声明时，记录 Evidence；
- 需要提交、PR、发布说明或交接时，写 Narrative。

当前 Skill 设计过度强调每次改动的 Exit Gate 和完成声明，使模型容易把“我已完成本次代码验证”与“我必须完成一整套长期知识治理”绑定。

这会让正常开发循环频繁中断，也会让模型将注意力从代码、测试和用户结果转移到工作流状态。

## 不应得出的结论

以下判断同样需要避免：

- 不能据此认为 GPT-5.6 不需要任何 Harness；复杂任务仍需要可恢复的决策、证据和边界。
- 不能简单把 12 个 Skill 合并成 4 个更长的 Skill；这只会把重复路由藏进更大的提示词。
- 不能删除历史召回；应删除的是每次都由模型从零判断如何召回的成本。
- 不能把所有控制改成 Hook 或校验脚本；脚本适合确定性验证，不适合替代模型对设计和风险的判断。
- 不能仅凭主观体感给各原因分配精确耗时比例；vNext 需要真实任务基准验证。

## 对 vNext 的设计要求

大版本升级的目标不应是“少几个 Skill”，而是改变 AgentMentor 的工作位置：从模型的逐步编排器，改为模型的按需上下文和长期记忆层。

```text
旧：任务 → 多层 Gate 判断 → 开发 → 多层 Gate 收尾
新：任务 + 路径 → 一次 context → 模型自主开发与验证 → 仅按事件沉淀
```

vNext 至少应满足：

1. 默认不强制 Start、Vision、Delegation、Readiness 等独立 Gate；这些判断回归 GPT-5.6 的原生规划能力。
2. 提供独立工作的 `agentmentor context`，以准确、低成本的历史召回替代多轮自然语言检索判断。
3. 保留 Capability、ADR、Lesson、Evidence 四类不可替代的长期知识，但仅在对应事件发生时写入。
4. 保留发布、交接、重大决策和高风险变更所需的明确验证；它们是按阶段触发的控制，不是日常开发的默认流水线。
5. 将“是否变快”转化为可验证目标：使用 10–20 个真实历史改动，测量 Top-3 召回、无关文档数、加载文本量、无命中时的快速退出，以及端到端完成时间。

## 与现有决策的关系

这份材料不是对 ADR-001、ADR-003 或 ADR-006 的简单否定。它的判断是：这些决策针对的模型能力边界已发生变化，因此 vNext 需要重新定义“哪些控制应留在热路径，哪些控制应降级为按需能力”。

后续若据此实施 vNext，应单独创建新的 ADR，明确哪些既有决策被替代、哪些长期记忆能力保留，以及如何用基准结果证明新的工作流既更快又没有丢失关键工程控制。

## 关联材料

- [Concept](../concept.md)
- [Architecture](../architecture.md)
- [Workflow](../workflow.md)
- [ADR-001: Start Gate Before Implementation](../decisions/ADR-001-start-gate-before-implementation.md)
- [ADR-003: Explicit Delegation Decision Before Complex Work](../decisions/ADR-003-explicit-delegation-decision-before-complex-work.md)
- [ADR-006: Skill Progressive Disclosure Boundary](../decisions/ADR-006-skill-progressive-disclosure-boundary.md)
- [F009: Feature Intake Governance](../features/F009-feature-intake-governance.md)
- [F010: Goal-Driven Feature Flow](../features/F010-goal-driven-feature-flow.md)
