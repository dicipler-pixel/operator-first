# HYPERSURFACE-TESTS-01

Controlled tests of the inside/surface/outside light model, electronic response,
charge neutrality, nonlinear Hall bias, photon geometry, and a candidate rigidity
identification. The original Beasley manuscripts are not modified.

Start with **proof_note.md**. The raw record is **checks/output.txt** and
**checks/results.json**. All 328 independent assertions passed in this runtime.
These are written proofs plus symbolic/model calculations, not experimental data.

## Lean status

**22 candidate declarations; zero compiled or kernel-certified here.**
The runtime has no Lean/Lake, and toolchain download attempts failed at DNS.
See checks/lean_status.json, checks/lean_checks.log, checks/environment_attempts.json.
Do not cite the candidates as formal certificates. They may contain elaboration
or API errors that only the real compiler will expose.

## Reproduce mathematical checks

Python 3.10+ with numpy, scipy, sympy:

    python checks/run_tests.py

No input file editing is needed. It writes its results beside itself.

## Actual Lean build

Install Lean's `elan`/`lake` tools in the execution environment. The project pins
Lean and Mathlib v4.19.0 for compatibility with the earlier offset proof project.
Then, from this folder:

    python verify.py --setup

This obtains pinned dependencies/cache, builds all modules, audits the axioms of
all declarations, and tests two deliberately false controls. Without `--setup`,
the script uses already present dependencies. Add `--math` to replay the model
checks as well. A Windows launcher and a Unix launcher are included.

Success requires all stages. A static scan is not a proof. A compiler error in a
negative test does not count unless positive modules compiled and the negative
failed as an unsolved mathematical goal, rather than missing infrastructure.
Axiom dependencies are restricted to propext, Classical.choice, Quot.sound.
No native_decide, custom axioms, or unfinished proofs are permitted.

## Formalization coverage

Hall.lean: 10 real polynomial/inequality results, including exact power balance,
field expansion, incremental positivity conditions, and a negative witness.
Boundary.lean: 5 rectangular complex-matrix identities, including the two-sided
harmonic lift, frame covariance, and second-frequency boundary equation.
ScopeControls.lean: 7 scalar consequences with explicit domain hypotheses and
counterexample controls.

Not formalized: continuum waveguide convergence, Berry-dipole integrals, general
spectral theory, microscopic material parameters, or any gravitational field
identification. The neutral-metric scalar lemma does not purport to encode the
entire Dirac model; its relationship is derived in the written note.
