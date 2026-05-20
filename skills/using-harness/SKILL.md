---
name: using-harness
description: MUST use as the entrypoint at the start of any non-trivial engineering task, multi-file bugfix, behavior change, refactor, review, commit, PR, handoff, completion claim, or when the user mentions Harness, gates, delegation, subagents, evidence, recovery, decisions, lessons, memory, repeated patches, patch churn, Fxxx.n follow-ups, recurring validation failures, rule/keyword growth, 开发前检查, 开工门禁, 知识沉淀, 经验沉淀, 复盘, 交接, 完成声明, 反复补丁, 规则越补越多, 归零审视, 提交信息, or PR 描述. Routes to Start Gate, Delegation Gate, retrieval, vision gate, readiness, change narrative, knowledge capture, and project rules.
---

# Using Harness

## Purpose

Use this as the entrypoint for an AI coding harness. It routes engineering work toward the right harness skill so knowledge can survive across sessions, agents, reviewers, and teammates.

This skill does not create artifacts directly. It decides which harness skill should run, or whether no formal harness action is needed.

## Bundled Resources

Installing this skill should install the complete Harness resource set, not just process text:

- `scripts/knowledge_check.py`: validates Feature, ADR, Lesson, and Evidence Markdown artifacts.
- `scripts/harness_closeout_check.py`: validates the structural completeness of a final Harness closeout block.
- `scripts/skill_metadata_check.py`: validates Harness skill metadata and bundled-resource presence.
- `assets/templates/`: reusable `FEATURE.md`, `EVIDENCE.md`, `LESSON.md`, `ADR.md`, and `AGENTS.md` templates.

Project repositories may vendor these resources for CI or offline policy reasons, but normal agent use should prefer the bundled resources under this skill before asking each project to copy them.

## Activation Contract

This skill is a high-recall entrypoint. Load it early, then decide whether Harness should continue.

After this skill is loaded:

1. Do not start implementation-oriented code search, editing, commit writing, PR writing, handoff, or completion claims until the Harness Presence Check below is resolved.
2. If the user mentions or reminds you about Harness, pause the current flow and route through this skill before continuing.
3. If the task is non-trivial and Harness is present or likely relevant, run `harness-start-gate` before implementation.
4. If the task is a commit, PR, handoff, progress summary, or rejected-path explanation, route to `harness-change-narrative`.
5. If you are about to claim work is complete, verified, ready, reviewed, safely closed, or ready for handoff, route to `harness-knowledge-capture`.
6. Treat Harness as a two-gate protocol for non-trivial work: Entry Gate before implementation, Exit Gate before any completion/readiness claim.
7. If no Harness action is needed, say that briefly and continue with the normal workflow.

## Entry And Exit Gates

For non-trivial work, Harness is not complete just because one artifact exists.

- Entry Gate: Run `harness-start-gate` before implementation and create or update the smallest durable pre-work anchor when the gate requires it.
- Exit Gate: Run `harness-knowledge-capture` before saying the work is complete, fixed, verified, ready for PR, ready for review, ready for handoff, safely closed, or mergeable.
- A spec, plan, ADR, Feature page, or Evidence document created during the work is an input to Exit Gate, not a substitute for it.
- If Exit Gate has not produced an explicit Evidence level, check status, and completion verdict, describe the state as `implementation done, harness closeout pending` instead of complete.
- If `harness-knowledge-capture` says completion is blocked or conditional, do not upgrade that to ready/completed language in the final response.

## Harness Presence Check

Check for these signals before deciding to exit:

- The user mentions Harness, gates, Start Gate, Evidence, ADR, Lesson, Feature, Backlog, handoff, recovery, knowledge capture, project memory, or process drift.
- The task is non-trivial: multi-file change, behavior change, refactor, cross-module bugfix, review/merge/release/handoff, or a decision future agents may question.
- The repository contains Harness-shaped memory or tooling such as `docs/features`, `docs/decisions`, `docs/lessons`, `docs/evidence`, `docs/BACKLOG.md`, project-vendored templates or scripts, or `ai-coding-harness`.
- The only way to recover intent, evidence, rejected paths, or next steps later would be the chat transcript.
- The user reports a bug, regression, validation failure, or broken accepted behavior that may belong to an existing Feature or prior fix chain.
- The user reports that Harness, documentation capture, Evidence, gate routing, or closeout was skipped, incomplete, or inconsistent.
- The user reports repeated patch iterations, patch churn, `Fxxx.n` follow-ups, recurring validation failures, or rule/keyword branches growing without convergence.

If none of these signals apply, exit with `Harness: not triggered` and continue normally. If any signal applies, use the Routing section below.

## Core Rule

If future sessions, agents, reviewers, teammates, or future you may need to understand what happened, why it happened, what was verified, or what should not be repeated, check the harness flow before closing the task.

