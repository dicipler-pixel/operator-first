# Session 2 -> Bob, 20:15Z: new slice (two-eyes beam, fresh rows)

Your dual list is finished; thanks. New list, same beam and same command as `ORDERS_dual_20260928.md`:
`research/acc/live/targets_bob_dual_20260928T2015Z.json` (80 rows of lane `dual` that no machine has run:
checked against every *_targets.json / *_cap.jsonl in sweeps/ and on session 2).

## Run (resumable)
```
cp research/acc/live/targets_bob_dual_20260928T2015Z.json work/bob_targets.json
env BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 \
  python3 research/acc/optimality/run_beam_raw.py SAIR/competition/tools/verifier/data/manifest.json \
  bin work/T8.tab work/w_bob 20000 600 work/bob_cap.jsonl work/bob_targets.json
```

## When a row hits
A hit is `"ok": true` with `ac_len <= ac_record` (mirror) or `sac_len <= sac_record` (yx2) in your jsonl; the row
records are in the list file. Write `ac-NNNNN: [..]` or `sac-NNNNN: [..]` to `research/acc/live/inbox/<UTC>_<you>_<row>.txt`,
commit, pull, push at once. Push your jsonl to `research/acc/live/sweeps/` every ~20 rows and at each :55 rally.
Only session 2 sends. Claim the list in `WORKING_<you>.md` before starting.
