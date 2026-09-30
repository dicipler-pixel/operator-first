#!/usr/bin/env bash
# Commit and push the harness state (ledger, artifacts, plans, queue, WORKING_upgh.md) to the current
# branch. Serialised with flock so lanes, the cycle loop and a person never collide. In an ephemeral
# container an unpushed ledger is an unwritten Z, so this runs after every task and every cycle.
# usage: bash tools/acc/upgh/commit_state.sh "message"
set -u
cd "$(dirname "$0")/../../.." || exit 1
MSG=${1:-"UPG-H: state"}
BR=$(git rev-parse --abbrev-ref HEAD)
mkdir -p research/acc/upgh/cache
exec 9>research/acc/upgh/cache/git.lock
flock -w 300 9 || { echo "commit_state: lock busy" >&2; exit 1; }
git add research/acc/upgh research/acc/live/WORKING_upgh.md research/acc/live/queue research/acc/live/boards \
  research/acc/live/submit_log.jsonl research/acc/live/SCOUT_latest.md 2>/dev/null
git add ACC_QUEUE_*.txt ACC_SUBMIT_API_*.txt 2>/dev/null
# never commit a file over 50 MB (builder scratch once put 3.6 GB into a local commit and every push failed)
git diff --cached --name-only --diff-filter=AM | while read -r f; do
  if [ -f "$f" ] && [ "$(stat -c%s "$f")" -gt 50000000 ]; then
    git rm -q --cached "$f" && echo "commit_state: left out $f (over 50 MB)" >&2
  fi
done
if ! git diff --cached --quiet; then
  git commit -q -m "$MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019Eg5822oBrr1G75rKvNXKh" || exit 1
fi
for i in 1 2 3 4; do
  git fetch -q origin "$BR" && git merge -q --no-edit "origin/$BR" >/dev/null 2>&1
  git push -q origin "$BR" 2>/dev/null && exit 0
  sleep $((2 ** i))
done
echo "commit_state: push failed after retries" >&2
exit 1
