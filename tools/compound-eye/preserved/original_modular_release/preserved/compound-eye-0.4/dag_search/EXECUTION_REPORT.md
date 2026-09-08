---
title: "Compound Eye now remembers the obstruction"
subtitle: "Implemented decision DAGs, measured proof savings, and new finite exclusions"
date: "Jeromie N. Beasley · Operator-First Atlas · Edition 0.4 · 7 September 2026"
lang: en
---

The proposed search machinery is now implemented. Compound Eye stores reusable obstructions with their assumptions, shares equivalent decision states, produces a finite coverage certificate, and checks that certificate independently. The new work is integrated into the existing command-line interface, and the original light, electrical, geometric, and frontier examples remain in the complete package.

The result is concrete: **470,232 distinct new arithmetic Kakeya configurations and 24,976 new Earth–Moon graphs are excluded within explicitly stated finite domains.** The Kakeya calculation closes 33 specified tower-and-pool cases at the target score across every admissible initial known set. Neither full Epoch problem is solved.

The performance result is also specific. Raw search time on our existing baseline is essentially unchanged. Producing and independently checking its complete mathematical evidence is about **35.9 times faster** with the new implementation in this measurement. This combines a new exact forcing implementation, shared states, reusable obstructions, and a more compact certificate; it is not an isolated speed claim about DAGs.

| Requested work | Delivered |
|---|---|
| Store reusable obstructions with precise assumptions | Context-bound integer separators, explicit nine-colorings, and triangle-free subgraph witnesses. |
| Share equivalent states in a decision DAG | Implemented for exact Kakeya relation spaces and Earth–Moon certificate compatibility. |
| Measure against the exhaustive baseline | Three timing repetitions per search mode, full outcome comparison, and freshly regenerated original certificates. |
| Search genuinely untested regions | Changed tower labels, another replication orientation, larger generator pools, every relevant initial set, and graphs with edges outside the old Earth–Moon host. |

**What the memory contains.** An arithmetic obstruction records the exact tower, ordered coordinates, allowed labels, initial known set, target direction, forcing rule, and a content hash. Its mathematical certificate consists of integer functionals. The stored family mask tells the search which generator options those functionals annihilate; the independent checker recomputes that mask.

A stored obstruction does not silently survive a changed problem. In the expanded-pool search, the earlier 1,471 baseline obstruction records were explicitly revalidated against the new context and option list. The record retains its parent certificate reference. Changing an edge label without revalidation is rejected.

The proof behind these records is short. Let $E$ be the fixed edge relations, and let $K$ be a proper set containing the initial known vertices. For each $e\notin K$, suppose $z_e$ vanishes on all coordinates in $K$, annihilates $E$, and satisfies

$$
z_e\cdot(1,-1)_e\ne0.
$$

If every selected generator also annihilates every $z_e$, forcing cannot leave $K$. The first proposed witness outside $K$ would pair to zero because it is a combination of permitted relations, but pair to a nonzero value because its new coordinate is $(a,-a)$ with $a\ne0$. This contradiction excludes every generator selection in the common kernel. The proof does not require the search to establish that every vertex of $K$ was reached.

**What states can be shared.** For a fixed tower, write

$$
M_R=\operatorname{span}_{\mathbb Q}(E\cup R).
$$

The decision state contains the next option, the remaining generator budget, and a canonical representation of $M_R/E$. Two routes merge only when these agree. At the six-vertex baseline, quotienting by the seven independent edge relations reduces twelve coordinates to five.

If two states have the same relation space and the same remaining choices, every common extension preserves that equality. Their possible forcing steps therefore agree. Denominators can be cleared because the public rule accepts a nonzero integer multiple of the target. This would not justify forgetting lattice index in a problem requiring a primitive unit witness.

Equal rank is insufficient. The tests include an intentionally false merge between equal-rank, unequal row spaces, and the independent checker rejects it. The implementation uses integer elimination; the checker independently reconstructs the quotient using rational Gauss–Jordan elimination with Python's `Fraction`.

