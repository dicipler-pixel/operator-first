# The growth-collapse conjecture

*Side quest. Status: one real finding, one killed by its own control.*

## Setup

`ac_corridor64_bidir_v2.c` already writes a per-level frontier trace to
stderr (`F depth d states n`). That trace is a **growth curve** for the
forward ball, and nobody had looked at it as one. `growth.py` fits an
exponential base to it.

Populations: 8 T1 rows (unsolved, `kTeams`=0) and 14 solved rows whose
record move-count is published, all at cap `|r|+6`, 20M states/side.

## What I first saw — and why it was wrong

Fitting over the **last half** of each curve gave an apparently clean split:

| population | growth base |
|---|---|
| solved, MEET found | 1.52 – 2.28 |
| solved, not found at this cap | 1.34, 1.44 |
| T1 unsolved, BUDGET | 1.10 – 1.25 |
| T1 unsolved, component CLOSED | ≈ 1.00 |

Zero overlap between MEET (min 1.516) and T1-unsolved (max 1.249). It looked
like a polynomial-time solvability oracle.

**It was an artifact.** MEET rows *stop* at depth 10–15; BUDGET rows run to
depth 26–129. The two populations were being fitted over completely different
depth regimes — early growth against late growth. Refitting both over the
identical window (depth 4–10):

| population | base, depth 4–10 |
|---|---|
| solved | 2.02 – 2.60 |
| T1 unsolved | 1.72 – 2.42 |

The populations **overlap**, and the T1 row `ac-03824` (2.415) grows faster
early than eight of the eleven solved rows. Early growth rate does not
predict solvability. The clean table above measured when each search stopped,
not how hard the row is.

## What survives, and it is the more interesting statement

Both populations start free-like — base ≈ 2, near the branching of the
underlying free group. They differ in **what happens next**:

| row | base @ depth 4–10 | base @ late depth | collapse |
|---|---|---|---|
| ac-06225 (solved) | 2.250 | 2.172 | none — meets at depth 11 |
| ac-00977 (solved) | 2.456 | 2.281 | none — meets at depth 10 |
| ac-03824 (T1) | 2.415 | 1.101 | **2.4 → 1.1** by depth 30 |
| ac-02976 (T1) | 2.148 | 1.239 | **2.1 → 1.2** by depth 26 |
| ac-00692 (T1) | 1.917 | 1.187 | 1.9 → 1.2 by depth 40 |
| ac-05468 (T1) | 1.727 | 1.009 | closes entirely at depth 129 |

> **Conjecture (growth collapse).** In the length-capped AC graph, the forward
> ball from any presentation begins with free-like growth (base ≈ 2) and, if
> the cap binds, undergoes a transition to near-linear growth at some collapse
> depth `d*(P, cap)`. The instance is solvable within that cap iff the target
> is reached before `d*` — solvability is a race between the required path
> length and the collapse depth, not a property of the growth rate itself.

This matches the corridor picture in `ACC_PATH_LENGTH_BOUNDS_v1.md` from the
other direction: ac-02422's forward frontier is flat at ~475,000 states/level
from depth 52 to 65. That is a fully collapsed ball — post-`d*`, the component
is a tube, not a ball.

## Why this might matter outside ACC

The folk intuition is that hard instances are hard because the search space
explodes. Here the explosion is what makes an instance **easy**: every row
solved at this cap kept base ≈ 2 until it hit the target. The hard rows are
the ones whose search space *stops* exploding — they are thin, not big.

That is the same shape as the clustering/freezing transition in random SAT
(hardness at the thin, frozen end, not the many-solutions end) and as
conductance bottlenecks in MCMC (slow mixing from thin cuts, not large state
spaces). And growth type is a quasi-isometry invariant — Gromov's theorem is
the statement that it is rigid enough to classify groups. If the collapse is
real and permanent rather than an artifact of the cap, then a growth-type
mismatch between a presentation's component and the identity's component is
an **obstruction to connectivity that costs polynomial time to measure**,
where the current disconnection proofs cost exponential enumeration.

## What would settle it

1. **Is the collapse cap-induced or intrinsic?** Re-measure `d*` for one row
   across caps `|r|+2 … |r|+16`. If `d*` grows without bound as the cap rises,
   the collapse is an artifact of the cap and there is no invariant here. If
   `d*` converges, there is.
2. **Depth-matched controls throughout.** The first result died to this; every
   subsequent comparison has to fix the depth window before fitting.
3. **n is 22 rows.** Far too small to claim a threshold.

## Honest status

Finding 1 (growth base separates solvable from hard): **dead**, killed by its
own depth-matched control.
Finding 2 (growth collapses, and solvability is a race against the collapse):
**alive, untested against question 1 above.**
