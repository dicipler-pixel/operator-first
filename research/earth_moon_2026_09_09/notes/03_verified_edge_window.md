# Checkpoint 3 — verified finite exclusion: the endpoint window is now 100–102

9 September 2026. This is a computationally certified necessary-condition result for the specific 19-vertex alpha(G)<=2 biplanar route. It is not a construction, a claim about all ten-chromatic graphs, or a new Lean theorem. No historical priority is asserted without a more complete literature comparison.

## New statement

If G is a simple biplanar graph on 19 vertices with no independent triple, then

    100 <= |E(G)| <= 102.

Consequently any completed pair of triangulations representing a successful endpoint has at most **two shared edges**, not six. Minimum degree>=10 and an induced C5 in H=complement(G) remain necessary. These are endpoint conditions; unrestricted discovery paths may temporarily violate the edge window.

## Written reduction to the finite census

H is triangle-free. It has no independent nine-set because such a set would give K9 in G, and K9 is nonbiplanar. Its neighborhoods are independent, hence degree_H<=8. H cannot be bipartite, since one bipartition part on 19 vertices would contain ten vertices. A shortest odd cycle has length g>=5; every outside vertex has at most two neighbors on it, since three cyclic gaps include an odd gap producing a shorter odd cycle. Therefore

    2e(H) <= 2g+2(19-g)+8(19-g) = 38+8(19-g).

Euler gives e(G)<=102, hence e(H)>=69. If g>=7 the preceding bound gives e(H)<=67, impossible. Thus there is an induced C5.

Fix this five-cycle. Let D_C be the sum, over the fourteen outside vertices, of 2 minus their number of neighbors on the cycle, and D_out the sum of 8 minus their degree in H. Both are nonnegative and

    D_C + D_out = 150 - 2e(H).

To exclude e(H)>=72 it suffices to consider D_C<=6. Every nonexceptional vertex has one of the five possible nonadjacent neighbor-pairs on C5. Put it into the class containing the cycle vertex with that neighbor-pair. The five nonempty class sizes are a_i. Let b_i count exceptional vertices with only cycle neighbor i, and z count exceptions with no cycle neighbors. All possible profiles satisfy

    sum(a_i)+sum(b_i)+z=19,
    2z+sum(b_i)<=6,
    a_(i-1)+a_(i+1)+b_i<=8,   a_i>=1, b_i,z>=0.

Common cycle neighbors forbid edges between the corresponding vertices of H. Between regular classes only consecutive classes can have H edges. Exception edges are otherwise variable. No assumption is made that the whole complement is a C5 blow-up. Rotations/reflections of the chosen cycle and permutations within each identical-neighborhood class preserve this family.

## Exact finite coverage and proof checks

The e(H)>=72 census has **8,044 profile orbits** under the ten dihedral symmetries. A separate auditor, which does not import either census producer, independently enumerates profiles using bounded degree capacities, constructs the ten automorphisms from all 120 permutations, reconstructs all edge-variable meanings and every final CNF, and checks every added graph-theoretic cut. All 8,044 cases are UNSAT, with independently checked reverse-unit-propagation proofs.

Audit totals:

- 8,044 independently matched profile orbits and final formulas.
- 4,799,908 verified RUP additions; 5,202,127 deletion lines safely ignored.
- Four cases contradicted by root unit propagation.
- 327 checked independent-nine cuts and 13 checked triangle-free subgraph density cuts.
- 337 SAT assignments rejected by those necessary conditions.
- Four corruption/malformed-certificate controls rejected.
- 3,586 separate exhaustive small cardinality-encoding checks passed.

An independent-nine cut requires at least one H edge among that nine-set. A density cut supplies a simple triangle-free subgraph W of G with e(W)>4|V(W)|-8, which cannot be the union of two planar restrictions. Each cut is checked from its actual edge/vertex set, including that no forced H edge is silently omitted from its clause. The final formula, rather than an implicit solver state, is the input to the Boolean proof checker.

The earlier threshold censuses are nested corroborating results, not disjoint new graph counts: e(H)>=74 had146 cases; e(H)>=73 had1,684. Their independent audits also pass. The strongest e(H)>=72 exclusion implies e(H)<=71 and therefore e(G)>=171-71=100.

Trust boundary: the mathematical C5 reduction, standard nonbiplanarity of K9 and triangle-free planar Euler bound, Python semantic checker, PySAT sequential cardinality compiler (separately tested), and the independent C++ RUP checker. This is not a full Lean formalization or an independently replayed Lean kernel result.

## What happens at the next edge level

The e(H)>=71 extension does NOT close: case3 already supplies a triangle-free 71-edge complement with maximum degree8 and no independent nine-set. Its G has100edges and survives the current C5-based density cuts. A more general bounded SAT probe found no violating triangle-free subgraph at subset sizes14–19; those negative probe answers do not yet have independently checked proof logs. The actual thickness-two partition test is running. The necessary-condition survivor is not being called biplanar or a winning graph.

## Literature connection

Banak, Ekim and Taskin, *Constructing extremal triangle-free graphs using integer programming*, arXiv:2304.01729, Table2, already compute74 as the maximum for triangle-free graphs with maximum degree8 and matching number9. For19vertices the matching bound is automatic. Their model does not require no independent nine-set or biplanarity of the complement. This related published extremal result is credited, not rebranded; our additional conditions and finite certificates are distinguished explicitly.

The code, case lists, semantic cuts and Boolean proof logs are being preserved with the full continuation package and the dedicated GitHub workstream. No winning graph or global Earth–Moon nonexistence is claimed.
