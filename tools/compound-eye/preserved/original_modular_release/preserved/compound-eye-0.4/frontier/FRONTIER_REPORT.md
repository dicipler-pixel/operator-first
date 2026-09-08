# Compound Eye — two problems, checked from several sides

Jeromie N. Beasley · Operator-First Atlas · Development edition 0.3 · 7 September 2026

The many-eye idea now has two exact mathematical applications. One follows a graph through edge changes, checking how its coloring and planar-layer requirements interact. The other follows arithmetic information through a labelled tower, retaining an explicit reason for every forced vertex and every final obstruction.

The useful improvement is that the views carry different logical jobs. A necessary condition can reject an object. A construction can certify a property. A counterexample can invalidate a proposed shortcut. Agreement between several necessary conditions does not turn them into a sufficient condition.

This edition closes an edge-deletion route for the supplied Earth–Moon candidate, corrects an unsafe Kakeya search restriction, and certifies a complete finite Kakeya search region. It does not solve either full Epoch target. The original sixteen-view quantum model, circuit examples, projector examples and calculation interface remain available.

## The two actual targets

Epoch's Earth–Moon task requires a graph partitioned into two planar layers, together with a proper coloring and a matching chromatic lower bound of 10, 11 or 12. Our example below has chromatic number 10 but needs three planar layers. [Epoch's Earth–Moon specification](https://epoch.ai/frontiermath/open-problems/earth-moon), consulted 7 September 2026.

The arithmetic Kakeya target requires a valid constructible tower and complete forcing with score at most 1.675, exactly 67/40. Our implementation uses the page's **verifiable setup**, including its permission to force a nonzero multiple of the forbidden direction. The private Epoch verifier was not run. [Epoch's arithmetic Kakeya specification](https://epoch.ai/frontiermath/open-problems/arithmetic-kakeya), consulted 7 September 2026.

| Target | What this run establishes | Full target status |
|---|---|---|
| Earth–Moon | The supplied C₇[K₄] has chromatic number 10 and thickness 3. Every biplanar subgraph of it is nine-colorable. | No qualifying construction. |
| Arithmetic Kakeya | Both supplied calibration examples force exactly; a false seeding rule is refuted; all 11,480 configurations in one fixed search region are excluded with exact evidence. | No new qualifying forcing pair. |

## What the eyes now do

| Eye | Concrete operation | Meaning of its output |
|---|---|---|
| Admission | Validate tower coordinates, labels, support, costs and graph incidences. | Invalid input never receives a mathematical score certificate. |
| Cost | Count expanded edges and generators; compare rational scores by integer arithmetic. | A low score is a numerical requirement, not complete forcing. |
| Cut | Examine triangle-free graph density or arithmetic cut directions. | A witnessed violation is an obstruction. Passing is inconclusive. |
| Transport | Form permitted edge relations and follow their support. | A relation can bring information from a remote vertex. |
| Forcing | Solve exact support equations and clear denominators. | An integer combination certifies each newly known vertex. |
| Obstruction | Produce an exact dual identity for every stalled vertex. | No next forcing step exists at the reported terminal set. |
| Geometry and coloring | Check planar rotation systems and explicit proper colorings. | Planarity and a chromatic upper bound are established separately. |
| Coverage | Record every enumerated configuration and its rejection evidence. | Exhaustion applies only to the stated finite region. |

These are callable calculations over shared objects, not eight independent votes. For an AI, the important output is a structured certificate, its input hash, the exact claim it supports and its scope. The tool does not install a persistent assistant or run indefinitely in the background.

## Earth–Moon: the original obstruction survives

Write G = Cₙ[Kᵣ]: replace each cycle vertex by a clique of size r and connect all pairs in adjacent cliques. Call the inter-clique edges the joins. For n ≥ 4 their subgraph J is triangle-free.

**Triangle-free subgraph bound.** If a simple graph G on N ≥ 3 vertices has two planar edge layers, every triangle-free subgraph H of G satisfies

\[
|E(H)|\le 4N-8.
\]

Indeed, restrict the two planar layers to H. Each is a simple triangle-free planar graph on the same N vertices and has at most 2N−4 edges. Adding the inequalities gives the bound. Isolated vertices do not invalidate it. For a connected tree the inequality is immediate; for other connected triangle-free plane graphs the face bound gives it, and disconnected components can be connected by bridges without creating triangles.

For G = C₇[K₄],

\[
N=28,\qquad |E(G)|=154,\qquad |E(J)|=112.
\]

The whole-graph Euler test allows 6N−12 = 156 edges and therefore misses the obstruction. The join subgraph is allowed only 4N−8 = 104. Its excess of eight proves that G is not biplanar.

More generally, for n ≥ 4 and r ≥ 4,

\[
|E(J)|-(4rn-8)=r^2n-4rn+8=rn(r-4)+8>0.
\]

Thus none of those inflated cycles is biplanar. This confirms the central obstruction in the supplied Earth–Moon paper.

### Corrections needed in that paper

The independent-set formula is α(Cₙ[Kᵣ]) = floor(n/2), independent of r. An independent set contains at most one vertex from a clique, and the occupied cliques must be nonadjacent on the base cycle. For C₇[K₄], α = 3, so any coloring needs at least ceil(28/3) = 10 colors. The delivered proper ten-coloring proves equality.

The triangle-free lemma needs N ≥ 3. Also, the whole-graph Euler margin for Cₙ[K₄] is 2n−12: the whole-graph count already rejects n = 4 and 5, is exactly saturated at n = 6, and passes for n ≥ 7. A claim that the whole-graph count never detects this family is too broad. None of these corrections weakens the join obstruction.

### An explicit three-layer upper bound

The package supplies three disjoint planar edge layers for C₇[K₄], with 62, 48 and 44 edges. Each layer includes a cyclic neighbor order at every vertex. A separate combinatorial check traverses its face orbits and verifies Euler characteristic 2 in each connected component. Combined with the obstruction, this gives thickness exactly 3.

There is also a transparent family construction. Put aᵢ,bᵢ in fibre i of Cₙ[K₂], with indices modulo n. For n ≥ 5 partition its edges into three forests:

1. The a-rail and b-rail cycles, with a₀a₁ and b₁b₂ removed.
2. All cross edges aᵢbᵢ₊₁ and bᵢaᵢ₊₁, with a₂b₃ and a₃b₄ removed.
3. All vertical edges aᵢbᵢ and the four removed edges.

The first part is two paths. For odd n the cross edges form one 2n-cycle; for even n they form two n-cycles and the removed edges lie in different cycles. Thus the second part is a forest. Contracting the vertical edges in the third part leaves the path 0−1−2−3−4, so it too is a forest.

Replace every vertex in these forests by two adjacent clones. A tree's closed two-clone blowup is planar: each tree edge contributes a K₄, and removing a leaf gives an induction by gluing another K₄ along the parent's clone edge. Assign each internal clone edge only to the first layer; the other layers are subgraphs of their corresponding planar blowups. The result partitions Cₙ[K₄] into three planar graphs.

For n = 4, a bounded witness search supplies a separately checked three-forest partition. Exact layer certificates are included for every n from 4 through 12. The formula above proves the upper bound for all n ≥ 5; finite tests alone are not being used to infer it.

### A stronger consequence: deleting edges cannot repair this host

**Proposition. Every biplanar subgraph of C₇[K₄] is nine-colorable.**

A biplanar subgraph, padded with isolated vertices if needed, must omit at least eight of the 112 join edges. It therefore lies in G−e for some join edge e. It suffices to nine-color G−e for each such edge.

All join edges are equivalent by rotation of the seven fibres and permutations within each fibre. Take the deleted edge between slot 0 in fibre 6 and slot 0 in fibre 0. Give one color to slot 0 in fibres 0, 2, 4 and 6. The only formerly adjacent pair in this class is the deleted edge.

For each j modulo 7 let Iⱼ = {j, j+2, j+4}. These are independent triples of fibres. Use eight additional colors, on triples Iⱼ with multiplicities

\[
(1,2,1,1,1,1,1).
\]

The resulting demands per fibre are (3,4,3,4,3,4,3), exactly the uncolored vertices. Assign different vertices within each fibre to these colors. Every color class is independent. This constructs a proper nine-coloring of the entire one-edge deletion, and restriction colors any of its subgraphs.

The program materializes and checks the transported coloring for **all 112 join-edge deletions**. This proves the proposition and closes the edge-deletion repair route for this particular host. It says nothing comparable about arbitrary ten-chromatic graphs. No historical-priority claim is made for this consequence.

### Following the closing edges

An open seven-fibre path has 96 join edges. Restoring k of its 16 closing joins produces 96+k. The global triangle-free count first rejects at k = 9, when the count reaches 105. Passing at k ≤ 8 does not certify biplanarity.

The supplied account's solver slowdown around four restored edges is not this mathematical threshold. Runtime behavior and an obstruction are different readouts. Until the last join is restored, the graph is a subgraph of a one-join deletion and is therefore nine-colorable. At all 16 joins restored it is ten-chromatic, but nonbiplanar. This is a concrete example of following two properties whose desirable regions fail to overlap in the proposed family.

## Arithmetic Kakeya: information can arrive from elsewhere

Represent all initial single-vertex generators and all expanded edge differences as integer rows b₁,…,bₛ of length 2N. Let K be the currently known set, initially T. To force an unknown vertex e, we need an integer combination w of these rows that vanishes outside K ∪ {e} and has w(e) = (a,−a), with a ≠ 0.

No condition requires two initial generators to be located at e. Edge differences allow a remote generator to be transported and combined there.

### The local seeding lemma is false

Consider two vertices, an edge labelled x = (1,0), and generators y = (0,1) at vertex 1 and x at vertex 2. In coordinates grouped by vertex, the three available rows are

\[
E=(1,0,-1,0),\quad R_1=(0,1,0,0),\quad R_2=(0,0,1,0).
\]

Then

\[
E+R_2-R_1=(1,-1,0,0).
\]

Vertex 1 is forced although it has only one initial generator. This small example need not force both vertices to refute a claim about the first step.

More decisively, both complete calibration constructions transcribed in the supplied appendix refute the claimed local requirement:

| Calibration | Exact score | First forced vertex in the checked order | Initial generators at that vertex |
|---|---|---|---|
| Figure 2, six vertices | 11/6 | (2,3) | 0 |
| Figure 3, four vertices | 7/4 | (2,1) | 0 |

Every step has an independently checked integer witness. These are recovered controls, not new record constructions.

Consequently, searches that require an initial pair of independent generators at one vertex are searching a restricted class. Empty results from that class cannot close a larger region that includes distributed generators. The large seeded record hunt in the supplied paper must be relabelled accordingly; its millions of trials were not reproduced or certified here as full coverage.

### A valid replacement: subset cut rank

For any nonempty U disjoint from the initial known set, collect all initial generator labels inside U and all edge labels crossing from U to its complement. If complete forcing occurs, these labels must span two dimensions over Q.

To prove this, consider the first vertex of U forced in a successful order. Sum its witness over U. Internal edge differences cancel; the remaining sum lies in the span of the collected labels and equals a nonzero multiple of (1,−1). A rank-zero span cannot contain it. A rank-one span generated by admissible labels cannot contain it either, because every nonzero allowed label has nonzero coordinate sum. Therefore the rank must be two.

This is a necessary condition. It is not a forcing algorithm by itself. Removing the last generator from the six-vertex calibration gives score 5/3 and leaves **all 63 nonempty subset cuts at rank two**, yet no vertex can be forced. The package contains exact terminal dual certificates for all six vertices. This is a concrete counterexample to upgrading cut feasibility to complete forcing.

### Why the new forcing calculation is exact

Write w = Σcⱼbⱼ. Form a matrix C whose rows impose every forbidden support coordinate and the condition w₁(e)+w₂(e)=0. Let t(c)=w₁(e). Forcing is equivalent to

\[
Cc=0,\qquad t(c)\ne0.
\]

Over Q, scale a nonzero solution so t(c)=1. Solve that rational linear system, then multiply all coefficients by a common denominator D. The resulting integer witness has value (D,−D) at e. Conversely, any valid integer witness can be scaled rationally to t(c)=1. Thus rational elimination is an exact existence test for this particular rule; there is no unit-coefficient divisibility requirement to lose.

If forcing is impossible, t lies in the rational row space of C. The producer returns integers λᵢ and D ≠ 0 satisfying

\[
D\,t=\sum_i\lambda_i C_i.
\]

For any c with Cc=0, this identity forces t(c)=0. A separate checker verifies the identity using integer multiplication and addition only. It does not import SymPy, NumPy, the source verifier or the certificate producer.

Forcing is monotone in the known set. At a terminal set with a valid obstruction for every remaining vertex, there is no legal first step outside that set, so no alternative ordering can complete the candidate. These dual certificates justify a negative result, rather than merely reporting that one search order failed.

### Input admission and the integer-kernel claim

The supplied verifier accepts a generator that is not in its declared X. For example, a one-vertex input with X = {(0,0),(1,0)} and the undeclared generator (1,−1) is reported as complete with apparent score 1. The generator is forbidden and the input is invalid. This is a verifier admission defect, not a construction proving AK(1).

The new producer and independent checker validate the declared labels, entire prefix domains, dimensions, distinct initial known vertices, single-vertex nonzero generator support and positive score denominator. Duplicate generators retain their cost because R is represented as a list. Omitted level entries represent zero-labelled edges. The implementation deliberately limits inputs to 128 vertices, with full subset enumeration limited to 16.

There is a narrower issue in the source's `kernel_of_functional`: its returned rows need not form the entire integer kernel claimed by its description. For the identity basis and functional (2,3,5), the valid kernel vector (−4,1,1) is absent from their integer span. Their rational span can still be correct. Because the forcing rule allows any nonzero a, that basis overclaim by itself does **not** invalidate the source's Boolean forcing decisions. The new integer certificates avoid depending on that overclaim.

The arithmetic stress control uses (M,M+1) and (M+1,M+2) for M=10³⁰. Their determinant is exactly −1; conversion to ordinary floating-point numbers collapses their numerical rank to one. Exact arithmetic preserves the distinction and yields a checked witness.

## A complete, certified finite search

The new search holds the six-vertex figure-2 edge labelling fixed, uses dimensions (2,3), starts with T empty and allows these seven primitive directions:

\[
(-1,2),\ (0,1),\ (1,0),\ (1,1),\ (1,2),\ (2,-1),\ (2,1).
\]

There are 42 vertex–direction placements. All sets of three distinct placements are enumerated, giving binomial(42,3) = **11,480** configurations. Each has m = 7, r = 3, N = 6 and score 5/3, so complete forcing would meet the numerical target. No local seeding restriction is used.

| Stage | Recorded result |
|---|---:|
| Configurations enumerated without omissions | 11,480 |
| Rejected by exact subset cut witnesses | 7,360 |
| Remaining configurations independently certified | 4,120 |
| Integer forcing steps checked across those certificates | 1,780 |
| Integer terminal obstruction identities checked | 22,940 |
| Complete forcing configurations | 0 |

Of the 11,480 sets, 6,860 place their three generators at three distinct vertices. The old local-seed restriction would discard these placements. The 4,620 remaining unique sets are not the same as the source's 5,040 seeded loop iterations, because the latter repeat some sets.

`fixed_ladder_search_trace.json` records the entire ordered enumeration. `fixed_ladder_certificates.jsonl.gz` holds the 4,120 full forcing-and-stall certificates. `fixed_ladder_certificate_audit.json` records complete enumeration checks, cut checks and independent integer verification. Cut-rejected cases carry their witnessing subset in the enumeration trace.

**Scope:** this excludes the stated generator choices for one fixed edge labelling. It does not exhaust other rail labellings, the reversed tower orientation, other starting sets, larger towers or a larger direction pool. It does not recertify the old paper's full claimed search region.

## Additional corrections and surviving methods

**Unimodular symmetry.** For row-vector action, the full family with (1,−1)M = σ(1,−1) is

\[
M=\begin{pmatrix}a&\lambda-a\\a-\sigma&\lambda-a+\sigma\end{pmatrix},
\qquad a\in\mathbb Z,\quad\sigma,\lambda\in\{-1,1\}.
\]

Its determinant is σλ. Conversely, the difference between its rows fixes σ, and unimodularity forces their common row sum to be λ = ±1. The displayed family in the source omitted a sign branch; −I is a simple missing example. Twenty maps, including that branch, were tested on the complete 7/4 calibration. A unimodular normalization need not preserve a finite coordinate-height cutoff, so it cannot silently justify coverage of every unnormalized height-bounded input.

**Generator transport.** If an edge from u to v has label x, the module contains x·u − x·v. Moving an initial generator x·u to x·v therefore preserves the generated module and its cost. This is a useful admissible move: it changes local placement without changing forcing. The package checks the corresponding move in the six-vertex calibration.

**Granularity.** For positive integers q < 40, p/q ≤ 67/40 implies p/q ≤ 5/3. If the latter failed, the positive integer 3p−5q would satisfy

\[
1\le3p-5q\le q/40<1,
\]

a contradiction. At q=40 the bound is sharp: 67/40 is larger than 5/3. Equality with 5/3 is available only when 3 divides q; it is a uniform upper bound, not the exact maximum for every fixed denominator.

**Products.** The supplied tower edge-count identity and its additive edge-density law survive. For the square of the six-vertex, seven-edge tower, N=36 and m=84, giving edge density 7/3. A lower bound coming from edge density does not, on its own, prove a universal statement that products can never improve an optimized forcing score over all R and T. That stronger inference needs a separate argument.

**Lean scope.** The supplied file was inspected, but no Lean compiler is installed here. Its `below_floor_excluded` statement assumes and returns the same inequality; it is not a formal proof of an arithmetic Kakeya impossibility theorem. Its product lemmas concern the defined counts and densities. No new Lean theorem is claimed in this edition.

## Verification and the supplied bridge packages

The new target suite passed **21 named checks**, including 240 deterministic small cases with arbitrary initial known sets and distributed generators. All 240 agreed between the source existence engine and the new producer, and every new certificate passed the independent integer checker. Twelve malformed inputs were rejected, and altered forcing, obstruction and score certificates were rejected. These are finite software checks, alongside the explicit mathematical arguments above.

The supplied small arithmetic scripts were rerun after providing the verifier under the import name they expect. `AK-SLOW-01` reported best score 2 in its own sampled/enumerated classes, with 3, 95, 2,928 and 37,609 trials for shapes [1], [2], [3] and [2,2]. Its cut test reported no violations on its two positive controls and rejected its rank-one negative control. These narrow reruns do not establish a global minimum.

Both supplied bridge archives were also rerun. `COMPLETE-COMPLEX-BRIDGE-01` passed its declared finite gauge checks, 36 group-pair retraction checks and spectral/probe controls. Its large balanced-lift entries explicitly did not use exhaustive gauge enumeration. `SMITH-BOUNDARY-01` passed five zero symbolic residuals, 60 matrix cases and 80 boundary-projector cases, including its negative controls. Floating residuals in those packages remain floating residuals. These bridge checks are relevant background for the instrument's transport and boundary views; they do not certify either Epoch construction.

All eight uploads are preserved byte-for-byte in `originals/`, with hashes in `input_manifest.json`. Corrections are documented here and implemented in the new adapters; the original papers have not been silently rewritten. Rerun logs are in `reference_runs/`.

## Run it without GitHub

Open the delivered `compound_eye.html` directly for the viewer. It embeds its data and works without a remote script or Python service. The exact calculations run locally from the extracted ZIP:

```bash
python -m pip install -r requirements.txt
python frontier_eye.py ak frontier/examples/kt_7_4.json
python frontier_eye.py check-ak frontier/certificates/kt_7_4.json
python frontier_eye.py earth frontier/examples/earth_moon_c7k4.json
python frontier/verify_frontier.py
python frontier/search_fixed_ladder.py
python frontier/certify_search_log.py
```

The last command regenerates the complete certificate audit; its delivered run took about 47 seconds on this machine. Runtime on another machine may differ. Earlier commands print JSON or regenerate their documented evidence. The full exact checker can also run by itself using only Python's standard library:

```bash
python frontier/check_ak_certificate.py frontier/certificates/kt_7_4.json
```

`frontier_eye.py` accepts `-` in place of a filename to read standard input. Exit status 0 means a valid analysis completed, including a candidate rejection; inspect the result's completion and target fields. Invalid input or certificate returns status 2. The JSON examples specify the complete tower or graph and require no expression evaluation or external repository.

Use Python 3.10 or later. This run used Python 3.12.13, NumPy 2.3.5, SymPy 1.14.0 and NetworkX 3.5. `requirements.txt` records compatible dependency ranges; exact environment versions are included in the manifest. The original numerical API remains documented in `LAB_GUIDE.md`.

## Unfinished checks and open work

- The supplied Lean file has not been recompiled here; the new forcing, cut and coloring arguments are not newly Lean-formalized.
- Epoch's official verifiers have not been run. Local certificates are checked against the public conditions.
- The historical SAT planar-layer witnesses mentioned by the Earth–Moon account were not attached and could not be rechecked.
- Full browser layout has not been inspected in a real browser. Event logic is checked separately and its result is in `viewer_verification.json`.
- The old seeded millions-of-cases search is not certified as exhaustive. Other Kakeya edge labellings and larger search regions remain open.
- The Earth adapter checks incidence, density, supplied planar layers and proper colorings. It does not contain a general solver for chromatic lower bounds or arbitrary two-layer decompositions.
- Integration with the physical Offset determinant problem, general experimental tracking and a common formal calculus across every Atlas paper remain development work.

The practical next change of direction is specific. Earth–Moon needs a host beyond subgraphs of C₇[K₄]. Arithmetic Kakeya needs additional edge labellings or tower shapes, with distributed generators retained and exact certificates attached. The instrument now records enough information to pursue those moves without mistaking a promising score or a passed screen for a completed construction.
