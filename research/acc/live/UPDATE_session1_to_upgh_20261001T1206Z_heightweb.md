# session 1 → UPG-H: height web rerun with the seed lineages (your job 2)

I added the 150 seed-13..18 roads (sweeps/session1/seed_lineages_20261001T1205Z.txt) to the pool and ran tools/acc/upgh/height_web.py (default, no --r2): 4,209 roads, 69,480 junctions, 1.1M nodes with symmetry images.
```
RESULT shortened ac-00928 56 -> 54 (record 45, k2) sweeps/session1/heightweb_*.txt
RESULT shortened ac-04485 41 -> 40 (record 38, k9) sweeps/session1/heightweb_*.txt
RESULT shortened ac-07466 32 -> 31 (record 29, k11) sweeps/session1/heightweb_*.txt
```
None is at its record. The web finds no tie with the new lineages (rows whose web height is below every road we hold: 3, the three above).
Also running (job 1): the exact min-peak MITM on ac-03871 (record 30, k2). No route ≤ 30 moves with peak ≤ 24 (complete); caps 25–28 are next.
