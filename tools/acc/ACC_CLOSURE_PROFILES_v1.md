# Closure profiles: every "live" challenge was disconnected at a narrower cap

## The reporting bug

`ac_corridor64_bidir_v1.c` printed `EXHAUSTED` only when **both** frontiers
emptied. That almost never happens: one side closes while the other runs on
to its allocation, and the run was then labelled `BUDGET`.

But a single empty frontier already decides it. If the forward frontier
empties with no meet, that component is **completely enumerated** and the
target is not in it — the two lie in different components of the capped
graph. The meet test is symmetric in time (every newly interned state is
checked against the other side's table, on whichever side is expanding), so
a closed side stays sound while the open side keeps growing.

`ac_corridor64_bidir_v2.c` reports `CLOSED_F` / `CLOSED_B` with the closed
component's size. v1 and the three one-sided engines are unchanged. v2
reproduces the four known certificate lengths exactly: ac-08491 8,
ac-01635 8, ac-07445 13, ac-09594 15.

The cost asymmetry is the practical point. ac-02422 closes at cap 19 in
**449,544 states**; at cap 23 it burns 20,000,000 and learns nothing. The
sweep ran exclusively at headroom 8 — the one setting that yields no
closure at all.

## Profiles

Largest cap at which each challenge is proved disconnected from `[[1],[2]]`,
20M states per side. All ten had previously been recorded as undecided.

| challenge | len | closed through cap | component at that cap |
|---|---|---|---|
| ac-01956 | 15 | **22** | 10,951,472 |
| ac-02828 | 15 | **22** | 10,951,472 |
| ac-02422 | 15 | **21** | 15,133,856 |
| ac-01083 | 15 | 19 | 97,704 |
| ac-01558 | 15 | 18 | 2,014,992 |
| ac-00399 | 13 | 18 | 2,014,992 |
| ac-00638 | 26 | 27 | 8,322,832 |
| ac-06600 | 27 | 28 | 7,997,304 |
| ac-08027 | 28 | 29 | 8,171,856 |
| ac-05058 | 30 | 31 | 11,194,988 |

Every component size is divisible by 4, as the by-4 theorem requires.

ac-02422's ladder shows the growth: 476, 3,880, 92,600, 449,544, 1,219,064,
15,133,856 at caps 16 through 21, then budget at 22.

## Recurring sizes are symmetry images, not shared components

Unrelated challenges keep landing on identical component sizes:

    ac-01956, ac-02828     265,392 / 696,024 / 4,458,672 / 10,951,472
    ac-01558, ac-00399     20,560 / 857,808 / 2,014,992

Every matched pair tested is a **different** component — five more
confirmations that equal size never implied equal component:

| pair | cap | verdict |
|---|---|---|
| ac-01956 vs ac-02828 | 22 | different (both 10,951,472) |
| ac-01956 vs ac-02828 | 19 | different (both 265,392) |
| ac-01558 vs ac-00399 | 18 | different (both 2,014,992) |
| ac-01558 vs ac-00399 | 16 | different (both 20,560) |
| ac-02422 vs ac-01956 | 16 | different (both 476) |
| **ac-03467 vs ac-01956** | 22 | **SAME — MEET at distance 33** |

The sizes agree because the order-8 symmetry group carries a component to
an isomorphic one. At cap 22 there are at least **three distinct components
of size exactly 10,951,472**: one containing both ac-03467 and ac-01956, its
`y -> y^-1` image containing ac-08126, and a third containing ac-02828
(whose own image contains ac-09961). All five challenges are MS-open.

`2,014,992` is the exact size of the cap-18 AK(3) well cross-validated
earlier from the War Room, reached here from two unrelated challenges.

## What this changes

The earlier "24 closed / 13 live" split was too coarse: **"live" mostly meant
"only looked at one cap."** Every one of the ten now carries disconnection
theorems, and the open question for each is a narrow band — for ac-01956 and
ac-02828 it is cap 23 and above, nothing below.

Combined with `ACC_PATH_LENGTH_BOUNDS_v1.md`, each challenge now has both a
cap below which it is provably disconnected and a length below which no path
exists at the next cap up. Neither is a solve; both bound where one could be.
