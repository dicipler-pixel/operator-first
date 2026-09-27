#!/bin/bash
S=/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad; R=/home/user/operator-first; sig=""
while :; do
  cur="$(wc -l < $S/work/ties.jsonl 2>/dev/null)-$(wc -l < $S/work/sac_swap.jsonl 2>/dev/null)"
  if [ "$cur" != "$sig" ]; then
    cd $R/research/acc/optimality && python3 make_ties.py $S/work/ties.jsonl $S/work/rows.json $S/sair $R/ACC_TIES_20260924.txt > /dev/null 2>&1
    python3 make_sac.py $S/work $S/sair $R > $S/work/autobackup_last.txt 2>&1
    cp $S/work/ties.jsonl runs/2026-09-24/ties_partial.jsonl; [ -f $S/work/sac_swap.jsonl ] && cp $S/work/sac_swap.jsonl runs/2026-09-24/sac_swap_partial.jsonl
    cd $R && git add ACC_*20260924* research/acc/optimality && git commit -qm "ACC ties + Stable AC: backup (ties/swap rows $cur)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01B1kuzz5XCRpjgsfCqZSo3d" && for i in 1 2 3 4; do git push -q origin claude/gallant-bardeen-0pgpae && break; sleep $((2**i)); done
    echo "$(date -u +%H:%M) rows $cur: $(tail -1 $S/work/autobackup_last.txt)"; sig="$cur"
  fi
  kill -0 $(cat $S/work/sac.pid) 2>/dev/null || { [ "$cur" = "$sig" ] && break; }
  sleep 30
done; echo AUTOBACKUP_DONE
