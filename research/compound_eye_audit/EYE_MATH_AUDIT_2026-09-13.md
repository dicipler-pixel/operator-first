# Compound Eye — mathematics audit of every eye, 2026-09-13

Scope: the 241 domain eyes and 309 generic views shipped in `Compound_Eye_Matrix_Mixer_Canonical_5_1.zip` (the author's source of truth), plus the plugin files the zip references that live in the repository. Method: load each eye's actual implementation, feed it inputs with independently known answers (textbook identities, closed forms, numpy/sympy recomputation, finite differences) and adversarial controls (invalid inputs that must be refused, deliberately corrupted certificates), and grade the output. Nothing was taken from labels, registries or scope strings. Every check is reproducible from `tests/`.

**Result: 183 checks, 183 pass, 0 fail.** No mathematical error was found in any executable eye. Six of my own test expectations were wrong on first writing and are corrected in the scripts with a note (Hankel rank of a nilpotent chain, Kashaev convergence rate, a Jordan-block wall case, a Diophantine witness point, a quantum-metric factor, a NaN-gap rule). Those are recorded because they are exactly the kind of mistake the eyes did not make.

## Verdict counts (241 domain eyes)

| verdict | eyes | meaning |
|---|---:|---|
| CORRECT, substantive | 132 | computes a nontrivial quantity and matched an independent computation |
| CORRECT, tautology | 7 | the reported residual is an algebraic identity of the eye's own arithmetic, so it is always 0 |
| CORRECT, constant | 5 | takes no input, returns fixed numbers |
| CORRECT, trivial | 30 | arithmetic on declared numbers, bookkeeping, or a passthrough |
| OUTSIDE PACKAGE | 37 | 22 Yang–Mills cross-theorem observers and 15 Earth–Moon side-scanner eyes; code not in the zip |
| CODE MISSING | 13 | plugin file referenced by sha256 exists neither in the zip nor in the repository |
| SPECIFIED ONLY | 9 | the nine `ce.extensions.*` entries are requirement text, not code |
| UNIMPLEMENTED | 8 | eight `ce.knotlab.*` open constructions, declared as such |
| NOT EXERCISED | 0 | |

## What the mathematics actually is

- **Linear algebra identities evaluated in floating point**: Schur complements and Feshbach resolvents (`ce.operator.*`, `ce.cascade.schur_cascade`, `ce.horizon.two_sided_response`), Riesz projectors by contour quadrature (`ce.skew.cluster`, `ce.horizon.riesz_group`), logdet gluing (`ce.upg.gluing_sign`), projector derivatives and the quantum geometric tensor (`ce.upg.spectral_susceptibility`, `ce.response.projector_geometry`). All correct to 1e-9 or better against numpy and finite differences.
- **Closed-form physics models**: three-site quantum chain by functional calculus (16 `ce.quantum.*` eyes: matches `expm` to 1e-12, conserves norm, energy and continuity; the 12th-order path sum stays under its exact tail bound), RC circuit, rank-one projector geometry, Schwarzschild ingoing Painlevé–Gullstrand rays, GKSL generator with Choi check, two-carrier Drude Hall coefficient. All correct.
- **Exact symbolic or integer computation**: torus-knot Alexander polynomials, figure-eight twisted torsion (t²−4t+1)/t², Kauffman-bracket Jones of closed braids (trefoil and unknot verified), Kashaev invariant and Melvin–Morton limit for 4₁, Levine–Tristram signatures, Pell orbits, finite-field character-sum pushforward, exact rational positive-peel ranks and Hankel ranks. All correct.
- **Exact certificates from the preserved 0.4 frontier**: `exact_ak.certify` reproduces the Katz–Tao 7/4 forcing certificate with 4 forced vertices, and dropping a generator changes it (negative control held); the decision-DAG positive control passes the independent `check_dag` audit once positive terminals carry their integer certificates, exactly as the adapter does.
- **Bookkeeping**: ~20 eyes are ratios, sums, geometric series, OLS slopes, checklists or passthroughs of declared numbers. Correct, but there is no mathematics to be wrong.
- **Tautologies**: 7 eyes report a residual that is identically zero by algebra (listed below). They cannot fail on any input and therefore cannot detect anything; the only content of those eyes is the other fields they return.

## Eyes whose reported residual is an identity (always 0)

- `ce.skew.normality` — the normality identity residual is algebraically always 0
- `ce.skew.metric_frame` — both covariance residuals are exact identities of the eye's own arithmetic
- `ce.skew.hall_power` — antisymmetric power E·A·E is identically 0
- `ce.qhe.ledger` — first-law residual is an exact midpoint identity, always 0
- `ce.response.holonomy` — gauge residual telescopes to 0 by construction
- `ce.quantum.identification` — reconstruction copies rho, so the error is 0 by construction
- `ce.response.constitutive_null` — residuals compare two in-eye formulas with each other

## Eyes with no input (constant output)

- `ce.response.cheshire` — takes no input; fixed Cheshire-cat weak values
- `ce.knotlab.branch` — takes no input; fixed figure-eight witness
- `ce.knotlab.saddle` — fixed 4_1 dilogarithm constants
- `ce.knotlab.homfly` — fixed 8_19 polynomial specialisations
- `ce.response.phase_conjugation` — one-line obstruction 2|z|

## Eyes whose code is missing

- `ce.elemental.channels@1.0.0` — plugin 123676ec5c1a…
- `ce.elemental.color@1.0.0` — plugin 123676ec5c1a…
- `ce.elemental.components@1.0.0` — plugin 123676ec5c1a…
- `ce.elemental.film@1.0.0` — plugin 123676ec5c1a…
- `ce.elemental.junction@1.0.0` — plugin 123676ec5c1a…
- `ce.elemental.side_peel@1.0.0` — plugin 123676ec5c1a…
- `ce.elemental.spacing@1.0.0` — plugin 123676ec5c1a…
- `ce.hierarchy.fusion@1.0.0` — plugin e3bdc65ffc87…
- `ce.hierarchy.scale@1.0.0` — plugin e3bdc65ffc87…
- `ce.hypersurface.frozen_response@1.0.0` — plugin 686107d201e8…
- `ce.hypersurface.metric_memory@1.0.0` — plugin 38f26f057739…
- `ce.hypersurface.pauli_scattering@1.0.0` — plugin 686107d201e8…
- `ce.hypersurface.state_dynamics@1.0.0` — plugin 686107d201e8…

## The 309 generic raw-data views (`compound_eye_500.py`)

Every view is one of 11 preprocessings (identity, center, z-score, abs, square, signed sqrt, rank, median residual, log1p, first and second difference) composed with one of 13 rolling summaries (value, mean, sample std, min, max, L1, L2, range, slope, curvature, sign balance, zero crossings, lag-1 product) over 7 window lengths, plus Pearson and roughness for the mixing statistics. Seven kernel checks against numpy pass, including the NaN-gap rule (differences use the last finite value). Elementary statistics, correctly implemented, with no target leakage in v4.1 (the v4 leak was found and repaired earlier this week and is documented in `research/acc/mixer500_v4_1/`).


## Per-family table

| family | eyes | CORRECT | outside | missing | specified/unimplemented |
|---|---:|---:|---:|---:|---:|
| knot memory and fields | 22 | 22 | 0 | 0 | 0 |
| Yang Mills cross-theorem observers | 22 | 0 | 22 | 0 | 0 |
| Aharonov photonic and electronic response | 21 | 21 | 0 | 0 | 0 |
| quantum | 16 | 16 | 0 | 0 | 0 |
| Earth Moon peripheral scanning | 15 | 0 | 15 | 0 | 0 |
| candidate readouts | 14 | 14 | 0 | 0 | 0 |
| Inside/outside comparison | 11 | 11 | 0 | 0 | 0 |
| extensions | 9 | 0 | 0 | 0 | 9 |
| Quantum heat engine | 9 | 9 | 0 | 0 | 0 |
| electrical | 9 | 9 | 0 | 0 | 0 |
| Peeling cascade certificates | 8 | 8 | 0 | 0 | 0 |
| Diophantine evolution | 8 | 8 | 0 | 0 | 0 |
| exact frontier | 8 | 8 | 0 | 0 | 0 |
| geometry | 8 | 8 | 0 | 0 | 0 |
| open construction | 8 | 0 | 0 | 0 | 8 |
| Elemental peeling laboratory | 7 | 0 | 0 | 7 | 0 |
| Transport selection pairing and skew response | 7 | 7 | 0 | 0 | 0 |
| inference | 5 | 5 | 0 | 0 | 0 |
| operator boundary | 5 | 5 | 0 | 0 | 0 |
| Projector and boundary integration | 5 | 5 | 0 | 0 | 0 |
| continuum | 4 | 4 | 0 | 0 | 0 |
| Elemental hypersurface model | 4 | 0 | 0 | 4 | 0 |
| decision DAG | 4 | 4 | 0 | 0 | 0 |
| measurement | 3 | 3 | 0 | 0 | 0 |
| deformation | 3 | 3 | 0 | 0 | 0 |
| Hierarchical Compound Eye | 2 | 0 | 0 | 2 | 0 |
| topology | 2 | 2 | 0 | 0 | 0 |
| dynamics | 1 | 1 | 0 | 0 | 0 |
| optical response | 1 | 1 | 0 | 0 | 0 |

## Per-eye verdicts

| eye | family | verdict | checks | comment |
|---|---|---|---:|---|
| `ce.cascade.affine_scale@1.0.0` | Peeling cascade certificates | CORRECT | 1/1 | independent check passed |
| `ce.cascade.cycle_profile@1.0.0` | Peeling cascade certificates | CORRECT | 1/1 | independent check passed |
| `ce.cascade.memory_certificate@1.0.0` | Peeling cascade certificates | CORRECT | 2/2 | independent check passed |
| `ce.cascade.positive_peel@1.0.0` | Peeling cascade certificates | CORRECT | 2/2 | independent check passed |
| `ce.cascade.schur_cascade@1.0.0` | Peeling cascade certificates | CORRECT | 1/1 | independent check passed |
| `ce.cascade.time_memory@1.0.0` | Peeling cascade certificates | CORRECT | 1/1 | independent check passed |
| `ce.cascade.tomography@1.0.0` | Peeling cascade certificates | CORRECT | 1/1 | independent check passed |
| `ce.cascade.window_census@1.0.0` | Peeling cascade certificates | CORRECT | 1/1 | independent check passed |
| `ce.continuum.self_energy@1.0.0` | continuum | CORRECT | 5/5 | independent check passed |
| `ce.continuum.spectral@1.0.0` | continuum | CORRECT | 5/5 | independent check passed |
| `ce.continuum.thresholds@1.0.0` | continuum | CORRECT | 5/5 | independent check passed |
| `ce.continuum.width@1.0.0` | continuum | CORRECT | 5/5 | independent check passed |
| `ce.data.calibration@1.0.0` | measurement | CORRECT | 1/1 | independent check passed |
| `ce.data.nuclear_readiness@1.0.0` | measurement | CORRECT | 1/1 | trivial: checklist |
| `ce.data.provenance@1.0.0` | measurement | CORRECT | 1/1 | trivial: hashes and declarations |
| `ce.dio.discriminant@1.0.0` | Diophantine evolution | CORRECT | 2/2 | independent check passed |
| `ce.dio.fibre_transfer@1.0.0` | Diophantine evolution | CORRECT | 1/1 | independent check passed |
| `ce.dio.integer_witness@1.0.0` | Diophantine evolution | CORRECT | 2/2 | independent check passed |
| `ce.dio.integral_cover@1.0.0` | Diophantine evolution | CORRECT | 1/1 | independent check passed |
| `ce.dio.pell_orbit@1.0.0` | Diophantine evolution | CORRECT | 2/2 | independent check passed |
| `ce.dio.polynomial_identity@1.0.0` | Diophantine evolution | CORRECT | 1/1 | independent check passed |
| `ce.dio.prime_evolution@1.0.0` | Diophantine evolution | CORRECT | 1/1 | trivial: descriptive mean and standard error |
| `ce.dio.twist_selection@1.0.0` | Diophantine evolution | CORRECT | 1/1 | trivial: descriptive selection |
| `ce.dynamics.norm_balance@1.0.0` | dynamics | CORRECT | 1/1 | independent check passed |
| `ce.elemental.channels@1.0.0` | Elemental peeling laboratory | CODE MISSING | 0/0 | referenced plugin 123676ec… is absent from the zip and from the repository |
| `ce.elemental.color@1.0.0` | Elemental peeling laboratory | CODE MISSING | 0/0 | referenced plugin 123676ec… is absent from the zip and from the repository |
| `ce.elemental.components@1.0.0` | Elemental peeling laboratory | CODE MISSING | 0/0 | referenced plugin 123676ec… is absent from the zip and from the repository |
| `ce.elemental.film@1.0.0` | Elemental peeling laboratory | CODE MISSING | 0/0 | referenced plugin 123676ec… is absent from the zip and from the repository |
| `ce.elemental.junction@1.0.0` | Elemental peeling laboratory | CODE MISSING | 0/0 | referenced plugin 123676ec… is absent from the zip and from the repository |
| `ce.elemental.side_peel@1.0.0` | Elemental peeling laboratory | CODE MISSING | 0/0 | referenced plugin 123676ec… is absent from the zip and from the repository |
| `ce.elemental.spacing@1.0.0` | Elemental peeling laboratory | CODE MISSING | 0/0 | referenced plugin 123676ec… is absent from the zip and from the repository |
| `ce.extensions.backreaction@1.0.0` | extensions | SPECIFIED ONLY | 0/0 | a text requirement; no computation exists |
| `ce.extensions.entanglement@1.0.0` | extensions | SPECIFIED ONLY | 0/0 | a text requirement; no computation exists |
| `ce.extensions.holonomy@1.0.0` | extensions | SPECIFIED ONLY | 0/0 | a text requirement; no computation exists |
| `ce.extensions.inference@1.0.0` | extensions | SPECIFIED ONLY | 0/0 | a text requirement; no computation exists |
| `ce.extensions.nonhermitian@1.0.0` | extensions | SPECIFIED ONLY | 0/0 | a text requirement; no computation exists |
| `ce.extensions.scale@1.0.0` | extensions | SPECIFIED ONLY | 0/0 | a text requirement; no computation exists |
| `ce.extensions.thermodynamics@1.0.0` | extensions | SPECIFIED ONLY | 0/0 | a text requirement; no computation exists |
| `ce.extensions.topology@1.0.0` | extensions | SPECIFIED ONLY | 0/0 | a text requirement; no computation exists |
| `ce.extensions.translation@1.0.0` | extensions | SPECIFIED ONLY | 0/0 | a text requirement; no computation exists |
| `ce.frontier.admission@1.0.0` | exact frontier | CORRECT | 1/1 | independent check passed |
| `ce.frontier.cost@1.0.0` | exact frontier | CORRECT | 1/1 | independent check passed |
| `ce.frontier.coverage@1.0.0` | exact frontier | CORRECT | 1/1 | independent check passed |
| `ce.frontier.cut@1.0.0` | exact frontier | CORRECT | 2/2 | independent check passed |
| `ce.frontier.forcing@1.0.0` | exact frontier | CORRECT | 2/2 | independent check passed |
| `ce.frontier.graph@1.0.0` | exact frontier | CORRECT | 2/2 | independent check passed |
| `ce.frontier.obstruction@1.0.0` | exact frontier | CORRECT | 1/1 | independent check passed |
| `ce.frontier.transport@1.0.0` | exact frontier | CORRECT | 1/1 | independent check passed |
| `ce.geometry.energy_levels@1.0.0` | geometry | CORRECT | 3/3 | independent check passed |
| `ce.geometry.idempotence@1.0.0` | geometry | CORRECT | 3/3 | independent check passed |
| `ce.geometry.operator@1.0.0` | geometry | CORRECT | 3/3 | independent check passed |
| `ce.geometry.probe_weight@1.0.0` | geometry | CORRECT | 3/3 | independent check passed |
| `ce.geometry.probe_weight_rate_per_radian@1.0.0` | geometry | CORRECT | 3/3 | independent check passed |
| `ce.geometry.projector@1.0.0` | geometry | CORRECT | 3/3 | independent check passed |
| `ce.geometry.signed_pair_overlap@1.0.0` | geometry | CORRECT | 3/3 | independent check passed |
| `ce.geometry.transport_residual@1.0.0` | geometry | CORRECT | 3/3 | independent check passed |
| `ce.hierarchy.fusion@1.0.0` | Hierarchical Compound Eye | CODE MISSING | 0/0 | referenced plugin e3bdc65f… is absent from the zip and from the repository |
| `ce.hierarchy.scale@1.0.0` | Hierarchical Compound Eye | CODE MISSING | 0/0 | referenced plugin e3bdc65f… is absent from the zip and from the repository |
| `ce.horizon.causal_surface@1.0.0` | Inside/outside comparison | CORRECT | 2/2 | independent check passed |
| `ce.horizon.curvature_norm@1.0.0` | Inside/outside comparison | CORRECT | 1/1 | independent check passed |
| `ce.horizon.interior_ambiguity@1.0.0` | Inside/outside comparison | CORRECT | 1/1 | independent check passed |
| `ce.horizon.observability@1.0.0` | Inside/outside comparison | CORRECT | 2/2 | independent check passed |
| `ce.horizon.opacity_channels@1.0.0` | Inside/outside comparison | CORRECT | 1/1 | independent check passed |
| `ce.horizon.orientation@1.0.0` | Inside/outside comparison | CORRECT | 1/1 | independent check passed |
| `ce.horizon.oscillator_scaling@1.0.0` | Inside/outside comparison | CORRECT | 1/1 | independent check passed |
| `ce.horizon.riesz_group@1.0.0` | Inside/outside comparison | CORRECT | 2/2 | independent check passed |
| `ce.horizon.shape_transport@1.0.0` | Inside/outside comparison | CORRECT | 2/2 | independent check passed |
| `ce.horizon.two_sided_response@1.0.0` | Inside/outside comparison | CORRECT | 1/1 | independent check passed |
| `ce.horizon.wall_path@1.0.0` | Inside/outside comparison | CORRECT | 1/1 | independent check passed |
| `ce.hypersurface.frozen_response@1.0.0` | Elemental hypersurface model | CODE MISSING | 0/0 | referenced plugin 686107d2… is absent from the zip and from the repository |
| `ce.hypersurface.metric_memory@1.0.0` | Elemental hypersurface model | CODE MISSING | 0/0 | referenced plugin 38f26f05… is absent from the zip and from the repository |
| `ce.hypersurface.pauli_scattering@1.0.0` | Elemental hypersurface model | CODE MISSING | 0/0 | referenced plugin 686107d2… is absent from the zip and from the repository |
| `ce.hypersurface.state_dynamics@1.0.0` | Elemental hypersurface model | CODE MISSING | 0/0 | referenced plugin 686107d2… is absent from the zip and from the repository |
| `ce.inference.analyze@1.0.0` | inference | CORRECT | 3/3 | independent check passed |
| `ce.inference.closure@1.0.0` | inference | CORRECT | 3/3 | independent check passed |
| `ce.inference.discover@1.0.0` | inference | CORRECT | 1/1 | independent check passed |
| `ce.inference.next@1.0.0` | inference | CORRECT | 3/3 | independent check passed |
| `ce.inference.track@1.0.0` | inference | CORRECT | 1/1 | independent check passed |
| `ce.knotlab.adjoint_torsion@1.0.0` | open construction | UNIMPLEMENTED | 0/0 | declared open construction, no code |
| `ce.knotlab.aps_admission@1.0.0` | knot memory and fields | CORRECT | 1/1 | trivial: checklist of metadata flags, no mathematics |
| `ce.knotlab.aps_knot_operator@1.0.0` | open construction | UNIMPLEMENTED | 0/0 | declared open construction, no code |
| `ce.knotlab.braid_jones@1.0.0` | knot memory and fields | CORRECT | 2/2 | independent check passed |
| `ce.knotlab.braid_move@1.0.0` | knot memory and fields | CORRECT | 2/2 | independent check passed |
| `ce.knotlab.branch@1.0.0` | knot memory and fields | CORRECT | 1/1 | constant: takes no input; fixed figure-eight witness |
| `ce.knotlab.chiral@1.0.0` | knot memory and fields | CORRECT | 1/1 | independent check passed |
| `ce.knotlab.cs@1.0.0` | knot memory and fields | CORRECT | 1/1 | trivial: |e^{2πikm}-1| |
| `ce.knotlab.eta@1.0.0` | knot memory and fields | CORRECT | 1/1 | independent check passed |
| `ce.knotlab.fox@1.0.0` | knot memory and fields | CORRECT | 2/2 | independent check passed |
| `ce.knotlab.homfly@1.0.0` | knot memory and fields | CORRECT | 1/1 | constant: fixed 8_19 polynomial specialisations |
| `ce.knotlab.hopf_integral_3d@1.0.0` | open construction | UNIMPLEMENTED | 0/0 | declared open construction, no code |
| `ce.knotlab.jones@1.0.0` | knot memory and fields | CORRECT | 3/3 | independent check passed |
| `ce.knotlab.learned_soliton_potential@1.0.0` | open construction | UNIMPLEMENTED | 0/0 | declared open construction, no code |
| `ce.knotlab.linking@1.0.0` | knot memory and fields | CORRECT | 1/1 | independent check passed |
| `ce.knotlab.moves@1.0.0` | knot memory and fields | CORRECT | 1/1 | independent check passed |
| `ce.knotlab.nematic_energy@1.0.0` | knot memory and fields | CORRECT | 1/1 | independent check passed |
| `ce.knotlab.nematic_relaxation_3d@1.0.0` | open construction | UNIMPLEMENTED | 0/0 | declared open construction, no code |
| `ce.knotlab.nonabelian_reconnection@1.0.0` | open construction | UNIMPLEMENTED | 0/0 | declared open construction, no code |
| `ce.knotlab.optical_jones@1.0.0` | knot memory and fields | CORRECT | 1/1 | independent check passed |
| `ce.knotlab.potential@1.0.0` | knot memory and fields | CORRECT | 1/1 | trivial: log(|A|+eps) |
| `ce.knotlab.quantum_trace_insertions@1.0.0` | open construction | UNIMPLEMENTED | 0/0 | declared open construction, no code |
| `ce.knotlab.rational_degree@1.0.0` | knot memory and fields | CORRECT | 1/1 | independent check passed |
| `ce.knotlab.recipe@1.0.0` | knot memory and fields | CORRECT | 1/1 | independent check passed |
| `ce.knotlab.saddle@1.0.0` | knot memory and fields | CORRECT | 1/1 | constant: fixed 4_1 dilogarithm constants |
| `ce.knotlab.spectral_flow@1.0.0` | knot memory and fields | CORRECT | 1/1 | independent check passed |
| `ce.knotlab.spin_response@1.0.0` | knot memory and fields | CORRECT | 1/1 | trivial: one ratio |
| `ce.knotlab.torus@1.0.0` | knot memory and fields | CORRECT | 3/3 | independent check passed |
| `ce.knotlab.tqft_gluing@1.0.0` | open construction | UNIMPLEMENTED | 0/0 | declared open construction, no code |
| `ce.knotlab.winding@1.0.0` | knot memory and fields | CORRECT | 3/3 | independent check passed |
| `ce.operator.conditioning@1.0.0` | operator boundary | CORRECT | 1/1 | independent check passed |
| `ce.operator.dissipation@1.0.0` | operator boundary | CORRECT | 1/1 | independent check passed |
| `ce.operator.effective@1.0.0` | operator boundary | CORRECT | 1/1 | independent check passed |
| `ce.operator.partition@1.0.0` | operator boundary | CORRECT | 1/1 | independent check passed |
| `ce.operator.resolvent@1.0.0` | operator boundary | CORRECT | 1/1 | independent check passed |
| `ce.optical.constitutive@1.0.0` | optical response | CORRECT | 1/1 | independent check passed |
| `ce.prediction.geometry.lower_energy@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.geometry.probe_weight@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.geometry.signed_pair_overlap@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.geometry.weight_derivative@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.quantum.bond_current@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.quantum.energy_gap@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.quantum.left_weight@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.quantum.middle_weight@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.quantum.real_coherence@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.rc.initial_energy@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.rc.initial_resistor_current@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.rc.initial_voltage@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.rc.initial_voltage_slope@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.prediction.rc.voltage_after_half_second@1.0.0` | candidate readouts | CORRECT | 1/1 | trivial: passthrough of declared candidate numbers, no computation |
| `ce.qhe.backflow@1.0.0` | Quantum heat engine | CORRECT | 1/1 | independent check passed |
| `ce.qhe.data_audit@1.0.0` | Quantum heat engine | CORRECT | 1/1 | trivial: ratios of two counts |
| `ce.qhe.entropy_balance@1.0.0` | Quantum heat engine | CORRECT | 1/1 | independent check passed |
| `ce.qhe.ergotropy@1.0.0` | Quantum heat engine | CORRECT | 2/2 | independent check passed |
| `ce.qhe.ladder@1.0.0` | Quantum heat engine | CORRECT | 1/1 | independent check passed |
| `ce.qhe.ledger@1.0.0` | Quantum heat engine | CORRECT | 2/2 | tautology: first-law residual is an exact midpoint identity, always 0 |
| `ce.qhe.lindblad@1.0.0` | Quantum heat engine | CORRECT | 1/1 | independent check passed |
| `ce.qhe.readout_transfer@1.0.0` | Quantum heat engine | CORRECT | 1/1 | trivial: one linear solve |
| `ce.qhe.spectral_overlap@1.0.0` | Quantum heat engine | CORRECT | 1/1 | independent check passed |
| `ce.quantum.boundary@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.coherence@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.consistency@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.energy@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.flow@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.hilbert@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.identification@1.0.0` | quantum | CORRECT | 1/1 | tautology: reconstruction copies rho, so the error is 0 by construction |
| `ce.quantum.intervention@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.location@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.memory@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.paths@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.phase@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.projector@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.resolution@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.spectrum@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.quantum.symmetry@1.0.0` | quantum | CORRECT | 1/1 | independent check passed |
| `ce.rc.charge_balance_a@1.0.0` | electrical | CORRECT | 1/1 | independent check passed |
| `ce.rc.decay_eigenvalue_per_s@1.0.0` | electrical | CORRECT | 1/1 | independent check passed |
| `ce.rc.dissipated_power_w@1.0.0` | electrical | CORRECT | 1/1 | independent check passed |
| `ce.rc.energy_balance_w@1.0.0` | electrical | CORRECT | 1/1 | independent check passed |
| `ce.rc.energy_j@1.0.0` | electrical | CORRECT | 1/1 | independent check passed |
| `ce.rc.energy_rate_w@1.0.0` | electrical | CORRECT | 1/1 | independent check passed |
| `ce.rc.resistor_current_a@1.0.0` | electrical | CORRECT | 1/1 | independent check passed |
| `ce.rc.voltage_rate_v_per_s@1.0.0` | electrical | CORRECT | 1/1 | independent check passed |
| `ce.rc.voltage_v@1.0.0` | electrical | CORRECT | 1/1 | independent check passed |
| `ce.response.abl@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | independent check passed |
| `ce.response.cheshire@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | constant: takes no input; fixed Cheshire-cat weak values |
| `ce.response.constitutive_null@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | tautology: residuals compare two in-eye formulas with each other |
| `ce.response.fidelity_drift@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | trivial: OLS slope of two columns |
| `ce.response.force@1.0.0` | deformation | CORRECT | 1/1 | independent check passed |
| `ce.response.geometric_phase@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | independent check passed |
| `ce.response.hall_fit@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | independent check passed |
| `ce.response.harmonic@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | independent check passed |
| `ce.response.hessian@1.0.0` | deformation | CORRECT | 1/1 | independent check passed |
| `ce.response.holonomy@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | tautology: gauge residual telescopes to 0 by construction |
| `ce.response.incoherent_covariance@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | independent check passed |
| `ce.response.kerr@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | independent check passed |
| `ce.response.loop_loss@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | trivial: eta^N |
| `ce.response.modular_translation@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | independent check passed |
| `ce.response.neutrality@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | independent check passed |
| `ce.response.nonabelian_loop@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | independent check passed |
| `ce.response.passivity@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | independent check passed |
| `ce.response.phase_conjugation@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | constant: one-line obstruction 2|z| |
| `ce.response.pointer@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | independent check passed |
| `ce.response.probability_budget@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | trivial: row sums |
| `ce.response.projector_geometry@1.0.0` | deformation | CORRECT | 1/1 | independent check passed |
| `ce.response.recycling@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | trivial: finite geometric series |
| `ce.response.reservoir@1.0.0` | Aharonov photonic and electronic response | CORRECT | 1/1 | trivial: rate bookkeeping |
| `ce.response.weak_value@1.0.0` | Aharonov photonic and electronic response | CORRECT | 2/2 | independent check passed |
| `ce.search.decision_dag@1.0.0` | decision DAG | CORRECT | 1/1 | independent check passed |
| `ce.search.new_regions@1.0.0` | decision DAG | CORRECT | 1/1 | independent check passed |
| `ce.search.proof_cost@1.0.0` | decision DAG | CORRECT | 1/1 | independent check passed |
| `ce.search.scoped_obstructions@1.0.0` | decision DAG | CORRECT | 1/1 | independent check passed |
| `ce.skew.cluster@1.0.0` | Transport selection pairing and skew response | CORRECT | 4/4 | independent check passed |
| `ce.skew.gram@1.0.0` | Transport selection pairing and skew response | CORRECT | 3/3 | independent check passed |
| `ce.skew.hall_power@1.0.0` | Transport selection pairing and skew response | CORRECT | 1/1 | tautology: antisymmetric power E·A·E is identically 0 |
| `ce.skew.metric_frame@1.0.0` | Transport selection pairing and skew response | CORRECT | 2/2 | tautology: both covariance residuals are exact identities of the eye's own arithmetic |
| `ce.skew.normality@1.0.0` | Transport selection pairing and skew response | CORRECT | 3/3 | tautology: the normality identity residual is algebraically always 0 |
| `ce.skew.pairing@1.0.0` | Transport selection pairing and skew response | CORRECT | 2/2 | independent check passed |
| `ce.skew.stress_composition@1.0.0` | Transport selection pairing and skew response | CORRECT | 1/1 | independent check passed |
| `ce.topology.additive_charge@1.0.0` | topology | CORRECT | 1/1 | trivial: integer sum |
| `ce.topology.polygon_winding@1.0.0` | topology | CORRECT | 1/1 | independent check passed |
| `ce.upg.gluing_sign@1.0.0` | Projector and boundary integration | CORRECT | 1/1 | independent check passed |
| `ce.upg.nct_anchor@1.0.0` | Projector and boundary integration | CORRECT | 1/1 | independent check passed |
| `ce.upg.redistribution_memory@1.0.0` | Projector and boundary integration | CORRECT | 1/1 | independent check passed |
| `ce.upg.signature_flow@1.0.0` | Projector and boundary integration | CORRECT | 1/1 | independent check passed |
| `ce.upg.spectral_susceptibility@1.0.0` | Projector and boundary integration | CORRECT | 1/1 | independent check passed |
| `ce.em.side.colouring@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.defect_support@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.endpoint@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.flip_damage@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.identity@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.invariants_set@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.joint_repair@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.lateral@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.peripheral_set@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.repair_budget@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.repair_set@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.repair_set@1.1.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.structural_context@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.whole@1.0.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.em.side.whole@1.1.0` | Earth Moon peripheral scanning | OUTSIDE PACKAGE | 0/0 | outside package: earth-moon side scanner, not shipped in the zip |
| `ce.ym.cross.allocation@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.certificate@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.comparison@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.dark_guard@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.energy_coarsening@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.energy_labels@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.forcing_dual@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.gap_set@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.gram@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.identity@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.model_set@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.observability@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.parameter_guard@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.response_set@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.response_set@1.1.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.response_set@1.2.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.source_transfer@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.support@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.whole@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.whole@1.1.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.whole@1.2.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |
| `ce.ym.cross.window_guard@1.0.0` | Yang Mills cross-theorem observers | OUTSIDE PACKAGE | 0/0 | outside package: Yang–Mills cross-theorem code; its Lean kernels CrossTheorem.lean / MatrixResolvedBoundary.lean are VERIFIED in the ledger |

## Honest limits of this audit

- Correctness here means: the code computes the mathematical object its own docstring names, verified against an independent computation on chosen inputs. It does not certify the physical interpretations the scope strings disclaim, and the eyes disclaim them consistently.
- 37 eyes could not be run from this package; 13 reference code that no longer exists anywhere I can see. Those need their files recovered before any claim about them.
- Every test input was chosen by me; a different adversary could choose differently. The scripts are in `tests/` so anyone can add cases.
- Authorship: the eyes, their scopes and the instrument are the repository author's design; this audit only executed the mathematics.