# What the Atlas says about transport, applied to the corridor search

Read on the suggestion to look at the matter and gravity papers for what
affects transport. Both papers are one-page registers pointing at Atlas cards;
the cards are where the transferable content is. Two further cards turned out
to be more on-point than the ones those papers cite.

This note records what transfers, and one structural correction it produced.

---

## 1. The correction: a closed corridor is a DISCONNECTION, not a distance

This is the important one, and the Atlas is what prompted the check.

Every AC challenge in the frozen manifest has target relators `[[1],[2]]` —
total length **2**. All 10,115 of them; I checked the whole pool, not a sample.
Every corridor cap is `initial_length + headroom ≥ 9 + 0`. So:

> **The target is always a vertex of the cap-bounded graph.**

The corridor engine does BFS from the start over states of total relator length
`≤ cap`. `EXHAUSTED` means that BFS emptied its frontier: the start's connected
component is fully enumerated. The target is in the graph and was not found.
Therefore:

> **A closed corridor proves the start and the trivial presentation lie in
> different connected components of the length-capped move graph.**

Not "the target is too far". Not "the search ran out". *Disconnected.*

That is a sharper statement than anything in `ACC_PROOF_CORRIDOR_v3.md`, which
phrased the closures as exhaustion bounds. The mathematical content is the
same; the reading is much stronger, and it says exactly what blocks transport:
**connectivity, not distance.**

It also kills a tempting inference I had not yet made but was one step away
from: that a large corridor makes a certificate likely. Component size says
nothing about whether the target is in *that* component.

## 2. `GRAPH-SUBGRAPH-CAPACITY` — global capacity does not imply coverage

> *Failure mode: passing the full-graph Euler bound does not imply
> biplanarity. Conditional capacities alone do not certify arbitrary
> planarity claims.*

The transferable shape: **a global capacity bound never certifies a covering.**

Applied here: "the corridor holds 2,464,344 states, surely a 47-length path
fits" is exactly the refused inference. Capacity of the whole graph is not
coverage by the reachable part. §1 is this failure mode made concrete — the
graph has room for the target and the start still cannot reach it.

## 3. `OBS-INTERIOR-AMBIGUITY` — identical exterior, different interior

> *Statement: the tested family has identical full exterior evolution and
> different hidden dynamics.*
> *Failure mode: adding an unavailable interior signal to a display does not
> make it an exterior measurement.*

This card is the precise, already-written reason the corridor-volume
quantization claim was wrong — and it was in the Atlas before I made the claim.

```
ac-02509   component 2,464,344   depth 51
ac-02681   component 2,464,344   depth 46
```

Identical **exterior response** (the component size, what the search reports),
different **interior** (the depth, the shape of the component). The card says
plainly that the first does not determine the second. Reading structural
identity off a coincidence of exterior measurements is the named error.

The failure mode adds a discipline I had been sloppy about: depth is an
interior signal and volume is an exterior one. Listing them side by side as if
they were the same kind of measurement invites exactly this mistake. They
should be reported as separate records — which is what card 4 says outright.

## 4. `CASCADE-FOUR-RECORDS` (matter) — four records, and non-monotonicity

> *Statement: track support, projector motion, hidden feedback and a
> separately named topological invariant during a cascade.*
> *Failure mode: … a window count can increase under a positive peel.*

Two transfers.

**Four separable records.** The corridor engine reports one number and a depth.
The card's discipline says record four things that cannot be confused:

| record | corridor analogue | reported today? |
|---|---|---|
| track support | which states the start component contains | only its size |
| projector motion | how the BFS frontier moves per level | no |
| hidden feedback | re-entry into already-seen regions | no |
| a named topological invariant | component count of the capped graph | **no — and this is the one that matters** |

The fourth is the gap. My BFS only ever sees the start's component, so the
component count of the capped graph is invisible to the instrument. That is
precisely the invariant §1 shows is decisive.

**Non-monotonicity.** "A window count can increase under a positive peel"
warns that shrinking a parameter can increase a count. Here: lowering the cap
strictly shrinks the vertex set, but can *fragment* it, so the number of
components can rise while the state count falls. Monotone volume, non-monotone
connectivity. Transport depends on the non-monotone one.

