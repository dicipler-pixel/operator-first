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

## Addendum: the short MS-open core is nine wells

Closure profile run over all 40 MS-open challenges of length <= 15
(`ac_msopen_closure_v1.py`, 20M states per side, headroom 1..8). These are
k=0 rows -- nobody has solved one -- so a MEET would score the full point.

**Zero solves.** Every row closed, and the 40 partition exactly into **nine**
(cap, component) classes:

| component | closes through cap | rows |
|---|---|---|
| 13,978,168 | 23 | 6 |
| 13,909,464 | 23 | 6 |
| 15,133,856 | 21 | 6 |
| 10,951,472 | 22 | 6 |
| 13,440,784 | 23 | 4 |
| 13,728,824 | 23 | 4 |
| 2,014,992 | 18 | 4 |
| 97,704 | 19 | 2 |
| 106,800 | 18 | 2 |

6+6+6+6+4+4+4+2+2 = 40. Every size divisible by 4. `2,014,992` is the cap-18
AK(3) well cross-validated earlier from the War Room.

The unit of study is the well, not the row: a row's identity beyond its well
carries no information that any measurement here could see. The earlier
observation that unrelated challenges keep landing on identical component
sizes is this, seen one pair at a time.

Placement of the Mad Hatters roots against this core: every one of the 40
opens by cap 23 at the latest, while R6 is still CLOSED at cap 26 and R7 at
cap 28 (`MH_ACC_RUN_20260916_v1.md`). The junction roots are harder than any
short MS-open row measured here.

**Bounded negative:** 40 MS-open rows, no path at the stated closure caps,
20M states per side, zero certificates.

## Addendum 2: cap-23 atlas pass over the 34 length-15 MS-open rows

One shared 60M atlas, 40M forward per challenge, 2,224s total. **0 solves.**

20 CLOSED, reproducing exactly the four large wells found by the independent
closure sweep — 13,440,784 (4 rows), 13,728,824 (4), 13,909,464 (6),
13,978,168 (6) — via a different engine path.

14 BUDGET, each now a proved path-length bound at cap 23:

| challenge | forward depth | no path of length <= |
|---|---|---|
| ac-09961 | 132 | **140** |
| ac-02828 | 131 | **139** |
| ac-08892 | 113 | 121 |
| ac-08168 | 112 | 120 |
| ac-01956 | 100 | 108 |
| ac-05811 | 100 | 108 |
| ac-03471 | 81 | 89 |
| ac-02422 | 80 | 88 |
| ac-03525 | 26 | 34 |
| ac-01083 | 25 | 33 |
| ac-04300 | 24 | 32 |
| ac-09350 | 24 | 32 |
| ac-01558 | 21 | 29 |
| ac-06672 | 20 | 28 |

Amortising the atlas lifted ac-02422 from a bound of 72 (20M/side, shared
budget) to 88. The atlas radius stayed at 8 even at 60M: radius 9 at cap 23
exceeds that allocation.
