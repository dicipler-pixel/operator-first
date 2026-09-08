# Proof status — verified 8 September 2026

**All 16 declarations in the new finite module passed Lean compilation,
per-declaration axiom auditing, and the independent leanchecker recheck.**
The intentionally false displaced-transmission equality was rejected.

- Verified source commit: `3eb373797a26f67eccb0ac0b95358d6cac2f39a7`.
- Lean: `leanprover/lean4:v4.33.0`.
- Mathlib: tag `v4.33.0`, resolved to `db584cd6d46c92f209a44c0f1c829460d327499d`.
- [Successful workflow](https://github.com/dicipler-pixel/operator-first/actions/runs/34191153154).
- [Successful job and full logs](https://github.com/dicipler-pixel/operator-first/actions/runs/34191153154/job/101949316110).
- Retained decoded log: `results/lean_verified_job.log`.
- Allowed standard axioms: `propext`, `Classical.choice`, `Quot.sound`.
  No `sorryAx`, admitted statement or custom physical axiom is accepted.

| Declarations | Scope |
|---|---|
| cross_expansion, cross_commutator, cross_zero_iff_commutes | Ring identities for an idempotent split; cross coupling vanishes iff the generator commutes with that split |
| centered_characteristic, denominator_positive, denominator_expansion | Two-orbital rational model algebra, global positive real denominator |
| mirror_transmission, initial_plus, initial_minus, isolated_optical_equal | Exact symmetry and matched scalar data |
| plus_later, minus_later, later_distinct | Exact rational displaced responses and their inequality |
| plus_first_order_remainder, minus_first_order_remainder | Polynomial remainder identities; the derivative limit is a separate written argument |
| no_conductance_only_predictor | No function of the equal initial conductance alone can give both distinct displaced responses |

The stronger manuscript statement about the joint common record has a written
proof using the same two models. The formal predictor theorem's input is only
initial conductance; its scope is not silently expanded to a formal theorem
about arbitrary observation tuples. The general scattering unitarity/graph
construction, Gram bundle refinements, singular-angle identity, FOFT flow and
ladder similarity have written proofs and numerical controls here.

The first two CI attempts exposed proof-elaboration issues and an unclosed
section; those failed builds are preserved in GitHub history. All 16 theorem
statements are unchanged by those fixes. The successful source revision above
is the certificate reference, not the earlier failed revisions.

Earlier proof modules stay pinned to their own sources: Light PR #7 at
`41d9523a53ad679d2240e5e40ed07a7ea0cc2bac`; Peel PR #11 at
`4675da5baf7ca4d35d57fae1004fe63466a31b5b`. Their prior coverage is not counted
among these 16 new declarations. The repository root build checks its core
module and does not certify every separately cataloged project.

## Physical and open obligations

There is no raw atom-by-atom cascade fit, no Au/Pt/Cu/Ag ab initio parameter
identification, and no proof that atomic number equals a projector census.
The complete APS/knot operator bridge, six prior Diophantine targets and
universal physical memory interpretation remain open. The exact benchmark is
a finite coherent model; its discrimination advantage is proved within that
model and must be tested independently on calibrated measurements.
