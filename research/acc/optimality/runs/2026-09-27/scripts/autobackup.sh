#!/bin/bash
S=/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad; R=/home/user/operator-first; P=$(cat $S/work/ties.pid); n=0
while :; do
  m=$(wc -l < $S/work/ties.jsonl)
  if [ "$m" -gt "$n" ]; then
    cd $R/research/acc/optimality && python3 make_ties.py $S/work/ties.jsonl $S/work/rows.json $S/sair $R/ACC_TIES_20260924.txt > $S/work/autobackup_last.txt 2>&1
    cp $S/work/ties.jsonl runs/2026-09-24/ties_partial.jsonl
    cd $R && git add ACC_TIES_20260924.txt ACC_TIES_20260924.txt.verify.json research/acc/optimality && git commit -qm "ACC ties: backup ($m/42 rows processed)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01B1kuzz5XCRpjgsfCqZSo3d" && for i in 1 2 3 4; do git push -q origin claude/gallant-bardeen-0pgpae && break; sleep $((2**i)); done
    echo "$(date -u +%H:%M) backed up $m rows: $(head -1 $S/work/autobackup_last.txt)"
    n=$m
  fi
  kill -0 $P 2>/dev/null || { [ "$(wc -l < $S/work/ties.jsonl)" -eq "$n" ] && break; }
  sleep 30
done
echo AUTOBACKUP_DONE
