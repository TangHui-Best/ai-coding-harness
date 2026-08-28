# AgentMentor

[简体中文](README.md)

[![Knowledge checks](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml/badge.svg)](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml)

## Let every AI development task
## leave engineering facts useful for the next decision.

AgentMentor gives Codex, Claude Code, and other coding agents **recoverable, explainable, and verifiable engineering memory** for codebases that evolve over time.

Code tells us what the system is now.

AgentMentor preserves the facts that code cannot reliably explain:

- what a feature is meant to achieve and where its boundary lies;
- why a design was chosen and which alternatives were rejected;
- which failures have already occurred and must not recur;
- which claims have been verified, including their scope and limitations.

The next agent should not have to infer the answer from chat history, Git diffs, and scattered comments:

> Why was the system designed this way?<br>
> Which options were already rejected?<br>
> What did this change actually verify?

```text
A prompt expresses a request once.
A workflow Skill helps complete a task once.
AgentMentor helps the project retain facts needed for the next task.
```

---

## Why AgentMentor

Coding models are already effective at implementing local changes. The hard part is retaining sound engineering judgment through many conversations, agents, reviews, and iterations.

Passing tests do not necessarily mean the right thing was built.

When the goal has drifted, a specification has become stale, a rejected approach is proposed again, or a new agent cannot understand an earlier design choice, neither the code nor a green test suite will reliably provide the answer.

Typical failures include:

- requirements drift while tests continue to pass;
- an agent faithfully implements stale specifications or acceptance criteria;
- a feature accumulates patches while its failing abstraction goes unnoticed;
- reviews see a diff but not the decisions, risks, or rejected alternatives behind it;
- an agent claims completion without reproducible verification facts;
- a new session or agent cannot recover critical engineering judgment;
- documentation grows without changing future engineering decisions.

AgentMentor does not ask you to document every change.

It records facts only when they can affect future judgment, and retrieves only a small, directly relevant context package when history actually matters.

---

## How it works

```text
Development task + known changed paths
        │
        ▼
Read one unified engineering Index
        │
        ├── Feature: goal, boundary, specification, acceptance
        ├── ADR: design choice and rejected alternatives
        ├── Lesson: real failure and prevention
        └── Evidence: verification facts, scope, limitations
        │
        ▼
The model plans, implements, tests, and collaborates normally
        │
        ▼
Durable facts are recorded only when an engineering event occurs
```

AgentMentor follows two principles:

1. **Retrieve precisely, then work autonomously**<br>
   For work that may affect feature behavior, specifications, architecture, interfaces, data meaning, or acceptance, the main agent reads the unified Index once and uses each Brief to select relevant documents instead of scanning the whole knowledge base.

2. **Record only facts worth retaining**<br>
   Ordinary small changes need no new document. Durable facts are recorded only for events such as intent conflict, a stable decision, recurring failure, or an important delivery claim.

No relevant Index entry is a valid result: project history should not interfere with a task that does not need it.

---

## Four kinds of engineering facts

| Document | Question it answers | Create or update it when |
| --- | --- | --- |
| **Feature** | What are we building, why, within which boundary, and how is it accepted? | A feature needs a durable specification or acceptance criteria |
| **ADR** | Why was this chosen, and why were other options rejected? | A decision will affect architecture, interfaces, risk, or cost over time |
| **Lesson** | What failed, why did it fail, and how do we prevent recurrence? | A specification drifts, a regression recurs, or a reusable failure pattern emerges |
| **Evidence** | Which claim was verified? What was verified, and what remains unverified? | Completion, release, handoff, or an important judgment needs proof |

The unified Index is a lightweight directory of current Features and accepted ADRs; it helps the main agent choose documents but never replaces their content.

---

## Feature is the feature-level SDD spec

AgentMentor does not require a separate Capability or Plan document type.

In AgentMentor, a **Feature is the feature-level SDD spec**. It contains:

