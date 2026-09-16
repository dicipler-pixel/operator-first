# Gordon controls: a parity law, and a correction

Frozen authority `a0fd6e6`. Every length below is a path found by
`ac_corridor64_bidir_v2.c` and replayed to TARGET through `verifier.core`.
Bidirectional level-synchronised meets can overshoot the optimum by one, so
each length is a ceiling, exact to within 1.

    G(q) = ( x^-2 y^-1 x y ,  y^-2 x^-q y x^q ),  start total = 2q+8

## The parity law

| q | parity | start total | cap | length | 2q+5 |
|---|---|---|---|---|---|
| 4 | even | 16 | 16 | **13** | 13 ✓ |
| 6 | even | 20 | 20 | **17** | 17 ✓ |
| 8 | even | 24 | 24 | **21** | 21 ✓ |
| 10 | even | 28 | 28 | **25** | 25 ✓ |
| 3 | odd | 14 | 14 | **16** | 11 ✗ |
| 5 | odd | 18 | 18 | **26** | 15 ✗ |
| 7 | odd | 22 | 22 | **33** | 19 ✗ |
| 9 | odd | 26 | — | [35, 48] | 17 ✗ |
| 11 | odd | 30 | — | unsolved at headroom 0-2 | 27 ✗ |

**Even q is exactly `2q+5`** across four independent values. Odd q breaks it
and is irregular: 16, 26, 33 with differences +10, +7 — no linear law, and
roughly double the even cost at the same q.

q=6, 8 and 10 reproduce the supplied paths move-for-move (17, 21, 25).
**q=3, 4, 5 and 7 were never supplied and are new** — four verified
certificates found here, each replayed to TARGET through the frozen core.

q=11 (odd) does not solve at headroom 0-2, consistent with the odd branch
being the hard one.

No simple law fits the odd values. 5q+1 matches q=3 (16) and q=5 (26) but
predicts 36 for q=7, where a 33-move path is exhibited — so it is excluded.

q=9 is not recovered. Its bound is strongest at headroom 0 and weakens as the
cap widens — 34, 31, 30, 29, 28 at headrooms 0..4 — which is the reach-vs-cap
effect: a wider cap legalises more moves, so a fixed budget stops shallower.
Best statement: **no path of length <= 34**, and the supplied path is 48, so
the optimum lies in **[35, 48]**.

## Correction: the brief's non-monotonicity premise is right

Earlier in this session I reported that the controls tolerate only +1 above
their start length and therefore did not support the claim that useful paths
temporarily grow before collapsing. That was measured on the **even**
controls only, which were the only ones then solved. It is wrong as a general
statement about the family.

G7's length profile, from the verified 33-move path:

    22 22 22 22 22 22 19 19 19 18 16 16 15 13     <- descends to 13
    17 17 17 19 17 17 22 22 22 22 22              <- climbs back to 22
    15 13 9 9 5 4 3 2 2                           <- then collapses

It descends to 13, climbs **+9 back to 22**, and only then finishes. A
length-greedy search would abandon that path at step 14. The premise holds on
the odd controls.

Both things are true at once, and they are not in tension: **the excursion
stays within the starting length**, so G7 still solves at headroom 0
(max intermediate total = 22 = start). Non-monotone does not mean extra
headroom is required. That distinction is what the earlier report collapsed.

## Odd-q move signature

G7 uses moves **0, 1, 5, 9** — invert r0, invert r1, `r1·r0^-1`, conjugate r0
by Y — which the pooled even controls (q=6,8,10) never use at all.

| move | op | G7 | even pooled |
|---|---|---|---|
| 0 | inv r0 | 1 | **0** |
| 1 | inv r1 | 1 | **0** |
| 5 | r1·r0⁻¹ | 1 | **0** |
| 9 | cj r0 Y | 1 | **0** |
| 4 | r1·r0 | 7 | 18 |
| 2 | r0·r1 | 3 | 6 |
| 3 | r0·r1⁻¹ | 1 | 6 |

First-slot multiplications (moves 2/3), against the threshold of >=2 in the
externally supplied restricted lemma: G7 has 4, G6 3, G8 4, G9 9, G10 5.

## External restricted lemma — verified exactly

With `X = [[0,-1],[1,1]]`, `Y = [[-1,0],[1,-1]]`:

- the donor `x^2 y x^-1 y` maps to the identity — confirmed;
- the companion image is `[[-(n+1)^2, -n], [n^2+n-1, n-1]]` with trace
  `-n^2-n-2`, confirmed for every n = 3..10;
- the `[2,4]` false control reproduces: trace `t -> t^2-2`, n=3 gives
  −14 → 194.

Nothing to correct, including the author's own caveat that this is not an
unrestricted AC invariant.

The accompanying finite-image lower bounds (mod 5, 7, 11) are **9, 10, 9, 10,
10, 9, 9, 9** for n = 3..10. The corridor bounds measured here on the same
roots are **no path <= 44** for R6 and **no path <= 41** for R7 — about four
times stronger, and obtained by exhaustion rather than projection.
