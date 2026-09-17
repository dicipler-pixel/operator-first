# Do we need more eyes? Live catalog audit — 10 September 2026

The answer is **some, but far fewer than the next architecture needs meta-organs**.

The Cortex 0.1 CI inspected the actual synchronized Universal 3.2 registry:

- 191 eye versions;
- 172 implemented;
- 17 specified but unimplemented;
- two archived results;
- 29 sets.

The 17 specified eyes are not all equal priorities. They are:

### Generic extension placeholders (9)

`backreaction`, `entanglement`, `holonomy`, `inference`, `nonhermitian`, `scale`,
`thermodynamics`, `topology`, `translation`.

Several already have narrower implemented cousins elsewhere in the catalog. We
should therefore **not implement them merely to turn the status green**. Each
needs an explicit model/input contract that adds a capability not already
covered. Examples: `inference` explicitly requires measured data, a noise model
and observability; `scale` requires a family of coarse-graining maps and error
estimates; `nonhermitian` requires a specified non-Hermitian operator and
resolvent/pseudospectral information.

### Open knot/construction eyes (8)

`adjoint_torsion`, `aps_knot_operator`, `hopf_integral_3d`,
`learned_soliton_potential`, `nematic_relaxation_3d`, `nonabelian_reconnection`,
`quantum_trace_insertions`, `tqft_gluing`.

These should be implemented only where the corresponding mathematics and input
representation are actually complete. Leaving a specified eye visibly blocked
is better than filling it with an analogy.

## New eyes that would genuinely add sensing power

The following are stronger candidates than generic renaming:

1. **Independent verifier eye.** Recompute a load-bearing quantity with a
   genuinely different implementation/formulation and compare certificates.
2. **Cross-resolution commutator eye.** Given an observable/operation and a
   coarse-graining map, test whether "observe then reduce" agrees with "reduce
   then observe", with an explicit error term. This makes the Scale placeholder
   useful rather than decorative.
3. **Generic observability/forcing eye.** Promote the Cortex rational
   blind-direction certificate into a properly contracted eye when a linear
   observation matrix and target are supplied.
4. **Uncertainty-propagation eye.** Carry calibrated input uncertainty through a
   named output instead of reporting point estimates. This should complement,
   not duplicate, the existing calibration/provenance eyes.
5. **Independent pseudospectral eye.** For explicitly non-normal models, use a
   separate implementation to check resolvent growth/transient sensitivity,
   rather than assuming eigenvalues are enough.
6. **Formal dependency eye.** Read a declared Lean/theorem dependency manifest
   and report axioms, admitted dependencies and exact source revision. Formal
   proof remains a different evidence class from numerical execution.
7. **Boundary label-loss eye.** Given a planned compression/binning/elimination,
   state which source/support/sign/orientation/energy labels are discarded and
   whether the downstream theorem explicitly needs them.

## Capabilities that should *not* be eyes

These belong in the cortex because they reason about other observations:

- attention / routing;
- contradiction and disagreement resolution;
- evidence lineage and independence warnings;
- theorem/claim dependency memory;
- correction history;
- counterfactual experiment planning;
- information-gain prioritization;
- alternate-representation preservation;
- search-obstruction memory;
- cross-domain assumption translation;
- approval-gated action planning.

Turning these into ordinary eye votes would recreate the problem we are trying
to solve.

## One audit correction

The first catalog audit grouped 81 eyes by the SHA of `plugins/eyes.py`. That is
**module reuse, not 81 copies of one calculation**. Many use different adapters.
Cortex 0.2 therefore distinguishes source-module identity from the stronger
`(implementation hash, function, adapter)` entry-point identity and separately
tracks dependency overlap. Module reuse alone is never counted as duplicate
evidence.

## Priority

1. Cortex theorem genome + discriminator planner.
2. Generic linear visibility eye and label-loss audit, after contracts are fixed.
3. Scale/uncertainty and independent verification eyes.
4. Non-Hermitian/pseudospectral independent validator.
5. Specialized knot-construction eyes only as their mathematics becomes
   independently executable.

The objective is **coverage quality, not eye count**.
