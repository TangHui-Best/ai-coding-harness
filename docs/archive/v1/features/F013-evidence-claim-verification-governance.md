---
id: F013
doc_kind: feature
status: completed
created: 2026-06-27
updated: 2026-06-27
---

# F013: Evidence Claim Verification Governance

## Goal

让 Evidence 从“记录命令和结果”升级为“约束完成声明”的证据文档：每份 Evidence 必须说明支撑哪个声明、验证覆盖什么、实际检查什么、结果是什么、有哪些材料、不能证明什么。

## Vision Anchor

- 原始请求或来源：用户认可 Evidence 的第一性原理是解决 LLM 虚假完成声明，而不是主要作为高复用开发知识库。
- 用户痛点或工程问题：旧 Evidence 能记录命令和结果，但当前或未来读者仍需要猜这些结果支撑哪个完成声明，以及验证边界和限制是什么。
- 期望结果：Evidence 结构包含 `Supports Claim`、`Verification Scope`、`Checks`、`Results`、`Artifacts`、`Limitations`、`Notes`。
- 非目标或边界：不新增 Evidence Index；不把 Evidence 设计成设计说明、ADR、Lesson、Backlog 或高频复用知识库。
- Exit Gate 对照来源：本 Feature、EV-020、Evidence 模板、`knowledge_check.py --strict`、`tests/test_knowledge_check.py`。

## Feature Intake

- Original problem: Evidence 需要更强地约束完成声明，避免 Agent 用语言直接替代验证事实。
- User pain point: 仅有 Commands / Results 时，Evidence 容易变成无归属命令列表，不能明确支撑哪个声明或限制过度声明。
- Capability promise: AgentMentor Evidence 能把完成声明、验证范围、检查动作、结果、材料和限制绑定起来。
- Non-goals: 不新增 Evidence Index，不提高 Evidence 召回权重，不把 Evidence 写成设计 rationale。
- Acceptance source: 用户确认的 Evidence 字段方案、EV-020 和 validator。
- Open questions: 是否未来对 `Results` 增加表格低线检查，等待真实写入质量问题再判断。

## Capability Contract

- `templates/EVIDENCE.md` 和 bundled `skills/using-agentmentor/assets/templates/EVIDENCE.md` 使用新版结构。
- `knowledge_check.py` 要求 Evidence 包含 `Supports Claim`、`Verification Scope`、`Checks`、`Results`、`Artifacts`、`Limitations`、`Notes`。
- `knowledge-capture` 和 artifact decision matrix 明确 Evidence 的核心是完成声明约束。
- 现有 Evidence 迁移到新版结构。
- Evidence 文件命名规范为 `EV-xxx-<work-or-feature>-<verification-focus>.md`。

## Decision Context

### Why

Evidence 的第一性原理是把 Agent 的完成声明从语言声明约束为可核验声明。它不主要承担未来开发知识复用，而是在完成、验收和决策声明发生时，迫使声明绑定到检查动作、结果和限制。

### Why Not

没有新增 Evidence Index，因为 Evidence 通常通过 Feature、ADR、Lesson 链接被打开，不是高频第一层召回入口。没有保留独立 `Harness Validation`，因为它过窄，验证可以是命令、人工检查、截图、review 或外部状态。没有新增 `Why`、`Decision` 或 `Next Steps`，因为这些属于 Feature、ADR、Lesson、Backlog 或 handoff。

### If Modifying This Area, Check

- 同步根 `templates/EVIDENCE.md` 和 bundled `skills/using-agentmentor/assets/templates/EVIDENCE.md`。
- 同步根 `scripts/knowledge_check.py` 和 bundled `skills/using-agentmentor/scripts/knowledge_check.py`。
- 检查 `skills/knowledge-capture/SKILL.md`、artifact decision matrix 和 completion closeout contract 的 Evidence 语义是否一致。
- 运行 `tests/test_knowledge_check.py`、strict knowledge check 和 F013 local Feature Index check。
- 迁移现有 Evidence 时，不把历史证据改写成新的完成结论。

## Current Status

Completed。Evidence 模板、validator、skill 规则、现有 Evidence 和本次 Evidence 已完成迁移并通过验证。

## Links

### Evidence

- [EV-020 Evidence Claim Verification Governance](../evidence/EV-020-evidence-claim-verification-governance.md)

### Decisions / ADRs

- None.

### Lessons

- None.

### Specs / Plans

- None.

### Related Features

- [F001 Closeout Entry Anchor Validation](F001-closeout-entry-anchor-validation.md)
- [F009 Feature Intake Governance](F009-feature-intake-governance.md)

### External Context

- [Evidence template](../../templates/EVIDENCE.md)
- [knowledge-capture](../../skills/knowledge-capture/SKILL.md)
- [artifact decision matrix](../../skills/knowledge-capture/references/artifact-decision-matrix.md)

## Acceptance Criteria

- [x] Evidence 模板包含 Supports Claim、Verification Scope、Checks、Results、Artifacts、Limitations、Notes。
- [x] `knowledge_check.py` 不再要求 Commands / Notes 旧结构，改为要求 claim-bound evidence 结构。
- [x] 现有 Evidence 迁移到新版结构。
- [x] Knowledge Capture 和 artifact decision matrix 的 Evidence 写入规则与新版结构一致。
- [x] Evidence 命名规范明确为 work or feature + verification focus。

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| Evidence 结构绑定完成声明 | 模板和现有 Evidence 均包含 Supports Claim | [EV-020](../evidence/EV-020-evidence-claim-verification-governance.md) | completed |
| Evidence 结构说明验证边界 | 模板和现有 Evidence 均包含 Verification Scope 和 Limitations | [EV-020](../evidence/EV-020-evidence-claim-verification-governance.md) | completed |
| Validator 固化新版 Evidence 结构 | `tests/test_knowledge_check.py` 覆盖 Supports Claim、Checks、Limitations 必备区块 | [EV-020](../evidence/EV-020-evidence-claim-verification-governance.md) | completed |
| Evidence 写入边界进入收尾规则 | Knowledge Capture、artifact decision matrix、closeout contract 使用 claim-bound Evidence 语义 | [EV-020](../evidence/EV-020-evidence-claim-verification-governance.md) | completed |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-06-27 | completed | Evidence governance iteration | [EV-020](../evidence/EV-020-evidence-claim-verification-governance.md) | Evidence 聚焦完成声明约束、验证范围、检查动作、结果和限制。 |

## Patch History

None yet.

## Evidence

- [EV-020 Evidence Claim Verification Governance](../evidence/EV-020-evidence-claim-verification-governance.md)

## Recovery Snapshot

- Read first: this Feature page, then EV-020 and the Evidence template.
- Current capability state: completed; Evidence uses Supports Claim/Verification Scope/Checks/Results/Artifacts/Limitations/Notes.
- Known risks: 既有 Evidence 的 Supports Claim 和 Limitations 采用保守迁移文字，未来新增 Evidence 应写得更具体。
- Next safe action: 如果 Evidence 仍出现泛泛 Pass 或过度声明，再考虑 validator 低线检查或模板示例强化。
- Unblock condition: not blocked.

## Next Step

观察后续 Evidence 写入质量；如果 `Supports Claim` 或 `Limitations` 继续空泛，再增加更具体的模板示例或 validator 检查。
