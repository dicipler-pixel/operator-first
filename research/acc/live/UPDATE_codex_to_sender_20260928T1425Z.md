# Codex + Helper B status for sender session (2026-09-28 14:25 UTC)

- Following `ORDERS_dual_20260928.md`: A and B have disjoint sets of 86 high-value AC rows each, records 41–52. Neither helper submits; verified hits go to `research/acc/live/inbox/` for the sender.
- Shared T8 table built locally and SHA-256 matches the order: `38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8`.
- Exact flags: `BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75`, width 20,000, depth 600, T8 finish, window shortener. Each helper split its 86 into two disjoint 43-row shards. Four processes active; cgroup was about 5.3 GiB of 8 GiB at the last check.
- Completed so far: A 6/86, B 5/86; **0 qualifying ties or beats; 0 lines for submission.** AC ac-04882 reached 54 moves against record 51 (SAC 56); shortener did not improve it. The other completed rows produced no path within the search settings.
- B2 is currently window-shortening a 50-move route for ac-03404 (record 45); it will be checked and uploaded if it reaches a record. The four lanes continue. A raw outputs: `work/dualA_cap.jsonl`, `work/dualA2_cap.jsonl`; B raw outputs: `helperB/work/dualB_cap.jsonl`, `helperB/work/dualB2_cap.jsonl`. These are local until the 20-row checkpoint or a hit.
- Working claims: `WORKING_Codex_dualA_20260928.md` and `WORKING_codex_helperB_20260928.md`.

## Follow-up 14:52 UTC

A 21/86, B 20/86; neither has a tie or beat. Raw checkpoints are `sweeps/dualA_codex_20260928.jsonl` and `sweeps/dualB_codex_20260928.jsonl`. Four lanes continue. We capped only low-value (+4..+6) post-beam windows to 180 s; raw paths are retained and timeouts marked. Smith chart and Snell-style routing pilots are logged in `ledger/smith_snell_pilot_20260928.md`: the tested Smith third eye tied one baseline and worsened another; the tested empirical Snell term weakened move ranking. Production dual beams were not changed.

## Final stop checkpoint 15:04 UTC (user request)

- All four Codex helper beam processes are stopped; A completed **25/86**, B **24/86**, combined **49/172**. A: 20 no-path, 5 above record. B: 21 no-path, 3 above record. **Zero ties/beats; no inbox lines and no SAIR submissions.** A's next incomplete rows are ac-01452 (A1) and ac-06134 (A2); B's interrupted rows and partial ac-06990 raw path are logged in `sweeps/dualB_codex_interrupted_20260928.jsonl`. Completed output persists in `sweeps/dualA_codex_20260928.jsonl` and `sweeps/dualB_codex_20260928.jsonl`, so both lists can resume without repeating complete rows.
- Tested the user's upside-down map: complete exact reverse BFS at total-length caps 2–10. The cap-10 identity component has 169,992 literal ordered states; cap 11 was **incomplete** at 500,001 seen. A length-7 pair's shortest confined route needs 7 moves at peak 7, while its globally shortest 4-move route peaks at 8; `D₂(2)=5` under the exact 14-move ordered convention. Pinned-core paths and all counts are in `ledger/reverse_ceiling_pilot_20260928.md` and `ledger/reverse_ceiling_profile_20260928.json`. These are synthetic states, not qualifying challenge submissions.
- Smith/Snell feature pilot remains a negative result on the tested arms. An additional matched ac-04882 Smith third-eye run tied the baseline at 54/56, above the 51/53 record; no production change.

## Charlie ZIP imported at 15:27 UTC

- Full text handoff is committed at `f20ab81b56580436af7495ada913a6e17a6297b2`: disk BFS C++/Python, exact-run ledger/logs, 540 chain routes, source candidate files, local controls, and `CHARLIE_HANDOFF_CHECKPOINT_20260928.md`. Source ZIP SHA-256 `31ba2e4f7ad1010989f60f0161bcac618017f1954c1f9315931da5addb5cb760`. Seven Python path fixes make the helpers portable; C++ unchanged.
- All four supplied candidate paths and all 540 chain paths pass an independent pinned official-core replay. The 15:13 UTC board snapshot changes Charlie's older beat/tie labels: **ac-02528 35 is now a tie (record 35, k8)** and is the only active inbox line, `inbox/charlie_ac-02528_tie35.txt`. ac-03719 37, sac-02528 37 and sac-03719 39 are behind by 2, 1 and 3 respectively, so they are archived outside the inbox. The 56 chain ties were already sent at equal/better lengths; 484 chain lines are behind. Recheck live board before sending the one tie.
- Engine compiled locally: 1,428 move checks, exact cap-10 identity layers (169,992), and ac-00738 cap21 closure (189,944) match official controls; Charlie's ported xcheck also reports 56,056/56,056. His deeper 533M-state run and large negative searches are represented by logs without their full frontier files. The missing radius-9 B36 ball and T16 table must be rebuilt before continuing his lane. No search resumed or SAIR line sent from this checkpoint.
