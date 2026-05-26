---
id: EV-003
doc_kind: evidence
scope: feature
feature_refs: [docs/features/F002-canonical-harness-artifact-placement.md]
created: 2026-05-26
---

# EV-003: Canonical Artifact Placement

## Commands

```text
python -m unittest tests.test_knowledge_check.KnowledgeCheckPlacementTests
python -m unittest tests.test_knowledge_check
python scripts\knowledge_check.py --root E:\Self-Project\Multi-Agent-Assi --docs-path docs --strict
python scripts\knowledge_check.py --root . --docs-path docs --strict
python -m unittest discover -s tests
python skills\using-harness\scripts\knowledge_check.py --root examples\project-harness --docs-path docs --strict
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
.\scripts\install.ps1 codex
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 codex
python C:\Users\HUAWEI\.codex\skills\using-harness\scripts\knowledge_check.py --root E:\Self-Project\Multi-Agent-Assi --docs-path docs --strict
```

## Results

```text
python -m unittest tests.test_knowledge_check.KnowledgeCheckPlacementTests
Ran 2 tests in 0.205s
OK

python -m unittest tests.test_knowledge_check
Ran 13 tests in 1.528s
OK

python scripts\knowledge_check.py --root E:\Self-Project\Multi-Agent-Assi --docs-path docs --strict
Errors: 6. Warnings: 0.
Detected:
- 3 evidence artifacts under docs/superpowers/evidence that must move to docs/evidence.
- 3 docs/superpowers/specs files with unsupported doc_kind 'spec'.

python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 17 markdown file(s). Checked 11 knowledge artifact(s). Errors: 0. Warnings: 0.

python -m unittest discover -s tests
Ran 40 tests in 2.214s
OK

python skills\using-harness\scripts\knowledge_check.py --root examples\project-harness --docs-path docs --strict
Scanned 4 markdown file(s). Checked 4 knowledge artifact(s). Errors: 0. Warnings: 0.

python scripts\skill_metadata_check.py --root . --skills-path skills --strict
Scanned 11 skill file(s). Errors: 0. Warnings: 0.

.\scripts\install.ps1 codex
Blocked by local PowerShell script execution policy.

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 codex
Installed Harness skills to C:\Users\HUAWEI\.codex\skills

python C:\Users\HUAWEI\.codex\skills\using-harness\scripts\knowledge_check.py --root E:\Self-Project\Multi-Agent-Assi --docs-path docs --strict
Errors: 6. Warnings: 0.
```

## Artifacts

- `scripts/knowledge_check.py`
- `skills/using-harness/scripts/knowledge_check.py`
- `tests/test_knowledge_check.py`
- `skills/using-harness/SKILL.md`
- `skills/harness-start-gate/SKILL.md`
- `skills/harness-knowledge-capture/references/artifact-decision-matrix.md`
- `docs/features/F002-canonical-harness-artifact-placement.md`
- `docs/decisions/ADR-005-canonical-harness-artifact-placement.md`

## Notes

本次修复针对 legacy `docs/superpowers/**` 与 Harness memory 的混用。目标项目 `E:\Self-Project\Multi-Agent-Assi` 在新 validator 下应明确失败，暴露 `docs/superpowers/evidence` placement 错误和 `doc_kind: spec` unsupported 错误。
