# Operator-first research master

Jeromie N. Beasley’s current research directory: **13 projects**, **18 Atlas cards**, and **Compound Eye Universal 3.2**.

Start with [current project status](MASTER_STATUS.md), the [paper register](catalog/README.md), or the [reusable-results Atlas](atlas/README.md).

The [complete instrument](tools/compound-eye/START_HERE.md) contains **191 eye versions in 29 sets**: 172 implemented, 17 specified, and 2 archived results. It combines the independent Universal 2.2 and 3.1 lines with Eye Mixer 1.0.0.

## Use or share the tool

Download this repository and open `tools/compound-eye/START_HERE.html`, or build the standalone package with `python scripts/package_compound_eye.py --output release-output`. The full scientific replay command is `python tools/compound-eye/run_all.py` after installing its requirements; Node.js is needed for the mixer checks. The HTML works offline. The package builder restores the large raw dataset automatically from checked repository pieces. For a raw-source audit directly in a clone, first run `python scripts/restore_large_files.py`.

The [original 3.1 upload backup](backups/2026-09-08-universal-3-1/README.md) and [earlier complete backup](backups/2026-09-08/README.md) preserve both release lines. Every registered source definition and installed implementation is retained.

## Research and proof scope

The root build incorporates the repair from PR #1 and checks its finite core. The [source snapshot](catalog/source_snapshot.json) records exact heads and available workflow evidence for the other proof branches. Their independent status and mathematical limits remain explicit in the register. A successful instrument integration does not establish new physical calibration or solve the six Diophantine equations.

## Keep the master current

Read [AGENTS.md](AGENTS.md) and [catalog policy](catalog/POLICY.md). Fetch branches before importing another chat’s work; compare source inventories, then add missing versions without rewriting existing ones. Run `python scripts/build_catalog.py`, `python scripts/validate_catalog.py` and `python scripts/verify_compound_eye_release.py` after relevant changes.

The register remains a partial inventory of the wider 20+ paper corpus. Unresolved publication identities and missing source material remain in the intake queue.
