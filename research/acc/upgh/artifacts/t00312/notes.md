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
