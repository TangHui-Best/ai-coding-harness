---
name: harness-delegation-gate
description: MUST use when non-trivial or high-risk engineering work may benefit from implementation subagents, parallel exploration, independent code review, or independent Vision Gate review; use before coding to decide whether to ask the user for subagent authorization, and before review, release, handoff, or completion to decide whether independent review is self-review, recommended, required, blocked, or conditional.
---

# Harness Delegation Gate

## Purpose

Decide whether the agent should ask the user to authorize implementation subagents or independent reviewers.

This gate does not spawn subagents, write code, or perform review. It turns delegation into an explicit decision so medium and large tasks do not silently fall back to single-agent work.

## Modes

Use exactly one mode:

| Mode | Use when |
| --- | --- |
| `implementation` | Before coding, planning execution, or splitting work. |
| `review` | Before review, merge, release, handoff, acceptance, or completion. |

## Implementation Decision

For `non-trivial` or `high-risk` work, ask whether implementation subagents should be proposed before coding.

Ask the user whether to authorize implementation subagents when any trigger is present:

- The task has two or more separable workstreams.
- The change spans multiple modules, ownership boundaries, or delivery steps.
- Exploration, implementation, tests, or verification can proceed independently.
- The work is likely to be long-running enough that parallelism reduces latency or tunnel vision.
- A separate implementation path would reduce anchoring on the main agent's assumptions.
- The user explicitly mentions subagents, delegation, parallel agents, or multi-agent development.

Do not ask when the work is tiny, tightly coupled, mainly conversational, or when coordination overhead would exceed the value of delegation.

If the platform requires explicit user permission before spawning subagents, ask a concise permission question and wait. Do not treat this gate as permission to spawn.

## Review Decision

Before review, merge, release, handoff, acceptance, or completion, decide the lightest honest independence level:

| Task/risk | Decision |
| --- | --- |
| Tiny or routine, low-risk | `self-review allowed` |
| Non-trivial feature, refactor, user-facing change, unclear scope, or meaningful drift risk | `ask user for independent review` |
| High-risk architecture, data model, security, migration, release, major UX, or external contract | `independent review required` |

If independent review is required but unavailable, mark the next stage `blocked` or `conditional` and name the residual risk. Do not silently self-approve high-risk work.

## Outputs

Return exactly one decision:

| Decision | Meaning |
| --- | --- |
| `not needed` | Single-agent work or self-review is sufficient; state why. |
| `ask user` | User authorization is needed before using implementation subagents or an independent reviewer. |
| `authorized` | The user has already authorized the requested delegation path. |
| `declined` | The user declined; continue with the named single-agent or self-review risk. |
| `required` | Independent review is mandatory for the current risk level. |
| `blocked` | Required authorization, reviewer, context, or platform support is unavailable. |
| `conditional` | Work may proceed only with an explicit residual risk. |

## Report Format

```text
Delegation Gate: not needed | ask user | authorized | declined | required | blocked | conditional
Mode:
- implementation | review
Task class:
- tiny | routine | non-trivial | high-risk
Triggers:
- ...
Decision:
- ...
User question, if needed:
- ...
Residual risk:
- ...
Allowed next action:
- ...
```

## Boundaries

- Do not default to subagents.
- Do not skip the decision for non-trivial or high-risk work.
- Do not ask for subagents when the work cannot be usefully split.
- Do not let `independent recommended` disappear into a status report; either ask the user, state why self-review is enough, or mark the stage conditional.
- Keep prompts to subagents minimal when the user authorizes them: pass the original goal, owned scope, relevant files, and expected output, not the main agent's conclusions.
