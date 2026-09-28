# WORKING: Astra
Lane: ORDERS_astra_20260928T2045Z.md part 1 (rk2 bottom-up), deadlines in ORDERS_astra_v2_20260928T2200Z.md.
Hourly lines below (UTC, rows done / 150, hits, near misses).

2026-09-28 21:55 UTC — setup done; Linux x86_64, 9 visible logical CPUs / 8 CPU quota, 8 GiB RAM limit, 32 GiB disk / 20 GiB free. SAIR a0fd6e6 checked out; acc_beam and acc_window built; T8 SHA-256 38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8 matches. Rows done 0 / 150 (149 entries in supplied file), hits 0, near misses 0. Initial detached launch did not persist; restarting with the same nohup command inside a retained execution session.

2026-09-28 22:01 UTC — 1 / 150 rows done, hits 0, near misses 0. ac-00289: bounded nopath at W=20000 / depth 51, 230.6 s. First row pushed to sweeps/astra_rank_cap.jsonl. Exact ordered background run continues with ac-00180. Last rk2 refresh has 14 completed rows at the other end; no overlap with our completed row. No submission.

2026-09-28 22:11 UTC — 3 / 150 completed rows; fourth row ac-06403 has a verified AC22 / SAC24 tie (1 hit row, 2 board candidates), already pushed to research/acc/live/inbox/20260928T221036Z_astra_ac-06403.txt. Official core and stable_core both pass; peak length 45. Window shortening still running, so this row is not yet in the raw sweep. Near misses 0. Latest SENT_ROWS has no ac/sac-06403 entry; latest rk2 ledger has 15 rows with no overlap. No submission.

2026-09-28 22:27 UTC — 9 / 150 rows done; hits 1 row / 2 board candidates (ac-06403 AC22, SAC24), near misses 0. Current row ac-09311. Experiment package pushed in a9673d1: exact-scoring P2 speed patch pilot and signed-finish archive negative. Production-width speed control still running separately. User asked to keep the ranked run active while we talk. Hourly :55 check armed; no submission.

2026-09-28 22:47 UTC — 11 / 150 rows done; 2 hit rows / 4 board candidates, near misses 0. Ten-row checkpoint and new official-verified ac-09311 AC42 / SAC44 ties pushed (59a865b, 21f1e84). Original retained process was absent when checked during the next turn; resumed from the ten-row checkpoint at 22:42Z using identical command/settings, then ac-09268 completed as bounded nopath. No work lost. Production-width speed control is complete: identical AC22/SAC24 and frontiers on ac-06403, linear 83.194 s / baseline 116.853 s (one concurrent-machine pair; raw result dc697c7). User also assigned kernel rows 101–213 via Drive relay; three small W2k workers are running alongside this lane.

2026-09-28 22:55 UTC rally — 11 / 150 rows done, 2 hit rows (4 verified board lines), near misses within 1: 0. Ranked runner is alive; ac-09219 window stage active, raw AC45 vs record43. Latest rk2 ledger: 15 completed rows, no collision. Kernel relay screen on the same machine: 70 / 113, zero hits; separate from the Claude Kernel/Charlie/Bob runs now visible in Drive. Formal identity/method roll call: rollcall/20260928T2256Z_astra.md. No submission.
