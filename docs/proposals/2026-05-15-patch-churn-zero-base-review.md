# Patch Churn 与归零审视：Harness Skill 迭代方案

## 背景

F018 的连续修补暴露了一个 Harness 当前没有显式捕捉的失控信号：同一个 Feature 在验收后持续出现同类问题，Agent 仍沿着既有方案继续打补丁，直到人工提出“归零思维”后才重新审视初始抽象是否错误。

这类问题不是普通 bug，也不是单次测试遗漏。它代表一种更危险的模式：

```text
测试持续变绿，但真实验收持续暴露同类失败；
补丁持续增加，但系统模型没有收敛；
Agent 继续修局部症状，却没有质疑原始方案。
```

F018 的具体表现是：F018.1 到 F018.7 逐步修复触发、展示、格式、流式边界、Composer 过滤等问题，直到 F018.7 才明确根因是 `retrieved candidate != accepted evidence`。也就是说，前面的补丁大多在下游修症状，真正需要前移的是证据合同边界。

## 目标

本次 Harness 迭代不应只是增加一条“修三次就停”的机械规则，而应建立一个跨 skill 的失控检测机制：

```text
Patch Churn / Zero-Base Review Gate
```

它的目标是让 Agent 在补丁震荡出现时主动暂停，回到 Feature 原始目标、领域模型、架构边界和验收证据，判断当前工作到底是在修实现，还是在替错误抽象续命。

## 核心原则

### 1. 补丁震荡本身就是证据

当同一 Feature 多轮补丁仍不收敛时，不要把每个失败都看作孤立缺陷。补丁链条本身可能证明：

- 初始需求理解有偏差。
- 验收标准压缩了真实用户痛点。
- 架构边界放错了层级。
- 规则逻辑正在枚举开放场景。
- 测试覆盖的是局部行为，不是系统不变量。

### 2. 阈值是提示，不是替代判断

“三轮补丁”可以作为默认触发阈值，但不能成为唯一条件。更可靠的触发信号是补丁形态：

- 新增越来越多关键词、规则分支或场景特例。
- 失败现象不同，但根因疑似相同。
- 每次修复都在更下游过滤、兜底或清洗。
- 测试通过后，手工验收仍暴露同类问题。
- 新补丁增加复杂度，但没有减少模型不确定性。

### 3. 归零不是重写一切

归零审视不是默认推翻 Feature，也不是要求大重构。它是一道判断门：

```text
当前方案是否仍然是解决原始问题的最小清晰路径？
```

可能结论包括：

- 继续当前方案，但补一个缺失测试。
- 保留主架构，只把边界前移。
- 写 ADR 记录新的架构判断。
- 拆出后续 Feature，而不是继续扩大当前 Feature。
- 停止补丁，重新设计核心抽象。

## 需要改哪些 Skill

### using-harness

定位：高召回入口。

建议改动：

- 在 Harness Presence Check 中加入 patch churn / repeated fix iteration 信号。
- 在 Routing 中明确：当用户提到连续补丁、反复修、Fxxx.n、多轮验收不过、规则越补越多时，先路由到 `harness-incident-learning`，必要时再进入 `harness-vision-gate`。

建议触发文案：

```text
- The user reports repeated patch iterations, patch churn, Fxxx.n follow-ups, recurring validation failures, or rule/keyword branches growing without convergence.
```

### harness-start-gate

定位：非平凡工作开工前判断是否能继续。

建议改动：

- 在 Risk Triggers 中加入补丁震荡触发器。
- 在 Outcomes 中不新增复杂状态，复用 `needs retrieval`、`needs vision gate`、`needs ADR`。
- 在 Boundaries 中强调：Feature 处于 patch churn 状态时，不得直接继续实现新补丁。

建议问题：

```text
- Is this a new coherent change, or another patch in a repeated fix chain?
- Does the new patch reduce system complexity, or add another scenario-specific branch?
- Has the Feature crossed the project's patch-churn threshold for zero-base review?
```

### harness-vision-gate

定位：防止方向跑偏。

建议改动：

- 在 Entry Gate 加入 Patch Churn Lens。
- 当补丁震荡出现时，不只检查“是否符合原始目标”，还要检查“当前抽象是否仍能表达原始目标”。
- 在 Exit Gate 增加一个问题：交付物是否减少了失败模式，还是只覆盖了最近一次失败样本。

建议新增 Lens：

```text
| Patch Churn | Same Feature has repeated fix iterations, scenario-specific branches, or manual validation keeps exposing related failures. | Are we fixing the implementation, or preserving a wrong abstraction? |
```

### harness-incident-learning

定位：把修复后的失败转成防复发机制。

这是最应该重点修改的 skill。

建议改动：

- 在 When To Use 中明确 repeated patch churn 是 incident learning 触发条件。
- 在 Incident Learning Loop 中加入“补丁链条分析”步骤。
- 在 Recurrence Decision 中加入“规则分支持续增长”和“局部补丁无法解释同类失败”的判断。
- 在 Protection Options 中强化 Gate / Lesson / ADR 的选择规则。

建议新增小节：

