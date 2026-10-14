# UPG-H sealed song ideas (written before running anything; compare with the partner at ~02:55Z)

Song: "Same pulse underneath / How often it returns ..." (owner, 14 Oct). My target is memcon's ladder construction: 95 solo rows, 0.5 per tie.

1. **"Two pitches meet ... Bring it down. Count the throb" (heterodyne) + "Integer times a radio step, plus offset, plus the air".**
   - Beat memcon's ladder records against ours, rung by rung and ladder by ladder: the throb Δ(n), its first and second differences, and the even/odd-n split of the √ term.
   - If the √ coefficient depends on the parity of n, their construction splits the exponent n into halves (⌊n/2⌋ and ⌈n/2⌉). The per-ladder offsets give the constant joins.
   - Test: exact fits on the five ladders, n = 5..10.
2. **"Two different drums can sing the same set of quotes" (isospectral drums).**
   - Find every board row family whose records dropped this week by the same law (≈ 2^n + c·2^(n/2)). These are the rows where the construction already applies.
   - Find the rows still on the old law (≈ 2^(n+1) + c). These are untouched targets: a beat for whoever matches the construction first.
   - Test: MS ladder map (ladders.json, 307 ladders) against the boards of 6 Oct and 14 Oct.
3. (REVISED 02:05Z, before running: the n=6 loop beam is moot because exact tests show our loop levels are optimal; replaced by 3b below.) **"If the engine isn't clean, the early bloom can fool the record" + "Sample too slow and the high folds onto the low".**
   - Stop studying n <= 5, where memcon equals us. Study n = 6/7, where the gain is 23 / 56 moves.
   - Run a progress-scored loop beam (loop_beam.c) with ALL moves, wide, at n = 6. Use a rotation-penalizing tie-break, so the beam does not alias the rare multiplication-dense roads into rotation-heavy ones.
   - Test: does any n = 6 loop beat our canonical 72 moves?
3b. **"The twin on the far side of the cut" (the (y,x) twin).** sac-01784 is the n = 4 XXYxy rung: AC record 48 (k8, matching our canonical), but Stable record 49 (k1). Someone reaches (y,x) in 47 moves.
   - Test: exact bidirectional search from our pre-finish state P_8 to (y,x).
   - If the finish to (y,x) is 26 or less (fin2 is 27), map it into 01784's frame and add [15,15]. That ties at 49 (0.5).

## Results (written 02:51Z, before reading the partner's ideas)

1. **Heterodyne (beat our law against theirs): partly run, no scorer.**
   - Ladder offsets over XXYxy are near-constant (XYXYxy +11..+16; others +15..+35), so it is one construction plus a fixed-cost opening per ladder (addendum 00:55Z in TOP_TEAMS_METHODS_BESTGUESS).
   - √ coefficient c = (record - 2^n) / 2^(n/2) on the current board, n = 4..10:

     | ladder | n4 | n5 | n6 | n7 | n8 | n9 | n10 |
     |---|---:|---:|---:|---:|---:|---:|---:|
     | XXYxy | 8.00 | 7.42 | 7.50 | 8.22 | 9.38 | 8.75 | 9.62 |
     | XYXYxy | 9.75 | 9.37 | 9.00 | 9.28 | 10.25 | 9.46 | 10.12 |
     | XYXyxY | 9.75 | 9.19 | 8.88 | 9.28 | 10.25 | 9.37 | 10.09 |
     | XYYXyxY | 11.25 | 11.31 | 10.50 | 10.52 | 11.12 | 10.08 | 10.62 |
     | XYYXYxy | 12.50 | 11.84 | 10.88 | 10.69 | 11.31 | 10.21 | 10.72 |

   - From n = 8 on, odd n sits below both even neighbours on every ladder. That is the parity split the idea predicted: the √ part is built from ⌊n/2⌋ / ⌈n/2⌉ halves (a baby-step / giant-step finish), not from n itself. c also creeps up with n, so there is an extra slowly growing term. The fit is weak (3 points per parity), so it is a lead for the construction, not a road.
2. **Old-law rows (isospectral drums): MISS, nothing left.** All 30 exponential rungs with n >= 8 (the 5 ladders above x n = 8, 9, 10 x 2 twin rows) were on the old law (about 2^(n+1)) on 6 Oct. All 30 now sit on the new law, held by memcon.ai (29 at k1, one at k2). No exponential ladder row is still untouched, so a beat needs a road shorter than memcon's, not just the construction. The other 182 ladder rungs with n >= 8 have short records (well under 2^n) and are not on this law at all.
3b. **(y,x) twin finish for sac-01784: MISS.** The exact finish from our pre-finish state P_m to (y,x) equals fin2 at m = 3 and 4 (27 moves at m = 8 is not beaten by a 26), so the Stable 49 tie on sac-01784 is not reachable through our P_8. Its holder's road leaves our level states earlier.
