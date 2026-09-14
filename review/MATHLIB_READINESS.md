# Mathlib readiness: arithmetic Kakeya proof supplement

Reviewed 14 September 2026. This review assesses source scope, existing mathlib APIs, and contribution fit. It does not replace the independent definition audit or the build and transitive axiom audit for the final repository revision. No proof files were modified and no maintainers were contacted.

## Decision

**The appropriate current deliverable is a downstream Lean proof supplement that depends on a pinned mathlib. These files are not presently an upstream mathlib contribution.** The distinction concerns integration, scope, and review readiness, not whether the mathematics is useful or the proofs can be checked.

The finite denominator result already exists in greater generality in mathlib. The useful project contribution is its precise application to the two-coordinate forcing predicate, the formal finite-step cut obstruction, and the adapter joining those definitions. Describe these as formalized bridges in the declared arithmetic model. Do not describe the denominator theorem as a new mathlib theorem or claim that mathlib has reviewed or accepted the package.

The official contribution guidance explicitly presents a separate repository depending on mathlib as a suitable option for specialized projects and projects that need to evolve quickly. Its upstream criteria include mathematical fit, reviewer expertise, generality, integration, and maintainability. [Official contribution guidance](https://leanprover-community.github.io/contribute/index.html)

## Source snapshot

The source hashes below identify the exact bytes read for this review; later edits require a new snapshot. Compilation status is intentionally left to the final build evidence.

| File | SHA-256 | Source inspection |
|---|---|---|
| `OperatorFirst/KakeyaDenominators.lean` | `57765a4f9e4fa224ba2c2d9778bf12939eea1db6d4658c0099073876c76b4c75` | 218 lines; 8 explicit axiom-print commands |
| `OperatorFirst/KakeyaCutCompletion.lean` | `58082824adc31c1cc9af0d1629b877c62f51e1474ff74f7bd8d201d472a64790` | 261 lines; 1 explicit axiom-print command |
| `OperatorFirst/KakeyaForcingBridge.lean` | `53855a666e57b007b10cbcf42a886f1b6175752fad1978e6b7416d6b915b1599` | 90 lines; 5 explicit axiom-print commands |

The inspected environment pins Lean `leanprover/lean4:v4.33.0` and mathlib revision `db584cd6d46c92f209a44c0f1c829460d327499d`. The project is a separate `kakeyaAudit` Lake package with an `OperatorFirst` library. That is already the correct dependency arrangement for a downstream supplement.

## Existing common-denominator API

The following declarations were checked in the **pinned local mathlib source**, rather than inferred only from current web documentation. They are in `Mathlib/RingTheory/Localization/Integer.lean`, namespace `IsLocalization`.

| Existing declaration | What it supplies | Relation to this package |
|---|---|---|
| `exist_integer_multiples` | One multiplier in the localization submonoid clears all fractions indexed by a specified `Finset` | General version of `finite_common_denominator` |
| `exist_integer_multiples_of_finite` | The same existence result for every index of a finite type | General version of `common_denominator` |
| `commonDenom` | A chosen common denominator for a finite indexed family | An existing API if an explicit selected scale is useful |
| `integerMultiple` | Chosen integer numerators after scaling | An existing API for the scaled coefficients |
| `map_integerMultiple` | Exact equality between the mapped numerator and scaled original fraction | The coordinate identity needed before commuting scaling with row sums |

The general setting is a commutative semiring `R`, a submonoid `M`, and an `R`-algebra `S` satisfying `IsLocalization M S`. In particular, the existing finite-family theorem has the form

```lean
theorem exist_integer_multiples_of_finite {ι : Type*} [Finite ι] (f : ι → S) :
    ∃ b : M, ∀ i, IsLocalization.IsInteger R ((b : R) • f i)
```

Specializing to integers localized in the rationals gives a common nonzero integer multiplier. Passing to its absolute value, with the corresponding numerator sign change, provides a positive natural multiplier. That extra normalization does not make the underlying common-denominator fact new. This review has not implemented or compiled that alternate proof route.

Sources: [exact pinned mathlib source](https://github.com/leanprover-community/mathlib4/blob/db584cd6d46c92f209a44c0f1c829460d327499d/Mathlib/RingTheory/Localization/Integer.lean), [official generated API documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/RingTheory/Localization/Integer.html).

The project's elementary induction over rational denominators is reasonable in a downstream supplement: it is short, transparent, and avoids bringing the localization API into a small arithmetic proof. For a possible upstream contribution, first express the desired result using the existing API. Only a demonstrably missing reusable specialization or bridge should be considered for addition; no such missing API has been established by this review.

## What the three modules actually contribute

| Module | Safe formal scope | Boundary that must remain visible |
|---|---|---|
| `KakeyaDenominators` | A finite integer row system has equivalent rational and integer two-coordinate nonzero-multiple forcing witnesses. One scale preserves both target signs and every required zero. | Does not produce a primitive multiplier, a unit target, or an index-one lattice. |
| `KakeyaCutCompletion` | A fixed finite family of admissibly labelled site/edge rows that completes by the defined forcing process has two independent surviving labels on every nonempty finite cut initially unknown. | Necessary condition only. No converse, new exponent, successful target construction, search coverage, or general constructibility theorem. |
| `KakeyaForcingBridge` | Restriction to the finite subtype `G` and zero-extension of coefficients exactly identify pair-valued `CanForce` with coordinate `StepZ`, then with `StepQ`. | A step-predicate equivalence; it does not supply a graph-file parser theorem, score adapter, or equivalence to every interpretation of the original challenge. |

The newly inspected `canForce_iff_stepZ` and `canForce_iff_stepQ` close the finite-index adapter gap noted in the earlier two-module definition review. `coordinateRows` retains exactly the active original rows; it does not introduce fresh generators. `extended_combination_eq_coordinate_sums` proves that zero-extension preserves the whole output, so the final equivalence retains known-site slack, zero output at other unknown sites, and target `(a,-a)` with `a ≠ 0`.

Neither isolated step predicate requires that the target be fresh. `Reachable.step` adds that requirement when a step is used in the finite process. An external search/checker adapter must preserve it too. The module bridges do not settle the difference between the recovered PDF's literal unit-target integer-closure list and the nonzero-multiple, known-coordinate-slack model used by the audited executable. Keep that distinction in the release description.

## Concrete style and import observations

All three inspected proof files keep lines within 100 characters, use focused imports rather than `import Mathlib`, and have module-level descriptions. Their definitions and proofs are reasonably readable for a research supplement. These are source observations, not a mathlib linter result.

The current official style guide requests a copyright/license/author header, `module`, alphabetized import blocks with the appropriate public/private distinction, module documentation, explicit types, and the standard indentation and line length. [Official library style guide](https://leanprover-community.github.io/contribute/style.html)

| Observation | Downstream consequence | Before any upstream proposal |
|---|---|---|
| No copyright/license/author header in these three files | Follow the host repository's actual license and provenance policy; do not invent authors or relicense third-party material. | Supply accurate headers compatible with mathlib's license and author policy. |
| Files use traditional imports without `module` / a public-import block | Validity is a compiler/build question; this is not a mathematical defect. | Adopt the current mathlib module/export convention for the chosen location. |
| Denominator imports are not alphabetized; CutCompletion imports `Ring` before `Push` | Cosmetic in the downstream package. | Sort the blocks. ForcingBridge's two imports are already ordered. |
| `Label`, `determinant`, `admissible`, `determinantHom`, `combination`, `restriction`, and `Completes` lack individual docstrings | Add concise docs when preparing the polished reusable interface. | Document exported definitions, choose an appropriate namespace, and compare with existing determinant/linear-map APIs. |
| Axiom-print commands occur in the theorem modules | Useful visible audit output in this research package. | Prefer separate audit/test files so importing a library theorem does not emit audit transcripts. |
| Small helper lemmas and project-specific predicates are exported | Convenient for the present supplement. | Decide which are genuinely reusable API, and which should be private helpers. |
| Import minimality and mathlib lint suite have not been independently checked in this review | No claim that imports are unnecessary or all style gates pass. | Run the relevant import and lint checks on the proposed exact files. |

The denominator module need not be refactored onto localization merely to earn the right to exist downstream. Conversely, passing a build does not by itself establish upstream integration quality. The bespoke `ℤ × ℤ` determinant and reachability machinery would need a separate reusable-library design review before being proposed as mathlib infrastructure. This review found the common-denominator overlap, but did not exhaustively prove that no comparable general cut/reachability API exists anywhere in mathlib.

## Human review and upstream communication

Current mathlib guidance requires disclosure of AI use, appropriate marking of substantially generated code, human understanding of the code and its design decisions, and expert supervision. It also explicitly disallows LLM-written GitHub/Zulip comments for its contribution discussions. This is a requirement for a potential **mathlib** contribution; it is not a claim that a downstream research repository cannot carry this proof supplement or an AI-assisted draft PR. No upstream submission is part of the present task. [Official AI contribution policy](https://leanprover-community.github.io/contribute/index.html#use-of-ai)

## Downstream release gate and wording

Proceed as a downstream supplement once the final exact revision has a clean build, the complete theorem/definition inventory and transitive axiom report, the independent definition review, and reproducible commands. Retain negative controls that distinguish nonzero-multiple forcing from primitive membership and necessity from sufficiency. Those controls test the interpretation of the formal statements; they are not substitutes for Lean checking.

Suggested factual scope statement for the package:

> This downstream Lean development, built against a pinned mathlib, formalizes rational/integer equivalence for the declared two-coordinate nonzero-multiple forcing rule and a necessary cut obstruction for finite completion. A finite-index adapter connects the two formal presentations. It does not establish an arithmetic Kakeya target improvement, cut sufficiency, an index-one criterion, or equivalence to the literal unit-target rule of the recovered challenge text.

A later upstream proposal should begin with one small, genuinely reusable missing lemma after checking existing APIs and completing human expert review. The full specialized Kakeya development should remain downstream unless mathlib reviewers separately establish that its design and scope fit the library.
