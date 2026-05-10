# AI Coding Harness

[English](README.md) | [简体中文](README.zh-CN.md)

[![knowledge-check](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml/badge.svg)](https://github.com/TangHui-Best/ai-coding-harness/actions/workflows/knowledge-check.yml)

A practical harness for AI-assisted coding: skills, memory, gates, evidence, and engineering workflows.

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

## What This Repository Provides

- A routing skill: `using-harness`
- Eight focused harness skills for start gates, retrieval, lifecycle, incident learning, vision checks, change narrative, knowledge capture, and project rule promotion
- Reusable templates for Feature, ADR, Lesson, Evidence, and AGENTS instructions
- A lightweight `knowledge_check.py` validator for structured Harness artifacts
- Minimal and project-level examples for gradually adopting the workflow

## Repository Structure

```text
skills/       Reusable agent workflow skills
docs/         Concepts, architecture, and workflow notes
templates/    Reusable document templates
examples/     Minimal and project-level harness examples
scripts/      Lightweight validation utilities
```

## Harness Capabilities

- Start Gate before non-trivial implementation to decide whether clarification or pre-work artifacts are required
- Knowledge retrieval before non-trivial work
- Vision gate before non-trivial implementation and before review, merge, release, or handoff
- Evidence gate before claiming completion
- Change narrative for commits, PRs, and handoffs
- Incident learning after bugs and regressions
- Document lifecycle management for stale or superseded knowledge
- Knowledge capture for durable project memory
- Project rule promotion for source-backed `AGENTS.md` constraints

## Skills

| Skill | Use when |
| --- | --- |
| `using-harness` | You need to route an engineering task through the right harness workflow. |
| `harness-start-gate` | You need to decide whether non-trivial work may start or first needs clarification, retrieval, Vision Gate, Feature, spec, plan, or ADR. |
| `harness-knowledge-retrieval` | You need existing project context before acting. |
| `harness-doc-lifecycle` | You need to govern stale, superseded, deprecated, or archived docs. |
| `harness-incident-learning` | A bug or incident is fixed and the system may need prevention. |
| `harness-vision-gate` | Work needs an original-intent check before implementation, review, merge, or handoff. |
| `harness-change-narrative` | A commit, PR, handoff, release note, or change summary needs a compact story. |
| `harness-knowledge-capture` | A task may need durable Evidence, ADRs, Lessons, Feature state, or handoff memory. |
| `harness-project-rules` | A source-backed behavior constraint may belong in `AGENTS.md` or another project-level agent rule file. |

## Quick Start

For a minimal project, copy:

```text
templates/AGENTS.md
```

Then define three things:

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

Use strict mode when preparing a stronger review or CI gate:

```bash
python scripts/knowledge_check.py --root . --docs-path docs --strict
```

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

This project is in early public shaping. The first goal is to publish a clear, minimal, reusable version of the harness skills and templates.

## Design Principle

Harness should reduce repeated rediscovery and unverifiable completion. It should not become a ceremony that creates documents for every tiny change.

## License

MIT
