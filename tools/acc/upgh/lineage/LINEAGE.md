# UPG-H lineage

Each version is kept as received. Later versions are added beside earlier ones and never overwrite them.

| Version | Author | What it is | Where |
|---|---|---|---|
| v0 | Jeromie + Grok | *UPG-H v0 — Harness Map*: typed objects (Π, M, g, Z, Φ/F, τ̇, grades), runtime loop, refusal rules, observation R, failure species S1–S4, pass-around questions | `UPG-H_v0_harness_map.md` (pasted in chat 2026-09-30, stored verbatim) |
| v1-note | Astra | DeepSeek Harness (`dsh`) reading and role split (Sol / Luna / Astra / checker / code), plus the new idea: every failed attempt gets a reopening condition | `astra_dsh_note.md` (pasted in chat 2026-09-30, stored verbatim) |
| v1 | Astra | *ACC Memory-First Harness v1*: SQLite controller, leases, four role prompts, pinned-checker gate, board eligibility, reopen on wake, 46 tests, toy demo | `astra_v1/` (extracted from the uploaded ZIP; all 27 `SHA256SUMS.txt` entries verified on 2026-09-30) |
| v2 | Claude | *UPG-H v2, Claude edition*: bound to the real SAIR manifest, the pinned official verifier, the live board and this repo's history | `../` (this tool) |

## Upload identities

| File | SHA-256 |
|---|---|
| `ACC_Memory_First_Harness_v1_20260930.zip` | `ebb15e565d4dd439c35e6c70a5ade9e57f7f05d19a640b3bccb821f22c35b3e6` |
| `ACC_Harness_Start_Here_20260930.html` (identical to `astra_v1/START_HERE.html`) | `37f3a74b6b4f8d9712b045797fff4ea9e05ead80d75efdbf94edb312534e4e86` |

Astra's `source_map.json` refers to paths in Astra's own workspace. Those paths are kept as written. They are not files in this repository.

Astra v1 still runs unchanged: `cd astra_v1 && python3 selftest.py && python3 demo.py` (46 tests passed and the six-stage demo completed on 2026-09-30).
