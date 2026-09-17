# The scope ledger — what each transformation actually preserves

Every row states what a transformation preserves, what it does **not**, and the
test that settles it. A "preserves" claim needs a proof; a "does not preserve"
claim needs a counterexample. Nothing here is asserted from plausibility.

The discipline is borrowed from the hidden-zeros review: *preserving a zero is
not preserving the amplitude.* There, an additive kinematic shift provably
preserves every non-adjacent `c_ij` and still changes the amplitude —
`A₄(2,3) = 5/6` becomes `5/4` under `δ=1`. Same zeros, same spectrum, same rank
and same full response are four different statements.

The ACC version is five statements, and this session collapsed them repeatedly:

> same Nielsen class · same component size · same AC component ·
> same optimal move count · same path

## The ledger

| Transformation / eye | Preserves | Does **not** preserve | Evidence |
|---|---|---|---|
| Automorphism `φ` applied to both relators | AC-triviality | the AC component at a fixed cap; the move count | transport identity 400/400 on random input; conjugation by `g` inflates to `\|φ(g)\|` moves |
| Same Nielsen class | AC-triviality | component identity, CLOSED count, solution | `ac-00945`/`ac-05233` both 386,320 — intersection **0** |
| Equal component size | nothing about identity | component identity | `ac-00026`/`ac-00036` both 12,012 — intersection **0** |
| Cyclic rotation | the AC component (it *is* conjugation) | move count — costs `\|c\|` moves | compiled in `class_bridge.py` |
| Relator inversion | the AC component | move count — costs 1 move | moves 0 / 1 |
| Relator **swap** | the AC component | move count — costs `4+\|a\|` moves | `2,5,2,1` then conjugate `r0` by `a⁻¹`; verified 346/346 |
| `T_16` membership | AC-triviality | **optimality of the path** | 57 rows sit in `T_16`; every path came back **+18 to +37** against the record |
| Calibrated cap band `\|r\|+0..+6` | search *efficiency* at fixed budget | containment of the *shortest* path | `ac-06639`: `MEET_EXACT` 35 at caps +3, +5, +7 — record is **34** |
| Any AC-invariant of the presentation | constant on the whole pool | any discrimination at all | every pool row presents the trivial group (`eyes/README.md`) |
| Path compression | the endpoint (re-replayed, else rejected) | optimality | 9.3× on random walks, **0×** on the 19 certificates |
| `BESTMEET` depth bound | shortest path **within the cap**, when both sides are complete | anything, when the budget truncated first | why the output now says `MEET_EXACT` vs `MEET_BUDGET` |

## The two that cost the most time

**Equal size is not equal component.** Burned three times — `ac-00945`/`ac-05233`,
`ac-00026`/`ac-00036`, and the 92,600 family, which conjugacy BFS denied outright.
A scalar summary of a set says nothing about which set it is.

**The cap band is about search speed, not about where solutions live.** The
`|r|+0..+6` calibration is real: past `+6` a fixed budget collapses to `budget`.
But that is a statement about *finding a path quickly*, and it was silently read
as *the shortest path lives here*. Two rows now prove it false, and prove it the
right way — `MEET_EXACT`, not "we didn't find one":

- `ac-00104`: provably 22 within `|r|+6`; record **21** → its optimal path uses a
  state of length > `|r|+6`.
- `ac-06639`: provably 35 within `|r|+7`; record **34** → same conclusion.

An exact negative is what makes this usable. "We searched and found nothing" would
have proved nothing at all.

## Standing rule

Before any transformation is used to move a result from one row to another, name
the invariant it preserves and the quantity it does not, and cite the test. A
transformation that preserves solvability is not thereby a transformation that
preserves the *length* of the solution — and on this board, length is the score.

---

## Addendum — "a long record means a sloppy path" is false

Tested because it looked like free points: 343 sole-held rows carry records of 60+,
up to **595 moves**, and our corridor routinely produces paths of 33–55. Beating a
595 should have been a rout.

Every one of the first nine came back **NOPATH**:

```
ac-00215 record 595 -> NOPATH      ac-03873 record 510 -> NOPATH
ac-05232 record 592 -> NOPATH      ac-06796 record 418 -> NOPATH
ac-01613 record 487 -> NOPATH      ac-00676 record 403 -> NOPATH
```

The inference was backwards. **A long record does not mean a sloppy path; it means
a hard row.** The record is 595 because nothing shorter has been found by anyone,
including us — those rows are exactly the ones where our corridor finds nothing at
all within the calibrated band.

It is consistent with the gap data already in hand, which I had misread as noise:

| record range | our median gap |
|---|---|
| 25–40 | +8 |
| 40–60 | +13 |
| 60+ | no path found |

So the corridor's reach is roughly fixed and tracks **row difficulty**, not record
length. Rows with short records are ones where short paths exist and we land ~10
moves long; rows with long records are ones where no short path exists and we land
nowhere.

**Consequence for target selection.** There is no easy end of this board. Value
comes only from closing a ~10-move gap on rows we already solve, or from solving
rows we currently cannot. Sorting by record — in either direction — is not a
difficulty proxy, and this is the second time today that a plausible ordering
heuristic cost compute: first hardest-record-first, now largest-record-first.
