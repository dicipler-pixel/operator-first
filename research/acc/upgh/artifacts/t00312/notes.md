# t00312 notes (UPG-H builder, claim 9856c555429b25cbebaeeb16; rerun of t00297)

Started 2026-10-01 (UTC). Wall limit 60 min. Rows: the 14 MS(n, w*) rows n=4..10 of family f-0ce69b0475.

## Prediction (written before running anything)

- (1) Level change: I expect to find an O(1) level change by never cyclically reducing / keeping the active
  site at the end of r0 (working with r0 as a non-cyclically-reduced word is allowed by the core: free reduction
  only). If this works, the canonical lengths should drop from 53/92/163/300/567/1092/2131 towards the
  P000013 constant-2 numbers (50/85/148/291/539/1064/2078) or below; a rough bound is sum over levels of
  (2^L multiplications + O(1)) + finish = 2^n + O(n) + |fin2| = 2^n + 2m + O(n) = 2*2^n + O(n).
  Beating the board records (n=4 48, n=7 278, n=10 2071 ...) needs also (2).
- (2) Short finish: fin2(m) costs 2(m-1)+13 = 2m+11 moves. An m+O(1) finish would make the road ~1.5*2^n+O(n),
  which beats every record from n=7 up. I think this is hard; my expectation is that I find at most a partial
  improvement (e.g. a finish of about 1.5m) or nothing, and the honest outcome is a scoped miss on (2).
- Null outcome: no row gets a path <= its live record (contract prediction). Any path shorter than our own BS
  road (59/62, 100/105, 171/177, 315/308, 575/583, 1109/1100, 2139/2149) still goes into lines.txt.

## Log

### Math for (1), level change (derived before coding)

Cyclic word at level L: x^a y^b X Y^c with a = 2^L, b = n+1-L, c = n-L (r0 of MS(n) inverted and rotated).
Two doubling rules come from r1 = x x Y X y: "Y x -> x x Y" (Y moves right through the x-block) and
"x y -> y x x" (y moves left through the x-block). A rule can only be applied by a right multiplication
r0 <- r0 r1^(+-1) at the END of the stored word, so a rule whose site moves right needs the site at the end of
W (orientation 1: r0 = W, r1 stored as rho = X y x x Y, move 2), and a rule whose site moves left needs the site
at the FRONT of W, i.e. at the end of W^-1 (orientation 2: r0 = W^-1, r1 stored as rho' = y x x Y X, move 3,
because W <- (y x x Y X) W is W^-1 <- W^-1 (x y X X Y) and (y x x Y X)^-1 = x y X X Y).
Within a pass each step is 1 multiplication + 1 single-letter conjugation (7 in orientation 1, 6 in orientation 2),
the last step has no conjugation: a pass of a steps costs 2a-1.
Orientation-1 pass: W = x^(a-1) P x, P = y^b X Y^c  -->  W = P' x^(2a) Y, P = P' Y   (a mults, a-1 moves 7)
Level change 1->2: W' = x Y . W . y X (moves 9 then 6), invert (0), r1: rho -> rho' (move 10): 4 moves.
Orientation-2 pass on r0 = W'^-1 = X^(2a-1) y^(c-1) x Y^(b-1) X: 2a mults (move 3), 2a-1 moves 6,
ending at r0 = y^(c-1) x Y^(b-2) X^(4a) Y.
Level change 2->1: invert (0), 9, 7, r1: rho' -> rho (11): 4 moves. Back to the orientation-1 form with a := 4a.
The identity is the same string rewrite at each level (induction on L), so it holds for every n; code replays it.
Expected canonical cost: sum_L (2^(L+1)-1) + 4(n-2) + setup + bridge + fin2(m) = 2^(n+1) + 3n + O(1).

### Measured (bs_alt.py, first run; every assertion in alt_loop passed for n = 2..7)
Canonical lengths (best of the two start orientations): n=4 52, n=5 88, n=6 154, n=7 286
(old bs_doubling.py: 53, 92, 163, 300; P000013 constant-2: 50, 85, 148, 291; records 48/50, 80/83, 145/149, 278/275).
Transferred: ac-01784 56, ac-04042 59 (not shorter than our 56/57), ac-01950 90, ac-05586 98, ac-02033 159,
ac-06018 166, ac-00676 298, ac-06796 288. Row frame (prefix + finish from g(goal)) costs 2-12 moves per row.

### Run 2 (prefix re-optimisation: enter the loop after its first k<=6 moves by a bidirectional BFS over all 14 moves,
### depth 4 per side, total length capped; suffix re-optimisation: replace the last k<=8 moves by a BFS finish)
Canonical lengths (best of the two start orientations), n=2..10: 22, 34, 52, 88, 154, 286, 544, 1060, 2086.
  (old bs_doubling.py: n=4..10 53, 92, 163, 300, 567, 1092, 2131; P000013 constant-2: 50, 85, 148, 291, 539, 1064, 2078;
   board records n=4..10: 48/50, 80/83, 145/149, 278/275, 532/538, 1051/1046, 2071/2079.)
