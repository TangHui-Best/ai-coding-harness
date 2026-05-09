# AI Coding Harness

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

## Repository Structure

```text
skills/      Reusable agent workflow skills
docs/        Concepts, architecture, and workflow notes
templates/   Reusable document templates
examples/    Minimal and project-level harness examples
```

## Harness Capabilities

- Knowledge retrieval before non-trivial work
- Vision gate before review, merge, release, or handoff
- Evidence gate before claiming completion
- Change narrative for commits, PRs, and handoffs
- Incident learning after bugs and regressions
- Document lifecycle management for stale or superseded knowledge
- Knowledge capture for durable project memory

## Status

This project is in early public shaping. The first goal is to publish a clear, minimal, reusable version of the harness skills and templates.

## License

MIT
