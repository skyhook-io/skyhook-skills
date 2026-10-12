#!/usr/bin/env bash
# Install the Agent Skill adapters used by Codex and Cursor Agent.
#
# Claude Code's plugin marketplace manages the Claude plugin separately.
# Codex uses its own skills mechanism (~/.codex/skills), which Claude marketplaces
# do NOT manage, so the Codex companions are installed with this script. Cursor
# Agent also discovers ~/.codex/skills for compatibility and uses the same copy.
#
# Works two ways:
#   - one-liner:  curl -fsSL https://raw.githubusercontent.com/skyhook-io/skyhook-skills/main/scripts/install-codex.sh | bash
#   - from a clone:  bash scripts/install-codex.sh
#
# The Agent Skills are thin adapters that read the SAME canonical command files as
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
  trap 'if [ -L "$CLEANUP" ]; then echo "Temporary checkout became a symlink; leaving it: $CLEANUP -> $(readlink "$CLEANUP")" >&2; else rm -rf -- "$CLEANUP"; fi' EXIT
  echo "Fetching $REPO_URL ..."
  git clone --depth 1 --quiet "$REPO_URL" "$TMP/skyhook-skills"
  REPO_DIR="$TMP/skyhook-skills"
fi

mkdir -p "$SKILLS_DIR" "$SHARED_DIR"
cp -R "$REPO_DIR/codex/skills/." "$SKILLS_DIR/"
cp "$REPO_DIR/plugins/skyhook-skills/commands/"*.md "$SHARED_DIR/"

if SOURCE_ROOT="$(git -C "$REPO_DIR" rev-parse --show-toplevel 2>/dev/null)" &&
   [ "$SOURCE_ROOT" -ef "$REPO_DIR" ] &&
   REVISION="$(git -C "$REPO_DIR" rev-parse --verify HEAD 2>/dev/null)"; then
  if [ -n "$(git -C "$REPO_DIR" status --porcelain --ignored --untracked-files=all -- codex/skills plugins/skyhook-skills/commands scripts/install-codex.sh)" ]; then
    REVISION="$REVISION (modified checkout)"
  fi
else
  REVISION="unavailable (git metadata could not be read)"
  echo "WARNING: source revision unavailable for $REPO_DIR; installed files were copied successfully." >&2
fi
printf '%s\n' "$REVISION" > "$SHARED_DIR/.source-revision"

echo "Installed skills (Codex + Cursor) -> $SKILLS_DIR"
echo "Installed source revision        -> $REVISION"
echo "Canonical commands               -> $SHARED_DIR"
echo "Adapter command references:"
HAS_DUPLICATES=false
for ADAPTER in "$REPO_DIR"/codex/skills/*/SKILL.md; do
  SKILL="$(basename "$(dirname "$ADAPTER")")"
  COMMAND_REF="$(sed -n 's/.*`\([^`]*skyhook-skills-commands\/[^`]*\.md\)`.*/\1/p' "$ADAPTER" | sed -n '1p')"
  printf '  %s -> %s\n' "$SKILL" "${COMMAND_REF:-self-contained skill}"

  if [[ "$COMMAND_REF" == '~/.codex/skills/'* ]] && ! [ "$SKILLS_DIR" -ef "$HOME/.codex/skills" ]; then
    echo "WARNING: $SKILL references the default ~/.codex/skills command bundle outside this custom install." >&2
  fi

  for OTHER_ROOT in "$HOME/.agents/skills" "$HOME/.codex/skills"; do
    OTHER_ADAPTER="$OTHER_ROOT/$SKILL/SKILL.md"
    if [ -f "$OTHER_ADAPTER" ] && ! [ "$OTHER_ADAPTER" -ef "$SKILLS_DIR/$SKILL/SKILL.md" ]; then
      HAS_DUPLICATES=true
      OTHER_REF="$(sed -n 's/.*`\([^`]*\.md\)`.*/\1/p' "$OTHER_ADAPTER" | sed -n '1p')"
      printf 'WARNING: another %s adapter exists: %s\n  First document reference: %s\n' "$SKILL" "$OTHER_ADAPTER" "${OTHER_REF:-not detected; inspect the adapter}" >&2
    fi
  done
done
if [ "$HAS_DUPLICATES" = true ]; then
  echo "Duplicate warnings do not establish loader precedence; inspect the selected skill before removing any copy."
fi
echo "Restart Codex or start a new Cursor Agent session to pick up changes."
