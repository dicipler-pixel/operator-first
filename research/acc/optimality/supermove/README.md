# Supermove solve-first tools (session 2, 2026-09-29)

Our own C/Python implementation of the ACSolverX substitution supermove idea (Math & AI Lab at Caltech, MIT license,
commit 6a12515; method only, no data or paths used). Purpose: find a FIRST route on rows where we have none.

- `smbeam.c`: class-space beam (words up to rotation+inversion, unordered pair). Move = replace x by
  cred(rot(x)·rot(y^±1)) with a cancelling junction. Output: the class road. `gcc -O2 -o smbeam smbeam.c`
  usage `smbeam W DMAX LCAP SEED l0 w.. l1 w..` (letters 1,-1,2,-2).
- `smbeam2.c`: cost-aware version. Tracks the real relators and the official move cost (rotations = conjugations,
  one multiplication, cyclic reduction). usage `smbeam2 W DMAX LCAP SEED LS LG EXTRA l0 w.. l1 w..` (we use LS 16, LG 2).
- `compile_direct.py ROW ROAD`: smbeam class road -> official ac-r2-v1 moves (verified with the official core).
- `compile_exact.py ROW ROAD`: smbeam2 actual road -> official moves at exactly the beam's cost.
- `skel_dp_local.py`: Git's road-keeping DP (session 3). With tight bounds (GROW 1-2, MAXC 8, SLACK 3) it shortens a
  compiled route in seconds (ac-08371 40 -> 35; ac-09317 65 -> 58).
- `sm_lane.py TARGETS OUT W DMAX LCAP TMAX [SEEDS]`: lane runner (smbeam -> compile_direct -> verify), resumable.
  env `ACC_S` = scratch dir holding `sair/competition/tools` (the official verifier and manifest); `SMBEAM` = binary path.

Pilot (10 single-team rows, records 42-55, where best-first 60M nodes and the two-eyes beam found nothing):
routes on 7/10 in 14-25 s each, 2-3x the record raw. Current use: first-solve sweep over the 2,672 unsolved rows.
