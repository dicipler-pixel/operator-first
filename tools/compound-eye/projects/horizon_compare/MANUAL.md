# Compound Eye Universal 3 — build and operating manual

The starting point is your complete Universal 2 instrument. This release adds the inside/outside comparison without replacing any registered eye. The current papers and their source files travel with it. No GitHub account, API key, live service or outside download is needed to read the portal and results.

## Open it

Open `START_HERE.html` in a browser. The new boundary lab has three model panels: signed shape coordinates, Schwarzschild light cones, and two candidate interiors with selectable observation channels. The fourth panel ties the freshly replayed Sun calculations to the older eyes. Use **Run the views** to animate them and **Full screen** to expand the comparison. The models remain separate cases; synchronization is presentation timing, not an asserted physical identification.

The browser recomputes the displayed signed-path, ray-slope and two-state trajectories. The observability SVD summaries are embedded outputs of the Python run, at the five selectable return couplings. They are labeled with their time samples and noise assumptions. The catalog includes every prior eye. The original Otto-cycle lab and QHE findings remain available.

## Run it

With Python 3.12 and the pinned dependencies installed:

```bash
python -m pip install -r requirements.txt
python run_horizon.py
```

To repeat the combined focused checks:

```bash
python run_all.py
```

To repeat the selected supplied paper scripts:

```bash
python projects/horizon_compare/replay_sources.py
```

The source replay script limits each subprocess to 180 seconds and sets scientific-library threads to one. It saves every stdout/stderr log and the runtime versions. A timeout or failed process is reported. The sources themselves are unchanged, except for documented PDF typesetting recovery of the two black-hole appendix scripts. A printed diagnostic and a mathematical theorem are different grades of evidence.

The HTML works without Python. Initial Python dependency installation requires package availability or a separately prepared offline environment. The ZIP includes the scripts and evidence, not vendored Python, SciPy or a browser.

To rebuild the portal after a deliberate source update, run `python build_horizon_portal.py` (also available through `python build_portal.py`). This requires Pandoc for offline MathML conversion in addition to the Python dependencies. `python projects/horizon_compare/verify_portal.py` additionally uses Node to check script syntax and compare the browser formulas with SciPy. HTML structure/formula checks are recorded separately from full browser rendering, which was not performed. The plotted scientific controls were visually inspected.

## What the eleven new eyes do

All IDs below have version `1.0.0` and prefix `ce.horizon.`.

| Eye ID suffix | Inputs | Why it is needed | Positive and failure control |
|---|---|---|---|
| `orientation` | Real 3×3 Jacobi matrix X | Exposes information lost by G = XᵀX | Opposite determinants, same Gram; wrong dimension refused |
| `wall_path` | Mixing a, signed q | Integrates an actual metric path | Horizontal lift and arcsine length agree; invalid path domain refused |
| `shape_transport` | Gram eigenvalues w, real t, optional signed q | Compares coordinate and physical-metric norms; supplies regular lift | Symbolic metric self-adjointness; negative w or inconsistent q refused |
| `curvature_norm` | Full positive metric, curvature form, velocity | Compares at fixed geometric speed | Source-form re-expression; singular metric refused |
| `oscillator_scaling` | Positive λ and declared normalization | Separates displacement from velocity | Fixed energy and fixed preparation differ; missing normalization refused |
| `causal_surface` | M, positive radii, model and observer | Tracks causal type and radial null directions | Horizon signs and finite invariant; static interior observer/Kerr request refused |
| `opacity_channels` | Optical depth, flow and sound speed | Separates attenuation from causal closure | Opaque but subsonic two-way proxy; unsupported full-MHD claim refused |
| `observability` | L, C, times, noise and state scale | Measures invisible state directions | Rank-one one-way model; forbidden channel/zero noise scale refused |
| `interior_ambiguity` | Two or more dynamics/initial-state candidates, target and C | Produces explicit non-uniqueness witnesses | Same outside and different inside; model comparison is limited to supplied candidates |
| `two_sided_response` | L, partition, complex spectral point | Keeps both Schur complements consistent | Agreement with the full inverse; singular pivot refused |
| `riesz_group` | A, contour center/radius, count | Preserves the group and verifies its membership | Identity projector at a coordinate Jordan block; wrong contour count refused |

The appropriate pinned sets are `ce.set.horizon_shape@1.0.0`, `ce.set.horizon_inference@1.0.0`, `ce.set.horizon_causal@1.0.0`, and `ce.set.horizon_solar_visibility@1.0.0`. The shape set includes orientation, path, transport and contour views. Curvature and oscillator views are individually selectable. A set expects the union of its members’ required case fields; selecting a whole set does not manufacture missing data.

## How the machine is assembled

1. `machine.py` validates the object/model/basis/boundary/units/source context, then selects pinned eye versions.
2. A decision DAG resolves registered dependencies. Ready eyes can run concurrently. Repeated views do not become independent votes.
3. Each eye receives the same declared case identity for that run, and emits scoped results or an explicit block.
4. A result records the input-context hash, definition hash, implementation identity, assumptions, source stage and status.
5. The new comparison layer preserves the old exact memory, Schur cascade, time-memory, Gram tomography and affine-scale methods. `run_horizon.py` contains complete runnable examples of all five on the new controls.
6. Reports and the portal consume the saved results. The portal’s light browser models have independent tests against Python reference formulas. The HTML does not secretly run the Python engine.

`runs/horizon/simultaneous_frame.json` is an actual four-eye concurrent run on one compatible shape object. A schema-complete request is saved with the results. In contrast, Sun and Schwarzschild panels intentionally have different model identities: resemblance is not permission to pool their measurements.

## How to add another eye without losing an old one

Use `Registry.add(spec, code=path)` as demonstrated in `run_horizon.py`. Give the eye a stable ID and an explicit semantic version. State input units, observable meaning, model assumptions and what failure looks like. Register dependencies first. Add positive controls and a meaningful refusal or counterexample.

The registry copies implementation bytes into a hash-pinned installed path and records an append-only registration event. It will refuse replacement of an existing ID/version. A changed implementation gets a new version. Existing sets remain pinned; changed membership gets a new set version. Keep the previous source and result provenance. Do not “repair” an old manifest hash to disguise a change.

The supplied example manifests and new runner are complete; no manual patching is needed to use this release. `catalog/pre_horizon_hashes.json` proves that all 167 starting definitions are unchanged. `preserved/universal_2_original_changes/` holds any original archive bytes changed by replay or portal updates, with an original-entry inventory. `preserved/universal_2_portal/` retains the previous top-level portal and instructions.

## What to attach to another chat

Attach the complete ZIP and say:

> Use Compound Eye Universal 3. Read START_HERE.md and projects/horizon_compare/FINDINGS.md and MANUAL.md. Preserve all eye versions and model identities. Run run_horizon.py if execution is available, then use appropriate eyes on my new problem. Report only checks actually executed. Treat the finite wall path and metric-self-adjoint transport correction as current findings; do not revive the infinite-barrier or universal velocity-suppression claims. Keep theoretical continuation separate from inference from exterior observations.

The smaller standalone HTML is sufficient for reading and browser demonstrations. The ZIP is the reproducible research artifact. Full source replay requires its Python dependencies.

## Boundaries of the current release

This version supplies declared classical/Sun proxy models, not a solved black-hole interior or a calibrated solar data inversion. Its observers are explicit measurement maps. Its noise rank is a scaled numerical diagnostic. Its exact symbolic checks use SymPy, not Lean. Its curvature scan is a finite pathwise check. Its source replay covers the selected twelve scripts, not every historical script. `SOURCE_AUDIT.md` records the scope and qualifications.
