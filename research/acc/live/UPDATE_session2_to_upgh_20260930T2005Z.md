# Session 2 to UPG-H (lead), 20:05Z: plan row 1 test is running

- **Plan row 1 (long k=1, records 60-99): the 25-row test started at 20:00Z.** Tool: `$S/smb/long_lane2.py` (smbeam2
  W 6000, DMAX 150, LCAP = 2 x record, 90 s per row; compile_exact to official moves; road DP GROW 1 / MAXC 8 / SLACK 3
  when the route is <= 2 x record; every route verified with the official core). Sample: 7 / 6 / 6 / 6 rows from the 60s / 70s /
  80s / 90s, drawn at random (seed 20260930) from the 1,257 AC k=1 rows on the 19:37Z board. It excludes rows claimed in any
  WORKING file in the last 6 h, rows where the ledger already has a route within 15%, and the owner's six. The rows are in
  WORKING_session2.md. Kill test as you set it: 0 of 25 within 15% of the record means stop. I will post the tally (every
  row, raw and DP length, ratio) when it ends, in about 40-60 min. Before this, my 09-29 long sample on records 100-540
  (W 2000) gave routes at about 2.2-2.8 x the record, so I expect a miss here too.
- **(y,x) list:** no route yet on sac-02341 (T 28), sac-08889 (T 35) or sac-06936 (T 25). sac-06768 (T 32) is running. Then
  sac-08862 (T 34; our AC 35 is the k10 tie you sent), then your heat rows: sac-02528, 04493, 02288, 02717, 08078 and 08578.
  I skipped sac-03272 because session 1 tied it (send 2907).
- **k3new:** 83 of 100 rows done in 4 lanes. The one tie was ac-08862 (sent in #2909). No other row is within the record.
- **Charlie:** no CHARLIE_lines file on the hub yet.

-- Session 2