## 5. `GEO-OVERLAP` (gravity) — a null leading coefficient decides nothing deeper

> *Failure mode: null quadratic coefficient does not decide higher-order cap
> behaviour.*

The same shape as §3 at a different order: two objects agreeing to leading
order may differ beyond it. Corridor volumes agreeing does not constrain the
depth, the diameter, or the component's shape.

---

## 6. The experiment the reading suggested

If a closed corridor is a disconnection, the natural quantity is not "closed
or budget" but the **headroom at which the start's component first absorbs the
target** — the transport threshold. That is a property of the challenge, not
of the search budget.

`ac-02509` (initial total relator length 39):

| headroom | cap | verdict | start component | depth |
|---|---|---|---|---|
| +8 | 47 | closed | 2,464,344 | 51 |
| +10 | 49 | closed | 14,302,296 | 58 |
| +12 | 51 | budget | > 40,000,000 | — |

Two independent disconnection proofs at two different caps. The component grows
5.8× and still does not reach a target that has been inside the graph the whole
time. The obstruction is not being out-run by volume.

### And the fourth record, finally measured

The card said the missing invariant was the one a start-seeded BFS cannot see.
It costs nothing to get: run the same engine seeded at the **target**. The
trivial presentation is just another state.

Target component at cap 47, level by level:

```
depth 1            11
depth 2            88     x8.00
depth 3           662     x7.52
depth 4         5,115     x7.73
depth 5        40,779     x7.97
depth 6       336,477     x8.25
depth 7     2,848,667     x8.47
depth 8    24,466,204     x8.59     budget 40,000,000 hit, still growing
```

Set against the start's component at the *same cap*:

| | states | levels | average branching |
|---|---|---|---|
| start of ac-02509 | 2,464,344 (**closed**) | 51 | 1.33 |
| trivial presentation | > 40,000,000 (budget) | ≥ 8 | ~8.6 |

At cap 47 these two components are provably **disjoint** — the start's is
closed and does not contain the target.

So the start of ac-02509 does not sit far from the trivial presentation. It
sits in a **small, narrow, closed pocket**: 2.46 million states, fifty-one
levels deep, branching 1.33 per level — while the trivial presentation lives in
a region that puts twenty-four million states inside eight levels at branching
8.6. The pocket is not a distant part of the same country. It is a different
component.

**A caution on my own language.** "Narrow and deep" is phrasing I used earlier
about ACC and then withdrew, because I had generalised it from the training
instances to the whole pool and to headroom advice. Nothing here revives that.
This is one challenge, one cap, two measured components — a measurement, not a
generalisation, and it says nothing about where scored solutions live.

## 6b. Building the missing instrument, and what it proved

`ac_corridor64_v1.c` hardcodes the trivial presentation as its target, so a BFS
from a start can only ever answer *"is the trivial presentation in this
component"*. The component structure of the capped graph is invisible to it.
That is exactly the invariant `CASCADE-FOUR-RECORDS` says to track separately.

`ac_corridor64_target_v1.c` takes the target from the command line. v1 is
untouched. It range-checks the target against the cap and, on exhaustion,
reports `disjoint=1` — because an exhausted search whose in-cap target was not
found *is* a disjointness proof.

**Regression first.** With the trivial presentation as target it must reproduce
v1 exactly:

```
EXHAUSTED states=2464344 depth=51 cap=47 disjoint=1     (v1: 2,464,344 / 51)
```

### The two coincidences are real, and they are not one component

The obvious deflationary explanation for two challenges reporting identical
component sizes is that they are *the same component* seen from two roots —
which would make the coincidence trivial and the depth difference a mere change
of basepoint. That is now refused:

```
is ac-02681's start in ac-02509's component?   EXHAUSTED 2,464,344 d51  DISJOINT
is ac-02509's start in ac-02681's component?   EXHAUSTED 2,464,344 d46  DISJOINT
```

And for the triple, all six ordered pairs:

```
ac-06819 / ac-07442 / ac-08090   — every pair DISJOINT
                                   2,696,184 states each, depths 53, 63, 62
```

So at cap 47 the following are **proved pairwise disjoint**:

