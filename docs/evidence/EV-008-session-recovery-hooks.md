---
id: EV-008
doc_kind: evidence
scope: feature
feature_refs: [docs/features/F005-session-recovery-hooks.md]
created: 2026-05-30
updated: 2026-06-07
---

# EV-008: Session Recovery Hooks

## Supports Claim

This Evidence supports the completion or validation claim for EV-008: Session Recovery Hooks.


## Verification Scope
Verified F005: the optional AgentMentor hook runner now supports `pre-compact` and `session-start`, writes same-session recovery snapshots under `.agentmentor/session-recovery/by-session/`, updates `latest.md` only for manual inspection, exposes Claude Code and Codex `SessionStart` additional context with the platform hook output shape, injects OpenCode compaction context through `output.context`, keeps Codex `PreCompact` broad enough to run on observed context compaction events, avoids cross-session recovery injection, and preserves the no-default-`PostToolUse` constraint.

F005.4 adds a diagnostic guardrail because real Codex Desktop sessions can record `compacted/context_compacted` without observable Harness `PreCompact` execution or recovery artifacts. The diagnostic distinguishes runner writability from platform lifecycle proof.

F005.5 adds hook runtime trace, root-level plus nested Codex `hooks.json`, Codex hook feature-gate checks, and removes unproven Codex command working-directory assumptions from the example config after Codex Settings showed all three AgentMentor hooks but no session produced observable `Stop`, `PreCompact`, or `SessionStart` execution.

F005.6 corrects the OpenCode Stop adapter after checking the current `@opencode-ai/plugin` `1.15.13` contract. `experimental.session.compacting` remains a direct trigger hook with `output.context`, but `session.idle` is a global SDK event and must be handled through the plugin `event(input)` hook. Because the idle event only carries `sessionID`, the adapter now fetches recent session messages through the OpenCode SDK and passes the latest assistant text to Harness as `last_assistant_message`.

F005.7 corrects the Codex Windows command boundary after real UI evidence showed every AgentMentor hook exiting with `code 1`. The failing command shape was reproduced by running the old `commandWindows` value through PowerShell: `%PLUGIN_ROOT%` was not expanded and the wrapper never started. The fix wraps each Windows command in `cmd /d /s /c`, preserving `%PLUGIN_ROOT%` expansion and `.cmd` execution even when Codex launches hooks through PowerShell.

## Checks
```text
python -m unittest tests.test_harness_hook
python -m unittest tests.test_hook_diagnostics
python -m unittest tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_optional_hook_runtime_resources_are_discoverable tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_default_hook_examples_do_not_wire_post_tool_use tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_default_hook_examples_wire_session_recovery_hooks tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_opencode_hook_example_uses_compaction_context_output
python -m unittest discover -s tests
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
python scripts\knowledge_check.py --root . --docs-path docs --strict
python skills\using-agentmentor\scripts\hook_diagnostics.py codex --project-root E:\Work-Project\OtherWork\ScienceClaw --format json
python -m unittest tests.test_harness_hook tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_codex_hook_example_uses_plugin_root_wrapper_commands tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_codex_hook_example_uses_codex_schema
manual smoke from C:\Users\HUAWEI\.codex\plugins\cache\personal\harness\0.1.0+codex.20260531010234 with command `hooks\run-agentmentor-hook.cmd stop`
python -m unittest tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_opencode_stop_uses_event_hook_for_session_idle tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_opencode_stop_fetches_latest_assistant_message tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_opencode_hook_example_uses_compaction_context_output tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_default_hook_examples_do_not_wire_post_tool_use tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_default_hook_examples_wire_session_recovery_hooks
python -m unittest tests.test_skill_progressive_disclosure.SkillProgressiveDisclosureTests.test_codex_command_windows_runs_under_powershell
python -m unittest tests.test_harness_hook tests.test_skill_progressive_disclosure tests.test_hook_diagnostics
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
PowerShell execution of installed cache `commandWindows` for SessionStart, PreCompact, and Stop
```

## Results

- `python -m unittest tests.test_harness_hook`: 17 tests passed after F005.2.
- `python -m unittest tests.test_hook_diagnostics`: 2 tests passed after F005.4.
- Targeted progressive-disclosure hook tests: 4 tests passed after F005.2.
- `python -m unittest discover -s tests`: 70 tests passed after F005.5.
- `python scripts\skill_metadata_check.py --root . --skills-path skills --strict`: scanned 11 skill files, 0 errors, 0 warnings.
- `python scripts\knowledge_check.py --root . --docs-path docs --strict`: scanned 33 Markdown files, checked 26 knowledge artifacts, 0 errors, 0 warnings.
- `python skills\using-agentmentor\scripts\hook_diagnostics.py codex --project-root E:\Work-Project\OtherWork\ScienceClaw --format json`: exited warning; runner smoke passed, 2 Codex compaction logs were found, and 0 recovery artifacts existed.
- F005.5 targeted hook tests: 21 tests passed, including runtime trace and Codex wrapper command assertions.
- F005.5 manual wrapper smoke: command returned `{}` for Codex allow output and wrote `.agentmentor/hook-events/events.jsonl` into the temporary payload `cwd`.
- F005.6 targeted OpenCode hook tests: 5 tests passed after confirming the new regression tests first failed against the direct `"session.idle"` hook key and missing session-message fetch.
- F005.7 regression test first failed with `Unexpected token 'session-start'` when PowerShell executed the old `"%PLUGIN_ROOT%\hooks\run-agentmentor-hook.cmd" session-start` command.
- F005.7 targeted regression test passed after wrapping Windows commands with `cmd /d /s /c`.
- F005.7 targeted suite passed: `python -m unittest tests.test_harness_hook tests.test_skill_progressive_disclosure tests.test_hook_diagnostics` ran 42 tests with OK.
- F005.7 installed cache smoke passed: SessionStart, PreCompact, and Stop `commandWindows` values all returned exit code 0 when executed through PowerShell with `PLUGIN_ROOT` set to the installed `agentmentor@personal` cache.

