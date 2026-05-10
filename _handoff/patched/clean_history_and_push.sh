#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Clean git history + push.
#
# What this does:
#   1. Removes the leftover .git/index.lock (if present)
#   2. Creates an orphan branch (no parent commits → no history)
#   3. Adds the current (redacted) working tree
#   4. Commits as a single fresh baseline
#   5. Replaces `main` with the orphan branch
#   6. Force-pushes to GitHub (overwrites remote completely)
#
# Why orphan branch and not history rewrite (e.g. git filter-repo)?
#   - filter-repo requires an extra Homebrew install
#   - the AgencyOS git history has only 2 commits — no value worth preserving
#   - orphan branch is bash-only, foolproof, and removes the secret commit
#     entirely (no trace of `7c7fcb9` remains)
#
# What you LOSE:
#   - Git history. There will be one commit after this runs. The "7c7fcb9
#     AgencyOS state for CC audit" and "25aa7b0 May 10 audit deliverables"
#     commits are gone forever.
#   - That's the whole point — they contained the leaked Slack token and
#     could not be safely pushed.
#
# What you KEEP:
#   - Every file currently in your working tree (with the .md secret already
#     redacted by Cowork)
#   - Your gh authentication
#   - Your remote URL setting
#
# Safe to re-run. Idempotent.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

REPO_DIR="/Users/andrewcherry/Documents/Claude/Projects/Agency OS"
REMOTE_URL="https://github.com/andrewpcherry/AgencyOS.git"   # mixed-case is the canonical name
COMMIT_MSG="AgencyOS clean baseline — 2026-05-10 (post-audit, secrets redacted)"

cd "$REPO_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  AgencyOS clean-history push"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ─── Step 0: sanity ──────────────────────────────────────────────────────────
echo ""
echo "▶ Step 0: Sanity check — confirm no live Slack bot token literal in the redacted .md file"
# Pattern matches any xoxb- bot token (3 numeric segments + 20+ char secret).
# Pattern itself is NOT a valid token — won't trigger GitHub Push Protection.
if grep -qE 'xoxb-[0-9]+-[0-9]+-[A-Za-z0-9]{20,}' AgencyOS_Fix_Thread_Prompt.md 2>/dev/null; then
  echo "  ✗ AgencyOS_Fix_Thread_Prompt.md STILL contains a Slack bot token literal."
  echo "    Stop and redact it before running this script."
  exit 2
fi
echo "  ✓ AgencyOS_Fix_Thread_Prompt.md is clean."

# ─── Step 1: clear the index lock ────────────────────────────────────────────
echo ""
echo "▶ Step 1: Clearing .git/index.lock if present"
if [ -f .git/index.lock ]; then
  rm -f .git/index.lock
  echo "  ✓ Removed leftover index.lock"
else
  echo "  ✓ No index.lock present"
fi

# ─── Step 2: confirm gh remote URL is correct ────────────────────────────────
echo ""
echo "▶ Step 2: Pointing origin at $REMOTE_URL"
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE_URL"
else
  git remote add origin "$REMOTE_URL"
fi
echo "  ✓ origin = $(git remote get-url origin)"

# ─── Step 3: create orphan branch ────────────────────────────────────────────
echo ""
echo "▶ Step 3: Creating orphan branch (no parent commits → no leaked history)"
# If a previous run left clean-baseline behind, kill it
if git show-ref --verify --quiet refs/heads/clean-baseline; then
  git branch -D clean-baseline
fi
git checkout --orphan clean-baseline
echo "  ✓ Now on orphan branch 'clean-baseline'"

# ─── Step 4: stage + commit current working tree ─────────────────────────────
echo ""
echo "▶ Step 4: Staging + committing current (redacted) working tree"
git add -A
git commit -m "$COMMIT_MSG"
NEW_SHA=$(git rev-parse --short HEAD)
echo "  ✓ Created clean commit $NEW_SHA"

# ─── Step 5: replace main with the orphan branch ─────────────────────────────
echo ""
echo "▶ Step 5: Replacing main with the clean orphan branch"
if git show-ref --verify --quiet refs/heads/main; then
  git branch -D main
fi
git branch -m clean-baseline main
echo "  ✓ main is now the clean baseline"

# ─── Step 6: force push ──────────────────────────────────────────────────────
echo ""
echo "▶ Step 6: Force-pushing to GitHub (overwrites the remote completely)"
echo "  → push target: $REMOTE_URL"
if git push --force --set-upstream origin main; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  ✅ DONE. Repo is on GitHub at:"
  echo "     https://github.com/andrewpcherry/AgencyOS"
  echo ""
  echo "  ⚠️  YOU STILL NEED TO ROTATE THE SLACK BOT TOKEN."
  echo "     The leaked value (xoxb-9815813665076-...) is no longer in your"
  echo "     git repo, BUT it was on your local Mac for ~24h and remains valid"
  echo "     in Slack until you revoke it. Treat it as compromised."
  echo ""
  echo "     30-second walkthrough — Cowork will give you the exact clicks."
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
  echo ""
  echo "  ✗ Push failed. Most likely reasons:"
  echo "     • Push Protection still found a secret somewhere we missed"
  echo "       → screenshot the error and send to Cowork; we'll grep + redact"
  echo "         the additional location and re-run this script."
  echo "     • gh authentication expired"
  echo "       → run: gh auth status (and re-auth if needed)"
  echo ""
  echo "  Safe to re-run this script after fixing the issue."
  exit 1
fi
