# S6 papers, Thomson certificates, and ACC: two-pass review

Private Mad Hatters research, 2026-09-29. Prepared at the owner's request for the team. This is a mathematical/implementation handoff, not new lane orders, a submission, a full referee report, or a claim of a new ACC solve.

## Executive decision

Keep three jobs distinct: **represent the words accurately; propose promising moves; certify what can be excluded.** The papers suggest ways to organize those jobs, but do not themselves prove anything about our scored AC graph. The new finite-affine representation is a cheap, lossy quotient, not an improvement on the information content of the faithful Sanov representation. Its best possible contribution is a low-cost rejection certificate. The first endpoint diagnostic sharply limits that prospect to short budgets with the present tables.

Do not duplicate session 1's skeleton transfer, Kernel/Bob's generator transfer, or session 2's BEAM_CHAIN A/B. No production flag, process, lane ownership, or automation was changed for this review. No SAIR API read or submission occurred.

## Pass 1: source and claim notes

Read the two supplied PDFs in full; revisited the prior chain report, pinned verifier semantics, current RALLY, Astra orders/updates, WORKING and fresh IDEAS. Pass 2 below re-examines the transferable claims against their hypotheses and actual implementation. Key PDF equations were also checked on rendered pages.

| Source | What is in it | What we can borrow | Boundary |
|---|---|---|---|
| Jeff Viaclovsky, *A two-parameter family of complex structures on S6*, 2609.33785v1, §§2-3 | Elliptic input, lifted translation, singular-fiber completions and an order-four affine quotient | Keep gluing/translation data and compatible markings, not just the linear part | Not an AC algorithm or formal certification of our construction |
| Viaclovsky §4.1, Lemma 4.1 | Affine winding vectors, change of lift, reduction to d=a-c; Hurwitz changes of factorization | Affine cocycles and explicit move words | Similar algebra does not identify the two mathematical problems |
| Viaclovsky §§4.2, 5.2-5.4 | Primitive image forces d²=1; integral minors and indices control torsion | Preserve exact integer certificates when using integer lattices | Rational rank alone is insufficient; trivial abelianization does not solve AC |
| Viaclovsky §5.1 | Meridians are killed, leaving a quotient of an already abelian fiber lattice, which is then killed | Audit precisely where abelian reasoning becomes justified | This is not a reduction of arbitrary balanced trivial presentations |
| Viaclovsky §6.3 | Deformation with fixed local combinatorial data and two independent complex parameters | Family-level transfer as a search hypothesis | No theorem that an AC route transfers unchanged across exponent changes; session 1 already owns this lane |
| David N. Pham, *Twists, Codazzi Tensors, and the 6-sphere*, 2603.05790v2, Definition 1.1 and Proposition 4.1 | Bundle twists change integrability via a Lie-bracket defect | Write a transformation's defect explicitly instead of calling every transformation a symmetry | Bundle maps are not diffeomorphisms; no literal ACC correspondence established |
| Pham Theorems 3.5 and 4.7 | Round-sphere g-Codazzi maps are self-adjoint; these twists cannot make standard S6 integrable | Rule out a restricted method by an invariant/obstruction when possible | Does NOT rule out general twists or complex structures on S6 |

Important bibliographic correction: Pham is an August 30 revised obstruction paper, not a second September construction. Viaclovsky §1.2 names Liu-Rollenske, *Yet another family of complex structures on S6*, as an independent related construction; that third manuscript was not supplied or reviewed here. We are extracting methods, not certifying the full S6 claims.

### Vals/Thomson source notes

