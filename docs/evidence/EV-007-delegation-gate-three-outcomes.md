---
id: EV-007
doc_kind: evidence
scope: feature
feature_refs: [docs/features/F004-delegation-gate-three-outcomes.md]
created: 2026-05-30
---

# EV-007: Delegation Gate Three Outcomes

## Scope

Verified F004: Delegation Gate now uses exactly three main-agent decisions, and the dependent Start Gate, Vision Gate, Readiness Dashboard, routing references, ADR link, and regression tests are aligned with that model.

## Commands

```text
python -m unittest tests.test_delegation_gate_policy
python -m unittest discover -s tests
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
python scripts\knowledge_check.py --root . --docs-path docs --strict
```

## Results

- `python -m unittest tests.test_delegation_gate_policy`: 5 tests passed.
- `python -m unittest discover -s tests`: 54 tests passed.
- `python scripts\skill_metadata_check.py --root . --skills-path skills --strict`: scanned 11 skill files, 0 errors, 0 warnings.
- `python scripts\knowledge_check.py --root . --docs-path docs --strict`: scanned 26 Markdown files, checked 19 knowledge artifacts, 0 errors, 0 warnings.
- `python scripts\knowledge_check.py --root . --docs-path docs --strict` after adding LL-003: scanned 27 Markdown files, checked 20 knowledge artifacts, 0 errors, 0 warnings.

## Harness Validation

`knowledge_check.py` command path and result:

```text
python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 27 markdown file(s). Checked 20 knowledge artifact(s). Errors: 0. Warnings: 0.
```

## Artifacts

- `skills/harness-delegation-gate/SKILL.md`
- `skills/harness-start-gate/SKILL.md`
- `skills/harness-readiness-dashboard/SKILL.md`
- `skills/harness-readiness-dashboard/references/readiness-checks.md`
- `skills/harness-vision-gate/SKILL.md`
- `skills/using-harness/SKILL.md`
- `skills/using-harness/references/routing.md`
- `docs/decisions/ADR-003-explicit-delegation-decision-before-complex-work.md`
- `docs/features/F004-delegation-gate-three-outcomes.md`
- `docs/lessons/LL-003-gate-outcomes-encode-next-action.md`
- `tests/test_delegation_gate_policy.py`

## Notes

The primary decision is now the main agent's judgment, not a user-authorization state. `delegate` may still require a platform-specific permission step before actual dispatch, but that step is no longer a separate Delegation Gate outcome.

LL-003 captures the reusable lesson from this change: gate outcomes should encode the next main-agent action, while permission source, target, reason, and residual risk belong in separate fields.
