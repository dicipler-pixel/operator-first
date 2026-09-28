# Codex Stable camera -> Session 2, 23:22Z

New reusable `tools/acc/ops/stable_finish_watch.py` checks every AC path in a beam JSONL for the shortest direct Stable finish, including early destabilization and inversion; it replays both AC and candidate SAC with the pinned official verifier and compares a Stable board snapshot. It reports candidate lines but does **not** submit. Example:

```bash
python3 tools/acc/ops/stable_finish_watch.py \
  --manifest SAIR/competition/tools/verifier/data/manifest.json \
  --board work/stable_board.json.gz \
  --sweep research/acc/live/sweeps/codex_mirror_20260928T230855Z.jsonl \
  --out work/stable_candidates.jsonl
```

On the 80-row mirror sweep (36 AC paths), it found precisely sac-05818 already sent in 2701 and **sac-09839 at 46** now in `inbox/20260928T2312Z_codex_sac-09839.txt`; raw results in `sweeps/codex_mirror_80_stable_hits_20260928.jsonl`. For future AC sweeps, run this per checkpoint so a Stable partner isn't missed. Check `SENT_ROWS.txt` and the live board before sending.
