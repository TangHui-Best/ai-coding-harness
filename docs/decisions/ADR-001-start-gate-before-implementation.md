---
id: ADR-001
doc_kind: adr
status: accepted
scope: project
feature_ids: []
decision_area: harness-workflow
created: 2026-05-09
updated: 2026-05-09
---

# ADR-001: Start Gate Before Implementation

## Context

Harness skills already required knowledge retrieval and Vision Gate around non-trivial work, but the workflow did not explicitly decide whether implementation could start or whether Feature, spec, plan, ADR, Backlog, or handoff anchors were required first.

That gap let agents rely on completion-time knowledge capture for artifacts that sometimes need to exist before coding begins.

## Decision

Add `harness-start-gate` as the first non-trivial implementation gate. It classifies the task, checks risk triggers, and returns one required next action before coding starts.

Keep Start Gate as a routing skill. It does not create artifacts or replace verification, Vision Gate, or completion-time knowledge capture.

## Alternatives

- Extend `harness-vision-gate`: rejected because Vision Gate should judge alignment with user intent, not own artifact readiness or implementation intake.
- Extend `knowledge_check.py`: rejected because the script can validate existing Markdown structure but cannot reliably infer task intent or missing pre-work context.
- Move `harness-knowledge-capture` earlier without a new gate: rejected because capture owns durable memory creation, while the missing control point is the decision about whether memory is required before implementation.

## Consequences

Agents get a clearer pre-coding control point and can stop before coding when clarification, retrieval, or durable pre-work anchors are missing.

The trade-off is one more skill in the routing surface. To keep the workflow lightweight, Start Gate must return `ready` for tiny or routine tasks where no project memory can change the result.

## Evidence

- `skills/harness-start-gate/SKILL.md`
- `skills/using-harness/SKILL.md`
- `docs/workflow.md`
- `docs/skill-index.md`
