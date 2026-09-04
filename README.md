# operator-first

Machine-checked statements from the operator-first corpus.

Jeromie Beasley — source paper *Light Keeps the Ledger*,
https://doi.org/10.5281/zenodo.22124938

## What is here

Two warm-up theorems, each stated in the most general setting in which it is
actually true.

**T1 — the commutator identity.**  For any ring and any `S`, `K`,

    [S + K, S - K] = -2 [S, K]

so that `C = S + K` with `Cᵀ = S - K` is normal exactly when `S` and `K`
commute.  The corollary carries an explicit hypothesis ruling out
characteristic two, where `-2x = 0` for every `x` and the statement is empty.
Real and complex matrices satisfy it.

**T2 — reciprocity.**  For square matrices over a commutative ring, if
`Bᵀ = B` and `Vᵀ B = B V`, then `B V` is symmetric, hence
`xᵀ(BV)y = yᵀ(BV)x` for every pair of vectors.  The hypotheses are minimal: positivity,
definiteness and invertibility of `B` are never used.

## Two builds

`standalone/Warmup.lean` depends on **nothing**.  It defines its own ring
axioms and proves both theorems from them.  It compiles under plain Lean 4
with no library:

    lean standalone/Warmup.lean

`#print axioms` reports that all three results *do not depend on any axioms* —
not choice, not propositional extensionality, nothing.  They are constructive
consequences of the ring axioms as written.

`OperatorFirst/Warmup.lean` is the mathlib version, which is the one that
belongs in a library and can be built on.  Build it with

    lake exe cache get
    lake build

## CI

`.github/workflows/ci.yml` runs `lake build` against the mathlib cache on every
push.  The green check is the verification.