- Goal: the user or business outcome;
- Scope: scope and explicit non-goals;
- Specification: behavior, rules, constraints, interfaces, and failure behavior;
- Acceptance: verifiable Given / When / Then scenarios;
- Current State: current implementation and verification state;
- Decision Context: historical tradeoffs needed before changing the feature;
- Links: related ADRs, Lessons, Evidence, and external specifications.

If a team also uses OpenSpec, Superpowers, or another specification tool, link its artifacts from the Feature. AgentMentor remains independently usable without them.

---

## TDD by default, without documentation theater

For deterministic behavior, AgentMentor recommends letting Feature acceptance scenarios drive tests:

```text
Acceptance scenario
        ↓
Test name and assertions
        ↓
Red → Green → Refactor
        ↓
Final verification recorded as Evidence
```

This means:

- acceptance criteria are not prose that disappears after implementation;
- tests are not technical artifacts detached from requirements;
- Evidence records final known facts, not every temporary attempt.

When test-first is unsuitable—for example, experience evaluation, an external integration, or exploratory validation—describe the alternative method and its limitations in the Feature's `Verification Strategy`.

---

## Six Skills, invoked only when they matter

| Skill | Purpose | Trigger |
| --- | --- | --- |
| `agentmentor` | Prompts one unified Index read and agent-led document selection | Work that may affect behavior, specifications, architecture, interfaces, data meaning, or acceptance |
| `agentmentor-intent` | Resolves a real goal, scope, or boundary conflict | A change conflicts with a Feature, ADR, or public boundary |
| `agentmentor-decision` | Records a durable tradeoff for future work | A decision establishes an architecture, module, interface, cost, or risk boundary |
| `agentmentor-learning` | Turns repeated failures into actionable prevention | Specification drift, regression, or repeat failure genuinely occurs |
| `agentmentor-evidence` | Binds an important claim to verifiable facts | A completion, release, handoff, or significant judgment needs proof |
| `agentmentor-closeout` | Compresses the facts known in the current task | Pausing, handing off, or ending work |

They are not a mandatory sequence.

The model should handle ordinary decomposition, implementation, testing, review, and collaboration. AgentMentor appears only when project memory, boundaries, decisions, or evidence are actually needed.

---

## OpenSpec, Superpowers, and AgentMentor

AgentMentor does not replace every development method. It solves a different problem:

> Make long-lived engineering facts from AI development recoverable, explainable, and verifiable.

| Tool | Primary focus | Best fit |
| --- | --- | --- |
| **AgentMentor** | Engineering memory, feature specifications, design rationale, failure learning, verification evidence | You want the codebase to retain its “why” across sessions and agents |
| **OpenSpec** | Change-oriented specifications, proposals, designs, and tasks | You want structured, spec-driven change proposals |
| **Superpowers** | A composable software-development methodology and execution workflow | You want a more complete workflow for planning, TDD, review, and delivery |

