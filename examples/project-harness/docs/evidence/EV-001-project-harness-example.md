---
id: EV-001
doc_kind: evidence
scope: project
feature_refs: [docs/features/F001-using-agentmentor.md]
created: 2026-05-09
---

# EV-001: Project Harness Example

## Commands

```bash
python skills/using-agentmentor/scripts/knowledge_check.py --root examples/project-harness --docs-path docs
```

## Results

Expected result: zero errors and zero warnings.

## Artifacts

- Feature: `docs/features/F001-using-agentmentor.md`
- ADR: `docs/decisions/ADR-001-markdown-as-source-of-truth.md`
- Lesson: `docs/lessons/LL-001-evidence-before-completion.md`

## Notes

This example demonstrates the minimum relationship between Feature, ADR, Lesson, and Evidence records.
