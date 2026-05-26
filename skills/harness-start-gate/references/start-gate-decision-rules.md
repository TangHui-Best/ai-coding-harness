# Start Gate Decision Rules

Use this reference when task class or Start Gate outcome is unclear.

## Task Classes

| Class | Meaning | Default gate pressure |
| --- | --- | --- |
| `tiny` | Local, reversible edit where project memory cannot change the outcome. | Usually `ready`. |
| `routine` | Bounded change with clear intent and known verification path. | Usually retrieval optional. |
| `non-trivial` | Feature work, refactor, behavior change, multi-file change, or unclear acceptance criteria. | Run retrieval or Vision Gate when triggered. |
| `high-risk` | Boundary, architecture, data model, security, cost, migration, or cross-feature decision. | Require durable pre-work anchor before implementation. |

## Risk Triggers

Check these before coding:

- Original goal, user pain point, acceptance criteria, non-goals, Vision Anchor, or owner boundary is unclear.
- Work spans multiple sessions, agents, modules, or delivery steps.
- Work changes public behavior, data shape, module boundaries, storage, infrastructure, permissions, or external contracts.
- Prior decisions, active Feature state, stale-doc status, Lessons, or Evidence may affect the answer.
- The proposed path looks broader, costlier, or more complex than the user goal requires.
- The task may have separable workstreams, parallel exploration, independent verification, or enough scope that implementation subagents should be proposed.
- The only way to recover context later would be the chat transcript.

## Outcomes

| Outcome | Use when | Required next action |
| --- | --- | --- |
| `ready` | Intent, scope, ownership, verification, and risk are clear enough for the task class. | Start implementation workflow. |
| `needs clarification` | Missing user intent or acceptance details could change implementation. | Ask specific questions before coding. |
| `needs retrieval` | Existing Feature, ADR, Lesson, Evidence, stale-doc, or prior decision context may affect work. | Use `harness-knowledge-retrieval`. |
| `needs vision gate` | The path may drift from the original goal or solve the wrong problem. | Use `harness-vision-gate` Entry Gate. |
| `needs feature` | Work changes or starts a delivery boundary that future sessions must recover. | Use `harness-knowledge-capture` to create or update a Feature anchor. |
| `needs spec` | Requirements or acceptance criteria need a durable source before implementation. | Create/update a spec and link it from Feature when applicable. |
| `needs plan` | Execution order, decomposition, rollback, or multi-agent coordination needs a durable route. | Create/update a plan and link it from Feature when applicable. |
| `needs ADR` | A decision affects long-term architecture, interfaces, cost, security, operations, or likely future debate. | Use `harness-knowledge-capture` to create an ADR before coding. |
| `blocked` | Required context, permissions, environment, or decision owner is unavailable. | Stop and name the blocker. |
