#!/bin/bash
# SCRIPT: NEWTARGET_BEAM  team beam rebuilt from current source; production flags; free depth record+20; W 100000
S=/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad
ARGS=$(python3 -c "
import sys;sys.path.insert(0,'$S/acc_private/pool/ACC_Replay_Idea_Pool');import replay_loop as rl;T=rl.load_targets();E={1:0,-1:1,2:2,-2:3}
r0,r1=T['$1']['initial_relators'];print(len(r0),*[E[t] for t in r0],len(r1),*[E[t] for t in r1])")
BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 $S/upgh/acc_beam_port $S/win/T8.tab 100000 $2 $ARGS > $S/upgh/nt_$1.out 2> $S/upgh/nt_$1.err
