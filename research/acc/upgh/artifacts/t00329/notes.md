# t00329 notes (UPG-H builder, claim 99a5b6206b6d599c83a040ad; follow-up to t00312)

Started 2026-10-01 06:25Z. Wall limit 60 min. Rows: the 14 MS(n, w*) rows n=4..10 (family f-c85238088e).
Question (Astra audit): a different finish entry, or a paid finish, that avoids fin2's linear rotation [7]*(m-1),
counting every frame change. Do not repeat the bounded m=8/16 BFS probes.

## Prediction (written before running anything)

- Exponent-matrix view (P000013 section 3, re-derived below): the multiplications of fin2 are forced once the road
  passes through the x-exponent pair (M, 1); only the m-1 conjugations [7]*(m-1) are not covered by that bound.
  The board records are 2^(n+1) + 2n + 3 = 4m + 2n + 3 (m = 2^(n-1)) for n >= 7, i.e. the record holders also pay
  ~4m moves (2m multiplications + ~2m conjugations). An m+O(1) finish would give ~3m roads, far below every record;
  I do not expect to find one. I expect at most a constant saving (a few moves) in the finish entry / bridge, which
  can matter only for n = 4 (gap 52 vs 48/50) and maybe n = 5.
- Null outcome (contract prediction): no row gets a path <= its live record. Any road shorter than the current row
  road (54/53/88/96/153/164/296/286/543/556/1072/1060/2085/2100) goes into lines.txt.
- What each outcome means: a finish of 2m + c with c < 11 + bridge from the loop end -> all 14 rows shorten by a
  constant (no record unless c saves >= 4 at n=4). A finish of (1+eps)m + O(1) -> every row from n = 7 up beats its
  record. A beam/best-first search that finds nothing is a scoped miss, not evidence of non-existence.

## Log

### 06:36Z  Exponent-matrix floor (measured by BFS over row operations, entries capped at 4M; conjugations free)
Row ops = moves 0..5 (negate / r0 +- r1 / r1 +- r0) on the (x, y) exponent-sum rows. Conjugations do not change them.
| m | fin2 entry [[m-1,1],[1,0]] -> I | fin2 row ops (m+7) | two-levels-early [[m/2-1,1],[1,0]] -> I | current (last pass m/2 + fin2 m+7) |
|---|---|---|---|---|
| 4 | 5 | 11 | 3 | 13 |
| 8 | 9 | 15 | 5 | 19 |
| 16 | 17 | 23 | 9 | 31 |
| 32 | 33 | 39 | 17 | 55 |
So from the fin2 entry the abelian floor is M+2 = m+1 row ops (path: r0 -= r1 (M-1 times), negate r1, r1 += r0, r0 -= r1);
fin2 spends m+7 row ops and m+4 conjugations. The floor is not achievable by words with r1 = x x Y X y in any
rotation (see the cancellation table below: no product of a rotation of r0^{+-1} = x^m y y X Y with a rotation of
r1^{+-1} shortens r0, so the x-block cannot be stripped one x at a time), which is why the word-level finish is 2m+O(1), not m+O(1). This floor bounds row ops only;
it says nothing about conjugations, so it neither forces nor forbids the [7]*(m-1) rotation.

Record arithmetic (inference, not proof): records are 2^(n+1)+2n+3 = 4m+2n+3 for n >= 7. With the same pass cost
(2a-1 per level: the a multiplications are forced by the floor, the a-1 conjugations are not), a 3-move level change
gives 4m - n - 1 + 3(n-2) + c = 4m + 2n + 3 for c = 10, i.e. a prefix+finish constant of ~10 (ours is 11+5+2 = 18); a 4-move level change would need a finish constant of 12-n,
impossible for large n. So the records are consistent with 2m multiplications + ~2m conjugations; nobody on the board
has an m+O(1) finish. The realistic target for this family is the level-change count and the finish constant, not
the linear rotation.

