---
name: using-agentmentor
description: MUST use as the AgentMentor entrypoint before non-trivial engineering work, behavior changes, reviews, commits, PRs, handoffs, or any completion claim; also use when the user mentions AgentMentor, harness, gates, Evidence, ADRs, Lessons, Feature memory, patch churn, 知识沉淀, 收尾, 完成声明, 提交信息, or PR 描述.
---

# Using AgentMentor

## Purpose

Use this skill as the lightweight router for AgentMentor. Keep it in memory only long enough to decide which specific AgentMentor skill, reference, or script is needed.

This skill does not create Feature, ADR, Lesson, Evidence, Backlog, or handoff artifacts. It routes to the smallest next action.

## Naming Boundary

The formal system name is `AgentMentor`. Use the full name when introducing the system, writing durable project memory, or distinguishing it from a project's own test harness, runtime harness, evaluation harness, or business feature named "harness".

Do not use `Harness` as the skill-suite short name. Treat lowercase `harness` as a generic engineering word unless the current context explicitly defines it as AgentMentor history.

The installed skill slugs are `using-agentmentor` plus short semantic workflow slugs such as `start-gate`, `readiness-dashboard`, and `knowledge-capture`. Pre-rename public skill slugs were removed by the breaking rename. Do not create `harness-*`, `ai-coding-harness-*`, or suite-prefixed workflow skills unless a future ADR explicitly accepts another migration path.

When the user or repository mentions "harness" ambiguously, distinguish project-internal harness code from AgentMentor gates before acting.

## Activation Contract

After this skill is loaded:

1. Resolve whether AgentMentor is triggered before implementation, commit writing, PR writing, handoff, or completion language.
2. For non-trivial work, run `start-gate` before implementation.
3. For completion/readiness claims, route to `knowledge-capture`.
4. For commit, PR, release, handoff, progress, or rejected-path narrative, route to `change-narrative`.
5. If no AgentMentor action is needed, say `AgentMentor: not triggered` with a short reason and continue.

## Entry And Exit Gates

For non-trivial work, AgentMentor is a two-gate protocol:

- Entry Gate: run `start-gate` before implementation and satisfy any required retrieval, Vision Anchor, Feature, spec, plan, ADR, or delegation decision before coding.
- Exit Gate: run `knowledge-capture` before saying the work is complete, fixed, verified, ready for PR, ready for review, ready for handoff, safely closed, or mergeable.
- A spec, plan, ADR, Feature page, or Evidence document created during the work is an input to Exit Gate, not a substitute for it.
- If Exit Gate has not produced Evidence level, check status, closeout verdict, and completion-claim permission, describe the state as `implementation done, AgentMentor closeout pending`.

## Core Rule

If future sessions, agents, reviewers, or teammates may need to recover what happened, why it happened, what was verified, or what should not be repeated, check the AgentMentor flow before closing the task.

AgentMentor is not a documentation tax. The required behavior is checking whether shared project memory is needed; the correct result may be `no formal artifact needed`.

## AgentMentor Presence Check

Trigger AgentMentor when any of these apply:

- The user mentions AgentMentor, harness, gates, Start Gate, Evidence, ADR, Lesson, Feature, Backlog, handoff, recovery, project memory, patch churn, or process drift.
- The task is non-trivial: multi-file change, behavior change, refactor, cross-module bugfix, review, merge, release, handoff, or a decision future agents may question.
- The repository has AgentMentor memory or tooling such as `docs/features`, `docs/decisions`, `docs/lessons`, `docs/evidence`, `docs/BACKLOG.md`, or vendored AgentMentor scripts/templates.
- The repository has Markdown with AgentMentor `doc_kind` frontmatter, even if it is under legacy paths such as `docs/superpowers`.
- The user reports a bug, regression, validation failure, or broken accepted behavior that may belong to an existing Feature or prior fix chain.

Tiny local edits may skip retrieval and formal artifacts when project memory cannot change the outcome.

## Routing Order

Prefer the most specific skill that can answer the current transition:

