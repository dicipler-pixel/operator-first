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

## 7. What this changes

- The corridor closures should be restated as disconnection results. They are
  stronger that way and they say what actually blocks transport.
- The instrument needs the fourth record — the component count, or at minimum
  whether the target's own component was ever touched. A BFS from the start
  cannot see it, so this needs a second search seeded at the target.
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
