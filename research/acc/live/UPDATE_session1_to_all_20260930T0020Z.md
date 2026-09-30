# session 1 → all, 00:20Z 2026-09-30: HOLD MODE acknowledged; retargeted to low-k
- **HOLD MODE:** session 1 makes no sends and no API pulls. It verifies offline and stacks only.
- **Reconciled:** 47 of the 49 lines in session 1's hold file went out in submission 2831. The only remaining pair, **ac/sac-01461** (loose DP; AC 32 k7 / Stable 34 k6, verified ties), is now in OWNER_SUBMIT_20260930_0005Z.txt. The old HOLD_FOR_NEXT_WINDOW file is marked superseded.
- **Retargeted to ORDERS_lowk:** the loose road-keeping DP (GROW 2, MAXC 16, SLACK 4) now runs on the 67 low-k rows with up to 6 roads per row: our pool, Kernel's paths and Git's pooled paths, 205 jobs, +1 rows first. Output: session 1 scratch skdp_lowk.jsonl. This is a different setting from session 2's default-cap DP; the loose caps produced 07337 (k2), 00345 (k3), 09758 (k4), 04157 and 01461.
- The gap 3–4 loose DP (two workers) keeps running on the rest.
