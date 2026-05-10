#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# RequityAI / Agency OS — GitHub auth + push setup
#
# What this does:
#   1. Installs the GitHub CLI (`gh`) via Homebrew if not already present
#   2. Logs you into GitHub via device-code flow
#       → this is the ONE step you have to do yourself: GitHub will
#         show a URL + code in the terminal, you paste the code in your
#         browser and click "Authorize"
#   3. Configures git to use gh's auth (no more password prompts ever)
#   4. Pushes the Agency OS repo to github.com/andrewpcherry/agencyos
#
# How to run it:
#   Open Terminal.app, then run:
#     bash "/Users/andrewcherry/Documents/Claude/Projects/Agency OS/_handoff/patched/setup_github_push.sh"
#
# Safe to re-run. Each step is idempotent — if it's already done, it skips.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

REPO_DIR="/Users/andrewcherry/Documents/Claude/Projects/Agency OS"
REMOTE_URL="https://github.com/andrewpcherry/agencyos.git"

cd "$REPO_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  RequityAI / Agency OS — GitHub setup"
echo "  Working directory: $REPO_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ─── Step 1: Homebrew + gh CLI ───────────────────────────────────────────────
echo "▶ Step 1/5: Checking for Homebrew + GitHub CLI..."

if ! command -v brew >/dev/null 2>&1; then
  echo "  ✗ Homebrew is not installed."
  echo "  Install it first by running this command in Terminal:"
  echo ""
  echo '    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  echo ""
  echo "  Then re-run this script."
  exit 1
fi
echo "  ✓ Homebrew is installed."

if ! command -v gh >/dev/null 2>&1; then
  echo "  → Installing GitHub CLI (gh)..."
  brew install gh
else
  echo "  ✓ GitHub CLI is already installed ($(gh --version | head -1))."
fi

# ─── Step 2: gh auth login ───────────────────────────────────────────────────
echo ""
echo "▶ Step 2/5: GitHub authentication..."

if gh auth status >/dev/null 2>&1; then
  echo "  ✓ You are already logged into GitHub as: $(gh api user --jq .login)"
else
  echo ""
  echo "  ┌─────────────────────────────────────────────────────────────────────┐"
  echo "  │  YOU DO THIS PART:                                                  │"
  echo "  │                                                                     │"
  echo "  │  1. The next prompt will give you a one-time code (8 chars).        │"
  echo "  │  2. Press Enter — your browser will open to github.com/login/device │"
  echo "  │  3. Paste the code. Click 'Authorize'.                              │"
  echo "  │  4. Come back here. You're done.                                    │"
  echo "  └─────────────────────────────────────────────────────────────────────┘"
  echo ""
  read -p "  Press Enter when ready..."

  # HTTPS protocol = simplest path; device flow handles the rest
  gh auth login --hostname github.com --git-protocol https --web --scopes "repo,workflow"
fi

# ─── Step 3: Git uses gh credentials ─────────────────────────────────────────
echo ""
echo "▶ Step 3/5: Wiring git to use gh's auth..."
gh auth setup-git
echo "  ✓ Git is now using your GitHub credentials. No more password prompts."

# ─── Step 4: Set git identity (only if not already set) ──────────────────────
echo ""
echo "▶ Step 4/5: Confirming git identity..."

GIT_NAME=$(git config --global user.name || echo "")
GIT_EMAIL=$(git config --global user.email || echo "")

if [ -z "$GIT_NAME" ]; then
  # gh api user --jq .name returns 'null' when no display name is set on the GitHub
  # profile — fall back to the username, then to a sensible default.
  GH_NAME=$(gh api user --jq .name 2>/dev/null || true)
  if [ -z "$GH_NAME" ] || [ "$GH_NAME" = "null" ]; then
    GH_NAME=$(gh api user --jq .login 2>/dev/null || echo "Andrew Cherry")
  fi
  git config --global user.name "$GH_NAME"
  echo "  → Set global git user.name = $GH_NAME"
else
  echo "  ✓ git user.name = $GIT_NAME"
fi

if [ -z "$GIT_EMAIL" ]; then
  # Default to GitHub's privacy noreply email — avoids needing the user:email scope.
  # If you want your real email here, change it manually after.
  GH_USER=$(gh api user --jq .login 2>/dev/null || echo "andrewpcherry")
  GH_EMAIL="${GH_USER}@users.noreply.github.com"
  git config --global user.email "$GH_EMAIL"
  echo "  → Set global git user.email = $GH_EMAIL"
else
  echo "  ✓ git user.email = $GIT_EMAIL"
fi

# ─── Step 5: Confirm remote + push ───────────────────────────────────────────
echo ""
echo "▶ Step 5/5: Pushing to $REMOTE_URL..."

if git remote get-url origin >/dev/null 2>&1; then
  CURRENT_REMOTE=$(git remote get-url origin)
  if [ "$CURRENT_REMOTE" != "$REMOTE_URL" ]; then
    echo "  → origin currently points to: $CURRENT_REMOTE"
    echo "  → updating it to: $REMOTE_URL"
    git remote set-url origin "$REMOTE_URL"
  else
    echo "  ✓ origin already points to $REMOTE_URL"
  fi
else
  echo "  → adding origin = $REMOTE_URL"
  git remote add origin "$REMOTE_URL"
fi

# Make sure we're on main
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "  → switching from $CURRENT_BRANCH to main"
  git branch -M main
fi

# Stage + commit anything new (the May 10 manual + Manual Mode manual + script)
if [ -n "$(git status --porcelain)" ]; then
  echo "  → there are uncommitted changes — committing them now"
  git add .
  git commit -m "May 10 audit deliverables: Manual Mode manual, patched SOPs, n8n cleanup log"
else
  echo "  ✓ working tree is clean"
fi

echo ""
echo "  → pushing to GitHub..."
if git push -u origin main; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  ✅ DONE. Repo is on GitHub."
  echo "  → https://github.com/andrewpcherry/agencyos"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
  echo ""
  echo "  ✗ Push failed. Most likely reasons:"
  echo "     • The remote repo doesn't exist yet — create it at:"
  echo "       https://github.com/new (name: agencyos, owner: andrewpcherry)"
  echo "     • Your GitHub account doesn't have access to that repo"
  echo "     • The .gitignore didn't catch a secret file (check the error above)"
  echo ""
  echo "  Re-run this script after fixing the issue. It's safe to re-run."
  exit 1
fi
