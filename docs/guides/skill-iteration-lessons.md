# Harness Skill 迭代复盘：渐进式加载不能隐藏热路径约束

## 背景

最近一轮 Harness skill 迭代一度很折腾：我们以为会话卡住可能来自 Harness skill 过重，于是借鉴业界 Skill 最佳实践，把大量细节从主 `SKILL.md` 移到 `references/`，并强调脚本默认只执行、不读取源码。

这个方向本身是对的。Agent 工作时上下文有限，Skill 如果每次都加载完整矩阵、案例、脚本细节和历史解释，会让简单任务也背上复杂成本。真正的问题不在于“渐进式加载”，而在于我们没有先区分哪些内容可以延迟加载，哪些内容必须在热路径中可见。

后续发现，会话卡住并不是 Harness skill 本身导致的。因此部分瘦身属于误判后的过度优化。更重要的是，过度瘦身让一些关键行为约束从写入期热路径中消失了。

## 这次暴露的问题

典型症状是 Feature 文档路径漂移。

Harness 的官方 Feature 应该写在：

```text
docs/features/Fxxx-slug.md
```

但真实开发中，Agent 容易沿用 Superpowers 的旧规范，把 spec 或 plan 写到：

```text
docs/superpowers/specs/YYYY-MM-DD-topic-design.md
docs/superpowers/plans/YYYY-MM-DD-topic.md
```

这些 spec/plan 可以作为 Feature 的 linked material，但它们不是 Harness Feature 本身。Harness 需要一个稳定的 Feature 聚合页来承载 Vision Anchor、状态、验收标准、Patch History、ADR/Lesson/Evidence 链接和恢复入口。

当 canonical placement 主要存在于 ADR、Evidence、validator 或 reference 中，而不在 `harness-knowledge-capture` 的主路径里时，Agent 可能等到 `knowledge_check.py --strict` 才发现自己写错了位置。校验能兜底，但不能替代写入前的判断。

## 根因

这次根因可以概括为一句话：

> 我们把降低上下文成本，误扩展成了隐藏行为约束。

脚本源码默认不读，是合理的。完整矩阵按需读，也是合理的。边界案例放 reference，也是合理的。

但以下内容不能只放在延迟层：

- 是否可以开始实现。
- 是否必须先跑 Start Gate、Vision Gate、Knowledge Retrieval 或 Delegation Gate。
- 是否必须创建或更新 Feature。
- 官方 artifact 应该写到哪里。
- 是否可以声明 complete、ready、verified、handoff。
- 非 tiny bugfix 是否必须做 Feature attribution。
- Patch History 达到阈值时是否必须暂停补丁并做归零审视。

这些规则一旦不可见，Agent 的第一步就可能错。

## 三层设计原则

后续 Harness skill 应采用三层分工。

### 1. 主 SKILL.md：热路径约束

主 `SKILL.md` 不需要写所有细节，但必须让 Agent 不读 reference 也能避免错误开始。

应该保留：

- Trigger：什么时候必须启用这个 Skill。
- Stop condition：什么时候不能继续。
- Next action：下一步应该路由到哪个 gate 或 artifact。
- Canonical placement：官方文档写到哪里。
- Completion permission：什么时候允许说完成。
- Guardrail：哪些情况必须降级为 blocked / conditional / needs retrieval / needs feature。

判断标准很简单：

> 如果这条规则会改变 Agent 第一行动，它必须在主 `SKILL.md`。

### 2. references/：细则、矩阵、案例

`references/` 适合承载：

- 详细决策矩阵。
- 完整 checklist。
- fallback search patterns。
- row-by-row readiness dashboard。
- routing fixtures。
- 示例、边界案例和解释性材料。

这些内容对复杂任务很有用，但不应该成为每次启动任务都必须读的负担。

### 3. scripts/：确定性校验

脚本负责机器可验证的规则：

- Markdown frontmatter 是否完整。
- `doc_kind` 是否允许。
- artifact 是否在 canonical directory。
- Feature refs 是否可解析。
- closeout block 结构是否完整。
- Skill metadata 是否满足安装和发布要求。

脚本的原则是 execute-first：

```text
先知道怎么运行。
失败、调试、编辑或审查时再读源码。
```

不要为了理解流程默认读取脚本源码，也不要把脚本当作唯一规则来源。

## 反模式

### 反模式一：只靠 validator 兜底

Validator 能阻止错误合入，但不能指导 Agent 第一步做对。一个 Harness artifact 写错路径后再失败，已经浪费了上下文、时间和注意力。

### 反模式二：把 spec/plan 当 Feature

Spec 和 plan 是材料，不是 Feature 聚合页。

Feature 负责交付边界和恢复入口；spec 负责详细需求；plan 负责执行路线。把三者混在一起，会让后续 retrieval、patch attribution 和 Evidence 链接都变得不稳定。

### 反模式三：为了瘦身删除 Gate 心智模型

Entry Gate / Exit Gate 不是文档仪式，而是 Agent 工作的状态机。

Entry Gate 防止直接开工；Exit Gate 防止“测试过了就说完成”。如果主 Skill 删除这两个概念，Agent 很容易退回普通 coding assistant 的行为模式。

### 反模式四：把所有经验写进 AGENTS.md

不是所有经验都应该升级成项目级规则。AGENTS.md 应该保留少量跨任务、可执行、可验证、值得每次加载的行为约束。更细的原因、权衡和案例应该放在 Lesson、ADR、Evidence 或 guide 中。

## 推荐迭代流程

后续修改 Harness skill 时，建议按这个顺序走：

1. 先判断这是 bug、设计决策、经验教训还是对外说明。
2. 如果是失败模式，写 Lesson。
3. 如果是长期设计取舍，写 ADR。
4. 如果要分享方法论，写 guide。
5. 如果会影响未来 Agent 行为，再考虑是否通过 `harness-project-rules` 提升到 AGENTS.md。
6. 修改 Skill 时，把热路径约束放主 `SKILL.md`，把细则放 reference。
7. 给关键热路径约束加结构性测试。
8. 跑 `knowledge_check.py --strict` 和 `skill_metadata_check.py --strict`。

## 可复用判断题

每次准备把主 Skill 的内容移到 reference 前，问这些问题：

- Agent 不读 reference 时，第一步会不会走错？
- 这条规则是否决定能不能开始实现？
- 这条规则是否决定官方 artifact 写在哪里？
- 这条规则是否决定能不能说完成？
- 这条规则是否决定 bugfix 是否需要 Feature attribution？
- 这条规则是否决定 patch churn 是否必须暂停？

只要有一个答案是“是”，它就不是普通细节，而是热路径约束。

## 最终原则

渐进式加载不是把重要规则藏起来，而是让 Agent 在正确的时刻读取正确粒度的信息。

主 Skill 负责不走错路，reference 负责走复杂路时不迷路，script 负责最后可验证。

这三层同时存在，Harness 才能既轻，又稳。
