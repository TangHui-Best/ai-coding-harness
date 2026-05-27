---
id: EV-004
doc_kind: evidence
scope: feature
feature_refs: [docs/features/F002-canonical-harness-artifact-placement.md]
created: 2026-05-27
---

# EV-004: Hot Path Harness Constraints

## Commands

```text
python -m unittest tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_hot_path_constraints_remain_in_primary_skill_text
python -m unittest tests.test_skill_progressive_disclosure tests.test_closeout_convergence_contract tests.test_knowledge_check
python scripts\knowledge_check.py --root . --docs-path docs --strict
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
```

## Results

```text
Initial red test:
FAILED (failures=1)
AssertionError: 'Entry And Exit Gates' not found in using-harness/SKILL.md

After restoring hot-path constraints:
python -m unittest tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_hot_path_constraints_remain_in_primary_skill_text
Ran 1 test in 0.052s
OK

python -m unittest tests.test_skill_progressive_disclosure tests.test_closeout_convergence_contract tests.test_knowledge_check
Ran 26 tests in 1.437s
OK

python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 17 markdown file(s). Checked 11 knowledge artifact(s). Errors: 0. Warnings: 0.

python scripts\skill_metadata_check.py --root . --skills-path skills --strict
Scanned 11 skill file(s). Errors: 0. Warnings: 0.
```

## Artifacts

- `skills/using-harness/SKILL.md`
- `skills/harness-knowledge-capture/SKILL.md`
- `skills/harness-start-gate/SKILL.md`
- `skills/using-harness/assets/templates/FEATURE.md`
- `templates/FEATURE.md`
- `tests/test_skill_progressive_disclosure.py`
- `docs/features/F002-canonical-harness-artifact-placement.md`

## Notes

本次补丁保留 2026-05-26 的 progressive disclosure 和 closeout convergence 设计，但把会改变 agent 第一行动、写入位置、Feature 创建、完成声明权限和 patch churn 判断的硬约束恢复到主 `SKILL.md` 热路径中。Reference 继续承载细则和案例，脚本继续执行优先、失败或编辑时再读取源码。