### 06:33Z-07:00Z  Candidates (a), (b): beam search from the loop-end states (fin_probe.py, acc_beam + T9 exact finish)
States probed (exact words at the end of the alternating loop, from loop_levels(n, orient, levels)):
  n=4 one level early  O1 (y^3 X Y x^8 Y, X y x x Y) current finish 33 = bridge 6 + fin2(8) 27
                       O2 (y y x Y Y X^8 Y, y x x Y X) current finish 31 = bridge 4 + fin2(8) 27
  n=4 two levels early O1 (y^3 x Y^3 X^4 Y, y x x Y X) current 44 ; O2 (y^4 X Y Y x^4 Y, X y x x Y) current 42
  n=5 one/two levels early likewise (current finishes 47/49 and 62/64).
Depth cap DMAX = current finish - 1 (a hit must be strictly shorter). Keys: plain length (W = 200000), BEAM_H=1
(W = 200000), BEAM_CLIMB=6 (W = 50000). Results are in beam_summary.jsonl / beam_*.log (one JSON line per state):
every run returned AC NONE within the cap (BEAM_H=1 returned finishes of 40 and 38 = depth + ball distance, longer
than the current 33 / 31).
CONTROL (beam_control.log): with DMAX = current finish (slack 1) the beam at W = 50000, with and without CLIMB, does
NOT reproduce the known finish from either n=4 loop-end state. fin2 passes through total length 5m+3 = 43 at m = 8
while the beam keeps states of length 9..41 and prefers short ones. So the beam null results only say: no finish whose
states stay inside the beam's selection; they are NOT evidence against fin2-shaped (grow-then-collapse) finishes.
Scoped miss, weak.

