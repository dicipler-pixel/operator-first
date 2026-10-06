#!/bin/bash
# Beam + exact finish (T8) + window shortening on the 6 single-holder rows with no road from us and records <= 40.
R=/home/user/operator-first; B=$HOME/.cache/acc_beam_bin; D=$R/research/acc/live/sweeps/beam_k1short
cd $R && python3 tools/acc/jev_handoff/src/run_beam.py $HOME/.cache/upgh/sair $B $B/T8.tab $HOME/.cache/acc_beam_work 100000 60 $D/out.jsonl $D/targets.json >> $D/log.txt 2>&1
git add $D && git commit -q -m "acc: beam on 6 short single-holder rows (results) [skip ci]" -m "$(printf 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_019Eg5822oBrr1G75rKvNXKh')" && for i in 1 2 3 4; do git push -q origin HEAD:claude/gallant-bardeen-0pgpae && break; sleep $((2**i)); done
