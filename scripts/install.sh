#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/install.sh [codex|claude|both]

Installs AI Coding Harness Skills into the selected agent skills directory.

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
  cp -R "$repo_root"/skills/* "$destination"/
  echo "Installed Harness skills to $destination"
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
