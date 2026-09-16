# A budget-limited bidirectional run is a theorem, not a non-answer

## The claim

Both sides of `ac_corridor64_bidir_v1.c` advance by **complete BFS levels**.
When a run stops without meeting, the forward ball of radius `df` and the
backward ball of radius `db` are each complete, and the meet test was applied
to every state interned on either side. So the two balls are provably
disjoint, and:

> If a path of length `L <= df + db` existed, the vertex on it at forward
> distance `df` would sit at backward distance `L - df <= db`, hence in both
> balls. There is none. **No solution of length `<= df + db` exists at that
> cap.**

This upgrades every `BUDGET` verdict in the transport sweep. They were
reported as "undecided"; each was carrying a bound.

## The six live n-for-one representatives

20M states per side. All six had resisted one-sided search at 120M and
bidirectional search at 50M/side.

| challenge | cap | fwd radius | bwd radius | proved: no path of length <= |
|---|---|---|---|---|
| ac-02828 | 23 | 93 | 7 | **100** |
| ac-01956 | 23 | 67 | 7 | **74** |
| ac-02422 | 23 | 65 | 7 | **72** |
| ac-00399 | 21 | 28 | 8 | **36** |
| ac-01083 | 23 | 21 | 8 | **29** |
| ac-01558 | 23 | 18 | 8 | **26** |

## The corridor is a corridor

Forward frontier growth for ac-02422 at cap 23 is essentially **linear** --
about 475,000 states per level, flat from depth 52 to depth 65:

    depth 52  13,401,960        depth 60  16,971,659
    depth 56  15,223,589        depth 65  19,646,264

Backward from the target it is exponential: 2.45M states in 7 levels.
The component is a long thin tube, not a ball, and that asymmetry is why
the forward side reaches depth 65 while the backward side reaches 7.

The forward radius at fixed budget varies enormously across challenges --
18, 21, 28, 65, 67, 93 -- so corridor width is a per-challenge property and
a direct measure of how bad the branching is.

Note this breaks the usual bidirectional argument. `2*b^(d/2)` assumes both
sides branch alike; here they do not, so the engine behaves as a deep
one-sided search meeting a small ball around the target. The engine is still
correct -- it reproduces four known certificate lengths exactly -- but the
speedup is not the textbook one.

## The backward ball does not depend on the challenge

`states_b` is identical across every run at a given cap:

    cap 23, radius 7:   2,452,439 states
    cap 23, radius 8:  15,614,326 states
    cap 21, radius 8:  12,804,277 states

Naturally so: the ball around `[[1],[2]]` has nothing to do with which
challenge is being searched. Recomputing it per challenge spends most of
the budget re-deriving the same set. It should be built **once per cap**,
stored, and reused -- a finishing atlas -- letting the whole budget go to
the forward corridor and pushing every bound up.

## Widening the cap makes it worse

ac-02422 at 40M/side, caps 27, 31, 40 and ac-00638 at caps 40, 48: all
budget-limited, and the wall-clock *fell* as the cap rose (102s, 79s, 66s).
A larger cap legalises more moves, so branching rises and a fixed budget is
consumed at a shallower depth. For a fixed budget, **a narrower cap reaches
deeper and yields a stronger bound**, which is what makes the sweep's
`headroom 8` the right choice rather than an arbitrary one.

The disconnection theorems are unaffected -- exhaustion at cap 22/23 is
exhaustion -- but a path for these challenges, if one exists, needs both
more headroom and far more depth than a breadth-first method reaches.
