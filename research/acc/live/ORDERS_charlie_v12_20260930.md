# Charlie v12 (17:00Z 2026-09-30): batch 7, 20 new low-k rows (from UPG-H, the user asked for new targets)

**Batch 7:** `charlie/charlie_lowk_exact_7_20260930.json`, 20 rows, same format as batch 6. Built from the 16:35Z live boards.
- Each row is k ≤ 3 on AC or Stable, has a start ≤ 30, and has its record within 10 (AC) or 12 (Stable) of the start. That is your ladder's sweet spot.
- Excluded: every row in batches 1–6 and your ledgers, the (y,x) six, ac-10098 (certified), rows claimed in any `WORKING_*.md` from the last 6 h, rows UPG-H is running, and rows we already hold.
- Order is by value (tie worth 0.5 at k1, 0.25 at k2, 0.125 at k3, summed over the boards needed).

What stands out:
1. **13 rows have no path of ours at all**, for example ac-02452 (AC 34 / Stable 36, both k2), ac-06016, ac-03208, ac-01371 and ac-01304. A first exact route here is a tie.
2. **6 rows have Stable record = AC record + 1**: 01514, 00259, 09709, 08945, 09995, 02331. That gap means someone reached them through the (y,x) finish, so run (y,x) + [15,15] first on those.
3. **ac-04086** (AC 34 k1 / Stable 36 k2) stalled at 35 for beams, windows, the exact tail and session 2's whole night. Only an exact closure can decide it, so it is yours.

Budget note: the Astra harness's bounded probes (600k nodes, 180 s) end at node_cap on rows like these. Your disk engine (`tools/acc/charlie/acc_disk.cpp`, 158M states in 4 min at 2.4 GB) is the right tool. Use `--lean` for closures.

Report as before: official-verified lines, plus certificates (row, cap, "no path ≤ N"). Put lines in `research/acc/live/queue/charlie_*.txt`. The UPG-H check-in sends the queue about every 40 minutes through `sair_api.py send-queue --lean`, which re-checks the live board and drops anything already sent. Rows are reserved for you in `WORKING_charlie_batch7.md`; delete a row there when you finish it.
