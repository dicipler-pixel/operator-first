# Checkpoint 1 — a complete plateau and a new fixed-roof result

9 September 2026. These are newly executed computations from the verified five-triple checkpoint, not a replay of the old radius-three search.

## Complete five-triple connected component

Exhaustive traversal constrained to at most five independent triples closes after **40 embedded pairs** (exact sorted face tuples, quotienting layer interchange only). All 40 still have exactly the original five bad triples. The traversal examines **2,828 legal layer-specific diagonal-flip transitions**: 164 stay at five; all others have 6–14 triples. The least exit score is six.

A second implementation reconstructs moves from raw face incidence, enumerates all 969 triples from scratch, checks all spherical complexes and the component's reachability/closure, and independently reproduces those numbers. Removing a state from the certificate is rejected.

**Finite conclusion:** every legal diagonal-flip path from this component to fewer than five independent triples passes through at least six. This is stronger than the earlier radius-three statement but remains local to this component. It is not a lower bound for all triangulation pairs or a proof of Earth–Moon nonexistence. Relative vertex permutations are different moves and are not covered by this flip barrier.

The ceiling-six traversal was separately stopped at its declared 30,000-state limit: 23,691 processed, 6,309 frontier states and 1,759,314 transitions. Minimum observed remained five. Its status is TRUNCATED_UNKNOWN, not a complete-component result.

## Larger moves actually tried

All 342 relative single-vertex transpositions (171 in either layer) at the old checkpoint were verified planar by relabeling the faces. None improves five. These are legal graph-changing moves, not just drawing changes, but not diagonal flips.

A C++ implementation now runs single-flip, multi-flip, hybrid relative-permutation, and persistent-triple-weighted searches. Every retained layer still has 51 edges and 34 faces. Proposals can temporarily raise the score and overlap; every actual best is stored with a replayable move sequence.

Pilot hybrid run seed90309, one million proposals: **five independent triples at exactly102 union edges and zero overlap**. This improves the previous fixed-102 best of six but does not lower the overall five-triple record or establish ten-chromaticity. Its complete33,918-move path was independently replayed from the original faces, and the final spherical complexes and all triple counts rechecked. Exact coloring is still to be added for this new saved graph; no winning graph is claimed.

Other pilots (single/macro: one million proposals each; weighted:100,000 selected moves) retained best five at101edges. A finite64-run continuation batch is running with16seeds for each of the four modes. Attempt counts, move evaluations, accepted moves and final checks will be separated. No new Lean certification is claimed.
