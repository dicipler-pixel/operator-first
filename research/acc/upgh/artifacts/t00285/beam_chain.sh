#!/bin/bash
# t00285 restart-beam chain: one acc_beam at a time (2-process budget shared with acc_capped).
A=/home/user/operator-first/research/acc/upgh/artifacts/t00285; B=~/.cache/upgh/bin/acc_beam; T=~/.cache/upgh/T9.tab
run() { # tag width dmax env... -- enc
  tag=$1; W=$2; D=$3; shift 3; envs=(); while [ "$1" != "--" ]; do envs+=("$1"); shift; done; shift
  echo "[$tag] start $(date -u +%T) W=$W DMAX=$D env=${envs[*]} state=$*" >> $A/beam_chain.log
  env "${envs[@]}" timeout 300 $B $T $W $D "$@" > $A/beam_$tag.out 2> $A/beam_$tag.err
  echo "[$tag] end $(date -u +%T) rc=$? $(grep -c PATH $A/beam_$tag.out) hits; $(tail -n1 $A/beam_$tag.err)" >> $A/beam_chain.log
}
[ -e /home/user/operator-first/research/acc/upgh/STOP ] && exit 0
run 09632_tot15_div0.6 20000 300 BEAM_DIV=0.6 -- 8 3 1 2 2 2 0 0 3 7 2 2 2 1 3 0 0
[ -e /home/user/operator-first/research/acc/upgh/STOP ] && exit 0
run 05538_tot17_div0.6 20000 300 BEAM_DIV=0.6 -- 8 3 1 2 2 2 0 0 3 9 2 2 2 2 1 3 3 0 0
[ -e /home/user/operator-first/research/acc/upgh/STOP ] && exit 0
run 05538_start_div0.6 20000 400 BEAM_DIV=0.6 -- 8 3 3 3 0 2 2 1 1 13 3 3 3 3 3 3 1 2 2 2 2 2 0
[ -e /home/user/operator-first/research/acc/upgh/STOP ] && exit 0
run 09632_start_H1 20000 300 BEAM_H=1 BEAM_DIV=0.6 -- 8 3 3 3 0 2 2 1 1 11 3 3 3 3 3 1 2 2 2 2 0
echo "[chain] done $(date -u +%T)" >> $A/beam_chain.log
