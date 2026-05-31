# AI Coding Harness

[简体中文](README.md) | English

[![knowledge-check](https://github.com/solitudeTG/harness-coding-skills/actions/workflows/knowledge-check.yml/badge.svg)](https://github.com/solitudeTG/harness-coding-skills/actions/workflows/knowledge-check.yml)

AI Coding Harness is a Skill suite and engineering collaboration template for **Codex / Claude Code**. It is not trying to make agents write more code in a single sitting. It helps AI-assisted development stay traceable, reviewable, and recoverable across sessions, agents, and human collaborators.

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

- `using-harness`: a high-recall entrypoint Skill that decides whether the current task needs Harness routing
- Ten focused `harness-*` Skills for start gates, delegation decisions, knowledge retrieval, document lifecycle, incident learning, vision checks, readiness, change narrative, knowledge capture, and project rule promotion
- Bundled templates for `AGENTS.md`, Feature, ADR, Lesson, and Evidence records
- Bundled `knowledge_check.py` and `harness_closeout_check.py` for validating structured Harness documents and closeout blocks
- Optional Stop hook runtime examples for Codex, Claude Code, and OpenCode under `using-harness/hooks/`
- `skill_metadata_check.py` for validating Skill metadata, trigger surfaces, and required bundled resources
- Minimal and project-level examples so adoption can start small and grow only when needed

## Install In 30 Seconds

Clone the repository:

```bash
git clone https://github.com/solitudeTG/harness-coding-skills.git
cd harness-coding-skills
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

Restart your agent after installation. Start with `using-harness`; it routes to the smaller `harness-*` Skills only when needed.

Hooks are optional. The Skills-only install remains the baseline. Default examples enable the Stop hook plus same-session compact recovery so completion claims and context restoration can be assisted without slowing down every edit. See `using-harness/hooks/` and the enhanced install notes in [INSTALL.md](INSTALL.md).

See [INSTALL.md](INSTALL.md) for more installation options.

## Minimal Adoption Path

Copy the agent rules template into your project:

```bash
cp ~/.codex/skills/using-harness/assets/templates/AGENTS.md /path/to/your-project/AGENTS.md
```

Windows PowerShell:

```powershell
Copy-Item "$HOME\.codex\skills\using-harness\assets\templates\AGENTS.md" "C:\path\to\your-project\AGENTS.md"
```

Then define three things in `AGENTS.md`:

```text
1. What project rules must agents always follow?
2. Which command proves the project still works?
3. Where should completion evidence be recorded?
```

For projects that evolve across multiple sessions, add:

```text
docs/BACKLOG.md
docs/features/
docs/decisions/
docs/lessons/
docs/evidence/
```

Use the bundled templates from `using-harness/assets/templates/`:

```text
using-harness/assets/templates/FEATURE.md
using-harness/assets/templates/ADR.md
using-harness/assets/templates/LESSON.md
using-harness/assets/templates/EVIDENCE.md
```

## Typical Workflow

```text
Receive task
  -> using-harness decides whether Harness applies
  -> harness-start-gate decides whether work may start
  -> retrieve project knowledge, clarify intent, or create a Feature / spec / plan / ADR when needed
  -> execute the smallest verifiable change
  -> run verification and record Evidence
  -> use readiness / change narrative / knowledge capture when preparing review, release, or handoff
```

Not every task needs the whole chain. The point is to choose the lightest workflow that protects the context future work will actually need.

## Skills

| Skill | Use when |
| --- | --- |
| `using-harness` | Route the current task to the right Harness workflow. |
| `harness-start-gate` | Decide whether non-trivial work may start or first needs clarification, retrieval, Vision Gate, Feature, spec, plan, or ADR. |
| `harness-delegation-gate` | Decide whether to ask for implementation subagents or an independent reviewer. |
| `harness-knowledge-retrieval` | Recover project context before acting. |
| `harness-doc-lifecycle` | Govern stale, superseded, deprecated, or archived documents. |
| `harness-incident-learning` | Turn bugs, incidents, and patch churn into prevention. |
| `harness-vision-gate` | Check original intent before implementation, review, merge, done, or handoff. |
| `harness-readiness-dashboard` | Summarize gate, reviewer, evidence, risk, and blocker status before review, release, handoff, or completion. |
| `harness-change-narrative` | Explain what changed and why for commits, PRs, handoffs, release notes, or progress summaries. |
| `harness-knowledge-capture` | Decide whether to record Feature, ADR, Lesson, Evidence, or handoff memory. |
| `harness-project-rules` | Decide whether a source-backed constraint belongs in `AGENTS.md` or another project-level agent rule file. |

See [docs/skill-index.md](docs/skill-index.md) for more detail.

## Repository Structure

```text
skills/       Installable agent workflow Skills, including using-harness bundled scripts/templates
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

Validate structured Harness documents:

```bash
python skills/using-harness/scripts/knowledge_check.py --root . --docs-path docs
```

Use strict mode when preparing a stronger review or CI gate:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills --strict
python skills/using-harness/scripts/knowledge_check.py --root . --docs-path docs --strict
```

After global installation, use the bundled script under the installed skill root, for example `$HOME/.codex/skills/using-harness/scripts/knowledge_check.py`. Projects may vendor the scripts for CI, but normal Harness use should not require per-project script setup.

## Examples

- [Minimal Harness example](examples/minimal-harness/README.md): the smallest useful loop around rules, verification, and Evidence
- [Project Harness example](examples/project-harness/README.md): shows how Feature, ADR, Lesson, and Evidence records work together

## Design Principle

Harness should reduce repeated rediscovery, repeated mistakes, and evidence-free completion claims. It should not become a ceremony that creates documents for every tiny change.

Knowledge before orchestration.  
Gate before automation.  
Governance before scale.

## Status

This project is in early public shaping. The current goal is to publish a clear, minimal, reusable Harness Skill suite and template set so AI-assisted development can move from "held together by a long prompt" toward an engineering system that keeps improving.

## License

MIT
