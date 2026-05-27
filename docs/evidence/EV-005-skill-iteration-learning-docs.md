---
id: EV-005
doc_kind: evidence
scope: feature
feature_refs: [docs/features/F002-canonical-harness-artifact-placement.md]
created: 2026-05-27
---

# EV-005: Skill Iteration Learning Docs

## Commands

```text
python scripts\knowledge_check.py --root . --docs-path docs --strict
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
python -m unittest discover -s tests
```

## Results

```text
python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 22 markdown file(s). Checked 15 knowledge artifact(s). Errors: 0. Warnings: 0.

python scripts\skill_metadata_check.py --root . --skills-path skills --strict
Scanned 11 skill file(s). Errors: 0. Warnings: 0.

python -m unittest discover -s tests
Ran 41 tests in 2.268s
OK

git diff --check
No output.
```

## Artifacts

- `docs/lessons/LL-002-skill-hot-path-constraints.md`
- `docs/decisions/ADR-006-skill-progressive-disclosure-boundary.md`
- `docs/guides/skill-iteration-lessons.md`
- `docs/features/F002-canonical-harness-artifact-placement.md`

## Notes

本 Evidence 记录 Harness skill 迭代复盘沉淀：将“渐进式加载不能隐藏热路径约束”的经验拆成 Lesson、ADR 和可分享 guide。验证完成后更新 Results。
