# Independent definition audit: denominator and iterative cut bridges

Reviewed 14 September 2026 by the arithmetic evidence lane. This is an independent source and mathematical-definition review. It makes **no compilation, kernel-check or transitive axiom-audit claim**. Those gates belong to the build/CI evidence for the final exact revision.

## Verdict

The two modules match the **two-coordinate, nonzero-multiple forcing model used by the audited search**. The denominator argument preserves the whole target pair and all required zeros. The cut proof derives a necessary independent-label pair from an actual finite forcing sequence; it does not assume that cuts already have rank two. I found no mathematical circularity or disguised cut-rank assumption in the reviewed proofs.

The release must retain one qualification: this is not a proved equivalence to the literal three-operation list in the recovered Epoch PDF. That list states unit-target membership and omits an explicit known-coordinate slack rule. Its explanatory prose supports the knowledge interpretation used by the search, but a precise operational definition or a separate interpretation theorem is still required before claiming official challenge-definition equivalence.

## Sources and reviewed snapshots

| Source | Identity |
|---|---|
| `OperatorFirst/KakeyaDenominators.lean` | SHA-256 `57765a4f9e4fa224ba2c2d9778bf12939eea1db6d4658c0099073876c76b4c75`; includes `pair_row_sum_eq` |
| `OperatorFirst/KakeyaCutCompletion.lean` | SHA-256 `58082824adc31c1cc9af0d1629b877c62f51e1474ff74f7bd8d201d472a64790`; inspected after its additional action import |
| [Recovered Epoch problem PDF](https://drive.google.com/file/d/1c5hVZ95_wN6lh8TQ9AOyoI-yIp6rem1n/view) | `arithmetic-kakeya.pdf`, original size 512,893 bytes; readable local extraction SHA-256 `626043b1f46773079494a47d81f4aed25a7ac06968b1e4d119076f0740a91f70` |
| [Current arithmetic research edition](https://drive.google.com/file/d/14AYLpWIBf7iqcqhqLgn8iPiBZlY3apH0/view) | 10 September 2026 edition; explicitly declares the nonzero-multiple verifier setting |
| [Independent certificate checker](https://github.com/dicipler-pixel/operator-first/blob/977b8e59514f83a67a4c13173d5457508518fda4/tools/compound-eye/preserved/original_modular_release/preserved/compound-eye-0.4/dag_search/check_ak_certificate.py) | Source commit `977b8e59514f83a67a4c13173d5457508518fda4`; exact file SHA-256 `6883e9975690105041ead51745c140aab701c2af632e53ca111d6f5d7783c677` |

The PDF hash above is explicitly a hash of normalized extracted text, **not the original binary PDF**. The original PDF bytes were not materialized in the earlier review. New source edits after these snapshots require corresponding review/build records; these hashes do not certify future revisions.

## Literal PDF versus the audited operational rule

Definition 2 on printed page 2 of the recovered PDF allows adding edge-difference rows, adding a vertex when the unit row `(1,-1)_g` belongs to `R`, and adding integer linear combinations. It does not explicitly say to add arbitrary coordinate rows at known vertices. The subsequent Figure 2 discussion on page 4 uses knowledge of a vertex to know other linear functionals there, and says two independent known functionals determine the target functional. That explanation naturally allows exact division by nonzero integers and use of both coordinates at a known site.

The knowledge interpretation is mathematically sensible: knowing `d * ((1,-1)·g)` for nonzero integer `d` determines `(1,-1)·g` uniquely over the rationals/integers; the text's injectivity reduction then identifies `g`. However, division is not itself an operation in the literal integer-row-closure list. A proof about the operational model must be identified as such.

A concrete separating example prevents this distinction from disappearing into wording. Take one vertex, initially unknown, with admissible site rows `(2,0)` and `(0,2)`. Integer coefficients `(1,-1)` give target `(2,-2)`, so the new `CanForce`/`StepZ` rule succeeds with multiplier 2. Every integer combination has two even coordinates, so none equals `(1,-1)`. Thus a theorem claiming that denominator clearing produces a primitive/unit target would be false. This example also shows that rank two does not mean an index-one lattice.

The recovered local checker explicitly checks an integer `nonzero_a`, verifies both coordinates are `(a,-a)`, checks zero output at every other unknown vertex, and allows output at known vertices. It also independently checks target freshness. The new definitions agree with these checks. This checker was independently replayed, but it is not an official Epoch verifier.

## Denominator module: exact assumptions and proof content

1. **Finitely many coefficients; integral rows.** `clear_row_denominators` requires a finite row-index type and an integer-valued row system `A`. The column/site type need not be finite. One denominator clears the finitely many coefficients, therefore scales every output coordinate even when there are infinitely many columns. The theorem does not clear an arbitrary infinite coefficient family, rational row labels, or transcendental coefficients.
2. **A positive common scale, not a primitive normal form.** The induction multiplies existing denominators by the positive denominator of each rational coefficient. It constructs integer coefficients and an equality after casting. It does not round, claim a minimal common denominator, or preserve target coefficient 1. Positivity makes the scale nonzero; integer-to-rational injectivity transfers zeros and nonzeros back to integers.
3. **The generic scalar theorem is not the complete Kakeya step.** `rational_integer_witness_iff` handles arbitrary prescribed zero coordinates and one nonzero coordinate. `forcing_nonzero_multiple_iff` is still a single-coordinate abstraction. Used alone it would not enforce the second target coordinate. The final `StepQ`, `StepZ` and `stepQ_iff_stepZ` expressly add the second equation, with the same scalar and opposite sign, closing that gap.
4. **Known-site slack is unrestricted.** Neither model requires output to vanish at a known site. At the target the output must be `(a,-a)` with `a≠0`; at every other unknown site both coordinates vanish. Both definitions allow a target that is already known when considered in isolation. A caller must impose freshness when using them as a move; `Reachable.step` in the cut module does so.
5. **No substituted primitive target.** In the forward proof, the integer target multiplier is the actual first output coordinate. Its rational cast equals `D*a`, and the second output is proved to be its negative. The proof neither silently treats a rational number as an integer nor assumes that the two coordinates can be cleared independently.
6. **Coordinate-to-pair evaluation.** `pair_row_sum_eq` states that the pair-valued integer sum is exactly the pair of coordinate sums. This is the correct alignment between flattened `(V × Fin 2)` coordinates and `V → ℤ × ℤ`. It is not itself a theorem relating the differently indexed step predicates, a graph parser, or complete forcing sequences.

The finite-index and finite-`G` presentations still need an explicit instantiation when composed: for arbitrary `G : Finset I`, use the finite subtype of indices in `G`, or supply the appropriate restricted-sum equivalence. No theorem in the reviewed two files directly states `StepZ ↔ CanForce` for that adapter or rational/integer reachability equivalence. These are small formal interfaces, but should not be reported as already present merely because the mathematics is straightforward.

## Cut module: actual process and noncircular derivation

`G` is a finite index set; each indexed row is fixed throughout the process. `CanForce` is existence of integer coefficients of these same rows whose output has the prescribed target and support. `Reachable.start` begins at the supplied set `T₀`; each `Reachable.step` requires an unknown target and its integer witness, then inserts only that target. **`Completes` is `Reachable ... Set.univ`.** It is neither a rank predicate nor an assumed catalogue of successful cuts.

The proof genuinely uses the missing iteration step:

1. Before any vertex of a cut `S` is known, restricting a legal witness to `S` kills every output except the new target. This produces a nonzero `(a,-a)` as an integer combination of the restricted fixed rows.
2. If those restricted rows lie on a line generated by admissible `q`, taking their determinant against `q` gives zero. But the determinant of the target is `-a*(q.1+q.2)`, which is nonzero. This is the obstruction.
3. Induction on the reachability derivation proves that a cut trapped on such a line remains wholly unknown, including after steps outside the cut. Completion contradicts that invariant because `S` is nonempty.
4. To obtain a pair rather than a line-exclusion statement, use `q=(1,0)` to find a nonzero restricted row. Its admissibility then permits a second application with that row as `q`, producing a row with nonzero determinant against it. Neither nonzero row nor the independent pair was assumed.
5. For site/edge rows, restriction is a scalar in `{0,1,-1}` times the original label. A nonzero determinant of restrictions implies nonzero survival coefficients and a nonzero determinant of the original labels. Distinct indices and nonzero labels follow from that determinant, though separate distinctness clauses are not needed in the statement.

The hypotheses are consequential, not decorative:

- `S` is a **finite nonempty** set disjoint from `T₀`. Without nonemptiness there need not be any surviving row. If initially known vertices are allowed inside `S`, known-site slack breaks the first-target restriction argument; a fully known graph with no rows is a simple counterexample to that weakened conclusion.
- The general row theorem assumes every **nonzero restricted row** is admissible. This is stronger than arbitrary pointwise labels for an arbitrary multi-site row; sums of unrelated admissible labels can land in the forbidden direction. The specialized site/edge theorem derives the needed restriction hypothesis correctly from the actual row shape.
- The final theorem assumes every active original label has nonzero coordinate sum, with zero allowed separately. Dropping this condition permits a single site row `(1,-1)` to complete a one-vertex graph while providing no independent pair. No primitive-label, positivity-of-label, genericity or local rank-two seed assumption is present.
- `V` itself need not be finite. Finite completion only adds finitely many vertices, so an infinite initially unknown complement cannot satisfy `Completes`. That is an honest conditional boundary; on the intended finite graph it causes no artificial vacuity. `T₀=Set.univ` also cannot satisfy a nonempty initially unknown-cut hypothesis.
- All row data stay fixed. Pre-adjoining all finite graph-edge rows and closing under integer linear combinations is compatible with fixed-row semantics. Arbitrarily adding genuinely new seed rows during the forcing sequence is not allowed by this definition and would invalidate a claim about the original cut labels.

## Graph, site, edge and zero-slot interface

`Generator.site u x` has label `x` only at `u`. `Generator.edge u v x` has the **same** label at its two endpoints with opposite signs. That equality of endpoint labels is what cancels internal edges. It would not hold for an arbitrary two-site row with unrelated labels.

An edge orientation is only a row-sign convention. Loops have zero row and zero cut coefficient. Parallel or repeated indexed rows are allowed; distinct row indices need not have distinct values. The theorem is therefore general enough for simple undirected graphs, but does not construct or validate such a graph. It imposes no tower grammar, no vertex-identification rules, no common finite slope set `X`, no edge budget and no score count. Those restrictions must come from the concrete configuration adapter.

Zero labels are permitted as zero rows. An omitted slot and an included zero row contribute the same zero to every combination and restriction. **`Survives` is geometric:** it means the cut coefficient is nonzero. A zero-label site inside the cut therefore satisfies this predicate even though its algebraic row is zero. This does not damage the final theorem because the returned nonzero determinant excludes zero labels. Documentation should retain that distinction. Empty/zero slots must not be counted as paid edges or initial generators by a score adapter; this module proves nothing about those counts.

The challenge PDF permits vertex identifications in its constructibility grammar; the audited executable tower format treats zero labels as absent edge slots. The two new files do not equate these grammars, and should not be used to imply that all constructible configurations have been covered by the tower search.

## Counterexamples and boundaries that must remain visible

- The archived six-vertex score-`5/3` configuration passes all 63 nonempty rank-two cuts and forces zero vertices. This remains a counterexample to sufficiency. The new theorem proves only the forward implication from completion.
- The old local-seeding lemma remains false. The proofs keep crossing-edge information and never require two independent seeds at the first forced site.
- The historical cut-satisfied search stopping rule remains unsound in general: an admissible reflected Figure 2 three-seed prefix passes all cuts and stalls, while a fourth later-ordered seed completes at score `11/6`. This is not a recovered target winner and does not refute the repaired fixed-budget DAG.
- Labels `(2,0),(0,2)` witness that denominator-cleared forcing and rank two do not imply a unit target, determinant `±1`, index one, or the full lattice `ℤ²`.

These two modules do not prove a new arithmetic Kakeya exponent, score-`67/40` construction, six-vertex barrier, search coverage, DAG-checker soundness, original-grammar equivalence, the analytic counting implication to AK, a Riesz-projector theorem or a transport/geometry connection. They supply two scoped algebraic/process bridges. Their content should not be multiplied into a claim of many new independent mathematical discoveries.

## Required release wording and remaining gates

Safe statement: **For a finite integer row system, rational and integer two-coordinate nonzero-multiple forcing steps are equivalent. For a finite family of admissibly labelled site and edge rows, completion by the fixed-row nonzero-multiple process implies two independent surviving labels on every nonempty initially unknown finite cut.**

Before stronger promotion, retain the fixed-row/site-edge adapter, distinguish the literal PDF from the operational rule, pin the final source revision, compile both modules, collect exact axiom reports and independently check the final build evidence. Static inspection of the reviewed snapshots found no standalone axioms, `sorry`, `admit` or `native_decide`; this observation is not a substitute for those gates.

## Final-source addendum — 14 September 2026, after local verification

This addendum preserves the initial review and its earlier hashes above. It updates the items resolved by the final five-module source and the local verification completed at **10:26:13 UTC**. I reread all five modules, compared the earlier denominator/cut snapshots retained in `logs/*attempts` against their final sources, and checked that all five current source files are byte-identical to the snapshots in the successful verification record.

| Final source | SHA-256 |
|---|---|
| `OperatorFirst/KakeyaDenominators.lean` | `c592ef5d4d4a85454c06930edefb19cef211658ee9ebac47c01c02a88170051f` |
| `OperatorFirst/KakeyaCutCompletion.lean` | `727ad20e673466d95a37cd54c9c714f8212f6a2543a8d22f4fb262cce093e895` |
| `OperatorFirst/KakeyaForcingBridge.lean` | `7c91a47ce7a883b4e52ce0d8ec2626b170c8491fd7e4f3c80cf211f3676fb34d` |
| `OperatorFirst/KakeyaAuditControls.lean` | `6b1e48cdc36c0f2ac49d333aa95e2b7a6aed2cae4c6e7442d5c40bed7fef6743` |
| `OperatorFirst/KakeyaCutAssumptionControl.lean` | `d5b0b85730a811e81dd0684aa8502269a48c6018cb71e976c00530338a345806` |

### Comparison with the original audit

The denominator theorem statements and definitions are unchanged in mathematical content. Its proof repairs replace two conditional-simplification references with `ite_true`, and use the current `Set.mem_ofPred_eq` identifier. The common-scale and nonzero-target argument is unchanged.

The cut theorem statements and forcing semantics are likewise unchanged. Repairs use the supported `push Not` tactic, explicitly unfold `admissible` before deciding the concrete `(1,0)` premise, and rename the site-row helper from `site` to `siteRow`. The renamed helper has the same body. There is no additional cut-rank premise, weaker target condition, altered known-site support, changed reachability constructor, or widened completion definition hidden in these fixes.

### Previously missing finite-row adapter is now present

`KakeyaForcingBridge` closes the **single-step representation interface** identified in the initial review:

- `coordinateRows G rows` indexes exactly the active finite subtype `G`; an index's value selects the original row. Coordinate 0 selects its first component, and coordinate 1 its second. There are no new row values, labels or active indices.
- `combination_eq_coordinate_sums` proves preservation of both outputs after restricting a coefficient function to that subtype. It uses the finite-subtype sum identity and the already reviewed `pair_row_sum_eq`.
- `extendCoefficients` assigns the subtype coefficient to an active index and zero otherwise. The application lemma and `extended_combination_eq_coordinate_sums` prove the reverse preservation. Its `noncomputable` annotation concerns classical membership selection, not an unproved proposition or numerical oracle.
- `canForce_iff_stepZ` transfers both target component equations and both zero equations at every other unknown site in both directions. The use of `Fin.forall_fin_two` covers the full coordinate type; it is not a one-coordinate proxy.
- `canForce_iff_stepQ` then composes that exact equality of integer models with `stepQ_iff_stepZ`. Consequently the active-row pair formulation used in `Reachable` is formally equivalent, step by step, to the rational two-coordinate witness formulation.

This resolves the earlier statement that the finite-`G`/finite-type adapter was missing. Target freshness remains a `Reachable.step` condition, as intended. The files do not introduce a separately named rational `Reachable` relation and prove equivalence of its derivations, nor do they formalize the JSON/tower parser or a search engine. They now supply the exact step equivalence required to build those further interfaces.

### Control modules independently reviewed

`KakeyaAuditControls` proves that rational unit normalization need not give integer unit normalization, and that the first and second coordinate projections have equal ranges but different kernels. Its final target-detection example makes the consequence explicit: the first-coordinate target is nonzero on a suitable element of the second projection's kernel, while it vanishes on the first projection's kernel. The contradiction `w.1=0 ∧ w.1≠0` is the intentionally impossible half of this countercontrol; it is not being used to advertise a substantive Kakeya theorem. These are elementary algebraic regression controls, not configurations, search-coverage results or new bounds.

`KakeyaCutAssumptionControl` uses the deliberately forbidden site label `(1,-1)` on one vertex. It proves non-admissibility, an actual supported integer forcing step, actual `Reachable` completion, and the absence of any independent label pair. It does not assume completion or assume the failure of independence. This is a valid demonstration that the admissibility hypothesis cannot be removed. The object remains explicitly outside the allowed arithmetic-Kakeya label domain.

### Verification evidence inspected

The successful local record is `verification/kakeya_bridges/20260914T102536.849552Z/report.json`, SHA-256 `349010779294da12307b3d0eeb4aff230d9eae9ea6e460bd0229eb9565be0e0c`. Its `sources/` snapshots match the five hashes above. I inspected the report, build transcript, the declaration-audit implementation/output, the checker-scope note and the two intended rejection logs.

- The build finished successfully for all five modules using Lean **4.33.0**, release commit `d8b18978322de05a8f3dba51ef03cf5461676c17`, with mathlib revision `db584cd6d46c92f209a44c0f1c829460d327499d`.
- All five explicitly named standard `leanchecker` module replays exited zero. This is a **Lean-kernel recheck with imported declarations assumed**, not an independent external prover or a fresh replay of the entire imported library. The local compatibility wrapper is recorded in the verification metadata.
- The module-based declaration inventory completed successfully and emitted **121 distinct declarations**, including definitions, generated declarations, constructors and recursors. This is not 121 new mathematical results. Independently parsing those records found only `propext`, `Classical.choice` and `Quot.sound` in their reported transitive axiom sets. The harness rejects additional axioms and standalone new axiom declarations.
- The deliberately false integer-unit and equal-kernel statements were rejected with the intended contradictory goals, not missing-import or syntax errors.

The earlier run `20260914T102434.877496Z` remains recorded as **FAIL**: its build and five checker invocations passed, but the declaration-audit harness failed before the local counter received an explicit `Nat` annotation. The later passing record resolves that harness failure; it does not rewrite the earlier outcome.

### Boundary retained after the adapter and build gates closed

The initial official-definition/unit-target discrepancy remains. Neither the added adapter nor successful compilation supplies an equivalence to the literal three-operation PDF list, an official Epoch verifier result, or a proof of the challenge's analytic counting implication. The zero-slot/cost distinction, constructibility/parser boundary, cut-insufficiency counterexample, and absence of a new exponent all remain exactly as described above. This addendum upgrades the evidence for the stated algebraic/process bridges and closes their step-representation adapter; it does not widen their mathematical claims.
