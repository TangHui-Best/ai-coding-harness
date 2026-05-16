---
name: harness-project-rules
description: MUST use when deciding whether a decision, lesson, incident learning, evidence pattern, recurring project constraint, patch-churn guardrail, zero-base review rule, or proposed agent instruction should be promoted into AGENTS.md or another project-level agent rule file. Guides rule promotion, rejection, wording, source linking, preventing AGENTS.md bloat, 项目军规, 写进 AGENTS.md, Agent 规则, 反复补丁, 归零审视, 沉淀到 AGENT.md, or 沉淀到 AGENTS.md.
---

# Harness Project Rules

## Overview

Use this skill as the upgrade gate from Harness memory to project-level agent rules.

Boundary:

```text
ADR, Lesson, Evidence, Feature, and Backlog explain what happened.
AGENTS.md constrains how future agents must act.
```

This skill does not replace `harness-knowledge-capture`. Use it after a decision, lesson, evidence pattern, or recurring constraint may need to become a durable rule that every future agent should see before working in the project.

## Core Principle

Promote only rules that change future agent behavior.

Do not put history, rationale, one-off context, or vague caution into `AGENTS.md`. Keep those in ADRs, Lessons, Evidence, Features, or handoff notes, then link them from the project rule when useful.

## Workflow

1. Identify the candidate rule and its source: ADR, Lesson, incident, evidence pattern, review finding, user instruction, or repeated project friction.
2. Check whether the source artifact already exists. If not, use `harness-knowledge-capture` first when rationale, recurrence, or evidence would otherwise be lost.
3. Apply the Promotion Gate.
4. Choose the destination:
   - `AGENTS.md` for repository-wide agent behavior rules.
   - A narrower agent rule file only when the repository already uses scoped agent instructions.
   - Existing Harness artifact only when the candidate is not a behavior constraint.
5. Rewrite the rule as a concise operational instruction.
6. Link the source artifact when the rule comes from a decision, lesson, incident, or evidence record.
7. Reject or defer candidates that fail the gate, and say where they should live instead.

## Promotion Gate

Promote a rule into `AGENTS.md` only when all are true:

- Cross-task: The rule applies to future work beyond the current task.
- Project-level: The rule affects multiple modules, workflows, agents, or review gates.
- Behavioral: The rule tells agents what to do, avoid, prefer, verify, or stop and ask.
- Operational: The rule can be written with MUST, MUST NOT, SHOULD, PREFER, or a clear trigger.
- Verifiable: A reviewer can tell whether the rule was followed.
- Source-backed: The rule is traceable to a user instruction, ADR, Lesson, Evidence, incident, or repeated observed failure.
- Worth the attention cost: Seeing the rule on every future task prevents more cost than its context footprint creates.

If any condition fails, do not promote it. Keep it in the smallest suitable Harness artifact.

## Reject Patterns

Do not promote:

- One-off task context.
- Temporary workaround details that should expire.
- Long rationale or historical narrative.
- Local implementation details already clear from code.
- Preferences without enforcement value.
- Advice that only says "be careful".
- Rules that duplicate existing `AGENTS.md` guidance.
- Rules that encode a controversial decision before an ADR or user confirmation exists.
- Rules that make every task heavier without preventing a real recurring failure.

## Rule Wording

Good project rules are short, actionable, and scoped.

Use this shape:

```markdown
### Rule: <specific behavior>
- Scope: <when this applies>
- Requirement: <MUST / MUST NOT / SHOULD / PREFER instruction>
- Source: <ADR / Lesson / Evidence / user instruction link, if available>
- Rationale: <one sentence explaining the risk prevented>
```

Keep rationale to one sentence. Put deeper reasoning in the linked source artifact.

## Examples

Promote:

```markdown
### Rule: Evidence before completion claims
- Scope: Any non-trivial code or behavior change.
- Requirement: Agents MUST record verification commands and outcomes before claiming completion.
- Source: LL-002 false-completion-regression.md
- Rationale: Prevents unverifiable handoff and repeated false completion.
```

Do not promote:

```markdown
We used parser X this time because it was quick.
```

Use an ADR instead if the parser choice will be questioned later. Leave it in the change narrative if it is only local context.

Promote after a Lesson:

```markdown
### Rule: Stop before AGENTS.md growth
- Scope: Any proposed project-level agent instruction.
- Requirement: Agents MUST run the Harness project-rules promotion gate before editing AGENTS.md.
- Source: LL-004 agents-md-bloat.md
- Rationale: Keeps project rules enforceable instead of becoming a memory dump.
```

Promote after a patch-churn Lesson:

```markdown
### Rule: Re-evaluate patch-heavy Features
- Scope: Any Feature with repeated fix iterations, especially 3+ follow-ups or scenario-specific rule growth.
- Requirement: Agents MUST pause further patching and run a zero-base review before implementing another patch when fixes repeatedly target symptoms instead of reducing the underlying invariant or boundary problem.
- Source: LL-00x patch-churn-zero-base-review.md
- Rationale: Repeated patch churn is evidence that the initial abstraction may be wrong, not merely incomplete.
```

## Relationship To Other Harness Skills

- Use `harness-change-narrative` first when the candidate rule comes from a specific change that needs its story distilled.
- Use `harness-incident-learning` first when the candidate rule comes from a bug, outage, regression, or repeated failure.
- Use `harness-knowledge-capture` first when the source should become an ADR, Lesson, Evidence, Feature, Backlog, or handoff artifact.
- Use this skill after those flows when the remaining question is whether a behavior constraint should be promoted into `AGENTS.md`.

## Final Check

Before editing `AGENTS.md`, answer:

```text
Candidate rule:
Source:
Promotion gate: pass / fail
Destination:
Rule text:
Why this belongs in project rules instead of ADR/Lesson/Evidence only:
```

If the gate fails, report the rejection and the better destination. Do not edit `AGENTS.md`.
