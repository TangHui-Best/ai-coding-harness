---
id: F011
doc_kind: feature
status: completed
created: 2026-06-27
updated: 2026-06-27
---

# F011: Lesson Case Protection Governance

## Goal

让 Lesson 从经验总结升级为可召回、可理解、可执行的防复发记录：文件名承担召回职责，正文承载客观案例、当时解决方式、失败模式、根因和防复发机制。

## Vision Anchor

- 原始请求或来源：用户认可 Lesson 的第一性原理是“把一次失败转化为未来 Agent 可触发、可执行、可验证的防复发机制”，并确认先从文件名召回和内容结构两方面优化。
- 用户痛点或工程问题：旧 Lesson 结构有 `Trigger` 和 `Fix`，容易把召回责任放进正文，也容易让 Fix 与 Protection 重复；同时缺少一次客观事情描述，后续读者难以独立判断。
- 期望结果：Lesson 文件名包含领域、失败现象和防护点；Lesson 正文包含 Case、Resolution、Pitfall、Root Cause、Protection、Source、Principle。
- 非目标或边界：不新增 Lesson Index；不把 `Trigger`、`Applies / Does Not Apply` 或独立 `Protection Evidence` 作为必备结构；不批量重命名既有 Lesson 文件。
- Exit Gate 对照来源：本 Feature、EV-018、Lesson 模板、`knowledge_check.py --strict`、`tests/test_knowledge_check.py`。

## Feature Intake

- Original problem: Lesson 当前可以记录经验，但触发读取和内容结构仍可能让防复发价值弱化。
- User pain point: 如果 Lesson 缺少客观 Case，读者只能接受作者抽象；如果 Protection 不明确，Lesson 会退化成“下次小心”。
- Capability promise: AgentMentor Lesson 以文件名承担粗召回，以 Case/Resolution/Protection 支撑读后判断和防复发。
- Non-goals: 不建设 Lesson Index，不强制 `Applies / Does Not Apply`，不把正文 `Recall Cues` 当作主召回机制。
- Acceptance source: 本 Feature、EV-018 和用户确认的 Lesson 结构方案。
- Open questions: 是否未来增加 Lesson frontmatter `trigger_terms` 或 Lesson Index，等待真实漏召回案例后再判断。

## Capability Contract

- `templates/LESSON.md` 和 bundled `skills/using-agentmentor/assets/templates/LESSON.md` 使用新版结构。
- `knowledge_check.py` 要求 Lesson 包含 `Case` 和 `Resolution`，不再要求 `Trigger` 或 `Fix`。
- `knowledge-capture` 和 artifact decision matrix 明确 Lesson 文件命名和写入边界。
- 现有 Lesson 迁移到新版结构，保留原始事实、解决过程、失败模式、根因、防护机制和来源。

## Decision Context

### Why

Lesson 的价值不是记录“我们当时学到了什么”，而是让未来 Agent 在相似失败出现时能更早识别风险，并知道防复发机制在哪里。正文里的召回提示只有打开文件后才生效，因此这一轮优先把召回职责交给文件名，把正文聚焦为客观 Case 和 Protection。

### Why Not

没有新增 `Applies / Does Not Apply`，因为多数 Lesson 可以通过清晰 Case 判断适用性，强制该区块会增加形式负担。没有单独新增 `Protection Evidence`，因为 Protection 可以同时说明动作和验证位置。没有保留 `Fix` 作为必备区块，因为 `Resolution` 更准确表达“当时如何解决或稳定”，并且不和 Protection 抢职责。

### If Modifying This Area, Check

- 同步根 `templates/LESSON.md` 和 bundled `skills/using-agentmentor/assets/templates/LESSON.md`。
- 同步根 `scripts/knowledge_check.py` 和 bundled `skills/using-agentmentor/scripts/knowledge_check.py`。
- 检查 `skills/knowledge-capture/SKILL.md`、artifact decision matrix 和 `skills/incident-learning/SKILL.md` 的 Lesson 写入边界是否一致。
- 运行 `tests/test_knowledge_check.py`、strict knowledge check 和 F011 local Feature Index check。
- 迁移现有 Lesson 时保留事实，不把历史改写成新的结论。

## Current Status

Completed。Lesson 模板、validator、skill 规则、现有 Lesson 和 Evidence 已完成迁移并通过验证。

## Links

### Evidence

- [EV-018 Lesson Case Protection Governance](../evidence/EV-018-lesson-case-protection-governance.md)

### Decisions / ADRs

- None.

### Lessons

- [LL-001 Patch Churn Requires Zero-Base Review](../lessons/LL-001-patch-churn-zero-base-review.md)
- [LL-004 Verify Codex Hook Schema Before Reinstalling Plugin Cache](../lessons/LL-004-codex-hook-plugin-schema-before-cache.md)
- [LL-008 Skill Naming Affects Discovery Scope](../lessons/LL-008-skill-naming-affects-discovery-scope.md)

### Specs / Plans

- None.

### Related Features

- [F009 Feature Intake Governance](F009-feature-intake-governance.md)

### External Context

- [Lesson template](../../templates/LESSON.md)
- [knowledge-capture](../../skills/knowledge-capture/SKILL.md)
- [incident-learning](../../skills/incident-learning/SKILL.md)

## Acceptance Criteria

- [x] Lesson 文件命名规则明确：领域、失败现象、防护点。
- [x] Lesson 模板包含 Case、Resolution、Pitfall、Root Cause、Protection、Source、Principle。
- [x] `knowledge_check.py` 不再要求 Trigger/Fix，改为要求 Case/Resolution。
- [x] 现有 Lesson 迁移到新版结构。
- [x] Knowledge Capture 和 Incident Learning 的 Lesson 写入规则与新版结构一致。

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| Lesson 结构承载客观案例与防复发 | 模板和现有 Lesson 均包含 Case、Resolution、Protection | [EV-018](../evidence/EV-018-lesson-case-protection-governance.md) | completed |
| Validator 固化新版 Lesson 结构 | `tests/test_knowledge_check.py` 覆盖 Case / Resolution 必备区块 | [EV-018](../evidence/EV-018-lesson-case-protection-governance.md) | completed |
| Lesson 写入边界进入收尾规则 | Knowledge Capture、artifact decision matrix、Incident Learning 使用新版 Lesson 语义 | [EV-018](../evidence/EV-018-lesson-case-protection-governance.md) | completed |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-06-27 | completed | Lesson governance iteration | [EV-018](../evidence/EV-018-lesson-case-protection-governance.md) | 文件名负责召回，正文负责 Case、Resolution 和 Protection。 |

## Patch History

None yet.

## Evidence

- [EV-018 Lesson Case Protection Governance](../evidence/EV-018-lesson-case-protection-governance.md)

## Recovery Snapshot

- Read first: this Feature page, then EV-018 and the Lesson template.
- Current capability state: completed; Lesson uses Case/Resolution/Pitfall/Root Cause/Protection/Source/Principle.
- Known risks: 旧 Lesson 文件名尚未批量重命名，召回率优化先通过命名规则约束后续新增 Lesson。
- Next safe action: 如果未来出现 Lesson 漏召回，再考虑 `trigger_terms` frontmatter 或 `docs/lessons/INDEX.md`。
- Unblock condition: not blocked.

## Next Step

观察真实 Lesson 写入质量；如果 Protection 仍写成空泛提醒，再给 validator 增加低线检查。
