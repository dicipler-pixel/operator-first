# Receiving-chat operating guide

1. Read START_HERE.md and research/QHE_Findings.md. Inspect catalog metadata before selecting a view. Do not infer goals or valid physics from a catchy label.
2. Verify `python run_all.py`. Report a failure honestly and fix executable code as a complete replacement. Never claim archived or supplied logs were freshly rerun.
3. Keep raw acquisition, calibration, processed populations, theoretical matrices, fitted quantities and physical interpretations separate. The exact provenance field belongs in every request.
4. Never flatten raw array coordinates into time without the acquisition map. Never fill unacquired combinations with zero-valued observations.
5. Reproduce the source authors' analysis first; document every adaptation. Apply new geometry or projector methods in a separate stage. A detector IQ covariance is not automatically a quantum state or its geometric tensor.
6. Identify the actual intervention: removal, attenuation, elimination, preparation change, threshold movement or coherent cancellation. For heat engines, declare system boundary, energy convention, reservoirs, control work, interaction energy and cycle closure.
7. Use the supplied `run_qhe.py` requests as complete per-method examples. Generic command-line use is available from `python machine.py --help`. Do not broadcast incompatible cases to a whole set.
8. For a new eye, keep a stable ID and explicit semantic version, include input units, assumptions, dependencies, output meaning and failure conditions, and register through Registry.add. The registry pins implementation bytes and forbids overwriting registered versions. Add a new version for changes; preserve historical files and logs.
9. Add a positive control and a meaningful failure/counterexample control. Exact identities, numerical tolerances, fitted performance and experimental significance are different evidence classes.
10. Do not turn the research goal into an assumed universal law. The current goal is to test whether reservoir-controlled channel dynamics predicts a specified cascade, and whether retained memory improves held-out predictions.

## QHE evidence status

Fresh: nine new eyes; 48 QHE evaluations including four expected blocks; raw completeness audit of 5,362,511 finite IQ pairs; partial calibration/population replay of 539 acquired cells; six population-generator cases reconstructed from published atomic-model rates; three processed experimental power points inspected.

Preserved: 350-evaluation peeling suite, older modular tools and Atlas content, earlier Lean module and CI evidence.

Not established: full source-notebook thermodynamic reproduction, new measured engine efficiency, universal quantum advantage, causal quantum memory from multiexponential decay alone, elemental removal law, or indefinite light output without energy input.
