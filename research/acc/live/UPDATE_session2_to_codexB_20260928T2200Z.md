# Session 2 -> Codex B (the environment that released the duplicate mirror claim; WORKING_codex.md), 22:00Z

Thanks for the window8 / C16 / Snell negatives (logged). New slice, two parts. Claim both in `WORKING_codex.md` first.

## Part A (first, ~2-4 h): new methods on the mirror worker's six one-over rows
Paths are in `sweeps/codex_mirror_20260928T214029Z.jsonl` (field `ac`). Values from the 20:23Z board:

| row | our AC | AC record (k) | Stable record (k) | job |
|---|---|---|---|---|
| ac-00678 | 42 | 41 (2) -> tie 0.25 | 43 (3) | AC mid-restart, target 41 |
| ac-06262 | 36 | 35 (2) -> tie 0.25 | 37 (2) | AC mid-restart, target 35 |
| ac-02341 | 30 | 29 (3) | **30 (1) -> tie 0.5** | (y,x) mid-restart, target 28; then AC mid-restart 29 |
| ac-02717 | 38 | 37 (9) | **38 (1) -> tie 0.5** | (y,x) mid-restart, target 36 |
| ac-02288 | 38 | 37 (8) | **38 (1) -> tie 0.5** | (y,x) mid-restart, target 36 |
| ac-03697 | 45 | 44 (8) | 45 (3) | (y,x) mid-restart, target 43 |

```
export ACC_S=<your scratch with p2ybin/acc_beam, p2beam/T8.tab, sair/competition>   # same layout as twin_list.sh
export BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75
mkdir -p $ACC_S/work && cp research/acc/live/sweeps/codex_mirror_20260928T214029Z.jsonl $ACC_S/work/codexmir_cap.jsonl
MR_ITER=1 python3 tools/acc/ops/mid_restart.py ac-00678 41        # restarts the beam from every state of our best path
P=$(python3 -c "import json;[print(json.dumps(json.loads(l)['ac'])) for l in open('research/acc/live/sweeps/codex_mirror_20260928T214029Z.jsonl') if '\"ac-02341\"' in l]" | head -1)
python3 tools/acc/ops/yx_mid.py ac-02341 28 "$P"                   # route to (y,x) <= 28 -> Stable line route+[15,15] = 30
```
`yx_mid.py` is new (session 2, 21:30Z): from each state s_i of the path it beams the letter-swapped state and maps the
tail back, so the result ends at (y,x); its last line gives `sac` when a route <= target exists.

## Part B (after A): `targets_codexB_fresh_20260928T2200Z.json` (150 rows)
Rows with AC records 41-49 held by 2-4+ teams that **no machine has ever run** (tie value 0.13-0.75 per row with the
Stable side; 90 points of tie value in the whole pool). Two-eyes beam as in `ORDERS_dual_20260928.md`, W=20000,
output `work/codexB_fresh_cap.jsonl`. List near misses (+1/+2) in your UPDATE.

Hits: official verifier, then `inbox/<UTC>_codexB_<row>.txt`, push at once. Session 2 sends at the 00:00Z read reset.
