# Private retina audit — 241 eyes, 48 sets

10 September 2026. This is an inventory/reconciliation note, **not** an upload of
the private Owner bundle and not a change to the clean public Companion share.

The locally preserved `Compound_Eye_Companion_Owner_1_1.zip` has SHA-256
`4bce92b9b5bb096e43ff1037c73236b9e3b5e44a866ae354bc4cd532790050d3`.
It was freshly extracted for this audit. Its unchanged native Registry reports
**241 eye versions and 48 set versions**; history lengths are exactly 241 and 48.
Every eye dependency and every set-to-eye reference resolves: zero broken
references.

The 54,473,436-byte `Compound_Eye_Whole_View_Complete.zip`, SHA-256
`638e3e1aa6ac369c55b8d8a7a9feec39a49077e11e7084cb0f9a2b7c94432b21`,
contains a 204-eye / 33-set predecessor. Its append-only history establishes the
13 additions after the synchronized 191-eye Universal 3.2 baseline:

1. `ce.elemental.spacing@1.0.0`
2. `ce.elemental.film@1.0.0`
3. `ce.elemental.color@1.0.0`
4. `ce.elemental.components@1.0.0`
5. `ce.elemental.channels@1.0.0`
6. `ce.elemental.junction@1.0.0`
7. `ce.elemental.side_peel@1.0.0`
8. `ce.hypersurface.frozen_response@1.0.0`
9. `ce.hypersurface.state_dynamics@1.0.0`
10. `ce.hypersurface.pauli_scattering@1.0.0`
11. `ce.hypersurface.metric_memory@1.0.0`
12. `ce.hierarchy.fusion@1.0.0`
13. `ce.hierarchy.scale@1.0.0`

The Owner instrument then preserves all 204 and appends 37 definitions from the
September 9 dedicated workstreams.

## Earth–Moon side scanner: 15 appended versions

- `ce.em.side.identity@1.0.0`
- `ce.em.side.endpoint@1.0.0`
- `ce.em.side.defect_support@1.0.0`
- `ce.em.side.repair_budget@1.0.0`
- `ce.em.side.flip_damage@1.0.0`
- `ce.em.side.colouring@1.0.0`
- `ce.em.side.lateral@1.0.0`
- `ce.em.side.structural_context@1.0.0`
- `ce.em.side.invariants_set@1.0.0`
- `ce.em.side.repair_set@1.0.0`
- `ce.em.side.peripheral_set@1.0.0`
- `ce.em.side.whole@1.0.0`
- `ce.em.side.joint_repair@1.0.0`
- `ce.em.side.repair_set@1.1.0`
- `ce.em.side.whole@1.1.0`

## Yang–Mills cross-theorem work: 22 appended versions

- `ce.ym.cross.identity@1.0.0`
- `ce.ym.cross.support@1.0.0`
- `ce.ym.cross.gram@1.0.0`
- `ce.ym.cross.energy_labels@1.0.0`
- `ce.ym.cross.allocation@1.0.0`
- `ce.ym.cross.certificate@1.0.0`
- `ce.ym.cross.comparison@1.0.0`
- `ce.ym.cross.observability@1.0.0`
- `ce.ym.cross.dark_guard@1.0.0`
- `ce.ym.cross.window_guard@1.0.0`
- `ce.ym.cross.source_transfer@1.0.0`
- `ce.ym.cross.parameter_guard@1.0.0`
- `ce.ym.cross.model_set@1.0.0`
- `ce.ym.cross.response_set@1.0.0`
- `ce.ym.cross.gap_set@1.0.0`
- `ce.ym.cross.whole@1.0.0`
- `ce.ym.cross.energy_coarsening@1.0.0`
- `ce.ym.cross.response_set@1.1.0`
- `ce.ym.cross.whole@1.1.0`
- `ce.ym.cross.forcing_dual@1.0.0`
- `ce.ym.cross.response_set@1.2.0`
- `ce.ym.cross.whole@1.2.0`

Thus the private lineage is exactly

`191 + 13 + 15 + 22 = 241`.

This count includes combined set/whole definitions and versioned revisions; it
is **not 241 independent scientific measurements or discoveries**.

## Architectural consequence

Cortex development should use two reference retinas:

- **public synchronized baseline:** Universal 3.2 on `main`, 191 eyes / 29 sets;
- **private research retina:** Owner 1.1, 241 eyes / 48 sets.

The second is scientifically richer but must not be copied into the clean friend
share. New cortex organs should be able to point at either Registry root, and
reconciliation into `main` should preserve all existing versions rather than
renaming research history.

The 50 private-retina additions are especially useful for Cortex because they
already contain domain-specific examples of the meta-principles: residue and
hierarchical fusion; hypersurface state/memory changes; alternate graph
representations and repair budgets; energy-labelled Yang–Mills hidden-sector
comparisons; and an explicit forcing-dual observer.

They should be used as **testbeds for the cortex**, not promoted to universal
meta-theorems merely because they exist in several domains.
