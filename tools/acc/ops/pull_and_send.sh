#!/bin/bash
# Owner's 06:50Z 09-30 rule: pull boards with every 30-min pull, and send verified lines as soon as they are ready.
# One run = pull_recent (1 API call) + board snapshots (2 calls) + offline rebuilds + (if the newest ready file has scoring
# lines and the budgets allow) one lean send (about 8 calls). Commits and pushes what it changed. Session 2 only.
# usage: bash tools/acc/ops/pull_and_send.sh [SCRATCH]
set -u
cd "$(dirname "$0")/../../.."
S=${1:-/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad}
NOW=$(date -u +%H:%MZ)
git pull -q --no-rebase origin claude/gallant-bardeen-0pgpae 2>&1 | tail -2
python3 tools/acc/ops/pull_recent.py
python3 -c "import sys; sys.path.insert(0, 'tools/acc'); import sair_api as s; s.pull_boards('research/acc/live/boards', leaderboards=False)"
python3 tools/acc/dashboard_data.py > /dev/null 2>&1
ACC_S=$S python3 tools/acc/ops/k12_targets.py
git add research/acc/live/RECENT_SUBMISSIONS.md research/acc/live/mine_recent.json research/acc/live/submit_log.jsonl \
        research/acc/live/SENT_ROWS.txt research/acc/live/dashboard.json research/acc/live/boards/ research/acc/live/TARGETS_K12_* 2>/dev/null
git commit -q -m "ACC: 30-min pull + boards $NOW

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HDg5qZWaFyKS9qc9tBTE37" 2>/dev/null

# send as soon as ready
F=$(ls OWNER_SUBMIT_2026*.txt 2>/dev/null | sort | tail -1)
if [ -n "$F" ] && grep -q '^s\?ac-' "$F"; then
  python3 tools/acc/plan_offline.py "$F" --sair "$S/sair" --out "$S/chk_asap.txt" | tail -3
  N=$(grep -c '^s\?ac-' "$S/chk_asap.txt" 2>/dev/null || echo 0)
  read UP LEFT < <(python3 - <<'EOF'
import re
t = open('research/acc/live/RECENT_SUBMISSIONS.md').read()
u = re.search(r'Uploads today \(UTC\): (\d+)', t); a = re.search(r'API calls left today: (\d+)', t)
print(u.group(1) if u else 99, a.group(1) if a else 0)
EOF
)
  if [ "$N" -gt 0 ] && [ "$UP" -lt 38 ] && [ "$LEFT" -ge 30 ]; then
    OUT=$(python3 tools/acc/sair_api.py send "$F" --yes --lean 2>&1); echo "$OUT" | tail -8
    SUB=$(echo "$OUT" | grep -o 'submission [0-9]*: complete.*' | tail -1)
    API=$(ls -t ACC_SUBMIT_API_*.txt 2>/dev/null | head -1)
    if [ -n "$SUB" ]; then
      mv "$F" research/acc/live/submitted/; [ -n "$API" ] && mv "$API" research/acc/live/submitted/
      T=$(date -u +%Y%m%d_%H%MZ)
      printf '# Ready for the next send (started %s, after %s). Stack verified lines below with a # comment line (row, source, length, record, k).\n' "$T" "$SUB" > "OWNER_SUBMIT_${T}.txt"
      echo "# ---- $NOW: $SUB (sent as soon as ready) ----" >> OWNER_STACK_20260929.txt
      python3 tools/acc/dashboard_data.py > /dev/null 2>&1
      git add -A research/acc/live/submitted/ "OWNER_SUBMIT_${T}.txt" OWNER_STACK_20260929.txt research/acc/live/submit_log.jsonl \
                 research/acc/live/SENT_ROWS.txt research/acc/live/dashboard.json research/acc/live/boards/; git add -u
      git commit -q -m "ACC: send as soon as ready ($NOW): $SUB

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HDg5qZWaFyKS9qc9tBTE37"
      echo "SENT: $SUB"
    fi
  else
    echo "ready file has $N scoring lines; uploads $UP/40, API calls left $LEFT: not sending"
  fi
else
  echo "nothing ready to send"
fi
git pull -q --no-rebase origin claude/gallant-bardeen-0pgpae 2>&1 | tail -2
git push -q origin claude/gallant-bardeen-0pgpae 2>&1 | tail -2
