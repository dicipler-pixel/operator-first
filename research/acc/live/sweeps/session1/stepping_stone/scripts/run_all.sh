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
python3 $SC/walks.py --bias band:12:34     --walks 10000 --steps 300 --seed 31 --out $W/w_g2_climb.txt
python3 $SC/walks.py --bias band:14:34     --walks 10000 --steps 200 --seed 32 --seed-roads $ROADS --seed-minlen 14 --sair $SAIR --out $W/w_g2_waypt.txt
G2W="$W/w_g2_band.txt $W/w_g2_profile.txt $W/w_g2_bal.txt"
# pass 1: group 1 (1 process) + group 2 (2 processes, then the 3rd shard)
python3 $SC/stones_search.py --sair $SAIR --roads $ROADS --targets $O/targets_g1.csv --walks $W/w_g1_band.txt $W/w_g1_profile.txt \
  --out $O/runs/g1 --depth 12 --slack 8 --maxstates 1500000 &
for i in 0 1 2; do
  python3 $SC/stones_search.py --sair $SAIR --roads $ROADS --targets $O/targets_g2.csv --walks $G2W \
    --out $O/runs/g2_s$i --depth 12 --slack 6 --maxstates 2000000 --shard $i/3
done &
wait
# pass 2: group 2 at cap 28 (>= the proven peak 26 for AK(3)/MS rows), halo + climbing and waypoint walks
for i in 0 1; do
  python3 $SC/stones_search.py --sair $SAIR --roads $ROADS --targets $O/targets_g2.csv --walks $W/w_g2_climb.txt $W/w_g2_waypt.txt \
    --halo 30 --out $O/runs/g2deep_s$i --depth 40 --slack 8 --capmin 28 --maxstates 1500000 --shard $i/2 &
done
# group 1 again with a radius-1 halo and donor attribution
python3 $SC/stones_search.py --sair $SAIR --roads $ROADS --targets $O/targets_g1.csv --halo 40 --out $O/runs/g1halo \
  --depth 12 --slack 8 --maxstates 1500000 &
wait
# gap-1/2 rows with a bigger budget
python3 - <<PY
import csv
R={r['row']:r for r in csv.DictReader(open('$H/TARGETS_ALL_ROWS_20261014.csv',newline=''))}
open('$O/targets_g1_gap12.csv','w').write(''.join(l for l in open('$O/targets_g1.csv') if R[l.split(',')[0]]['status'].strip() in ('gap 1','gap 2')))
PY
for i in 0 1 2; do
  python3 $SC/stones_search.py --sair $SAIR --roads $ROADS --targets $O/targets_g1_gap12.csv --halo 40 --out $O/runs/g1gap12_s$i \
    --depth 20 --slack 10 --maxstates 5000000 --recon 80 --shard $i/3 &
done
wait
# controls on 80 SOLVED short rows (targets_control_B.csv, seed 7 sample): walks only (B) and roads+halo (A)
python3 $SC/stones_search.py --sair $SAIR --roads /dev/null --targets $O/targets_control_B.csv \
  --walks $W/w_g2_band.txt $W/w_g2_profile.txt $W/w_g2_bal.txt $W/w_g2_climb.txt --out $O/runs/controlB --depth 12 --slack 6 --maxstates 1500000 --recon 20 &
python3 $SC/stones_search.py --sair $SAIR --roads $ROADS --targets $O/targets_control_B.csv --halo 40 --out $O/runs/controlA \
  --depth 12 --slack 6 --maxstates 1500000 --recon 20 &
wait
cat $O/runs/g1*_roads.txt $O/runs/g2*_roads.txt | sort -u > $O/roads_new.txt   # (the shipped file also drops roads already in the pool)
python3 tools/acc/plan_offline.py --sair $SAIR --out $O/scoring_lines.txt $O/roads_new.txt | tee $O/plan_offline_output.txt
