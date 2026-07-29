---
name: agentmentor
description: Use when starting or resuming engineering work that may depend on project Feature specifications, ADRs, Lessons, Evidence, or prior design history. Retrieve one bounded AgentMentor context package before acting; do not use for tiny local edits with no context dependency.
---

# AgentMentor

Provide project memory, not a development state machine.

1. Run `python <skill-root>/scripts/context.py --root <project-root> --task "<task>"` once. Add `--path <changed-or-relevant-path>` for each known path.
2. Read only the returned Feature and directly linked documents. The package contains at most three body documents; `no relevant context` is a successful result.
3. Let the model decide normal planning, implementation, tests, review, and collaboration. Do not invoke a Start Gate, Vision Gate, Delegation Gate, Readiness Dashboard, or a second retrieval.
4. Use another AgentMentor vNext Skill only if its event actually occurs.

## Boundaries

- Search only vNext document roots. `docs/archive/v1/` is human-readable history, never runtime input.
- Do not expand a weak match into a global scan.
- Do not create a Feature, ADR, Lesson, or Evidence merely because this Skill was used.
- Use `assets/templates/` when creating vNext knowledge artifacts.

## Resources

- `scripts/context.py`: deterministic, bounded retrieval.
- `scripts/knowledge_check.py`: validate vNext documents after explicit document edits or in CI.
- `assets/templates/`: Feature, ADR, Lesson, Evidence, and compact closeout templates.
