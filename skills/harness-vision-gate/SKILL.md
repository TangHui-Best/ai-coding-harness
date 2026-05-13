---
name: harness-vision-gate
description: MUST use when non-trivial engineering work may drift from user intent before implementation, coding, refactoring, review, merge, done, acceptance, release, or handoff; covers original-intent checks, scope alignment, acceptance-criteria drift, product direction, user pain point, UI alignment, deliverable-goal fit, independent reviewer decisions via Delegation Gate, 开发前防跑偏, 愿景守护, 原始需求, 用户真实目标, AC 偏差, 方向跑偏, or 是否解决痛点.
---

# Harness Vision Gate

## Purpose

Use this gate before implementation to align the work with the original user goal, and before review, merge, done, acceptance, release, or handoff to check whether the final deliverable still serves that goal.

It protects against two failures:

- Entry drift: the agent starts coding from a distorted goal, unclear boundary, or false requirement.
- Exit drift: tests, acceptance criteria, and code review pass, but the user would still say, "this is not what I needed."

Vision Gate is a judgment checkpoint grounded in pre-work artifacts and original intent. It is not a replacement for tests, Evidence, ADRs, Lessons, specs, or formal project memory.

For non-trivial work, the gate must identify a durable Vision Anchor that later Entry or Exit Gates can reuse. Prefer the active Feature page. Use a linked spec, plan, discussion, or Evidence record only when it is the strongest available source. Do not treat chat history as sufficient when the work creates a delivery boundary that future sessions must recover.

## When To Use

Use Entry Gate before implementation when:

- Starting non-trivial development, refactoring, feature work, UI/UX work, or behavior changes.
- The original request may be underspecified, ambiguous, or compressed into acceptance criteria.
- The proposed path may be overbuilt, too broad, or misaligned with the user pain point.
- Work depends on product direction, UX tone, visual direction, module boundaries, or success criteria.

Use Exit Gate before review, merge, done, acceptance, release, or handoff when:

- Work is about to be marked reviewed, merged, done, accepted, shipped, or handed off.
- Acceptance criteria may be a lossy compression of the original request.
- A technically correct change may miss the user pain point, product intent, UX goal, or visual direction.
- UI work has prototypes, screenshots, design artifacts, or visual expectations that should anchor the final experience.
- A reviewer asks whether the deliverable matches the goal or whether product direction has drifted.

Do not use this for:

- Basic lint/build/test verification.
- Deciding whether a Feature, spec, plan, or ADR must exist before coding. Use `harness-start-gate`.
- Writing official ADR, Lesson, Evidence, or Feature updates. Route to `harness-knowledge-capture`.
- Explaining why implementation paths were rejected. Route to `harness-change-narrative`.
- Reopening scope because a new idea is attractive. Vision Gate protects the original goal; it is not a feature wishlist.

## Standard Sources

Evaluate alignment from the strongest available source, in this order:

1. Feature Vision Anchor, linked spec, or another durable original-intent record.
2. Original user request, pain point, or conversation statement.
3. Feature, spec, plan, or acceptance criteria created before implementation.
4. `AGENTS.md` or project-level rules.
5. Relevant ADRs, Lessons, Evidence, or stale-doc lifecycle records.
6. Domain standards such as accessibility, security, performance, release, or platform conventions.
7. General industry practice only as supporting context, never as a replacement for project truth.

If no durable Vision Anchor exists for non-trivial work, report the gap and return `needs knowledge capture` or `needs clarification` instead of approving implementation. Do not turn Vision Gate into a taste-based review.

## Required Inputs

For Entry Gate, gather the smallest set that lets the agent judge intent before acting:

- Original request, user story, spec, Feature page, or conversation context.
- Durable Vision Anchor: user pain point, desired outcome, non-goals, and the source the Exit Gate will compare against.
- Known acceptance criteria, constraints, non-goals, and module boundaries.
- Proposed implementation path or task plan, if one exists.
- Existing Harness context that may affect intent, after `harness-knowledge-retrieval` when needed.
- For UI: design/prototype/screenshot/visual brief or stated product tone.

For Exit Gate, gather the smallest set that lets an independent reviewer judge intent against outcome:

- Original request, user story, spec, or Feature page.
- Durable Vision Anchor used at Entry Gate, or the reason it was absent and how alignment will be judged.
- Acceptance criteria and later scope changes.
- Final deliverable: behavior, PR, artifact, UI, screenshot, prototype, demo, or release note.
- Verification evidence already collected: tests, build, screenshots, browser checks, or manual validation notes.
- For UI: design/prototype/screenshot/visual brief, plus the final rendered result.

## Reviewer Policy

Use the lightest honest independence level:

| Task/risk | Reviewer policy |
| --- | --- |
| Tiny or routine, low-risk | Self-review is allowed. |
| Non-trivial feature, refactor, user-facing change, or unclear scope | Independent agent or human review is recommended. |
| High-risk architecture, data model, security, migration, release, major UX, or external contract | Independent agent or human review is required unless unavailable. |

Use `harness-delegation-gate` in `review` mode when independent review is recommended or required, or when platform policy requires user authorization before dispatching an independent reviewer.

When using an independent reviewer, give them the original request and final deliverable first. Avoid giving the full implementation history unless they ask for it. This reduces anchoring on how the work was built.

