#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/install.sh [codex|claude|both]

Installs AgentMentor Skills into the selected agent skills directory.
Hook examples are bundled under using-agentmentor/hooks/ and are copied with the Skills.
OpenCode uses the bundled opencode-plugin.example.ts as a plugin example rather
than a dedicated skills-directory install target.

Examples:
  bash scripts/install.sh codex
  bash scripts/install.sh claude
  bash scripts/install.sh both
EOF
}

target="${1:-both}"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

install_to() {
  local destination="$1"
  mkdir -p "$destination"
  rm -rf \
    "$destination/using-harness" \
    "$destination/harness-start-gate" \
    "$destination/harness-delegation-gate" \
    "$destination/harness-knowledge-retrieval" \
    "$destination/harness-doc-lifecycle" \
    "$destination/harness-incident-learning" \
    "$destination/harness-vision-gate" \
    "$destination/harness-readiness-dashboard" \
    "$destination/harness-change-narrative" \
    "$destination/harness-knowledge-capture" \
    "$destination/harness-project-rules" \
    "$destination/ai-coding-harness" \
    "$destination/ai-coding-harness-start-gate" \
    "$destination/ai-coding-harness-delegation-gate" \
    "$destination/ai-coding-harness-knowledge-retrieval" \
    "$destination/ai-coding-harness-doc-lifecycle" \
    "$destination/ai-coding-harness-incident-learning" \
    "$destination/ai-coding-harness-vision-gate" \
    "$destination/ai-coding-harness-readiness-dashboard" \
    "$destination/ai-coding-harness-change-narrative" \
    "$destination/ai-coding-harness-knowledge-capture" \
    "$destination/ai-coding-harness-project-rules"
  cp -R "$repo_root"/skills/* "$destination"/
  echo "Installed AgentMentor skills to $destination"
}

case "$target" in
  codex)
    install_to "$HOME/.codex/skills"
    ;;
  claude)
    install_to "$HOME/.claude/skills"
    ;;
  both)
    install_to "$HOME/.codex/skills"
    install_to "$HOME/.claude/skills"
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

echo "Restart your agent so it can reload Skill metadata."
