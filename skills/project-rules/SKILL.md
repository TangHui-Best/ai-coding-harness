---
name: project-rules
description: MUST use when deciding whether a decision, lesson, incident learning, evidence pattern, recurring project constraint, patch-churn guardrail, zero-base review rule, or proposed agent instruction should be promoted into AGENTS.md or another project-level agent rule file. Guides rule promotion, rejection, wording, source linking, preventing AGENTS.md bloat, 项目军规, 写进 AGENTS.md, Agent 规则, 反复补丁, 归零审视, 沉淀到 AGENT.md, or 沉淀到 AGENTS.md.
---

# Project Rules

## Overview

Use this skill as the upgrade gate from AgentMentor memory to project-level agent rules.

The reusable project-rule starter template is bundled with the `using-agentmentor` entrypoint skill at `using-agentmentor/assets/templates/AGENTS.md`. Copy that template only when a project needs an `AGENTS.md` file or an existing file needs a small, source-backed AgentMentor section, and only after the user explicitly asks for or approves the project-rule edit.

Boundary:

```text
ADR, Lesson, Evidence, Feature, and Backlog explain what happened.
AGENTS.md constrains how future agents must act.
```

This skill does not replace `knowledge-capture`. Use it after a decision, lesson, evidence pattern, or recurring constraint may need to become a durable rule that every future agent should see before working in the project.

## Core Principle

Promote only rules that change future agent behavior and are worth default attention.

Do not put history, rationale, one-off context, or vague caution into `AGENTS.md`. Keep those in ADRs, Lessons, Evidence, Features, or handoff notes, then link them from the project rule when useful.

`AGENTS.md` is a high-attention behavior-control surface, not a knowledge archive. It should stay short, hard, source-backed, and human-authorized.

## Human Authorization Boundary

Agents may identify candidate rules, run this promotion gate, draft rule text, and recommend whether to promote or reject a rule.

Agents MUST NOT edit `AGENTS.md` or repository-wide agent instructions unless one of these is true:

- The user explicitly asks to update project rules or `AGENTS.md`.
- The user approves a proposed rule for promotion.
- The repository already has a documented process that authorizes this promotion.

If authorization is missing, stop after the recommendation and present the candidate rule for user approval.

## Workflow

1. Identify the candidate rule and its source: ADR, Lesson, incident, evidence pattern, review finding, user instruction, or repeated project friction.
2. Check whether the source artifact already exists. If not, use `knowledge-capture` first when rationale, recurrence, or evidence would otherwise be lost.
3. Apply the Promotion Gate, including the human authorization boundary.
4. Choose the destination:
   - `AGENTS.md` for repository-wide agent behavior rules.
   - A narrower agent rule file only when the repository already uses scoped agent instructions.
   - Existing AgentMentor artifact only when the candidate is not a behavior constraint.
5. Rewrite the rule as a concise operational instruction.
6. Link the source artifact when the rule comes from a decision, lesson, incident, or evidence record.
7. Check the AGENTS length budget before editing.
8. Reject or defer candidates that fail the gate, and say where they should live instead.

## Promotion Gate

Promote a rule into `AGENTS.md` only when all are true:

- Cross-task: The rule applies to future work beyond the current task.
- Project-level: The rule affects multiple modules, workflows, agents, or review gates.
- Behavioral: The rule tells agents what to do, avoid, prefer, verify, or stop and ask.
- Hard constraint: The rule can be written as a MUST or MUST NOT behavior constraint.
- Verifiable: A reviewer can tell whether the rule was followed.
- Source-backed: The rule is traceable to a user instruction, ADR, Lesson, Evidence, incident, or repeated observed failure.
- Worth the attention cost: Seeing the rule on every future task prevents more cost than its context footprint creates.
- Human-authorized: The user explicitly asked for or approved the AGENTS/project-rule edit, or the repository has a documented promotion process.

If any condition fails, do not promote it. Keep it in the smallest suitable AgentMentor artifact.

## Reject Patterns

Do not promote:

- One-off task context.
- Temporary workaround details that should expire.
- Long rationale or historical narrative.
- Local implementation details already clear from code.
- Preferences without enforcement value.
- Advice that only says "be careful".
- SHOULD/PREFER preferences unless the user explicitly asks for them as project-level rules and the boundary can be written as MUST/MUST NOT.
- Rules that duplicate existing `AGENTS.md` guidance.
- Rules that encode a controversial decision before an ADR or user confirmation exists.
- Rules that make every task heavier without preventing a real recurring failure.
- Rules without a source reference.
- Rules that exceed the AGENTS length budget without explicit user approval.

## Rule Wording

Good project rules are short, actionable, and scoped.

Use this shape:

```markdown
### Rule: <specific behavior>
- Scope: <when this applies>
- Requirement: <MUST / MUST NOT behavior constraint>
- Source: <user instruction / ADR / Lesson / Evidence / Feature>
- Rationale: <one sentence explaining the risk prevented>
```

Keep rationale to one sentence. Put deeper reasoning in the linked source artifact.

## Length Budget

Keep `AGENTS.md` short by default:

- Target: 100 lines or fewer.
- Soft limit: 200 lines. New rules need clear attention-cost justification.
- Hard limit: 300 lines. Exceeding this requires explicit user approval and a reason the content cannot live in Feature, ADR, Lesson, Evidence, or guide material.

If a proposed edit pushes `AGENTS.md` beyond the budget, propose consolidation, replacement, or rejection before editing.

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
- Requirement: Agents MUST run the project-rules promotion gate and get user approval before editing AGENTS.md.
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

## Relationship To Other AgentMentor Skills

- Use `change-narrative` first when the candidate rule comes from a specific change that needs its story distilled.
- Use `incident-learning` first when the candidate rule comes from a bug, outage, regression, or repeated failure.
- Use `knowledge-capture` first when the source should become an ADR, Lesson, Evidence, Feature, Backlog, or handoff artifact.
- Use this skill after those flows when the remaining question is whether a behavior constraint should be promoted into `AGENTS.md`.

## Final Check

Before editing `AGENTS.md`, answer:

```text
Candidate rule:
Source:
Promotion gate: pass / fail
Human authorization: present / missing
Length budget: pass / needs consolidation / needs explicit approval
Destination:
Rule text:
Why this belongs in project rules instead of ADR/Lesson/Evidence only:
```

If the gate fails, report the rejection and the better destination. Do not edit `AGENTS.md`.
