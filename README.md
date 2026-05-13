# AI Coding Harness

[English](README.md) | [Simplified Chinese](README.zh-CN.md)

[![knowledge-check](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml/badge.svg)](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml)

AI Coding Harness is a **Codex / Claude Code Skill suite** for AI-assisted software development.

It gives coding agents reusable skills for start gates, project memory, evidence, change narrative, incident learning, and handoff discipline. If you found this repository on GitHub, the fastest path is:

```text
Install skills -> add AGENTS.md template -> run one validation command
```

See [INSTALL.md](INSTALL.md) for one-command installs, manual installs, and project-local setup.

## Install In 30 Seconds

Clone the repository:

```bash
git clone https://github.com/TangHui-Best/ai-coding-harness.git
cd ai-coding-harness
```

Install for Codex:

```bash
bash scripts/install.sh codex
```

Install for Claude Code:

```bash
bash scripts/install.sh claude
```

On Windows PowerShell:

```powershell
.\scripts\install.ps1 both
```

Restart your agent after installing skills. Start with `using-harness`; it routes to the smaller `harness-*` skills only when they are needed.

## Why This Exists

AI coding assistants can produce code quickly, but speed alone does not make a software system stronger.

In real projects, the hard problems are often not "can the agent write code?", but:

- Does the agent know the project rules?
- Can a future session recover the context?
- Is completion backed by evidence?
- Are decisions and rejected paths preserved?
- Do incidents become durable prevention rules?
- Can humans and agents collaborate without losing state?

This repository explores a lightweight engineering harness for AI-assisted development.

## Core Idea

```text
Prompt solves one-time expression.
Skill solves one-time workflow.
Harness solves long-term engineering system behavior.
```

An AI coding harness turns repeated collaboration experience into reusable workflows, project memory, gates, and traceable evidence.

Harness is not just a component list. It is a control loop:

```text
Run -> Trace -> Diagnose -> Patch Harness -> Eval -> Deploy -> Learn
```

The practical question is whether each AI-assisted task leaves the engineering system more recoverable, verifiable, and resistant to repeated mistakes.

## What This Repository Provides

- A routing Skill: `using-harness`
- Ten focused harness skills for start gates, delegation decisions, retrieval, lifecycle, incident learning, vision checks, readiness dashboards, change narrative, knowledge capture, and project rule promotion
- Reusable templates for Feature, ADR, Lesson, Evidence, and AGENTS instructions
- A lightweight `knowledge_check.py` validator for structured Harness artifacts
- A lightweight `skill_metadata_check.py` validator for Skill trigger metadata
- Minimal and project-level examples for gradually adopting the workflow

## Repository Structure

```text
skills/       Installable agent workflow Skills
docs/         Concepts, architecture, and workflow notes
templates/    Reusable document templates
examples/     Minimal and project-level harness examples
scripts/      Lightweight validation utilities
```

## Skill Activation Model

Harness skills are designed for gradual skill loading. Agents may only see a Skill name and description before choosing whether to load the full `SKILL.md`, so trigger-critical guidance lives in frontmatter descriptions as well as in the Skill body.

`using-harness` is the high-recall entrypoint for non-trivial engineering work, multi-file bugfixes, behavior changes, commits, PRs, handoffs, and completion claims. Once loaded, it runs a lightweight Harness Presence Check and exits when Harness is not relevant. The focused `harness-*` skills also carry independent trigger descriptions so they can activate directly when a task clearly matches their boundary.

## Skills

| Skill | Use when |
| --- | --- |
| `using-harness` | You are starting non-trivial engineering work or need to route a commit, PR, handoff, completion claim, or Harness mention through the right workflow. |
| `harness-start-gate` | You need to decide whether non-trivial work may start or first needs clarification, retrieval, Vision Gate, Feature, spec, plan, or ADR. |
| `harness-delegation-gate` | You need to decide whether to ask the user for implementation subagents or an independent reviewer. |
| `harness-knowledge-retrieval` | You need existing project context before acting. |
| `harness-doc-lifecycle` | You need to govern stale, superseded, deprecated, or archived docs. |
| `harness-incident-learning` | A bug or incident is fixed and the system may need prevention. |
| `harness-vision-gate` | Work needs an original-intent check before implementation, review, merge, or handoff. |
| `harness-readiness-dashboard` | Work needs a concise gate, reviewer, Evidence, and knowledge status before review, release, handoff, or completion. |
| `harness-change-narrative` | A commit, PR, handoff, release note, or change summary needs a compact story. |
| `harness-knowledge-capture` | A task may need durable Evidence, ADRs, Lessons, Feature state, or handoff memory. |
| `harness-project-rules` | A source-backed behavior constraint may belong in `AGENTS.md` or another project-level agent rule file. |

## Quick Start

First install the Skill suite. Then copy the agent rules template into your project:

```bash
cp templates/AGENTS.md /path/to/your-project/AGENTS.md
```

On Windows PowerShell:

```powershell
Copy-Item ".\templates\AGENTS.md" "C:\path\to\your-project\AGENTS.md"
```

Then define three things in `AGENTS.md`:

```text
1. What project rules should agents always follow?
2. What command proves the project still works?
3. Where should completion evidence be recorded?
```

For a project that lasts across multiple sessions, also create:

```text
docs/BACKLOG.md
docs/features/
docs/decisions/
docs/lessons/
docs/evidence/
```

Use the templates:

```text
templates/FEATURE.md
templates/ADR.md
templates/LESSON.md
templates/EVIDENCE.md
```

Validate structured Harness docs:

```bash
python scripts/knowledge_check.py --root . --docs-path docs
```

Validate Skill metadata and trigger-surface health:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills
```

Use strict mode when preparing a stronger review or CI gate:

```bash
python scripts/knowledge_check.py --root . --docs-path docs --strict
python scripts/skill_metadata_check.py --root . --skills-path skills --strict
```

## Skill Layout

Each Skill is a directory under `skills/` with a `SKILL.md` entrypoint:

```text
skills/
  using-harness/
    SKILL.md
  harness-start-gate/
    SKILL.md
  ...
```

The repository-level `scripts/` directory is for validation utilities. It is not required at Skill runtime unless you choose to add those checks to your project or CI.

## Minimal Adoption Path

Start with the smallest useful loop:

```text
AGENTS.md
  -> start gate
  -> verification command
    -> evidence record
      -> change narrative
        -> project-rules gate before AGENTS.md changes
```

Then add structure only when the project needs it:

```text
Feature pages
  -> ADRs
    -> Lessons
      -> document lifecycle
        -> knowledge check in CI
```

## Status

This project is in early public shaping. The first goal is to publish a clear, minimal, reusable version of the Harness Skills and templates.

## Design Principle

Harness should reduce repeated rediscovery and unverifiable completion. It should not become a ceremony that creates documents for every tiny change.

Knowledge before orchestration. Gate before automation. Governance before scale.

## License

MIT
