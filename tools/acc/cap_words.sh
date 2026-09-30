#!/bin/bash
# exact capped search from arbitrary words: cap_words.sh R0 R1 CAP MAXD [BUDGET]
S=${ACC_SCRATCH:-.}
ENC=$(python3 -c "
import sys
E={'x':0,'X':1,'y':2,'Y':3}; a,b=sys.argv[1],sys.argv[2]
print(' '.join([str(len(a))]+[str(E[c]) for c in a]+[str(len(b))]+[str(E[c]) for c in b]))" $1 $2)
W=$S/work_cw_$$; mkdir -p $W
MAXD=$4 INIT_LOG2=24 $S/acc_capped $S/work/T9.tab $3 ${5:-100000000} $W cw $ENC 2>/dev/null | tail -3
rm -rf $W
