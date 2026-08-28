---
id: EV-024
doc_kind: evidence
scope: project
feature_refs:
  - docs/features/F007-agentmentor-semantic-skill-routing.md
  - docs/features/F015-stop-only-hook-runtime.md
created: 2026-06-29
---

# EV-024: Install Script Verification

## Supports Claim

AgentMentor 安装脚本已增强为可验收的 Skills-only 安装入口：安装后自动验证正式 skill slug、清理旧公开 slug、检查 bundled validators/templates/hook runner；同时提供 `--verify` / `-Verify` 只读验证模式和目标目录环境变量覆盖，方便其它 Agent 在沙箱或 CI 中验证安装结果。

## Verification Scope

覆盖 `scripts/install.sh`、`scripts/install.ps1`、README、INSTALL、quickstart、`using-agentmentor` 安装提示，以及新增安装脚本测试。验证不覆盖真实 Codex Desktop personal plugin 安装、真实平台 Stop hook lifecycle dispatch，或不可用 Bash runtime 上的 Bash 脚本执行。

## Checks

```text
python -m unittest discover -s tests -p test_install_scripts.py
python -m unittest tests.test_skill_progressive_disclosure tests.test_skill_metadata_check tests.test_skill_breaking_rename
python scripts/skill_metadata_check.py --root . --skills-path skills --strict
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs --strict
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs --feature-index F007-agentmentor-semantic-skill-routing
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs --feature-index F015-stop-only-hook-runtime
git diff --check
```

## Results

- Pass: `python -m unittest discover -s tests -p test_install_scripts.py` ran 2 tests; PowerShell install/verify passed, Bash test skipped because local `bash.exe` points to an unusable WSL runtime.
- Pass: `python -m unittest tests.test_skill_progressive_disclosure tests.test_skill_metadata_check tests.test_skill_breaking_rename` ran 30 tests.
- Pass: `python scripts/skill_metadata_check.py --root . --skills-path skills --strict` scanned 12 skill files with 0 errors and 0 warnings.
- Pass: `python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs --strict` scanned 66 markdown files, checked 56 knowledge artifacts, with 0 errors and 0 warnings.
- Pass: `python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs --feature-index F007-agentmentor-semantic-skill-routing` returned 0 errors and 0 warnings.
- Pass: `python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs --feature-index F015-stop-only-hook-runtime` returned 0 errors and 0 warnings.
- Pass: `git diff --check` reported no whitespace errors; Git emitted line-ending conversion warnings for `scripts/install.ps1` and `scripts/install.sh`.

## Artifacts

- `scripts/install.sh`
- `scripts/install.ps1`
- `tests/test_install_scripts.py`
- `INSTALL.md`
- `docs/quickstart.md`
- `README.md`
- `README.en.md`
- `skills/using-agentmentor/SKILL.md`

## Limitations

本 Evidence 证明脚本的可验收安装路径和 PowerShell 实际执行路径；不证明当前机器的 Bash runtime 可用，也不证明 Codex Desktop personal plugin 或 Stop hook lifecycle 已真实触发。Hook runtime 仍需在目标项目中使用 `hook_diagnostics.py` 或 `.agentmentor/hook-events/events.jsonl` 作为独立证据。

## Notes

本次优化保持 F015 的边界：基础安装仍是 Skills-only；Hooks 是可选增强，不作为安装成功的前置条件。
