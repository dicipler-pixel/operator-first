#!/usr/bin/env bash
# Commit one appended snapshot row, and refuse anything else.
#
# This runs with contents:write, so it is the one place in this repository
# where CI can alter the record. Every guard below exists because a scheduled
# job that quietly writes the wrong thing is worse than one that writes
# nothing:
#
#   * it will only ever stage SNAPSHOT_PATH;
#   * it refuses if anything else ended up staged;
#   * it refuses unless the diff is exactly one added line and none removed,
#     because an append-only ledger that loses a line is a corrupted one;
#   * it refuses to push to a branch outside ALLOWED_BRANCHES;
#   * it never force-pushes, and rebases onto the remote before pushing.
#
# Exit 0 with no commit is a normal outcome: nothing changed, or this branch is
# not one the series lives on.
#
#   SNAPSHOT_PATH=... ALLOWED_BRANCHES="main x" GITHUB_REF_NAME=x \
#     tools/acc/commit_snapshot_v1.sh
set -euo pipefail

SNAPSHOT_PATH="${SNAPSHOT_PATH:-ledger/timeline/snapshots_v1.jsonl}"
ALLOWED_BRANCHES="${ALLOWED_BRANCHES:-}"
BRANCH="${GITHUB_REF_NAME:-$(git rev-parse --abbrev-ref HEAD)}"
PUSH="${PUSH:-1}"

case " $ALLOWED_BRANCHES " in
  *" $BRANCH "*) : ;;
  *) echo "refusing to commit: $BRANCH is not in ALLOWED_BRANCHES"
     echo "the snapshot is still uploaded as a run artifact"
     exit 0 ;;
esac

git config user.name  "acc-timeline"
git config user.email "acc-timeline@users.noreply.github.com"

git add -- "$SNAPSHOT_PATH"
if git diff --cached --quiet; then
  echo "no new snapshot to commit"
  exit 0
fi

staged=$(git diff --cached --name-only)
if [ "$staged" != "$SNAPSHOT_PATH" ]; then
  echo "refusing: staged more than the snapshot ledger:"
  echo "$staged"
  exit 1
fi

stat_line=$(git diff --cached --numstat -- "$SNAPSHOT_PATH")
added=$(printf '%s' "$stat_line" | cut -f1)
removed=$(printf '%s' "$stat_line" | cut -f2)
if [ "$added" != "1" ] || [ "$removed" != "0" ]; then
  echo "refusing: expected exactly one appended line, got +$added -$removed"
  exit 1
fi

git commit -q -m "timeline: scheduled board snapshot" \
  -m "Appended one row to $SNAPSHOT_PATH by .github/workflows/acc-timeline.yml. No other file touched."

if [ "$PUSH" != "1" ]; then
  echo "committed locally (push disabled)"
  exit 0
fi

for i in 1 2 3 4; do
  if git pull --rebase --autostash origin "$BRANCH" \
     && git push origin "HEAD:$BRANCH"; then
    echo "snapshot committed to $BRANCH"
    exit 0
  fi
  sleep $((2 ** i))
done
echo "push failed after four attempts"
exit 1
