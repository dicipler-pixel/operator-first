# session 1 → UPG-H lead, 04:58Z

- **The container restarted at about 04:51Z.** All lanes are relaunched; two stale y-run claims were cleared (21 of 128 rows done, 0 solves).
- **Queued:** ac-09736 AC 33 = record 33 (k9) TIE. It is low value but free, from session 1's pooled roads. Verified offline on board 0250Z.
- **Lanes:**
  - Seeds 13 (38/38) and 16 (5/5) are finished. **Seed 17** started on the 38 section D rows, one-over rows first.
  - Seeds 14 (32/38) and 15 (12/38) are continuing.
  - The yx finish (gap 0–1, k ≤ 5, commute-cleaned roads) is on all new roads.
- **New lineages since 02:45Z, all one over, to Bob for crossing:** ac-10098 (k1), four distinct 41s; ac-06969 (k3), a seed-16 39; ac-02341, ac-08889, ac-06262 and ac-08995 (k1, a seed-15 46).
- **Sol 6.1 support:** her ac-09409 control has not passed. Session 1's exact facts for her:
  - **No route ≤ 20 moves stays within peak 28.** acc_disk forward BFS, layers 0–20 complete, 365M states.
  - A cap-28/30 meet-in-the-middle is running now (forward 14 + backward ball 9 = 23) to tell her the cap at which a ≤ 23 route exists.
  - Session 1 will pass her the cap only, never a path.
