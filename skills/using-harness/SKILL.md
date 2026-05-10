---
name: using-harness
description: Use when working in an AI-assisted engineering workflow that may need start gates, project memory, retrieval, vision checks, evidence, incident learning, change narrative, document lifecycle, handoff, ADRs, Lessons, Features, Backlog, AGENTS.md project rules, archive, 知识沉淀, 经验沉淀, 交接, 复盘, 项目军规, or durable project memory.
---

# Using Harness

## Purpose

Use this as the entrypoint for an AI coding harness. It routes engineering work toward the right harness skill so knowledge can survive across sessions, agents, reviewers, and teammates.

This skill does not create artifacts directly. It decides which harness skill should run, or whether no formal harness action is needed.

## Core Rule

If future sessions, agents, reviewers, teammates, or future you may need to understand what happened, why it happened, what was verified, or what should not be repeated, check the harness flow before closing the task.

Harness is not a documentation tax. The required behavior is checking whether shared project memory is needed; the correct result may be "no formal artifact needed."

## Routing

Use `harness-start-gate` before non-trivial implementation starts:

- Development kickoff, task intake, or pre-coding readiness checks.
- Deciding whether implementation may start now.
- Deciding whether clarification, retrieval, Vision Gate, Feature, spec, plan, ADR, Backlog, or handoff anchor is required first.
- Preventing direct coding when task boundaries, acceptance criteria, or durable pre-work memory are missing.
- Chinese trigger phrases such as `开发前检查`, `开工门禁`, `需求边界`, `前置沉淀`, or `防止直接开工`.

Use `harness-knowledge-retrieval` when the task needs existing project context before acting:

- Starting or resuming non-trivial work, recovering context, finding prior decisions, checking ADRs, Lessons, Features, specs, plans, or Evidence.
- Search results mention stale, superseded, deprecated, invalidated, archived, or old documents.
- Chinese trigger phrases such as `开始任务`, `恢复上下文`, `查历史决策`, `查 ADR`, `查 Lesson`, `查 Feature`, `查知识库`, `避免重复踩坑`, or `找以前为什么这么做`.

Use `harness-doc-lifecycle` when document validity, archive state, supersession, or replacement links are in question:

- Document archive, cleanup, invalidates, updates, superseded_by, active directory growth, old ADR, old plan, old spec, old research, resolved discussion, landed research, completed plan, or completed Feature.
- Chinese trigger phrases such as `文档归档`, `过期文档`, `旧文档`, `被替代`, `废弃`, `清理文档`, `归档目录`, `生命周期`, `活跃目录膨胀`, `计划执行完`, `讨论收敛`, `研究落地`, or `Feature 完成`.

Use `harness-incident-learning` after a bug, incident, outage, regression, or recurring failure is fixed or stabilized:

- Root cause, trigger, recurrence risk, prevention, tests, Gate, Skill, Lesson, ADR, CI, or immunity mechanism needs to be considered.
- Chinese trigger phrases such as `事故复盘`, `bug 修完`, `缺陷修复后`, `故障恢复后`, `回归问题`, `重复失败`, `避免复发`, `根因`, `触发器`, `改规则`, `免疫机制`, or `以后别再出现`.

Use `harness-vision-gate` when original intent or user-goal alignment may drift before or after implementation:

- Before non-trivial implementation, coding, refactoring, feature work, UI/UX work, or behavior changes.
- Before review, merge, done, acceptance, release, or handoff.
- Product direction, UX, visual quality, user pain point, scope alignment, or deliverable-goal fit is in question.
- Chinese trigger phrases such as `Review 前`, `Merge 前`, `Done 前`, `验收前`, `愿景守护`, `原始需求`, `用户真实目标`, `AC 偏差`, `方向跑偏`, `体验是否跑偏`, or `是否解决痛点`.

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
2. `harness-knowledge-retrieval` to read existing context.
3. `harness-doc-lifecycle` when document validity, archive state, supersession, or replacement links are in question.
4. `harness-incident-learning` when a bug, incident, outage, regression, or recurring failure is fixed or stabilized.
5. `harness-vision-gate` before implementation when intent, scope, or path alignment may drift; run it again before review, merge, done, acceptance, release, or handoff when deliverable-goal alignment may have drifted.
6. `harness-change-narrative` when a commit, PR, handoff, progress update, release note, or rejected-path explanation needs the compact story of a specific change.
7. `harness-knowledge-capture` last to decide durable artifacts, links, validation, Evidence, and final knowledge status.
8. `harness-project-rules` when the remaining question is whether a source-backed behavior constraint belongs in `AGENTS.md` or another project-level agent rule file.

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

## Non-Goals

- Do not require a project-level `AGENTS.md` change to use Harness.
- Do not edit `AGENTS.md` just because Harness memory exists. Route through `harness-project-rules` when a candidate rule may deserve project-level agent visibility.
- Do not create Feature, ADR, Lesson, Evidence, or Backlog artifacts from this skill.
- Do not create documents for every small change.
- Use the smallest durable carrier that prevents repeated rediscovery, unverifiable completion, or repeated mistakes.
