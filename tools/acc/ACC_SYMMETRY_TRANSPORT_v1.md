# Generator symmetries transport solutions, and explain the equal-size components

## The symmetry

Every automorphism `phi` of the free group `F(x,y)` commutes with the AC
move set `ac-r2-v1`. Inversion `r -> r^-1` and multiplication
`r_i -> r_i r_j^{+-1}` are equivariant outright; conjugation
`r -> g r g^-1` maps to `phi(r) -> phi(g) phi(r) phi(g)^-1`. So `phi`
permutes the 14 moves by permuting the **conjugators only**, fixing moves
0-5. For `phi: y -> y^-1` the permutation is exactly `8<->9`, `12<->13`.

`phi` is therefore a graph automorphism of the capped AC graph, and
**components come in phi-isomorphic pairs of exactly equal size**.

## It explains the equal-size components

The transport sweep produced nine closed components whose vertex counts
fell into exact pairs:

| size | components | all MS-open |
|---|---|---|
| 13,440,784 | ac-01571, ac-02563 | yes |
| 13,728,824 | ac-02216, ac-04619 | yes |
| 13,909,464 | ac-01657, ac-06349 | yes |
| 13,978,168 | ac-04967, ac-06576 | yes |
| 10,951,472 | ac-03467, ac-08126 | yes |

Each pair is a `phi`-image of the other. They are genuinely **distinct**
components — the grouping runs exhausted one and did not hit the other,
and a direct check of ac-03467 against ac-08126 at cap 22 returned
`EXHAUSTED` with no hit. Equal size never implied equal component; here
the symmetry says why the sizes agree anyway.

## Pool-wide pairing

Over all 10,115 AC challenges, matching each presentation's symmetry image
against the pool under the pool's own uniqueness relation:

| symmetry | pairs | solved/unsolved splits |
|---|---|---|
| y->Y | 1,193 | 4 |
| swapinvx | 160 | 0 |
| swapinvy | 160 | 0 |
| x->X | 126 | 0 |
| swap | 112 | 0 |
| xy->XY | 96 | 0 |
| swapinv | 56 | 0 |

1,903 pairs, **4 splits**. Paired challenges share board status almost
perfectly — as they must, if a solution for one yields a solution for the
other.

## Transport is sound but not length-preserving

`phi` maps challenge A's presentation to something *canonically* equal to
B's — equal up to relator order, cyclic rotation and inversion, which is
the pool's uniqueness relation but **not free in the AC graph**. The
transported path is

    bridge(B -> phi(A))  +  relabel_phi(path_A)  +  target_fixup

`ac_symmetry_transport_v1.py` builds it and replays every step through the
official verifier core. Measured against the certificates on file:

| transport | length | direct search |
|---|---|---|
| ac-09594(15) --x->X--> ac-08327 | 18 | 17 |
| ac-09594(15) --y->Y--> ac-08327 | 21 | 17 |
| ac-08327(17) --x->X--> ac-09594 | 20 | 15 |
| ac-08327(17) --y->Y--> ac-09594 | 23 | 15 |
| ac-00286(53) --y->Y--> ac-03919 | **61** | none — search was budget-limited |
| ac-08651(58) --y->Y--> ac-05406 | **67** | none — search was budget-limited |

The bridge and fixup cost moves, so transport **loses to a direct search
wherever one succeeds**. Scoring is on the shortest verified solution, so
transport never improves a row that has already been searched.

Its value is the last two rows: ac-03919 and ac-05406 were `BUDGET` at
cap 22 — direct search found nothing — and transport produced verified
paths anyway. Both confirmed through the official verifier against
`manifest.json`, `accepted: true`, `ok: true`, lengths 61 and 67,
certificate hashes in `ac_symmetry_certificates_v1.jsonl`.

**Transport buys coverage where search fails, not length where it
succeeds.**

## What it is worth on the MS-open set

Unioning symmetry pairing with the measured transport components gives
**266 orbits covering 720 challenges, 550 of them MS-open** — a mean of
**2.71 challenges won per MS-open solve**, up from 2.47 for components
alone.

| orbit size | count |
|---|---|
| 2 | 180 |
| 3 | 27 |
| 4 | 29 |
| 5 | 22 |
| 6 | 6 |
| 8 | 1 |
| 9 | 1 |

The two largest are exactly the merged equal-size pairs:

    9x  ac-02217 ac-03772 ac-04967 ac-05117 ac-06576 ac-06785 ac-07128 ac-07698 ac-09294
    8x  ac-00568 ac-01657 ac-02883 ac-06349 ac-06572 ac-06801 ac-07653 ac-10066

Both are closed at cap 23 (see below), so the largest multipliers need
depth before they pay.

## The 37 n-for-one targets, priced against the real target

The earlier grouping runs carried other challenges as targets, so their
`EXHAUSTED` verdicts measured component size only. Re-run with `[[1],[2]]`
as the target, exhaustion becomes a disconnection theorem:

| verdict | components | challenges |
|---|---|---|
| **closed** — no solution exists at cap | 9 | **24** |
| **budget** — still live | 6 | **13** |

Closed: ac-00413 (cap 22), ac-01657, ac-04967, ac-06349, ac-06576,
ac-01571, ac-02216, ac-02563, ac-04619 (cap 23).
Live: ac-02422, ac-00399, ac-01083, ac-01558, ac-01956, ac-02828.

All closed component sizes are divisible by 4, as the by-4 theorem
requires.

The live six are the only ones of the 37 still worth searching at that
cap. The closed 24 need a higher cap: any solution to them must push
intermediate total relator length past the cap that closed them.

Coordinate-transport and donor-restoration ideas follow Robert Sneiderman
(ACC-P000002, `github.com/Robby955/ac-square-divisibility` @ `d0ed2c06`).
