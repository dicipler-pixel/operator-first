#!/bin/bash
# First-solve beam on Bob's unsolved clusters: one representative per class, production beam flags (Git's nt lane),
# W 100k, depth 80 + exact T8 finish. A road on any member carries to its whole cluster (Bob's bridges + symmetry).
R=/home/user/operator-first; B=$HOME/.cache/acc_beam_bin; D=$R/research/acc/live/sweeps/beam_clusters; i=$1
export BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75
mkdir -p $HOME/.cache/acc_beam_work/c$i
cd $R && python3 tools/acc/jev_handoff/src/run_beam.py $HOME/.cache/upgh/sair $B $B/T8.tab $HOME/.cache/acc_beam_work/c$i 100000 80 $D/out_$i.jsonl $D/targets_$i.json >> $D/log_$i.txt 2>&1
git add $D && git commit -q -m "acc: cluster first-solve beam shard $i finished [skip ci]" -m "$(printf 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_019Eg5822oBrr1G75rKvNXKh')" && for k in 1 2 3 4; do git push -q origin HEAD:claude/gallant-bardeen-0pgpae && break; sleep $((2**k)); done
