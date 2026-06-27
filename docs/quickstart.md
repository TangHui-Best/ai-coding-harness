# Quickstart

AgentMentor is a **Codex / Claude Code Skill suite** with optional hook examples for Codex, Claude Code, and OpenCode. Install the Skill directories first, then add the project templates you need.

## Install Skills

From the repository root:

```bash
bash scripts/install.sh codex
```

For Claude Code:

```bash
bash scripts/install.sh claude
```

Windows PowerShell:

```powershell
.\scripts\install.ps1 both
```

Restart your agent after installation. Use `using-agentmentor` as the entrypoint.

## Optional Hooks

Skills-only install remains valid. Hooks are optional runtime checks. Default examples enable only the Stop hook so completion claims can be checked without slowing down every edit.

Examples live under:

```text
using-agentmentor/hooks/
```

If hook setup fails, remove the hook config and continue with the Skill workflow.

AgentMentor no longer provides default `pre-compact` / `session-start` recovery hooks. Platform compaction remains the platform's responsibility. Use explicit handoff notes only when the user asks for handoff or an unfinished task is intentionally paused.

For Codex, verify hook runtime evidence after installation:

```bash
python ~/.codex/skills/using-agentmentor/scripts/hook_diagnostics.py codex --project-root /path/to/project
```

If the diagnostic reports a Stop runner warning, keep using Skills-only closeout until the hook path is fixed on that machine.

## Minimal Harness

Copy the bundled `AGENTS.md` template into your project and fill in:

- Project rules agents must follow.
- When non-trivial work must pass Start Gate before coding.
- Verification commands.
- Evidence expectations.

This gives the project a shared operating surface outside a single prompt.

## Project Harness

When work spans multiple sessions or contributors, add:

```text
docs/BACKLOG.md
docs/features/
docs/decisions/
docs/lessons/
docs/evidence/
```

Use the bundled templates from `using-agentmentor/assets/templates/`:

```text
using-agentmentor/assets/templates/FEATURE.md
using-agentmentor/assets/templates/ADR.md
using-agentmentor/assets/templates/LESSON.md
using-agentmentor/assets/templates/EVIDENCE.md
```

## Validate Knowledge Artifacts

Validate Skill metadata:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills
```

Run:

```bash
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs
```

Use strict mode for review or CI gates:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills --strict
python skills/using-agentmentor/scripts/knowledge_check.py --root . --docs-path docs --strict
```

## Stop Rule

Do not create AgentMentor artifacts just to look disciplined.

Create the smallest artifact that prevents future confusion, repeated mistakes, or unverifiable completion.
