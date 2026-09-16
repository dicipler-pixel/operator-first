# Response to the external sync audit — corrections accepted, one defended

Three of their corrections are right and I verified each before accepting.
One challenge is answered by the code. Two of my own claims are withdrawn.

## Accepted: DONOR_EXIT is not a kernel test

`DONOR_EXIT` in `mh_eyes_v1.py` detects disappearance or relocation of a
four-run **exponent pattern**. It does not test whether `rho(r0)` leaves the
identity. Verified on all eight roots:

| n | rho(r0) before | rho(r0) after move 2 | left kernel | my DONOR_EXIT |
|---|---|---|---|---|
| 3 | I | [[-16,-3],[11,2]] | yes | **0** |
| 4 | I | [[-25,-4],[19,3]] | yes | **0** |
| 5 | I | [[-36,-5],[29,4]] | yes | **0** |
| 6 | I | [[-49,-6],[41,5]] | yes | **0** |
| 7 | I | [[-64,-7],[55,6]] | yes | **0** |
| 8 | I | [[-81,-8],[71,7]] | yes | **0** |
| 9 | I | [[-100,-9],[89,8]] | yes | **0** |
| 10 | I | [[-121,-10],[109,9]] | yes | **0** |

**8/8.** Two genuinely different events. They must be recorded under separate
labels — `EXPONENT_PATTERN_EXIT` and `DONOR_KERNEL_EXIT` — and neither
subsumes the other. Their additive kernel eye is the right fix and leaves
mine unchanged.

## Accepted: the single-fire claim was even-only

I reported that the pattern exit fires exactly once per control path, always
on move 3. Measured across all four supplied controls:

    q=6   1 fire   step 12, move 3
    q=8   1 fire   step 15, move 3
    q=10  1 fire   step 18, move 3
    q=9   2 fires  step 15 move 2, and step 40 move 5

The claim holds for the **even** subset only. q=9 fires twice, on different
moves. The contrast belongs in calibration and must not be averaged away.

## Withdrawn: "all 40 open by cap 23"

Wrong, and the raw sweep says so: **20 rows are CLOSED at cap 23**, the
highest cap they were tested at. Closed means disconnected, not open. The
correct statement is that those rows' walls are **no higher than cap 23**
under a 25M allocation, and they become *undecided* at cap 24 — and
undecided is not connected.

## Withdrawn: "nine wells"

I grouped the 40 MS-open rows by `(cap, component size)` and called the nine
resulting classes wells. That contradicts my own earlier result, proved
repeatedly in this session, that **equal component size does not imply the
same component** — ac-01956 vs ac-02828 at four separate caps, ac-01558 vs
ac-00399 at three, ac-03467 vs ac-08126 at cap 22. I proved the principle and
then violated it.

Nine distinct cardinalities are nine distinct **size classes**. Establishing
nine components needs membership transports, which were not run. The
partition claim is withdrawn; the individual closure theorems behind it stand.

## Defended: the df + db bounds

Their concern is that a budget stop may leave a partial layer, making the sum
unjustified. The engine's loop is:

    uint32_t stop = S->lvlend;
    while (S->head < stop) { ...expand, BUDGET returns HERE... }
    S->depth++;  S->lvlend = S->nst;      // only after a FULL level

`depth` increments only after an entire level is expanded, so `depth == d`
implies every state at distance `<= d` is interned. BUDGET fires inside the
loop, part-way through expanding the distance-`d` states, at which point
`depth` is still `d` and the ball of radius `d` is complete. The partial
level is `d+1` and is never claimed.

The meet test is symmetric in time: each newly interned state on the
expanding side is looked up in the other side's table, so if F interns X
first and B reaches X later, B's own intern finds it. No meet is missed by
ordering.

Hence two complete disjoint balls, and any path of length `L <= df + db`
would place the vertex at forward distance `df` at backward distance
`L - df <= db`. The bound stands. The same invariant governs the atlas
radius: `atlas_R` advances only on a complete level, with an explicit
`if(!full) break;` before the increment.

Source uploaded to the Hub with this invariant documented at the top, so it
can be checked rather than taken on trust.

## Their reproduction

Their independent older forward engine returned R6 cap 27 = 18,503,200 and
R7 cap 29 = 27,589,040 — exact matches to mine. Since then both walls have
moved one cap further, closing at 65,724,220 (R6 cap 28) and 102,424,140
(R7 cap 30), so headroom is **>= +9** on both, not +8.

## Family ladder, current

| n | closed through | component | min total length |
|---|---|---|---|
| 3 | 19 | 23,609,984 | 20 |
| 4 | 22 | 2,064,600 | 23 |
| 5 | 25 | 11,688,560 | 26 |
| 6 | **28** | 65,724,220 | **29** |
| 7 | **30** | 102,424,140 | **31** |
| 8 | **31** | 39,303,140 | **32** |
| 9 | **33** | 54,022,680 | **34** |
| 10 | 34 | 16,768,300 | 35 |

Additional bounds where the next cap did not close: R6 cap 29 no path <= 54,
R_8 cap 32 no path <= 53, R_9 cap 34 no path <= 50.

## Their row counts supersede mine

My 4 and 5 symmetry-only rows are subsets of their constructive groups of 20
and 26. Their group sizes n3:14, n4:14, n5:14, n6:20, n7:26, n8:10, n9:10,
n10:10 total 118. I could not reach those because the branch-root map was
absent from this environment; that was a transfer gap, not a missing artifact.
Their count is the operative one.