```text
## Patch Churn Review

When the same Feature has repeated fix iterations, inspect the fix chain before accepting another patch:

1. List the last 3+ fixes and the validation symptom each addressed.
2. Group symptoms by suspected root cause.
3. Identify whether fixes are moving upstream toward the invariant boundary or downstream into presentation/filtering patches.
4. Ask whether the current abstraction can explain all observed failures.
5. If the answer is no, route to Vision Gate and consider ADR or Lesson before more implementation.
```

### harness-knowledge-capture

定位：收尾和知识沉淀。

建议改动：

- 在 Lesson 触发条件中加入 patch churn。
- 在 Evidence 要求中增加 trajectory：连续补丁链必须记录每一轮暴露了什么，以及最终为什么不是继续局部修补。
- 在 Completion Closeout Gate 中加入：如果 Feature 有 3+ follow-up fixes，必须说明是否运行了 Patch Churn Review。

建议新增 closeout category 可选项：

```text
Patch Churn Review: not triggered / pass / routed to Vision Gate / routed to ADR / routed to Lesson / blocked
```

### harness-readiness-dashboard

定位：收尾状态面板。

建议改动：

- 在 ready 状态中显示 patch churn 风险。
- 对 release / handoff 之前的 Feature，如果存在连续补丁链，要求说明是否已经收敛到不变量或架构边界。

建议字段：

```text
Patch churn:
- not triggered / low / medium / high
- Evidence: F018 / EV-017 / LL-00x, when applicable
- Required action: none / Vision Gate / Incident Learning / ADR / Lesson
```

### harness-project-rules

定位：判断是否进入项目级规则。

建议改动：

- 不要把 F018 的完整历史直接写进 `AGENTS.md`。
- 允许把“连续补丁触发归零审视”作为源自 Lesson 的项目级行为规则。
- 要求 source-backed：先有 Lesson 或 Evidence，再晋升为项目规则。

推荐规则草案：

```markdown
### Rule: Re-evaluate patch-heavy Features
- Scope: Any Feature with repeated fix iterations, especially 3+ follow-ups or scenario-specific rule growth.
- Requirement: Agents MUST pause further patching and run a zero-base review before implementing another patch when fixes repeatedly target symptoms instead of reducing the underlying invariant or boundary problem.
- Source: LL-00x patch-churn-zero-base-review or EV-017 F018 evidence trail.
- Rationale: Repeated patch churn is evidence that the initial abstraction may be wrong, not merely incomplete.
```

## 推荐实施顺序

### 第一阶段：让 skill 能识别补丁震荡

修改：

- `using-harness`
- `harness-start-gate`
- `harness-incident-learning`

验收：

- 用户提到“反复补丁”“F018.8”“规则越补越多”时，Agent 不应直接继续实现。
- Start Gate 应返回 `needs retrieval` 或 `needs vision gate`，而不是 `ready`。
- Incident Learning 应要求列出补丁链条并判断根因是否收敛。

### 第二阶段：让收尾显式报告 Patch Churn

修改：

- `harness-knowledge-capture`
- `harness-readiness-dashboard`

验收：

- 对有 3+ follow-up fixes 的 Feature，完成声明中必须出现 Patch Churn Review 状态。
- Evidence 必须记录补丁轨迹和最终边界判断。

### 第三阶段：把经验沉淀为 Lesson，再决定是否进 AGENTS.md

修改：

- 新增 Lesson 示例。
- 通过 `harness-project-rules` 判断是否更新模板 `AGENTS.md`。

验收：

- `AGENTS.md` 只保留短规则。
- F018 这类案例的长背景留在 Lesson / Evidence / 文章中。
- 项目规则可操作、可验证，不变成泛泛提醒。

## 验收用例

### Case 1: 三轮补丁但根因不同

输入：

```text
F020 做完后有三个小问题：一个 typo，一个按钮间距，一个测试 mock 路径。
```

期望：

- 不强制架构归零。
- 可以记录 quick Evidence。
- 不写 Lesson。

### Case 2: 规则分支持续增长

输入：

```text
F021 已经 F021.4 了，每次都是补关键词规则，但新的自然表达还是漏。
```

期望：

- Start Gate 不允许直接补第五个关键词。
- Incident Learning 要求分析规则逻辑是否选型错误。
- Vision Gate 检查原始目标是否应由模型/tool contract 而不是规则关键词承担。
- 可能需要 ADR。

### Case 3: 下游过滤反复失败

输入：

```text
F018.6 仍然把无关 web snippet 写进报告，之前已经在 Composer 过滤过几轮。
```

期望：

- Patch Churn Review 识别“过滤位置太晚”。
- 归零审视得出 `retrieved candidate != accepted evidence`。
- 修复方向前移到 orchestration evidence contract。
- Evidence 记录为什么不继续 Composer-side filtering。

## 非目标

- 不把所有多轮补丁都升级为架构事故。
- 不要求每次小修都写 Lesson。
- 不把 “3 次” 变成僵硬的阻塞规则。
- 不在当前迭代直接建设自动统计 Feature patch count 的 runtime。
- 不用 AGENTS.md 承载完整事故复盘。

## 一句话总结

Patch Churn Gate 要保护的不是某个 Feature，而是 Agent 的判断力：当系统用越来越多补丁维持一个越来越脆弱的抽象时，Harness 必须让 Agent 停下来，重新问“这个模型是不是一开始就错了”。