1. `start-gate` before non-trivial implementation.
2. `knowledge-retrieval` when prior Feature, ADR, Lesson, spec, plan, Evidence, or bug attribution may change the fix.
3. `doc-lifecycle` for stale, archived, superseded, deprecated, invalidated, or replaced documents.
4. `incident-learning` after a fixed or stabilized bug, incident, recurring failure, or patch chain needs prevention analysis.
5. `delegation-gate` before work that may need subagents or independent review.
6. `vision-gate` when intent, scope, product direction, or acceptance may drift.
7. `readiness-dashboard` for review, release, handoff, progress assessment, maturity assessment, distance to target, roadmap gap, blocker, or readiness rollups.
8. `change-narrative` for commit messages, PR descriptions, release notes, handoff notes, progress summaries, root cause, rejected paths, and history-aware change explanations.
9. `knowledge-capture` for Evidence, closeout, durable memory, completion verdict, and completion-claim permission.
10. `project-rules` before promoting a decision, Lesson, or repeated constraint into `AGENTS.md` or another project-level rule file.

If the user describes a long-running or unattended task, route to Delegation Gate early so the main agent explicitly chooses `single_agent`, `delegate`, or `blocked` before progress depends on that choice.

For non-trivial or high-risk implementation work, Start Gate must produce an explicit Delegation Gate decision before implementation may begin.

For a non-tiny bug, regression, validation failure, or broken accepted behavior, retrieval should establish Feature attribution before code search or edits.

AgentMentor knowledge artifacts must use canonical directories under the selected docs root:

- Feature: `docs/features/Fxxx-slug.md`
- ADR: `docs/decisions/ADR-xxx-slug.md`
- Lesson: `docs/lessons/LL-xxx-slug.md`
- Evidence: `docs/evidence/EV-xxx-slug.md`

Legacy Superpowers documents under `docs/superpowers/**` may remain as linked specs or plans, but do not create AgentMentor Feature, ADR, Lesson, or Evidence artifacts there.

Superpowers specs and plans are linked material, not AgentMentor artifacts. When Superpowers writes `docs/superpowers/specs/...` or `docs/superpowers/plans/...`, create or update the owning AgentMentor Feature separately under `docs/features/Fxxx-slug.md` and link the spec or plan from that Feature when the work needs durable recovery.

## Closeout Convergence Protocol

This entrypoint routes transitions; it must not become a recursive closeout loop.

- Do not re-enter `using-agentmentor` for the same task transition after it has already routed to a more specific AgentMentor skill.
- `knowledge-capture` owns the final completion verdict. When it returns `pass`, or an explicitly permitted `conditional` verdict for the requested stage, the closeout is terminal.
- Reuse fresh verification, knowledge-check, readiness, and narrative evidence already gathered in this turn instead of restarting equivalent AgentMentor gates.
- Do not route a normal final response to `change-narrative`. Use change narrative for commit messages, PR descriptions, handoff notes, release notes, progress summaries, rejected-path explanations, and history-aware engineering narratives.
- If a specific AgentMentor skill reports blocked or conditional status, preserve that status directly instead of re-routing through this entrypoint to look for a different answer.

## Reference Map

Use references only when their trigger applies.

- `references/routing.md`: read when routing is ambiguous, multiple AgentMentor skills appear to apply, or trigger wording needs detail.
- `references/task-routing-fixtures.md`: read when a common workflow route is unclear or a regression test needs expected AgentMentor behavior.
- `assets/templates/`: copy templates when creating Feature, ADR, Lesson, Evidence, or AGENTS artifacts.
- `assets/templates/CLOSEOUT_COMPACT.md`: use when a concise visible closeout block is needed.

## Script Use

Execute bundled scripts; do not read script source unless debugging or editing that script.

- `scripts/knowledge_check.py`: execute to validate AgentMentor Markdown artifacts.
- `scripts/closeout_check.py`: execute to validate a closeout block.
- `scripts/skill_metadata_check.py`: execute to validate skill metadata and bundled resources.
- `scripts/hook_diagnostics.py`: execute after optional hook installation or suspected hook drift to check local runner smoke and Codex compaction evidence.

For this repository, prefer `scripts/install.ps1 codex` or `scripts/install.sh codex` to sync AgentMentor skills into the local Codex skills directory instead of hand-copying individual files.