[Vals report, September 28](https://www.vals.ai/blogs/thomson-n7-lean-proof): ten Sonnet 5.5 agents, about 15 hours, 17,895 Lean lines; numerical SDP certificates made exact, cases partitioned and integrated. This suggests fixed obligations and exact checking rather than identical searches.

[Public proof repository](https://github.com/huwngtran/thomson-n7-lean) reports minimality and uniqueness, a fixed-statement Comparator, standard-axiom audit, a second kernel and a tampered-certificate negative control. Its description also explicitly says the statement is not human-certified and the work is not peer reviewed. We inspected documentation, not rebuilt the proof or audited all 17,895 lines.

[Reproduction instructions](https://github.com/huwngtran/thomson-n7-lean/blob/main/REPRODUCE.md) pin Lean 4.34.1 and Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612; they request about 14 GB RAM. No build was attempted on our 8 GiB production machine. Their proof does not transfer to ACC.

## Pass 2: mathematical and operational audit

### A. Affine word evaluation: precise definition and limited claim

Viaclovsky's winding data motivate retaining a translation alongside a linear action. Our diagnostic uses the elementary semidirect product

    (t,a,b)(u,c,d) = (tu, a+t*c, b+t*d) mod p,
    (t,a,b)^-1 = (t^-1, -t^-1*a, -t^-1*b),
    X=(2,1,0), Y=(3,0,1), p in {5,7,11}.

Evaluate each relator as an ordered product of generator images. The translation obeys the Fox-style product rule v(uv)=v(u)+t(u)v(v). This is a standard algebraic construction, not a new theorem or the same local system as the S6 paper. It distinguishes some words with equal exponent sums: xy and yx already give different translations. It is metabelian and finite, so it has many collisions; it cannot replace literal-word identity or a faithful encoding.

Every one of the 14 scored AC moves induces exactly inversion, multiplication or generator conjugation on the ordered quotient pair. A full BFS from the projected target supplies h_p(s). Any literal path projects to a quotient path with the same number of atomic steps, hence

    h_p(s) <= d_AC(s, goal).

The maximum across primes is safe; a sum is not generally safe. More generally,

    L(s,t) = max_p |h_p(s)-h_p(t)| <= d_AC(s,t).

Therefore a splice search with budget b can be skipped when L(s,t)>b. For a witnessed span k, L>=k certifies that no shorter AC route joins its endpoints. These are written graph arguments, not Lean-certified statements. Implementation cross-checks are finite evidence, not universal proofs of the program.

The tables use the unrestricted 14-move graph. Bounds remain lower bounds if literal searches impose additional length/work restrictions, but do not certify feasibility under those restrictions. Do not use these AC-only bounds to prune paths that may use stabilization or extra Stable-AC moves. A separate goal/table is required for a different endpoint such as (y,x).

### B. Fresh reproduction and new endpoint diagnostic

`review_checks.py` replays all 77 frozen routes with the clean pinned official verifier, checks the Hurwitz identities on every distinct nonterminal state, enumerates the three quotient components, and verifies closure, inverse moves, edgewise distance inequalities and descending witnesses throughout each component. It makes no network request and starts no beam. `checks.json` contains route verification receipts, example states, all 18 start bounds, source hashes and aggregate tests.

- 77/77 routes pass official AC verification at a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e.
- 2,372 nonterminal visits; 2,148 distinct literal nonterminal states.
- 90,216 literal-move/projected-move comparisons pass (2,148 x 14 x 3).
- 142,632 quotient directed-edge certificate checks pass.
- Exactly three distinct sampled nonterminal states have exponent ledger **equal to I**. They are (Yxy,y), (x,Xyx), (x,xyX), with capitals denoting inverses. All receive bound 1 in each quotient. These are easy one-move examples, not evidence of strength on hard identity-ledger states.
- The earlier chain report's 15 nonterminal **chart-center** states are a different set: matrices other than I can fix the basepoint. Do not conflate the counts.

| p | Target component size | Maximum distance FROM target |
|---|---:|---:|
| 5 | 300 | 5 |
| 7 | 1,176 | 6 |
| 11 | 8,712 | 7 |

These maxima are **goal eccentricities**, not computed all-pairs diameters. Across 18 wide starts, individual-prime bounds range 2-6 and their maxima range 3-6, far below the records. No optimality claim follows.

The new endpoint diagnostic used L above on every overlapping span 2-14 of the same 77 routes, testing whether any shortening could be ruled out:

| Span | Windows | Shortening ruled out |
|---|---:|---:|
| 2 | 2,295 | 695 |
| 3 | 2,218 | 267 |
| 4 | 2,141 | 132 |
| 5 | 2,064 | 55 |
| 6 | 1,987 | 14 |
| 7 | 1,910 | 1 |
| 8-14 | See JSON by span | 0 |

This is a descriptive, overlapping, selected-route sample, not independent trials or a runtime benchmark. L can never exceed 7 with these target-distance tables, so it cannot reject a budget >=7 anywhere in their target components. In particular, it is not a filter for a whole span-14 search with budget13. It might help individual low-budget subsearches, but production may already reject those cheaply. Exact quotient endpoint distances, more landmarks, or larger quotients are untested extensions, not demonstrated improvements.

### C. Hurwitz macros: exact but restricted

For reduced words u,v, the forward Hurwitz map is

    (u,v) -> (u*v*u^-1, u), moves [2,5,2,1], cost FOUR.

Its inverse is [1,3,4,3], also cost four. Algebraically, the intermediate states of the forward word reduce to (uv,v), (uv,u^-1), (uvu^-1,u^-1), (uvu^-1,u). Our fresh checks confirm the formula, inverse and product preservation on all 2,148 sampled states.

Both directions preserve the reduced product uv exactly. Consequently, a Hurwitz-only run cannot reach (x,y) unless the starting product is xy; even that condition is not sufficient. An experimental macro must supplement ordinary moves, retain true atomic costs and check intermediate length/work limits. Existing acc_beam.c already has BEAM_MACROS and accumulates MACL in path cost. This is a proposed macro choice, not a new macro engine. No search-benefit test was run and nothing was enabled.

### D. Corrections important for the team's existing notes

1. General Aut(F2) changes of generators do **not** necessarily preserve distance or heuristic difficulty in our fixed generator-conjugation move metric. A conjugation by y becomes conjugation by phi(y); if phi(y)=xy it generally expands into two atomic conjugations. The goal also changes under phi. Track the transformed endpoint, conversion cost and literal verification. Thus automorphic changes can still be useful; do not conclude that only non-automorphism substitutions could help. Arbitrary non-automorphism substitutions do not automatically preserve the desired problem either.
2. A solved Stable-AC presentation does not automatically give an AC solution by deleting stabilization moves; descending requires its own valid route.
3. A complete finite/capped negative excludes its stated domain. A beam nopath is not a proof of nonexistence. A route gives an upper bound, not an optimum.
4. Smith's (z-1)/(z+1) maps the right half-plane, while the upper-half-plane map is (w-i)/(w+i). The modular orbit is not a regular hexagon lattice, and conjugations can be invisible in the exponent ledger. The prior report already records these corrections.
5. Pooled length drops along selected successful paths are not intrinsic Snell speeds or admissible search bounds. Fermat's principle supplies stationary optical length; global minimality needs additional conditions.

## Current team evidence and non-duplication

Fresh IDEAS and lead UPDATE1115 were consulted. Session 1 has already started skeleton transfer; preserve that ownership. Session 2 has already implemented and is testing the ordered-chain tie-break. At the read snapshot, its one explicitly matched example is ac-03871, 31/33 versus production32/34, equal to noisy seed11 and still above records30/32. That is one-row evidence, not a completed A/B win.

The lead's later IDEAS entry reports a junction-splice Stable tie on sac-08031 using the enlarged route pool. We did not independently verify that new line here, and the entry does not isolate which method supplied the decisive junction. Do not award causal credit to chain alone. The reported window rerun already converted several Astra near misses to ties; distinguish this demonstrated engineering gain from speculative scores.

Production observation during this review: one unchanged W200000 beam on ac-07194/depth46; runner690203/start4294021, beam690204/start4294033, watcher690232/start4294114. One wide row completed (04316, non-hit); no completed07194 receipt at that inspection. Direct /proc cwd access was permission-denied; command/start identity was readable. These are dated observations, not promises that a process remains alive later.

## Recommended next decisions (lead approval, not new assignments)

1. Finish the existing chain A/B, recording matched flags, seeds, width, depth, compiler/window recovery, lengths and wall time. Separate chain-only from noise and splicing effects; preserve every route.
2. If a cheap-filter pilot is wanted, replay a fixed set of already-recorded radius2/3 splice requests. Baseline and filtered runs must produce identical accepted results. Charge table construction, projection and lookups. Keep only a measured net runtime win with zero discrepancies; stop if overhead cancels saved search. Do not begin with span14, where this particular bound cannot exclude the full budget.
3. Only after that, consider a separate, budget-matched four-cost Hurwitz-macro experiment. Never discount a macro to one scored move. Do not overlap existing claimed rows.
4. For proof work, a compact first Lean target is the general graph lemma: edge-compatible projection implies a quotient-distance lower bound, followed by a finite distance-label checker. Reuse existing ACC formal work if applicable, and fix the scored move specification before proving anything. This does not require trying to solve the full Andrews-Curtis conjecture.

## Reproduce / provenance

From repository root, with Python 3 and a clean SAIR checkout at the pin above:

    python3 research/acc/optimality/experiments/astra_paper_transfer_20260929/review_checks.py

Use `--output NEW_FILE.json` to retain a fresh result (exclusive creation prevents overwriting prior evidence). The 71+6 route inputs are the existing astra_snell_smith_chain files; the script checks their exact official replay and records SHA-256 hashes. No T8 or compiled beam is needed for this review diagnostic.

Supplied PDFs (not republished here):

- https://arxiv.org/abs/2609.33785v1 ; SHA-256 effd22502f2eb17619036fa60dd81f2df0c960e8a20af5bb43d77135892c4578.
- https://arxiv.org/abs/2603.05790v2 ; SHA-256 91ee1eee90a85410f20b2030678851cc5b4cb62bef9f4f1586bb895bd92c2d74.

No new scoring hit, Lean build, production speedup or universal ACC theorem is claimed. The deliverable is an exact, reproducible diagnostic plus a narrower test worth considering, with the team's existing work and negative results preserved.
