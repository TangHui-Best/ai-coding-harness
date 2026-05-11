---
id: F001
doc_kind: feature
status: active
created: 2026-05-09
updated: 2026-05-09
---

# F001: AI Coding Harness

## Goal

Provide a reusable workflow for AI-assisted coding that preserves context, decisions, lessons, and verification evidence across sessions.

## Vision Anchor

- Original request or source: project-level Harness example.
- User pain point or engineering problem: AI-assisted work loses context, rationale, and proof across sessions.
- Desired outcome: future agents can recover delivery intent, related knowledge artifacts, and validation evidence from project files.
- Non-goals or boundaries: this example does not prescribe a heavyweight documentation process for every small change.
- Exit Gate source: this Feature page, linked ADR, linked Lesson, and linked Evidence record.

## Current Status

Active example for demonstrating a project-level harness.

## Links

- [ADR-001](../decisions/ADR-001-markdown-as-source-of-truth.md)
- [LL-001](../lessons/LL-001-evidence-before-completion.md)
- [EV-001](../evidence/EV-001-project-harness-example.md)

## Acceptance Criteria

- [x] Feature page links related ADR, Lesson, and Evidence records.
- [x] Knowledge artifacts include required frontmatter.
- [x] `knowledge_check.py` can validate the example.

## Evidence

- [EV-001](../evidence/EV-001-project-harness-example.md)

## Next Step

Use this example as a reference when adding structured Harness docs to a real project.
