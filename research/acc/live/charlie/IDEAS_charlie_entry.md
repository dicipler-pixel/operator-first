## Charlie, 2026-09-28: the memory wall is down, and the rotate-and-cut pattern

**What was built.** `acc_disk` is an exact frontier BFS under a total-length cap for `ac-r2-v1`. Every layer sits on disk as a sorted file. The official move table is closed under inversion, so the capped graph is undirected, and each new layer only has to be checked against the two before it. Nothing is pruned or quotiented: states are raw ordered pairs.

- **Controls:** the moves match `core.apply_move` on 56,056 applications. The trivial component matches to cap 12. The certified closures of ac-02842 (cap 18) and ac-00738 (cap 21) match. ac-03467 at cap 23 closes at 158,016,512 states, in 4 minutes and 2.4 GB. The board's own completed runs ac-03060, ac-03871 and ac-02452 give identical state counts.
- **Two-sided exactly like the board runs:** forward to depth record − 9, meeting a trivial ball of radius 9 (183,402,071 states, built under cap 36, which covers every row's cap). The first meeting layer a, together with the smallest ball depth t among the meeting states, gives the exact shortest length under the cap, a + t. No meeting by the last layer is a certificate: no path as short as the record under that cap.

**Results on the stalled board runs** (full list in `ledger/charlie_exact_disk_runs.jsonl`):

- ac-03719: TIE, 37 = record 37, cap 35. 37 is optimal under cap 35.
- ac-02528: BEAT, 35 < record 37, cap 32 (the team's run stalled here at 211M states; this one finished at 533M).
- Certified, no path ≤ record under the cap: ac-08428 (caps 31 and 32), ac-05818 (25, 26), ac-01638 (33, 34), ac-01304 (27, 28), ac-06737 (24), ac-00587 (28), ac-02381 (29), ac-04011 (35).

**The pattern.**

1. **Rotate and cut.** The ac-03719 tie is about 24 rotations and 13 cuts out of 37 moves. A conjugation by a relator's own end letter turns the word one place. After a few turns, one multiplication cancels a whole block: step 6 takes the total from 35 to 23. In 45 of the 76 ledger rows, and in 7,526 of the 10,115 AC pool rows, the shorter relator sits whole inside the longer one as a cyclic block, so that first cut is always there.
2. **Cap = starting total hides the answers.** 74 of the 76 board runs used cap = starting total. The certified rows show their records must rise above the start at some point. The one beat came from one of the only two rows whose cap sat above the start. Re-run the certified rows at cap = start + 1, + 2, + 3 (queued).
3. **Greedy chaining is not the optimum.** Cutting greedily down to a small core and then looking the core up in the stored trivial component (T16) or the radius-9 ball gives 270 verifier-accepted complete paths, with no search. But they are long: 52 against 34 and 51 against 36 where the record is known. They are useful only for rows that are still unsolved (`cutchain_lines.txt`; label them with `plan_offline.py`). The optimal paths take cuts that sometimes grow the total first.

**Stable AC.** Moves 0–13 are identical in `sac-r8-v1`, so any AC path followed by destabilize r1, then r0 (moves 16, 15) is a Stable path of length + 2. Accepted: sac-03719 (39), sac-02528 (37), and 270 carries of the chain lines.
