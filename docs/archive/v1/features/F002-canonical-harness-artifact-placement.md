---
id: F002
doc_kind: feature
status: completed
created: 2026-05-26
updated: 2026-05-26
---

# F002: Canonical Harness Artifact Placement

## Goal

让 AgentMentor knowledge artifacts 使用稳定、可校验的 canonical 目录，避免 Agent 把 Superpowers spec/plan 路径和 Harness Feature/Evidence 语义混用后仍然通过校验。

## Vision Anchor

- 原始请求或来源：用户指出某次 Harness skill 会话沉淀的 Feature 没有使用 `F001` 编码，且路径落在 `docs/superpowers/**`，要求分析后优化 Harness skill 并同步到本机。
- 用户痛点或工程问题：`knowledge_check.py` 默认忽略 `doc_kind: spec`，同时接受 `docs/superpowers/evidence` 下的 Evidence，导致错误沉淀路径没有被闸门发现。
- 期望结果：带 `doc_kind` 的 Markdown 默认都被检查；Harness Feature、ADR、Lesson、Evidence 必须位于 canonical 目录；skill 文案明确 `docs/superpowers/**` 只能作为 legacy spec/plan 被链接。
- 非目标或边界：不迁移其他项目的历史文档，不把 Superpowers spec/plan 本身纳入 AgentMentor artifact 类型，不引入项目级 registry。
- Exit Gate 对照来源：本 Feature 的 Acceptance Criteria、ADR-005、EV-003、`tests.test_knowledge_check.KnowledgeCheckPlacementTests`。

## Feature Intake

- Original problem: See `## Vision Anchor` original request or source.
- User pain point: See `## Vision Anchor` user pain point or engineering problem.
- Capability promise: Preserve the capability described by `## Goal` and `## Acceptance Criteria`.
- Non-goals: See `## Vision Anchor` non-goals or boundaries.
- Acceptance source: This Feature page and linked Evidence.
- Open questions: none recorded for this completed Feature.

## Capability Contract

- The completed capability boundary is defined by `## Goal`, `## Vision Anchor`, and `## Acceptance Criteria`; detailed proof stays in linked Evidence.

## Decision Context

### Why

AgentMentor artifact 需要稳定路径，未来 Agent 才能用相同规则检索 Feature、ADR、Lesson 和 Evidence。

### Why Not

没有沿用 `docs/superpowers/**` 作为正式 artifact 目录，因为 Superpowers spec/plan 是 linked material，不是 AgentMentor 的事实源目录。

### If Modifying This Area, Check

- 检查 `knowledge_check.py` 的 canonical directory 规则。
- 检查 Feature、ADR、Lesson、Evidence 模板和相关安装文档是否需要同步更新。

## Current Status

Done。validator、bundled skill validator 和 Harness skill 文案已经更新；本机 Codex skills 已同步。

## Links

### Evidence

- [EV-003 Canonical Artifact Placement](../evidence/EV-003-canonical-artifact-placement.md)
- [EV-004 Hot Path Harness Constraints](../evidence/EV-004-hot-path-harness-constraints.md)
- [EV-005 Skill Iteration Learning Docs](../evidence/EV-005-skill-iteration-learning-docs.md)

### Decisions / ADRs

- [ADR-005 Canonical Harness Artifact Placement](../decisions/ADR-005-canonical-harness-artifact-placement.md)
- [ADR-006 Skill Progressive Disclosure Boundary](../decisions/ADR-006-skill-progressive-disclosure-boundary.md)

### Lessons

- [LL-002 Skill Hot Path Constraints Must Stay Visible](../lessons/LL-002-skill-hot-path-constraints.md)

### Specs / Plans

- None.

### Related Features

- None.

### External Context

- [Guide: AgentMentor Skill 迭代复盘](../guides/skill-iteration-lessons.md)

## Acceptance Criteria

- [x] `knowledge_check.py` 默认检查所有带 `doc_kind` frontmatter 的 Markdown。
- [x] `doc_kind: spec` 在默认校验中被拒绝，而不是只在 `--all-markdown` 下暴露。
- [x] `doc_kind: evidence` 放在 `docs/superpowers/evidence` 会被拒绝，并提示应放在 `docs/evidence/`。
- [x] root validator 与 bundled `skills/using-agentmentor/scripts/knowledge_check.py` 行为一致。
- [x] `using-agentmentor`、`start-gate`、`knowledge-capture` 明确禁止把 AgentMentor artifacts 放进 `docs/superpowers/**`。
- [x] `scripts/install.ps1 codex` 可把更新后的 AgentMentor skills 同步到本机 Codex skills。

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| Feature acceptance criteria are satisfied | Checked items in `## Acceptance Criteria` | See `## Evidence` | completed |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-05-26 | completed | Feature implementation closed | See `## Evidence` | Legacy Feature migrated to the stricter governance shape. |

## Patch History

| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |
| --- | --- | --- | --- | --- | --- | --- |
| F002.1 | 2026-05-27 | pending | Agent could still follow Superpowers spec/plan naming during real development even though canonical Harness placement existed in validator and references. | 2026-05-26 slimming moved some action-changing constraints out of primary `SKILL.md` hot paths while trying to avoid session stalls; the actual stall root cause was elsewhere. | Restored Entry/Exit Gate, placement, template, task-class, risk-trigger, and patch-churn constraints in primary skill text; added a regression test and Feature template path hint. | Done |

## Evidence

[EV-003 Canonical Artifact Placement](../evidence/EV-003-canonical-artifact-placement.md)
[EV-004 Hot Path Harness Constraints](../evidence/EV-004-hot-path-harness-constraints.md)
[EV-005 Skill Iteration Learning Docs](../evidence/EV-005-skill-iteration-learning-docs.md)

## Recovery Snapshot

- Read first: this Feature page, then linked Evidence.
- Current capability state: completed; see `## Current Status`.
- Known risks: none recorded beyond `## Patch History`.
- Next safe action: follow `## Next Step`; record any delivered-behavior follow-up in `## Patch History`.
- Unblock condition: not blocked.

## Next Step

若后续发现其他 legacy docs 路径仍能伪装为 AgentMentor memory，通过本 Feature 的 Patch History 记录补丁，并优先补 validator 测试。
