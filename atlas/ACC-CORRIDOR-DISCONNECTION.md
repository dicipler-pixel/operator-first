# A closed capped corridor is a disconnection, not a distance

Stable ID: `ACC-CORRIDOR-DISCONNECTION`

## Statement

If breadth-first search over presentations of total relator length at most the cap exhausts its frontier from the start without reaching the target, and the target lies inside the cap, then the start and the target lie in different connected components of the length-capped move graph. For every official AC row the target has length 2 and every cap is at least 9, so every exhausted corridor is such a disconnection.

## Assumptions

The move set and cancellation rule of the official verifier; the cap applied to total relator length; exhaustive enumeration of the start's component within the cap.

## Failure mode

Component size says nothing about whether the target is in that component, so a large corridor does not make a certificate likely. A cap proof excludes only paths inside the cap. The closed-set bottleneck method itself is not novel; the candidate contribution is the reproducible instance table on hard official rows.

## Evidence status

Exact finite computation with the official verifier: six pairwise-disjoint components and twelve closed corridors on the complete length-39 profile (15 September 2026). A target-outside Lean barrier theorem exists on PR #69 (draft); its numerical rows are release-gate pending.

## Verification scope

claude/confident-fermi-09rd02 commits b8ec58b5, 452ead28, ec60f90e, 0eedd1fb, e56bd253; tools/acc/ATLAS_TRANSFER_TRANSPORT_v1.md section 1; ACCSublevelBarrier.lean on proof/acc-sublevel-barriers-2026-09-19 at 471cdc6f84c6b1b9702ead754106de94a36c3264.

## Credit

Jeromie N. Beasley and the Mad Hatters ACC team; the reading was prompted by the Atlas card GRAPH-SUBGRAPH-CAPACITY.

## Next step

Commit the exact finite certificates for each closed corridor and pass the independent recheck gate on PR #69 before promoting any row.

## Sources

- [ATLAS_TRANSFER_TRANSPORT_v1.md (branch claude/confident-fermi-09rd02)](https://github.com/dicipler-pixel/operator-first/blob/claude/confident-fermi-09rd02/tools/acc/ATLAS_TRANSFER_TRANSPORT_v1.md)
- [PR #69 ACC proof track](https://github.com/dicipler-pixel/operator-first/pull/69)

## Paper applications

- [andrews-curtis](../papers/andrews-curtis/README.md)
