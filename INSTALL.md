# Install AgentMentor Skills

AgentMentor is distributed as a **Skill suite** with an optional hook runtime.

Basic install: Skills only. Install the directories under `skills/` into the skills directory used by your agent, then restart the agent so it can discover the new Skill metadata.

Enhanced install: Skills + optional Hooks. Default hook examples enable Stop-time completion checks plus lightweight session recovery; hooks are not required for Harness to work.

Hook installation failure must not roll back Skills, block Skill loading, or make the Skill-only workflow unusable.

## Codex

Install globally with the helper script:

```bash
git clone https://github.com/TangHui-Best/using-agentmentor.git
cd using-agentmentor
bash scripts/install.sh codex
```

Windows PowerShell:

```powershell
git clone https://github.com/TangHui-Best/using-agentmentor.git
Set-Location using-agentmentor
.\scripts\install.ps1 codex
```

Restart Codex after installation. In a project, mention AgentMentor or ask the agent to use `using-agentmentor`; the entrypoint Skill will route to the focused workflow skills such as `start-gate` and `readiness-dashboard`.

Breaking rename note: the formal system name is `AgentMentor`. The installed slugs are `using-agentmentor` plus short semantic workflow slugs such as `start-gate` and `readiness-dashboard`; pre-rename skill directories should be removed before reinstalling this version. See `docs/decisions/ADR-008-agentmentor-semantic-skill-routing.md` for the exact migration record.

If your Codex environment has the skill installer available, you can also ask Codex to install this repository as a Skill source.

For Codex Desktop personal plugin installs, the plugin identity is `agentmentor@personal`. Do not keep an older `harness@personal` personal plugin enabled, because Codex can regenerate its plugin cache and expose the removed `using-harness` / `harness-*` Skill slugs. This repository includes `.codex-plugin/plugin.json`, root `hooks.json`, `hooks/hooks.json`, and the `skills/` directory required for the personal plugin package.

## Claude Code

Install globally with the helper script:

```bash
git clone https://github.com/TangHui-Best/using-agentmentor.git
cd using-agentmentor
bash scripts/install.sh claude
```

Windows PowerShell:

```powershell
git clone https://github.com/TangHui-Best/using-agentmentor.git
Set-Location using-agentmentor
.\scripts\install.ps1 claude
```

Restart Claude Code after installation.

For project-local installation, copy the skills into the project:

```bash
mkdir -p .claude/skills
cp -R /path/to/using-agentmentor/skills/* .claude/skills/
```

Claude Code expects each Skill to have this shape:

```text
<skills-root>/<skill-name>/SKILL.md
```

## Manual Install

If you do not want to run the helper script, copy the Skill directories directly.

Codex:

```bash
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills", "$HOME\.claude\skills"
Copy-Item ".\skills\*" "$HOME\.codex\skills\" -Recurse -Force
Copy-Item ".\skills\*" "$HOME\.claude\skills\" -Recurse -Force
```

## Optional Project Rules

Installing Skills teaches the agent workflows and installs bundled Harness scripts/templates under `using-agentmentor/`. Adding `AGENTS.md` teaches project-specific operating rules.

AgentMentor does not automatically modify global or project `AGENTS.md` files. You may copy the bundled `AGENTS.md` template when a project needs repository-level rules:

```bash
cp ~/.codex/skills/using-agentmentor/assets/templates/AGENTS.md /path/to/your-project/AGENTS.md
```

Windows PowerShell:

```powershell
Copy-Item "$HOME\.codex\skills\using-agentmentor\assets\templates\AGENTS.md" "C:\path\to\your-project\AGENTS.md"
```

Fill in:

```text
1. The project rules agents must always follow.
2. The verification command that proves the project still works.
3. Where completion evidence should be recorded.
```

Recommended additions:

```text
- Run Start Gate before non-trivial implementation.
- If real cases, validation, or user feedback contradict an existing spec, run Spec Drift before changing code.
- If repeated patches add scenario-specific branches, pause and run Patch Churn Review before continuing.
```

For longer-lived projects, add the optional AgentMentor memory directories:

```text
docs/BACKLOG.md
docs/features/
docs/decisions/
docs/lessons/
docs/evidence/
```

## Optional Hook Runtime

The optional hook runner is bundled under:

```text
<skills-root>/using-agentmentor/hooks/agentmentor_hook.py
```

The runner calls the existing Skill-owned scripts:

```text
<skills-root>/using-agentmentor/scripts/knowledge_check.py
<skills-root>/using-agentmentor/scripts/closeout_check.py
<skills-root>/using-agentmentor/scripts/hook_diagnostics.py
```

For Codex plugin-bundled hooks, use the `agentmentor@personal` plugin identity and keep both root-level `hooks.json` and `hooks/hooks.json` available, with identical content, because Codex Desktop installations have shown different discovery evidence during local iteration. Enable both `[features].hooks = true` and `[features].plugin_hooks = true` before expecting runtime dispatch. The command should call `hooks/run-agentmentor-hook.cmd`, which resolves the plugin root from the wrapper location and then runs `skills/using-agentmentor/hooks/agentmentor_hook.py`; on Windows, use `commandWindows` with `%PLUGIN_ROOT%` wrapped by `cmd /d /s /c` so it still works when Codex invokes the hook command through PowerShell. Do not call `python ./skills/...` directly from `hooks.json`, because the hook runtime current working directory is not a stable contract. If hook setup fails, remove the hook config and continue using the Skills-only install.

Default hook examples enable Stop plus session recovery hooks. They do not wire PostToolUse because tool-call granularity is too fine for multi-edit AgentMentor artifacts and can slow down ordinary editing. Run `knowledge_check.py --strict` at Stop/readiness/closeout/CI boundaries instead.

Session recovery uses:

```text
pre-compact  -> write .agentmentor/session-recovery/by-session/<session_id>.md and update latest.md for manual inspection
session-start -> on compact recovery only, read the same session snapshot and expose context when the platform supports it
```

The recovery file is local project state. It is intentionally outside `docs/` because it is runtime context, not canonical AgentMentor memory.

Codex example:

```text
<skills-root>/using-agentmentor/hooks/codex-hooks.example.json
```

Claude Code example:

```text
<skills-root>/using-agentmentor/hooks/claude-settings.example.json
```

OpenCode example:

```text
<skills-root>/using-agentmentor/hooks/opencode-plugin.example.ts
```

OpenCode session recovery is injected during `experimental.session.compacting(input, output)` through `output.context`. Do not wire `session.created` as an automatic recovery reader; new independent sessions must not inherit a prior session's compaction snapshot.

These examples are intentionally additive. Merge the AgentMentor entries into existing hook/plugin configuration instead of replacing user or project hooks.

After installing or changing Codex hooks, run the local diagnostic from the project you want to verify:

```bash
python ~/.codex/skills/using-agentmentor/scripts/hook_diagnostics.py codex --project-root /path/to/your-project
```

Windows PowerShell:

```powershell
python "$HOME\.codex\skills\using-agentmentor\scripts\hook_diagnostics.py" codex --project-root "C:\path\to\your-project"
```

The diagnostic performs a runner smoke test and scans Codex session logs for `compacted/context_compacted` events that did not produce `.agentmentor/session-recovery/` artifacts. A warning means the Skill suite is still usable, but the optional Codex `PreCompact` recovery hook is not proven in that environment.

When a AgentMentor hook actually runs, the runner writes a minimal runtime trace to `.agentmentor/hook-events/events.jsonl` under the project root. The trace records event, platform, session id, decision, check, and severity only; it does not store assistant/user message bodies.

## Verify

Validate Skill metadata from this source checkout:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills
```

Validate AgentMentor knowledge artifacts:

```bash
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs
```

Use strict mode for CI or review gates:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills --strict
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs --strict
```

For an installed Codex skill suite, use `$HOME/.codex/skills/using-agentmentor/scripts/knowledge_check.py` and `$HOME/.codex/skills/using-agentmentor/scripts/closeout_check.py`. Projects may vendor these files for CI, but vendoring is not required for normal AgentMentor use.
