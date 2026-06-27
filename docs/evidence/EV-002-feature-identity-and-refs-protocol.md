---
id: EV-002
doc_kind: evidence
scope: project
feature_refs: []
created: 2026-05-24
---

# EV-002: Path-Based Feature References

## Supports Claim

This Evidence supports the completion or validation claim for EV-002: Path-Based Feature References.


## Verification Scope

This Evidence covers the checks and results recorded below.

## Checks
```text
python -m unittest tests.test_knowledge_check
python -m unittest discover -s tests
python scripts\knowledge_check.py --root . --docs-path docs --strict
python skills\using-agentmentor\scripts\knowledge_check.py --root examples\project-harness --docs-path docs --strict
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
```

## Results

```text
python -m unittest tests.test_knowledge_check
Ran 11 tests in 1.277s
OK

python -m unittest discover -s tests
Ran 26 tests in 1.908s
OK

python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 14 markdown file(s). Checked 8 knowledge artifact(s). Errors: 0. Warnings: 0.

python skills\using-agentmentor\scripts\knowledge_check.py --root examples\project-harness --docs-path docs --strict
Scanned 4 markdown file(s). Checked 4 knowledge artifact(s). Errors: 0. Warnings: 0.

python scripts\skill_metadata_check.py --root . --skills-path skills --strict
Scanned 11 skill file(s). Errors: 0. Warnings: 0.
```

## Artifacts

- `scripts/knowledge_check.py`
- `skills/using-agentmentor/scripts/knowledge_check.py`
- `templates/FEATURE.md`
- `templates/ADR.md`
- `templates/LESSON.md`
- `templates/EVIDENCE.md`
- `skills/using-agentmentor/assets/templates/`
- `docs/decisions/ADR-004-feature-identity-and-refs-protocol.md`
- `tests/test_knowledge_check.py`

## Limitations

This Evidence does not prove behavior outside the verification scope recorded above.

## Notes
The 2026-05-25 red phase failed because `knowledge_check.py` still accepted only `FNNN` / `FP-*` references and treated duplicate short Feature ids as duplicate identities.

The green phase made `feature_refs` resolve Feature paths and file stems directly, warn on bare short ids, reject ambiguous bare short ids, and remove alias/canonicalization validation from the default workflow.
