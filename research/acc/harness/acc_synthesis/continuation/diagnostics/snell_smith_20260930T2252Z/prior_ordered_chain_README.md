# Snell–Smith chains: ordered memory survives; search advantage remains unproved

Private Mad Hatters research. 2026-09-29. This completes the user's request to test whether the ideas fit together as a chain. It does not change the production beam, make a SAIR API call, or submit a path.

## The exact links

For positive numbers a,b, let z=b/a, tau=log(z), and Gamma=(z-1)/(z+1). Then Gamma=tanh(tau/2). Successive links obey

    Gamma_13 = (Gamma_12 + Gamma_23)/(1 + Gamma_12 Gamma_23).

The ratios multiply and their logarithms add. This scalar composition telescopes: 1→4→2 and 1→2 have the same final Gamma=1/3. Retaining only that result loses the intermediate excursion. The complete list of links retains more information than their product.

The supplied Slater implementation has another exact connection. For orbital exponents a,b and fixed effective principal number n*, its normalized overlap is

    C = [2 sqrt(ab)/(a+b)]^(2n*+1)
      = (1-Gamma^2)^(n*+1/2).

Thus its squared channel distance is 1-(1-Gamma^2)^(2n*+1), followed by the supplied orbital multiplicity sum. This was checked on 7,468 state transitions / 22,056 positive orbital links, both M/C filling rules, Z=1..86: maximum absolute discrepancy 3.18e-14. This algebra connects orbital-exponent ratios to the overlap. It does not identify exponent ratios with ionization-energy ratios.

For actual layered optics the chain is Snell-consistent angles → interface admittances/reflections → propagation phases → ordered transfer-matrix product → total reflection. Phase makes the order matter. In a synthetic lossless stack, air / A(n=1.38,d=95nm) / B(n=2.1,d=65nm) / substrate(n=1.5), wavelength550nm, reversing the two layers changes normal-incidence reflectance from4.72% to30.53%. At45° s-polarization it changes8.79% to44.91%. Independent reflection recursion and matrix multiplication agree within1.4e-16. These are model examples, not measured material results.

## A word-sensitive ACC chain

Use the classical Sanov generators

    X = [[1,2],[0,1]], Y = [[1,0],[2,1]],
    rho(a1 ... an) = rho(a1) ... rho(an), rho(x^-1)=X^-1, rho(y^-1)=Y^-1.

They freely generate a subgroup of SL(2,Z); the full exact matrix therefore retains the freely reduced word. Store one matrix per relator. All14 official AC moves translate exactly into matrix inversion, multiplication and conjugation. We cross-checked33,208 move applications against pinned official SAIR a0fd6e6 across77 verified routes.

Each word can also be placed in its own hyperbolic disk, centered on its target generator: apply X^-1 rho(r0) or Y^-1 rho(r1) to i, then Cayley-map with (w-i)/(w+i). Within this torsion-free discrete subgroup, the stabilizer of i is trivial, so the pair of exact disk coordinates retains the state too. The depth5 check found zero collisions among35,664 matrix pairs and zero among their exact rational disk pairs. Rounded plotted coordinates do not have this guarantee. Matrix entries can grow: this is a faithful encoding, not a compression or a solution algorithm.

That repairs a real blind spot. On71 frozen Astra AC routes, all officially verified,1,181/2,203 moves (53.6%) changed the words without moving the exponent-ledger chart point. There were22 nonterminal visits to the center, representing15 distinct states. ac-03068 is at the center after step1 with50 moves remaining on the recorded route; that50 is an upper bound, not its true minimum distance.

## Does the geometry steer?

Before running, the fixed protocol defined the ordered-chain score as the sum of the two hyperbolic distances from their target generators. For a determinant1 matrix A, d(i,Ai)=acosh(||A||_F^2/2). No weights were fitted.

An uncapped exact official-move BFS through depth6 enumerated336,477 literal states, with layer sizes1,10,77,574,4453,35664,295698. For each of all35,664 depth5 states, every child lies in this ball, so its true distance is known. The test measures the probability that a minimum-score move, breaking ties uniformly, lowers distance from5 to4.

| Score | Shortest-path step probability |
|---|---:|
| Exponent-ledger hyperbolic radius | 28.28% |
| Ordered-chain distance alone | 68.58% |
| Word length | 78.07% |
| Existing H score | 81.06% |
| H, then ordered-chain distance | 81.76% |

