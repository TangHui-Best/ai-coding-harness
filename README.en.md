# AgentMentor

[简体中文](README.md) | English

[![knowledge-check](https://github.com/TangHui-Best/using-agentmentor/actions/workflows/knowledge-check.yml/badge.svg)](https://github.com/TangHui-Best/using-agentmentor/actions/workflows/knowledge-check.yml)

AgentMentor is a Skill suite for governing AI-assisted software engineering across **Codex / Claude Code / OpenCode**. It is not meant to make agents write more code. It helps long-running AI development stay recoverable, verifiable, traceable, and less likely to repeat the same failures across sessions, agents, reviews, and handoffs.

```text
Confirm the real goal -> retrieve project memory -> make the smallest verifiable change -> close with evidence and durable learning
```

## Why AgentMentor Exists

AI coding assistants can already generate code quickly. The harder problem is that fast local progress can make the engineering system drift:

- Goals drift across multiple iterations while tests still pass.
- Old specs or acceptance criteria become stale, but the agent keeps following them.
- One Feature receives repeated patches, yet nobody notices that the abstraction is failing.
- Reviews see the diff, but not the decisions, rejected paths, risks, or verification limits.
- The agent confidently says the work is done without Evidence.
- A new session or compacted context cannot recover the important engineering judgment.
- Documentation grows, but nobody knows which documents actually changed future agent behavior.

AgentMentor's core idea:

```text
Prompt solves one-time expression.
Skill solves one-time workflow.
AgentMentor solves long-term engineering governance.
```

It is not documentation theater. It is a control loop for the AI-agent era: keep goals real, boundaries clear, outcomes verifiable, history recoverable, and failures reusable as prevention.

## Core Mechanisms

AgentMentor turns senior engineering judgment into control points that agents can trigger, execute, and check:

- **Gate**: Decide whether work may proceed before implementation, review, release, handoff, or completion claims.
- **Knowledge**: Recover context from Feature, ADR, Lesson, Evidence, and AGENTS.md records.
- **Evidence**: Bind completion claims to reproducible checks, results, and known limitations.
- **Lifecycle**: Decide whether old documents are active, completed, superseded, deprecated, or archived.
- **Narrative**: Explain why a change was made for commits, PRs, handoffs, and release notes.
- **Project Rules**: Promote only source-backed, cross-task, behavior-changing constraints into `AGENTS.md`.
- **Usage Telemetry**: Record only documents that truly affected judgment or change narrative, not every read.

## Design Principles

- In the agent era, the bottleneck is not slow code writing; it is goal drift, false completion, lost context, repeated failures, and control-plane sprawl.
- AgentMentor is not about producing formal documents. Its value is making agent development governable, recoverable, verifiable, and less likely to repeat failures.
- Documentation value is not measured by quantity, but by whether it is retrieved, judged, and used in a closed loop.
- Code carries how the system runs now; documentation carries why it runs that way and what future changes must not forget.
- Automation with unstable value should be downgraded to an explicit workflow or removed.

## What This Repository Provides

- `using-agentmentor`: the high-recall entrypoint Skill. It decides whether the current task needs AgentMentor routing.
- Eleven focused workflow Skills: Start Gate, Vision Gate, Spec Drift, Delegation Gate, Knowledge Retrieval, Doc Lifecycle, Incident Learning, Readiness Dashboard, Change Narrative, Knowledge Capture, and Project Rules.
- Templates for `AGENTS.md`, Feature, ADR, Lesson, and Evidence records.
- `knowledge_check.py` and `closeout_check.py` for validating structured AgentMentor documents and closeout blocks.
- Optional Stop-only hook examples for Codex, Claude Code, and OpenCode under `using-agentmentor/hooks/`.
- Codex Desktop personal plugin package: `.codex-plugin/plugin.json`, plugin-level `hooks.json` / `hooks/hooks.json`, `hooks/run-agentmentor-hook.cmd`, `hook_diagnostics.py`, and `.agentmentor/hook-events/events.jsonl` runtime traces; the plugin identity is `agentmentor@personal`.
- `usage_record.py` for recording real document usage that affected decisions.
- `skill_metadata_check.py` for validating Skill metadata, trigger surfaces, and required bundled resources.
- Minimal and project-level examples so teams can start small and grow only when the project needs more memory.

## The 12 Skills

| Skill | Use when |
| --- | --- |
| `using-agentmentor` | Route the current task to the right AgentMentor workflow. |
| `start-gate` | Decide whether non-trivial work may start or needs clarification, retrieval, Feature, spec, plan, or ADR first. |
| `vision-gate` | Check whether implementation, review, merge, done, release, or handoff still matches the original intent. |
| `knowledge-retrieval` | Recover project context, decisions, Evidence, and Lessons before acting. |
| `doc-lifecycle` | Decide whether old documents are still trustworthy or have been superseded, deprecated, or archived. |
| `spec-drift` | Repair stale specs or acceptance criteria before changing code when real cases contradict them. |
| `delegation-gate` | Decide whether implementation subagents or independent reviewers are needed. |
| `readiness-dashboard` | Summarize readiness, progress, maturity, blockers, and gap before review, release, handoff, or completion. |
| `change-narrative` | Explain what changed and why for commits, PRs, handoffs, release notes, or progress summaries. |
| `knowledge-capture` | Decide whether Feature, ADR, Lesson, Evidence, or handoff memory is needed before completion claims. |
| `incident-learning` | Turn bugs, incidents, and patch churn into reusable prevention. |
| `project-rules` | Decide whether a lesson or constraint belongs in `AGENTS.md` or another project-level agent rule file. |

See [docs/skill-index.md](docs/skill-index.md) for more detail.

## Install

Clone the repository:

```bash
git clone https://github.com/TangHui-Best/using-agentmentor.git
cd using-agentmentor
```

Install for Codex:

```bash
bash scripts/install.sh codex
bash scripts/install.sh --verify codex
```

Install for Claude Code:

```bash
bash scripts/install.sh claude
bash scripts/install.sh --verify claude
```

Windows PowerShell:

```powershell
.\scripts\install.ps1 both
.\scripts\install.ps1 -Verify both
```

Restart your agent after installation. Start with `using-agentmentor`; it routes to smaller workflow Skills only when needed.

See [INSTALL.md](INSTALL.md) for more installation options.

## Optional Project Rules

AgentMentor does not automatically modify global or project `AGENTS.md` files. When repository-level rules would help future agents, copy the bundled `AGENTS.md` template manually:

```bash
cp ~/.codex/skills/using-agentmentor/assets/templates/AGENTS.md /path/to/your-project/AGENTS.md
```

Windows PowerShell:

```powershell
Copy-Item "$HOME\.codex\skills\using-agentmentor\assets\templates\AGENTS.md" "C:\path\to\your-project\AGENTS.md"
```

Define three things first:

```text
1. Which project rules must agents always follow?
2. Which command proves the project still works?
3. Where should completion evidence be recorded?
```

For longer-lived projects, add these rules to the copied `AGENTS.md`:

```text
- Run Start Gate before non-trivial implementation.
- If real cases, validation, or user feedback contradict an existing spec, run Spec Drift before changing code.
- If repeated patches add scenario-specific branches, pause and run Patch Churn Review before continuing.
```

Then gradually add:

```text
docs/BACKLOG.md
docs/features/
docs/decisions/
docs/lessons/
docs/evidence/
```

## Typical Workflow

```text
Receive task
  -> using-agentmentor decides whether AgentMentor applies
  -> start-gate decides whether work may start
  -> run retrieval / spec drift / vision gate / delegation gate when needed
  -> create or update necessary Feature, spec, plan, or ADR memory
  -> execute the smallest verifiable change
  -> run verification and record Evidence
  -> use readiness-dashboard for progress, maturity, blocker, and gap status before delivery
  -> use change-narrative to explain the change
  -> use knowledge-capture to decide whether completion may be claimed
```

Not every task needs the whole chain. The point is to choose the lightest workflow that protects the context future work will actually need.

## Hook Boundary

Hooks are optional. Skills-only installation is the baseline.

The current default hook examples enable only **Stop-time completion checks**: when an agent is about to say done, fixed, verified, ready, or similar completion language, the hook checks closeout and Evidence status.

AgentMentor no longer provides default `pre-compact` / `session-start` recovery hooks. Platform compaction remains the platform's responsibility. If a handoff is needed, explicitly ask the agent to write one.

After installing or updating Codex hooks, run:

```powershell
python "$HOME\.codex\skills\using-agentmentor\scripts\hook_diagnostics.py" codex --project-root "C:\path\to\your-project"
```

A Stop runner warning means the optional hook path is not proven on that machine; keep using Skills-only closeout.

## Compared With Superpowers And OpenSpec

| System | Primary problem | Layer |
| --- | --- | --- |
| Superpowers | Make agents follow better workflows for a single task. | Workflow discipline |
| OpenSpec | Organize requirement changes around specs, proposals, tasks, and archive. | Spec governance |
| AgentMentor | Make goals, evidence, decisions, failures, recovery, and rules form a long-term loop. | Engineering governance |

Superpowers helps agents work with discipline. OpenSpec gives requirement changes structure. AgentMentor asks whether those workflows, specs, evidence records, and lessons actually change future agent behavior.

## Repository Structure

```text
skills/       Installable agent workflow Skills, including using-agentmentor bundled scripts/templates
hooks/        Codex plugin-level Stop hook wrapper and example config
docs/         Concepts, architecture, Features, ADRs, Lessons, and Evidence
templates/    Reusable document templates
examples/     Minimal and project-level AgentMentor examples
scripts/      Lightweight validation and usage-recording utilities
```

## Validate

Validate Skill metadata:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills
```

Validate structured governance documents:

```bash
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs
```

Use strict mode for stronger review or CI gates:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills --strict
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs --strict
```

## Examples

- [Minimal example](examples/minimal-harness/README.md): the smallest useful loop around rules, verification, and Evidence.
- [Project-level example](examples/project-harness/README.md): shows how Feature, ADR, Lesson, and Evidence records work together.

## Articles

- [AgentMentor: bringing AI agents into governable software development](docs/articles/agentmentor-governable-ai-agent-development-flow.md)

## Current Status

AgentMentor is still evolving quickly. The current focus is moving AI-assisted development from "held together by a long prompt" toward an engineering system governed by Gates, Evidence, Knowledge, and Lifecycle.

## License

MIT
