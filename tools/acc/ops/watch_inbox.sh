#!/bin/bash
# Wake the lead when a session pushes a new inbox or exchange file (or a non-API ACC_SUBMIT_* file). Private ref only.
cd /home/user/operator-first || exit 1
SEEN=${ACC_S:-/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad}/work/inbox_seen.txt
list() { git ls-tree -r --name-only refs/watch/lead 2>/dev/null | grep -E '^research/acc/live/(inbox|exchange)/[^/]+\.[a-z]+$|^ACC_SUBMIT_[^/]*\.txt$' | grep -v '^ACC_SUBMIT_API_' | sort; }
git fetch -q origin +claude/gallant-bardeen-0pgpae:refs/watch/lead 2>/dev/null
[ -f "$SEEN" ] || list > "$SEEN"
end=$(( $(date +%s) + 8*3600 ))
while [ "$(date +%s)" -lt "$end" ]; do
  sleep 180
  git fetch -q origin +claude/gallant-bardeen-0pgpae:refs/watch/lead 2>/dev/null || continue
  NEW=$(comm -13 "$SEEN" <(list))
  if [ -n "$NEW" ]; then echo "NEW FILES FROM SESSION 1:"; echo "$NEW"; list > "$SEEN"; exit 0; fi
done
echo "no new inbox files in 8h"