Harness is not a documentation tax. The required behavior is checking whether shared project memory is needed; the correct result may be "no formal artifact needed."

## Routing

Use `harness-start-gate` before non-trivial implementation starts:

- Development kickoff, task intake, or pre-coding readiness checks.
- Deciding whether implementation may start now.
- Deciding whether clarification, retrieval, Vision Gate, Feature, spec, plan, ADR, Backlog, or handoff anchor is required first.
- Preventing direct coding when task boundaries, acceptance criteria, or durable pre-work memory are missing.
- For non-trivial or high-risk implementation work, Start Gate must produce an explicit Delegation Gate decision before implementation may begin.
- Chinese trigger phrases such as `开发前检查`, `开工门禁`, `需求边界`, `前置沉淀`, or `防止直接开工`.

Use `harness-delegation-gate` when implementation subagents, parallel work, or independent review may be useful:

- Before coding non-trivial or high-risk work that has separable workstreams, cross-module scope, parallel exploration, or tunnel-vision risk.
- If the user describes a long-running or unattended task, route to Delegation Gate early to ask for any needed preauthorization before work reaches a blocking point.
- Before review, merge, release, handoff, acceptance, or completion when independent code review or independent Vision Gate review is recommended or required.
- When the platform requires explicit user authorization before spawning subagents; the gate should ask instead of silently self-reviewing or single-agenting the work.
- Trigger phrases such as `subagent`, `delegation`, `parallel agents`, `multi-agent`, `independent reviewer`, `independent review`, `vision guardian`, or `独立审视`.

Use `harness-knowledge-retrieval` when the task needs existing project context before acting:

- Starting or resuming non-trivial work, recovering context, finding prior decisions, checking ADRs, Lessons, Features, specs, plans, or Evidence.
- Before non-tiny bugfixes when the bug may be a regression, accepted-Feature follow-up, repeated validation miss, or symptom of a prior fix chain. Retrieval should establish Feature attribution before debugging continues.
- Search results mention stale, superseded, deprecated, invalidated, archived, or old documents.
- Chinese trigger phrases such as `开始任务`, `恢复上下文`, `查历史决策`, `查 ADR`, `查 Lesson`, `查 Feature`, `查知识库`, `避免重复踩坑`, or `找以前为什么这么做`.

Use `harness-doc-lifecycle` when document validity, archive state, supersession, or replacement links are in question:

- Document archive, cleanup, invalidates, updates, superseded_by, active directory growth, old ADR, old plan, old spec, old research, resolved discussion, landed research, completed plan, or completed Feature.
- Chinese trigger phrases such as `文档归档`, `过期文档`, `旧文档`, `被替代`, `废弃`, `清理文档`, `归档目录`, `生命周期`, `活跃目录膨胀`, `计划执行完`, `讨论收敛`, `研究落地`, or `Feature 完成`.

Use `harness-incident-learning` after a bug, incident, outage, regression, or recurring failure is fixed or stabilized:

- Root cause, trigger, recurrence risk, prevention, tests, Gate, Skill, Lesson, ADR, CI, or immunity mechanism needs to be considered.
- A Harness process miss is reported or discovered, such as skipped closeout, missing Evidence status, missing knowledge check after artifact edits, or design-only documentation being treated as completion.
- A Feature shows repeated patch churn: multiple follow-up fixes, `Fxxx.n` slices, recurring manual-validation misses, or growing rule/keyword/filter branches that may indicate the original abstraction is wrong.
- Chinese trigger phrases such as `事故复盘`, `bug 修完`, `缺陷修复后`, `故障恢复后`, `回归问题`, `重复失败`, `避免复发`, `根因`, `触发器`, `改规则`, `免疫机制`, or `以后别再出现`.

Use `harness-vision-gate` when original intent or user-goal alignment may drift before or after implementation:

- Before non-trivial implementation, coding, refactoring, feature work, UI/UX work, or behavior changes.
- Before review, merge, done, acceptance, release, or handoff.
- Product direction, UX, visual quality, user pain point, scope alignment, or deliverable-goal fit is in question.
- Chinese trigger phrases such as `Review 前`, `Merge 前`, `Done 前`, `验收前`, `愿景守护`, `原始需求`, `用户真实目标`, `AC 偏差`, `方向跑偏`, `体验是否跑偏`, or `是否解决痛点`.

Use `harness-readiness-dashboard` when the task needs a concise readiness status before review, merge, release, handoff, PR readiness, or completion:

- Summarizing gate status, source documents, reviewer independence, Evidence level, ADR/Lesson triggers, and blockers.
- Deciding whether work can move to review, release, handoff, or completion without re-running every gate.
- Chinese trigger phrases such as `ready 检查`, `readiness dashboard`, `收尾前状态`, `是否可以交付`, `是否可以 review`, `是否可以 handoff`, or `发布前状态`.