### 06:38Z-06:46Z  Candidate (c): multiplications instead of the rotation (macro_probe.py, exact, replayed on the core)
Model: from A(m) = (x^m y x^(m-1) y, Y Y X^(m-1) y X) (the state after fin2's first five moves [4,1,11,3,8]), a route is
<= K blocks of [conjugation run on r0 (<= len+2), conjugation run on r1, optional inversions, one multiplication 2..5];
cost = exact number of official moves (Dijkstra; conjugations of different relators commute, so this covers every move
sequence with <= K multiplications whose conjugation runs lengthen a relator by at most 2). fin2 reaches the class of
Y X^m (rotations of (Y X^m)^(+-1)) from A in m+2 moves: 4, [7]*(m-1), 12, 5.
  m=4,  K=2, budget 6:  cheapest route to the Y X^m class = fin2's own [4,7,7,7,12,5] (cost 6). No other at that cost.
  m=8,  K=2, budget 10: cheapest = fin2's own [4,7*7,12,5] (cost 10).
  m=8,  K=3, budget 9:  NO route with <= 3 multiplications and <= 9 moves reaches the Y X^m class (exhaustive).
  m=16, K=2, budget 17: (see macro_K2_m16.out; running at 06:46Z)
So within three multiplications the [7]*(m-1) rotation cannot be bought by r1 <- r1 r0^(+-1) tricks at m = 8: the
cheapest way to the collapse product Y X^m is the rotation. Scope: K <= 3, m <= 8 (m = 16 at K = 2), target = the
Y X^m class only (a finish not passing through Y X^m is not excluded by this); conjugation runs that lengthen a
relator by more than 2 letters are not enumerated.
Side result: 4 moves [9,2,10,2] from A reach (Y x y X X, x Y Y X^(m-1) y X X) = (r1_0^-1, conj of Y Y X^(m-1) y X),
total length m+9: the roles of the relators swap (short BS relator in r0, the x^(m-1) relator in r1). Not shorter
to finish from; recorded because it is the only state of total length <= 2m+2 within 4 moves of A at m = 8.

### Candidate (d): exponent-matrix guidance (table at 06:36Z)
The row-op floor from the fin2 entry is m+1 and from two levels early m/2+1; fin2 uses m+7 row ops. The floor cannot be
met by words with r1 = x x Y X y (cancellation table: max 6 letters cancel in any product of rotations of r0^(+-1) and
r1^(+-1); the only shortening products are the single doubling/halving steps). The floor does not count conjugations.
Cancellation table at m = 8 (all 2(m+4) rotations of r0^(+-1), r0 = x^m y y X Y class, times all 10 rotations of
r1^(+-1)): only two products shorten r0, both by one letter: x^7 y y X Y x * X y x x Y = x^7 y y x Y and its mirror
Y Y X^8 y x * X Y x y X = Y Y X^7 y X (the halving step X Y x -> x Y). No product strips an x from the x-block.

### Level-change arithmetic (derived, not searched; relevant because the records' gap is linear in n, not in m)
With rho = X y x x Y kept in r1 for both orientations (O2 uses move 3: U Y -> U X X Y x, which is the same cyclic
rewrite as U' Y X -> U' X X Y), the O2 pass costs 2a (a multiplications + a conjugations) and the O2->O1 level change
3 moves (invert, de-wrap, rotate); with the stored rotation of t00312 the pass costs 2a-1 and the change 4. Both give
2a+3 per level. The y...Y wrapper after a pass is forced because the site Y|x occurs once in the cyclic word, so W
must end with Y x and start with the y-block. A 3-move-per-level scheme (what the records' 4m+2n+3 suggests) needs a
different representation (e.g. a longer r1 that doubles two letters at a time, or a pass whose last step is merged
with the change); not explored here.

## Scope, honestly (what is proved, what is measured, what is missing)
- PROVED (exact enumeration, replayed on the official core): from A(8) = (x^8 y x^7 y, Y Y X^7 y X), no move
  sequence with <= 3 multiplications, <= 9 moves and conjugation runs lengthening a relator by <= 2 reaches the
  Y X^8 class; fin2's rotation route (10 moves) is the cheapest with <= 2 multiplications at m = 4 and m = 8.
  Abelian floor from the fin2 entry: m+1 row ops (BFS over exponent matrices, entries <= 4M); fin2 uses m+7.
- MEASURED (scoped misses): acc_beam from the four n=4 loop-end states (one and two levels early, both
  orientations), W = 200000 (plain and BEAM_H=1) and W = 50000 (BEAM_CLIMB=6), depth cap = current finish - 1:
  no finish. The control at depth cap = current finish does not reproduce the known finish at W = 50000, so these
  probes do not cover grow-then-collapse finishes. n = 5 and m = 16 runs: see the end of this file (cut by the wall).
- NOT FOUND: a different finish entry, or a paid finish, cheaper than bridge + fin2(m); nothing here says one does
  not exist. No road shorter than the current row roads was produced, so lines.txt is not written.
- Inference (not proof): the records 4m+2n+3 are consistent with 2m multiplications + ~2m conjugations and a 3-move
  level change; the open m+O(1) finish is not something any board record demonstrates.

### 07:04Z  End of run (stopped by me at 07:04Z, 21 min before the hard wall, to leave time for the write-up)
- n=5, one level early, O1 start state (y y x Y Y X^16 Y, y x x Y X), current finish 47, W = 200000, DMAX 46:
  plain key AC NONE; BEAM_H=1 AC NONE. The remaining n=5 states (O2 one level early; both two levels early) were
  cut by the wall: not covered.
- macro_probe m=16 K=2 budget 17: cut by the wall after 22 min (Python); not covered.
- No STOP file appeared. All background jobs (fin_probe.py x2, macro_probe.py, their acc_beam children) killed.
- lines.txt: not written (no road shorter than any current row road).
Files: fin_probe.py (beam probe + transfer/replay), macro_probe.py (exact macro enumeration), beam_summary.jsonl
(one line per beam run), beam_len.log / beam_h1.log / beam_climb.log / beam_control.log / beam_test.log (raw acc_beam
output), macro_K2.out / macro_K3_m8.out (macro results), run_*.out (stdout of the background runs).
