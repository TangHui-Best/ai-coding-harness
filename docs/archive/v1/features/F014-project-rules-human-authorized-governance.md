---
id: F014
doc_kind: feature
status: completed
created: 2026-06-27
updated: 2026-06-27
---

# F014: Project Rules Human Authorized Governance

## Goal

让 AGENTS.md / Project Rules 从“可随手追加的说明文档”收敛为高注意力行为约束层：只晋升短小、source-backed、可验证、经过人类授权的 MUST / MUST NOT 规则。

## Vision Anchor

- 原始请求或来源：用户认可 AGENTS.md 不是知识沉淀层，而是高注意力行为约束层，并要求控制长度，通常建议 100 行，不超过 200-300 行。
- 用户痛点或工程问题：如果 Agent 可以自行把经验、偏好、长叙事写入 AGENTS.md，AGENTS.md 会膨胀成知识垃圾场，反而降低每个未来 Agent 的注意力质量。
- 期望结果：project-rules skill 明确人类授权边界、晋升门槛、规则结构、source-backed 要求和长度预算；starter AGENTS 模板体现这些规则。
- 非目标或边界：本迭代不直接创建或修改当前项目根目录 `AGENTS.md`；不把 Feature、ADR、Lesson、Evidence 内容迁移进 AGENTS.md；不允许 Agent 未授权自动晋升规则。
- Exit Gate 对照来源：本 Feature、EV-021、`tests/test_project_rules_governance.py`、Project Rules skill、AGENTS starter templates。

## Feature Intake

- Original problem: AGENTS.md 的价值来自默认可见和默认遵守，但这也意味着它的注意力成本最高，必须避免变成历史、理由和经验的堆放处。
- User pain point: 规则晋升如果没有人类授权和低线结构，Agent 可能为了“沉淀”而扩张 AGENTS.md，造成后续每个任务都背负噪音。
- Capability promise: AgentMentor 能在修改 AGENTS.md 前要求 promotion gate、人类授权、source-backed 规则、MUST/MUST NOT 约束和长度预算检查。
- Non-goals: 不设计完整规则数据库；不做自动全局 AGENTS 重写；不把 SHOULD/PREFER 偏好作为默认项目规则。
- Acceptance source: 用户确认的 Project Rules / AGENTS 第一性原理、授权边界、规则结构和长度预算。
- Open questions: 未来是否需要针对已有大型 AGENTS.md 提供机械瘦身工具，等待真实仓库规模问题再判断。

## Capability Contract

- `skills/project-rules/SKILL.md` 明确 AGENTS.md 是高注意力 behavior-control surface，不是 knowledge archive。
- Agent 可以识别候选规则、运行晋升门、草拟规则文本和给出建议，但未经授权不得编辑 AGENTS.md 或仓库级 Agent 指令。
- 晋升规则必须是 cross-task、project-level、behavioral、MUST/MUST NOT、verifiable、source-backed、worth attention cost、human-authorized。
- 规则形态固定为 `Scope`、`Requirement`、`Source`、`Rationale`。
- AGENTS 长度预算固定为 target <=100 lines、soft limit 200 lines、hard limit 300 lines with explicit user approval。
- 根 `templates/AGENTS.md` 和 bundled `skills/using-agentmentor/assets/templates/AGENTS.md` 保持一致。

## Decision Context

### Why

AGENTS.md 的第一性原理不是记录知识，而是改变每个未来 Agent 的默认行为。因为它默认被读、默认影响所有任务，所以进入 AGENTS.md 的内容必须比普通文档承担更高的注意力成本审查。规则需要 source-backed，是为了防止“漂浮规则”；需要人类授权，是为了防止 Agent 自行扩张控制面；需要 MUST/MUST NOT，是为了让规则可执行、可审查、可删除。

### Why Not

没有允许 Agent 自动编辑 AGENTS.md，因为这会让控制面被被治理对象自行扩张。没有保留 SHOULD/PREFER 作为默认规则级别，因为如果一个偏好不能写成明确边界，放进 AGENTS.md 只会制造模糊负担。没有把 ADR、Lesson、Evidence 的理由全文写入 AGENTS.md，因为深层上下文应留在源 artifact，AGENTS.md 只承载行为约束和 source link。

### If Modifying This Area, Check

