---
id: F012
doc_kind: feature
status: completed
created: 2026-06-27
updated: 2026-06-27
---

# F012: ADR Decision Boundary Governance

## Goal

让 ADR 从“记录一次决策”升级为“帮助未来维护者或 Agent 正确遵守、挑战或修改长期决策边界”的治理文档。

## Vision Anchor

- 原始请求或来源：用户认可 ADR 整体迭代方案，并要求按方案落地；同时要求触发规则从 future agents 泛化为 future maintainers or agents。
- 用户痛点或工程问题：旧 ADR 结构能说明背景、决策和替代方案，但读后仍可能不知道适用边界、非适用边界，以及修改或推翻前必须检查什么。
- 期望结果：ADR 模板、validator、写入规则和现有 ADR 都使用 `Decision Boundary`、`Rejected Options`、`Before Changing This Decision`。
- 非目标或边界：不新增 `Revisit When`；不新增 ADR Index；不批量重命名历史 ADR 文件。
- Exit Gate 对照来源：本 Feature、ADR-009、EV-019、ADR 模板、`knowledge_check.py --strict`、`tests/test_knowledge_check.py`。

## Feature Intake

- Original problem: ADR 需要更好支撑未来维护者或 Agent 的长期决策判断。
- User pain point: 只记录背景和决策还不够，未来修改者需要知道边界、被拒绝方案和修改前检查。
- Capability promise: AgentMentor ADR 结构能表达决策边界、已拒绝方案、后果和修改前门禁。
- Non-goals: 不新增 Revisit When，不新增 ADR Index，不批量重命名历史 ADR。
- Acceptance source: 用户确认的 ADR 结构方案、ADR-009 和 EV-019。
- Open questions: 是否未来基于真实漏召回案例增加 ADR Index，暂不处理。

## Capability Contract

- `templates/ADR.md` 和 bundled `skills/using-agentmentor/assets/templates/ADR.md` 使用新版 ADR 结构。
- `knowledge_check.py` 要求 ADR 包含 `Decision Boundary`、`Rejected Options` 和 `Before Changing This Decision`。
- `knowledge-capture`、artifact decision matrix 和 `incident-learning` 的 ADR 写入边界使用 durable decision boundary 表述。
- 现有 ADR 迁移到新版结构，不强制重命名历史文件。
- ADR 文件命名规范为 `ADR-xxx-<decision-area>-<accepted-choice>.md`。

## Decision Context

### Why

ADR 的第一性原理不是证明过去决策正确，而是让未来维护者或 Agent 能判断一个长期决策边界是否应被遵守、挑战或修改。旧结构缺少明确边界和修改前检查，容易让读者误扩大、误缩小或无证据推翻决策。

### Why Not

没有新增 `Revisit When`，因为它难以稳定填写，容易变成空泛预测。没有新增 ADR Index，因为 ADR 通常通过 Feature Links、文件名和关键词检索命中。没有重命名历史 ADR 文件，因为现有文件名整体可用，重命名会制造链接 churn。

### If Modifying This Area, Check

- 同步根 `templates/ADR.md` 和 bundled `skills/using-agentmentor/assets/templates/ADR.md`。
- 同步根 `scripts/knowledge_check.py` 和 bundled `skills/using-agentmentor/scripts/knowledge_check.py`。
- 检查 `skills/knowledge-capture/SKILL.md`、artifact decision matrix 和 `skills/incident-learning/SKILL.md` 的 ADR 写入边界是否一致。
- 运行 `tests/test_knowledge_check.py`、strict knowledge check 和 F012 local Feature Index check。
- 迁移现有 ADR 时保留历史事实，不把旧决策改写成新结论。

## Current Status

Completed。ADR 模板、validator、skill 规则、现有 ADR 和 Evidence 已完成迁移并通过验证。

## Links

### Evidence

- [EV-019 ADR Decision Boundary Governance](../evidence/EV-019-adr-decision-boundary-governance.md)

### Decisions / ADRs

- [ADR-009 ADR Decision Boundary Structure](../decisions/ADR-009-adr-decision-boundary-structure.md)

### Lessons

- None.

### Specs / Plans

- None.

### Related Features

- [F009 Feature Intake Governance](F009-feature-intake-governance.md)
- [F011 Lesson Case Protection Governance](F011-lesson-case-protection-governance.md)

### External Context

- [ADR template](../../templates/ADR.md)
- [knowledge-capture](../../skills/knowledge-capture/SKILL.md)
- [artifact decision matrix](../../skills/knowledge-capture/references/artifact-decision-matrix.md)

## Acceptance Criteria

- [x] ADR 模板包含 Decision Boundary、Rejected Options、Before Changing This Decision。
- [x] `knowledge_check.py` 不再要求 Alternatives，改为要求 Rejected Options 和边界检查区块。
- [x] 现有 ADR 迁移到新版结构。
- [x] Knowledge Capture 和 Incident Learning 的 ADR 写入规则与新版结构一致。
- [x] ADR 命名规范明确为 decision area + accepted choice。

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| ADR 结构承载决策边界 | 模板和现有 ADR 均包含 Decision Boundary | [EV-019](../evidence/EV-019-adr-decision-boundary-governance.md) | completed |
| ADR 结构承载已拒绝方案 | `Alternatives` 被 `Rejected Options` 替代并由 validator 固化 | [EV-019](../evidence/EV-019-adr-decision-boundary-governance.md) | completed |
| ADR 修改前门禁进入结构 | 模板和现有 ADR 均包含 Before Changing This Decision | [EV-019](../evidence/EV-019-adr-decision-boundary-governance.md) | completed |
| ADR 写入边界进入收尾规则 | Knowledge Capture、artifact decision matrix、Incident Learning 使用 durable decision boundary 语义 | [EV-019](../evidence/EV-019-adr-decision-boundary-governance.md) | completed |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-06-27 | completed | ADR governance iteration | [EV-019](../evidence/EV-019-adr-decision-boundary-governance.md) | ADR 结构聚焦决策边界、拒绝方案和修改前检查。 |

## Patch History

None yet.

## Evidence

- [EV-019 ADR Decision Boundary Governance](../evidence/EV-019-adr-decision-boundary-governance.md)

## Recovery Snapshot

- Read first: this Feature page, then ADR-009, EV-019, and the ADR template.
- Current capability state: completed; ADR uses Context/Decision/Decision Boundary/Rejected Options/Consequences/Before Changing This Decision/Evidence.
- Known risks: 历史 ADR 文件名未批量重命名；后续新增 ADR 通过命名规范提升召回。
- Next safe action: 如果未来出现 ADR 漏召回，再基于真实案例评估 ADR Index。
- Unblock condition: not blocked.

## Next Step

观察后续 ADR 写入质量；如果 `Decision Boundary` 或 `Before Changing This Decision` 变成空泛文字，再考虑 validator 低线检查或模板示例强化。
