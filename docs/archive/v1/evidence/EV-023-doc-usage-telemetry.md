---
id: EV-023
doc_kind: evidence
scope: feature
feature_refs:
  - docs/features/F016-doc-usage-telemetry.md
created: 2026-06-28
---

# EV-023: Doc Usage Telemetry

## Supports Claim

F016 的最小文档使用观测机制已经落地：AgentMentor 现在可以在 `knowledge-retrieval` 和 `change-narrative` 中，对真实影响判断或叙事的文档调用脚本追加 usage JSONL 记录。

## Verification Scope

覆盖：root/bundled `usage_record.py`、usage JSONL 路径与 schema、doc_type / impact 校验、Git 用户文件名规范化、`.gitignore` usage 例外、`knowledge-retrieval` 和 `change-narrative` usage 规则、F016 Feature Index 本地条目。

不覆盖：真实长期统计报表、去重策略、文件分片、所有 Skill 的 usage 记录、自动判断文档是否“真正使用”、不同团队成员真实合并冲突概率。

## Checks

```text
python -m unittest tests.test_usage_record
python -m unittest tests.test_usage_record tests.test_skill_progressive_disclosure tests.test_skill_metadata_check
python scripts/usage_record.py --root . --doc docs/features/F016-doc-usage-telemetry.md --doc-type feature --task "implement doc usage telemetry" --impact changed_design --actor Test-Usage
python scripts/knowledge_check.py --root . --docs-path docs --strict
python scripts/knowledge_check.py --root . --docs-path docs --feature-index F016-doc-usage-telemetry
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict
git diff --check
```

## Results

- `python -m unittest tests.test_usage_record`: passed, 3 tests.
- `python -m unittest tests.test_usage_record tests.test_skill_progressive_disclosure tests.test_skill_metadata_check`: passed, 29 tests.
- `python scripts/usage_record.py --root . --doc docs/features/F016-doc-usage-telemetry.md --doc-type feature --task "implement doc usage telemetry" --impact changed_design --actor Test-Usage`: passed; generated `.agentmentor/usage/events/test-usage.jsonl`, which was deleted after verification because it was a non-real sample event.
- `python scripts/knowledge_check.py --root . --docs-path docs --strict`: passed, 66 markdown files scanned, 56 knowledge artifacts checked, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index F016-doc-usage-telemetry`: passed, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict`: passed, 12 skill files scanned, 0 errors, 0 warnings.
- `git diff --check`: passed; Git emitted the existing line-ending conversion warning for `.gitignore` but no whitespace errors.

## Artifacts

- `scripts/usage_record.py`
- `skills/using-agentmentor/scripts/usage_record.py`
- `tests/test_usage_record.py`
- `.gitignore`
- `skills/knowledge-retrieval/SKILL.md`
- `skills/change-narrative/SKILL.md`
- `skills/using-agentmentor/SKILL.md`
- `scripts/skill_metadata_check.py`
- `skills/using-agentmentor/scripts/skill_metadata_check.py`
- `docs/features/INDEX.md`
- `docs/features/F016-doc-usage-telemetry.md`
- `docs/evidence/EV-023-doc-usage-telemetry.md`

## Limitations

本 Evidence 证明最小 usage 记录能力和规则已经落地；不证明 usage 数据已经足够支撑归档、重命名、规则晋升或长期无使用分析。第一阶段刻意不做去重、不做分片、不做统计报表。

## Notes

本次测试命令会用 `--actor Test-Usage` 写入一条样例 usage event。它用于证明 `.agentmentor/usage/events/*.jsonl` 可以被生成并进入 Git 例外路径；该样例不代表真实文档使用统计。
