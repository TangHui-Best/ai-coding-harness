---
id: F009
doc_kind: feature
status: completed
created: 2026-06-11
updated: 2026-06-11
---

# F009: Feature Intake Governance

## Goal

让 Harness Feature 从“简略功能记录”升级为长期治理入口：创建或重大更新 Feature 前必须先完成 Feature Intake，完成态 Feature 必须能把能力声明、验收标准、证据和恢复入口连起来，避免 Agent 把未澄清需求写成长期项目记忆。

## Vision Anchor

- 原始请求或来源：用户指出 ScienceClaw 生成的 Feature 文档简陋，无法很好承载历史数据记录；随后确认短期重点是治理优化 Feature，并认可借鉴 Superpowers brainstorming 的澄清约束，但由 Harness 自己拥有 Feature 前置门禁。
- 用户痛点或工程问题：旧 Feature 模板只有 Vision Anchor、Current Status、Acceptance Criteria、Patch History、Evidence 和 Next Step，容易出现两类失控：一类是未问清楚就写 Feature，另一类是把所有历史塞进 Patch History，导致可追溯但不可恢复。
- 期望结果：Feature 创建/重大更新前有 Feature Intake 六问；Feature 页面保留能力边界、验收证据映射、状态时间线和恢复快照；校验器能阻止缺失 Intake、完成态验收无证据、blocked Feature 无解除条件。
- 非目标或边界：不直接依赖 Superpowers 实现、不把 Feature 变成完整 spec/plan/log 容器、不迁移外部项目全部历史、不重写已有 Feature 的原始语义。
- Exit Gate 对照来源：本 Feature、EV-012、更新后的 Feature 模板、Start Gate / Knowledge Capture 规则和 `knowledge_check.py` 测试。

## Feature Intake

- Original problem: Feature 文档缺少写入前澄清门禁和历史恢复结构。
- User pain point: 后续 Agent 难以判断能力边界、验收证据和下一步，容易继续局部补丁或误读历史。
- Capability promise: Harness 能约束新 Feature 先完成 Intake，并要求完成态 Feature 具备验收证据映射和恢复快照。
- Non-goals: 不复制 Superpowers spec 流程，不把所有详细设计或执行日志塞进 Feature。
- Acceptance source: 本 Feature、EV-012 和 `tests/test_knowledge_check.py`。
- Open questions: 是否后续拆出独立 `feature-intake` Skill，留待真实使用反馈后决定。

## Capability Contract

- 新版 Feature 模板包含 `Feature Intake`、`Capability Contract`、`Acceptance Map`、`State Timeline` 和 `Recovery Snapshot`。
- Start Gate 在新建或重大更新 Feature 前检查 Intake 六问，缺失时要求澄清。
- Knowledge Capture 明确 Feature 是长期治理入口，详细 spec/plan/Evidence/handoff 通过链接外置。
- `knowledge_check.py` 校验 Feature Intake 六问、Acceptance Map 证据、Recovery Snapshot 下一步和 blocked 解除条件。

## Current Status

Completed。模板、Skill 规则、根校验器、bundled 校验器、测试和仓库内既有 Feature 迁移均已完成；严格知识校验和 skill metadata 校验通过。

## Links

- Evidence: [EV-012 Feature Intake Governance](../evidence/EV-012-feature-intake-governance.md)
- Evidence: [EV-014 Feature Index Coarse Retrieval](../evidence/EV-014-feature-index-coarse-retrieval.md)
- Template: [Feature template](../../templates/FEATURE.md)
- Bundled template: [using-agentmentor Feature template](../../skills/using-agentmentor/assets/templates/FEATURE.md)
- Start Gate: [start-gate](../../skills/start-gate/SKILL.md)
- Knowledge Capture: [knowledge-capture](../../skills/knowledge-capture/SKILL.md)

## Acceptance Criteria

- [x] Feature 模板包含 Feature Intake 六问、Capability Contract、Acceptance Map、State Timeline 和 Recovery Snapshot。
- [x] Start Gate 明确：新建或重大更新 Feature 时，Intake 缺失必须 `needs clarification`。
- [x] Knowledge Capture 明确：Feature 是治理入口，不是 spec、plan、Evidence 或 handoff 的全文容器。
- [x] `knowledge_check.py` 拒绝缺失 Feature Intake、缺失 Intake prompt、完成态 Acceptance Map 无 Evidence、blocked Feature 无 unblock condition。
- [x] bundled `using-agentmentor/scripts/knowledge_check.py` 与根脚本同步。
- [x] 仓库内既有 Feature 已迁移到新版结构并通过严格知识校验。

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| Feature Intake 成为写入前门禁 | Start Gate / Knowledge Capture 规则写明缺失 Intake 应澄清 | [EV-012](../evidence/EV-012-feature-intake-governance.md) | completed |
| Feature 页面能承载恢复索引 | 模板包含 Capability Contract、Acceptance Map、State Timeline、Recovery Snapshot | [EV-012](../evidence/EV-012-feature-intake-governance.md) | completed |
| 校验器提供机器约束 | `test_knowledge_check` 覆盖新失败场景并通过 | [EV-012](../evidence/EV-012-feature-intake-governance.md) | completed |
| Feature 粗召回具备低成本入口 | `docs/features/INDEX.md`、命名规则和 retrieval hot path 支持先选 1-3 个候选 Feature | [EV-014](../evidence/EV-014-feature-index-coarse-retrieval.md) | completed |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-06-11 | completed | Feature governance optimization implemented | [EV-012](../evidence/EV-012-feature-intake-governance.md) | Superpowers brainstorming 思想被内化为 Harness Feature Intake 门禁。 |
| 2026-06-23 | completed | Feature recall optimization implemented | [EV-014](../evidence/EV-014-feature-index-coarse-retrieval.md) | Feature Index、命名规则和粗召回流程进入热路径。 |

## Patch History

| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |
| --- | --- | --- | --- | --- | --- | --- |
| F009.1 | 2026-06-23 | uncommitted | Feature 只有被打开后才有机会发挥作用，召回前入口不足 | 召回职责缺少文件名规则、低成本 Index 和 hot-path retrieval 约束 | Feature Index、命名规则、retrieval 1-3 候选限制、knowledge_check 非 artifact skip | completed |

## Evidence

- [EV-012 Feature Intake Governance](../evidence/EV-012-feature-intake-governance.md)
- [EV-014 Feature Index Coarse Retrieval](../evidence/EV-014-feature-index-coarse-retrieval.md)

## Recovery Snapshot

- Read first: this Feature page, then EV-012 and EV-014.
- Current capability state: completed; new Feature pages must satisfy Intake and recovery sections; no-ref retrieval should use Feature Index or filename fallback before opening candidates.
- Known risks: migrated legacy Feature sections are intentionally concise and point back to existing Evidence rather than rewriting historical detail.
- Next safe action: observe real Feature creation/update usage before splitting a dedicated `feature-intake` Skill.
- Unblock condition: not blocked.

## Next Step

在后续真实 Feature 生成中观察 Intake 是否足够；若 Agent 仍然跳过澄清或把历史塞进 Patch History，再评估拆出独立 `feature-intake` Skill 或增强 closeout/readiness 约束。
