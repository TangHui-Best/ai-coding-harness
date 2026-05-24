---
id: LL-001
doc_kind: lesson
status: active
scope: project
feature_refs: [F001]
applies_to: [completion, review, handoff]
created: 2026-05-09
updated: 2026-05-09
---

# LL-001: Evidence Before Completion

## Pitfall

Agents may claim work is complete because the implementation looks plausible, even when no verification was run.

## Root Cause

Completion language is cheaper than verification unless the workflow requires evidence.

## Trigger

The risk appears before final responses, commits, PRs, reviews, and handoffs.

## Fix

Require every completion claim to identify where the evidence was recorded.

## Protection

Use `harness-knowledge-capture` before claiming completion and run the relevant verification command before making success claims.

## Source

Harness workflow design.

## Principle

Evidence before completion claims.
