# FABLE build update — first roads for the no-road MS/BS rows (2026-10-01, ~14:15Z)

Scope: four rows with no team road. Only the official core (`core.verify`, ac-r2-v1) is the judge; every length below is
the length of a path that returned `ok: True` on that exact row. Nothing was committed, pushed or submitted.
Doubling idea credited to Proof Track entry ACC-P000013 ("Baumslag–Solitar doubling in Miller–Schupp presentations").

Files:
- roads: `research/acc/live/inbox/fable_build_20261001.txt`
- builder: `tools/acc/upgh/fable_build.py` (`--n 9 --A 2` rebuilds and re-verifies both n = 9 rows; `reduce_n5_A4()` gives the n = 5 prefix)

## Results per row

| row | relation pair (twin_lookup.key) | result | method |
|---|---|---|---|
| ac-05169 | twin of msA(9, A=2) | **road, 143 moves; 139 after commute_clean** (record 88) | (n+1)-block doubling + y-elimination |
| ac-03786 | twin of msA(9, A=2) | **road, 151 moves** (record 94) | same canonical 134-move road, different paid symmetry prefix |
| ac-09026 | twin of msA(5, A=4) | no road | loop fragments; two reduced starts searched, see below |
| ac-02552 | twin of msA(5, A=4) | no road | same canonical presentation as ac-09026 |

Both n = 9 rows are symmetry twins of the single canonical presentation `(X y^9 x Y^10, x x Y Y X y y)`, and both n = 5
rows are twins of `(X y^5 x Y^6, x x Y^4 X y^4)` (checked with `twin_lookup.key`). So one canonical road per pair,
transferred with `bs_doubling.transfer` (paid prefix + relabelled body + BFS finish), verified on each row.

## The construction that worked (n = 9, A = 2)

ACC-P000013 section 5 states condition (T): the doubling loop needs |A| to divide n, because it rewrites the n-block of the
pump `X y^n x Y^(n+1)` with `Y^A x -> x x Y^A`. The BS relation `y^-A x y^A = x^2` equally gives `x y^A = y^A x x`, whose
inverse is the rule `Y^A X -> X X Y^A`, and that rule acts on the **(n+1)-block**:

    X y^n x Y^(n+1)  ~  Y^(n+1) X y^n x  ->  X^(2^((n+1)/A)) Y^(n+1) y^n x  =  X^(2^((n+1)/A) - 1) Y     when A | n+1.

So (T) is really "|A| divides n or n+1" (the n+1 case is the x -> X image of the n case, which keeps the BS relator up to
rotation/inversion). For n = 9, A = 2: 31 rewrites, each one move 3 (`r0 -> r0 r1^-1`, with r1 held at the rotation
`y y x x Y Y X`) plus single-letter conjugations of r0 that bring the site to the suffix; 85 moves to reach `r0 = X^31 Y`.
Finish: y = x^-31, so each of the four y-letters of r1 is rotated to the end of r1 and multiplied away by a rotation of
r0^±1 (moves 4/5), leaving r1 = x; then 31 moves 3 take r0 = y x^31 to y; BFS finish of 5 moves swaps to (x, y). Canonical
road 134 moves. The elimination finish is the fat part (~100 moves); the collapse itself is 85.

Checked on the small instances (n, A) = (1,2) 23, (3,2) 32, (5,2) 48, (7,2) 78, (3,4) 35, (7,4) 46 moves, all reaching the goal.

## What failed (n = 5, A = 4) — scope

Neither 5 nor 6 is divisible by 4, so both the n-block loop (paper) and the (n+1)-block loop (above) stop after one rewrite.
Exact replays from the canonical start (both prefixes in `reduce_n5_A4()`):

- 10 moves `[12,12,12,12,6,3,9,9,9,9]` -> S5 = `(y x Y Y X X, y^4 x x Y^4 X)`, 17 letters (this is the paper's
  "y-block deposited inside the x-block" state; group-theoretically r0 says x^-2 y x y^-2 = 1, i.e. the pump conjugated by y^4).
- 10 more moves (rule `x Y Y -> Y x x` read off r0, applied twice to r1) -> `(X X y x Y Y, y^4 x Y x Y x)`, 15 letters,
  the shortest state I reached. In letters w = x Y it reads `w^3 = y^-5` and `w^-1 y w = y w y^2`.

Searches run (one process at a time, nice 10, each under 10 min, `acc_beam` from `tools/acc/jev_handoff/src` with the T9
finish table `/root/.cache/upgh/T9.tab`):
- beam W = 100 000, depth 50, from the 15-letter state: no hit (kept lengths stayed 15–23).
- beam W = 250 000, depth 60, BEAM_LOOK=1, from S5: no hit (kept lengths 15–37).
No exhaustive statement follows from a beam; these are scoped misses, not non-existence.

Structural attempts, all abandoned with a reason:
- Idea (a), finishing identity on a small instance: the smallest same-residue analogue is n = 1 (A = 4); I did not search it,
  because a finish found there would still need a pattern in m = 2^floor(n/4) that I could not justify in the time.
- Idea (b), transfer from the n = 10 / n = 8 roads: the n = 5 pair has A = 4, not 2; no bridge attempted.
- Idea (c), Aut(F2): no automorphism keeps the BS relator in BS form except x -> X, y -> Y (which is what the (n+1) trick uses).
- Group derivation that does exist: from pump P and BS one gets x^-1 y^20 x = y^24, y^-20 x y^20 = x^32, y^-24 x y^24 = x^64,
  hence x^32 = 1 and the group collapses; equivalently P_4 := X y^20 x Y^24 satisfies (T) with A = 4. But P_4 = P · P^(y^-6)
  · P^(y^-12) · P^(y^-18) multiplies r0 by its own conjugates, which is not an AC move; every attempt to absorb P-conjugates
  through r1 consumed the BS relator (r1 = P^-1 afterwards), and the loop needs B as r1. I could not bootstrap it.

## Most promising next step for the n = 5 pair

Run the exact capped meet (`acc_capped` or `meet` mode, which the team already uses for optimality proofs) from the 15-letter
state `(X X y x Y Y, y^4 x Y x Y x)` with a cap around 18–20, and from `S5`; the 20-move prefix is exact and both states are
much smaller than the 24-letter row start, so a capped exhaustive run there is a different search than anything run on the
row itself. If that fails, search the n = 1, A = 4 analogue `(X y x Y Y, x x Y^4 X y^4)` exactly and look for a finishing
identity in the spirit of `finA2` that can be stated for the state `(Y x^m y y X, x x Y^4 X y^4)` with m = 2^q.

For the n = 9 pair, the fat part is the ~100-move elimination finish from `X^31 Y`; a finA2-style identity from the level-4
state `(Y Y X^16 y x, R1)` (search it at m = 1, 2, 4, 8 and generalise) should bring the road near the paper's 3m + c shape.
