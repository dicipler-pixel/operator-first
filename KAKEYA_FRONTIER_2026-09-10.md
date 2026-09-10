# Arithmetic Kakeya frontier — corrected status and a small-complexity conjecture

**Jeromie N. Beasley — 10 September 2026**

**Status.** This is a current research-frontier note, not a claim to solve the Arithmetic Kakeya Conjecture. It records the surviving results, corrections, finite exclusions, formal scope, and the smallest clean conjecture suggested by the present evidence. The research direction and finite programme are author-directed; AI systems assisted with search, coding, formalization, checking, drafting, and the present formulation. Established literature is cited as literature rather than relabeled as original work.

## 1. Why I arrived here

My route to Kakeya began from a different question: what does it cost for a finite system to retain many distinguishable directions at once? Earlier operator-first work treated directions through spectral projectors, directional support sets, channel capacity, and loss of rank-one directional information under coarse-graining.

Those papers are **motivation and provenance**, not evidence for the arithmetic conjecture below.

- J. N. Beasley, *The Price of a Direction: Boundary Channel Budgets, Directional Capacity, and Kakeya Structure in Operator Transport*, Zenodo record 21918464 (published inventory v4): https://doi.org/10.5281/zenodo.21918464
- Earlier directional-transport lineage, *Integrated Quadralogy Architecture: Directional Transport Geometry*: https://doi.org/10.5281/zenodo.21089303

The arithmetic work then moved to the public Katz–Tao / FrontierMath constructible formulation and its exact forcing rules.

## 2. Exact target

Use Epoch's current **verifiable formulation**: `X ⊂ Z²` is finite, `(0,0) ∈ X`, and every nonzero `(a,b) ∈ X` satisfies `a+b ≠ 0`. For an admissible `X`-constructible graph/tower with `n` vertices and `m` edges and a forcing pair `(R,T)`, put

`q = n - |T|`

and

`S = (m + |R|) / q`.

The target is a completely forcing construction with score below the Katz–Tao reference

`γ = 1.675130870566...`,

the largest real root of `x³ - 4x + 2`. In my finite searches I use the slightly stronger exact target

`S ≤ 67/40 = 1.675`.

Nothing in this note claims that target has been reached.

## 3. Surviving exact algebra

Let `B` be the rational span of the edge relations and the initial generators. Let `E_K` be the full coordinate subspace supported on the currently known vertices `K`. Under the public forcing rule, a vertex `v` can be forced exactly when

`(1,-1)_v ∈ B + E_K`.

The rational test is faithful here because a rational witness can be cleared of denominators to give a legal integer witness with a nonzero integer target multiple.

A useful dual form is the general linear-algebra criterion formalized in Lean. For observation map `A` and target functional `b`, define a hidden forcing direction by

`A c = 0` and `b c ≠ 0`.

Then

`CanForce(A,b) ↔ ker(A) ⊄ ker(b)`.

If `b = y ∘ A`, a dual certificate proves that no such hidden forcing direction exists.

Lean source:
https://github.com/dicipler-pixel/operator-first/blob/41fbf3b9e6ad8143d597928e477a9d94adb6d6d6/OperatorFirst/KakeyaForcingLinear.lean

## 4. Subset-cut obstruction

For any nonempty set `U` of still-unknown vertices, sum a hypothetical first forcing witness over `U`. Relations internal to `U` cancel. Only initial generators inside `U` and edge labels crossing the boundary of `U` remain. Those surviving labels must span two dimensions.

This gives a reusable necessary rank obstruction.

It is **not sufficient**. A recovered six-vertex score-`5/3` control passes all 63 nonempty subset-cut tests and nevertheless cannot force even its first vertex; exact dual certificates detect the stall. This negative control is part of the reason the present conjecture is not being promoted as a theorem.

## 5. Correction to my 2 September draft

The earlier draft *Constructible Proofs for the Arithmetic Kakeya Conjecture* contained a false local-seeding lemma: it required two independent initial generators at the first forced vertex.

That is wrong. The paper's own four-vertex Figure 3 supplies a counterexample: three initial generators distributed over three different vertices can force the whole graph, beginning at the vertex carrying no initial generator.

The explicit four-step correction is formalized in Lean. Therefore the old locally seeded search must not be treated as an exhaustive search of the unrestricted forcing grammar.

Correction:
https://github.com/dicipler-pixel/operator-first/blob/41fbf3b9e6ad8143d597928e477a9d94adb6d6d6/KAKEYA_SEEDING_CORRECTION.md

## 6. Corrected finite evidence

For the fixed six-vertex, seven-edge baseline, the unrestricted three-generator domain contains **11,480** generator subsets. The old local restriction omitted **6,860** distributed-generator subsets. The corrected baseline enumerated all 11,480 and found no completely forcing construction meeting the target in that fixed family.

The later exact DAG/certificate release covers 33 declared tower-and-generator-pool cases: the original tower, 30 single-table-label mutations, a specified reversed `(3,2)` replication orientation, and a larger generator pool on the original tower, including every initial-known set that can meet the score budget in those declared cases.

