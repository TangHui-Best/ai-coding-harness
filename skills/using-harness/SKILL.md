---
name: using-harness
description: MUST use as the Harness entrypoint before non-trivial engineering work, behavior changes, reviews, commits, PRs, handoffs, or any completion claim; also use when the user mentions Harness, gates, Evidence, ADRs, Lessons, Feature memory, patch churn, 知识沉淀, 收尾, 完成声明, 提交信息, or PR 描述.
---

# Using Harness

## Purpose

Use this skill as the lightweight router for Harness. Keep it in memory only long enough to decide which specific Harness skill, reference, or script is needed.

This skill does not create Feature, ADR, Lesson, Evidence, Backlog, or handoff artifacts. It routes to the smallest next action.

## Activation Contract

After this skill is loaded:

1. Resolve whether Harness is triggered before implementation, commit writing, PR writing, handoff, or completion language.
2. For non-trivial work, run `harness-start-gate` before implementation.
3. For completion/readiness claims, route to `harness-knowledge-capture`.
4. For commit, PR, release, handoff, progress, or rejected-path narrative, route to `harness-change-narrative`.
5. If no Harness action is needed, say `Harness: not triggered` with a short reason and continue.

## Harness Presence Check

Trigger Harness when any of these apply:

- The user mentions Harness, gates, Start Gate, Evidence, ADR, Lesson, Feature, Backlog, handoff, recovery, project memory, patch churn, or process drift.
- The task is non-trivial: multi-file change, behavior change, refactor, cross-module bugfix, review, merge, release, handoff, or a decision future agents may question.
- The repository has Harness memory or tooling such as `docs/features`, `docs/decisions`, `docs/lessons`, `docs/evidence`, `docs/BACKLOG.md`, or vendored Harness scripts/templates.
- The repository has Markdown with Harness `doc_kind` frontmatter, even if it is under legacy paths such as `docs/superpowers`.
- The user reports a bug, regression, validation failure, or broken accepted behavior that may belong to an existing Feature or prior fix chain.

Tiny local edits may skip retrieval and formal artifacts when project memory cannot change the outcome.

## Routing Order

Prefer the most specific skill that can answer the current transition:

1. `harness-start-gate` before non-trivial implementation.
2. `harness-knowledge-retrieval` when prior Feature, ADR, Lesson, spec, plan, Evidence, or bug attribution may change the fix.
3. `harness-doc-lifecycle` for stale, archived, superseded, deprecated, invalidated, or replaced documents.
4. `harness-incident-learning` after a fixed or stabilized bug, incident, recurring failure, or patch chain needs prevention analysis.
5. `harness-delegation-gate` before work that may need subagents or independent review.
6. `harness-vision-gate` when intent, scope, product direction, or acceptance may drift.
7. `harness-readiness-dashboard` for review, release, handoff, or readiness rollups.
8. `harness-change-narrative` for commit messages, PR descriptions, release notes, handoff notes, progress summaries, root cause, rejected paths, and history-aware change explanations.
9. `harness-knowledge-capture` for Evidence, closeout, durable memory, completion verdict, and completion-claim permission.
10. `harness-project-rules` before promoting a decision, Lesson, or repeated constraint into `AGENTS.md` or another project-level rule file.

If the user describes a long-running or unattended task, route to Delegation Gate early so any needed authorization is resolved before it blocks progress.

For non-trivial or high-risk implementation work, Start Gate must produce an explicit Delegation Gate decision before implementation may begin.

For a non-tiny bug, regression, validation failure, or broken accepted behavior, retrieval should establish Feature attribution before code search or edits.

Harness knowledge artifacts must use canonical directories under the selected docs root:

- Feature: `docs/features/Fxxx-slug.md`
- ADR: `docs/decisions/ADR-xxx-slug.md`
- Lesson: `docs/lessons/LL-xxx-slug.md`
- Evidence: `docs/evidence/EV-xxx-slug.md`

Legacy Superpowers documents under `docs/superpowers/**` may remain as linked specs or plans, but do not create Harness Feature, ADR, Lesson, or Evidence artifacts there.

## Closeout Convergence Protocol

This entrypoint routes transitions; it must not become a recursive closeout loop.

- Do not re-enter `using-harness` for the same task transition after it has already routed to a more specific Harness skill.
- `harness-knowledge-capture` owns the final completion verdict. When it returns `pass`, or an explicitly permitted `conditional` verdict for the requested stage, the closeout is terminal.
- Reuse fresh verification, knowledge-check, readiness, and narrative evidence already gathered in this turn instead of restarting equivalent Harness gates.
- Do not route a normal final response to `harness-change-narrative`. Use change narrative for commit messages, PR descriptions, handoff notes, release notes, progress summaries, rejected-path explanations, and history-aware engineering narratives.
- If a specific Harness skill reports blocked or conditional status, preserve that status directly instead of re-routing through this entrypoint to look for a different answer.

## Reference Map

Use references only when their trigger applies.

- `references/routing.md`: read when routing is ambiguous, multiple Harness skills appear to apply, or trigger wording needs detail.
- `references/task-routing-fixtures.md`: read when a common workflow route is unclear or a regression test needs expected Harness behavior.
- `assets/templates/`: copy templates when creating Feature, ADR, Lesson, Evidence, or AGENTS artifacts.
- `assets/templates/CLOSEOUT_COMPACT.md`: use when a concise visible closeout block is needed.

## Script Use

Execute bundled scripts; do not read script source unless debugging or editing that script.

- `scripts/knowledge_check.py`: execute to validate Harness Markdown artifacts.
- `scripts/harness_closeout_check.py`: execute to validate a closeout block.
- `scripts/skill_metadata_check.py`: execute to validate skill metadata and bundled resources.

For this repository, prefer `scripts/install.ps1 codex` or `scripts/install.sh codex` to sync Harness skills into the local Codex skills directory instead of hand-copying individual files.

Run `knowledge_check.py` in `--strict` mode for review, closeout, or CI. The validator checks every Markdown file with `doc_kind` frontmatter and rejects Harness artifacts outside their canonical directory.

## Verification Use

Run verification commands before reading verification source.

Do not read test files, validator scripts, or workflow files merely to verify behavior. Read them only when debugging a failure, editing them, reviewing them, or explaining their behavior.

## Non-Goals

- Do not load every Harness skill preemptively.
- Do not read bundled scripts just to learn how to run them.
- Do not create documents for every small change.
- Do not edit `AGENTS.md` just because Harness memory exists; route through `harness-project-rules`.
