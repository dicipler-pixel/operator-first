# WORKING: Astra
Lane: ORDERS_astra_20260928T2045Z.md part 1 (rk2 bottom-up), deadlines in ORDERS_astra_v2_20260928T2200Z.md.
Hourly lines below (UTC, rows done / 150, hits, near misses).

2026-09-28 21:55 UTC — setup done; Linux x86_64, 9 visible logical CPUs / 8 CPU quota, 8 GiB RAM limit, 32 GiB disk / 20 GiB free. SAIR a0fd6e6 checked out; acc_beam and acc_window built; T8 SHA-256 38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8 matches. Rows done 0 / 150 (149 entries in supplied file), hits 0, near misses 0. Initial detached launch did not persist; restarting with the same nohup command inside a retained execution session.

2026-09-28 22:01 UTC — 1 / 150 rows done, hits 0, near misses 0. ac-00289: bounded nopath at W=20000 / depth 51, 230.6 s. First row pushed to sweeps/astra_rank_cap.jsonl. Exact ordered background run continues with ac-00180. Last rk2 refresh has 14 completed rows at the other end; no overlap with our completed row. No submission.
