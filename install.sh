#!/usr/bin/env bash
# install.sh — installs the `release-commander` command globally.
#
# Usage:
#   chmod +x install.sh && ./install.sh
#
# What it does:
#   1. Installs Python dependencies (pytest, fastapi, httpx, pydantic).
#   2. Creates a `release-commander` symlink in /usr/local/bin (or ~/bin if
#      /usr/local/bin is not writable without sudo).
#   3. Makes release_commander.py executable.
#
# After install:
#   release-commander --repo /path/to/your/repo
#   release-commander --repo /path/to/your/repo --fix

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/release-commander/release_commander.py"

# ── 1. Dependencies ──────────────────────────────────────────────────────────
echo "→ Installing Python dependencies..."
python3 -m pip install --quiet pytest fastapi httpx pydantic uvicorn

# ── 2. Make the script executable ────────────────────────────────────────────
chmod +x "$PY_SCRIPT"

# ── 3. Choose install target ─────────────────────────────────────────────────
if [ -w /usr/local/bin ]; then
    INSTALL_DIR=/usr/local/bin
elif [ -d "$HOME/.local/bin" ]; then
    INSTALL_DIR="$HOME/.local/bin"
else
    mkdir -p "$HOME/bin"
    INSTALL_DIR="$HOME/bin"
fi

LINK="$INSTALL_DIR/release-commander"

# Remove stale link if present
[ -L "$LINK" ] && rm "$LINK"

ln -s "$PY_SCRIPT" "$LINK"
echo "✓ Installed: $LINK → $PY_SCRIPT"

# ── 4. PATH hint ─────────────────────────────────────────────────────────────
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    echo ""
    echo "  Note: $INSTALL_DIR is not in your \$PATH."
    echo "  Add this line to your ~/.zshrc or ~/.bashrc:"
    echo "    export PATH=\"$INSTALL_DIR:\$PATH\""
    echo ""
fi

echo ""
echo "Done. Try it:"
echo "  release-commander --repo /path/to/your/repo"
echo "  release-commander --repo /path/to/your/repo --fix"
echo "  release-commander --help"
