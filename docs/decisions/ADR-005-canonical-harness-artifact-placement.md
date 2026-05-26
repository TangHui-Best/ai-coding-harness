---
id: ADR-005
doc_kind: adr
status: accepted
scope: project
feature_refs: [docs/features/F002-canonical-harness-artifact-placement.md]
decision_area: harness-knowledge-model
created: 2026-05-26
updated: 2026-05-26
---

# ADR-005: Canonical Harness Artifact Placement

## Context

Harness 的价值来自可检索、可验收、可恢复的结构化记忆。一次实际使用暴露出混用风险：Agent 在 legacy `docs/superpowers/specs` 下写入 `doc_kind: spec`，又在 `docs/superpowers/evidence` 下写入 `doc_kind: evidence`。旧 validator 默认忽略 unsupported `doc_kind`，并且只要目录名不是 top-level Harness 目录就不会检查 placement，导致错误路径安静通过。

这会让后续 Agent 误以为已经有 Harness Feature memory，但实际没有 `docs/features/Fxxx-*.md` 作为 Vision Anchor。

## Decision

Harness knowledge artifacts 只能放在 selected docs root 的 canonical 目录：

- `docs/features/Fxxx-slug.md`
- `docs/decisions/ADR-xxx-slug.md`
- `docs/lessons/LL-xxx-slug.md`
- `docs/evidence/EV-xxx-slug.md`

`knowledge_check.py` 默认检查任何带 `doc_kind` frontmatter 的 Markdown。若 `doc_kind` 不属于 `feature`、`adr`、`lesson`、`evidence`，直接报错。若 supported artifact 不在对应 canonical 目录，也直接报错。

`docs/superpowers/**` 可以作为历史 Superpowers spec/plan 存在，并可从 Feature 链接，但不能承载 Harness Feature、ADR、Lesson 或 Evidence。

## Alternatives

- 只在 `--all-markdown` 下检查 legacy 路径：拒绝，因为 closeout 和普通 review 很容易漏掉该参数，问题会继续安静通过。
- 对非 canonical placement 只给 warning：拒绝，因为 artifact 路径错误会破坏 Feature attribution 和 retrieval，属于结构错误，不是风格问题。
- 允许项目自定义 Harness artifact 目录：暂不采用。可配置目录会提高每个项目和每个 Agent 的解析成本；当前收益不足以抵消复杂度。
- 把 `spec` 加入 Harness artifact 类型：拒绝。spec/plan 可以作为 Feature 的 linked material，但 Harness durable memory 的入口仍应是 Feature、ADR、Lesson、Evidence。

## Consequences

Agent 不能再因为项目已有 `docs/superpowers/**` 就把 Harness memory 写进去。第一次为 legacy Superpowers 项目引入 Harness 时，应创建 canonical `docs/features`、`docs/evidence` 等目录，然后链接旧 spec/plan。

代价是旧项目中带 `doc_kind` 的 Superpowers 文档会在新 validator 下失败，需要迁移或移除伪 Harness frontmatter。这个失败是有意的：它把错误记忆结构显式暴露出来。

## Evidence

- [F002 Canonical Harness Artifact Placement](../features/F002-canonical-harness-artifact-placement.md)
- [EV-003 Canonical Artifact Placement](../evidence/EV-003-canonical-artifact-placement.md)
- `tests/test_knowledge_check.py`
- `scripts/knowledge_check.py`
- `skills/using-harness/scripts/knowledge_check.py`
