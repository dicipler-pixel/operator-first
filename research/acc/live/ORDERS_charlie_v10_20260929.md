# Charlie v10 (18:50Z): run the (y,x) ladder, plus batch 5 of rows close to the start
Your analysis is confirmed and logged. Ties come when the record is within 4 of the start (7 of 12). Each tie climbs early, holds flat, then collapses; the ladder finds it at the first cap above the peak. The (y,x) gap is real.
1. **Yes, start the (y,x) runs now**, on the six rows in your order, ac-04566 first (Stable 34, 1 team: a full point). Session 1's exact tool (acc_capped) already ends routes with [15,15], so both finishes are covered on our side too.
2. **Batch 5:** `charlie/charlie_easy_exact_5_20260929.json`, 20 rows. The AC or Stable record is within 4 of the start on each, and none is tied or stacked by us.
   - Order is by value. It opens with ac-09767 (AC 32 k1 / Stable 34 k1) and ac-08904 (AC 33 k1 / Stable 35 k1), then ac-02341 (Stable 30 k1).
   - Both finishes on every row where need_sac is true.
   - Starts are 25–30, so the state counts are larger. Caps are start+4 to start+14 (the `caps` field). Watch the disk.
3. **Drop rows 15+ above the start** on this machine, as you suggest.
