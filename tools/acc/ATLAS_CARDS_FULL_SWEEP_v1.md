# All 93 Atlas cards, swept against the ACC work

Source: `preserved/atlas-cards/cards/` in the Compound Eye modular package,
edition **2026-09-07**, `card_count: 93`, numbers 91–93 marked unavailable,
`old_cards_unchanged: true`. Manifest sha `11183b06…19599e9`.

The instruction was to find **all** of them that can help, not one. Below is
every card, classified by how it bears on the corridor/search programme. The
striking result is that four cards describe, in advance and in general terms,
mistakes this session actually made.

---

## Tier 1 — cards that name an error already committed here

### B52 — "The endpoint decides, not the size."
> *class ⇔ |β| at the arc endpoint, not |λmin|. The endpoint distances differ
> by three orders of magnitude between classes while the gaps themselves
> overlap — so a threshold on gap magnitude misclassifies, and the arc
> endpoint never does.*

This is exactly the **nine wells** error. I classified 40 MS-open rows by
component **size** and called the nine size-classes components — after having
separately proved, five times over, that equal size does not imply the same
component (ac-01956 vs ac-02828 at four caps; ac-01558 vs ac-00399 at three;
ac-03467 vs ac-08126 at cap 22). Size overlaps across classes; membership
decides. The card states the general form of the trap; I walked into it and
the external audit caught it.

### B65 — "Two diagnostics, not two views."
> *One operator, two questions… complementary, not equivalent.*

### B70 — "Two null-space questions, and confusing them costs a programme."
> *When something degenerates there are two entirely different questions and
> one word for both.*

Both describe the **DONOR_EXIT** finding precisely. My eye detects a
four-run exponent pattern disappearing; the trefoil eye detects `rho(r0)`
leaving the identity. Verified 8/8: move 2 sends `rho(r0)` from `I` to `H_n`
while my flag reads zero. Two diagnostics, one word. B70's warning — that
conflating them *costs a programme* — is the accurate severity.

### B20 — "Some questions are closed to their own instrument."
> *No amount of counting separates them: the degeneracy is structural, and
> the answer is to change the measurement rather than buy more of it.*

Two independent hits:
1. **Finite images cannot disconnect.** Verified at p=5: the target is
   reachable from `(I,H_n)` for every root, component 14,396 of 14,400
   possible pairs. The instrument cannot answer the question put to it.
2. **The memory ceiling.** More budget does not move R6 cap 30 or R7 cap 31.
   The answer is a different method, not a larger allocation — which is the
   card's prescription verbatim.

---

## Tier 2 — cards that describe the mechanics in play

| card | statement | bearing |
|---|---|---|
| **B13** | Going around swaps the pair; twice restores it | The by-4 group V: moves 0,1 are commuting involutions, twice restores. Also the external `[2,3]` undo control — leaving and re-entering the kernel is not progress |
| **B56** | A curve and a point do not meet — codimension one against codimension two | Disconnection as a generic phenomenon: the target is a single vertex, the component a bulk set; non-intersection is the default, not an anomaly |
| **B46** | The failure to close is the mechanism | Every CLOSED verdict in the ladders. The defect is not an error term to discard — closure *is* the result |
| **B17** | Overflow builds the wall it overflows | The cap creates the corridor. Constraining total length is what makes the component a long thin tube rather than a ball |
| **B19** | The wall stiffens as fast as it is stressed — onset gated by a ratio, not a product | Growth vs cap. Widening the cap raises branching, so reach falls; the trade is a ratio |
| **B37** | A finite count makes it finite | A bounded budget turning an unbounded search into a decidable one — every bound here is of this shape |
| **B94** | A ledger that is Lipschitz in the forgiving metric cannot mark a wall | Why a smooth invariant cannot certify the corridor wall. Bears directly on the search for an unrestricted separating invariant |
| **B49** | One locus, three names — det Hess = adjoint Reidemeister torsion | The external Fox/torsion lane; also the card explicitly cites this as *input, not claim*, which is the right posture for their Fox admission |
| **B95** | The threshold profile reads the cycle type | Reading structure off a threshold sweep — the cap-vs-reach profile |
| **B96** | The gap between the rails is the supply | Bracketing: G9 in [35,48], the gap between bound and known path is the working room |
| **B60** | Saturation flags a hidden rank-one structure | Component sizes saturating at a factor — a structural cause, not noise |
| **B67** | A record that is a group element | Move sequences as group elements; path composition and inversion |
| **B71** | Distance is blind to orientation; holonomy is not | Why component distance misses what the transport/symmetry sees |
| **B81** | The transport is flat; the bundle keeps the curvature | Symmetry transport preserving component structure while the bridge costs moves |
| **B76** | A degenerate point is a count in hiding | Repeated component cardinalities as a count, not a coincidence |
| **B5** | Without a boundary there is no list to count | The cap as the thing that makes enumeration possible at all |
| **B6** | Entropy is membership ambiguity, counted | Membership as the primitive — the same correction B52 forces |

---

## Tier 3 — the remaining 70 cards

B1–B4, B7–B12, B14–B16, B18, B21–B36, B38–B45, B47, B48, B50, B51, B53–B55,
B57–B59, B61–B64, B66, B68, B69, B72–B75, B77–B80, B82–B93.

These are physics- and spectral-theory-facing (curvature bounds, entropy
production, band structure, holonomy, refraction, horizons). None has a
demonstrated bearing on the corridor programme **as of now**. They are not
dismissed — the instruction was that all of them can help at some point, and
the Tier 1 result argues for that: B52 and B70 would have read as generic
methodology a day ago and turned out to name two concrete errors exactly.

---

## What the sweep is actually worth

Not a search speed-up. The Atlas is a **checklist of failure modes**, and on
this session's record it is a good one: three of the four Tier-1 cards
correspond to errors made and then caught by an external audit rather than by
me. Read before the fact, B52 stops the wells claim, B65/B70 stop the
DONOR_EXIT conflation, and B20 stops the budget-escalation lane earlier than
it was stopped.

The operational recommendation is narrow and testable: before promoting any
classification, check it against B52 (is this a size threshold or a
membership test?), and before promoting any detector, check it against B70
(is this one question or two wearing one word?).
