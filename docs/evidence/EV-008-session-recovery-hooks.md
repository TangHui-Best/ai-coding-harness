---
id: EV-008
doc_kind: evidence
scope: feature
feature_refs: [docs/features/F005-session-recovery-hooks.md]
created: 2026-05-30
updated: 2026-05-31
---

# EV-008: Session Recovery Hooks

## Scope

Verified F005: the optional Harness hook runner now supports `pre-compact` and `session-start`, writes same-session recovery snapshots under `.harness/session-recovery/by-session/`, updates `latest.md` only for manual inspection, exposes Claude Code and Codex `SessionStart` additional context with the platform hook output shape, avoids cross-session recovery injection, and preserves the no-default-`PostToolUse` constraint.

## Commands

```text
python -m unittest tests.test_harness_hook
python -m unittest tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_optional_hook_runtime_resources_are_discoverable tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_default_hook_examples_do_not_wire_post_tool_use tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_default_hook_examples_wire_session_recovery_hooks
python -m unittest discover -s tests
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
python scripts\knowledge_check.py --root . --docs-path docs --strict
```

## Results

- `python -m unittest tests.test_harness_hook`: 16 tests passed.
- Targeted progressive-disclosure hook tests: 3 tests passed.
- `python -m unittest discover -s tests`: 63 tests passed after F005.1.
- `python scripts\skill_metadata_check.py --root . --skills-path skills --strict`: scanned 11 skill files, 0 errors, 0 warnings.
- `python scripts\knowledge_check.py --root . --docs-path docs --strict`: scanned 30 Markdown files, checked 23 knowledge artifacts, 0 errors, 0 warnings.

## Harness Validation

`knowledge_check.py` command path and result:

```text
python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 29 markdown file(s). Checked 22 knowledge artifact(s). Errors: 0. Warnings: 0.
```

F005.1 rerun:

```text
python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 30 markdown file(s). Checked 23 knowledge artifact(s). Errors: 0. Warnings: 0.
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
- `skills/using-harness/SKILL.md`
- `INSTALL.md`
- `docs/quickstart.md`
- `docs/features/F005-session-recovery-hooks.md`
- `tests/test_harness_hook.py`
- `tests/test_skill_progressive_disclosure.py`

## Notes

Session recovery is runtime context, not canonical Harness memory. The automatic injection snapshot is intentionally written under `.harness/session-recovery/by-session/<session_id>.md` so only the same session can recover from compaction. `.harness/session-recovery/latest.md` remains a manual inspection pointer and must not be injected into unrelated new sessions.

The follow-up learning from F005.1 is captured in [LL-005 Session Recovery Must Be Session-Scoped](../lessons/LL-005-session-recovery-must-be-session-scoped.md).

The OpenCode example maps its `session.created` plugin event to the normalized Harness `session-start` runner event, and maps `experimental.session.compacting` to `pre-compact`.
