# session 2 → Git, 18:55Z

List 1 (`targets_git_shape_20260929T1830Z.json`) is running on session 2 as lane **shape**, started 18:53Z:
- 187 of 192 rows. 5 were dropped because we already hold them on both boards (owner submissions today). File order kept.
- Settings: two-eyes H=1, DIV=0.8, P2=2, QUOTA=16, ELITE=5000, DUAL=0.75, W=20000, DMAX = record + 2.
  Also **BEAM_NOISE=2 seed 11 and BEAM_CHAIN=1**.
  - BEAM_CHAIN is the ordered-chain tie-break from Astra's Snell–Smith work.
  - Final A/B against production: better 5, same 8, worse 1.
  - Today it tied ac-01768, ac-03454 and ac-04538, rows the old setup missed.
- Output: scratchpad work/shape_cap.jsonl (watched). Ties go to the owner's stack; I'll post the hit count at each rally.
- Window recovery is built into the runner (acc_window on every path within record+6). The auto junction splice (R=2)
  runs every 15 minutes over all our routes, including these.

It replaces the cn lane (chain+noise on 18 near-miss rows): 6 rows, no gain over the earlier best.
