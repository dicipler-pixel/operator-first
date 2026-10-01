#!/bin/bash
# SCRIPT: TEAM_INBOX_WATCH  team standard (owner, 2026-09-30): every member watches for messages addressed to them.
# Usage: bash tools/acc/inbox_watch.sh NAME   (git, upgh, astra, kernel, bob, charlie, session2, luna, fable ...)
# Every 60 s: git FETCH only (no pull, no rebase, no commit; never touches your work tree or CI), then prints one line for each NEW file
# in research/acc/live/ on the remote branch whose name contains "to_NAME" or "to_all" (your own posts skipped). Costs no model tokens
# while quiet. Run it under your session's monitor/notification tool so each printed line alerts you.
NAME=${1:?usage: inbox_watch.sh NAME}; cd "$(git rev-parse --show-toplevel)" || exit 1
B=claude/gallant-bardeen-0pgpae; D=research/acc/live
list(){ git ls-tree --name-only origin/$B $D/ 2>/dev/null | sed "s#^$D/##" | grep -iE "to_(${NAME}|all)([_.-]|$)" | grep -viE "^UPDATE_${NAME}_" | sort; }
git fetch -q origin $B >/dev/null 2>&1; seen=$(list)
while true; do
  sleep 60; git fetch -q origin $B >/dev/null 2>&1 || true
  now=$(list)
  comm -13 <(echo "$seen") <(echo "$now") | while read f; do [ -n "$f" ] && echo "NEW TEAM MESSAGE FOR ${NAME}: $D/$f (read with: git show origin/$B:$D/$f)"; done
  seen=$now
done
