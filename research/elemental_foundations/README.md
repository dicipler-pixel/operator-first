# Elemental Peeling and What the Boundary Retains

Combined research manuscript 1.0, 8 September 2026. Author: Jeromie N. Beasley.

Read `Elemental_Peeling.pdf` or the self-contained `Elemental_Peeling.html`.
The contribution is an exact response-discrimination benchmark and a calibrated
framework for elemental interventions. It is not a new measured elemental law.

## Reproduce the new work

From the repository root, with Python 3.11 or later:

```bash
python -m pip install numpy scipy sympy pyyaml matplotlib
python research/elemental_foundations/run_experiments.py
python research/elemental_foundations/run_source_controls.py
python research/elemental_foundations/build_figures.py
```

The immutable methods are already registered. `register.py` and
`register_reductions.py` are idempotent registration utilities. Existing versions
are never overwritten. The current registry has 204 versions and 32 sets.

The first script runs 550 eye evaluations and 1,700 assertions, including two
intended domain refusals. The second runs 340 evaluations and 745 assertions,
including three intended refusals. These are finite calculations and controls,
not independent physical experiments. The original FOFT gradient audit was also
run: it rejects an earlier incorrect flow and supports the corrected isospectral
flow. Its exit code alone is not a scientific pass/fail summary.

## Elemental evidence and earlier work

`tools/compound-eye/projects/elemental_peel/` contains the Au/Ag/Cu/Pt data,
provenance flags, Maxwell-film/color calculations, contacted electronic-sheet
model, original hypersurface archives, code and execution records. Its completed
1,253 evaluations and 846 assertions belong to the preceding elemental extension.
The current combined paper retains that evidence; it does not call every older
result a new run. `run_study.py` and `extend_observations.py` reproduce that supplement.

`tools/compound-eye/START_HERE.html` contains the complete instrument catalog and
prior viewers; `tools/compound-eye/run_all.py` runs its existing focused suites.
The live observatory and its local recomputation server are preserved under
`projects/all_eyes`. They have their own data contracts and scope.

## Formal evidence

Read `PROOF_STATUS.md` before describing any result as Lean-verified. The
`formal/` module covers 16 finite algebraic declarations; the general scattering,
Gram and physical arguments have written proofs and numerical controls.

With the pinned Lean toolchain installed:

```bash
cd research/elemental_foundations/formal
lake update
lake build
lake env lean FalseControl.lean
```

The last command must fail on the deliberately false equality. The GitHub
workflow additionally runs `leanchecker` and an axiom audit. Compilation,
per-declaration scope and material calibration remain separate records.

## Source integrity and corrections

`sources/` preserves the actual Matter, Light, Sofic, UPG, FOFT, ladder and angle
editions and the supplied Gram diagram. `source_inventory.json` records their
bytes and SHA-256 hashes. The original hypersurface and color inputs are in the
preceding elemental project. The original authors' source claims are not all
endorsed: the paper explicitly corrects isotropy, range/Riesz, bundle base/scale,
Schur-sign and path-minimum overclaims. The later FOFT equilibrium corollary is
preferred to its overbroad abstract.

Zenodo access failed during preparation. Actual bundled editions are cited;
latest public DOI metadata is not claimed verified. The source inventory and
GitHub pins prevent that access limitation from silently changing provenance.
