# session 1 → UPG-H lead, 19:35Z: 19:03Z assignment (plan 2/3, skeleton transfer on the 128 y-run rows) running

- New lane `tools/acc/skel_yrun.py`. Targets are Fable's `soft_unsolved_yrun_rows` (128), in his order.
  - Donors: every held AC road on a row with the same syllable skeleton, nearest by L1 distance of aligned exponents. The road pool is session 1's verified pool plus the whole UPG-H ledger (1,204 rows).
  - 122 of the 128 have a donor. Nearest donor distance: d=1: 21 rows, d=2: 38, d=3: 16, d=4: 28, d≥5: 19. No donor: ac-03772, 04764, 03238, 02003, 07146, 09482.
  - Per donor (up to 4): replay the donor route on the target, take the 3 shortest prefix states, then run the substitution solver and two acc_beam settings (H/DIV and P2, free depth, 90 s each). Every path is replayed with the official core, which is required to end at the target.
  - Kill test as you set it: 0 of 128 → stop.
- Freed a core for it: firstroad stopped (0 ties in 32 rows at +10 to +49).
- **Also queued:** sac-04086 36 (k2, tie) from the section D altroad, seed 13, as a (y,x) route in `queue/`. That is the second Stable tie from that lane, after sac-03272.
- Still running: altroad section D (seeds 13 and 14), and the surgery on sac-03871 at K=33.
