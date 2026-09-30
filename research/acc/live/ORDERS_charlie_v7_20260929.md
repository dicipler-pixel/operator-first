# Charlie v7 (13:05Z, morning checkpoint): easy exact targets, batch 3
Batch 1 gave 4 ties, and batch 2 gave ac/sac-00559. Your cap-ladder finding (ties appear at cap start+8 to start+12) is the rule now.
Batch 3: `charlie/charlie_easy_exact_3_20260929.json`, 18 rows, AC records 23–36, start lengths 18–24. None is tied, sent or
inboxed by us, and none was in batches 1–2 or your ledgers.
- **Caps:** start+8 to start+14 in steps of 2 (the `caps` field). Climb further while the machine allows. Stop a row at a tie.
- **Both boards are open on every row where `need_sac` is true.** Stable = AC path + [16,15], or a (y,x) route + [15,15].
- **Order:**
  - First 10 by value, where the record is held by 1–5 teams: ac-03871 (AC 30 k1, Stable 32 k1), ac-02404 (k1/k1), ac-04566, ac-05726, ac-08031, ac-03310, ac-05526, ac-06737, ac-08094, ac-03868.
  - Then 8 "easy" rows where the record is closest to the start length (your batch-2 hit, 00559, was that kind): ac-04346, ac-05171, ac-09409, ac-01828, ac-09857, ac-05414, ac-09212, ac-08371.
- **Report:** tie lines as `ac-XXXXX: [...]` / `sac-XXXXX: [...]`, plus a certified-negative table (row, record, caps cleared), as before.
- The user collects everything at lunch. Session 1 verifies each line against the board and stacks it.
