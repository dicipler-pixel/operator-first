# New targets from component structure

Written against the 2026-09-15 search-pass report. It is not an attempt to
re-solve those four candidates; it takes the *logic* of that pass — reverse
ball, finish dictionary, transformation grouping, representative-first
scheduling — and states what component analysis adds to each, and what new
targets fall out.

---

## 1. The two groupings are the same relation

The report groups 2,673 unsolved rows into **1,156 constructively linked
groups** by replaying 32,008 transformation steps, and drops 1,517 redundant
targets from scheduling.

Component analysis groups challenges by membership of a connected component of
the length-capped move graph.

These are the same relation, with the cap as the only parameter:

> Two presentations lie in the same component at cap `K` **iff** there is an
> Andrews–Curtis move sequence between them whose every intermediate state has
> total relator length `≤ K`.

Left to right is the BFS path; right to left is that the sequence never leaves
the capped graph. A constructive transformation with maximum intermediate
length `M` therefore proves same-component at every cap `≥ M`, and
same-component at cap `K` yields a constructive transformation bounded by `K`.

## 2. What each method can prove that the other cannot

|  | transformation search | component enumeration |
|---|---|---|
| proves two rows **are** linked | yes, with an explicit path | yes, with an explicit path |
| bounded intermediates | not guaranteed | by construction, `≤ K` |
| proves two rows are **not** linked | **no** — a failed search is not a proof | **yes**, when the component closes |
| cost | cheap per pair | one exhaustive enumeration per component |

The asymmetry is the whole contribution. A transformation search that fails to
connect two rows has found nothing; an exhausted component enumeration that
does not contain the other row is a **proof of non-transferability at that
cap**. That is a scheduling fact the transformation audit cannot produce:

> these rows will never transfer to one another below cap `K`, so do not
> schedule a transfer attempt — they need genuinely separate searches.

## 3. Cross-validation of the reverse ball

The report rebuilt an exact 8-move reverse ball of **24,587,144 states** with
zero cap rejections. Because the AC move set is closed under inverses, that
object is the same as a *forward* BFS ball around the trivial presentation, and
this repository computed it independently with a different implementation:

```
depth        cap 47        cap 64     truncated by cap 47
    1            11            11                       0
    2            88            88                       0
    3           662           662                       0
    4         5,115         5,115                       0
    5        40,779        40,779                       0
    6       336,477       336,477                       0
    7     2,848,667     2,849,131                     464
    8    24,466,204    24,583,188                 116,984

  reported uncapped 8-move ball : 24,587,144
  independent cap-64 ball       : 24,583,188
  difference                    :      3,956
```

Two independent implementations agree to **99.9839 %**, and the residual 3,956
states are exactly those whose total relator length exceeds 64 — the hard guard
in this repository's engine. So the report's "zero rejections" claim is
corroborated from the outside: it really is the uncapped ball, and the gap is
*this* engine's limit, not theirs.

Two consequences worth acting on:

- **This engine structurally cannot hold the full 8-move ball.** Its two-uint64
  state packing caps a relator pair at 64 letters. Any bidirectional scheme
  built on it inherits a 3,956-state blind spot at depth 8, growing at deeper
  levels.
- **Level sizes grow ×8.6 and are still accelerating at depth 8.** A 9-move
  ball is therefore ≈ 210 M states and a 10-move ball ≈ 1.8 G. Depth 9 is
  reachable with real memory; depth 10 is not, by this construction.

## 4. New targets

### 4a. Multi-member components — free leverage

A component containing `n` challenges is an `n`-for-one target: a certificate
for any member transfers to all the others along the connecting path, and the
transfer path is bounded by the cap for free.

Measured in the complete length-14 profile at cap 22:

```
ac-00413, ac-02089, ac-04376, ac-05932   one component, 37,464,032 states
```

All six pairs return `FOUND`. **Four challenges, one component.** They are
currently disconnected from the trivial presentation at cap 22, so none is
solvable there — but the moment that component joins the target's, all four
become solvable together.

This is the target class worth hunting: not individual unsolved rows, but
components with high challenge-multiplicity. It is representative-first
scheduling with the representative chosen by proof rather than by heuristic.

### 4b. Proven-dead caps — a scheduling filter

Every closed corridor is a proof that forward search at that headroom is
wasted, because the target is provably in another component. The complete
profiles so far give 20 such proofs at lengths 37 and 39, 3 at length 14, plus
the census. Those rows should not be scheduled again at those caps by any
method.

### 4c. The connection threshold as the real difficulty measure

"Closed vs budget" is an artifact of the node limit. The invariant quantity is

> the least headroom at which a challenge's component contains the trivial
> presentation.

Two measurements bound it already: `ac-02509` is disconnected at +8 and again
at +10, so its threshold exceeds 10.

### 4d. The wall that says build bidirectional

`ac-04308` has a known 21-move record. Forward BFS gives 23 at +8, and at every
headroom from +10 to +24 the corridor exceeds 40 M states at depths
16, 12, 10, 9, 9, 8, 8 — **reachable depth falls as headroom rises.** Too
narrow to hold the record at +8, too wide to reach its depth above it. No
single forward cap closes this gap, which is the concrete case the report's
bidirectional approach answers.

## 5. What this does not claim

- No pricing. Nothing here is a submission or a score estimate.
- The 1,156 groups are not re-derived or checked; §1 argues the relations
  coincide, not that either enumeration is correct.
- Component multiplicity is measured on complete short profiles only. Whether
  high-multiplicity components are common among the 2,673 unsolved rows is
  untested — that is the next measurement, not a claim.
- Equal component size does **not** imply same component, and does not imply
  different either. The length-14 profile contains both outcomes at equal size
  *and* equal depth. Only a search decides.

## Attribution

Author: Jeromie N. Beasley (research direction). Mathematical assistance: AI.
The reverse-ball, finish-dictionary and transformation-audit results discussed
in §1 and §3 are from the 2026-09-15 search pass and are credited there; this
note cross-checks one of them and builds scheduling logic on top.

No part of this note uses the root-conjugacy, donor-restoration,
coordinate-transport, divisibility, period or companion-restoration ideas of
Robert Sneiderman (ACC-P000002), so no such citation is claimed.