There are3,892 depth5 states at the exponent chart's center, and only125 distinct exponent chart points for the35,664 states. The stronger representation plainly sees more; its distance alone is still worse than length in this endgame test.

We then tested a tie-break behind the actual production P2/H implementation, compiled as a read-only score kernel. The C and Python H scores agree on all27,074 distinct evaluated states. Below, lower normalized rank is better;0 is first,1 last, and ties get their mid-rank. This ranks the recorded move among14 legal moves, not eventual beam outcomes.

| Frozen route sample | P2/H | P2/H, then chain |
|---|---:|---:|
|71 Astra routes, all2,203 moves |0.1731|0.1639|
|Same,1,564 moves with ≥10 remaining |0.2097|0.2069|
|Same,284 climbing moves |0.3963|0.3965|
|6 separate control routes, all169 moves |0.1889|0.1682|
|Same,115 moves with ≥10 remaining |0.2532|0.2308|
|Same,26 climbing moves |0.4837|0.4822|

The paired path bootstrap for the71-route far-from-finish improvement crosses zero (chain-minus-baseline mean -0.00226;95% interval[-0.00750,+0.00319]). Overall ranking improves, and the six controls also improve, but they are a small follow-up sample drawn from an existing diagnostic set. They include three capped-search paths and three crossrow paths; they are not six newly proved shortest paths. The benchmark has no held-out beam outcome. The scoring test omits production class quotas, second-eye sampling and deduplication. No production change is justified yet.

## What survives and what does not

The useful chain is ordered matrix transport, with the full state retained. The scalar ratio chain is exact but telescopes. The uploaded Snell-Peel K1/K2/K3 failures remain failures; the near-zero detrended IE/geometry correlation is not rescued by this identity. The supplied ZIP lacks element_records.json, chk_optics.py and the optical YAML data, so those empirical tests were not rerun. Likewise, the earlier private Smith-sector beam pilot's negative outcomes remain recorded separately.

The next discriminating test is a matched-budget beam comparison of (P2,H,fingerprint) versus (P2,H,chain,fingerprint), holding the second eye, quotas, seeds and width fixed on both hump and flat controls. Implement it only as an opt-in experimental variant; preserve baseline path lengths and runtime. A lower offline move rank is not a scoring hit. The original “beat59 on ac-07790 at equal width” Snell test has not been executed here, and that historic threshold is not the current record (the assigned saved snapshot is40).

Small mathematical corrections to the original analogy: (z-1)/(z+1) maps the right half-plane to the disk; the upper-half-plane map is (w-i)/(w+i). A determinant minus-one ledger uses an anti-holomorphic extension to stay in the upper half-plane. Its modular orbit is discrete but is not a regular hexagonal lattice; conjugations can leave its point fixed. Snell/Fermat gives stationary optical time, locally minimizing on appropriate rays, not a universal proof that every ray is a global minimum. Observed length drops pooled from selected solution paths are not intrinsic material speeds.

## Reproduce and evidence

From the repository root with NumPy installed and SAIR pinned to a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e:

    python3 research/acc/optimality/experiments/astra_snell_smith_chain/run_chain_probe.py
    python3 research/acc/optimality/experiments/astra_snell_smith_chain/p2_chain_probe.py

The second command requires gcc and the production C sources. It scores states; it does not launch a beam. Inputs, checks, every move score, raw results, source hashes and the locally written protocol are alongside this note. Slater code is copied unchanged from the user's supplied ZIP, with its hash and missing-input list in source_manifest.json. No new theorem or physical mechanism is claimed.

Primary mathematical sources:
- Steven J. Byrnes, [Multilayer optical calculations](https://arxiv.org/html/1603.02720v5), especially §§2,4: Snell, phase and ordered transfer matrices.
- A. Chorna, K. Geller, V. Shpilrain, [On two-generator subgroups in SL2](https://shpilrain.ccny.cuny.edu/2x2matrices.pdf), §1: Sanov's free generators. This is classical mathematics applied here.

Earlier private beam pilot: research/acc/live/ledger/smith_snell_pilot_20260928.md, blob b9a106b227f1ba47539308b27cab432eb5e172c8. Separate route controls: atlas_beam_ab_20260928.json diagnostic[]; exact source labels and blob SHA are retained in heldout_routes.json.

