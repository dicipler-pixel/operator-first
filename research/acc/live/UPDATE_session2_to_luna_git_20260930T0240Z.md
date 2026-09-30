# session 2 → Luna + Git, 02:40Z: the doubling family, what the records are doing, and the open step

**Scale.** The family is bigger than the 36-row list. Every AC row with r1 = Y^(n+1) X y^n x is in it (2,372 rows). About 20 r0
variants form "doubling chains" whose records grow as 2^(n+1). From n = 6 to 10, most of those rows are k = 1. One route
per row that is **one move under the record** scores 1.0 on AC and again on Stable.

**Anchor chain: r0 = YXXyx** (Lisitsa's w\*, the relation y x Y = x x). Records: n5 80, n6 145, n7 275, n8 532, n9 1046, n10 2071.
They fit **2^(n+1) + 1.4·n + 9** within one move for every n. Other chains are this chain plus a short prelude.
For example, YXyXyx reaches (YxxyX, B) in 10 moves, and its records run 11–17 above YXXyx.

**What every route we can find looks like.** This includes the exact capped optimum from the C16 table (total length ≤ 16)
for YXXyx, which is 8 / 15 / 30 moves at n = 1 / 2 / 3.
1. Pump: rewrite y^n x Y^n into x^(2^n), one relation use at a time. Each use costs 2 moves: one multiply, plus one conjugation
   to bring the next site to the end.
2. Collapse: about 5 moves.
3. Strip: remove the run one letter per move.

Pump plus strip costs about 3·2^n moves, which is 1.5× the records from n = 5 on.

**Why the strip can't be shortened.** Every multiply changes the exponent-sum matrix of (r0, r1) by one row operation, and
conjugations don't change it. Once r1 holds y = x^D, the route needs at least D more multiplies. So any route that goes
through y = x^(2^n − 1) costs at least 2·2^n multiplies plus its conjugations.

**What the records must be doing.** They cost 2^(n+1) + O(n), which is exactly our pump cost with **no strip**. So the leaders
do the 2^n relation uses at about 2 moves each, but they mix orientations: some uses raise the x-exponent sum and some lower it.
The matrix stays shallow, and the route never holds y = x^(2^n − 1). A tool of mine that guides by syllables and matrix depth
found no route (n = 3 and n = 5, width 3000).

**The open step (Luna's job; Git's "eye" tools may help).** Find a derivation of a shallow relation that uses about 2^n
relation uses with balanced signs. Candidates:
- r1 = y (then r0 = A collapses to X in 2 multiplies, and the finish is 3 moves);
- a conjugate of x;
- anything whose exponent-sum row stays within a few units of the start.

Suggested ways in:
- (a) Expand the inner x of y^n x Y^n (sum +1 per use) and the outer X of B (X → Y X X y, sum −1 per use) alternately. Check
  whether some interleaving ends at a short relator.
- (b) Search the n = 3 and n = 4 YXXyx presentations for routes of length ≤ 29 / ≤ 47 with the capped beam. Reject any state
  whose exponent-sum depth exceeds 3; that forces the shallow shape.
- (c) Once a shallow n = 3 or 4 route exists, read its level structure and write the general-n constructor.

**Negatives to skip.**
- Plain beams: n = 5 YXyXyx ac-07182 at W 20000, depth 160, found no route. n = 6 was stopped.
- Pump-macro search up to 8 moves: never better than 1 x per 2 moves in the pump shape.
- Lisitsa's archive routes compile to 1,332–49,926 moves.

Files: `yxxyx_chain.py` (research/acc/optimality) is the 09-28 level-block generator (~3·2^n);
RIVAL_METHODS_20260928.md §5.7 has the same bound.

## Addendum 03:20Z (session 2): the one-line crux
- In BS(1,2) (y x Y = x x), B_n = y^n x Y^(n+1) X is conjugate to Y. The annular diagram has about 2^(n+1) cells: nested
  corridors 1+2+…+2^(n−1), plus one corridor of 2^n − 1. So every route needs about 2^(n+1) uses of the relation. The records
  (2^(n+1) + 1.4n + 9) therefore spend **about 1 move per use**.
- Our pump spends 2 moves per use: a multiply plus a one-letter re-alignment (conjugate r1, or conjugate r0 by one more x). A
  fixed appended relator can only insert whole blocks, never extend a run, and a relator worth k uses (x-sum k) cannot sit next to
  r1 because the exponent matrix must keep determinant ±1. Our strip reaches 1 move per unit only because r0 is then a
  conjugate of x.
- **Open question: an AC implementation of one y-corridor (y x^k Y → x^(2k)) at about 1 move per cell.** Answer that and a
  general-n constructor beats the whole family.
- More negatives: a beam limited to exponent-matrix depth ≤ 2 (YXXyx n=3 to depth 40, n=4 to depth 70, W 4000, length key) found
  no route, and a syllable/depth-guided beam found none at n=3 or n=5 (W 3000).
