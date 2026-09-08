from pathlib import Path
import shutil,json,hashlib,sys,importlib.metadata
p=Path(__file__).resolve().parent
shutil.copytree(p.parents[1]/'peel_progress/formal',p/'formal',dirs_exist_ok=True)
report=json.loads((p/'formal/evidence/report.json').read_text());h=hashlib.sha256((p/'formal/OpticalMetric.lean').read_bytes()).hexdigest();assert h==report['sha256']
(p/'formal/FRESH_STATUS.md').write_text('Source hash freshly matches archived CI report: '+h+'\n\nNo fresh Lean compilation was performed in this release. Archived report covers 16 declarations. New manuscript propositions outside that module have written proofs and computational controls, not new Lean certification.\n')
shutil.copyfile(p.parent/'complete_complex_k3_source/fresh_witness.log',p/'permutation_witness_fresh.log')
u=p.parents[2]/'upload';manifest=[]
for name in ['complete_complex_k3_source.zip','complete_complex_k3_permutation.pdf','matter_at_a_scale (2).html','Matter_v5_release.zip','compound_eye_modular_complete.zip','What_Transport_Keeps (3)(1).html','Ramanujan_Challenge_Proofs_02_08.pdf','LIGHT-CONSTITUTIVE-02.zip','SMITH-BOUNDARY-01.zip']:
 f=u/name
 if f.exists():manifest.append({'uploaded_name':name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size})
(p/'input_source_hashes.json').write_text(json.dumps(manifest,indent=2))
(p/'requirements.txt').write_text('\n'.join(x+'=='+importlib.metadata.version(x) for x in ['numpy','scipy','sympy','mpmath','networkx','matplotlib'])+'\n')
(p/'README.md').write_text('''# Peeling Cascades — research release 1

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
''')
(p/'Atlas_Cascade_Map.md').write_text('''# Atlas-to-cascade claim map

This is a focused integration map, not a claim that all prior results or historical recollections are correct. The present manuscript admits only links with an explicit observable and hypothesis set.

| Source / thread | Retained contribution | Boundary on its use | Evidence in this release |
|---|---|---|---|
| Earlier Paper 1 working section and LIGHT-CONSTITUTIVE-02 | Fixed amplitudes, nonnegative weights, kernel persistence, tune-out distinction | Relaxing amplitudes or signed interference leaves the positive-peel theorem | Exact new positive-peel controls; archived Lean source and verification report; existing optical eye rerun |
| Compound Eye and successive instrument extensions | Independent measurement and algebraic views; explicit blocking; version provenance | A registry entry is not a validated detector | All 150 earlier specification hashes preserved; 8 new implementations; 350 focused evaluations |
| Matter at a Scale, v5 | Compressed-projector boundary census; scale tracking | A two-sided census is not rank or electron number; external energy references must be tracked | New contraction counterexample, projector dilation, affine covariance checks |
| Complete-complex permutation source | Displacement Gram spectrum; support, scale, cycle type | Zero entropy does not imply transposition-only support; complete-complex vertex count is not an element label | Corrected general proof; 259 partition controls; supplied k=5..8 witness verifier rerun |
| What Transport Keeps, edition 3 | Keep the pairing and transport observable explicit | An arbitrary Euclidean norm does not replace a declared pairing | Existing pairing and nonnormality controls rerun; no new universal transport theorem asserted |
| Offset belongs to boundary / Smith boundary | Distinguish a retained boundary response from a chosen parametrization | A Schur reduction does not by itself identify a spatial hypersurface or conductivity | Nested Schur and boundary-resolvent tests; no new Smith-chart physical fit |
| Light ledger / electron-photon loop | Interference, response and recycling need separate bookkeeping | A dark response need not remove a degree of freedom | Existing optical and recycling controls rerun |
| Aharonov / Cheshire / modular translation | Preparation, postselection and phase can change a readout | A conditional weak readout does not certify constituent separation | Existing response controls rerun; not promoted to an elemental mechanism |
| Three-body pairing and skew hierarchy | Pairing degeneracy and nonnormality demand explicit conventions | This cascade does not assume every metric is positive or every operator self-adjoint | Existing cluster, pairing, normality and stress-composition controls rerun |
| APS / eta / twisted torsion / Alexander–Jones | Admission conditions before joining spectral and knot data | No derived atomic assignment or knot-volume potential; nonunitary representation is not automatically self-adjoint APS data | Existing Fox valid/corrupt, torus and APS admission controls rerun; not used as proof premises |
| Ramanujan and older Big Unknot / FKS material | Source of hypotheses to audit | No imported fit percentages, universal frequency, CN conflation or element–knot table | Excluded from evidential premises of the new paper |
| Gravity and cosmological ledgers | Broader research context | No gravity/CMB fitting is needed or performed | Outside the present empirical claim |

## What “peel” means in this paper

The proved peel is a decrease of nonnegative channel weights with fixed channel amplitudes. A coordinate peel is separately an exact elimination operation that keeps hidden influence in self-energy and memory. Electron emission and nuclear constituent removal remain separately specified physical interventions. They are not inferred from either mathematical definition.

## Next evidence needed

Select one prepared species and a resolved intervention. Obtain raw detector and calibration records, outgoing-channel or charge-state information, and time/frequency response data. Compare bare deletion, memory reduction and attenuation on the same held-out observable. Do not train a knot-to-element assignment and score it on the same elements. No existing synthetic pass rate substitutes for this test.
''')
