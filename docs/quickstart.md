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

Skills-only install remains valid. Hooks are optional runtime checks. Default examples enable the Stop hook plus lightweight session recovery so completion claims and context restoration can be assisted without slowing down every edit.

Examples live under:

```text
using-agentmentor/hooks/
```

If hook setup fails, remove the hook config and continue with the Skill workflow.

Session recovery writes `.agentmentor/session-recovery/by-session/<session_id>.md` before compaction and updates `.agentmentor/session-recovery/latest.md` only for manual inspection. `session-start` injects recovery context only for compact recovery of the same session, so a new independent session does not automatically inherit old task context. This is local runtime state, not canonical AgentMentor memory.

For OpenCode, recovery context is injected during `experimental.session.compacting(input, output)` through `output.context`. Do not use `session.created` as an automatic recovery reader.

For Codex, verify hook runtime evidence after installation:

```bash
python ~/.codex/skills/using-agentmentor/scripts/hook_diagnostics.py codex --project-root /path/to/project
```

If the diagnostic reports compaction events without recovery artifacts, keep using Skills and manual/canonical AgentMentor handoff until the Codex hook path is proven on that machine.

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
