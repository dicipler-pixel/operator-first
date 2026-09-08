# Compound Eye Universal 2.0

Owner: Jeromie N. Beasley. Research snapshot: 7 September 2026.

This is the complete shareable instrument, not a patch. It contains the current registry, implementations, original modular release, prior nested tools, the peeling paper project, nine new QHE eyes, two source datasets with attribution, execution records, and the handoff guide below. “Universal” means extensible across declared domains; it does not mean every physical hypothesis is covered or validated.

## Give this to another chat

Upload the complete ZIP and say:

> Extract this Compound Eye package. Read START_HERE.md, CHAT_HANDOFF.md and research/QHE_Findings.md. Run run_all.py if Python execution is available. Preserve existing eye definitions and histories. Select relevant eyes using the catalog; add new versioned eyes when needed. Report which calculations actually ran, distinguish source measurements from models, and do not treat registry membership or an old assistant statement as proof. Use the instrument on the problem I give next.

The standalone START_HERE.html is an offline catalog and live, labelled two-level Otto model. It includes the research report and original eye definitions, but does not execute the Python plugins or contain the large raw files. Share the ZIP to transfer the full tool. If a receiving chat cannot execute code, it must say so and can still inspect the contracts and evidence.

## Ready-to-run commands

```sh
python -m pip install -r requirements.txt
python run_all.py
```

This runs the current QHE and preserved peeling suites. It does not replay every old project. It requires no GitHub checkout. Scripts resolve their files relative to their own location.

To repeat the raw source audit and the seeded partial population replay:

```sh
python -m pip install -r requirements-data.txt
python audit_sources.py
python run_all.py
```

The two deposits are included as ZIPs under data/. The audit script extracts them automatically. Repeating the source audit uses additional disk space and performs ten million Monte Carlo calibration samples for each of four fitted Gaussian components. It does not execute the authors' full Qutip simulation or certify new efficiency values.

## Where things live

- START_HERE.html: standalone searchable eye catalog, literature findings and live illustrative Otto-cycle controls.
- catalog/: immutable registered definitions, version histories, sets and pre-QHE hashes.
- machine.py: dependency-aware Python dispatcher and validation.
- extensions/qhe_eyes.py: nine new QHE implementations; pinned installed copies are under plugins/installed/.
- run_qhe.py: complete example requests and expected rejection tests.
- research/: source-backed audit, findings, data/model distinctions, all 539 acquired-cell population records.
- projects/peeling_cascade/: complete paper and its instrument snapshot, source, scripts, figures and archived Lean evidence.
- preserved/original_modular_release/: original modular distribution and all its nested preserved tools.
- preserved/original_upload.zip: the originally uploaded modular ZIP, byte-for-byte.
- data/: the two original CC BY 4.0 scientific deposits and metadata.
- runs/: current QHE records and combined verification.

## Limits that matter

A successful eye calculation is a result under its input contract. It is not an independent vote for a theory. A specified eye has no executable implementation. Archived results are historical evidence, not freshly rerun calculations. The QHE set names a collection of methods; use run_qhe.py to supply method-specific cases. The case contracts differ, so one arbitrary input must not be broadcast indiscriminately to all nine methods.

The new readout diagnostic highlights a calibration-map question; it does not publish a corrected thermodynamic result. The raw NetCDF padding pattern is not a temporal memory gap. A Markov ladder can have many relaxation times. A one-way heat discharge is not a closed engine cycle. Unitary extractable work is not the same as total energy. These distinctions are recorded in the eye outputs.