Run `knowledge_check.py` in `--strict` mode for review, closeout, or CI. The validator checks every Markdown file with `doc_kind` frontmatter and rejects AgentMentor artifacts outside their canonical directory.

## Optional Hook Runtime

Skills-only install remains valid. Hooks are an optional runtime enhancement, not a prerequisite for using AgentMentor.

Hook resources live under this Skill so the Skill owns scripts and hook entrypoints:

- `hooks/agentmentor_hook.py`: normalized hook runner. Default examples use `stop`, `session-start`, and `pre-compact`; `post-tool-use` remains available for explicit experiments.
- `hooks/codex-hooks.example.json`: Codex hook configuration example.
- `hooks/claude-settings.example.json`: Claude Code hook configuration example.
- `hooks/opencode-plugin.example.ts`: OpenCode plugin example.

Default examples install only `stop`, `session-start`, and `pre-compact`. Hook installation or runtime failure must fail open unless the hook clearly proves an AgentMentor rule failed at a completion boundary. A broken hook config must not roll back Skills, block Skill loading, or replace normal Skill-triggered gates. The default hook slice only automates:

- Checking completion claims with `closeout_check.py` before the agent stops. This is the default hard boundary for incomplete closeout blocks.
- Writing a lightweight `.agentmentor/session-recovery/by-session/<session_id>.md` snapshot before compaction, then exposing it only when the same session resumes from `compact` and the platform supports contextual hook output. `.agentmentor/session-recovery/latest.md` is updated for manual inspection only and must not be injected into unrelated new sessions.

Do not run `knowledge_check.py` from PostToolUse by default. Tool-call granularity is too fine for multi-edit AgentMentor artifacts and can slow the agent down. Run `knowledge_check.py --strict` at Stop/readiness/closeout/CI boundaries instead. The `post-tool-use` runner mode is experimental and should only be wired manually when immediate feedback is explicitly worth the cost.

Do not move Start Gate, Vision Gate, ADR, Lesson, or Feature ownership judgment into deterministic hook code.

After installing or changing Codex hooks, verify actual runtime evidence instead of relying only on UI visibility or cached files:

```bash
python <skills-root>/using-agentmentor/scripts/hook_diagnostics.py codex --project-root <repo>
```

If the diagnostic reports Codex `compacted/context_compacted` events without `.agentmentor/session-recovery/` artifacts, treat `PreCompact` recovery as not proven on that Codex install and keep using normal AgentMentor handoff or canonical project docs.

Codex plugin-bundled hooks should keep both root-level `hooks.json` and `hooks/hooks.json` available with identical content. The user config must enable both `[features].hooks = true` and `[features].plugin_hooks = true`; UI visibility and trusted hashes do not prove runtime dispatch. Route commands through `hooks/run-agentmentor-hook.cmd` instead of calling `python ./skills/...` directly, and use `commandWindows` with `%PLUGIN_ROOT%` on Windows. Runtime proof comes from `.agentmentor/hook-events/events.jsonl` or the expected recovery/check output.

## Verification Use

Run verification commands before reading verification source.

Do not read test files, validator scripts, or workflow files merely to verify behavior. Read them only when debugging a failure, editing them, reviewing them, or explaining their behavior.

## Non-Goals

- Do not load every AgentMentor skill preemptively.
- Do not read bundled scripts just to learn how to run them.
- Do not create documents for every small change.
- Do not edit `AGENTS.md` just because AgentMentor memory exists; route through `project-rules`.

## Red Flags

| Thought | Reality |
| --- | --- |
| "This is done; I can just say completed." | Completion needs Evidence status and a closeout verdict. |
| "I wrote a spec, so AgentMentor is done." | A spec anchors intent; Exit Gate still needs Evidence, check status, and completion permission. |
| "The next agent can infer intent from the diff." | Diffs show what changed, not why alternatives were rejected. |
| "No formal artifact is needed, so no AgentMentor skill is needed." | AgentMentor may conclude no artifact is needed; the check is still the gate. |
| "This Superpowers plan is the Feature." | Plans can be linked from a Feature; official AgentMentor Feature memory lives in `docs/features/Fxxx-slug.md`. |
