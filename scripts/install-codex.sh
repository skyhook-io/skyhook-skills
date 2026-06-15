#!/usr/bin/env bash
# Install the Codex-side skills.
#
# Claude Code's plugin marketplace manages the CLAUDE plugin (auto-updates).
# Codex uses its own skills mechanism (~/.codex/skills), which Claude marketplaces
# do NOT manage, so the Codex companions are installed with this script.
#
# Works two ways:
#   - one-liner:  curl -fsSL https://raw.githubusercontent.com/skyhook-io/skyhook-skills/main/scripts/install-codex.sh | bash
#   - from a clone:  bash scripts/install-codex.sh
#
# The Codex skills are thin adapters that read the SAME canonical command files as
# the Claude plugin (single source of truth); this copies those files into a shared
# dir the skills reference.
set -euo pipefail

REPO_URL="https://github.com/skyhook-io/skyhook-skills"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="$CODEX_HOME/skills"
SHARED_DIR="$SKILLS_DIR/skyhook-skills-commands"

# Use the local checkout if we're running inside one; otherwise clone to a temp dir.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
if [ -n "${SCRIPT_DIR:-}" ] && [ -d "$SCRIPT_DIR/../codex/skills" ]; then
  REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
  CLEANUP=""
else
  TMP="$(mktemp -d)"
  CLEANUP="$TMP"
  trap '[ -n "$CLEANUP" ] && rm -rf "$CLEANUP"' EXIT
  echo "Fetching $REPO_URL ..."
  git clone --depth 1 --quiet "$REPO_URL" "$TMP/skyhook-skills"
  REPO_DIR="$TMP/skyhook-skills"
fi

mkdir -p "$SKILLS_DIR" "$SHARED_DIR"
cp -R "$REPO_DIR/codex/skills/." "$SKILLS_DIR/"
cp "$REPO_DIR/plugins/skyhook-skills/commands/"*.md "$SHARED_DIR/"

echo "Installed Codex skills -> $SKILLS_DIR"
echo "Canonical commands     -> $SHARED_DIR"
echo "Restart Codex to pick up the new skills."
