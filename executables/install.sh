#!/usr/bin/env bash
set -e

REPO_URL="https://github.com/Anonymous-birthman2024/iOrchid-Horticulture-Management.git"
REPO_DIR="$HOME/iOrchid-Horticulture-Management"

if [ -d "$REPO_DIR" ]; then
  echo "Repository already exists in $HOME"
else
  cd "$HOME"
  git clone "$REPO_URL"
fi
