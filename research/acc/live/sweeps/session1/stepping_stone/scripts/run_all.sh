#!/usr/bin/env bash
# Rerun the whole stepping-stone experiment without a model (about 1-2 h on 3 cores).
# usage: bash run_all.sh /path/to/sair-checkout     (run from the repo root: /home/user/operator-first)
set -euo pipefail
SAIR=${1:?sair checkout}
H=research/acc/live/sweeps/session1/handoff
O=research/acc/live/sweeps/session1/stepping_stone
SC=$O/scripts
W=$O/walks_cache; mkdir -p $W $O/runs
ROADS=$H/ALL_VERIFIED_ROADS_20261014.txt
python3 $SC/make_targets.py --sair $SAIR --csv $H/TARGETS_ALL_ROWS_20261014.csv --out $O
# idea B walk files (deterministic seeds)
python3 $SC/walks.py --bias band:12:18     --walks 10000 --steps 200 --seed 11 --out $W/w_g2_band.txt
python3 $SC/walks.py --bias profile:12:18  --walks 10000 --steps 200 --seed 12 --targets $O/targets_g2.csv --sair $SAIR --out $W/w_g2_profile.txt
python3 $SC/walks.py --bias balanced:12:18 --walks 10000 --steps 200 --seed 13 --out $W/w_g2_bal.txt
python3 $SC/walks.py --bias band:16:28     --walks 10000 --steps 150 --seed 21 --out $W/w_g1_band.txt
python3 $SC/walks.py --bias profile:16:28  --walks 10000 --steps 150 --seed 22 --targets $O/targets_g1.csv --sair $SAIR --out $W/w_g1_profile.txt
G2W="$W/w_g2_band.txt $W/w_g2_profile.txt $W/w_g2_bal.txt"
# pass 1: group 1 (1 process) + group 2 (2 processes, then the 3rd shard)
python3 $SC/stones_search.py --sair $SAIR --roads $ROADS --targets $O/targets_g1.csv --walks $W/w_g1_band.txt $W/w_g1_profile.txt \
  --out $O/runs/g1 --depth 12 --slack 8 --maxstates 1500000 &
for i in 0 1 2; do
  python3 $SC/stones_search.py --sair $SAIR --roads $ROADS --targets $O/targets_g2.csv --walks $G2W \
    --out $O/runs/g2_s$i --depth 12 --slack 6 --maxstates 2000000 --shard $i/3
done &
wait
# pass 2: group 2 deeper, with a radius-1 halo around every road state
for i in 0 1 2; do
  python3 $SC/stones_search.py --sair $SAIR --roads $ROADS --targets $O/targets_g2.csv --walks $G2W --halo 24 \
    --out $O/runs/g2deep_s$i --depth 40 --slack 8 --maxstates 3000000 --shard $i/3 &
done
wait
cat $O/runs/*_roads.txt | sort -u > $O/roads_new.txt
python3 tools/acc/plan_offline.py --sair $SAIR --out $O/scoring_lines.txt $O/roads_new.txt | tee $O/plan_offline_output.txt