Per level: pass of a = 2^L steps costs 2a-1 (1 multiplication + 1 conjugation per step, no conjugation after the last);
level change 4 moves; loop entry 2-3 moves; bridge into fin2 4 moves (orientation 2 end) or 6 (orientation 1 end);
fin2(m) = 2m+11.  Total = 2^(n+1) + 3n + 8 +- 2.  The records are about 2^(n+1) + 2n + 3, so this closes the gap to
the records to 6-15 moves per row but does not tie any of them. No road here ties or beats a board record (as predicted).
Transferred rows in run 2 before the fallback fix: ac-01784 54 (ours 56), ac-04042 53 (57), ac-01950 88 (100),
ac-05586 96 (105), ac-02033 153 (171), ac-06796 286 (308), ac-03079 543 (575), ac-06727 1060 (1100), ac-00106 2085 (2139);
five rows (ac-06018, ac-00676, ac-03773, ac-03984, ac-01523) had no road because the 8-move prefix search cannot
rotate their long relator; run 3 adds a rotation-only fallback for those.

### (2) The short finish: what was tried, what failed
- fin2(m) traced for general m (notes above in code comments): after [4,1,11,3,8,4] the pair is
  (x^m y x^(m-1) y, Y Y X^(m-1) y x^(m-1) y x^(m-1) y); the m-1 conjugations [7]*(m-1) rotate r0 to x y x^(m-1) y x^(m-1)
  so that r1 r0^-1 collapses to Y X^m; then (y x^(m-1), x) Euclid: [5]*(m-1). Multiplications in fin2: m+6, which is
  within O(1) of the exponent-matrix minimum for [[m-1,1],[1,0]] -> I, so an m+O(1) finish must remove the m-1
  conjugations, i.e. produce the aligned rotation of r0 for free.
- Bidirectional BFS over all 14 moves (total length capped at the state length + 8) between the state before the
  rotation and the state after it: no path of <= 8 moves at m = 8 (the rotation itself, 7 moves, is returned as
  shortest) and no path of <= 10 moves at m = 16 (rotation 15). Scoped miss: depth 8 / 10, two values of m, length cap.
- Bidirectional BFS from the loop-end state to each of the first 7 states of fin2 (n = 4, 5): nothing shorter than the
  rotation bridge + fin2 prefix. Scoped miss (depth 8 / 10).
- Stopping two levels early does not help by itself: the finish from (Y Y x^(m/2) y^3 X, r1) has exponent matrix
  [[m/2-1,1],[1,0]] but no known identity; fin2's alignment trick (r1 <- r1 r0 then r0 <- r0 r1^-1) uses the single Y.
- Not found: an m+O(1) finish. Nothing here says one does not exist.

### Run 3 (final; rotation-only fallback for the prefix). All 14 AC lines replayed again in a fresh process with
### verifier.core.verify(challenge, path, "ac-r2-v1", manifest["limits"]) from the official start: 14 ok, 0 bad.
| row | n | new road | our BS road | board record |
|---|---|---|---|---|
| ac-01784 | 4 | 54 | 56 | 48 |
| ac-04042 | 4 | 53 | 57 | 50 |
| ac-01950 | 5 | 88 | 100 | 80 |
| ac-05586 | 5 | 96 | 105 | 83 |
| ac-02033 | 6 | 153 | 171 | 145 |
| ac-06018 | 6 | 164 | 177 | 149 |
| ac-00676 | 7 | 296 | 315 | 278 |
| ac-06796 | 7 | 286 | 308 | 275 |
| ac-03079 | 8 | 543 | 575 | 532 |
| ac-03773 | 8 | 556 | 583 | 538 |
| ac-03984 | 9 | 1072 | 1109 | 1051 |
| ac-06727 | 9 | 1060 | 1100 | 1046 |
| ac-00106 | 10 | 2085 | 2139 | 2071 |
| ac-01523 | 10 | 2100 | 2149 | 2079 |
lines.txt holds these 14 AC lines and the 14 Stable lines (moves + [16, 15]); roads.jsonl the same as JSON lines.
The relator-swapped rows (ac-06018, ac-00676, ac-03773, ac-03984, ac-01523) still pay 10-14 frame moves
(long-relator rotation in the prefix, g(goal) -> goal at the end); the others 1-2.

### Scope, honestly
- PROVED (for every n, by the induction step written above; each pass's output word is asserted in alt_loop and
  the assertions held for n = 2..10): the alternating-orientation loop with a 4-move level change
  [0, 9, 6, 10] (orientation 1 -> 2) / [0, 9, 7, 11] (orientation 2 -> 1). Claimed identity: with
  W = x^(a-1) y^b X Y^c x and r1 = X y x x Y, the sequence (2, 7)^(a-1), 2 gives W = y^b X Y^(c-1) x^(2a) Y;
  then 0, 9, 6, 10 gives (X^(2a-1) y^(c-1) x Y^(b-1) X, y x x Y X) and (3, 6)^(2a-1), 3 gives
  y^(c-1) x Y^(b-2) X^(4a) Y; then 0, 9, 7, 11 returns to the orientation-1 form with a := 4a, b := b-2, c := c-2.
- MEASURED (not proved optimal): canonical lengths 2^(n+1) + 3n + 8 +- 2; the fin2 bridge and the row frames were
  found by bounded BFS and are shortest only within their depth/length caps.
- NOT FOUND: an O(1) level change cheaper than 4 moves (argument in notes: one inversion is forced because the two
  chaining rules act at opposite ends of W, and one r1 rotation is forced because no single stored word r1 has both
  X y x x Y and x y X X Y among {r1, r1^-1}); and the m+O(1) finish (scoped misses listed above).
- No road here ties or beats a board record; every road beats our own current BS road for its row.
