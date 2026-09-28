# Codex short Stable AC yx2 lane — claimed 2026-09-28 22:00 UTC

Exclusive eight Stable AC targets in `targets_codex_stable_yx2_20260928T2200Z.json`: sac-02888 sac-00786 sac-03826 sac-05460 sac-04880 sac-02257 sac-03070 sac-09272. Snapshot Stable records 43–47, k=1–2. These IDs were excluded from Session 2 yxl, Luna yx2, Fable/Sonnet yx, Astra, Bob, Session 1 p2c and the ranked top 300, plus other WORKING claims.

Method: relator-swap twin to reach (y,x), append the two Stable moves, width 20,000, two-eyes P2=2 beam, per-row depth ceiling Stable record −2. Any tie/beat is checked by pinned official stable_core before inbox. Raw output in sweeps/codex_stable_yx2_20260928.jsonl. One process at a time due shared 8 GiB limit. Only Session 2 submits.

## Relator-swap pass — 2026-09-28 22:24 UTC

8/8 complete in `sweeps/codex_stable_yx2_20260928.jsonl`: 4 bounded nopath and four official-valid Stable routes, all over record. Best is **sac-02257 48 vs record 47 (k=2)**. The three others are sac-00786 50/43, sac-03826 50/44, sac-05460 49/44. Official Stable replay passed the near miss. The ceiling-16 reverse-map scan queried 9 short states on the transformed rank-two route, seven in table, no cut. Radius-3+4 exact windows (<=8) and radius-5+5 exact windows (<=11) found no cut; the radius-6+7 original `acc_window` timed out after 180s with no partial splice, so gap<=14 is **incomplete**. Both small-window tools pass a planted 2-move-cut control. `acc_window11.c` is committed.

I am now running the opposite letter-swap orientation (`TWIN_MODE=yx`) on ac-02257 with W=20,000 and DMAX=45. If it ties/bests 47, I will officially verify and inbox. The other seven Stable IDs are released for other methods; ac-02257 remains claimed for this follow-up.
