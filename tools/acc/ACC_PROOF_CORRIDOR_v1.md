# Length-corridor obstructions for six unsolved ACC Discovery presentations

**Track:** Proof · **Conjecture:** AC · **Direction:** proof (partial result)
**Status:** draft for submission — not yet submitted

## Summary

For six balanced two-generator presentations from the ACC Discovery AC pool, we
establish by exhaustive enumeration that **no Andrews–Curtis trivialization
exists that keeps every intermediate presentation within a stated total relator
length**. Each result binds paths of *any* length: it is exhaustion of a closed
region of the move graph, not failure of a bounded search.

All six are, as of this writing, unsolved by every team on the public ACC
Discovery leaderboard.

| challenge | initial length | corridor cap | headroom | exhausted at depth | component size |
|---|---|---|---|---|---|
| ac-00035 | 19 | 27 | +8 | 57 | 79,338,584 |
| ac-00002 | 25 | 33 | +8 | 51 | 4,658,392 |
| ac-00008 | 16 | 24 | +8 | 46 | 2,605,640 |
| ac-00007 | 22 | 30 | +8 | 42 | 578,752 |
| ac-00026 | 24 | 32 | +8 | 55 | 507,800 |
| ac-00036 | 24 | 32 | +8 | 39 | 398,824 |

**Theorem (six instances).** Let `P` be one of the presentations above and `C`
its corridor cap. There is no finite sequence of ac-r2-v1 moves carrying `P` to
`(x, y)` in which every intermediate presentation has total relator length at
most `C`.

*Proof.* Enumerate the connected component of `P` in the subgraph induced by
states of total relator length `≤ C`. The component is finite and was closed
(no new states at the stated depth). `(x, y)` is not in it. Since any
trivialization staying within the corridor would be a path inside this
component, none exists. ∎

## What this does and does not say

It does **not** claim these presentations are AC-nontrivial. The AC conjecture
places no bound on intermediate word size, and these results say nothing outside
their corridor. Each presentation's abelianized determinant is ±1, so the
standard obstruction does not forbid triviality; they remain live candidates.

What it does say is that any trivialization must **expand**. For ac-00008 that
means growing from 16 letters past 24 — more than 50% — before it can descend.
This is a concrete obstruction for search methods that penalize length, and it
is a plausible reason these instances are unsolved across the field.

## A separator: corridor volume

Define `V(h)` as the number of presentations reachable from `P` without any
intermediate total length exceeding `init(P) + h`. At the **same** headroom
`h = 8`, the six span a factor of **199**:

```
ac-00035  init 19   79,338,584
ac-00002  init 25    4,658,392
ac-00008  init 16    2,605,640
ac-00007  init 22      578,752
ac-00026  init 24      507,800
ac-00036  init 24      398,824
```

The ordering tracks neither initial length nor exhaustion depth: ac-00035 is the
second shortest presentation yet has the largest corridor by 17×, while ac-00026
is longer and has 156× less room. Small `V(h)` means the moves barely open the
presentation up at all.

`V(h)` is a property of the move graph under a length cap. It is **not** claimed
as an invariant up to AC-equivalence, and we offer it as an empirical separator
rather than a theorem.

## Method and verification

Forward breadth-first enumeration from `P` over the length-capped subgraph, with
every discovered state tested for membership in a precomputed ball of radius 7
around `(x, y)` (2,512,679 states, built once and reused).

Two independent implementations were used and cross-checked:

1. Python, applying moves through the competition's own
   `verifier.core.apply_move` (move spec `ac-r2-v1`) with no re-implementation.
2. A C engine with 2-bit letter packing, used where the state count exceeds
   Python's practical reach.

On ac-00035 the two agree **exactly** on cumulative state counts at all 17
depths the Python run reached, up to 7,812,471 states, with zero disagreements.
Across randomly generated presentations the C engines reproduce
`verifier.core` component sizes exactly (10/10 and 5/5), and every certificate
they emit is accepted by the official `core.verify` (7/7 each).

## Open

ac-00012, ac-00001, ac-00025, ac-00014, ac-00019 and ac-00010 reached their node
budgets without closing. Those runs establish **nothing** and are reported here
only so they are not mistaken for evidence of hardness.

Corridor enumeration becomes impractical well before `+16` headroom: on ac-00008
at cap 32 the frontier grows ~2.7× per level, putting exhaustion beyond reach of
the hardware used here.

## Prior work and attribution

Move semantics, challenge data and all verification are the ACC organizers'
(`saircompetition/andrews-curtis`, move spec `ac-r2-v1`). The mathematics of the
Andrews–Curtis conjecture is not ours; the contribution here is computational —
the six corridor exhaustions and the `V(h)` observation.

No part of this result uses the root-conjugacy, donor-restoration,
coordinate-transport, divisibility, period or companion-restoration ideas of
Robert Sneiderman (ACC-P000002), so no such citation is claimed.
