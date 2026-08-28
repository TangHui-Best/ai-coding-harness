---
id: EV-018
doc_kind: evidence
scope: feature
feature_refs:
  - docs/features/F011-lesson-case-protection-governance.md
created: 2026-06-27
---

# EV-018: Lesson Case Protection Governance

## Supports Claim

This Evidence supports the completion or validation claim for EV-018: Lesson Case Protection Governance.


## Verification Scope

This Evidence covers the checks and results recorded below.

## Checks
```text
rg -n "^## Trigger|^## Fix" docs/lessons templates/LESSON.md skills/using-agentmentor/assets/templates/LESSON.md
python -m unittest tests.test_knowledge_check
python scripts/knowledge_check.py --root . --docs-path docs --strict
python scripts/knowledge_check.py --root . --docs-path docs --feature-index F011-lesson-case-protection-governance
python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --feature-index F011-lesson-case-protection-governance
python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict
git diff --check
```

## Results

- `rg -n "^## Trigger|^## Fix" docs/lessons templates/LESSON.md skills/using-agentmentor/assets/templates/LESSON.md`: no matches; old required Lesson headings are not present in Lesson docs or templates.
- `python -m unittest tests.test_knowledge_check`: passed, 27 tests.
- `python scripts/knowledge_check.py --root . --docs-path docs --strict`: passed, 55 markdown files scanned, 45 knowledge artifacts checked, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index F011-lesson-case-protection-governance`: passed, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --feature-index F011-lesson-case-protection-governance`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict`: passed, 12 skill files scanned, 0 errors, 0 warnings.
- `git diff --check`: passed.

## Artifacts

- `templates/LESSON.md`
- `skills/using-agentmentor/assets/templates/LESSON.md`
- `scripts/knowledge_check.py`
- `skills/using-agentmentor/scripts/knowledge_check.py`
- `tests/test_knowledge_check.py`
- `skills/knowledge-capture/SKILL.md`
- `skills/knowledge-capture/references/artifact-decision-matrix.md`
- `skills/incident-learning/SKILL.md`
- `docs/lessons/LL-001-patch-churn-zero-base-review.md`
- `docs/lessons/LL-002-skill-hot-path-constraints.md`
- `docs/lessons/LL-003-gate-outcomes-encode-next-action.md`
- `docs/lessons/LL-004-codex-hook-plugin-schema-before-cache.md`
- `docs/lessons/LL-005-session-recovery-must-be-session-scoped.md`
- `docs/lessons/LL-006-platform-hooks-native-context-channels.md`
- `docs/lessons/LL-007-hook-runtime-needs-lifecycle-evidence.md`
- `docs/lessons/LL-008-skill-naming-affects-discovery-scope.md`
- `docs/features/INDEX.md`
- `docs/features/F011-lesson-case-protection-governance.md`
- `docs/evidence/EV-018-lesson-case-protection-governance.md`

## Limitations

This Evidence does not prove behavior outside the verification scope recorded above.

## Notes
本次治理把 Lesson 定位为客观失败案例、当时解决方式、可迁移失败模式和防复发机制。文件名承担粗召回职责；正文不把 Recall Cues 当主召回机制。
