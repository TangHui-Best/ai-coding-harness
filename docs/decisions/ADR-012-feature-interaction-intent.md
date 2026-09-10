---
id: ADR-012
doc_kind: adr
status: accepted
index_summary: 将用户旅程作为条件化的 Feature 交互意图，而非新增默认 Gate、Skill 或 UI 设计规范。
feature_refs:
  - F017-agentmentor-vnext-gpt56-workflow
decision_area: feature-interaction-specification
supersedes: []
created: 2026-09-10
updated: 2026-09-10
---

# ADR-012: 在 Feature 中沉淀条件化的交互意图

## Context

Feature 已能记录目标、行为和验收，却没有稳定位置记录用户在何种情境下理解状态、完成任务和从失败中恢复。仅靠愿景或业务行为不足以约束用户旅程；后续 Agent 容易在实现正确时仍让流程违背用户心智。

## Decision

对改变用户任务流程、状态理解或关键操作的 Feature，在 `## Specification` 下按需添加 `### Interaction Intent`。它只包含三个部分：用户目标与情境、主旅程、关键状态与保护。

主 Skill 只在涉及这类变化时读取和维护该契约；交互意图缺失且旅程发生实质变化时，先补最小规格再实现。与既定旅程的真实冲突使用 `agentmentor-intent`，长期且跨 Feature 的交互政策取舍使用 ADR。

## Boundary

- 交互意图属于 Feature 规格，不新增文档类型、Index 条目、默认 Gate 或第七个 Skill。
- 它不规定组件、布局、视觉 token、像素、具体文案或技术实现。
- 纯视觉润色、机械局部修改和无用户流程的后端任务不要求该章节。
- 该章节是条件化语义规格，不采用静态校验器强制每个 Feature 必填；验收场景与人工体验验证可按风险补充证据。

## Rejected Options

- 新增默认 UI/UX Gate：重新引入 vNext 刻意移除的串行热路径，且会误伤无用户流程的工程任务。
- 新建用户旅程文档类型：会使用户意图与所属 Feature 的目标、范围和验收分离，增加检索与生命周期成本。
- 在每个 Feature 强制填写完整 UX 模板：会诱发形式化填空，稀释真正影响用户决策的交互事实。
- 将组件或视觉规范放入交互意图：混淆行为契约与设计系统/实现边界。

## Consequences

- 用户可感知的流程拥有可检索、可审查、可验收的行为锚点。
- Feature 模板增加极小的条件化章节；普通任务的热路径不增加新的默认步骤。
- 交互质量仍需要适当的 E2E、人工走查、截图或原型证据，文本规格不替代体验验证。

## Revisit When

- 真实样本显示 Agent 经常漏写关键旅程，或反复把组件细节写入交互意图。
- 关键跨 Feature 流程需要独立生命周期，而无法由 Feature 链接和 ADR 清晰表达。
- 条件触发导致稳定、可测的漏检，且更强约束的收益明显超过热路径成本。

## Links / Evidence

- [F017](../features/F017-agentmentor-vnext-gpt56-workflow.md)
- 用户确认的 2026-09-10 方案：三段式交互意图；不新增默认 Gate 或 Skill。
