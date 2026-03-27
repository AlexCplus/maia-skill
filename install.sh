#!/usr/bin/env bash
# Tododeia / MAIA Skill — Installer
# Usage: curl -sL https://raw.githubusercontent.com/AlexCplus/maia-skill/main/install.sh | bash

set -e

REPO="https://github.com/AlexCplus/maia-skill.git"
SKILL_NAME="investment-analysis"
INSTALL_DIR="$HOME/.claude/skills/$SKILL_NAME"
CLONE_DIR="$HOME/.claude/plugins/maia-skill"

is_git_repo() {
  git -C "$1" rev-parse --is-inside-work-tree >/dev/null 2>&1
}

remove_path() {
  if [ -L "$1" ]; then unlink "$1" 2>/dev/null || true; fi
  if [ -e "$1" ] || [ -L "$1" ]; then rm -rf "$1" 2>/dev/null || true; fi
  if [ -d "$1" ]; then rmdir "$1" 2>/dev/null || true; fi
}

echo ""
echo "  Tododeia — Multi-Agent Investment Analysis"
echo "  by @soyenriquerocha"
echo ""

# Check if already installed
if [ -e "$INSTALL_DIR" ]; then
  echo "  Skill already installed at $INSTALL_DIR"
  if [ -d "$INSTALL_DIR/.git" ] || is_git_repo "$INSTALL_DIR"; then
    echo "  Updating..."
    git -C "$INSTALL_DIR" pull --quiet
    echo "  Updated successfully."
    echo ""
    exit 0
  fi
  echo "  Existing installation is invalid. Reinstalling..."
  remove_path "$INSTALL_DIR"
fi

# Clone the repo
mkdir -p "$HOME/.claude/plugins"
if [ -d "$CLONE_DIR" ]; then
  if is_git_repo "$CLONE_DIR"; then
    if [ -d "$CLONE_DIR/.claude/skills/$SKILL_NAME" ]; then
      echo "  Updating..."
      git -C "$CLONE_DIR" pull --quiet
    else
      echo "  Existing clone is incomplete. Reinstalling..."
      rm -rf "$CLONE_DIR"
    fi
  else
    rm -rf "$CLONE_DIR"
  fi
fi

if [ ! -d "$CLONE_DIR" ]; then
  echo "  Cloning skill..."
  git clone --quiet "$REPO" "$CLONE_DIR"
fi

# Symlink skill to Claude Code skills directory
mkdir -p "$HOME/.claude/skills"
SOURCE_SKILL_DIR="$CLONE_DIR/.claude/skills/$SKILL_NAME"
remove_path "$INSTALL_DIR"
if [ -e "$INSTALL_DIR" ] || [ -L "$INSTALL_DIR" ]; then
  echo "  Error: could not clean $INSTALL_DIR";
  exit 1;
fi
if ln -s "$SOURCE_SKILL_DIR" "$INSTALL_DIR"; then
  :
else
  echo "  Symlink not permitted — copying files instead..."
  if [ ! -d "$SOURCE_SKILL_DIR" ]; then
    echo "  Error: source skill directory missing at $SOURCE_SKILL_DIR"
    exit 1
  fi
  remove_path "$INSTALL_DIR"
  mkdir -p "$INSTALL_DIR"
  cp -RL "$SOURCE_SKILL_DIR"/. "$INSTALL_DIR"
fi

# Install dashboard dependencies if Node.js is available
if command -v npm &> /dev/null; then
  echo "  Installing dashboard dependencies..."
  npm install --prefix "$CLONE_DIR/dashboard" --silent 2>/dev/null
  echo "  Dashboard ready."
else
  echo "  Node.js not found — dashboard will use HTML fallback."
  echo "  Install Node.js 18+ for the interactive dashboard."
fi

echo ""
echo "  Installed successfully!"
echo ""
echo "  Open Claude Code and say:"
echo "    \"Run an investment analysis\""
echo "    \"Analyze the markets\""
echo "    \"Run tododeia\""
echo ""
echo "  To uninstall:"
echo "    rm -rf $INSTALL_DIR $CLONE_DIR"
echo ""
