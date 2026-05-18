# Project Harness

A project-level harness adds durable memory and gates:

- backlog or active work index
- feature aggregation pages
- ADRs
- lessons
- evidence records
- vision and evidence gates
- document lifecycle rules

Use this when the project lasts across multiple sessions, features, or contributors.

This example includes a small set of structured docs under `docs/`:

```text
docs/features/F001-ai-coding-harness.md
docs/decisions/ADR-001-markdown-as-source-of-truth.md
docs/lessons/LL-001-evidence-before-completion.md
docs/evidence/EV-001-project-harness-example.md
```

Validate it from the repository root:

```bash
python skills/using-harness/scripts/knowledge_check.py --root examples/project-harness --docs-path docs
```
