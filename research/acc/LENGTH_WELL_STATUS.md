# ACC Length-Well Eye — 2026-09-12 checkpoint

This checkpoint records one surviving Compound-Eye observable for the SAIR Andrews--Curtis challenge and the nearby negative results that motivated it.

## Scope

The rank-2 move kernel in `length_well_eye.py` matches the official SAIR `ac-r2-v1` specification:

- moves 0--1: relator inversion;
- moves 2--5: right multiplication by the other relator or its inverse;
- moves 6--13: one-letter conjugation by `x^{±1}` or `y^{±1}`;
- free reduction after every move;
- exact target remains the ordered pair `(x,y)`.

The eye is finite and computational. It does **not** prove the Andrews--Curtis conjecture, nontriviality of an instance, or minimal solution length.

## Definition: length well and escape ceiling

For a presentation state `P=(r0,r1)`, let

`L(P) = |r0| + |r1|`.

For an integer ceiling `B >= L(P)`, define the **cap-B well** of `P` to be the exact connected component of `P` under legal AC moves after discarding every state `Q` with `L(Q)>B`.

If the cap-B component closes and contains no state shorter than `P`, then every path from `P` to any shorter state must visit length at least `B+1`.

The **escape ceiling** is the smallest ceiling that permits a path to a shorter state. The **well depth** is escape ceiling minus starting length.

This is a bottleneck observable. It is not intended as a linear predictor of total solution length.

## Exact first well: `ac-00015`

Start length: `21`.

An exhaustive cap-26 traversal closes after exactly

`105,912`

states and never reaches length below `21`.

An explicit 20-move path

`[8,12,3,8,7,2,0,9,13,10,3,7,8,8,8,12,2,10,13,3]`

has length profile

`21,21,21,26,26,26,25,25,25,25,25,24,24,24,24,26,26,27,27,27,20`.

Therefore the minimum escape ceiling is **exactly 27** and the first length-well depth is **exactly +6**.

A separate cap-27 breadth-first search found a 20-move descent as well, so 20 is the shortest descent length subject to the optimal ceiling 27. This is a finite statement about the first descent, not the full trivialization.

The user's independent solved reference for this instance uses 622 moves. That number is used only as a hard calibration reference here, not as a claim of minimality.

## Layered well discovered after the first descent

The first escape lands at the length-20 state

`((2,2,2,-1,-1,-2,-1,-1,2), (-2,1,2,1,-2,-2,1,-2,1,-2,1))`.

Running the same exact cap-component test on this state reveals a substantially deeper second well:

| ceiling | exact component size | minimum length | result |
| ---: | ---: | ---: | --- |
| 25 | 81,472 | 20 | closed, no descent |
| 26 | 190,920 | 20 | closed, no descent |
| 27 | 919,656 | 20 | closed, no descent |
| 28 | 1,737,200 | 20 | closed, no descent |
| 29 | 5,149,128 | 20 | closed, no descent |

Therefore any second descent from this state must visit total length at least **30**. Its currently certified second-well depth is **at least +10**.

A cap-30 run exceeded the execution limit before completion. No conclusion about cap 30 is recorded.

This layered-well behavior is the strongest current explanation for why the 622-move control is qualitatively harder than the accepted controls: escaping one uphill barrier does not enter a monotone downhill basin; it enters another, deeper barrier.

The large closures above were reproduced with `length_well_fast.cpp`, a C++17 implementation of the same exact move kernel. The default GitHub regression currently certifies the smaller first-well result in Python; the multi-million-state second-well closures are reproducible but are not run on every commit.

## Exact lower bound: `ac-00002`

Start length: `25`.

Independent exhaustive reruns with the same exact move kernel give:

- cap 31: closed component of `1,021,696` states, minimum length 25;
- cap 32: closed component of `1,303,928` states, minimum length 25.

Therefore every path from the initial state to any shorter state must visit total length at least **33**. The currently certified well depth is therefore **at least +8**.

No claim is made here about what happens under cap 33; the attempted cap-33 run was stopped by the execution limit before completion and is not evidence either way.

## Accepted-path calibration

Ten verifier-accepted paths from the 2026-09-11 user backup were checked. Their stored path lengths are upper bounds, not certified minima.

| challenge | accepted path length | start length | measured well depth |
| --- | ---: | ---: | ---: |
| ac-00076 | 123 | 24 | 0 |
| ac-00145 | 116 | 15 | 1 |
| ac-00219 | 140 | 24 | 0 |
| ac-00576 | 121 | 15 | 1 |
| ac-00742 | 15 | 17 | 0 |
| ac-00862 | 132 | 16 | 0 |
| ac-00977 | 30 | 20 | 0 |
| ac-01198 | 103 | 15 | 1 |
| ac-01217 | 61 | 16 | 0 |
| ac-01411 | 12 | 17 | 0 |

A second sample consisting of ten of the longest stored accepted paths (132--168 moves) also had depth 0 or 1 in the working analysis. Those instances are not duplicated in the executable calibration table yet.

The correct interpretation is qualitative: the hard controls exhibit genuine uphill barriers that are absent from the accepted controls tested so far. Well depth is **not** currently justified as a numerical estimator of solution length.

## Negative controls / rejected primary eyes

The following were explicitly rejected as primary distance observables after calibration:

1. **Finite quotient word distance.** Small quotients saturate too quickly. They may remain useful as filters, but not as a long-range hardness meter.
2. **Integral exponent-sum matrix distance.** The abelianized matrix shadow gives only distance 7 on `ac-00015` versus the 622-move reference, and distance 5 on `ac-00002`. Dynamic range is inadequate.
3. **One- and two-ply branching counts.** On the twelve initial controls tested, every state had 14 unique one-step neighbors and 146 unique two-step states; the counts did not separate hard from accepted cases.
4. **Latent cyclic cancellation by itself.** It contains useful policy information but is not monotone with hardness and is retained only as a potential move-ordering eye.
5. **Naive conjugacy/cyclic canonicalization as a transition quotient.** Replacing a whole conjugacy class by one canonical representative is not transition-complete: multiplication from different representatives can lead to different next classes. That shortcut was rejected before using it for any barrier claim.

## Search implication

The public length-first baseline is structurally blind to states that must get longer before cancellation becomes available. The length-well eye measures exactly that obstruction instead of penalizing it.

A practical Compound-Eye search should therefore treat total length and well structure differently:

- total length remains a cheap local observable;
- well depth / cap-component growth is a bottleneck diagnostic;
- layered wells should be expected rather than assuming one escape creates a downhill path;
- latent cancellation and overlap are candidate policy eyes inside or near a well;
- failed shallow shadows should not be promoted to distance functions.

## Regression status

GitHub workflow `.github/workflows/acc-length-well.yml` recomputes the full `ac-00015` cap-26 closure, replays the ceiling-27 witness, and runs the accepted calibration controls. The first branch run completed successfully.

## Next proof/search target

The next useful object is a **boundary-of-well policy**: identify moves from states near the cap boundary that increase access to lower-length components, rather than ranking only by immediate length. Candidate measurements include cap-component frontier size, structural multiplication exits versus pure conjugation exits, return-channel count, and cancellation gain after crossing the boundary.

Any new eye should be tested first against `ac-00015`, `ac-00002`, and the accepted calibration set before being added to the solver.
