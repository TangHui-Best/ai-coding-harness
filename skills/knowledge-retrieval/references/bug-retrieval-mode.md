# Bug Retrieval Mode

Use this reference when Start Gate asks for Feature attribution before a non-tiny bugfix.

## Search Terms

Search with the smallest useful set:

- User symptom, expected behavior, error text, failing command, UI/workflow name, or validation message.
- Module, file, API, CLI command, screen, data model, or integration named by the report.
- Known Feature IDs, patch IDs such as `F010.2`, ADR IDs, Lesson IDs, and related PR or commit identifiers.
- Synonyms such as `bug`, `regression`, `follow-up`, `validation`, `Patch History`, `Patch Churn Review`, and domain-specific nouns.

## Attribution Steps

1. If a Feature is found, read it first and inspect `## Patch History`, `## Patch Churn Review`, related links, status, and Evidence.
2. Read linked or relevant Evidence, ADRs, Lessons, bug reports, discussions, and archive pointers before trusting a local code hypothesis.
3. Classify attribution as `existing Feature <path-or-stem>`, `none found`, `ambiguous`, or `stale/superseded`.
4. If attribution is ambiguous, name candidate Features and the missing fact needed to choose between them.
5. Return the attribution result to Start Gate or Knowledge Capture. Retrieval itself must not update Patch History.

If no Feature is found, say so explicitly. A negative retrieval result is still useful evidence.
