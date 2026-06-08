# AgentMentor

[简体中文](README.md) | English

[![knowledge-check](https://github.com/TangHui-Best/using-agentmentor/actions/workflows/knowledge-check.yml/badge.svg)](https://github.com/TangHui-Best/using-agentmentor/actions/workflows/knowledge-check.yml)

AgentMentor is a Skill suite and engineering collaboration template for **Codex / Claude Code**, with optional hook examples for Codex, Claude Code, and OpenCode. It is not trying to make agents write more code in a single sitting. It helps AI-assisted development stay traceable, reviewable, and recoverable across sessions, agents, and human collaborators.

If you are opening this repository for the first time, think of it as engineering guardrails for AI coding work:

```text
Confirm the goal -> retrieve context -> make the smallest coherent change -> close with evidence
```

It gives agents a reason to pause at the moments that matter: Is the request real? Are the boundaries clear? How will the result be verified? Can the next session recover the context? Did a failure become durable learning?

## Who This Is For

- Developers using Codex, Claude Code, or similar coding agents on real projects
- Teams that want agents to remember project rules, preserve handoff context, and explain changes clearly
- Projects that have already felt the pain of lost context, evidence-free completion claims, unclear PR narratives, repeated patching, or multi-agent work that does not converge

For a one-off experiment, you may only need a small part of the suite.  
For a project that keeps evolving, the Harness becomes more valuable.

## Why Harness Exists

AI coding assistants can already produce code quickly. The harder problem is usually not whether an agent can write code, but whether the engineering system gets stronger after the work.

Real projects need answers to questions like:

- Does the agent know the project's long-lived rules?
- Can a new session recover why earlier work was done?
- Is a completion claim backed by actual verification evidence?
- Are decisions, rejected paths, and risks preserved?
- Do bugs and incidents become reusable prevention?
- Can humans, agents, and multiple agents collaborate without losing state?

The core idea:

```text
Prompt solves one-time expression.
Skill solves one-time workflow.
Harness solves long-term engineering system behavior.
```

Harness is not documentation theater. It is a lightweight control loop:

```text
Run -> Trace -> Diagnose -> Patch Harness -> Eval -> Deploy -> Learn
```

After each AI-assisted task, the system should be more recoverable, more verifiable, and less likely to repeat the same mistake.

## What This Repository Provides

- `using-agentmentor`: a high-recall entrypoint Skill that decides whether the current task needs AgentMentor routing
- Eleven focused semantic workflow Skills such as `start-gate`, `spec-drift`, `readiness-dashboard`, and `knowledge-capture` for start gates, spec drift checks, delegation decisions, knowledge retrieval, document lifecycle, incident learning, vision checks, readiness, change narrative, knowledge capture, and project rule promotion
- Bundled templates for `AGENTS.md`, Feature, ADR, Lesson, and Evidence records
- Bundled `knowledge_check.py` and `closeout_check.py` for validating structured AgentMentor documents and closeout blocks
- Optional Stop and session recovery hook runtime examples for Codex, Claude Code, and OpenCode under `using-agentmentor/hooks/`
- Codex Desktop personal plugin package: `.codex-plugin/plugin.json`, plugin-level `hooks.json` / `hooks/hooks.json`, `hooks/run-agentmentor-hook.cmd`, `hook_diagnostics.py`, and `.agentmentor/hook-events/events.jsonl` runtime traces; the plugin identity is `agentmentor@personal`
- `skill_metadata_check.py` for validating Skill metadata, trigger surfaces, and required bundled resources
- Minimal and project-level examples so adoption can start small and grow only when needed

## Naming Boundary

The formal system name is **AgentMentor**. `Harness` is only a short name after the full name has been defined; when a project also has a test harness, runtime harness, evaluation harness, or business feature named harness, prefer the full name to avoid ambiguity.

The formal Skill slugs are `using-agentmentor` and the eleven semantic workflow Skills such as `start-gate`, `spec-drift`, `readiness-dashboard`, and `knowledge-capture`. If you are upgrading from a pre-rename version, remove the previous Skill directories before reinstalling; see [ADR-007](docs/decisions/ADR-008-agentmentor-semantic-skill-routing.md) for migration details.

The formal Codex Desktop personal plugin entry is `agentmentor@personal`. If an older `harness@personal` plugin remains enabled, Codex may regenerate the old plugin cache and expose the removed `using-harness` / `harness-*` slugs.

## Install In 30 Seconds

Clone the repository:

```bash
git clone https://github.com/TangHui-Best/using-agentmentor.git
cd using-agentmentor
```

Install for Codex:

```bash
bash scripts/install.sh codex
```

Install for Claude Code:

```bash
bash scripts/install.sh claude
```

Windows PowerShell:

```powershell
.\scripts\install.ps1 both
```

Restart your agent after installation. Start with `using-agentmentor`; it routes to the smaller semantic workflow Skills such as `start-gate`, `readiness-dashboard`, and `knowledge-capture` only when needed.

Hooks are optional. The Skills-only install remains the baseline. Default examples enable the Stop hook plus same-session compact recovery so completion claims and context restoration can be assisted without slowing down every edit. The OpenCode recovery example injects context through `experimental.session.compacting(input, output)` and `output.context`; do not wire `session.created` as an automatic recovery reader. See `using-agentmentor/hooks/` and the enhanced install notes in [INSTALL.md](INSTALL.md).

For Codex Desktop, runtime evidence matters more than whether the settings UI lists the hooks. Use the bundled hook diagnostic after installing or updating hooks. It runs a local runner smoke test and scans Codex session logs for compaction events that did not produce AgentMentor recovery artifacts:

```powershell
python "$HOME\.codex\skills\using-agentmentor\scripts\hook_diagnostics.py" codex --project-root "C:\path\to\your-project"
```

If the diagnostic reports compaction events without recovery artifacts, the optional Codex `PreCompact` recovery path is not proven on that machine; keep using Skills-only, manual handoff, or canonical AgentMentor documents. When a AgentMentor hook actually runs, it writes a minimal runtime trace to `.agentmentor/hook-events/events.jsonl` under the project root.

See [INSTALL.md](INSTALL.md) for more installation options.

## Minimal Adoption Path

AgentMentor does not automatically modify global or project `AGENTS.md` files. You may copy the bundled `AGENTS.md` template into your project when repository-level rules would help future agents:

```bash
cp ~/.codex/skills/using-agentmentor/assets/templates/AGENTS.md /path/to/your-project/AGENTS.md
```

Windows PowerShell:

```powershell
Copy-Item "$HOME\.codex\skills\using-agentmentor\assets\templates\AGENTS.md" "C:\path\to\your-project\AGENTS.md"
```

Then define three things in `AGENTS.md`:

```text
1. What project rules must agents always follow?
2. Which command proves the project still works?
3. Where should completion evidence be recorded?
```

## Optional Project Rules

For longer-lived projects, consider adding these manual rules to the copied `AGENTS.md`:

```text
- Run Start Gate before non-trivial implementation.
- If real cases, validation, or user feedback contradict an existing spec, run Spec Drift before changing code.
- If repeated patches add scenario-specific branches, pause and run Patch Churn Review before continuing.
```

For projects that evolve across multiple sessions, add:

```text
docs/BACKLOG.md
docs/features/
docs/decisions/
docs/lessons/
docs/evidence/
```

Use the bundled templates from `using-agentmentor/assets/templates/`:

```text
using-agentmentor/assets/templates/FEATURE.md
using-agentmentor/assets/templates/ADR.md
using-agentmentor/assets/templates/LESSON.md
using-agentmentor/assets/templates/EVIDENCE.md
```

## Typical Workflow

```text
Receive task
  -> using-agentmentor decides whether Harness applies
  -> start-gate decides whether work may start
  -> retrieve project knowledge, run Spec Drift, clarify intent, or create a Feature / spec / plan / ADR when needed
  -> execute the smallest verifiable change
  -> run verification and record Evidence
  -> use readiness / change narrative / knowledge capture when preparing review, release, or handoff
```

Not every task needs the whole chain. The point is to choose the lightest workflow that protects the context future work will actually need.

## Skills

| Skill | Use when |
| --- | --- |
| `using-agentmentor` | Route the current task to the right AgentMentor workflow. |
| `start-gate` | Decide whether non-trivial work may start or first needs clarification, retrieval, Vision Gate, Feature, spec, plan, or ADR. |
| `delegation-gate` | Decide whether to ask for implementation subagents or an independent reviewer. |
| `knowledge-retrieval` | Recover project context before acting. |
| `spec-drift` | Decide whether a current spec or acceptance criteria is still trustworthy before changing code. |
| `doc-lifecycle` | Govern stale, superseded, deprecated, or archived documents. |
| `incident-learning` | Turn bugs, incidents, and patch churn into prevention. |
| `vision-gate` | Check original intent before implementation, review, merge, done, or handoff. |
| `readiness-dashboard` | Summarize gate, reviewer, evidence, risk, and blocker status before review, release, handoff, or completion. |
| `change-narrative` | Explain what changed and why for commits, PRs, handoffs, release notes, or progress summaries. |
| `knowledge-capture` | Decide whether to record Feature, ADR, Lesson, Evidence, or handoff memory. |
| `project-rules` | Decide whether a source-backed constraint belongs in `AGENTS.md` or another project-level agent rule file. |

See [docs/skill-index.md](docs/skill-index.md) for more detail.

## Repository Structure

```text
skills/       Installable agent workflow Skills, including using-agentmentor bundled scripts/templates
hooks/        Codex plugin-level hook wrapper and example config
docs/         Concepts, architecture, and workflow notes
templates/    Reusable document templates
examples/     Minimal and project-level Harness examples
scripts/      Lightweight validation utilities
```

## Validate

Validate Skill metadata:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills
```

Validate structured AgentMentor documents:

```bash
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs
```

Use strict mode when preparing a stronger review or CI gate:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills --strict
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs --strict
```

After global installation, use the bundled script under the installed skill root, for example `$HOME/.codex/skills/using-agentmentor/scripts/knowledge_check.py`. Projects may vendor the scripts for CI, but normal AgentMentor use should not require per-project script setup.

## Examples

- [Minimal Harness example](examples/minimal-harness/README.md): the smallest useful loop around rules, verification, and Evidence
- [Project Harness example](examples/project-harness/README.md): shows how Feature, ADR, Lesson, and Evidence records work together

## Design Principle

Harness should reduce repeated rediscovery, repeated mistakes, and evidence-free completion claims. It should not become a ceremony that creates documents for every tiny change.

Knowledge before orchestration.  
Gate before automation.  
Governance before scale.

## Status

This project is in early public shaping. The current goal is to publish a clear, minimal, reusable AgentMentor Skill suite and template set so AI-assisted development can move from "held together by a long prompt" toward an engineering system that keeps improving.

## License

MIT
