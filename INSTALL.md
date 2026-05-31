# Install AI Coding Harness Skills

AI Coding Harness is distributed as a **Skill suite** with an optional hook runtime.

Basic install: Skills only. Install the directories under `skills/` into the skills directory used by your agent, then restart the agent so it can discover the new Skill metadata.

Enhanced install: Skills + optional Hooks. Default hook examples enable Stop-time completion checks plus lightweight session recovery; hooks are not required for Harness to work.

Hook installation failure must not roll back Skills, block Skill loading, or make the Skill-only workflow unusable.

## Codex

Install globally with the helper script:

```bash
git clone https://github.com/solitudeTG/harness-coding-skills.git
cd harness-coding-skills
bash scripts/install.sh codex
```

Windows PowerShell:

```powershell
git clone https://github.com/solitudeTG/harness-coding-skills.git
Set-Location harness-coding-skills
.\scripts\install.ps1 codex
```

Restart Codex after installation. In a project, mention Harness or ask the agent to use `using-harness`; the entrypoint Skill will route to the focused `harness-*` skills.

If your Codex environment has the skill installer available, you can also ask Codex to install this repository as a Skill source.

## Claude Code

Install globally with the helper script:

```bash
git clone https://github.com/solitudeTG/harness-coding-skills.git
cd harness-coding-skills
bash scripts/install.sh claude
```

Windows PowerShell:

```powershell
git clone https://github.com/solitudeTG/harness-coding-skills.git
Set-Location harness-coding-skills
.\scripts\install.ps1 claude
```

Restart Claude Code after installation.

For project-local installation, copy the skills into the project:

```bash
mkdir -p .claude/skills
cp -R /path/to/harness-coding-skills/skills/* .claude/skills/
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

## Add Harness Rules To A Project

Installing Skills teaches the agent workflows and installs bundled Harness scripts/templates under `using-harness/`. Adding `AGENTS.md` teaches project-specific operating rules.

Copy the bundled template when a project needs repository-level rules:

```bash
cp ~/.codex/skills/using-harness/assets/templates/AGENTS.md /path/to/your-project/AGENTS.md
```

Windows PowerShell:

```powershell
Copy-Item "$HOME\.codex\skills\using-harness\assets\templates\AGENTS.md" "C:\path\to\your-project\AGENTS.md"
```

Fill in:

```text
1. The project rules agents must always follow.
2. The verification command that proves the project still works.
3. Where completion evidence should be recorded.
```

For longer-lived projects, add the optional Harness memory directories:

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
<skills-root>/using-harness/hooks/harness_hook.py
```

The runner calls the existing Skill-owned scripts:

```text
<skills-root>/using-harness/scripts/knowledge_check.py
<skills-root>/using-harness/scripts/harness_closeout_check.py
```

Set `HARNESS_SKILL_ROOT` to the installed `using-harness` directory before using the examples below. If hook setup fails, remove the hook config and continue using the Skills-only install.

Default hook examples enable Stop plus session recovery hooks. They do not wire PostToolUse because tool-call granularity is too fine for multi-edit Harness artifacts and can slow down ordinary editing. Run `knowledge_check.py --strict` at Stop/readiness/closeout/CI boundaries instead.

Session recovery uses:

```text
pre-compact  -> write .harness/session-recovery/by-session/<session_id>.md and update latest.md for manual inspection
session-start -> on compact recovery only, read the same session snapshot and expose context when the platform supports it
```

The recovery file is local project state. It is intentionally outside `docs/` because it is runtime context, not canonical Harness memory.

Codex example:

```text
<skills-root>/using-harness/hooks/codex-hooks.example.json
```

Claude Code example:

```text
<skills-root>/using-harness/hooks/claude-settings.example.json
```

OpenCode example:

```text
<skills-root>/using-harness/hooks/opencode-plugin.example.ts
```

These examples are intentionally additive. Merge the Harness entries into existing hook/plugin configuration instead of replacing user or project hooks.

## Verify

Validate Skill metadata from this source checkout:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills
```

Validate Harness knowledge artifacts:

```bash
python skills/using-harness/scripts/knowledge_check.py --root . --docs-path docs
```

Use strict mode for CI or review gates:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills --strict
python skills/using-harness/scripts/knowledge_check.py --root . --docs-path docs --strict
```

For an installed Codex skill suite, use `$HOME/.codex/skills/using-harness/scripts/knowledge_check.py` and `$HOME/.codex/skills/using-harness/scripts/harness_closeout_check.py`. Projects may vendor these files for CI, but vendoring is not required for normal Harness use.
