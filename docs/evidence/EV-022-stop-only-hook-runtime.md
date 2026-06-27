---
id: EV-022
doc_kind: evidence
scope: feature
feature_refs:
  - docs/features/F015-stop-only-hook-runtime.md
created: 2026-06-27
---

# EV-022: Stop Only Hook Runtime

## Supports Claim

F015 的 Stop-only hook runtime 收敛已经落地：默认 hook runner、平台示例、diagnostics、现役文档和测试不再把 `pre-compact` / `session-start` session recovery 作为当前能力。

## Verification Scope

覆盖：hook runner event choices、Codex/Claude/OpenCode hook examples、root/nested Codex hook configs、hook diagnostics、README/INSTALL/quickstart/using-agentmentor 文档、F003/F005/F015 Feature 状态、Feature Index 本地召回。

不覆盖：未来是否彻底移除 Stop hook、历史 Evidence/Lesson 中关于 session recovery 的历史记录、真实平台 hook runtime dispatch。

## Checks

```text
python -m unittest tests.test_harness_hook
python -m unittest tests.test_hook_diagnostics
python -m unittest tests.test_skill_progressive_disclosure
python -m unittest tests.test_knowledge_check tests.test_harness_hook tests.test_hook_diagnostics tests.test_skill_progressive_disclosure
python scripts/knowledge_check.py --root . --docs-path docs --strict
python scripts/knowledge_check.py --root . --docs-path docs --feature-index F015-stop-only-hook-runtime
python scripts/knowledge_check.py --root . --docs-path docs --feature-index F005-session-recovery-hooks
python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all
python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict
python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict
git diff --check
```

## Results

- `python -m unittest tests.test_harness_hook`: passed, 12 tests.
- `python -m unittest tests.test_hook_diagnostics`: passed, 2 tests.
- `python -m unittest tests.test_skill_progressive_disclosure`: passed, 22 tests.
- `python -m unittest tests.test_knowledge_check tests.test_harness_hook tests.test_hook_diagnostics tests.test_skill_progressive_disclosure`: passed, 71 tests.
- `python scripts/knowledge_check.py --root . --docs-path docs --strict`: passed, 64 markdown files scanned, 54 knowledge artifacts checked, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index F015-stop-only-hook-runtime`: passed, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index F005-session-recovery-hooks`: passed, 0 errors, 0 warnings.
- `python scripts/knowledge_check.py --root . --docs-path docs --feature-index-all`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --strict`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\knowledge_check.py --root . --docs-path docs --feature-index F015-stop-only-hook-runtime`: passed, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\skill_metadata_check.py --root . --skills-path skills --strict`: passed, 12 skill files scanned, 0 errors, 0 warnings.
- `git diff --check`: passed; Git emitted line-ending conversion warnings for JSON/TypeScript files but no whitespace errors.

## Artifacts

- `skills/using-agentmentor/hooks/agentmentor_hook.py`
- `skills/using-agentmentor/hooks/codex-hooks.example.json`
- `skills/using-agentmentor/hooks/claude-settings.example.json`
- `skills/using-agentmentor/hooks/opencode-plugin.example.ts`
- `hooks.json`
- `hooks/hooks.json`
- `skills/using-agentmentor/scripts/hook_diagnostics.py`
- `tests/test_harness_hook.py`
- `tests/test_hook_diagnostics.py`
- `tests/test_skill_progressive_disclosure.py`
- `skills/using-agentmentor/SKILL.md`
- `README.md`
- `INSTALL.md`
- `docs/quickstart.md`
- `docs/features/F003-optional-harness-hook-runtime.md`
- `docs/features/F005-session-recovery-hooks.md`
- `docs/features/F015-stop-only-hook-runtime.md`
- `docs/evidence/EV-022-stop-only-hook-runtime.md`

## Limitations

本 Evidence 证明当前仓库能力已收敛为 Stop-only；不证明真实 Codex / Claude Code / OpenCode runtime 一定触发 Stop hook。平台实际触发仍需安装后的 runtime trace 或平台诊断证明。

## Notes

历史 F005、EV-008、LL-005、LL-006、LL-007 中保留 session recovery 的设计和踩坑记录。这些记录不再代表当前默认能力；当前事实源是 F015。
