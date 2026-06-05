---
id: EV-010
doc_kind: evidence
scope: feature
feature_refs: [docs/features/F007-agentmentor-semantic-skill-routing.md]
created: 2026-06-04
updated: 2026-06-04
---

# EV-010: AgentMentor Semantic Skill Routing

## Scope

验证 F007：仓库内公开 skill 命名、插件身份、hook runner、session recovery 状态目录、metadata validator 和 readiness 触发描述已迁到 AgentMentor 目标形态。

## Commands

```text
python -m unittest tests.test_skill_breaking_rename tests.test_skill_metadata_check tests.test_skill_progressive_disclosure tests.test_harness_hook tests.test_harness_closeout_check tests.test_hook_diagnostics tests.test_delegation_gate_policy tests.test_closeout_convergence_contract tests.test_harness_bugfix_routing_contract
python -m unittest discover -s tests
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
python scripts\knowledge_check.py --root . --docs-path docs --strict
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 codex
python C:\Users\HUAWEI\.codex\skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict
python C:\Users\HUAWEI\.codex\skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
python C:\Users\HUAWEI\.codex\plugins\cache\personal\agentmentor\0.2.0+codex.20260604093000\skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict
python C:\Users\HUAWEI\.codex\plugins\cache\personal\agentmentor\0.2.0+codex.20260604093000\skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
python C:\Users\HUAWEI\.codex\plugins\cache\personal\agentmentor\0.2.0+codex.20260604093000\skills\using-agentmentor\scripts\hook_diagnostics.py codex --project-root .
```

## Results

- Targeted AgentMentor rename and hook suite: Pass, 69 tests passed.
- Full unittest discovery: Pass, 82 tests passed.
- `skill_metadata_check.py --strict`: Pass, scanned 11 skill files, 0 errors, 0 warnings.
- `knowledge_check.py --strict`: Pass, scanned 39 markdown files, checked 32 knowledge artifacts, 0 errors, 0 warnings.
- `scripts/install.ps1 codex`: Pass, installed AgentMentor skills to `C:\Users\HUAWEI\.codex\skills`.
- Local Codex skills: Pass, only the 11 current AgentMentor skill directories remain among this suite; old `ai-coding-harness*` directories were removed.
- Codex config: Pass, `[plugins."agentmentor@personal"]` is enabled; old `ai-coding-harness@personal` plugin config and hook trust entries were removed.
- Personal plugin source/cache: Pass, source is `C:\Users\HUAWEI\plugins\agentmentor`; cache is `C:\Users\HUAWEI\.codex\plugins\cache\personal\agentmentor\0.2.0+codex.20260604093000`; old `ai-coding-harness` source/cache removed.
- Installed skill validator: Pass, scanned 11 skill files, 0 errors, 0 warnings.
- Installed knowledge validator: Pass, scanned 39 markdown files, checked 32 knowledge artifacts, 0 errors, 0 warnings.
- Personal cache skill validator: Pass, scanned 11 skill files, 0 errors, 0 warnings.
- Personal cache knowledge validator: Pass, scanned 39 markdown files, checked 32 knowledge artifacts, 0 errors, 0 warnings.
- Personal cache hook diagnostics: Pass, runner smoke passed; Codex compaction trigger evidence was not applicable because no compacted/context_compacted events existed for this project root.

## AgentMentor Validation

```text
python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 39 markdown file(s). Checked 32 knowledge artifact(s). Errors: 0. Warnings: 0.

python C:\Users\HUAWEI\.codex\skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 39 markdown file(s). Checked 32 knowledge artifact(s). Errors: 0. Warnings: 0.

python C:\Users\HUAWEI\.codex\plugins\cache\personal\agentmentor\0.2.0+codex.20260604093000\skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 39 markdown file(s). Checked 32 knowledge artifact(s). Errors: 0. Warnings: 0.
```

## Artifacts

- `skills/using-agentmentor/SKILL.md`
- `skills/readiness-dashboard/SKILL.md`
- `.codex-plugin/plugin.json`
- `hooks/run-agentmentor-hook.cmd`
- `skills/using-agentmentor/hooks/agentmentor_hook.py`
- `scripts/skill_metadata_check.py`
- `tests/test_skill_breaking_rename.py`
- `tests/test_skill_metadata_check.py`
- `tests/test_skill_progressive_disclosure.py`
- `docs/lessons/LL-008-skill-naming-affects-discovery-scope.md`

## Notes

本轮不是“只把 AI Coding Harness 改成 AgentMentor”的品牌替换，而是恢复 discovery 的结构：suite 身份由插件和入口表达，workflow 能力由短 slug 表达。