These are fixed-budget decision states. We do not claim to have implemented every possible cross-budget cost-dominance optimization. No graph-isomorphism reduction or coordinate normalization is used to claim search coverage.

**What the benchmark actually says.** All modes use the same 11,480 three-generator choices in the original fixed tower. Every classification agrees with the stored exhaustive baseline. All 4,120 cases that pass the cut screen also reproduce their previous exact forcing closure.

| Calculation | Median raw run, seconds | Forcing calculations |
|---|---:|---:|
| Original search with cut screening | 0.743 | 4,120 |
| New integer engine with ordinary enumeration and cuts | 0.736 | 4,120 |
| DAG alone, including its proof production | 1.370 | 2,947 |
| DAG with cuts and learned obstructions, including proof production | 0.742 | 1,460 |

The DAG alone is slower here. Learned obstructions bring its raw time back to the original search time while retaining a proof graph. Forcing calls fall by **64.6%**, but this does not become a corresponding raw runtime gain because graph and certificate handling have costs.

For a comparison that includes evidence, the original producer freshly regenerated and checked 4,120 integer certificates: 1,780 forcing steps and 22,940 stall identities. This took 44.408 seconds beyond the original search. The new DAG's separate checker took approximately 0.516 seconds.

| Complete calculation and verification | Seconds |
|---|---:|
| Original search plus fresh individual certificates and checks | 45.151 |
| New search/proof graph plus independent DAG check | 1.259 |

The ratio is **35.9×** on this run. Shared context preparation and disk serialization are excluded from both reported pipelines. These figures compare the delivered algorithms and certificate formats, not just one isolated optimization. They are local measurements, not a guaranteed speedup on other problems or machines.

The baseline proof graph has 6,647 nodes, 1,919 reused visits, and 1,471 obstruction records. Its compressed certificate is 158,002 bytes. Every feasible include/exclude branch and every claimed merge is checked; a compressed graph is not being accepted merely because it has the expected final count.

**The new arithmetic Kakeya regions.** The target is a valid forcing construction with

$$
\frac{m+|R|}{n-|T|}\le\frac{67}{40}.
$$

