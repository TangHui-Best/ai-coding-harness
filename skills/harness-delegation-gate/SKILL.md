---
name: harness-delegation-gate
description: "MUST use when non-trivial or high-risk engineering work may benefit from implementation subagents, parallel exploration, independent code review, or independent Vision Gate review; use before coding, review, release, handoff, or completion to choose exactly one main-agent decision: single_agent, delegate, or blocked."
---

# Harness Delegation Gate

## Purpose

Decide whether the main agent should proceed alone, delegate part of the work or review, or stop because the required delegation path is unavailable.

This gate does not spawn subagents, write code, or perform review. It turns delegation into an explicit decision so medium and large tasks do not silently fall back to single-agent work.

## Modes

Use exactly one mode:

| Mode | Use when |
| --- | --- |
| `implementation` | Before coding, planning execution, or splitting work. |
| `review` | Before review, merge, release, handoff, acceptance, or completion. |

## Decision Model

Return exactly one decision:

| Decision | Meaning |
| --- | --- |
| `single_agent` | The main agent proceeds without subagents or independent reviewers; state the concrete reason. |
| `delegate` | The main agent should use an implementation subagent, independent reviewer, or both. |
| `blocked` | The needed delegation path, reviewer, permission, context, or platform support is unavailable. |

This is a main-agent decision, not an automatic dispatch. If the platform or user policy requires permission before spawning a subagent or reviewer, `delegate` means ask or invoke through the approved mechanism before continuing.

## Implementation Decision

For `non-trivial` or `high-risk` work, decide whether implementation subagents should be used before coding.

Default to an explicit delegation decision for non-trivial or high-risk work. Do not default to spawning subagents.

Choose `delegate` when any trigger is strong enough to justify the coordination cost:

- The task has two or more separable workstreams.
- The change spans multiple modules, ownership boundaries, or delivery steps.
- Exploration, implementation, tests, or verification can proceed independently.
- The work is likely to be long-running enough that parallelism reduces latency or tunnel vision.
- The task is long-running or unattended, so discovering a subagent authorization need mid-task would block progress.
- A separate implementation path would reduce anchoring on the main agent's assumptions.
- The user explicitly mentions subagents, delegation, parallel agents, or multi-agent development.

Choose `single_agent` when the work is tiny, tightly coupled, mainly conversational, or when coordination overhead would exceed the value of delegation.

Choose `blocked` when delegation is needed but cannot be performed or authorized in the current environment.

When a user gives preauthorization for a long-running or unattended task, treat that as permission only for the delegation paths they explicitly named. If the preauthorization is broad but does not mention subagents, parallel agents, or independent reviewers, decide at the beginning whether to proceed as `single_agent`, choose `delegate` and request the missing permission, or return `blocked`.

## Review Decision

Before review, merge, release, handoff, acceptance, or completion, decide the lightest honest independence level:

| Task/risk | Decision |
| --- | --- |
| Tiny or routine, low-risk | `single_agent` |
| Non-trivial feature, refactor, user-facing change, unclear scope, or meaningful drift risk | Usually `delegate`; use `single_agent` only with a concrete reason. |
| High-risk architecture, data model, security, migration, release, major UX, or external contract | `delegate`; use `blocked` if the needed reviewer or permission is unavailable. |

Do not silently self-approve high-risk work. If independent review is needed but unavailable, return `blocked` and name the residual risk.

## Report Format

```text
Delegation Gate: single_agent | delegate | blocked
Mode:
- implementation | review
Task class:
- tiny | routine | non-trivial | high-risk
Delegation target:
- none | implementation subagent | independent reviewer | both
Triggers:
- ...
Reason:
- ...
User constraint:
- ...
Residual risk:
- ...
Allowed next action:
- ...
```

## Boundaries

- Do not default to spawning subagents.
- Do not default away the decision; non-trivial or high-risk work needs an explicit delegation result even when that result is `single_agent`.
- Do not skip the decision for non-trivial or high-risk work.
- Do not ask for subagents when the work cannot be usefully split.
- Do not let useful independent review disappear into a status report; choose `delegate`, state why `single_agent` is enough, or return `blocked`.
- Keep prompts to subagents minimal when the user authorizes them: pass the original goal, owned scope, relevant files, and expected output, not the main agent's conclusions.
