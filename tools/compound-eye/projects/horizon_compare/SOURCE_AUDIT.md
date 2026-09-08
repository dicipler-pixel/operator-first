# Current source replay and qualifications

Python 3.12.13; NumPy 2.3.5; SciPy 1.18.1; SymPy 1.14.0; mpmath 1.3.0; NetworkX 3.5; Matplotlib 3.10.8. Actual per-file hashes, process exit codes, elapsed times and logs are in `runs/horizon/source_replay/manifest.json`. All twelve selected processes completed with exit code zero. That is an execution statement, not blanket validation of the papers.

| Supplied or recovered script | Fresh outcome | Interpretation |
|---|---|---|
| `bh_curv_01.py` | Kendall K≈4, symmetry, metric, interior finiteness, component wall laws reproduce | Components are not normalized invariant tidal magnitudes; new metric-speed re-expression recorded separately |
| `bh_ledger_01.py` | Rank-one Euclidean growth, count two for valid contours, Jordan trace-log residual pass | ε=0.1 intentionally misses the pair with radius .15; full grouped projector is I₂, with no added nilpotent part |
| `upg_gate_01.py` | Winding examples and 200 redistribution identity trials reproduce | Finite theoretical controls |
| `upg_gate_02.py` | Clock/shift, commuting and relator checks pass; 0/1000 random domain violations; d=2 refused | The branch refusal is a successful negative control |
| `upg_prove_01a.py` | 0/1000 curvature-bound violations; exact-model two-band saturation and 200 persistence checks reproduce | The rigidity example is synthetic |
| `upg_prove_02.py` | Stated lattice model and parameter scans execute | Coarse-grid near-gap values are not converged integer certificates; pointwise finite-difference saturation is imperfect |
| `dirac_spine_01.py` | Dirac ladder and random-matrix integral reproduce | Synthetic finite matrix plus published parameter; truncation produces a second zero mode, not a new measured mode |
| `bh_dynamo_01b.py` | Corrected onset, norm ladder, two-mode ledger reproduce | Full-domain phase-slope outputs do not by themselves prove a clean directional reversal |
| `shear_lane_01.py` | Tilt scan reproduces | Gains and positive-real resolvent values are sampled; NaNs mark intentionally skipped unstable-regime columns. PhiF is unnormalized |
| `n_recovery_01b.py` | One-loop exchange, two-loop return, winding and returning ledger reproduce | The chosen larger contour contains three modes at the tested phases; distinct from the separate two-mode ledger |
| `n_recovery_02_final.py` | Listed torus-knot/figure-eight finite signatures and inherited table inputs reproduce | Not a physical knot-to-Sun identification; its “k/7” staircase header is not a precise listing of the Alexander-root wall angles |
| `dkist_compare_02.py` | Width-convention and growth-rate arithmetic reproduce | Comparison to published summaries; no new data acquisition/calibration |

The black-hole scripts were recovered from printed Appendix B, with only formatting repairs documented in `sources/bh/RECOVERY.md`. The supplied UPG and Sun Python files are copied byte-for-byte. PDFs remain unchanged under `papers/`.

The Sun package also contains `bh_dynamo_01.py`, `sun_open_01.py`, `sun_open_02.py`, `sun_open_02b.py`, `n_recovery_01.py`, the figure-generation scripts and figure assets. These are preserved, but not all executed in this release. The UPG figure-generation script and every historical Eye project were likewise not all replayed. The original QHE/peeling focused suite did run. The earlier acquisition audit stored in Universal 2 remains historical evidence, not a fresh acquisition audit in this task.

Current new gates are in `runs/horizon/summary.json` and `exact_checks.json`. These address metric conventions, admissible continuation, observation nullspaces, two-sided response and contour membership. They do not replace the unperformed empirical and convergence tests listed in FINDINGS.md.
