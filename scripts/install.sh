#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/install.sh [--verify] [codex|claude|both]

Installs AgentMentor Skills into the selected agent skills directory.
Hook examples are bundled under using-agentmentor/hooks/ and are copied with the Skills.
OpenCode uses the bundled opencode-plugin.example.ts as a plugin example rather
than a dedicated skills-directory install target.

Environment overrides:
  AGENTMENTOR_CODEX_SKILLS_DIR   Override the Codex skills destination.
  AGENTMENTOR_CLAUDE_SKILLS_DIR  Override the Claude Code skills destination.

Examples:
  bash scripts/install.sh codex
  bash scripts/install.sh claude
  bash scripts/install.sh both
  bash scripts/install.sh --verify codex
EOF
}

verify_only=0
target="both"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --verify)
      verify_only=1
      shift
      ;;
    -h|--help|help)
      usage
      exit 0
      ;;
    codex|claude|both)
      target="$1"
      shift
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac
done

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

formal_skills=(
  "using-agentmentor"
  "start-gate"
  "delegation-gate"
  "knowledge-retrieval"
  "spec-drift"
  "doc-lifecycle"
  "incident-learning"
  "vision-gate"
  "readiness-dashboard"
  "change-narrative"
  "knowledge-capture"
  "project-rules"
)

removed_skill_dirs=(
  "using-harness"
  "harness-start-gate"
  "harness-delegation-gate"
  "harness-knowledge-retrieval"
  "harness-doc-lifecycle"
  "harness-incident-learning"
  "harness-vision-gate"
  "harness-readiness-dashboard"
  "harness-change-narrative"
  "harness-knowledge-capture"
  "harness-project-rules"
  "ai-coding-harness"
  "ai-coding-harness-start-gate"
  "ai-coding-harness-delegation-gate"
  "ai-coding-harness-knowledge-retrieval"
  "ai-coding-harness-doc-lifecycle"
  "ai-coding-harness-incident-learning"
  "ai-coding-harness-vision-gate"
  "ai-coding-harness-readiness-dashboard"
  "ai-coding-harness-change-narrative"
  "ai-coding-harness-knowledge-capture"
  "ai-coding-harness-project-rules"
)

required_bundled_resources=(
  "using-agentmentor/scripts/knowledge_check.py"
  "using-agentmentor/scripts/closeout_check.py"
  "using-agentmentor/scripts/hook_diagnostics.py"
  "using-agentmentor/hooks/agentmentor_hook.py"
  "using-agentmentor/assets/templates/AGENTS.md"
)

destination_for() {
  case "$1" in
    codex)
      echo "${AGENTMENTOR_CODEX_SKILLS_DIR:-$HOME/.codex/skills}"
      ;;
    claude)
      echo "${AGENTMENTOR_CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
      ;;
  esac
}

verify_installation() {
  local destination="$1"
  local label="$2"
  local errors=0

  if [[ ! -d "$destination" ]]; then
    echo "Verification: failed for $label; destination does not exist: $destination" >&2
    return 1
  fi

  for skill in "${formal_skills[@]}"; do
    if [[ ! -f "$destination/$skill/SKILL.md" ]]; then
      echo "Verification error: missing $skill/SKILL.md in $destination" >&2
      errors=$((errors + 1))
    fi
  done

  for skill in "${removed_skill_dirs[@]}"; do
    if [[ -e "$destination/$skill" ]]; then
      echo "Verification error: removed legacy skill still exists: $destination/$skill" >&2
      errors=$((errors + 1))
    fi
  done

  for resource in "${required_bundled_resources[@]}"; do
    if [[ ! -f "$destination/$resource" ]]; then
      echo "Verification error: missing bundled resource: $destination/$resource" >&2
      errors=$((errors + 1))
    fi
  done

  if [[ "$errors" -gt 0 ]]; then
    echo "Verification: failed for $label with $errors error(s)." >&2
    return 1
  fi

  echo "Verification: passed for $label at $destination"
}

install_to() {
  local destination="$1"
  local label="$2"
  mkdir -p "$destination"
  for skill in "${removed_skill_dirs[@]}"; do
    rm -rf "$destination/$skill"
  done
  cp -R "$repo_root"/skills/* "$destination"/
  echo "Installed AgentMentor skills to $destination"
  verify_installation "$destination" "$label"
}

verify_to() {
  local destination="$1"
  local label="$2"
  echo "Verify-only: no files were copied for $label."
  verify_installation "$destination" "$label"
}

print_next_steps() {
  cat <<'EOF'
Restart your agent so it can reload Skill metadata.
Use `using-agentmentor` as the entrypoint after restart.
Hooks are optional. To check Codex Stop hook runtime after hook setup, run:
  python <skills-root>/using-agentmentor/scripts/hook_diagnostics.py codex --project-root <project>
EOF
}

case "$target" in
  codex)
    if [[ "$verify_only" -eq 1 ]]; then
      verify_to "$(destination_for codex)" "Codex"
    else
      install_to "$(destination_for codex)" "Codex"
    fi
    ;;
  claude)
    if [[ "$verify_only" -eq 1 ]]; then
      verify_to "$(destination_for claude)" "Claude Code"
    else
      install_to "$(destination_for claude)" "Claude Code"
    fi
    ;;
  both)
    if [[ "$verify_only" -eq 1 ]]; then
      verify_to "$(destination_for codex)" "Codex"
      verify_to "$(destination_for claude)" "Claude Code"
    else
      install_to "$(destination_for codex)" "Codex"
      install_to "$(destination_for claude)" "Claude Code"
    fi
    ;;
esac

print_next_steps
