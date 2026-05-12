---
name: harness-change-narrative
description: MUST use before explaining, summarizing, committing, handing off, or publishing a specific engineering change, including commit messages, PR descriptions, merge notes, release notes, progress summaries, root cause, rejected approaches, why not alternatives, verification context, historical intent, workaround decisions, future caution, 提交信息, PR 描述, 交接说明, 变更总结, 当前进展, 复盘, or 为什么这么改.
---

# Harness Change Narrative

## Purpose

Use this skill to explain a specific engineering change clearly enough that a future agent can commit it, review it, continue it, or debug it without rediscovering the reasoning.

Boundary:

```text
This skill writes change narrative.
harness-knowledge-capture owns structured project memory.
```

This skill distills facts, rationale, rejected paths, verification context, and next-step caution. It does not create source-of-truth Harness artifacts.

## Use When

- Preparing a commit message, PR description, merge note, release note, or handoff.
- Summarizing current progress or recent development.
- Explaining which approach was chosen, which approaches were rejected, and why.
- A substantial feature or cross-module change is completed.
- Work is reverted, backed up, forked, temporarily bypassed, or introduced as a compatibility shim.
- A bug fix needs more than a local code diff to understand why it exists.
- A long session is ending and the next session needs a compact recovery point.

## Do Not Use As

- A Feature, ADR, Lesson, Evidence, or Backlog creation workflow.
- A replacement for verification.
- A project memory database.
- A reason to write process artifacts when a commit body or short handoff is enough.
- A way to bypass `harness-knowledge-capture` when structured Harness artifacts are triggered.

## Workflow

1. Identify the change being explained: commit, PR, merge, release, handoff, reverted work, non-trivial bugfix, or history-aware decision.
2. Gather local evidence first: recent commits, changed files, relevant docs, tests run, failures, and user constraints.
3. For non-trivial bug fixes, inspect history around touched files. Identify when behavior likely changed, the earlier intent, and whether the new fix preserves or revises that intent.
4. Separate facts from interpretation. Facts include files, commits, commands, errors, and observed behavior. Interpretation includes root cause, rejected paths, and design intent.
5. Write the smallest narrative that prevents future confusion.
6. Choose the immediate narrative destination:
   - Commit or PR body for change-local context.
   - Handoff note for session-local recovery.
   - Merge or release note for published context.
   - Decision narrative when a formal ADR may be needed but has not been created yet.
   - Agent rule draft when a repeated lesson should constrain future agents.
7. If durable project memory is triggered, hand off to `harness-knowledge-capture`.

## Output Rules

- Lead with what the next agent needs to continue safely.
- Record chosen and rejected approaches when the decision affected architecture, cost, risk, or future debugging.
- Include root cause for bugfixes when known. If unknown, say what evidence is still missing.
- For non-trivial bugfixes, include likely introducing commit, original intent, current mismatch, and fix rationale when available.
- Keep handoffs compact enough to be read at session start.
- Prefer concrete project nouns over generic advice.
- Keep agent-rule drafts operational and specific.
- Link or summarize existing spec, plan, verification, Feature, ADR, Lesson, or Evidence artifacts instead of duplicating them.

## Commit And PR Narrative

For commit messages and PR bodies, include the smallest useful version of:

- What changed.
- Why the change is needed.
- How the implementation works.
- Why not the tempting alternatives.
- Verification performed.

Do not force a long template into tiny commits. For non-trivial changes, missing `why not` is a signal that future agents may rediscover the same rejected path.

## Report Template

```markdown
## Change

What changed?

## Why

What problem, goal, or constraint caused this change?

## Rejected Paths

What alternatives were considered and not chosen?

## Verification

What commands, checks, screenshots, or reviews support the result?

## Future Caution

What should the next agent or reviewer keep in mind?
```

## Quick Checks

- Would this help someone debug when or why a bug was introduced?
- Does this explain why an obvious alternative was not used?
- Would this stop the next agent from repeating a costly mistake?
- Is this explaining a specific change, or trying to own structured project memory?
- Does this overlap with an existing source artifact? If yes, link or summarize it instead of duplicating it.
