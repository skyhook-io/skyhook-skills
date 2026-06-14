#!/usr/bin/env bash
# Install the Codex-side skills.
#
# Claude Code's plugin marketplace manages the CLAUDE plugin (auto-updates).
# Codex uses its own skills mechanism (~/.codex/skills), which Claude marketplaces
# do NOT manage, so the Codex companions are installed manually with this script.
#
# The Codex skills are thin adapters that read the SAME canonical command files as
# the Claude plugin (single source of truth) — this script copies those command
# files into a shared dir the skills reference.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="$CODEX_HOME/skills"
SHARED_DIR="$SKILLS_DIR/skyhook-skills-commands"

mkdir -p "$SKILLS_DIR" "$SHARED_DIR"

# Codex skills (autodev, plan-loop, review-loop, product-review, claude-review)
cp -R "$REPO_DIR/codex/skills/." "$SKILLS_DIR/"

# Canonical command files the skills read (kept in sync with the Claude plugin)
cp "$REPO_DIR/plugins/skyhook-skills/commands/"*.md "$SHARED_DIR/"

echo "Installed Codex skills -> $SKILLS_DIR"
echo "Canonical commands     -> $SHARED_DIR"
echo "Restart Codex to pick up the new skills."
