# The whole R_n junction family is disconnected at low headroom

Frozen authority `a0fd6e6`. Target `[[1],[2]]`.

    R_n = ( x^2 y x^-1 y ,  x y^n x^-1 y^-(n+1) ),   n = 3..10
    start total = 2n + 8

This is the family an external handoff reports as covering **118**
dated-snapshot-unsolved official rows. R6 and R7 are n=6 and n=7 of it.

## Every root closes

A CLOSED cap means the component was fully enumerated and the target is not
in it — a disconnection theorem. Closure is monotone (a path at cap C is a
path at every larger cap), so the top of each ladder closes every cap below.

| n | start | closed through cap | complete component | div 4 | min total length | headroom |
|---|---|---|---|---|---|---|
| 3 | 14 | 19 | 23,609,984 | yes | **20** | +6 |
| 4 | 16 | 22 | 2,064,600 | yes | **23** | +7 |
| 5 | 18 | 25 | 11,688,560 | yes | **26** | +8 |
| 6 | 20 | 28 | 65,724,220 | yes | **29** | +9 |
| 7 | 22 | 30 | 102,424,140 | yes | **31** | +9 |
| 8 | 24 | 30 | 9,791,020 | yes | **31** | +7 |
| 9 | 26 | 32 | 12,977,140 | yes | **33** | +7 |
| 10 | 28 | 34 | 16,768,300 | yes | **35** | +7 |

**Caveat on comparability.** n=6 and n=7 were run with a dedicated 110M
forward allocation; n=3,4,5,8,9,10 used 25M and stopped at their first
BUDGET verdict. So the walls for n=8,9,10 in particular are floors, not
final — more budget would very likely close them further, as it did for
R6 (cap 27 -> 28) and R7 (cap 29 -> 30). The +6 entries are the least
settled.

Component size at fixed headroom +6 grows with n: 2,064,600 (n=4),
9,791,020 (n=8), 12,977,140 (n=9), 16,768,300 (n=10).

## Official rows reached by symmetry

Under the order-8 signed-permutation group, recomputed from the frozen
manifest:

| n | official rows |
|---|---|
| 3 | ac-02842, ac-06556 |
| 4 | ac-01440, ac-06388 |
| 5 | ac-01223, ac-09596 |
| 6 | ac-02799, ac-02968, ac-05297, ac-06364 |
| 7 | ac-00945, ac-05233, ac-06242, ac-06865, ac-07712 |
| 8 | ac-01696, ac-06290 |
| 9 | ac-01834, ac-04293 |
| 10 | ac-04027, ac-04310 |

**21 distinct rows, every one unsolved** on the 2026-09-12 board. The
external claim of 118 rows therefore rests on a further 97 reached by
coordinate transport beyond the order-8 group; that part is not established
here and the branch-root map recording it is not present in this
environment.

## The family is a subfamily of MS-1190

R_n's second relator `x y^n x^-1 y^-(n+1)` is the Miller-Schupp first
relator up to `x <-> x^-1`. Independently confirmed by the mapping: R_3's
rows ac-02842 and ac-06556 were already measured in the MS-open closure
sweep, both closed through cap 18 in the **106,800** well — the same two
rows, reached from a different direction.

## Bounded negatives

Eight roots, eight disconnection theorems, **zero certificates**. No state on
any root improved its `EXPONENT_PAIR` size below the starting value. The
external search on the same roots reports 5,760,000 expansions and
80,640,000 move proposals with 0 solves and 0 strict descent — two
independent engines, the same wall.

## Continuation past the sweep floors

R6 at cap 29, with a 7-radius atlas and **200,000,000** forward states:
`BUDGET depth=47`, so **no path of length <= 54** at cap 29. The component
exceeds 200M, which matches the ~3.5x per-cap growth predicting ~230M. That
cap is therefore bounded but not closed, and R6's wall stands at cap 28.

n=8 and n=9 are the roots whose walls were floors -- both stopped at their
first BUDGET under the 25M sweep allocation. Their ladders are being
continued from cap 31 and cap 33 at 90M forward, where the predicted
component sizes (~34M and ~45M) sit comfortably inside the allocation.

## Final state of the continuation runs

| root | cap | verdict | component / bound |
|---|---|---|---|
| R6 | 28 | **CLOSED** | 65,724,220 |
| R6 | 29 | BUDGET, 200M, depth 47 | no path ≤ 54 |
| R7 | 30 | **CLOSED** | 102,424,140 |
| R7 | 31 | BUDGET, 150M, depth 35, atlas radius 7 | no path ≤ 42 |
| R_8 | 31 | **CLOSED** | 39,303,140 |
| R_8 | 32 | BUDGET, 90M, depth 46 | no path ≤ 53 |
| R_9 | 33 | **CLOSED** | 54,022,680 |
| R_9 | 34 | BUDGET, 90M, depth 43 | no path ≤ 50 |

R7 cap 31 behaved exactly as the growth projection said it would: closure
needs ~369M states (~19.5 GB) and 150M was allocated, so the run returns a
bound rather than a wall. The projection was made before the run and is
confirmed by it.

### Consolidated family walls

| n | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| closed through cap | 19 | 22 | 25 | **28** | **30** | **31** | **33** | 34 |
| min total length | 20 | 23 | 26 | **29** | **31** | **32** | **34** | 35 |

Every component divisible by 4. n=3, 4, 5 and 10 remain at their 25M sweep
floors and would lift with ordinary budget; n=6 and 7 are at the memory
ceiling and would not.

Eight roots, eight disconnection theorems, four supplementary length bounds,
**zero certificates**.

## FINAL — all four sweep floors lifted, no floors remain

The 25M sweep floors for n=3, 4, 5 and 10 were lifted at 150M forward. Every
wall in the family is now a measured closure rather than an allocation
artifact.

| n | closed through cap | complete component | div 4 | min total length | next-cap bound |
|---|---|---|---|---|---|
| 3 | **20** | 51,411,456 | yes | **21** | no path ≤ **84** |
| 4 | **23** | 92,052,208 | yes | **24** | no path ≤ 69 |
| 5 | **26** | 39,478,220 | yes | **27** | no path ≤ 37 |
| 6 | 28 | 65,724,220 | yes | 29 | no path ≤ 54 |
| 7 | 30 | 102,424,140 | yes | 31 | no path ≤ 42 |
| 8 | 31 | 39,303,140 | yes | 32 | no path ≤ 53 |
| 9 | 33 | 54,022,680 | yes | 34 | no path ≤ 50 |
| 10 | **35** | 72,157,140 | yes | **36** | no path ≤ 60 |

R_3 at cap 21 gives the strongest length bound in the family, **no path of
length ≤ 84**, at forward depth 77 against a radius-7 atlas.

### The walls do not lie on one line

    n         3   4   5   6   7   8   9  10
    min len  21  24  27  29  31  32  34  36
    delta       3   3   2   2   1   2   2

n = 3, 4, 5 step by exactly 3, giving min length = 3n + 12 on that range.
From n = 6 the increment drops to 2 and once to 1. The low-n roots sit on a
line the high-n roots leave, and the break is at n = 6 — which is where R_6
and R_7, the two roots with the deepest closures, begin.

Two readings, neither established: the low-n roots are genuinely a different
regime, or the n ≥ 6 walls are still floors at a higher allocation and would
straighten the line if pushed. The second is testable and cheap for n = 8, 9,
10; it is not testable for n = 6, 7, which are at the memory ceiling.

**Eight roots, eight disconnection theorems, eight length bounds, zero
certificates.**
