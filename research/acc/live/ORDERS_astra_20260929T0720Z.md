# ORDERS: session 2 (lead) to Astra, 2026-09-29 07:20Z

**Stop the easy-tail list now** (`targets_astra_easy_fwd_20260929T0610Z.json`). Those rows are k14–15. A tie there is
worth 2^(1-k) with k counting us: about 0.00006 per line. Your last 9 rows together were worth under 0.002 points.
Thank you for the clean verified work; it is the list that is low value, not the work.

**New list: `research/acc/live/targets_astra_wide_20260929T0720Z.json` (18 rows).**
- Every row is k1–2 on AC or Stable. Value is 0.25–0.5 points per row.
- We already hold a route **1–3 moves over** the record on each row (fields `gap_ac` and `gap_sac`).
- W=20000 did not close any of them. The notes show width helps: ac-09311 went 44 at width 100k to 43 at width 180k.

How to run:
1. Use the **widest beam your machine can hold**: at least W=100k, 150k–200k if it fits. Two-eyes settings:
   H=1, DIV=0.8, P2=2, QUOTA=16, ELITE=5000, DUAL=0.75. Set DMAX = record + 2.
2. Window-shorten every path (acc_window, span 14) toward (x,y), and toward (y,x) on the letter-swapped presentation.
3. A Stable tie can come from a (y,x) route: that is sac_record − 2 moves, then [15,15].
4. Go in file order; it is sorted by value, then gap.

Session 2 runs rows 1–18 of the same ranking at W=150k (not in your file). Do not run those.

Return hits as usual: inbox file with `ac-NNNNN: [..]` / `sac-NNNNN: [..]` lines, official-core verified.
Also send your best route per row, even when it is over the record, as one jsonl line in
`research/acc/live/sweeps/astra_wide_20260929.jsonl`, so junction splice can use it.
Never include ac-09839, ac-09311, ac-06403, ac-04718, ac-05378, sac-02257 (the owner sends those).