OpenSpec stores specifications in the codebase and organizes change proposals, designs, tasks, and specification deltas. Superpowers provides a composable workflow from clarification and planning through TDD and review. [OpenSpec](https://openspec.dev/) · [Superpowers](https://github.com/obra/superpowers)

They can work together:

```text
OpenSpec or another tool
    └── produces a proposal or plan for one change
                │
                ▼
AgentMentor Feature
    └── retains the feature specification and durable boundary
                │
                ├── ADR: lasting design rationale
                ├── Lesson: prevention for repeated failure
                └── Evidence: verification facts for key claims
```

AgentMentor also works on its own: Features, ADRs, Lessons, Evidence, and one bounded retrieval form a complete engineering-memory loop.

---

## Quick start

### 1. Install

Clone the repository:

```bash
git clone https://github.com/TangHui-Best/ai-coding-harness.git
cd ai-coding-harness
```

Install for Codex:

```powershell
.\scripts\install.ps1 codex
.\scripts\install.ps1 -Verify codex
```

Install for Claude Code:

```powershell
.\scripts\install.ps1 claude
.\scripts\install.ps1 -Verify claude
```

Install for both:

```powershell
.\scripts\install.ps1 both
.\scripts\install.ps1 -Verify both
```

From Bash:

```bash
bash scripts/install.sh codex
bash scripts/install.sh --verify codex
```

Restart the target agent after installation so it loads the new Skill metadata.

### 2. Start with a real change

When a task depends on project history, an existing feature specification, or prior decisions, use `agentmentor`:

```text
Add inventory restoration when an order is cancelled.

Known affected paths:
- src/orders/
- src/inventory/
- tests/orders/
```

AgentMentor performs one bounded retrieval:

```text
Known paths
  → read the unified Index
  → the main agent semantically selects 0–3 relevant Features and needed ADRs
  → read directly linked Lessons / Evidence only when needed
```

The model then implements and verifies the change normally.

### 3. Record only when an event occurs

For example:

- “Should a shipped order restore inventory when cancelled?”<br>
  If this establishes a lasting business rule, record an ADR.

- “This is the third regression caused by duplicate asynchronous messages.”<br>
  If there is a reusable root cause and prevention, record a Lesson.

- “This feature passed the specified integration tests and is ready for QA.”<br>
  If the claim must be reviewable later, record Evidence.

You do not need to create a complete documentation system up front. Start with the Feature you are changing.

---

## What AgentMentor does not do

AgentMentor does not:

- decide whether a product request is worth building;
- force every task through planning, delegation, review, or closeout stages;
- load all historical documents simply because a knowledge base exists;
- turn every chat, Git diff, or temporary attempt into project memory;
- replace tests, code review, or real verification with documentation;
- mistake a complete-looking workflow for reliable engineering.

It provides the smallest reusable engineering facts precisely where the model cannot reliably derive them from the current code but future work depends on them.

---

## Validate the repository

Validate Skill metadata:

```powershell
python scripts\skill_metadata_check.py --root . --strict
```

Check that the Index is current:

```powershell
python scripts\generate_index.py --root . --check
```

Validate AgentMentor document structure:

```powershell
python scripts\knowledge_check.py --root . --docs-path docs --strict
```

Run tests:

```powershell
pytest -q
```

---

## Design evolution: why the new architecture orchestrates less

Earlier AI-coding frameworks often used layered gates, prescribed subflows, and large rule sets to compensate for models that struggled to decompose tasks, choose verification, and retain context.

For capable coding models, repeating those controls has a cost:

- the same task is classified and reclassified by several gates;
- the same project material is repeatedly read;
- overlapping rules consume attention needed to understand and verify the actual change;
- a default workflow replaces judgment the model could apply directly.

This is not an argument against Skills. It changes their role from **controlling model behavior by default** to **providing high-value engineering facts when an event warrants them**.

Anthropic has described reducing the Claude Code system prompt by more than 80% for its Claude 5 generation models with no measurable loss on coding evaluations. Its context-engineering direction is to remove repeated constraints, leave room for judgment, and disclose context progressively when it is useful. [The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)

Verification is not removed: deterministic checks such as tests, linting, and builds remain essential. The better boundary is to trigger specialized capabilities when a task needs them, not to chain every Skill into every task. [Building verification loops in Claude Code with skills](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills)

AgentMentor therefore chooses to:

> Trust capable models with ordinary reasoning and execution.<br>
> Concentrate engineering constraints on facts that models cannot retain by themselves but future evolution depends on.

---

## Project status

- `v1.0.0` is the stable historical baseline;
- `main` carries the incompatible AgentMentor v2 architecture;
- real historical-task benchmarks remain follow-up quality evaluation work; until then, they are not evidence of a performance improvement.

---

## Documentation

- [Installation](INSTALL.md)
- [Quick start](docs/quickstart.md)
- [Skill index](docs/skill-index.md)
- [Engineering Index](docs/INDEX.md)
- [Architecture Feature](docs/features/F017-agentmentor-vnext-gpt56-workflow.md)
- [Architecture ADR](docs/decisions/ADR-010-agentmentor-vnext-event-triggered-memory-layer.md)

---

## License

MIT