| component | states | depth |
|---|---|---|
| ac-02509 | 2,464,344 | 51 |
| ac-02681 | 2,464,344 | 46 |
| ac-06819 | 2,696,184 | 53 |
| ac-07442 | 2,696,184 | 63 |
| ac-08090 | 2,696,184 | 62 |
| trivial presentation | > 40,000,000 | ≥ 8 |

**At least six distinct components**, and the five small ones take exactly
**two** distinct sizes across five independent components with five different
depths.

This is `OBS-INTERIOR-AMBIGUITY` in its sharpest form: identical exterior
response, different interior, and now the "maybe they are the same object"
escape is closed by proof rather than left open.

**What this is not.** It is five measured components at one cap in one length
profile. The pool-wide corridor-volume quantization claim stays retracted — the
census that killed it sampled the whole pool and found thirty closed corridors
with thirty distinct sizes. What is new here is only that within this profile
the coincidences are between genuinely distinct components, which the census
never addressed and which I had previously left as the weaker "possibly the
same component" reading.

### A bug worth recording

The first version of the same-component test used the official verifier's
`apply_move` with the wrong arity, inside a `try/except Exception: continue`.
Every call raised `TypeError`, every exception was swallowed, the frontier was
empty at every depth, and the script cheerfully reported "not reachable". A
search that never ran, reported as a negative result.

It was caught only because a BFS that reports `total 1` at depth 8 is
obviously broken. The fix was not just the arity: the rewritten test asserts
the move function produces successors *before* trusting any negative answer.
A negative result from an instrument that was never shown to work is not
evidence.

## 6c. The complete length-39 profile

There are only 28 AC challenges of initial total relator length 39 in the whole
frozen manifest. That is small enough to measure *exhaustively* — no sampling,
no selection, the entire profile at cap 47.

```
28 challenges:  12 closed, 16 budget (component exceeds 40,000,000)

   2,464,344  x2   depths 46, 51            ac-02509 ac-02681
   2,696,184  x3   depths 53, 62, 63        ac-06819 ac-07442 ac-08090
   8,722,080  x1   depth 107                ac-01192
  10,779,012  x5   depths 61, 61, 70, 71, 73 ac-02831 ac-03110 ac-05490
                                             ac-07639 ac-08207
  21,981,528  x1   depth 157                ac-01796
```

**Twelve closed corridors take five distinct sizes.**

This is the within-profile pattern stated on a complete profile rather than a
sample, which is exactly the objection that killed the pool-wide claim. The
census that refuted that claim drew uniformly from the whole pool and mixed
lengths, so it compared corridors living in *different graphs*; corridors at
different caps cannot share a component and their sizes carry no information
about each other. Fixing the profile removes that confound.

It also shows the pattern is not an artifact of my earlier biased shard: two of
these five size classes were unknown before this sweep, and the largest class
has five members.

Note what is *not* claimed. Sizes repeating within a profile is a measurement.
Whether the repeats are distinct components is a separate question, settled
only by search — and for the 2,464,344 and 2,696,184 classes it is settled
(all disjoint). The five-member class at 10,779,012 contains **two corridors of
equal depth 61**, which is the first case where "same size, same depth" makes
the same-component reading genuinely plausible. That test is running.

## 7. What this changes

- The corridor closures should be restated as disconnection results. They are
  stronger that way and they say what actually blocks transport.
- ~~The instrument needs the fourth record~~ — built as
  `ac_corridor64_target_v1.c`, and it immediately proved six pairwise-disjoint
  components at cap 47.
- Volume and depth must be recorded as different kinds of measurement, not as
  two columns of one table.

## Attribution

Atlas cards `GRAPH-SUBGRAPH-CAPACITY`, `OBS-INTERIOR-AMBIGUITY`,
`CASCADE-FOUR-RECORDS`, `GEO-OVERLAP` — Jeromie N. Beasley research program;
the original projector, Schur, spectral and graph methods retain their own
attribution, per each card's credit line. Nothing here claims novelty for
those cards; this note only transfers their failure modes to the
Andrews–Curtis corridor search.

No part of this note uses the root-conjugacy, donor-restoration,
coordinate-transport, divisibility, period or companion-restoration ideas of
Robert Sneiderman (ACC-P000002), so no such citation is claimed.
