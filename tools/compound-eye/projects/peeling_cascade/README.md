# Peeling Cascades — research release 1

Read `Peeling_Cascades.pdf` or the standalone `Peeling_Cascades.html`. The canonical manuscript is `Peeling_Cascades.tex`.

## Reproduce the focused instrument run

Python 3.11 or later recommended. In the extracted folder:

```sh
python -m pip install -r requirements.txt
python run_cascade.py
python make_figures.py
```

The script resolves paths relative to its own location. No GitHub checkout is needed. Its expected result is 350 evaluations: 347 successful, 3 expected blocks, all assertions passed. Eight new implementations are registered alongside 150 preserved eye specifications. Historical registry membership does not mean every older proposal is executable. Inputs and outputs are fully recorded in `cascade_runs.json`; all inputs are synthetic or theoretical, not raw atomic measurements. Random seed: 20260907.

To rebuild the PDF with TeX Live and the listed LaTeX packages:

```sh
pdflatex -interaction=nonstopmode -halt-on-error Peeling_Cascades.tex
pdflatex -interaction=nonstopmode -halt-on-error Peeling_Cascades.tex
```

## Evidence levels

- Exact rational: positive-channel ranks and nullspaces; finite moment certificates; one symbolic nested Schur identity.
- Written general proofs: the four numbered manuscript propositions.
- Floating-point controls: resolvents, time convolution, permutation spectra, tomography, projector dilation, affine covariance. Assertion tolerances appear in the runner.
- Archived Lean: 16 earlier declarations, source hash freshly matched; no new local compilation.
- Experiment: no raw measurement fit, no constituent assignment, no established advantage over experimental or computational competitors.

`Atlas_Cascade_Map.md` explains the use and limits of prior projects. `permutation_witness_fresh.log` records an additional rerun of the supplied k=5..8 gauge-minimization witness verifier; it is distinct from the 350 eye evaluations. Input source hashes identify uploads, not a claim that every paragraph of every old paper was independently verified.

The new methods are narrowly scoped research controls. Shape and domain validation is not yet a complete hardened API; use the supplied well-formed cases or validate new inputs carefully. Formal-project dependencies are configured in `formal/`; installing Lean and mathlib is a separate operation from the Python run.
