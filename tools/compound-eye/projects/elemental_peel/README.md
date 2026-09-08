# Elemental Peel Observatory

Open `Elemental_Peel_Observatory.html` directly in a browser. No server is needed. Thickness, substrate, optical-fit controls and electronic orientation recompute immediately. The simulation is not a live experimental feed.

Read `FINDINGS.md`, then `METHODS.md` and `Elemental_Peel_Paper_Section.md`. The static figure is `Elemental_Peel_Findings.png`.

From this directory, with Python 3.11+:

```bash
python -m pip install -r requirements.txt
python run_study.py
python extend_observations.py
python build_artifacts.py
python check_viewer.py
```

Node.js is required only for `check_viewer.py`. NumPy 2 or later is required for trapezoid integration. Inputs are bundled for offline reproduction; `fetch_data.py` is optional source retrieval, and its recorded NIST HTTP failure is not repaired by inventing data. The NIST transcription is already included. The original recovered color script has its own historical dependency record in `sources/requirements.txt`.

This supplement contains the current registry and installed scientific implementations, plus the complete elemental study. It preserves all 191 prior definitions and adds seven; it does **not** include every older project's raw dataset or replace the full Universal archive. Reproduce the elemental commands above. Consult the master GitHub repository for the whole project and other suites.

`sources/` contains recovered original inputs. Re-running the extracted historical hypersurface verifier can overwrite its local historical output; the original ZIP preserves the supplied version. The registry's installed plugin is content-addressed and immutable; new scientific behaviour requires a new registered version.

The study's useful unanswered question is physical: which geometry-controlled sequence of a specified element simultaneously explains conductance, noise, energy-dependent response and optics? The supplied controls show why one scalar response cannot answer that by itself.
