# Finite Lean kernels of fifteen Atlas cards, with B56 repaired

Stable ID: `ATLAS-FINITE-KERNELS`

## Statement

Exact finite kernels of cards B2, B16, B31, B32, B48, B51, B57, B60, B61, B66, B68, B74, B85 and B90 compile in Lean/mathlib; B56 is replaced by the corrected statement that a regular codimension-one wall and a regular codimension-two coalescence locus in a two-real-parameter model cannot meet transversely, because the combined derivative is a linear map from R^2 to R^3 and cannot be surjective.

## Assumptions

Finite real matrices and polynomial identities over the stated rings; two real parameters for B56; B90 is restricted to explicit local normal forms.

## Failure mode

The English card captions are stronger than the kernels. B56 makes no disjointness claim. The generic n=2 versus n=1 exponent statement of B90, measurements, continuum statements and physical readings are not certified.

## Evidence status

Lean source compiled on PR #21 with axiom audit, leanchecker and four mathematical false controls; GitHub Actions run 34684818137 succeeded at the pinned head. Not yet assigned an LC tag in the certificate registry.

## Verification scope

proofs/atlas_formal/AtlasFormalCore.lean at f4e682ff428b5e941a3da7d2a1b211dc925bdbc6: 21 theorem declarations, 5 definitions. Source-reported CI; not recompiled during this audit.

## Credit

Jeromie N. Beasley, Operator-First Atlas; standard finite linear algebra and polynomial identities are not claimed as new.

## Next step

Promote in the certificate registry or record the exclusion; compile the second batch B1, B18, B22, B23, B39, B46, B54, B70, B75, B84, B89.

## Sources

- [AtlasFormalCore.lean (pinned PR #21)](https://github.com/dicipler-pixel/operator-first/blob/f4e682ff428b5e941a3da7d2a1b211dc925bdbc6/proofs/atlas_formal/AtlasFormalCore.lean)
- [FORMALIZATION_MAP.md (pinned PR #21)](https://github.com/dicipler-pixel/operator-first/blob/f4e682ff428b5e941a3da7d2a1b211dc925bdbc6/proofs/atlas_formal/FORMALIZATION_MAP.md)
- [Atlas formal verification run](https://github.com/dicipler-pixel/operator-first/actions/runs/34684818137)

## Paper applications

- [atlas](../papers/atlas/README.md)
