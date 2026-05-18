# Install AI Coding Harness Skills

AI Coding Harness is distributed as a **Skill suite**. Install the directories under `skills/` into the skills directory used by your agent, then restart the agent so it can discover the new Skill metadata.

## Codex

Install globally with the helper script:

```bash
git clone https://github.com/TangHui-Best/ai-coding-harness.git
cd ai-coding-harness
bash scripts/install.sh codex
```

Windows PowerShell:

```powershell
git clone https://github.com/TangHui-Best/ai-coding-harness.git
Set-Location ai-coding-harness
.\scripts\install.ps1 codex
```

Restart Codex after installation. In a project, mention Harness or ask the agent to use `using-harness`; the entrypoint Skill will route to the focused `harness-*` skills.

If your Codex environment has the skill installer available, you can also ask Codex to install this repository as a Skill source.

## Claude Code

Install globally with the helper script:

```bash
git clone https://github.com/TangHui-Best/ai-coding-harness.git
cd ai-coding-harness
bash scripts/install.sh claude
```

Windows PowerShell:

```powershell
git clone https://github.com/TangHui-Best/ai-coding-harness.git
Set-Location ai-coding-harness
.\scripts\install.ps1 claude
```

Restart Claude Code after installation.

For project-local installation, copy the skills into the project:

```bash
mkdir -p .claude/skills
cp -R /path/to/ai-coding-harness/skills/* .claude/skills/
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
