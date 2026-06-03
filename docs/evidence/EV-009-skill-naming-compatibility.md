---
id: EV-009
doc_kind: evidence
scope: feature
feature_refs: [docs/features/F006-skill-naming-compatibility.md]
created: 2026-06-03
updated: 2026-06-03
---

# EV-009: AI Coding Harness Skill Rename

## Scope

验证 F006：AI Coding Harness 公开 skill slug 已从 `using-harness` / `harness-*` 硬切到 `ai-coding-harness` / `ai-coding-harness-*`；skill 标题、agent display name、安装提示和 session recovery 输出使用 `AI Coding Harness`；本机独立 Codex skills 已重新安装为新版本；validator、tests、knowledge check 和 hook wrapper 路径均使用新入口目录。后续会话验证发现 Codex personal plugin cache 仍可能由旧插件包重新生成，因此插件发布/卸载链路不在本 Evidence 中声明完成。

## Commands

```text
python -m unittest tests.test_skill_metadata_check
python -m unittest tests.test_skill_breaking_rename tests.test_skill_metadata_check
python -m unittest discover -s tests
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
python scripts\knowledge_check.py --root . --docs-path docs --strict
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 codex
python "$HOME\.codex\skills\ai-coding-harness\scripts\skill_metadata_check.py" --root . --skills-path skills --strict
python "$HOME\.codex\skills\ai-coding-harness\scripts\knowledge_check.py" --root . --docs-path docs --strict
PowerShell check for local skill headings and `personal/harness` cache absence
PowerShell check after another Codex session recreated `personal/harness` cache
```

## Results

- `python -m unittest tests.test_skill_breaking_rename`: first run failed as expected before rename because 11 formal directories were missing and 11 legacy directories remained.
- `python -m unittest tests.test_skill_breaking_rename tests.test_harness_hook tests.test_skill_metadata_check`: 26 tests passed.
- `python -m unittest discover -s tests`: 78 tests passed.
- `python scripts\skill_metadata_check.py --root . --skills-path skills --strict`: scanned 11 skill files, 0 errors, 0 warnings.
- `python scripts\knowledge_check.py --root . --docs-path docs --strict`: scanned 36 markdown files, checked 29 knowledge artifacts, 0 errors, 0 warnings.
- `.\scripts\install.ps1 codex`: blocked by local PowerShell execution policy before script execution.
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 codex`: installed AI Coding Harness skills to `C:\Users\HUAWEI\.codex\skills`.
- Local Codex skills after reinstall: 11 `ai-coding-harness*` directories present; 0 `using-harness` / `harness-*` legacy directories present.
- Installed skill headings after reinstall: all 11 headings use `# AI Coding Harness...`.
- Codex personal plugin cache cleanup: `C:\Users\HUAWEI\.codex\plugins\cache\personal\harness` can be removed manually, but another Codex session recreated the same old cache from plugin source.
- Recreated plugin cache inspection: `personal_harness_cache=present`; cache contains `skills\using-harness`, `skills\harness-*`, `# Harness ...` headings, and `display_name: "Harness Delegation Gate"`.
- Active legacy public-name scan: no old public skill names, display titles, session recovery headings, or validation headings remain outside intentional negative test fixtures.
- Installed `skill_metadata_check.py`: scanned 11 skill files, 0 errors, 0 warnings.
- Installed `knowledge_check.py`: scanned 36 markdown files, checked 29 knowledge artifacts, 0 errors, 0 warnings.

## AI Coding Harness Validation

`knowledge_check.py` command path and result:

```text
python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 36 markdown file(s). Checked 29 knowledge artifact(s). Errors: 0. Warnings: 0.
```

`skill_metadata_check.py` command path and result:

```text
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
Scanned 11 skill file(s). Errors: 0. Warnings: 0.
```

Installed skill validator command path and result:

```text
python "$HOME\.codex\skills\ai-coding-harness\scripts\skill_metadata_check.py" --root . --skills-path skills --strict
Scanned 11 skill file(s). Errors: 0. Warnings: 0.
```

Installed knowledge validator command path and result:

```text
python "$HOME\.codex\skills\ai-coding-harness\scripts\knowledge_check.py" --root . --docs-path docs --strict
Scanned 36 markdown file(s). Checked 29 knowledge artifact(s). Errors: 0. Warnings: 0.
```

## Artifacts

- `docs/features/F006-skill-naming-compatibility.md`
- `docs/decisions/ADR-007-ai-coding-harness-skill-naming-compatibility.md`
- `docs/evidence/EV-009-skill-naming-compatibility.md`
- `skills/ai-coding-harness/SKILL.md`
- `skills/ai-coding-harness-start-gate/SKILL.md`
- `skills/ai-coding-harness-knowledge-capture/SKILL.md`
- `README.md`
- `README.en.md`
- `INSTALL.md`
- `docs/skill-index.md`
- `scripts/skill_metadata_check.py`
- `skills/ai-coding-harness/scripts/skill_metadata_check.py`
- `tests/test_skill_metadata_check.py`
- `tests/test_skill_breaking_rename.py`

## Known Limitation

`scripts/install.ps1 codex` updates `C:\Users\HUAWEI\.codex\skills`, not the Codex personal plugin package source. If Codex has a personal plugin named `harness` installed, the app can recreate `C:\Users\HUAWEI\.codex\plugins\cache\personal\harness\...` with old skill slugs and headings. That explains why another new session may still show or use `Harness Skill` wording even after the independent local skills directory is correct.

Required follow-up: uninstall the old personal plugin or republish/reinstall the plugin package with `ai-coding-harness-*` skills and an updated plugin manifest.

## Notes

本迭代最终采用用户确认的 breaking rename，不保留旧 skill slug 兼容。内部脚本名 `harness_hook.py`、`harness_closeout_check.py` 暂不重命名，因为它们不是公开 skill slug，且 hook runtime 风险应单独评估。仓库 active skills 和本机独立 skills 中已无旧 `using-harness` / `harness-*` 安装目标；旧称呼只保留在 ADR/F006/EV 的迁移背景说明、测试反例和待处理的插件缓存链路描述中。

实现过程中曾出现一次机械替换污染：新建的 breaking rename 测试常量被替换成 `ai-coding-ai-coding-harness-*`。Root cause 是批量替换没有排除测试中的目标常量；修复方式是手动恢复测试数据，并用该测试锁定最终目录/frontmatter 契约。
