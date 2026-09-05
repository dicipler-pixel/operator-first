# Earth-Moon / arithmetic Kakeya / FCS extension

This draft extends PR #3 without modifying its branch, PR #2, or main.
Verification status is determined by the exact extension CI run, not this text.

- `EarthMoon`: explicit C7[K4] adjacency, triangle-freeness, edge-list and edge-set counts, a proper 10-coloring, and a contradiction from assumed planar-layer Euler bounds. No full planarity formalization, no formal chromatic lower bound, and no Epoch solution.
- `RestrictionBridge`: finite-set edge-cover counting and cancellation of antisymmetric exchanges internal to a chosen subset. The restriction of the total exchange to a subset equals its boundary exchange. This is a precise structural connection, not a proof that the particular arithmetic Kakeya rank module satisfies the required identifications.
- `KakeyaExtension`: interprets the original proved integer power identity as an exact rational density identity with positive denominators; adds conditional full-score exclusion and genuine eventual growth for positive initial density. It does not prove score attainability, a rank floor, or a universal monotonicity of full scores.
- `FCSMoments`: positive normalized four-point laws with equal first two moments and different endpoint weights; third central moment 6t; an injectivity theorem showing that moments of orders 0 through 3 determine a four-point law. Independent-mode realizability and physical Gaussian-tail approximation remain separate.

PR #3 already checks both original supplied FCS/AK files and includes weak/strict granularity corrections (thresholds 40/43). Those are not claimed as new results here. No complete arithmetic Kakeya manuscript was in this turn's attachments; the supplied Lean file explicitly excludes the subset-rank theorem. A full connection requires the actual module/generator definitions and a proof that restriction kills exactly the internal terms while leaving the claimed rank budget.

Nothing here identifies graph biplanarity with spacetime geometry or supplies a cosmological constant. The common mechanism is restriction followed by cancellation or capacity counting, with a separately justified map needed for each application.

Imported Lean/mathlib libraries remain trusted. Every extension theorem is directly elaborated with an axiom report and independently rechecked with leanchecker. False controls are required to fail mathematically. Until that execution succeeds, these are proof candidates, not certified additions.
