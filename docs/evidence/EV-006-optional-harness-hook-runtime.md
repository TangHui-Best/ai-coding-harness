---
id: EV-006
doc_kind: evidence
scope: feature
feature_refs: [docs/features/F003-optional-harness-hook-runtime.md]
created: 2026-05-30
---

# EV-006: Optional Harness Hook Runtime

## Scope

Verified the first optional Hook Runtime slice for F003: a bundled `harness_hook.py` runner, hard default `Stop` completion checks, non-default experimental `post-tool-use` runner mode, Codex/Claude Code/OpenCode example hook configs, Skill-only fallback documentation, metadata validation, and Harness knowledge validation.

## Commands

```text
python -m unittest tests.test_harness_hook
python -m unittest tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_optional_hook_runtime_resources_are_discoverable
python -m unittest tests.test_skill_metadata_check
python -m unittest discover -s tests
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
python scripts\knowledge_check.py --root . --docs-path docs --strict
```

## Results

Pass.

- `python -m unittest tests.test_harness_hook`: 9 tests passed.
- `python -m unittest tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_optional_hook_runtime_resources_are_discoverable`: 1 test passed.
- `python -m unittest tests.test_skill_metadata_check`: 1 test passed.
- `python -m unittest discover -s tests`: 53 tests passed.
- `python scripts\skill_metadata_check.py --root . --skills-path skills --strict`: scanned 11 skill files, 0 errors, 0 warnings.
- `python scripts\knowledge_check.py --root . --docs-path docs --strict`: scanned 23 Markdown files, checked 16 knowledge artifacts, 0 errors, 0 warnings.

## Harness Validation

`knowledge_check.py` command path and result:

```text
python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 23 markdown file(s). Checked 16 knowledge artifact(s). Errors: 0. Warnings: 0.
```

`skill_metadata_check.py` command path and result:

```text
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
Scanned 11 skill file(s). Errors: 0. Warnings: 0.
```

## Artifacts

- `skills/using-harness/hooks/harness_hook.py`
- `skills/using-harness/hooks/codex-hooks.example.json`
- `skills/using-harness/hooks/claude-settings.example.json`
- `skills/using-harness/hooks/opencode-plugin.example.ts`
- `tests/test_harness_hook.py`
- `tests/test_skill_metadata_check.py`
- `INSTALL.md`
- `docs/quickstart.md`
- `README.en.md`

## Notes

The hook runtime is optional. It fails open on runtime/configuration errors. Default examples wire only `Stop`, because `PostToolUse` is too fine-grained for multi-edit artifact updates and can slow ordinary editing. The `post-tool-use` runner mode remains available only for explicit experiments. `Stop` is the hard completion boundary for invalid or missing closeout blocks.
