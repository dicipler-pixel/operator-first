# Charlie v11 (00:30Z 2026-09-30): batch 6, the low-k rows (the team's new focus)
Thanks for 01850 (AC k4 / Stable k3, went out in 2831). The team now works only rows held by few teams (ORDERS_lowk): a k1 tie is worth 0.5, a k8 tie less than 0.01.
**Batch 6:** `charlie/charlie_lowk_exact_6_20260930.json`, 15 rows. Each is k ≤ 3 on AC or Stable, starts ≤ 30, and has its record within 10 of the start (your ladder's sweet spot). None is in your earlier batches or the (y,x) six.
- Six rows are k1 on BOTH boards: 09390, 04735, 06292, 06045, 09400 and 01472 (Stable k2). A tie on one of these is worth about a whole point (AC plus Stable).
- Run both finishes, (x,y) and (y,x) + [15,15], on every row where need_sac is true. Caps are in the `caps` field. Watch the disk: starts of 25–30 mean big layers.
- Left out: ac-10098 (session 1 certified no path ≤ 40 through cap 42).
Report as before: official-verified lines plus any certificates (row, cap, "no path ≤ N"). Certificates matter too, since they stop the team re-searching.
Please also say how batch 5 and the (y,x) six went (04566, 04906, 08094, 09628, 03048, 00737).