Use `harness-change-narrative` when the task needs a compact explanation of a specific engineering change:

- Commit messages, PR descriptions, merge notes, release notes, progress summaries, handoff notes, change summaries, or development logs.
- Root cause, rejected approaches, verification context, historical intent, workaround/fallback/shim decisions, or future caution.
- Chinese trigger phrases such as `提交信息`, `PR描述`, `交接说明`, `当前进展`, `变更总结`, `复盘`, or `为什么这么改`.

Use `harness-knowledge-capture` when the task may need durable Harness memory or completion gating:

- Before claiming work is complete, verified, reviewed, ready to commit, ready for PR, ready for handoff, or safely closed.
- Feature state changes, spec/plan links, PR readiness, review readiness, incident resolution, recurring failures, ADRs, Lessons, Evidence, Backlog, or handoff state.
- Chinese trigger phrases such as `收尾`, `完成声明`, `准备提交`, `准备PR`, `交接`, `知识沉淀`, `经验沉淀`, `复盘`, or `避免以后踩坑`.

Use `harness-project-rules` when the task asks whether a decision, Lesson, incident learning, Evidence pattern, repeated constraint, or proposed instruction should be promoted into `AGENTS.md` or another project-level agent rule file:

- Promoting durable Harness memory into project-level agent behavior rules.
- Reviewing or editing `AGENTS.md` to add, reject, tighten, or remove project rules.
- Preventing `AGENTS.md` from becoming a history dump, preference list, or vague caution log.
- Chinese trigger phrases such as `项目军规`, `升级到 AGENTS.md`, `写进 AGENTS.md`, `Agent 规则`, `沉淀到 AGENT.md`, or `沉淀到 AGENTS.md`.

## Routing Order

When multiple skills apply, prefer this order. Prefer the most specific gate before narrative; keep `harness-knowledge-capture` as the structured-memory closeout and `harness-project-rules` as the final gate before changing `AGENTS.md`.

1. `harness-start-gate` before non-trivial implementation to decide whether pre-work is required.
2. `harness-knowledge-retrieval` to read existing context, including Feature attribution for non-tiny bugfixes.
3. `harness-doc-lifecycle` when document validity, archive state, supersession, or replacement links are in question.
4. `harness-incident-learning` when a bug, incident, outage, regression, recurring failure, or repeated patch chain is fixed, stabilized, or has grown enough to require zero-base review.
5. `harness-delegation-gate` before implementation when medium or large work may need implementation subagents, and before review/acceptance when independent review may be recommended or required.
6. `harness-vision-gate` before implementation when intent, scope, or path alignment may drift; run it again before review, merge, done, acceptance, release, or handoff when deliverable-goal alignment may have drifted.
7. `harness-readiness-dashboard` before review, release, handoff, or completion when the user needs a status rollup or blocker list.
8. `harness-change-narrative` when a commit, PR, handoff, progress update, release note, or rejected-path explanation needs the compact story of a specific change.
9. `harness-knowledge-capture` last to decide durable artifacts, links, validation, Evidence, and final knowledge status.
10. `harness-project-rules` when the remaining question is whether a source-backed behavior constraint belongs in `AGENTS.md` or another project-level agent rule file.

For simple commit, PR, or handoff writing with no incident, lifecycle, or vision-gate ambiguity, go directly to `harness-change-narrative`, then use `harness-knowledge-capture` only if durable project memory may be needed.

## Red Flags

| Thought | Reality |
| --- | --- |
| "This is done; I can just say completed." | Completion needs Evidence status, even if it stays in the final response. |
| "The next agent can infer intent from the diff." | Diffs show what changed, not why alternatives were rejected. |
| "This workaround is obvious." | Workarounds are exactly where future agents need context. |
| "We can write the ADR or Lesson later." | Later often means after the rationale is gone. |
| "This is just a PR description." | PR descriptions are one of the main change narrative surfaces. |
| "No formal artifact is needed, so no harness skill is needed." | The harness may conclude no artifact is needed; the check is still the gate. |
| "I wrote a spec, so Harness is done." | A spec anchors intent; Exit Gate still needs Evidence, check status, and a completion verdict. |
| "Tests passed, so I can say ready." | Tests are Evidence input; readiness needs the closeout categories to be explicit. |

## Non-Goals

- Do not require a project-level `AGENTS.md` change to use Harness.
- Do not require every project to copy Harness scripts or templates before Harness can work; bundled resources in this skill are the default source.
- Do not edit `AGENTS.md` just because Harness memory exists. Route through `harness-project-rules` when a candidate rule may deserve project-level agent visibility.
- Do not create Feature, ADR, Lesson, Evidence, or Backlog artifacts from this skill.
- Do not create documents for every small change.
- Use the smallest durable carrier that prevents repeated rediscovery, unverifiable completion, or repeated mistakes.
