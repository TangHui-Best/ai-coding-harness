---
id: EV-011
doc_kind: evidence
scope: feature
feature_refs: [docs/features/F008-spec-drift-guardrails.md]
created: 2026-06-08
updated: 2026-06-08
---

# EV-011: Spec Drift Guardrails

## Scope

验证 F008：AgentMentor 已新增 Spec Drift Guardrails，并能在旧 spec / acceptance criteria 被真实案例、验证失败或用户反馈挑战时，把 Agent 从继续局部打补丁分流到 `spec-drift` 判断。

## Commands

```text
python -m unittest tests.test_spec_drift_guardrails tests.test_skill_breaking_rename
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict
python -m unittest
python -m unittest discover -s tests
# pre-Evidence check
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
# post-Evidence check
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
```

## Results

- Targeted Spec Drift tests: Pass, 10 tests passed.
- Root `skill_metadata_check.py --strict`: Pass, scanned 12 skill files, 0 errors, 0 warnings.
- Bundled `using-agentmentor/scripts/skill_metadata_check.py --strict`: Pass, scanned 12 skill files, 0 errors, 0 warnings.
- `python -m unittest`: Did not discover tests in this repository layout, 0 tests ran; replaced by explicit discovery.
- Full unittest discovery: Pass, 89 tests passed.
- Pre-Evidence `knowledge_check.py --strict`: Pass, scanned 40 markdown files, checked 33 knowledge artifacts, 0 errors, 0 warnings.
- Post-Evidence `knowledge_check.py --strict`: Pass, scanned 42 markdown files, checked 35 knowledge artifacts, 0 errors, 0 warnings.

## AgentMentor Validation

```text
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 42 markdown file(s). Checked 35 knowledge artifact(s). Errors: 0. Warnings: 0.
```

## Artifacts

- `skills/spec-drift/SKILL.md`
- `skills/spec-drift/references/spec-drift-decision-rules.md`
- `skills/using-agentmentor/SKILL.md`
- `skills/start-gate/SKILL.md`
- `skills/start-gate/references/start-gate-decision-rules.md`
- `skills/start-gate/references/bug-intake-and-patch-churn.md`
- `skills/vision-gate/SKILL.md`
- `scripts/skill_metadata_check.py`
- `skills/using-agentmentor/scripts/skill_metadata_check.py`
- `tests/test_spec_drift_guardrails.py`
- `tests/test_skill_breaking_rename.py`
- `README.md`
- `README.en.md`
- `INSTALL.md`
- `docs/skill-index.md`

## Notes

本轮增强刻意保持克制：Start Gate 只识别并分流 Spec Drift 风险；Vision Gate 继续守护原始目标；Spec Drift 只判断 spec 是否仍可信。AGENTS 规则仍由用户手动复制和维护，避免把 AgentMentor 从辅助治理能力变成侵入式项目配置接管。
