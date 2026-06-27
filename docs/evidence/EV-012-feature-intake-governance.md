---
id: EV-012
doc_kind: evidence
scope: feature
feature_refs:
  - docs/features/F009-feature-intake-governance.md
created: 2026-06-11
---

# EV-012: Feature Intake Governance

## Supports Claim

This Evidence supports the completion or validation claim for EV-012: Feature Intake Governance.


## Verification Scope

This Evidence covers the checks and results recorded below.

## Checks
```powershell
python -m unittest ai-coding-harness.tests.test_knowledge_check.KnowledgeCheckFeatureGovernanceTests
python -m unittest ai-coding-harness.tests.test_knowledge_check
python ai-coding-harness\scripts\knowledge_check.py --root ai-coding-harness --docs-path docs --strict
python ai-coding-harness\scripts\skill_metadata_check.py --root ai-coding-harness --skills-path skills --strict
python ai-coding-harness\skills\using-agentmentor\scripts\knowledge_check.py --root ai-coding-harness --docs-path docs --strict
```

## Results

- Feature governance tests: `Ran 4 tests ... OK`.
- Full knowledge check unit tests: `Ran 17 tests ... OK`.
- Root strict knowledge check: `Scanned 41 markdown file(s). Checked 34 knowledge artifact(s). Errors: 0. Warnings: 0.`
- Skill metadata strict check: `Scanned 12 skill file(s). Errors: 0. Warnings: 0.`
- Bundled strict knowledge check: `Scanned 41 markdown file(s). Checked 34 knowledge artifact(s). Errors: 0. Warnings: 0.`

## Artifacts

- `templates/FEATURE.md`
- `skills/using-agentmentor/assets/templates/FEATURE.md`
- `scripts/knowledge_check.py`
- `skills/using-agentmentor/scripts/knowledge_check.py`
- `tests/test_knowledge_check.py`
- `skills/start-gate/SKILL.md`
- `skills/knowledge-capture/SKILL.md`
- `skills/knowledge-capture/references/artifact-decision-matrix.md`
- `skills/knowledge-capture/references/bugfix-attribution-and-patch-churn.md`
- `docs/features/F001` through `F008` migrated to the stricter Feature shape.

## Limitations

This Evidence does not prove behavior outside the verification scope recorded above.

## Notes
This change intentionally borrows the discipline of Superpowers brainstorming but keeps ownership inside AgentMentor. Superpowers can still produce linked specs or plans, but AgentMentor Feature Intake is now the gate that decides whether an idea is clear enough to enter long-lived project memory.
