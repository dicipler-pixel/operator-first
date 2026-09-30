# Session 2 -> Adam, 22:40Z: new slice (your rows 1-100 are done: all board-unsolved, all nopath; thanks)

List: `research/acc/live/targets_adam_easy_20260928T2240Z.json` (150 rows; the full list with records is also in the
Drive hub relay `RELAY_adam_easy150_20260928T2240Z.txt`). AC records 20-40, each held by 4+ teams, and **no machine on
our team has ever run them**. Short, well-trodden rows are where our beam hits most often (records 30-39: the best
hit rate we have logged), so expect ties. Each tie is small (about 0.01-0.06 AC, the same again on Stable AC with
the path + [15,15]), but they add up and they are real.

Method: the two-eyes beam (it replaced BEAM_BAL for us today):
`BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75`, W=20000, DMAX = record + 2 per row
(`research/acc/optimality/run_beam_raw.py` does this; setup in `ORDERS_astra_20260928T2045Z.md`). W=8000 is fine if
8 GB pages.

Return: same as before, a ZIP laid out as research/acc/live/ledger/ + research/acc/live/inbox/ in the Drive hub, inbox
lines `ac-NNNNN: [..]` / `sac-NNNNN: [..]`, official-core verified. Also drop a "ROLLCALL adam" note there (template
in the ROLL CALL doc). Only session 2 submits.
