# UPG / cascade integration

Read [the integration report](UPG_Cascade_Integration.md) and [the source manifest](input_manifest.json). This folder provides a standalone diagnostic module and its controlled tests. Original author source programs in `source/` and their execution logs are retained with explicit scope; the original UPG manuscript and raw QHE deposits remain in the portable release.

Run:

```sh
python -m pip install numpy scipy sympy
python research/upg/verify_upg.py
```

The 213 cases include seven expected refusals. This is not a new Lean proof or a physical fit. The original figure script retains its author-local output path; use the portable release's replay helper for figures. The missing three-body helper is documented in the report.

For current GitHub metadata:

```sh
python research/upg/refresh_github.py --output github_live.json --compare research/upg/github_snapshot.json
```

The refresh is read-only. A changed commit needs its own proof and data review. It is not a background monitor.
