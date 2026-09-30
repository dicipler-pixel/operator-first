# t00092 notes: y-run hand construction on 6 unsolved MS rows

Prediction (before running): the ac-03855 / ac-04662 template (one multiplication cancels the y-run of w against the
MS relator, giving a single-x relator, then move to (x y^m, y) and peel) closes on ac-08441 in ~15-18 moves; if it
breaks, it breaks at the "move to (x y^m, y)" step.

Outcome: the template does not start on any of the 6 rows. The break is one step earlier than predicted: no single
multiplication by the MS relator shortens w, because the y-run sits in the wrong flank orientation.

## The orientation rule (checked on the pinned core, `work/orient.py`)

MS relator r1 = Y^(n+1) X y^n x gives exactly two shortening rewrites on a cyclic word (and their y<->Y mirrors):

- `X y^L x -> y^(L+1)` needs L = n  (shortens by 1)
- `x y^L X -> y^(L-1)` needs L = n+1 (shortens by 3)

So a y-run of length n must be flanked (X, x) and a run of length n+1 must be flanked (x, X). The zoom-out "y-run law"
only checked L, not the flanks.

| row | n | w | run / flanks | rule |
|---|---|---|---|---|
| ac-08441 | 4 | YYYYYxYXX | Y^5 flanked (X, x) | L = n+1 needs (x, X): wrong |
| ac-06010 | 4 | YYYYXXYYYx | Y^4 flanked (x, X) | L = n needs (X, x): wrong |
| ac-00724 | 3 | YYYYxYXX | Y^4 flanked (X, x) | wrong |
| ac-08692 | 3 | YYYYxxYX | Y^4 flanked (X, x) | wrong |
| ac-02255 | 3 | YYYXYYxx | Y^3 flanked (x, X) | wrong |
| ac-07069 | 3 | YYYXXYYx | Y^3 flanked (x, X) | wrong |

Solved siblings with the right orientation: ac-04662 (n=5, same w as ac-08441, X Y^5 x = X Y^n x) record 15, k=28;
ac-06244 (n=6, w=YYYYYYxYXX) 16, k=28; ac-09975 (n=3) 58; ac-02932 (n=4) 94. Every k>=28 short record in the list is a
right-orientation row. Siblings with no matching run at all still get solved at 35-60 (ac-00345 35, ac-02483 37,
ac-09758 38, ac-04282 46): those are search routes (build-up to ~43 letters, then collapse), not the template.

Across the 128 unsolved y-run rows (`soft_unsolved.json`): 102 have only wrong-orientation runs; 26 have a
right-orientation run, and their one-step rewrite lands on a wrong-orientation core, sometimes literally another
unsolved pool row: ac-02572 / ac-04158 (n=4, YYYYxxYXXX) -> Y^5 x Y X X = ac-08441's w at n=4; ac-08954 (n=3,
YYYYXXYYxxx) -> YYYXYYxx = ac-02255's w at n=3. So the 26 are not easier than the 102; they are the same cores plus
3-4 moves.

## What the template does at n=5 and why it fails at n=4 (ac-08441)

ac-04662 (n=5) route 15 = [7, 4, 3, 12, 2, 0, 1, 6, 5, 3x6]: conj r0 by X, then r1 <- r1 r0 = Y^6 X y^5 x X Y^5 x Y X
= Y^7 X, i.e. x = Y^7 after 2 moves; the rest is mechanical (Y^7 X and w give X Y^6, then (x y^6, y), 6 peels).
Same two moves at n=4: r1 <- Y^5 X y^4 x X Y^5 x Y X = Y^5 X Y x Y X (10 letters, no collapse). Every further single
multiplication returns w or a 9-10 letter word; by hand I could only derive length-9 relators equivalent to w
(y = x Y x y X^2, x = y^5 x^2 y, ...), never x = y^k.

Exact checks on the pinned core (`work/bfs.py`, all 14 moves, dedup):
- r0-only subgraph (r1 fixed = MS), cap 22, depth 9: 158 states, none with <= 1 x-letter.
- full, cap 22, depth 12: 84,535 states, none with a relator of <= 1 x-letter.
- full, cap 24, depth 11: 177,654 states, none with a relator of <= 1 x-letter.
Scope: total length <= 24 and depth <= 11/12 only. The sibling search routes peak at 43 letters, so a route through
longer states is not excluded by this.

## Beam runs (acc_beam, T9 finish, `work/drive.py` = t00091 driver with ART repointed)

See the "beam" section below (appended after the runs).
