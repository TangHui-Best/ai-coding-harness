# Artifact Decision Matrix

Use this reference when deciding whether Harness needs a durable artifact.

## Matrix

| Boundary | Preferred carrier | Rule |
| --- | --- | --- |
| Current active work, next step, recovery context | `docs/BACKLOG.md` or handoff note | Update only when future sessions need this state. |
| Delivery boundary, Vision Anchor, status, acceptance criteria, related links | Feature page | Create or update when the task advances a Feature or needs a durable original-intent anchor. |
| Detailed requirement or scope | Spec linked from Feature | Link it; do not copy the spec into the Feature page. |
| Execution route or task breakdown | Plan linked from Feature | Link it; update Feature status and next step if they changed. |
| Decision conversation, issue thread, review thread | Discussion linked from Feature | Link it when it explains current state or open questions. |
| Defect reproduction, impact, expected behavior | Bug report linked from Feature | Link it; create a Lesson only if the failure mode can recur. |
| Exploration before a decision | Research linked from Feature or ADR | Link it; create an ADR only when a decision is made. |
| Why this option, why not alternatives | ADR | Create a dedicated ADR when the decision will be questioned later. |
| Recurring failure mode and protection | Lesson | Create a dedicated Lesson when caution must become a guardrail. |
| Proof of completion | Evidence location or Evidence doc | Record proof every time; create an Evidence doc only when retrieval or audit matters. |

## Feature Pages

Feature pages are indexes, not containers for all material. Prefer linking spec, plan, discussion, bug report, research, and detailed Vision Gate Evidence over copying their content.

Keep the Feature page's Vision Anchor short enough to remain a stable source for later Exit Gates.

Create or update a Feature page when:

- A Feature status changes.
- A spec, plan, discussion, bug report, research, ADR, Lesson, or Evidence artifact is added.
- Acceptance criteria change.
- New constraints are discovered.
- The task advances a Feature.
- Non-trivial work would otherwise rely on chat history as the only Vision Gate source.

## ADR

Write an ADR when the task makes a decision future agents are likely to question.

Trigger on:

- High-cost rollback technical choices.
- Changes to module boundaries, data models, or interface contracts.
- New frameworks, infrastructure, storage, or messaging mechanisms.
- Rejected alternatives that are likely to be proposed again.
- Decisions affecting multiple Features or long-term evolution.
- Security, performance, cost, compliance, or operational tradeoffs.

## Lesson

Write a Lesson when a failure mode can recur and needs a protection mechanism.

If the fix ends with "be careful next time", write a Lesson and turn caution into protection.

## Placement

Use these canonical paths under the selected docs root:

```text
docs/BACKLOG.md
docs/features/Fxxx-slug.md
docs/decisions/ADR-xxx-slug.md
docs/lessons/LL-xxx-slug.md
docs/evidence/EV-xxx-slug.md
```

Do not place Harness Feature, ADR, Lesson, or Evidence artifacts under `docs/superpowers/**`. Legacy Superpowers specs and plans may remain linked from a Feature, but Harness memory uses the canonical directories so `knowledge_check.py --strict` can validate it deterministically.