- 修改 `skills/project-rules/SKILL.md` 时，检查人类授权边界、Promotion Gate、Reject Patterns、Rule Wording、Length Budget 是否一致。
- 修改 AGENTS starter template 时，同步根 `templates/AGENTS.md` 和 bundled `skills/using-agentmentor/assets/templates/AGENTS.md`。
- 修改 artifact decision matrix 时，确认 AGENTS.md 仍被定位为 behavior constraint，而不是知识沉淀层。
- 运行 `tests/test_project_rules_governance.py`、strict knowledge check 和 F014 Feature Index 本地校验。
- 不要在没有用户明确要求时创建或修改项目根目录 `AGENTS.md`。

## Current Status

Completed。Project Rules / AGENTS 治理规则已落地到 skill、starter templates、artifact decision matrix、测试、Feature Index 和 Evidence。

## Links

### Evidence

- [EV-021 Project Rules Human Authorized Governance](../evidence/EV-021-project-rules-human-authorized-governance.md)

### Decisions / ADRs

- None.

### Lessons

- None.

### Specs / Plans

- None.

### Related Features

- [F009 Feature Intake Governance](F009-feature-intake-governance.md)
- [F013 Evidence Claim Verification Governance](F013-evidence-claim-verification-governance.md)

### External Context

- [Project Rules skill](../../skills/project-rules/SKILL.md)
- [AGENTS template](../../templates/AGENTS.md)
- [Bundled AGENTS template](../../skills/using-agentmentor/assets/templates/AGENTS.md)
- [Artifact decision matrix](../../skills/knowledge-capture/references/artifact-decision-matrix.md)

## Acceptance Criteria

- [x] project-rules skill 明确 AGENTS.md 是高注意力行为约束层，不是知识沉淀层。
- [x] project-rules skill 明确未经用户授权不得编辑 AGENTS.md 或仓库级 Agent 指令。
- [x] Promotion Gate 要求规则必须 source-backed、verifiable、human-authorized，并可写成 MUST/MUST NOT。
- [x] Rule Wording 固定为 Scope、Requirement、Source、Rationale。
- [x] AGENTS 长度预算明确 target <=100 lines、soft limit 200 lines、hard limit 300 lines。
- [x] root/bundled AGENTS templates 保持一致，并包含短规则示例。

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| AGENTS 被定位为行为约束层 | project-rules skill 和 artifact decision matrix 明确 high-attention behavior-control surface / control surface | [EV-021](../evidence/EV-021-project-rules-human-authorized-governance.md) | completed |
| 规则晋升必须人类授权 | project-rules skill 包含 Human Authorization Boundary 和 MUST NOT edit 约束 | [EV-021](../evidence/EV-021-project-rules-human-authorized-governance.md) | completed |
| 规则结构可执行可审查 | Rule Wording 和 starter template 使用 Scope / Requirement / Source / Rationale | [EV-021](../evidence/EV-021-project-rules-human-authorized-governance.md) | completed |
| AGENTS 反膨胀机制已落地 | Length Budget 和 Reject Patterns 限制无 source、超预算、偏好型规则 | [EV-021](../evidence/EV-021-project-rules-human-authorized-governance.md) | completed |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-06-27 | completed | Project Rules / AGENTS governance iteration | [EV-021](../evidence/EV-021-project-rules-human-authorized-governance.md) | 人类授权、source-backed、MUST/MUST NOT、长度预算进入规则晋升流程。 |

## Patch History

None yet.

## Evidence

- [EV-021 Project Rules Human Authorized Governance](../evidence/EV-021-project-rules-human-authorized-governance.md)

## Recovery Snapshot

- Read first: this Feature page, then `skills/project-rules/SKILL.md` and EV-021.
- Current capability state: completed; Project Rules promotion gate now protects AGENTS from unauthorized and bloated rule growth.
- Known risks: 未来真实项目中已有 AGENTS.md 可能很长，需要另行设计瘦身或分层迁移策略。
- Next safe action: 如果要修改某个项目的 AGENTS.md，先运行 project-rules promotion gate，再确认用户授权和长度预算。
- Unblock condition: not blocked.

## Next Step

观察后续 AGENTS.md 修改场景；如果大型 AGENTS 已经存在，再设计“规则瘦身 / 分层迁移”工具或流程。
