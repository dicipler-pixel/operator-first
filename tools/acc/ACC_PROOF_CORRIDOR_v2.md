# Length-corridor obstructions in the ACC AC pool

*v2 — supersedes v1 by adding a uniform random census; v1 reported six
hand-picked instances only.*

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


## A uniform random census

The six results above are hand-picked (they are instances no team has solved),
so they cannot speak for the pool. To test whether the obstruction is general, a
**uniform random sample of 240 challenges** was drawn from the full 10,115-item
AC pool (fixed seed `20260914`, reproducible) and each run at headroom +8 under
an 8,000,000-node budget.

| outcome | count | share |
|---|---|---|
| corridor **closed**, no certificate exists | 30 | 12.5% |
| budget reached (corridor > 8M states, unknown) | 210 | 87.5% |
| **certificate found inside the +8 corridor** | **0** | **0%** |

Every challenge that yielded a verdict yielded the same one. Closed-corridor
volumes ran from 242,960 to 7,505,816 (median 1,225,696), across initial lengths
16 to 34, and all 30 were distinct.

**Observation.** In 240 uniformly random ACC AC presentations, not one admits an
AC-trivialization that keeps every intermediate presentation within +8 of its
own initial total length. For 30 this is proved by exhaustion; for the other 210
the corridor exceeds 8M states and the question is open.

Since 6,466 of these challenges do have verified solutions on the public
leaderboard, those solutions must expand beyond +8. The obstruction is therefore
not an artifact of unsolvability — it is a property of how AC trivializations in
this pool are shaped: they go up before they come down.

## Two unexplained observations

Offered as observations, with no mechanism claimed.

1. **Equal volumes across non-isomorphic corridors.** ac-03165 and ac-09417 have
   corridors of 29 and 27 BFS levels respectively, diverging by depth 3
   (423 vs 433 states), so the graphs are *not* isomorphic. Both contain exactly
   397,312 states. Neither lies in the other's component, and neither is the
   other's image under any of the 16 signed-permutation/relator-swap maps — by
   Nielsen the only length-preserving automorphisms of F₂.

2. **Few volumes within a fixed length profile.** Among challenges of profile
   (|r0|,|r1|,cap) = (8,13,29), 11 closed corridors take only 2 distinct volumes;
   at (10,11,29), 7 take 4. Across differing profiles no such collapse occurs —
   the random census's 30 volumes are all distinct — so this is a within-profile
   effect, not a pool-wide quantization.

   *An earlier draft of this work reported the second observation as a pool-wide
   law. That was wrong: the sweep producing it processed challenges in
   length-sorted order, concentrating its closures in two profiles. The random
   census refutes the general claim and is the reason it is stated narrowly here.*

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
budgets without closing, as did 210 of the 240 census challenges. Those runs
establish **nothing** and are reported only so they are not mistaken for
evidence of hardness. ac-00001 is the largest measured: 149,999,998 states at
depth 26 without closing, so its +8 corridor exceeds every one that did close.

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
