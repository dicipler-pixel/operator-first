# Bob job 3 final (cross-class transfer of our 946 best paths): Git's check, 2026-09-29 16:50Z

- **All 173 lines pass the official core** (ac-r2-v1). Sections: A 2, B 46, C 125.
- Compared against boards ac_20260929T1145Z and stable_ac_20260929T1126Z (the newest on the branch) and against SENT_ROWS:
  - **A (ties):** ac-01618 41 = record (k7). We already hold this at 41, so no change.
    ac-04416 29 = record (k12). This is new for us (we sent 48). It is already in inbox/20260929T1330Z_bob_04416.txt
    with sac-04416 (31 = SAC record, k10).
  - **B and C:** every line is above the record. 0 beats, 0 ties, 0 first solves.
    B lines improve our own path. C rows had no path in our bundle; their first paths come from Bob.
    Gap over record: 1 over on 5 rows, 2 on 1, 3 on 3, 4 on 6, and a long tail up to +63.
  - The 1-over rows are ac-09758 39/38, ac-08389 46/45, ac-08031 36/35, ac-06269 37/36 and ac-07337 42/41.
- **Next (running):** the road-keeping DP (exchange/session3/skel_dp.py) on all 171 over-record lines, nearest first.
  This is the same tool that turned Kernel's ac-07119 34 into a 33 tie this morning. Hits will be verified, board-checked and
  sent to the inbox.
