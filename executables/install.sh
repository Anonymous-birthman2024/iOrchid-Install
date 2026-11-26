#!/usr/bin/env bash
set -Eeuo pipefail

REPO_URL="https://github.com/Anonymous-birthman2024/iOrchid-Horticulture-Management.git"
REPO_DIR="${HOME}/iOrchid-Horticulture-Management"
MIN_FREE_KB=40960

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

echo "Checking installation requirements..."

case "$(uname -s)" in
  Linux|Darwin) ;;
  *) fail "Unsupported operating system: $(uname -s). Supported systems are Linux and macOS." ;;
esac

command -v git >/dev/null 2>&1 || fail "Git is not installed. Install Git and run this installer again."
command -v python3 >/dev/null 2>&1 || fail "Python 3 is not installed or is not on PATH."
python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)' || fail "iOrchid requires Python 3.9 or newer."

[ -n "${HOME:-}" ] || fail "HOME is not set."
[ -d "$HOME" ] || fail "Home directory does not exist: $HOME"
[ -w "$HOME" ] || fail "Home directory is not writable: $HOME"

AVAILABLE_KB="$(df -Pk "$HOME" | awk 'NR==2 {print $4}')"
[[ "$AVAILABLE_KB" =~ ^[0-9]+$ ]] || fail "Could not determine available disk space."
[ "$AVAILABLE_KB" -ge "$MIN_FREE_KB" ] || fail "At least 40 MB of free space is required in the filesystem containing $HOME."

echo "Checking access to the iOrchid repository..."
git ls-remote --exit-code "$REPO_URL" HEAD >/dev/null 2>&1 || fail "Cannot reach the iOrchid Git repository. Check your internet connection and repository access."

if [ -e "$REPO_DIR" ]; then
  [ -d "$REPO_DIR/.git" ] || fail "$REPO_DIR already exists but is not a Git repository. Move it aside or choose another installation location."
  [ -f "$REPO_DIR/run.py" ] || fail "The existing directory does not look like a complete iOrchid installation (run.py is missing). Back it up before repairing it."

  CURRENT_REMOTE="$(git -C "$REPO_DIR" remote get-url origin 2>/dev/null || true)"
  [ "$CURRENT_REMOTE" = "$REPO_URL" ] || fail "The existing Git repository has a different origin. It has been left untouched."

  if [ -n "$(git -C "$REPO_DIR" status --porcelain)" ]; then
    fail "The existing iOrchid directory contains local changes. Commit or back them up before updating; no files were changed."
  fi

  CURRENT_BRANCH="$(git -C "$REPO_DIR" branch --show-current)"
  [ "$CURRENT_BRANCH" = "main" ] || fail "The existing installation is on branch $CURRENT_BRANCH, not main. Switch to main before updating."

  echo "Existing iOrchid installation found. Updating it safely..."
  git -C "$REPO_DIR" pull --ff-only origin main || fail "Could not fast-forward the existing installation. Check its branch and Git status."
else
  TEMP_DIR="$(mktemp -d "${HOME}/.iorchid-install.XXXXXX")"
  cleanup() {
    rm -rf "$TEMP_DIR"
  }
  trap cleanup EXIT

  echo "Downloading iOrchid into a temporary directory..."
  git clone --depth 1 "$REPO_URL" "$TEMP_DIR/iOrchid-Horticulture-Management"
  mv "$TEMP_DIR/iOrchid-Horticulture-Management" "$REPO_DIR"
  echo "Repository installed at $REPO_DIR"
fi

if [ -f "$REPO_DIR/requirements.txt" ]; then
  echo "Creating an isolated Python environment..."
  python3 -m venv "$REPO_DIR/venv" || fail "Could not create a Python virtual environment. On Debian/Ubuntu, install the python3-venv package and retry."
  echo "Installing Python dependencies into the virtual environment..."
  "$REPO_DIR/venv/bin/python" -m pip install --upgrade pip || fail "Could not upgrade pip in the virtual environment."
  "$REPO_DIR/venv/bin/python" -m pip install -r "$REPO_DIR/requirements.txt" || fail "Python dependency installation failed. Review the pip error above."
else
  echo "No requirements.txt was found; no Python packages were installed."
fi

[ -f "$REPO_DIR/run.py" ] || fail "Post-install verification failed: run.py is missing."
echo "Post-install verification passed."
echo "iOrchid is ready at: $REPO_DIR"
