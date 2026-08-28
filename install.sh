#!/usr/bin/env bash
# install.sh — installs the `release-commander` command globally (editable).
#
# Run from the repository root:
#   bash install.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -f "$SCRIPT_DIR/pyproject.toml" ]; then
  echo "error: run this from the repository root (where pyproject.toml lives)." >&2
  exit 1
fi

echo "→ Installing release-commander (editable)..."
cd "$SCRIPT_DIR"
python3 -m pip install --quiet --upgrade pip
python3 -m pip install --quiet -e .

echo ""
echo "✓ Installed. Try it:"
echo "  release-commander --repo /path/to/your/repo"
echo "  release-commander --repo /path/to/your/repo --fix"
echo "  release-commander --help"
