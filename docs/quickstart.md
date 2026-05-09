# Quickstart

## Minimal Harness

Copy `templates/AGENTS.md` into your project and fill in:

- Project rules agents must follow.
- Verification commands.
- Evidence expectations.

This gives the project a shared operating surface outside a single prompt.

## Project Harness

When work spans multiple sessions or contributors, add:

```text
docs/BACKLOG.md
docs/features/
docs/decisions/
docs/lessons/
docs/evidence/
```

Use templates:

```text
templates/FEATURE.md
templates/ADR.md
templates/LESSON.md
templates/EVIDENCE.md
```

## Validate Knowledge Artifacts

Run:

```bash
python scripts/knowledge_check.py --root . --docs-path docs
```

Use strict mode for review or CI gates:

```bash
python scripts/knowledge_check.py --root . --docs-path docs --strict
```

## Stop Rule

Do not create Harness artifacts just to look disciplined.

Create the smallest artifact that prevents future confusion, repeated mistakes, or unverifiable completion.
