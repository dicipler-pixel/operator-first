# Compound Eye Universal 3.0

This is the complete Universal 2 instrument plus the current Sun, black-hole and UPG comparison. **All 167 previous eye versions remain; 11 new ones bring the catalog to 178 versions in 27 sets.**

Open `START_HERE.html` for the offline dark-background portal. Begin with the Boundary lab and New findings tabs. The original catalog, Otto-cycle lab, QHE findings, source datasets, Atlas and prior projects remain included.

Read `projects/horizon_compare/FINDINGS.md` for the mathematical findings and physical limits. Read `projects/horizon_compare/MANUAL.md` for the build, reproducibility instructions and extension contract. The self-contained `projects/horizon_compare/Horizon_Comparison_and_Manual.html` combines the report and manual with readable offline equations.

## Current result

The black-hole paper's own quotient metric makes its stated principal-frame transport block self-adjoint. Its rank-one projector norm is one in that metric, despite growth in its coordinate Euclidean norm. A signed Jacobi lift supplies an explicit finite-length path through the coplanar wall, and a regular limiting transport matrix. A divergent coordinate component therefore does not establish an infinite barrier. The oscillator velocity-suppression claim also needs an additional normalization assumption.

The new observation eyes exhibit different interiors with the same exterior signal in a finite one-way model. They track practical noise resolution separately from algebraic rank. The Schwarzschild comparison predicts inside-horizon ray directions in its declared classical model; it does not infer a real hidden interior or let a message escape.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run_horizon.py
python run_all.py
python projects/horizon_compare/replay_sources.py
```

The first command installs dependencies when needed. The new suite has 86 individual eye evaluations and one four-eye concurrent frame, 13 expected refusals, 165 assertions and 9 exact symbolic checks. `run_all.py` includes the existing QHE and peeling suites. Source replay covers twelve selected current-paper scripts. Full historical source/data and archived results are preserved but are not all newly rerun.

Results: `runs/horizon/`. Current papers and runnable sources: `projects/horizon_compare/papers/` and `sources/`. Prior top-level portal and instructions: `preserved/universal_2_portal/`. Original bytes changed by replay or editing are retained under `preserved/universal_2_original_changes/` with an archive inventory. Registered eye definitions and implementation histories remain immutable.

No new Lean formalization, calibrated solar inversion, Kerr model, physical shape-to-horizon map or observed black-hole interior is claimed. This research state supersedes the former active QHE-only task while preserving that project intact.
