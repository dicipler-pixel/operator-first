# Shape atlas

Raw eyes are microscope readings. The search should not see six of them; it
should see a small number of **fused shapes**, discovered by working backward
from outcomes. This file holds every shape we have actually earned, and — just
as importantly — every eye we tested and rejected.

The atlas stays small on purpose. A new eye may only: fold into an existing
shape, split one shape into two behaviours, or expose a genuinely new mechanism.
Anything else is eye explosion, which is noise wearing a lab coat.

---

## S1 — OPENING (uphill move that buys a two-step collapse)

**Ingredients** (fused, not voted):

```
len_delta   >= 0          immediate length does NOT improve
floor2      <= -3         best length reachable in TWO moves drops by 3+
```

**How it was found.** Not by picking plausible eyes. The 19 verified
certificates take a non-length-reducing move 52.6% of the time (163/310), so
length alone cannot explain half their choices. Scoring *all 14 moves at every
state* gives 310 chosen against 4,030 **declined** — the negative class the
original audit had no way to see — and then asking what separates chosen from
declined **within the non-decreasing moves only**:

| reading | chosen | declined | separation |
|---|---|---|---|
| **2-step floor** | **−1.215** | **−0.370** | **−0.845** |
| len_delta | +0.589 | +2.196 | −1.607 |
| ledger_same | 0.663 | 0.589 | +0.074 |

**Historical stats**

```
observed            163 chosen non-decreasing moves, 3,925 declined
precision at -3     17.7%   against a 4.0% chance rate   -> 4.4x lift
coverage at -3      33/163 of the chosen non-decreasing moves
source              19 verified certificates, 310 primitive moves
scope               SMALL SAMPLE. One corpus, all of it winning paths.
```

**Where it is used: nowhere. RETIRED from the mixer, with the A/B that retired it.**

| variant in `ac_descent_ball_v1.c` | vs baseline, identical rows and budget |
|---|---|
| FLOOR2 as a scoring rule | improved 0, same 8, **worse 10** of 18 |
| FLOOR2 as an atomic two-move macro | improved 0, worse 0, same 21 of 21 |

Scoring the opener alone licenses wandering uphill, because a random walk then
picks its next move at random instead of the one that cashes the drop in. Making
the pair atomic repaired that damage exactly — and bought nothing.

**And it was genuinely exercised**, which is what makes this a negative rather
than a non-event. Instrumented fire counts:

```
ac-01199   macro fired 17,618 of 302,386 openers evaluated   (5.8%)
ac-00215   macro fired 13,282 of 306,613                     (4.3%)
```

A 5% injection rate of the right moves moved `minlen` not at all. So the descent's
failure to get below 18–21 is **not a move-selection problem**. The barrier is
structural: from these starts there is no short route down within a random walk's
reach, whatever the local rule. That is consistent with the corridor proof —
`ac-06639`'s shortest path under `|r|+8` is 35 moves at forward depth 28, and a
random walk does not find a specific 35-move sequence.

**Consequence: stochastic descent is the wrong tool for these rows.** Exact
bidirectional search is the right one. S1 stays in the atlas as a real offline
regularity, not as a search heuristic.

---

## Rejected eyes — recorded, because a silent eye is also data

### R1 — move-space rotation ("turn")

The 14-entry profile of what each move would do to length, re-oriented across a
step. Proposed as the replacement for length-based scoring, on the statistic
*"turn ≥ 0.50 is followed by a lower state within 5 moves, 89.7% of the time."*

**Rejected on two independent grounds.**

*No base rate.* Over all 310 moves the collapse-within-5 rate is **85.5%** — these
are short winning paths, so almost every point has a lower state ahead. Measured
lift of the turn eye: **+0.9pp**.

*Below chance as a discriminator.* Against the declined moves:

| threshold | covers (chosen) | declined | precision | chance |
|---|---|---|---|---|
| turn ≥ 0.3 | 72/310 | 1100 | 6.1% | 7.1% |
| turn ≥ 0.5 | 22/310 | 334 | 6.2% | 7.1% |
| turn ≥ 0.7 | 0/310 | 21 | 0.0% | 7.1% |

Mean turn on chosen moves is 0.194; on declined moves, 0.200. There is no signal.
Building the search around it would have been steering on noise.

**Kept in `ce_shapes.py` anyway.** It costs nothing to compute, and if a later
corpus gives it a negative class where it *does* separate, the record is here to
compare against. An eye is retired from the *mixer*, not deleted from the
*record*.

---

## Method

```
raw eyes on every candidate, chosen AND declined
        |
   align by outcome (chosen / declined; later, certificate / dead)
        |
   test each ingredient against a BASE RATE and a chance rate
        |
   drop what does not separate, fuse what does
        |
   SHAPE + its historical stats
```

The step that does the work is the negative class. A statistic computed only over
successes measures the corpus, not the mechanism — which is how a 4.4× signal and
a below-chance one ended up quoted side by side as though both were findings.
