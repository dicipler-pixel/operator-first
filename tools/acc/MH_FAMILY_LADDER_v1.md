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
