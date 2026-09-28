# WORKING — Fable (2026-09-28 20:45Z)
- Lane: (y,x) lane, slice `targets_yx_fable_20260928.json` (200 rows), per `ORDERS_fable_yx_20260928.md`.
- Running: `tools/acc/ops/twin_beam.py <row> 20000 <sac_record-2>` with BEAM_H=1 DIV=0.8 P2=2 QUOTA=16 ELITE=5000 DUAL=0.75 TWIN_MODE=yx, T8 (hash 38f05b56...).
- Output: work/yx_fable.jsonl -> sweeps/yx_fable_cap.jsonl every ~25 rows; hits -> inbox at once.
- Machine: 2 cores, 8 GB. One process.
