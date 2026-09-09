# Checkpoint 2 — searches checked, structural census in progress

9 September 2026. This checkpoint separates completed computations from the remaining reduction/coverage audit.

## Planarity-preserving search outcomes

The 64-run batch completed: 16 seeds in each of single-flip, coordinated-flip, hybrid relative-permutation, and persistent-triple-weighted modes. The first three modes attempted 20 million proposals per seed (960 million total); weighted mode made one million selection steps per seed, each evaluating all legal flips. Those unlike work units must not be described as 976 million accepted flips.

A second search now replaces an entire triangulated disk by an allowed triangulation of the same polygon. Every proposal preserves the boundary, vertex set, faces and edge count of the planar layer; diagonals conflicting with the exterior are forbidden. Thirty-two runs of 200,000 patch proposals (thermal and weighted modes, 16 seeds each) were completed. Each selected polygon has at most ten vertices and all allowed tilings are evaluated. This is exact local evaluation inside a heuristic global search, not an exhaustive enumeration of all planar pairs.

All **96 saved endpoints** were independently replayed and checked, including their complete move sequences, final spherical complexes, a separate NetworkX planarity check and an explicit nine-coloring. They represent **45 distinct union-graph isomorphism classes**, not 96 inequivalent graphs. The overall minimum remains five independent triples. Several endpoints have five triples at102edges. That improves the old density-specific endpoint record, but these unrestricted trajectories were not constrained to remain at102 throughout.

## Exact fixed-layer repair

The lazy SAT implementation fixes one starting layer and encodes all second-layer edge choices within a declared symmetric-edge-difference radius. Nonplanar assignments produce checked K5/K3,3 subdivision cuts. The final fixed formula receives a DRUP proof, checked independently by the C++ RUP checker.

Both fixed-side radius-six and radius-eight, target-at-most-four-triple domains are UNSAT with independently checked RUP proofs. These radii count second-layer edge toggles after overlaps are removed, not diagonal flips. Zero-triple full-radius trials timed out and remain UNKNOWN. The eager order encoding also returned UNSAT at radius8, but its independent proof checks have not yet succeeded; it is not being substituted for the checked lazy result.

The first CI attempt stopped on its trivial UNSAT control because Glucose emits no proof steps for a root unit-propagation conflict. The checker has been repaired to independently test that root conflict, not to waive proof checking. Local controls now pass. A persistent Boost Boyer–Myrvold witness proposer has passed400 independent NetworkX/degree-suppression controls and is running larger fixed-layer domains; positive candidate embeddings still use NetworkX independently.

## A new five-cycle deficit representation

For a potential solution G and triangle-free H=complement(G), fix an induced C5. Every outside vertex has zero, one or two neighbors on it. Write

    D_C = sum_outside (2 - number of cycle neighbors),
    D_out = sum_outside (8 - degree_H),
    D_C + D_out = 150 - 2*edges(H).

Thus high-edge complements have very few exceptional vertices with fewer than two cycle neighbors. All nonexceptional vertices fall into five classes determined by their two cycle neighbors. Edges between those classes are restricted to the corresponding five-cycle; the exceptions remain fully variable. This is a bounded-defect decomposition, NOT a claim that every possible complement is a blow-up.

A SAT census has completed146 symmetry-reduced cases for edges(H)>=74, using triangle-freeness, degree<=8 and no independent9. All cases are UNSAT with RUP proofs. A further census completed1684 cases for edges(H)>=73 after adding only independently checkable triangle-free subgraph density cuts in G. Those cases are also UNSAT with RUP proofs. The full independent audit of case coverage, encoding, and cut reconstruction is in progress; do not announce the implied sharpened endpoint edge window from proof logs alone.

The edges(H)>=72 extension is running. Any surviving necessary-condition graph will still require an actual planar partition; it will not be called a winning graph. This complement census is a structural exclusion experiment alongside the planarity-preserving discovery searches, not a return to reporting unplaced edges as progress.

Relevant primary literature found during this step: Banak, Ekim and Taskin, arXiv:2304.01729, compute74 as the maximum for triangle-free graphs with maximum degree8 and matching number9. That does not include our no-independent9 or biplanarity conditions. Existing extremal results retain their attribution; no novelty claim is based just on an absent search hit.
