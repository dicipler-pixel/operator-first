# Lean work register — merges on hold

6 September 2026. The user has asked to finish proof work in the draft branches
and defer merging and consolidation. No PR was merged during this pass.

A branch keeps this work separate. A pull request displays the proposed change
and its checks. A passing check verifies the stated Lean propositions and their
assumptions; it does not supply a missing physical or mathematical hypothesis.

## Existing drafts

| PR | Work | Depends on | State of this pass |
|---|---|---|---|
| [#1](https://github.com/dicipler-pixel/operator-first/pull/1) | Build repair and core verifier | main | Previously checked; unchanged; merge held |
| [#2](https://github.com/dicipler-pixel/operator-first/pull/2) | Offset finite log-odds and Fock core | #1 | Previously checked; unchanged; merge held |
| [#3](https://github.com/dicipler-pixel/operator-first/pull/3) | Mixed-file intake and scoped review | #2 | Previously checked; unchanged; merge held |
| [#4](https://github.com/dicipler-pixel/operator-first/pull/4) | Kakeya, atlas, graph and moment extensions | #3 | Previously checked; unchanged; merge held |
| [#5](https://github.com/dicipler-pixel/operator-first/pull/5) | Offset reflection and endpoint corrections | #2 | Previously checked; unchanged; merge held |
| [#6](https://github.com/dicipler-pixel/operator-first/pull/6) | Endpoint analysis and finite proof completion | #5 | New work in this pass; exact verification evidence accompanies this register |

The preserved heads of #1–#5 are respectively `9bbc220aabf9`, `92a95a427ddf`,
`1619b042f2e3`, `41fbf3b9e6ad`, and `7818a3c4ac87`. The repository's main
branch is unchanged at `032ec75a360fa55caa83c687d2038558103a36fb`.

## Offset work completed in this batch

- The band equation now leads formally to the polynomial contradiction;
  both polynomial components must vanish on an exact band.
- Finite projection compression gives the occupation and determinant domains
  once the two projected embeddings are injective.
- The three-site interpolation is explicitly assembled from the affine determinant.
- The relative perturbation bound, its convergence consequence, parity handling,
  and conversion to the half-offset magnitude are formalized.
- One runnable verifier compiles, audits and independently kernel-checks all
  three new modules and rejects four false controls. Endpoint CI runs it.

See [the exact scope](OFFSET_COMPLETION_SCOPE.md) and
`offset_completion/report.json` for the checked source hashes and results.
There are 28 new named theorems, bringing the Offset modules to 119 named
theorems (53 core, 30 endpoint, 8 earlier progress, 28 in this batch). This is
an inventory of formal statements, not a count of new physical discoveries.

## All-size analytic transfer completed after the finite Lean batch

The moduli-space argument in
[ALL_SIZE_TRANSFER.md](moduli_transfer/ALL_SIZE_TRANSFER.md) proves the
unequal-hopping interpolation for every odd block size. It first reduces
the determinant to a polynomial in the bulk invariants and v, then bounds
its degree in v by isolating one unpaired boundary column.

The fixed-parameter general Rice–Mele endpoint follows by combining this
identity with the existing equal-hopping Hankel argument. The remainder
itself transfers with the same v/e factor, so its successive ratio is
unchanged along the isospectral family wherever defined.

This is an ordinary mathematical proof, not a new Lean certificate.
The 119 named Offset Lean statements and their sources are unchanged.
The companion verifier supplies exact symbolic finite checks, exact rational
determinant-pencil checks, two rejected false controls, and independent
200-digit physical determinant tests. Its numerical output is not an
interval enclosure.

## General all-size degree argument formalized

`OperatorFirst/LaurentBoundary.lean` contains 20 additional named statements.
They cover Laurent coefficient bounds, arbitrary finite determinants with
column budgets, the one-boundary specialization, survival of the leading
coefficient under a faithful chart, and the literal affine-polynomial result.
The verification report supplies the exact checked source and allowed axioms.

This is the general algebraic mechanism. Applying it to the actual Rice–Mele
matrix still requires the invariant-polynomial representation, explicit
similarity identity, and concrete chart hypotheses in Lean. The complete
written proof remains valid; these are remaining formalization steps.
See `laurent_boundary/FORMAL_BOUNDARY_SCOPE.md` for the line-by-line scope map.

The verifiers now accept extracted supplements with no research checkout.
They record Git provenance when present, otherwise the supplied source revision
and exact file hashes. This changes provenance handling, not theorem statements.

## Proof work still open

These entries remain open. They are not fixed by merging, and they are not
being marked complete because a finite example or a conditional theorem passes.

| Area | Missing argument |
|---|---|
| Offset covariance | Formal Fourier construction, the almost-everywhere step and the integral-to-matrix identification connecting the band obstruction to the physical restricted covariance |
| Offset endpoint formalization | The all-size interpolation is now proved in moduli_transfer/ALL_SIZE_TRANSFER.md; the general Laurent-degree and faithful-substitution mechanism is formalized; encode the model-specific invariant-polynomial reduction, block similarity, and concrete chart hypotheses |
| Offset analytic limit | Lean formalization of the equal-hopping Fourier/Hankel reduction and its asymptotic theorem |
| Offset remainder and cosmology | A sharp remainder proof and a justified physical calibration to the cosmological constant |
| Kakeya general rank | Assemble the general iterative forcing/subset-rank argument and lattice-rank conclusion beyond the checked finite examples |
| Kakeya atlas | General rational-to-integer clearing and the full constructibility grammar beyond the fixed certified family |
| Earth–Moon graph | Full planarity/Euler identification and the chromatic lower bound beyond the checked edge/counting and colouring statements |

The last three rows are recorded from #4's scope documents. This pass has
focused on Offset, in accordance with the one-paper-at-a-time instruction;
it has not silently closed those other papers' outstanding work.

Merging, combining the branches, and incorporating these later proofs into a
new paper edition remain deliberately deferred. No merge order is being
executed by this register.
