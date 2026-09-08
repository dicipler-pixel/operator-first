# Compound Eye — First modular instrument build

Jeromie N. Beasley · Operator-First Atlas · 7 September 2026

Open `START_HERE.html` after extracting this ZIP. The complete dark-navy manual is
`BUILD_MANUAL.html`. Both work offline. The original sixteen-eye viewer is linked
from the console and preserved inside this package.

This release registers 91 eye definitions in 18 sets: 80 implemented calculations,
two archived-result readers, and nine specified extensions. These are connected
readouts and operations, not independent measurements. Every located prior eye and
source snapshot is retained. The preservation manifest covers 1,080 files.

## Run the build

Python 3.11 or later; verified with Python 3.12.13. From this folder:

```bash
python -m pip install -r requirements.txt
python run_project.py
python tests/test_machine.py
python machine.py verify-preservation
```

The first command obtains the three pinned numerical dependencies. With those
installed, these computations need no network, GitHub account, or hosted service.
Fifteen example jobs and their recorded outputs are included. The current run has
80 successful eye executions, one intentional missing-data result, and no errors.
The 34-test verification log is included under `tests/`.

Windows S mode may prevent installing Python. The HTML manual, saved records, and
browser instruments can still be read locally without changing that setting.

## Select one or several compatible sets

```bash
python machine.py catalog
python machine.py run requests/quantum.json --sets ce.set.quantum@1.0.0
python machine.py run requests/nuclear_boundary.json --sets ce.set.nuclear_boundary@1.0.0
python machine.py run requests/operator_boundary.json --sets ce.set.operator_boundary@1.0.0
```

Run records are added under `runs/`; `latest_project_index.json` is a convenience
index, not a replacement for those historical files. `run_project.py --only
quantum operator_boundary` selects example jobs. The engine accepts a JSON request
on standard input when the request path is `-`.

## Add an eye without replacing an older version

The following complete extension is deliberately not preinstalled in the main
catalog, so you can try the public installation interface:

```bash
python machine.py add-eye examples/extensions/range_eye.json --code examples/extensions/range_eye.py
python machine.py add-set examples/extensions/range_set.json
python machine.py run examples/extensions/range_request.json --sets ce.set.example_range@1.0.0
```

Its expected output is minimum 1, maximum 7, range 6. A second registration of the
same ID and version is refused. Improvements use a new version; older code and
sets stay available. The norm-balance eye in this release was itself added through
this mechanism. Register with one writer at a time and retain dated project copies.

`python build_manual.py` regenerates the HTML pages using the standard library.
The appended catalog and set list reflect the registry; the narrative and delivered
verification statements document this first release. Retest and revise those
statements when publishing a changed release. The optional scientific chart can be
regenerated with `pip install -r requirements-figures.txt` and
`python build_charts.py`. Chart SVG is already included.

## Scientific scope

The new sets calculate finite projection identities, a solvable outgoing-channel
response, additive charge and planar winding, operator deformation responses,
calibration covariance, and scalar norm balance. Nuclear demonstrations are model
calculations. No raw He-5 or Be-8 event data were acquired or fitted. A field-defined
nuclear invariant and a physical relation from that invariant to channel coupling
remain research tasks. `raw_inputs/nuclear_requirements.json` records the next data
requirements.

The preserved Earth–Moon and arithmetic Kakeya calculations retain their precise
finite scopes. The full Epoch problems remain open. Existing written and Lean
materials are preserved; this build adds no new Lean formalization and does not
claim every historical workflow was rerun.

## Reproducibility and preservation

`RELEASE_MANIFEST.json` lists the bytes and hashes of the packaged files, excluding
itself. `preservation_manifest.json` maps each preserved file to its original
snapshot and hash. `catalog/history.jsonl` and `catalog/set_history.jsonl` track
registrations. The runtime checks registered definitions and plugin source hashes.

These records detect changes relative to a saved copy; they are not detector
authentication, distributed consensus, or a substitute for backups. Original
attribution and any existing source license notices stay with preserved files.
This bundle does not relicense those sources.
