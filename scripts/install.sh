#!/usr/bin/env bash
# Install Create Wiki Skill for Cursor, Claude Code, Codex, or Hermes Agent.
set -euo pipefail

SKILL_NAME="create-wiki-skill"
REPO_URL="https://github.com/Tamaz-sujashvili/create-wiki.git"
TMP_DIR=""

cleanup() {
  if [[ -n "$TMP_DIR" && -d "$TMP_DIR" ]]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT

usage() {
  cat <<EOF
Create Wiki Skill — installer

Usage: install.sh [target]

Targets:
  cursor    Install to ~/.cursor/skills/$SKILL_NAME/  (default)
  claude    Install to ~/.claude/skills/$SKILL_NAME/
  codex     Install to ~/.codex/skills/$SKILL_NAME/
  hermes    Install to ~/.hermes/skills/research/$SKILL_NAME/
  all       Install to all of the above
  local DIR Install to a custom directory

Examples:
  curl -fsSL https://raw.githubusercontent.com/Tamaz-sujashvili/create-wiki/main/scripts/install.sh | bash
  ./scripts/install.sh cursor
  ./scripts/install.sh local ~/.cursor/skills/$SKILL_NAME
EOF
}

install_to() {
  local dest="$1"
  mkdir -p "$dest"
  cp -R "$TMP_DIR/create-wiki-skill/"* "$dest/"
  echo "Installed to $dest"
}

TARGET="${1:-cursor}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# If run from a cloned repo, use local files; otherwise fetch from GitHub.
if [[ -f "$SCRIPT_DIR/../SKILL.md" ]]; then
  SRC_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
  install_to() {
    local dest="$1"
    mkdir -p "$dest"
    cp -R "$SRC_DIR/"* "$dest/"
    echo "Installed to $dest"
  }
else
  TMP_DIR="$(mktemp -d)"
  git clone --depth 1 "$REPO_URL" "$TMP_DIR/repo" >/dev/null 2>&1
  if [[ -d "$TMP_DIR/repo/create-wiki-skill" ]]; then
    TMP_DIR="$TMP_DIR/repo/create-wiki-skill"
  else
    TMP_DIR="$TMP_DIR/repo"
  fi
  install_to() {
    local dest="$1"
    mkdir -p "$dest"
    if [[ -f "$TMP_DIR/SKILL.md" ]]; then
      cp -R "$TMP_DIR/"* "$dest/"
    else
      cp -R "$TMP_DIR/create-wiki-skill/"* "$dest/"
    fi
    echo "Installed to $dest"
  }
fi

case "$TARGET" in
  cursor)
    install_to "$HOME/.cursor/skills/$SKILL_NAME"
    ;;
  claude)
    install_to "$HOME/.claude/skills/$SKILL_NAME"
    ;;
  codex)
    install_to "$HOME/.codex/skills/$SKILL_NAME"
    ;;
  hermes)
    install_to "$HOME/.hermes/skills/research/$SKILL_NAME"
    ;;
  all)
    install_to "$HOME/.cursor/skills/$SKILL_NAME"
    install_to "$HOME/.claude/skills/$SKILL_NAME"
    install_to "$HOME/.codex/skills/$SKILL_NAME"
    install_to "$HOME/.hermes/skills/research/$SKILL_NAME"
    ;;
  local)
    if [[ -z "${2:-}" ]]; then
      echo "Error: local target requires a directory path" >&2
      usage
      exit 1
    fi
    install_to "$2"
    ;;
  -h|--help|help)
    usage
    exit 0
    ;;
  *)
    echo "Unknown target: $TARGET" >&2
    usage
    exit 1
    ;;
esac

echo ""
echo "Done. Set your wiki path:"
echo '  export WIKI_PATH="$HOME/wiki"'
echo ""
echo "Then ask your agent: \"Create a wiki about [your domain]\""