We continue to use Epoch's public verifiable setup. The private verifier was not executed. [Epoch's arithmetic Kakeya specification](https://epoch.ai/frontiermath/open-problems/arithmetic-kakeya).

The completed work covers 230 newly declared fixed contexts, with 481,964 configuration checks. We remove both kinds of overlap when reporting progress: 11,480 configurations were in the old baseline, and another 252 occur in both nested singleton-$T$ generator pools. The resulting count is **470,232 distinct new labelled configurations**.

| New region | Exact scope |
|---|---|
| Changed labels | Each of the five nonzero level-table entries is changed individually to each of the other six height-two directions: 30 fixed towers. Changing the first-level entry changes three replicated edges together. |
| New orientation | A specified $(3,2)$ tower with its own replication pattern and labels. |
| Larger generator pool | The original fixed tower with all fifteen primitive height-three directions normalized by $a+b>0$; the old seven-direction pool is included and its overlap is counted. |
| Initial known sets | Empty $T$ and every singleton $T$ for all these cases and the original baseline tower. Larger $T$ is excluded by the score alone. |

The exact direction pools, table entries, coordinates, and per-region proofs are included as JSON. The result is not claimed to classify these cases up to every possible symmetry or projective change of coordinates. The seven-direction and fifteen-direction versions of the original tower remain distinct declared contexts, while shared generator selections are counted once in the progress total.

**Why every initial set is covered.** These cores all have $n=6$ and $m=7$. Empty $T$ permits at most three generators at the target score. A singleton $T$ permits at most one. If $|T|\ge2$, even zero generators cost at least

$$
\frac{7}{6-|T|}\ge\frac74>\frac{67}{40}.
$$

Therefore the empty and six singleton cases complete the initial-set analysis. An excluded exact generator budget also covers every smaller budget: delete duplicates from a hypothetical successful list, then pad it with distinct allowed generators. Adding generators cannot destroy forcing, and enough allowed options exist in every tested pool. The maximum qualifying budget is still respected.

This closes **33 specified tower-and-pool cases across all $R,T$ allowed by their target budget**. It does not close other towers, simultaneous changes to multiple level entries, or unrestricted slope pools. None of the tested configurations provides a new qualifying construction.

**Earth–Moon moves outside the old host.** The preceding result excluded every biplanar subgraph of the particular $C_7[K_4]$ host. This search adds edges absent from that host, so it is not another subgraph-deletion sweep.

Keep the old numbering: fibre $i$ contains vertices $4i,\ldots,4i+3$. Delete the eight joins connecting vertices 24 and 25 to vertices 0 through 3. Then add exactly two distinct edges chosen from the 224 edges absent from the original host. There are

$$
\binom{224}{2}=24,976
$$

graphs in this explicitly fixed family. Epoch requires a biplanar graph needing at least ten colors; either a nonbiplanarity certificate or a nine-coloring rejects a candidate. [Epoch's Earth–Moon specification](https://epoch.ai/frontiermath/open-problems/earth-moon).

| Certificate used | Graphs rejected |
|---|---:|
| A retained triangle-free subgraph exceeding $4N-8$ edges | 19,620 |
| An explicit proper nine-coloring, after the density rejections | 5,356 |
| Unresolved | 0 |

The density records include 120 triggering optional edges and an explicit witness for each. The checker verifies their edge support and triangle-freeness. The coloring memory starts with eight inherited colorings that remain valid on the new base graph. **Twenty additional coloring searches produce twenty reusable colorings**, covering the 1,189 cases left by the initial checks. All 28 colorings are checked edge by edge.

The Earth–Moon DAG shares states with the same remaining choices and the same surviving certified colorings. This preserves the rejection test; it does not assert that the underlying graphs have the same topology or planarity. A second, direct enumeration independently checks coverage of all 24,976 pairs without relying on DAG traversal.

**Verification and proof status.** The delivered bundle includes an independent checker for every proof graph, plus an aggregate checker that verifies the all-initial-set argument and removes overlapping generator-pool counts. The checks use exact integers and rational arithmetic.

- The two complete Katz–Tao calibrations survive the new engine.
- All 240 earlier test certificates, including nonempty initial known sets, agree with the new forcing closures.
- 120 independently computed row-space tests and 300 indexed obstruction queries pass.
- Eleven deliberately invalid Kakeya inputs or certificates are rejected, including false merging, stale assumptions, broken coverage, and forged family membership.
- Four invalid Earth–Moon proof controls are rejected.
- A complete positive DAG control carries an independently checked integer forcing certificate.

The general merge and obstruction arguments are written mathematical proofs supported by these exact finite checks. **Their Lean formalization is not completed.** No new SAT/SMS/QBF implementation or benchmark is claimed. Neither full Epoch problem is solved, and no official submission or GitHub publication was made.

**Use and reproduce.** The complete archive preserves the earlier tool and adds `dag_search/`. From the unpacked package directory, verify all delivered search proofs with:

```bash
python3 dag_search/check_all.py
```

That command needs only Python's standard library. To run or modify the searches, install the included dependencies and use the complete scripts:

```bash
python3 -m pip install -r requirements_reproducible.txt
python3 dag_search/run_searches.py benchmark --full-baseline-certificates
python3 dag_search/run_searches.py search
python3 dag_search/earth_families.py
python3 dag_search/verify_engine.py
```

The search runner reuses completed proof files only when their recorded hashes match. To force fresh enumeration, use `python3 dag_search/run_searches.py search --fresh`. The baseline benchmark creates the obstruction records needed by the larger-pool search.

The main interface now accepts `search-ak`, `check-dag`, and `check-earth-family`, alongside the earlier commands. A ready-made request is provided:

```bash
python3 frontier_eye.py search-ak dag_search/examples/search_baseline.json --output my_search.json
python3 frontier_eye.py check-dag my_search.json
```

All exact assumptions and resulting certificates travel with the output. The full HTML browser-layout check remains unavailable in this environment; mathematical checking and HTML structural validation are separate from that outstanding display check.
