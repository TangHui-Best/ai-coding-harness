---
name: harness-knowledge-capture
description: MUST use before claiming engineering work is complete, fixed, verified, reviewed, ready to commit, ready for PR, ready for handoff, or safely closed; also use for Evidence, Feature state, ADR/Lesson decisions, Backlog or handoff state, patch churn, bugfix attribution, 知识沉淀, 经验沉淀, 完成声明, 收尾, 准备提交, 准备 PR, or 交接.
---

# Harness Knowledge Capture

## Purpose

Use this skill to decide the smallest durable memory and completion gate needed before an engineering task is called complete.

Core boundary:

```text
This skill owns closeout and completion permission.
References own detailed policy.
Scripts own deterministic validation.
```

Do not create documents to look disciplined. Capture only the smallest artifact that prevents future confusion, repeated mistakes, or unverifiable completion claims.

Prefer Chinese for human-written Harness prose. Keep YAML keys, enum values, required headings, commands, paths, and code identifiers in English.

## Trigger Discipline

If you are about to say work is done, complete, fixed, verified, reviewed, ready to commit, ready for PR, ready for handoff, or safely closed, use this skill first.

This skill may conclude `no formal artifact needed`. The check is still required; the artifact is optional.

If this skill has not produced a `Completion claim allowed` verdict, do not use completion language. Say `implementation done, harness closeout pending` and finish the missing closeout work or report the blocker.

## Completion Verdict Ownership

This skill owns the completion verdict for Harness closeout.

- This skill owns the completion verdict, Evidence level, required closeout categories, and completion-claim permission.
- A `pass` or permitted `conditional` verdict is terminal for the requested stage. Do not re-run `using-harness`, `harness-change-narrative`, or this skill merely because a final answer is about to be written.
- If verification, readiness, knowledge-check, Vision Gate, or change narrative evidence was gathered earlier in the same turn and is still fresh, consume that evidence instead of re-running equivalent checks.
- If a required category is missing, produce `blocked` or `conditional` with the named blocker. Do not try to reach `pass` by recursively invoking adjacent Harness skills.
- A normal final response may summarize this verdict and evidence without triggering a new change narrative.

## Terminal Closeout Output

Terminal means no recursion, not invisible.

After this skill reaches a `pass` or permitted `conditional` verdict, the agent must still expose visible closeout status before claiming completion or readiness. The final response may use a compact closeout block, but it must not collapse the result to only "tests passed", "committed", or "Harness closeout check: pass".

A structural `harness_closeout_check.py` pass is not a substitute for the human-visible closeout status. It proves that a block was structurally valid; it does not by itself communicate Entry Gate, Vision Anchor, Evidence, Feature, ADR, Lesson, and Check state to the user or next agent.

For normal final responses, use this compact closeout block unless the user asks for the full status or the work is high risk:

```text
Closeout verdict: pass / conditional / blocked
Completion claim allowed: yes / no
Entry Gate: ...
Vision Anchor: ...
Evidence: ...
Evidence level: quick / standard / exhaustive
Feature: ...
ADR: ...
Lesson: ...
Check: ...
```

Expand to the full Final Response Contract when any omitted category is non-trivial, conditional, blocked, or newly updated. Never omit a blocked or conditional category.

## Workflow

1. Identify the smallest knowledge boundary: active work state, handoff, Feature delivery, decision, failure mode, evidence, or none.
2. Read only the references needed for that boundary.
3. Create or update the lightest durable artifact that fits the risk.
4. Link ADR, Lesson, and Evidence artifacts from the Feature page when a Feature is involved.
5. Update `docs/BACKLOG.md` or a handoff note only when active work state changed.
6. Record Evidence for every completion claim.
7. Run validators when Harness artifacts or closeout blocks changed.
8. Produce a visible closeout verdict and completion-claim permission.

## Artifact Placement

Use these canonical paths under the selected docs root:

```text
docs/BACKLOG.md
docs/features/Fxxx-slug.md
docs/decisions/ADR-xxx-slug.md
docs/lessons/LL-xxx-slug.md
docs/evidence/EV-xxx-slug.md
```

Do not place Harness Feature, ADR, Lesson, or Evidence artifacts under `docs/superpowers/**`. Superpowers specs and plans may remain there as linked material, but official Harness memory uses the canonical directories so `knowledge_check.py --strict` can validate it deterministically.

Create or update a Feature page when:

