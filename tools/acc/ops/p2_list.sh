#!/bin/bash
# usage: p2_list.sh NAME W   P2 beam (BEAM_P2=2: P2 lookahead, then H priority) + window-14 over $S/work/NAME_targets.json
# -> $S/work/NAME_cap.jsonl (watch_sweeps.py sees hits: ac_len <= ac_record or sac_len <= sac_record).
# Needs $S/p2bin/acc_beam -> acc_beam built with BEAM_P2 (research/acc/optimality/acc_beam.c) and a finish table:
# T8 ($S/p2beam/T8.tab, 640 MB) by default, T9 if P2_TABLE=T9.
# P2_DUAL=0.75 (with P2_ELITE=5000): the 13:00Z winner, "two eyes" (ledger/dual_beam_ab_20260928.json): 3/4 of the beam by
#   the P2 key with quota/elite, 1/4 by plain H; binary $S/p2ybin/acc_beam = acc_beam_y (acc_beam.c at HEAD).
# P2_ELITE=5000: the earlier A/B winner (P2=2 + BEAM_QUOTA=16 + BEAM_ELITE=5000, binary $S/p2xbin/acc_beam = acc_beam_x).
S=${ACC_S:-/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad}; R=/home/user/operator-first
TF=$S/p2beam/T8.tab; [ "$P2_TABLE" = T9 ] && TF=$S/work/T9.tab
[ -f $S/work/$1_cap.jsonl ] || cp $R/research/acc/live/sweeps/$1_cap.jsonl $S/work/ 2>/dev/null
BIN=$S/p2bin; [ -n "$P2_ELITE" ] && BIN=$S/p2xbin; [ -n "$P2_DUAL" ] && BIN=$S/p2ybin
env BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 ${P2_ELITE:+BEAM_QUOTA=16 BEAM_ELITE=$P2_ELITE} ${P2_DUAL:+BEAM_DUAL=$P2_DUAL} python3 $R/research/acc/optimality/run_beam_raw.py $S/sair/competition/tools/verifier/data/manifest.json \
  $BIN $TF $S/work_$1 $2 600 $S/work/$1_cap.jsonl $S/work/$1_targets.json >> $S/work/$1_cap.log 2>&1
