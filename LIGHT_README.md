# Light Keeps the Ledger: finite formalization

This branch brings the submitted light supplement into the verified operator-first project and adds finite consequences developed during the manuscript evaluation. It is based on core PR #1; it does not merge the offset or other research branches.

## Declaration inventory

| Modules | Named theorem declarations |
|---|---:|
| LightBridges (eight modules) | 62 |
| OpticalMetric | 12 |
| Rigidity | 8 |
| LightCompletion | 9 |
| Light-specific total | 91 |

The inherited OperatorFirst core contains 14 additional declarations. Counts are inventories, not claims of novelty or certification of the entire manuscript.

LightCompletion proves equal metric with unequal static response; the unique lossless positive-residue two-pole zero and its strict placement between poles; an obstruction to fixed calibration of scalar field-Jacobian rigidity with optical response; and equality of full finite real weighted-Gram kernels. Its calibration obstruction assumes squared transport singular value equals the field metric, fixed positive regularizer, and optical coefficient 1+k*g with k>0. It excludes that particular identification only.

## Reproduce and assess verification

Use the Lean version in lean-toolchain and the Mathlib revision in lakefile.toml:

```
lake update
lake exe cache get
python3 scripts/verify_light.py
```

The script first compiles the full light target, then audits the axiom dependencies of every named theorem and invokes leanchecker for each module. Only propext, Classical.choice, and Quot.sound are allowed. Four false statements must be mathematically rejected. The report is PASS only after all stages succeed. Actual workflow outcomes and downloadable logs are the verification evidence; this inventory alone does not assert a successful run.

The inherited CI separately builds the project and rechecks the original OperatorFirst core. The light workflow uploads all its reports and logs, including failures, as light-ledger-proof-evidence. Review the workflow for the exact commit being evaluated.

## Scope limits

The statements do not formalize spectral differentiation, density-matrix dynamics, Maxwell boundary conditions, homogenization, analytic contour integrals, entropy functional calculus, continuum optical capacity, Kakeya/local smoothing, or a physical transport-to-permittivity identification. The census is formalized as scalar/count algebra plus a projector-block identity; full singular-value spectral mapping remains a written argument. Rigidity starts from a specified scalar singular value.

The manuscript's 18 original numerical verification programs and three independent verifiers were replayed during the evaluation. They provide computational evidence with different scope from the Lean declarations. The supplementary symbolic script scripts/check_light_completion.py checks the new scalar formulas; it requires SymPy.

All merges remain held. This branch is a draft research follow-up.
