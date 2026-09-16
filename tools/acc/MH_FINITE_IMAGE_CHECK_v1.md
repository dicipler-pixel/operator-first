# The finite-image lane cannot disconnect — verified independently

## Why it was worth checking

Any homomorphism `phi: F(x,y) -> G` is **AC-equivariant**: applying an
`ac-r2-v1` move to `(r0, r1)` and then mapping gives the same result as
mapping first and applying the corresponding move to `(phi(r0), phi(r1))`,
with conjugators `phi(x)`, `phi(y)`. Inversion, right multiplication and
conjugation by a generator are all group operations a homomorphism respects.

So the image pair evolves under the same 14 moves. If `(I, H_n)` and `(X, Y)`
lay in **different components** of the move-graph on `G x G`, then R_n would
be disconnected from the target **with no cap at all** — an unconditional
disconnection theorem, unlike every corridor result in this session, which
holds only below a stated cap.

## The check, at p = 5

`X = [[0,-1],[1,1]]`, `Y = [[-1,0],[1,-1]]` reduced mod 5; start
`(I, H_n)` with `H_n = [[-(n+1)^2, -n], [n^2+n-1, n-1]]`; target `(X, Y)`.

| n | H_n trace mod 5 | target reachable | distance | component |
|---|---|---|---|---|
| 3 | 1 | yes | 6 | 14,396 |
| 4 | 3 | yes | 4 | 14,396 |
| 5 | 3 | yes | 4 | 14,396 |
| 6 | 1 | yes | 6 | 14,396 |
| 7 | 2 | yes | 7 | 14,396 |
| 8 | 1 | yes | 6 | 14,396 |
| 9 | 3 | yes | 4 | 14,396 |
| 10 | 3 | yes | 4 | 14,396 |

`|SL2(F5)| = 120`, so there are 14,400 pairs in total and the component
holds **14,396 of them** — the move-graph on pairs is nearly complete.

## Independent confirmation of the external numbers

These were computed here from scratch. They reproduce the externally
supplied figures exactly: `reached_states 14396` and
`root_bounds [6,4,4,6,7,6,4,4]` for n = 3..10. Digit for digit, two
implementations.

## Consequence

The target is reachable in the image for **every** root, so no finite
quotient of this shape can separate R_n from the target. The lane yields
**lower bounds only** — an image path is a projection of a word path, so
image distance bounds word distance from below, and it cannot certify
disconnection.

Those bounds are also weak against the corridor results. The external
maximum over p = 5, 7, 11 is 9-10 per root. The corridor bounds measured
here are **no path <= 44** for R6 at cap 28 and **<= 54** at cap 29 — about
five times stronger.

This closes the direction. An unconditional separating invariant, if one
exists, has to be finer than a finite matrix quotient; the external
restricted trace lemma is the right shape but carries a kernel hypothesis
that AC moves do not preserve.
