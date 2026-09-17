# Non-normality as an eye — the lemma diagnosed the failure and fixed it

## The identity

For `A* = -A`, `D = diag(d_1..d_N)` real, and the graph of `A` connected, with `H = D + A`:

    [H,H*]_ij = -2 (d_i - d_j) A_ij         H normal  <=>  d_1 = ... = d_N

`H* = D - A`, so `[H,H*] = 2(AD - DA) = -2[D,A]`, and `[D,A]_ij = (d_i - d_j)A_ij`.
Vanishing forces `d_i = d_j` across every edge; connectivity propagates it to the component.
Verified numerically to machine precision on random skew `A` over a connected graph, and the
constant-`D` case returns exactly zero.

## Why it matters here: it diagnoses the eye that just failed

The commutator is supported **on edges**, valued by the gradient of a real potential across
each edge. The entire collision ladder that collapsed at the wall was **per-state**.

And concretely: with `d` = total length, the 14-vector `(d_j - d_i)` over the moves out of a
state **is exactly `delta_total_by_move`**. So the labelled 14-channel eye was already a
non-normality measurement — with a weak potential. It gave 734 classes on 23.6M states
because length barely varies, not because edge-gradient eyes are weak.

The lemma also says when an eye is worth running at all: the commutator vanishes iff `D` is
constant on the component. An eye carries information exactly to the extent its potential
varies. That converts "which eye next?" from taste into a measurable question.

## Swapping the potential

`d` = exact distance to the trivial pair in the finite image of
`rho: x -> [[0,-1],[1,1]], y -> XZ` reduced mod 5 — a true lower bound on remaining moves,
not a proxy. Same 23,609,984-state component, same run:

| ladder level | classes | largest cell | mean cell |
|---|---:|---:|---:|
| scalar total length | 7 | 17,862,272 | 3,372,855 |
| R/D/S/U histogram | 14 | 11,788,096 | 1,686,427 |
| labelled 14-channel | 734 | 420,128 | 32,166 |
| exponent ledger | 1,032 | 218,746 | 22,878 |
| **non-normality gradient, `d` = img_dist mod 5** | **12,315** | **57,798** | **1,917** |

**16.8x more classes than the labelled channel, and a 7.3x smaller largest cell.**
Mean cell 32,166 -> 1,917.

## The small-component result pointed the wrong way

On the 180-state cap-14 component the new eye gives **17** classes against the labelled
channel's **25** — it *loses*. At the wall it wins by 16.8x.

This is the same lesson as the 16/16 boundary calibration, running in the opposite
direction: a measurement at small n carried no information about the wall, and had I trusted
it I would have discarded the best eye available. Only the wall measurement counts, whichever
way it happens to point.

## What is still not solved

100% of states remain in collision cells — 12,315 classes over 23.6M states means a mean
class of ~1,900. So an escalation trigger of "cell has more than one member" still selects
everything. The cell sizes fell 7.3x, which is real movement on the same axis, but the
trigger rule needs a size threshold rather than a nonempty test.

## Immediate follow-up

The lemma says: find a `D` that varies more. Mod 5 has eccentricity 8. Mod 7 reaches 9 and
mod 11 reaches 11 over 1,742,396 image states, so both should be strictly finer potentials
for a one-line change. That is the next measurement, and it is now a directed search rather
than a guess.
