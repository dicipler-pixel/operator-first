# Longline: road hooks in the beam's end table (2026-11-15)

Sonar, chum/longline and match-the-hatch, tried on ac-07337 (AC 41 vs record 40) and sac-00989 (Stable 38 vs 37).

- `acc_opt_8bit.patch`: table distances widened from 4 to 8 bits (fingerprint loses 4 of 128 bits). Apply to
  research/acc/optimality/acc_opt.c; build acc_beam (with ../ballmap/acc_beam_loop.patch if wanted) against it.
- `sonar.py OUT`: replays every road in ACC_ROUNDUP_20261020/moves (19,789 roads, AC and Stable prefixes), marks
  collapse positions (new running minimum after a 1.5x peak: 49,864, 77% within 10 moves of the finish) and writes
  `records.txt` (320,103 distinct states with moves left <= 255).
- `bait OLD_T8 records.txt OUT NSLOTS`: converts T8 to 8-bit, adds every record under all 16 AC symmetries
  (8 signed letter permutations x 2 relator orders; offset = T8 distance of the image finish), relaxes to a fixpoint
  (states sorted by distance first: 70 passes, 13 min) and checks every entry has an exact d-1 neighbour.
  Result: 2,660,126 hooks at distances 9..255 on top of 24,587,144 T8 states; 64M slots, 1.0 GB.
- `probe TABLE LURES AC_T ST_T EDITS start...`: replays lure roads (and all one-move edits) on a start and looks up
  every prefix (and its letter swap) in the table. `startscan TABLE starts.txt`: every row's start against the table.
- `gradtest.py`: which mixer reading slopes toward the finish (700 best roads, 32,713 states).

Results (no tie or beat anywhere):
- Lures: 13,591 roads as-is on both starts; 222 (ac-07337) and 140 (ac-00989) sibling roads with all one-move edits
  (341k / 151k variants). Best = our own lengths.
- Start scan over all 10,115 rows: no beats; 6 joins on rows with k >= 13.
- Hooked beam from the start, W 100000: ac-07337 AC 41 / Stable 43, ac-00989 AC 36 / Stable 40 (our own roads' hooks).
- Gradual readings: loop at z 5-8 ranks moves-left best (Spearman 0.51 vs letters 0.455) but goes downhill on only
  52% of road steps (letters 61%); six-ratio average 0.50 / 50%; axis angle is anti-correlated (-0.07 to -0.31).
  The loop is a position indicator, not a per-move gradient.
