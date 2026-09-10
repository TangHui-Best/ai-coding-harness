---
name: agentmentor
description: Use when starting or resuming engineering work that may depend on project Feature specifications, ADRs, Lessons, Evidence, or prior design history. Retrieve one bounded AgentMentor context package before acting; do not use for tiny local edits with no context dependency.
---

# AgentMentor

Provide an engineering map, not a development state machine or routing engine.

1. Read `docs/INDEX.md` once when the task may change feature behavior, business rules, user-visible journeys, interface contracts, data meaning, architecture boundaries, or acceptance criteria. Skip it for a clearly mechanical, local edit with no behavior meaning.
2. Based on the task and each Index brief, choose the Feature and ADR documents that can change the current decision. Default to zero to three Feature documents; an exact user-provided Feature may be read directly.
3. Read directly linked ADRs, Lessons, or Evidence only when they materially affect the current implementation, acceptance, or risk judgment. Do not automatically expand every link or recursively search history.
4. Let the model decide normal planning, implementation, tests, review, and collaboration. Do not invoke a Start Gate, Vision Gate, Delegation Gate, Readiness Dashboard, or a second Index read.
5. Use another AgentMentor vNext Skill only if its event actually occurs.

## User-visible Interaction Changes

When a Feature changes a user's task flow, their understanding of state, or a consequential action, inspect its optional `### Interaction Intent` before planning or implementation. It is a behavioral contract, not a UI design system:

- Preserve its stated user goal, primary journey, and critical states or guardrails.
- If it is absent and the change materially alters a journey, add the smallest useful three-part interaction intent to the Feature before implementation.
- Do not add it for visual-only polishing, a mechanical local edit, or work with no user-visible flow; do not specify components, layouts, tokens, or implementation details there.
- Route a genuine conflict between the intended journey and a proposed change to `agentmentor-intent`. Record only stable, cross-Feature interaction-policy trade-offs through `agentmentor-decision`.

## Boundaries

- `docs/INDEX.md` is a generated directory of current Features and accepted ADRs. It is not a rule table and does not choose documents for the model.
- Search only vNext document roots. `docs/archive/v1/` is human-readable history, never runtime input.
- Do not create a Feature, ADR, Lesson, or Evidence merely because this Skill was used.
- Use `assets/templates/` when creating vNext knowledge artifacts.
- `Interaction Intent` is an optional section of a Feature, never a standalone artifact or a default Gate.

## Resources

- `scripts/generate_index.py`: generate or check the compact engineering index.
- `scripts/knowledge_check.py`: validate vNext documents after explicit document edits or in CI.
- `assets/templates/`: Feature, ADR, Lesson, Evidence, and compact closeout templates.
