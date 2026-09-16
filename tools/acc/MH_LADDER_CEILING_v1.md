# Where the corridor-ladder method runs out

Measured per-cap component growth on the two fully-laddered roots.

## Growth factor

| R6 | | R7 | |
|---|---|---|---|
| 21→22 | ×3.91 | 23→24 | ×3.90 |
| 22→23 | **×11.85** | 24→25 | **×13.03** |
| 23→24 | ×4.13 | 25→26 | ×4.27 |
| 24→25 | ×4.24 | 26→27 | ×4.50 |
| 25→26 | ×3.92 | 27→28 | ×4.12 |
| 26→27 | ×3.68 | 28→29 | ×3.85 |
| 27→28 | **×3.55** | 29→30 | **×3.71** |

Two features, both consistent across the roots:

- a single **spike** at the third rung, ×11.9 and ×13.0, where the component
  jumps two orders of magnitude in one cap — a structural transition early in
  the ladder, not a gradual opening;
- a **slowly declining trailing factor**, 4.24 → 3.92 → 3.68 → 3.55 on R6 and
  4.50 → 4.12 → 3.85 → 3.71 on R7. Growth is a little sub-geometric, so the
  projections below are mildly pessimistic.

## Projection and the memory wall

The engine holds ~45 bytes per state (40-byte packed state, 4-byte parent,
1-byte move) plus a power-of-two open-addressed index table at 4 bytes per
slot, sized to at least twice the state count.

| root | next cap | projected states | memory | reachable at 15 GB |
|---|---|---|---|---|
| R6 | 29 | ~226M | ~11.5 GB | **yes, barely** |
| R6 | 30 | ~757M | ~39.7 GB | no |
| R6 | 31 | ~2,454M | ~134.8 GB | no |
| R7 | 31 | ~369M | ~19.5 GB | **no** |
| R7 | 32 | ~1,288M | ~70.0 GB | no |
| R7 | 33 | ~4,365M | ~247.0 GB | no |

Both projections are confirmed against runs already made: R6 at cap 29 with
**200,000,000** forward states returned BUDGET (depth 47, no path ≤ 54),
which is exactly what a ~226M component predicts. R7 at cap 31 under the
same 200M allocation cannot close either, needing ~369M.

## Consequence

**The ladder method is at its ceiling on this hardware.** R6 may take one
further cap with a squeeze to ~250M states, which would move its wall to
total length ≥ 30. R7 cannot advance at all. Past that the limit is memory,
not budget or patience, and every additional cap costs another ×3.6.

Further progress on these two roots therefore needs a different method, not
a larger allocation. The lower-n roots are the opposite case: n=8, 9 and 10
stopped at their first BUDGET under a 25M sweep allocation while their next
caps project to only ~34M, ~45M and ~59M, so those walls are floors that
ordinary budget will lift.
