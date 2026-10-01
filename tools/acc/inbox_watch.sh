#!/bin/bash
# SCRIPT: TEAM_INBOX_WATCH  team standard (owner, 2026-09-30): every member watches for messages addressed to them.
# Usage: bash tools/acc/inbox_watch.sh NAME   (NAME as used in file names: git, upgh, astra, kernel, bob, charlie, session2 ...)
# Every 60 s: git pull, then print one line for each NEW file in research/acc/live/ whose name contains "to_NAME"
# (for example UPDATE_upgh_to_git_*.md) or "to_all". The check runs in the shell and costs no model tokens; only a printed line
# (a real new message) reaches the session. Run it under your session's monitor/notification tool so each line alerts you.
NAME=${1:?usage: inbox_watch.sh NAME}; cd "$(git rev-parse --show-toplevel)" || exit 1
BR=claude/gallant-bardeen-0pgpae; D=research/acc/live
list(){ ls $D | grep -iE "to_(${NAME}|all)([_.-]|$)" | grep -viE "^UPDATE_${NAME}_" | sort; }   # skip your own posts
seen=$(list)
while true; do
  git pull -q --rebase origin $BR >/dev/null 2>&1 || true
  now=$(list)
  comm -13 <(echo "$seen") <(echo "$now") | while read f; do [ -n "$f" ] && echo "NEW TEAM MESSAGE FOR ${NAME}: $D/$f"; done
  seen=$now; sleep 60
done
