# Orders for Luna: the Miller–Schupp doubling chains (2026-09-28)

## What we were missing
We have been searching row by row. The board isn't random rows. It is **Miller–Schupp families**
MS(n,w) = < x, y | y^-(n+1) x^-1 y^n x , w >, n = 1..10, with 1,006 different short second words w.
(3,363 rows, 1,977+ of the 2,672 unsolved rows.) Data: `ledger/ms_families_by_w_20260928.json`
({"w|pos": {n: [record, teams, id]}}; pos 1 = the MS relator is r1 and w is r0).

For 10 second words, every n = 3..10 is solved and the record is **2^(n+1) + small**:

| w (r0) | n=3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| YXyXyx | 32 | 56 | 91 | 158 | 288 | 547 | 1061 | 2088 |
| YXXyx | – | – | 80 | 145 | 275 | 532 | 1046 | 2071 |
| YYxyXYx | 40 | 66 | 105 | 173 | 304 | 564 | 1079 | 2107 |
(full list in the ledger file; 10 chains)

**68 of these rows are held by 1–2 teams; most by 1.** Stable AC on them is exactly AC + 2, also 1–2 teams.
A k=1 tie is a full point. **One matched row ≈ 2 points (AC + Stable AC). Our whole score is ~2.4.**
Nobody finds a 2,088-move path by search. The leaders have a **construction**, and so can we.

## How the construction works (checked on our own paths)
- w = YXXyx is the Baumslag–Solitar relation y^-1 x^2 y = x. Every chain word collapses to it.
- The path grows a run of x's, 2 per two moves with the pair (move 5 = r1 <- r1·r0^-1, then 11 = conjugate r1
  by x^-1), up to x^(2^n - 1). Then it peels the run with move 2 (r0 <- r0·r1), one letter per move.
  Build ≈ 2^n, peel ≈ 2^n, so the length is 2^(n+1) + overhead. Records fit 2^(n+1) + about 1.5n + 8.5 for YXXyx.
- Our beam on MS(n, YXXyx) (made-up rows, not on the board): n=3 **29** (= the formula),
  n=4 **55** = prefix(18) · (5 11)^7 · 5 · [12 6 1 3 10 4] · 2^13 · [4 1 2]. The formula says about 47, so
  our prefix/middle is about 8 moves too long. Exact windows up to 14 don't shorten it.

## Who does what
- **Session 1 (me):** w = YXXyx. Write `ms_construct.py`: path(n) for any n, verified by the official verifier,
  then exact-search the non-repeating parts (prefix, middle, suffix) to hit the record exactly.
- **Luna:** the other 9 chains. For each w:
  1. Find the shortest move sequence that turns (w, MS_n) into a state where one relator is the BS relation
     (YXXyx or a mirror/rotation of it). Use our small made-up rows n = 1, 2, 3 and exact search:
     `ACC_SCRATCH=<folder with acc_capped and work/T9.tab> python3 tools/acc/ms_exact.py <w> <n> <cap> <maxd>`
     (cap = start length + 2 works for n <= 3; raise it for n = 4).
  2. Check whether that prefix is the same for every n, or grows by a fixed block per n. Write it down as a rule.
  3. Then prefix + my YXXyx construction = path(n) for that chain. Verify every n = 3..10 with the official
     verifier and compare with the record (`plan_offline.py`). Tie = inbox.
- **Stable AC beat (both):** Stable AC can finish from (y,x) with [15,15]. If our road reaches (y,x) one move
  sooner than (x,y), then SAC = record - 1 on a 1-team row: a **beat**. The n=4 beam path already had SAC = AC + 1.

## Rules
- Put paths only in the inbox after the official verifier accepts them. Session 2 sends.
- Log every n tried, cap, states, complete or incomplete, in `research/acc/live/ledger/`.
- Watch the disk: exact runs with no cap write huge layer files (one used 20 GB today). Use a length cap.

## Also open (lower priority)
- 106 second words where small n is solved and bigger n is not (e.g. YXYxYx: n=2 solved, n=3..10 unsolved by
  every team). If a chain construction works there, each row is a first solve (1 point).
- 480 more MS rows are written in rotated/inverted/mirrored spellings (256 unsolved). Normalize before grouping.
