---
id: ADR-009
doc_kind: adr
status: accepted
scope: project
feature_refs: [docs/features/F012-adr-decision-boundary-governance.md]
decision_area: adr-governance
created: 2026-06-27
updated: 2026-06-27
---

# ADR-009: ADR Decision Boundary Structure

## Context

AgentMentor 已经治理了 Feature 和 Lesson：Feature 负责能力边界、验收和恢复入口；Lesson 负责客观失败案例、当时解决方式和防复发机制。ADR 仍沿用传统 `Context / Decision / Alternatives / Consequences / Evidence` 结构。

这个结构能记录基本决策事实，但对未来维护者或 Agent 的行动支撑不足：读完后仍可能不知道这个决策约束什么、不约束什么，也不知道如果要修改或推翻该决策，必须先检查哪些事实和证据。

同时，`Alternatives` 这个标题偏中性，不能直观表达“这些方案已经被明确放弃，未来不要无成本重复提出”。

## Decision

ADR 结构采用：

```text
Context
Decision
Decision Boundary
Rejected Options
Consequences
Before Changing This Decision
Evidence
```

`Alternatives` 改名为 `Rejected Options`。

ADR 文件命名采用：

```text
ADR-xxx-<decision-area>-<accepted-choice>.md
```

ADR 写入触发规则收敛为：当一个决策创建或改变了长期边界，并且未来维护者或 Agent 可能需要遵守、挑战或修改它时，写 ADR。

不新增 `Revisit When`，因为它很难稳定写好，容易变成空泛预测。未来读者应基于 `Context`、`Decision Boundary`、`Rejected Options` 和 `Consequences` 判断事实是否已经变化。

## Decision Boundary

### Applies To

- AgentMentor ADR 模板、bundled ADR 模板和 ADR validator required sections。
- 新增 ADR 的文件命名规范。
- Knowledge Capture 和 artifact decision matrix 中关于 ADR 写入触发、写入边界和命名的说明。
- 现有 ADR 正文结构迁移。

### Does Not Apply To

- Feature `Decision Context`，它仍用于单个 Feature 内的轻量 why / why not / 修改前检查。
- Lesson 的失败模式防复发结构。
- Evidence 的事实证明结构。
- 历史 ADR 文件名；本次不为了命名规范批量重命名既有 ADR。

## Rejected Options

- 保留 `Alternatives` 标题：拒绝，因为它像平行备选项，不如 `Rejected Options` 直观表达“已被明确放弃的方案”。
- 新增 `Revisit When`：拒绝，因为多数情况下作者无法稳定预测未来哪些事实会变化，容易写成空话。
- 新增 ADR Index：拒绝，因为 ADR 通常通过 Feature Links、文件名和关键词检索命中，不是当前最高价值的第一层召回入口。
- 批量重命名历史 ADR 文件：拒绝，因为现有 ADR 文件名大多已经能表达决策领域和接受方案，重命名会制造链接 churn。

## Consequences

收益：

- 未来维护者或 Agent 能更清楚地区分决策适用范围和非适用范围。
- ADR 能直接表达修改或推翻前必须检查的事实、文档和边界。
- `Rejected Options` 更明确地降低重复提出旧方案的概率。
- ADR 命名更利于从文件列表中判断决策领域和已接受方向。

代价：

- 每份 ADR 需要多写两个实质区块：`Decision Boundary` 和 `Before Changing This Decision`。
- 现有 ADR 需要迁移结构。
- Validator required sections 变化会让旧结构 ADR 失败，需要同步模板、测试和 bundled scripts。

## Before Changing This Decision

- 先检查 F012、EV-019、ADR 模板、root/bundled `knowledge_check.py` 和 `tests/test_knowledge_check.py`。
- 如果要恢复 `Alternatives`，先证明它比 `Rejected Options` 更能帮助未来读者理解已拒绝方案。
- 如果要新增 `Revisit When` 或 ADR Index，先提供真实 ADR 漏召回或误改案例。
- 如果要重命名历史 ADR 文件，先评估 Feature Links、Evidence、外部引用和历史路径 churn。

## Evidence

- [F012 ADR Decision Boundary Governance](../features/F012-adr-decision-boundary-governance.md)
- [EV-019 ADR Decision Boundary Governance](../evidence/EV-019-adr-decision-boundary-governance.md)
- `templates/ADR.md`
- `skills/using-agentmentor/assets/templates/ADR.md`
- `scripts/knowledge_check.py`
- `skills/using-agentmentor/scripts/knowledge_check.py`
- `tests/test_knowledge_check.py`
