# Quickstart

AI Coding Harness is a **Codex / Claude Code Skill suite**. Install the Skill directories first, then add the project templates you need.

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

Restart your agent after installation. Use `using-harness` as the entrypoint.

## Minimal Harness

Copy `templates/AGENTS.md` into your project and fill in:

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

Use templates:

```text
templates/FEATURE.md
templates/ADR.md
templates/LESSON.md
templates/EVIDENCE.md
```

## Validate Knowledge Artifacts

Validate Skill metadata:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills
```

Run:

```bash
python scripts/knowledge_check.py --root . --docs-path docs
```

Use strict mode for review or CI gates:

```bash
python scripts/skill_metadata_check.py --root . --skills-path skills --strict
python scripts/knowledge_check.py --root . --docs-path docs --strict
```

## Stop Rule

Do not create Harness artifacts just to look disciplined.

Create the smallest artifact that prevents future confusion, repeated mistakes, or unverifiable completion.