- A Feature status, acceptance criteria, constraints, related links, or next step changes.
- A spec, plan, discussion, bug report, research, ADR, Lesson, or Evidence artifact is added.
- The task advances a delivery boundary.
- Non-trivial work would otherwise rely on chat history as the only Vision Anchor.
- A completed or accepted Feature receives a non-tiny follow-up fix; update `## Patch History` on the original Feature with a patch id such as `F010.1`.

## Templates

Copy the matching bundled template from `using-harness/assets/templates/` and fill every required field and section. If a project vendors templates, prefer the project copy only when it is intentionally current with this Harness suite.

- Feature: `using-harness/assets/templates/FEATURE.md`
- ADR: `using-harness/assets/templates/ADR.md`
- Lesson: `using-harness/assets/templates/LESSON.md`
- Evidence: `using-harness/assets/templates/EVIDENCE.md`

Use Stable IDs:

- Feature: `F001`, with filename `docs/features/F001-slug.md`.
- ADR: `ADR-001`, with filename `docs/decisions/ADR-001-slug.md`.
- Lesson: `LL-001`, with filename `docs/lessons/LL-001-slug.md`.
- Evidence: `EV-001`, with filename `docs/evidence/EV-001-slug.md`.

Keep titles specific enough to scan in search results.

## Reference Map

Use references only when their trigger applies.

- `references/completion-closeout-contract.md`: read when a full closeout block, conditional/blocked status, readiness, Vision Gate Exit, or category-level completion rule matters.
- `references/artifact-decision-matrix.md`: read when deciding whether to create or update Feature, ADR, Lesson, Evidence, Backlog, handoff, spec, plan, discussion, bug report, or research artifacts.
- `references/bugfix-attribution-and-patch-churn.md`: read for non-tiny bugfixes, regressions, completed Feature owners, Patch History rows, repeated fixes, `Fxxx.n` follow-ups, or 3+ patch churn.

## Script Use

Execute bundled scripts; do not read script source unless debugging or editing that script.

Run verification commands before reading verification source.

Do not read test files, validator scripts, or workflow files merely to verify behavior. Read them only when debugging a failure, editing them, reviewing them, or explaining their behavior.

Run the bundled knowledge validator when Harness artifacts changed:

```bash
python <skills-root>/using-harness/scripts/knowledge_check.py --root <repo> --docs-path docs --strict
```

Run the bundled closeout validator when a closeout block exists in a file:

```bash
python <skills-root>/using-harness/scripts/harness_closeout_check.py --file <closeout.md>
```

These scripts are structural guardrails. Their output is Evidence input; it does not replace judgment about whether the selected Evidence level is sufficient.

Use `using-harness/assets/templates/CLOSEOUT_COMPACT.md` when you need a compact visible closeout block without expanding the full contract.

## Evidence Levels

- `quick`: tiny or routine low-risk work. Minimum proof can be final response, commit message, manual inspection note, or the smallest relevant command.
- `standard`: non-trivial feature, bugfix, refactor, or user-visible behavior. Minimum proof is tests, build or lint when available, key workflow check, and concise diff or behavior summary.
- `exhaustive`: high-risk release, architecture, data model, security, migration, major UX, RPA/browser flow, or external contract. Minimum proof is standard proof plus E2E, browser, screenshot, trace, reviewer record, rollback note, or dedicated Evidence when relevant.

## Bugfix Closeout

For every non-tiny bugfix, record attribution before completion language:

- `existing Feature <id>`: update that Feature's `## Patch History` when the bug changes completed, accepted, or previously delivered behavior.
- `none found after retrieval`: record the negative retrieval result in Evidence or final closeout.
- `not triggered`: use only for tiny local fixes where project memory cannot change the outcome, and state why.
- `ambiguous`: keep completion blocked or conditional unless the claim is explicitly limited to investigation.

Non-tiny bugfix completion requires a Bugfix attribution status, and existing completed Feature owners have an updated Patch History row when applicable.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Claiming work is done without Evidence status. | Record Evidence location and level. |
| Treating scripts as reading material. | Execute scripts; read source only when debugging or editing them. |
| Omitting a category because no artifact was needed. | Mark it `not triggered` with a reason. |
| Fixing a completed Feature bug without updating Patch History. | Attribute first, then update the owning Feature. |
| Writing a Lesson that only says to be careful. | Turn caution into a test, gate, CI check, permission rule, or skill. |