If an independent reviewer is required but unavailable, say so and route the residual risk to `harness-readiness-dashboard` or `harness-knowledge-capture` instead of silently self-approving.

## Optional Lenses

Keep the default gate focused on original intent. Add these lenses only when the task source or risk triggers them:

| Lens | Trigger | Question |
| --- | --- | --- |
| Product | User-facing behavior, scope, or strategy changed. | Does the result still solve the original pain point? |
| Engineering | Architecture, module boundary, data model, performance, or reliability changed. | Does the result respect known constraints, ADRs, and test expectations? |
| UX/DX | UI, API, CLI, SDK, docs, onboarding, or developer workflow changed. | Does the real user or developer path still fit the promised experience? |
| Release | PR, merge, deployment, handoff, rollback, or operational risk is in scope. | Is the release path backed by evidence and a clear next owner? |

Lenses are aids, not new sources of truth. If a lens finds a recurring issue, route the learning through `harness-knowledge-capture`.

## Gate Questions

For Entry Gate, answer these before implementation:

1. What is the original user goal or pain point, in one sentence?
2. Is the proposed work the smallest coherent path toward that goal?
3. Are scope boundaries, non-goals, and module ownership clear enough to start?
4. Are acceptance criteria faithful to the original request, or have they dropped key intent?
5. Is there ambiguity that must be clarified before coding instead of guessed?
6. Is the proposed path unnecessarily costly, broad, or complex compared with a clearer route?
7. Does any decision, risk, or assumption need durable capture before work begins?
8. Which durable Vision Anchor will the Exit Gate use later?

For Exit Gate, answer these before review, merge, done, acceptance, release, or handoff:

1. Does this deliverable move the system closer to the original user vision?
2. Did the implementation introduce anything that moves the product away from that vision?
3. If the user saw the final experience now, would they believe the original pain point was solved?
4. Did the acceptance criteria drop, narrow, or distort any key intent from the original request?
5. For UI work, does the final experience match the agreed visual direction, interaction feel, and product tone?
6. Are there unresolved gaps that should become follow-up work instead of blocking this delivery?
7. Is there a decision, lesson, evidence item, or Feature state change that needs durable capture?
8. Did the required reviewer policy run, or is readiness conditional on independent review?

Treat "all tests pass" as evidence of implementation health, not proof of product alignment.

## Outcomes

Return exactly one primary outcome:

| Outcome | Use when | Next action |
| --- | --- | --- |
| `ready to implement` | Entry Gate finds clear intent, bounded scope, and a proportionate path. | Proceed with implementation workflow. |
| `needs clarification` | Entry Gate finds ambiguity that could change the implementation. | Ask the user specific questions before coding. |
| `scope mismatch` | Entry Gate finds the proposed work is too broad, too narrow, or solving the wrong problem. | Revise the scope or implementation path before coding. |
| `pass` | Deliverable aligns with the original goal and no meaningful drift is found. | Proceed with review, merge, done, or acceptance. |
| `needs revision` | The current deliverable misses or contradicts a core part of the original intent. | Revise before proceeding. Name the drift clearly. |
| `needs follow-up` | The core goal is served, but non-blocking gaps or adjacent work remain. | Create follow-up work if the project uses a backlog. |
| `needs knowledge capture` | A decision, lesson, evidence record, or Feature state needs durable memory. | Use `harness-knowledge-capture`. |

If the gate exposes a rejected path that must be explained for reviewers or future maintainers, use `harness-change-narrative`.

## Report Format

```text
Vision Gate: ready to implement | needs clarification | scope mismatch | pass | needs revision | needs follow-up | needs knowledge capture
Mode:
- Entry Gate | Exit Gate
Original intent:
- ...
Alignment:
- ...
Drift risks:
- ...
User pain point:
- ...
Source documents:
- ...
Vision Anchor:
- ...
Reviewer policy:
- self-review allowed | independent recommended | independent required
Independent review decision:
- not needed | ask user | authorized | declined | required | blocked | conditional
Optional lenses used:
- none | Product | Engineering | UX/DX | Release
Acceptance-criteria drift:
- ...
UI/visual alignment, if applicable:
- ...
Required next action:
- ...
```

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Running Vision Gate only at the end. | Use Entry Gate before non-trivial implementation and Exit Gate before acceptance or handoff. |
| Treating acceptance criteria as the whole truth. | Compare acceptance criteria back to the original request and user pain point. |
| Letting the Vision Anchor live only in chat for non-trivial work. | Capture the smallest durable anchor in the Feature page or linked spec before coding. |
| Letting tests stand in for product judgment. | Tests prove behavior, not whether the behavior was worth building. |
| Reviewing the implementation journey first. | Start from original intent and final experience to reduce anchoring. |
| Expanding scope during the gate. | Separate "missed original intent" from "interesting new idea." |
| Writing ADR/Lesson/Evidence here. | Route durable knowledge work to `harness-knowledge-capture`. |
| Using optional lenses as generic best-practice audits. | Activate lenses only when task type or risk requires them, and ground them in source documents. |
| Self-approving high-risk work because review is inconvenient. | Mark independent review as required or explicitly record the residual risk. |
