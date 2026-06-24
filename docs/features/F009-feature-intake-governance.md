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

## Decision Context

### Why

代码只能表达当前实现如何运行，无法稳定表达一个 Feature 当初为什么进入长期记忆、验收证据是什么、未来修改时不能忘记哪些判断。Feature 因此需要承载写入前澄清、能力边界、证据映射、恢复入口，以及本次新增的决策上下文。

Feature Index 和文件命名只负责打开 Feature 之前的粗召回；Feature 正文负责打开之后的判断质量。这个分工能让 Agent 少读但读对，同时避免把所有召回提示塞进正文后才生效。

### Why Not

没有把 Feature 变成完整 spec、plan 或执行日志容器，因为那会让 Feature 从治理入口膨胀成重复信息仓库，降低后续 Agent 的阅读效率。

没有在本阶段加入 `Last Accepted Decision`、独立 `Fragile Boundary` 或独立 `Before Modifying`，因为它们的价值可以被 `Why`、`Why Not` 和 `If Modifying This Area, Check` 覆盖；过多相近标题会诱导重复注意事项。

没有优先做 frontmatter recall fields、任务类型召回强度、向量化结构或 key-section-only reading，因为这些属于召回基础设施；本次目标是提升 Feature 被打开之后对后续修改判断的支撑。

### If Modifying This Area, Check

- 检查 `templates/FEATURE.md` 与 `skills/using-agentmentor/assets/templates/FEATURE.md` 是否同步。
- 检查 `scripts/knowledge_check.py` 与 bundled `skills/using-agentmentor/scripts/knowledge_check.py` 是否同步。
- 检查 `tests/test_knowledge_check.py` 是否覆盖新增 Feature 必备区块。
- 检查 F009 的 Acceptance Map、Patch History、Evidence 和 Recovery Snapshot 是否同步更新。
- 确认修改没有把 Feature 重新变成 spec/plan/log 容器，也没有新增与 `Decision Context` 重复的 guard 标题。

## Current Status

Completed。模板、Skill 规则、根校验器、bundled 校验器、测试和仓库内既有 Feature 迁移均已完成；严格知识校验和 skill metadata 校验通过。

## Links

- Evidence: [EV-012 Feature Intake Governance](../evidence/EV-012-feature-intake-governance.md)
- Evidence: [EV-014 Feature Index Coarse Retrieval](../evidence/EV-014-feature-index-coarse-retrieval.md)
- Evidence: [EV-015 Feature Decision Context](../evidence/EV-015-feature-decision-context.md)
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
- [x] Feature 模板包含 `Decision Context`，用于记录 why、why not 和修改前检查项。

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| Feature Intake 成为写入前门禁 | Start Gate / Knowledge Capture 规则写明缺失 Intake 应澄清 | [EV-012](../evidence/EV-012-feature-intake-governance.md) | completed |
| Feature 页面能承载恢复索引 | 模板包含 Capability Contract、Acceptance Map、State Timeline、Recovery Snapshot | [EV-012](../evidence/EV-012-feature-intake-governance.md) | completed |
| 校验器提供机器约束 | `test_knowledge_check` 覆盖新失败场景并通过 | [EV-012](../evidence/EV-012-feature-intake-governance.md) | completed |
| Feature 粗召回具备低成本入口 | `docs/features/INDEX.md`、命名规则和 retrieval hot path 支持先选 1-3 个候选 Feature | [EV-014](../evidence/EV-014-feature-index-coarse-retrieval.md) | completed |
| Feature 能支撑后续修改判断 | 模板、校验器和现有 Feature 均包含 `Decision Context`，F009 提供完整 why / why not / modification check 示例 | [EV-015](../evidence/EV-015-feature-decision-context.md) | completed |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-06-11 | completed | Feature governance optimization implemented | [EV-012](../evidence/EV-012-feature-intake-governance.md) | Superpowers brainstorming 思想被内化为 Harness Feature Intake 门禁。 |
| 2026-06-23 | completed | Feature recall optimization implemented | [EV-014](../evidence/EV-014-feature-index-coarse-retrieval.md) | Feature Index、命名规则和粗召回流程进入热路径。 |
| 2026-06-24 | completed | Feature decision-context optimization implemented | [EV-015](../evidence/EV-015-feature-decision-context.md) | Feature 增加 why / why not / modification check，用于支撑后续修改决策。 |

## Patch History

| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |
| --- | --- | --- | --- | --- | --- | --- |
| F009.1 | 2026-06-23 | uncommitted | Feature 只有被打开后才有机会发挥作用，召回前入口不足 | 召回职责缺少文件名规则、低成本 Index 和 hot-path retrieval 约束 | Feature Index、命名规则、retrieval 1-3 候选限制、knowledge_check 非 artifact skip | completed |
| F009.2 | 2026-06-24 | uncommitted | Feature 被召回后仍可能只说明能力和证据，缺少修改决策所需的 why / why not / guard | Feature 结构没有显式承载代码之外的设计理由、放弃方案和修改前检查项 | `Decision Context` 模板区块、必备区块校验、F009 示例和 EV-015 | completed |

## Evidence

- [EV-012 Feature Intake Governance](../evidence/EV-012-feature-intake-governance.md)
- [EV-014 Feature Index Coarse Retrieval](../evidence/EV-014-feature-index-coarse-retrieval.md)
- [EV-015 Feature Decision Context](../evidence/EV-015-feature-decision-context.md)

## Recovery Snapshot

- Read first: this Feature page, then EV-012, EV-014, and EV-015.
- Current capability state: completed; new Feature pages must satisfy Intake, Decision Context, and recovery sections; no-ref retrieval should use Feature Index or filename fallback before opening candidates.
- Known risks: migrated legacy Feature sections are intentionally concise and point back to existing Evidence rather than rewriting historical detail.
- Next safe action: observe real Feature creation/update usage before splitting a dedicated `feature-intake` Skill.
- Unblock condition: not blocked.

## Next Step

在后续真实 Feature 生成中观察 Intake 是否足够；若 Agent 仍然跳过澄清或把历史塞进 Patch History，再评估拆出独立 `feature-intake` Skill 或增强 closeout/readiness 约束。
