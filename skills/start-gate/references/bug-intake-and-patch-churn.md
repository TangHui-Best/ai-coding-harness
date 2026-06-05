# Bug Intake And Patch Churn

Use this reference when Start Gate is classifying a bugfix or follow-up patch.

## Bug Intake

Before implementation-oriented debugging for a non-tiny bugfix, ask:

1. Is this a tiny typo or local defect where project memory cannot change the fix?
2. Does the symptom mention an existing Feature ID, accepted behavior, prior fix, regression, validation miss, workflow, module boundary, or error likely to appear in docs?
3. Could fixing this without prior Feature, Evidence, ADR, or Lesson records cause another local patch against the wrong boundary?
4. If this belongs to a completed or accepted Feature, which Feature should receive the Patch History row after the fix?

If question 1 is no and Feature ownership or prior history is unknown, return `needs retrieval` before code search or edits.

Do not create a new Feature only because the owner is unknown. First attempt retrieval and attribution.

## Patch Churn Check

Before allowing another patch against an accepted or completed Feature, retrieve the Feature page and Evidence, then inspect `## Patch History`.

Ask:

1. Is this a new coherent change, or another patch in the same failure chain?
2. Does the patch reduce underlying complexity, or add another scenario-specific branch?
3. Are failures moving upstream toward an invariant or boundary problem?
4. Has `## Patch History` reached 3+ rows, or is there equivalent evidence of repeated validation misses?

If the Feature has 3+ Patch History rows and no `## Patch Churn Review`, do not return `ready`; return `needs vision gate`, `needs ADR`, or `needs retrieval` depending on missing context.
