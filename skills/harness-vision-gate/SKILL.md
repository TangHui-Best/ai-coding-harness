---
name: harness-vision-gate
description: Use before review, merge, done, acceptance, release, or handoff when a deliverable may need an original-intent check, acceptance-criteria drift check, product-direction check, user-pain-point check, UI alignment check, or deliverable-goal fit check.
---

# Harness Vision Gate

## Purpose

Use this gate before review, merge, done, acceptance, release, or handoff to check whether the final deliverable still serves the original user goal.

The failure mode it protects against is subtle: tests, acceptance criteria, and code review pass, but the user would still say, "this is not what I needed."

Vision Gate is a judgment checkpoint, not a replacement for tests, Evidence, ADRs, Lessons, or formal project memory.

## When To Use

Use this when:

- Work is about to be marked reviewed, merged, done, accepted, shipped, or handed off.
- Acceptance criteria may be a lossy compression of the original request.
- A technically correct change may miss the user pain point, product intent, UX goal, or visual direction.
- UI work has prototypes, screenshots, design artifacts, or visual expectations that should anchor the final experience.
- A reviewer asks whether the deliverable matches the goal or whether product direction has drifted.

Do not use this for:

- Basic lint/build/test verification.
- Writing official ADR, Lesson, Evidence, or Feature updates. Route to `harness-knowledge-capture`.
- Explaining why implementation paths were rejected. Route to `harness-change-narrative`.
- Reopening scope because a new idea is attractive. Vision Gate protects the original goal; it is not a feature wishlist.

## Required Inputs

Gather the smallest set that lets an independent reviewer judge intent against outcome:

- Original request, user story, spec, or Feature page.
- Acceptance criteria and later scope changes.
- Final deliverable: behavior, PR, artifact, UI, screenshot, prototype, demo, or release note.
- Verification evidence already collected: tests, build, screenshots, browser checks, or manual validation notes.
- For UI: design/prototype/screenshot/visual brief, plus the final rendered result.

When possible, ask an independent agent or human to run this gate. Give them the original request and final deliverable first; avoid giving the full implementation history unless they ask for it. This reduces anchoring on how the work was built.

## Gate Questions

Answer these in order:

1. Does this deliverable move the system closer to the original user vision?
2. Did the implementation introduce anything that moves the product away from that vision?
3. If the user saw the final experience now, would they believe the original pain point was solved?
4. Did the acceptance criteria drop, narrow, or distort any key intent from the original request?
5. For UI work, does the final experience match the agreed visual direction, interaction feel, and product tone?
6. Are there unresolved gaps that should become follow-up work instead of blocking this delivery?
7. Is there a decision, lesson, evidence item, or Feature state change that needs durable capture?

Treat "all tests pass" as evidence of implementation health, not proof of product alignment.

## Outcomes

Return exactly one primary outcome:

| Outcome | Use when | Next action |
| --- | --- | --- |
| `pass` | Deliverable aligns with the original goal and no meaningful drift is found. | Proceed with review, merge, done, or acceptance. |
| `needs revision` | The current deliverable misses or contradicts a core part of the original intent. | Revise before proceeding. Name the drift clearly. |
| `needs follow-up` | The core goal is served, but non-blocking gaps or adjacent work remain. | Create follow-up work if the project uses a backlog. |
| `needs knowledge capture` | A decision, lesson, evidence record, or Feature state needs durable memory. | Use `harness-knowledge-capture`. |

If the gate exposes a rejected path that must be explained for reviewers or future maintainers, use `harness-change-narrative`.

## Report Format

```text
Vision Gate: pass | needs revision | needs follow-up | needs knowledge capture
Original intent:
- ...
Alignment:
- ...
Drift risks:
- ...
User pain point:
- ...
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
| Treating acceptance criteria as the whole truth. | Compare acceptance criteria back to the original request and user pain point. |
| Letting tests stand in for product judgment. | Tests prove behavior, not whether the behavior was worth building. |
| Reviewing the implementation journey first. | Start from original intent and final experience to reduce anchoring. |
| Expanding scope during the gate. | Separate "missed original intent" from "interesting new idea." |
| Writing ADR/Lesson/Evidence here. | Route durable knowledge work to `harness-knowledge-capture`. |
