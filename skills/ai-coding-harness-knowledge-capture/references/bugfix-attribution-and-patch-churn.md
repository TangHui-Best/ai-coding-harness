# Bugfix Attribution And Patch Churn

Use this reference for non-tiny bugfixes, regressions, broken accepted behavior, repeated validation failures, or completed Feature follow-up fixes.

## Attribution

For every non-tiny bugfix, record one of:

- `existing Feature <id>`: retrieval found the Feature that owns the behavior.
- `none found after retrieval`: no Feature owner was found; record the negative retrieval result in Evidence or final closeout.
- `not triggered`: only for tiny local fixes where project memory cannot change the outcome.
- `ambiguous`: owner is unclear; completion is blocked or conditional unless the claim is limited to investigation.

When the owner is an existing completed, accepted, or previously delivered Feature, update that Feature's `## Patch History`.

## Patch History

Patch History rows are follow-up fix records on the original Feature, not new Feature documents.

Include:

- Patch id such as `F010.1`.
- Symptom.
- Root cause or suspected root cause.
- Verification.
- Whether the fix preserves or revises original intent.

Do not hide completed follow-up fixes only in a final response, commit message, or PR body when an existing Feature owns the behavior.

## Patch Churn Review

When a Feature reaches 3 `## Patch History` rows, `Fxxx.n` patch slices, or equivalent repeated validation misses, add `## Patch Churn Review` before another patch can be cleanly closed.

Patch Churn Review should record whether the pattern:

- passed as unrelated local fixes,
- routed to Vision Gate because the abstraction may be wrong,
- routed to ADR because a decision boundary changed,
- routed to Lesson because the failure mode can recur,
- or blocked completion.

## Evidence

For patch churn, Evidence must include the fix trajectory:

- What each relevant patch exposed.
- Which shared root cause was found or ruled out.
- Why another local patch is sufficient or insufficient.
- Whether final protection moved upstream to the right invariant, contract, or boundary.
