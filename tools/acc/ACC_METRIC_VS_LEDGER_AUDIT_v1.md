# Metric versus ledger — an audit of this session against the split

    METRIC = eye(state)                          may lie, may loop
    LEDGER = (challengeId, moves, verifier ok, endpoint)

    AC ledger endpoint:     (x,y)
    Stable ledger endpoint: []  via (x,y)|[16,15] or (y,x)|[16,15]

    Scoreboard reads LEDGER length only.
    If kTeams already holds a shorter LEDGER, the METRIC improvement is 0.

Test applied: **delete the eyes and see what receipt survives.**

---

## The accounting

| | count |
|---|---|
| Ledger lines the frozen verifier will cash | **14** |
| …on rows the 2026-09-12 board lists UNSOLVED | **0** |
| …worth 0 because another team holds shorter | **14** |

    ac-00104 22  ac-00286 53  ac-01635  8  ac-03919 61  ac-04308 23
    ac-04359 17  ac-05406 67  ac-06500 15  ac-07445 13  ac-08327 17
    ac-08491  8  ac-08651 58  ac-09594 15  ac-09868 25

All fourteen on already-solved rows. **Scoring value: zero.**

## Everything else this session is metric

| output | count | why it is not a ledger |
|---|---|---|
| family disconnection theorems, n=3..10 | 8 | proves where a receipt *cannot* be written |
| path-length lower bounds | 8 | a bound is not a path |
| MS-open closure theorems | 40 | same |
| "Gordon certificates" | 7 | **Gordon is not an official challenge ID** |
| proven-optimal Gordon lengths | 7 | optimal within a research fixture |
| eyes built | 7 | metric by definition |
| eyes surviving calibration | 2 | still metric |

### The category error I was making all session

I called the seven Gordon paths **certificates**. They replay to TARGET
through the frozen core, so they are sound mathematics — but there is no
`challengeId` for them in `manifest.json`, so the frozen verifier cannot cash
one. Under the split they are metrics wearing a ledger's name. The same goes
for calling the family results "results": eight disconnection theorems are
the *opposite* of a ledger line, since each proves that no receipt exists
below a stated cap.

Negative information with real operational value — do not search there — and
zero scoring value.

## CYCLE_TYPE fails the routing test, for the reason it looked good

Promoted earlier because it is invariant under all eight conjugation moves.
Routing test on the verified Gordon q=6 path, target signature
`r0=(3,3), r1=(5,1)` at p=5:

    both signatures match the target at exactly ONE step: step 17, the target
    r0 never matches before the final move; the reading is flat-False throughout

So it is a **goal test with no gradient**. And the cause is the property that
made it attractive: conjugation-invariance means it cannot separate states
inside a conjugacy orbit, which is exactly what a router must do. The
stability and the uselessness are one fact.

Revised status: `CYCLE_TYPE` is **[COMPUTED], invariant, not a router**. Its
only demonstrated value is the seven-transition refinement over the binary
kernel test along a known path — diagnostic, not navigational.

## Eye scorecard under the split

| eye | metric quality | routes to a ledger? |
|---|---|---|
| EXPONENT_PAIR | separates control/target at step 0 | untested |
| CYCLE_TYPE | conjugation-invariant, refines kernel test 7:0 | **no — no gradient** |
| PINCH_PROFILE | found the R=46.7 step-1 bottleneck | untested |
| EUCLIDEAN_PROGRESS | flat on every control | FAILED |
| CORRIDOR_RESISTANCE | identical across all roots | FAILED |
| RELATIONAL_ACTION | 491 vs 503, no separation | not promoted |
| POTENTIAL_V | trivial | not promoted |

**Zero eyes demonstrated to route toward a receipt.**

## What the split says to do next

The only thing that moves the scoreboard is a verified path on a row where
`kTeams` holds nothing shorter. Every such row in reach is either:

- **MS-open (550 rows, k=0)** — any verified path scores the full point, and
  all 40 at length ≤ 15 are closed at their caps; or
- **a family root (21 rows by symmetry, 118 by the external map)** — all
  eight roots closed through caps 20–35, walls at total length 21–36.

So the disconnection work has ruled out the cheap regions where a receipt
could have been written. That is the honest reading: the session bought
better knowledge of where *not* to look and produced no line to cash.

**SUBMIT NOW: NONE** — and the ledger is telling the truth.