### AgentMentor Validation
`knowledge_check.py` command path and result:

```text
python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 29 markdown file(s). Checked 22 knowledge artifact(s). Errors: 0. Warnings: 0.
```

F005.1 rerun:

```text
python scripts\knowledge_check.py --root . --docs-path docs --strict
Scanned 32 markdown file(s). Checked 25 knowledge artifact(s). Errors: 0. Warnings: 0.
```

`skill_metadata_check.py` command path and result:

```text
python scripts\skill_metadata_check.py --root . --skills-path skills --strict
Scanned 11 skill file(s). Errors: 0. Warnings: 0.
```

## Artifacts

- `skills/using-agentmentor/hooks/agentmentor_hook.py`
- `skills/using-agentmentor/scripts/hook_diagnostics.py`
- `skills/using-agentmentor/hooks/codex-hooks.example.json`
- `skills/using-agentmentor/hooks/claude-settings.example.json`
- `skills/using-agentmentor/hooks/opencode-plugin.example.ts`
- `skills/using-agentmentor/SKILL.md`
- `INSTALL.md`
- `docs/quickstart.md`
- `docs/features/F005-session-recovery-hooks.md`
- `tests/test_agentmentor_hook.py`
- `tests/test_skill_progressive_disclosure.py`

## Limitations

This Evidence does not prove behavior outside the verification scope recorded above.

## Notes
Session recovery is runtime context, not canonical AgentMentor memory. The automatic injection snapshot is intentionally written under `.agentmentor/session-recovery/by-session/<session_id>.md` so only the same session can recover from compaction. `.agentmentor/session-recovery/latest.md` remains a manual inspection pointer and must not be injected into unrelated new sessions.

The follow-up learning from F005.1 is captured in [LL-005 Session Recovery Must Be Session-Scoped](../lessons/LL-005-session-recovery-must-be-session-scoped.md).

The follow-up learning from F005.2 is captured in [LL-006 Platform Hooks Must Use Native Context Channels](../lessons/LL-006-platform-hooks-native-context-channels.md).

The OpenCode example intentionally does not use `session.created` for automatic recovery. It handles `experimental.session.compacting(input, output)`, writes a same-session snapshot with `pre-compact`, reads that same-session snapshot through `session-start` with `source=compact`, and pushes recovered context into OpenCode's native `output.context` channel.

The F005.3 Codex follow-up came from a real `E:\Self-Project\Multi-Agent-Assi` session where the session log contained `compacted/context_compacted` but no `.agentmentor/session-recovery/` file. Codex `PreCompact` now uses an empty matcher so compaction variants are not missed; `SessionStart` remains `compact`-scoped to prevent unrelated startup pollution.

The F005.4 Codex follow-up came from a later new Codex Desktop session in `E:\Work-Project\OtherWork\ScienceClaw` where the session log again contained `compacted/context_compacted` but no `.agentmentor/session-recovery/` file. Manual runner smoke succeeded in that project root, so the protection moved from another matcher patch to a diagnostic that reports platform lifecycle evidence gaps.

The F005.5 Codex follow-up came from the same machine after Codex Settings displayed `Stop`, `PreCompact`, and `SessionStart`, while session logs and project runtime files still showed no hook execution. Local evidence showed Codex trusted `hooks/hooks.json`, while plugin examples also show root-level `hooks.json`; later comparison with Superpowers and Codex docs showed the missing user-level hook feature gates and the need for Windows-specific command expansion. The adapter now includes both config locations, routes commands through `hooks/run-agentmentor-hook.cmd`, uses `commandWindows` with `%PLUGIN_ROOT%`, and writes `.agentmentor/hook-events/events.jsonl` on actual runner execution.

The F005.7 Codex follow-up came from local Codex Desktop UI showing `hook exited with code 1` for every AgentMentor hook. Manual reproduction showed the runner and wrapper returned 0 when invoked directly, but the exact old `commandWindows` string returned 1 under PowerShell. The corrected config now uses `cmd /d /s /c ""%PLUGIN_ROOT%\hooks\run-agentmentor-hook.cmd" <event>"`, and the installed personal plugin source plus cache were updated on the local machine.

The F005.6 OpenCode follow-up came from rechecking the current official plugin contract on 2026-06-03. The npm type definition exposes `event(input)` for global events and direct trigger hooks for names such as `experimental.session.compacting`; the SDK event union includes `session.idle`, but the plugin `Hooks` interface does not expose `"session.idle"` as a direct hook key. The SDK also exposes `client.session.messages({ path: { id }, query: { directory, limit } })`, so the example now filters `input.event.type` inside `event(input)`, reads recent messages for that session, and sends the latest assistant text to the normalized `stop` runner.
