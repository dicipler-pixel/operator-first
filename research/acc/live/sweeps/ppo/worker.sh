#!/bin/bash
# Claims 20-key chunks of data/unsolvedM.txt (atomic mkdir) and runs the 610model beam search on each; resumable.
S=/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad; R=$S/acsx_run; cd $R || exit 1
W=${1:-1024}; N=1156; C=20
for ((s=3; s<N; s+=C)); do
  e=$((s+C)); [ $e -gt $N ] && e=$N
  mkdir claims/chunk_$s 2>/dev/null || continue
  $S/acsx_venv/bin/python /home/user/math-ai-caltech/acsolverx/beam/beam_search.py --ckpt_path 610model --dataset unsolvedM \
     --training_dataset train157217 --start $s --end $e --beam_width $W --max_steps 150 --out_csv out/chunk_$s.csv > logs/chunk_$s.log 2>&1
  echo "$(date -u +%H:%MZ) chunk $s-$e rc $? $(grep -c SOLVED logs/chunk_$s.log) solved" >> progress.txt
done
