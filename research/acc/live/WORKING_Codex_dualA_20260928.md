# Codex Helper A two-eyes beam (2026-09-28)

- Assignment: 86 AC rows in `research/acc/live/targets_dual_helperA_20260928.json`.
- Began: 2026-09-28 14:11Z; machine: Codex 8 GiB cgroup, shared T8 hash `38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8`.
- Command: `BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 python3 research/acc/optimality/run_beam_raw.py SAIR/competition/tools/verifier/data/manifest.json bin work/T8.tab work/w_dualA 20000 600 work/dualA_cap.jsonl work/dualA_targets.json`.
- This lane is separate from Helper B and sender p2 lanes. Output is appended per completed row. A hit will be independently checked by the pinned SAIR official verifier before being placed in `research/acc/live/inbox/`. Sender session alone submits.
- Status at 14:12Z: both A and B beam processes running; no A row complete yet.

- Update at 14:17Z: first row ac-02818 exhausted in 169 s with no path. The 86 rows were split into first 43 (A1) and last 43 (A2) on the same 8-core machine, with identical search flags and separate work directories. The A1 output is `work/dualA_cap.jsonl`; A2 is `work/dualA2_cap.jsonl`. The original full-list process was interrupted after row one, and A1 resumed from that saved row. No rows overlap between active A1/A2 runners.

- Update at 14:51Z: A1 full exact windows unchanged; A2 after its tenth saved result restarted with identical beam flags and 180-second post-beam AC/SAC window caps only when the raw path is +4..+6 over record and value ≤0.125. On timeout it preserves the raw path and records `ac_window_timeout_s`/`sac_window_timeout_s`; this is incomplete polishing, not a negative proof. A2 processed ac-02454 at 52/54 versus 46/48 in 700s with no cut before the cap. A and B have 41 completed rows combined and still no qualifying line. Smith/Snell pilot logged separately in `ledger/smith_snell_pilot_20260928.md`.

- **Stopped at 15:00Z at user's requested checkpoint.** A1/A2 runners exited on interruption; no beam or window process remains. A completed 25/86: 20 `nopath`, five verified paths above live records, **zero ties or beats**. Last complete outputs are in `research/acc/live/sweeps/dualA_codex_20260928.jsonl` (13 A1 + 12 A2). Next incomplete A1 ac-01452, A2 ac-06134. Run lists and output JSONL resume without repeating completed rows. No inbox line, no SAIR submission. Helper B stopped separately at 24/86.
