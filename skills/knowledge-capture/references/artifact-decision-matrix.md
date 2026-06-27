# Artifact Decision Matrix

Use this reference when deciding whether Harness needs a durable artifact.

## Matrix

| Boundary | Preferred carrier | Rule |
| --- | --- | --- |
| Current active work, next step, recovery context | `docs/BACKLOG.md` or handoff note | Update only when future sessions need this state. |
| Delivery boundary, Vision Anchor, status, acceptance criteria, related links | Feature page | Create or update when the task advances a Feature or needs a durable original-intent anchor; require Feature Intake before writing. |
| Detailed requirement or scope | Spec linked from Feature | Link it; do not copy the spec into the Feature page. |
| Execution route or task breakdown | Plan linked from Feature | Link it; update Feature status and next step if they changed. |
| Decision conversation, issue thread, review thread | Discussion linked from Feature | Link it when it explains current state or open questions. |
| Defect reproduction, impact, expected behavior | Bug report linked from Feature | Link it; create a Lesson only if the failure mode can recur. |
| Exploration before a decision | Research linked from Feature or ADR | Link it; create an ADR only when a decision is made. |
| Durable decision boundary, accepted option, rejected options | ADR | Create a dedicated ADR when future maintainers or agents may need to preserve, challenge, or revise the decision boundary. |
| Recurring failure mode and protection | Lesson | Create a dedicated Lesson when caution must become a guardrail. |
| Proof of completion | Evidence location or Evidence doc | Record proof every time; create an Evidence doc only when retrieval or audit matters. |

## Feature Pages

Feature pages are indexes, not containers for all material. Prefer linking spec, plan, discussion, bug report, research, and detailed Vision Gate Evidence over copying their content.

Keep the Feature page's Vision Anchor short enough to remain a stable source for later Exit Gates.

Feature owns the capability boundary and recovery entrypoint. It should answer:

- What capability or delivery boundary is being governed?
- Why does this capability exist, and what is outside its scope?
- What must be true before the capability can be called accepted?
- Which Evidence, ADRs, Lessons, specs, plans, discussions, or related Features should a future Agent open next?

Feature should not be the primary carrier for architecture decisions, recurring failure-mode protections, command output logs, or full specs/plans. Link those artifacts by type from `## Links`.

Before writing a new Feature or materially changing an existing one, complete Feature Intake:

- Original problem.
- User pain point.
- Capability promise.
- Non-goals.
- Acceptance source.
- Open questions.

If any answer is unknown, ask the user or retrieve the source first. Do not create a Feature that turns ambiguity into durable memory.

Feature pages should also include:

- `Capability Contract`: the current capability boundary, not implementation steps.
- `Acceptance Map`: claim-to-acceptance-to-Evidence traceability.
- `State Timeline`: meaningful state changes without becoming a full changelog.
- `Recovery Snapshot`: the shortest path for a future Agent to continue safely.

Create or update a Feature page when:

- A Feature status changes.
- A spec, plan, discussion, bug report, research, ADR, Lesson, or Evidence artifact is added.
- Acceptance criteria change.
- New constraints are discovered.
- The task advances a Feature.
- Non-trivial work would otherwise rely on chat history as the only Vision Gate source.

## ADR

Write an ADR when the task creates or changes a durable decision boundary that future maintainers or agents may need to preserve, challenge, or revise.

Trigger on:

- High-cost rollback technical choices.
- Changes to module boundaries, data models, or interface contracts.
- New frameworks, infrastructure, storage, or messaging mechanisms.
- Rejected options that are likely to be proposed again.
- Decisions affecting multiple Features or long-term evolution.
- Security, performance, cost, compliance, or operational tradeoffs.

ADR owns durable decision rationale. It should answer:

- What decision was made?
- What boundary does the decision apply to, and what does it not apply to?
- Which options were rejected?
- Why is this tradeoff acceptable now?
- What consequences or constraints must future agents preserve?
- What must be checked before changing or reversing the decision?

Do not write an ADR for every local implementation choice. If the choice is fully explained by the Feature's capability boundary and has low future reversal cost, keep it in Feature `Decision Context`.

Name ADR files for recall before reading. Prefer `ADR-xxx-<decision-area>-<accepted-choice>.md`; the file name should carry the decision area and accepted choice without listing every rejected option.

## Lesson

Write a Lesson when a failure mode can recur and needs a protection mechanism.

If the fix ends with "be careful next time", write a Lesson and turn caution into protection.

Lesson owns recurring failure prevention. It should answer:

- What objective case happened?
- How was it resolved or stabilized at the time?
- What failure mode recurs or could recur?
- What concrete protection prevents recurrence?
- Which Feature, ADR, Evidence, test, hook, or rule proves the protection exists?

Do not write a Lesson for one-off history, ordinary status, or a decision tradeoff without a failure mode. Use Feature, ADR, or Evidence instead.

Name Lesson files for recall before reading. Prefer `LL-xxx-<domain>-<failure-symptom>-<protection>.md` over abstract titles; the file name should carry the domain, observable failure symptom, and protection point.

## Placement

Use these canonical paths under the selected docs root:

```text
docs/BACKLOG.md
docs/features/Fxxx-slug.md
docs/decisions/ADR-xxx-slug.md
docs/lessons/LL-xxx-slug.md
docs/evidence/EV-xxx-slug.md
```

Do not place Harness Feature, ADR, Lesson, or Evidence artifacts under `docs/superpowers/**`. Legacy Superpowers specs and plans may remain linked from a Feature, but AgentMentor memory uses the canonical directories so `knowledge_check.py --strict` can validate it deterministically.