Distinct accounting:

- corrected baseline: **11,480** configurations;
- distinct new configurations beyond the baseline: **470,232**;
- distinct union: **481,712**;
- complete qualifying constructions found: **0**.

A separate 344,400-candidate run overlaps the later certified region and is therefore **not** counted again as 344,400 additional exclusions.

These are exact finite exclusions of declared families, not an exhaustive search of all six-free-vertex constructible objects.

## 7. All-parameter Lean result in one fixed family

In the fixed four-vertex family obtained by replacing one edge label with `(1,q)`, the formal development proves over the rationals that the construction completes **if and only if `q = 2`**, allowing every fresh-vertex forcing order. At `q = 1`, a first move is possible but the process stalls. The sole completing member has score `7/4`, above the target.

At `q = 2`, the initial kernel is the line generated by

`c = (-1,-1,1,-1,2,-1,-2)`,

and `P = c cᵀ / 13` is formally proved symmetric and idempotent with the required kernel and target-response properties.

Formal scope and verification record:
https://github.com/dicipler-pixel/operator-first/pull/4

## 8. Granularity: why six vertices are a sharp small test

Because `m + |R|` is an integer, for `1 ≤ q ≤ 6` a score below `γ` is equivalent to

`m + |R| ≤ floor(5q/3)`.

Thus the record-breaking question on at most six free vertices is an exact finite-complexity barrier question, not a numerical-precision issue.

The known six-vertex Katz–Tao construction has score `11/6`; simply removing one generator gives the attractive score `5/3` but destroys forcing. My corrected searches repeatedly encounter this same tension: lowering the numerator is easy; retaining complete forcing is the hard part.

## 9. Conjecture — the six-free-vertex barrier

> **Small-constructible Arithmetic Kakeya Conjecture (six-free-vertex barrier).**
>
> Let `X` be any admissible finite dilate set in Epoch's current verifiable formulation: `(0,0) ∈ X` and every nonzero `(a,b) ∈ X` obeys `a+b ≠ 0`. Let `G` be any `X`-constructible object under that verifiable arithmetic-Kakeya grammar, and let `(R,T)` completely force `G`. If
>
> `1 ≤ q = n - |T| ≤ 6`,
>
> then
>
> `S = (m + |R|)/q ≥ γ`,
>
> where `γ` is the largest real root of `x³ - 4x + 2`.
>
> Equivalently, no completely forcing object with at most six free vertices satisfies
>
> `m + |R| ≤ floor(5q/3)`.

**This is a conjecture, not a consequence of the finite searches above.**

Why it is useful either way:

- A **counterexample** is immediately a record-breaking constructible arithmetic-Kakeya object.
- A **proof** establishes a genuine small-complexity obstruction and says that any successful constructible attack must leave the six-free-vertex regime.

The finite evidence motivating it is substantial but deliberately incomplete.

## 10. The exact unclosed region

The current certificates do **not** exclude:

- simultaneous changes to several table labels;
- all labelings of the reversed tower;
- arbitrary constructible graph/tower topologies;
- unrestricted finite slope/dilate pools;
- altered edge budgets;
- genuinely larger tower structures.

Within the six-free-vertex regime, these unsearched coupled changes and alternative topologies are precisely where the conjecture can still fail.

The next constructive search should therefore attack specific terminal dual obstructions by changing several structural choices together, while retaining distributed generators and the public forcing grammar. Every new candidate should record exactly which old obstruction it escapes and then be checked by an independent closure/certificate implementation.

## 11. Literature and scope

The Katz–Tao arithmetic method, its subsequent formulations, generalized arithmetic-Kakeya work, and recent related constructions are prior art and provide the problem being attacked. This note does not claim ownership of Arithmetic Kakeya, the Katz–Tao score, row-space duality as general linear algebra, or standard decision-DAG/search ideas.

A targeted search performed while preparing this note did not identify this exact **all constructible objects with at most six free vertices** barrier as a published theorem or conjecture. That is not an exhaustive novelty proof. References, equivalent formulations, prior results, or counterexamples are explicitly invited.

## 12. Verification/provenance boundary

The strongest current formal record is draft PR #4 at commit

`41fbf3b9e6ad8143d597928e477a9d94adb6d6d6`

with successful isolated verification run

`33989244224`.

The branch includes compilation, axiom auditing, kernel rechecking, and deliberately false controls. Its 95 named declarations span several modules and projects; they are **not** 95 Kakeya discoveries.

The broad general iterative cut theorem, arbitrary constructibility grammar, and the full decision-DAG proof system are not completely formalized in Lean. No official accepted Arithmetic Kakeya submission or improved bound is claimed here.

---

Copyright © 2026 Jeromie N. Beasley. Scholarly text is governed by the repository's CC BY 4.0 policy; source code and Lean formalizations are governed by the repository's MIT policy unless a file states otherwise.