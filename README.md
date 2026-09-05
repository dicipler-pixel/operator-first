# operator-first

Lean statements from the operator-first corpus, with verification tied to the exact CI commit.

Jeromie Beasley — source paper *Light Keeps the Ledger*,
https://doi.org/10.5281/zenodo.22124938

## What the default build checks

`OperatorFirst.lean` is the single library root. It contains 14 theorem declarations:

- **Commutator algebra:** `[S + K, S - K] = -2 [S, K]`, and the zero-commutator equivalence under an explicit hypothesis that multiplication by two has trivial kernel. Calling the partner a transpose or adjoint requires the corresponding identification.
- **Reciprocity:** if `Bᵀ = B` and `Vᵀ B = B V`, then `B V` is symmetric and the bilinear response is symmetric in its probes. No positivity or invertibility of `B` is assumed.
- **Pure-marker Gram algebra:** conjugate-symmetry and determinant identities, Cauchy–Schwarz, and the identity `D² + V² = 1` for unit markers with `V = ‖⟪u,v⟫‖` and `D = sqrt(1 - V²)`. The operational state-discrimination interpretation of `D` is not independently proved by defining it this way.

The root emits `#print axioms` for every theorem. The older `Warmup.lean` and `Warmup (1).lean` uploads are retained unchanged, but are **not** default build targets. This repository's CI does not certify files merely because they are present in the tree.

## Pinned toolchain and build

The project uses Lean `v4.33.0` and the matching mathlib tag.

```sh
lake update
lake exe cache get
lake build OperatorFirst
lake env leanchecker OperatorFirst
```

## CI verification boundary

The workflow in `.github/workflows/ci.yml` runs on pushes and pull requests. It must:

1. Build the actual `OperatorFirst` library.
2. Recheck that module with `leanchecker` (the imported compiled libraries remain part of the trusted foundation).
3. Run the compiled-environment axiom audit, allowing only `propext`, `Classical.choice`, and `Quot.sound`.

An installation step passing, a file containing no visible `sorry`, or a green run on a different commit is not a verification result for the current source. Inspect the build/recheck/audit steps of the exact commit. A failed or pending job is not a proof certificate.

The September 5 repair restores TOML accidentally replaced by workflow YAML and repairs Matrix notation and a complex norm cast proof. The associated pull request records actual run results; edits alone do not establish verification.

## Scope

This project checks the encoded mathematical statements and their explicit hypotheses. It does not certify the whole paper or its physical interpretations. The separate light, offset, gravity, and hypersurface candidate archives from the research conversation are not included in this 14-theorem build.
