# Finite certificates for the combined elemental and hypersurface paper

Run `python3 run_lean_checks.py` after installing elan (Lean version manager), Git and Python 3. The runner uses the shipped Lean/mathlib pins: 4.19.0 for the recovered hypersurface library and 4.33.0 for the optical/elemental libraries plus the new `PauliMemory` file. It downloads official mathlib cache files, compiles the positive libraries, prints axioms for every named theorem, and demands rejection of all five deliberately false controls.

`PauliMemory.lean` contains 17 finite algebraic theorems: complex two-orbital Gram/exclusion identities; a declared common-coordinate delayed-response model and its prediction obstruction; the two-level box equilibrium cube ratio and strict size increase; a synthetic metamer/filter witness; and the force-memory/quantum-metric coefficient identity and positivity.

The proof statements explicitly delimit physical scope. They do not certify the derivation of a microscopic element, an optical force, an ODE solution, geometric phase, Maxwell's equations, numerical code or the identification of observer color with a quantum metric. The box lemmas assume stationarity equations derived separately by calculus. The force-memory lemma checks the coefficient identity after its physical definitions have been supplied. Standard dependencies are formal certificates, not claims of new laws.

Original source comments saying `uncompiled candidate` are preserved as provenance. Only a successful fresh report supersedes that status. Runtime binaries and mathlib caches are deliberately excluded from this source deliverable.
