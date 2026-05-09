---
id: ADR-001
doc_kind: adr
status: accepted
scope: project
feature_ids: [F001]
decision_area: knowledge-source
created: 2026-05-09
updated: 2026-05-09
---

# ADR-001: Markdown As Source Of Truth

## Context

AI-assisted development needs durable project memory that can be reviewed by humans, edited in Git, and recovered by future agents.

## Decision

Use Markdown documents as the source of truth for Harness knowledge artifacts. Search indexes and summaries may exist, but they are compiled outputs.

## Alternatives

- Store knowledge only in chat history: rejected because future sessions and teammates cannot reliably recover it.
- Store knowledge only in a database: rejected for the minimal harness because it adds operational complexity before the project needs it.

## Consequences

The project gets readable, reviewable, versioned knowledge. The trade-off is that teams need lightweight conventions and validation to keep the documents consistent.

## Evidence

This example links Feature, ADR, Lesson, and Evidence documents and can be checked with `scripts/knowledge_check.py`.
