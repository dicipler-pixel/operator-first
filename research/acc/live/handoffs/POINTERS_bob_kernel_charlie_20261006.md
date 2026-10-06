# Handoffs from Bob, Kernel and Charlie (6 Oct): where they are

| member | handoff (Drive hub) | attachments sent to Jeremy (not yet in the hub or repo) | headline |
|---|---|---|---|
| Kernel | `HANDOFF_KERNEL_20261006T0325Z.md` (Drive 1hrsrGwa7x4HWO_7xGzH1bkrfLUl_N5Vf, 14,807 B) | `KERNEL_all_roads_20261006.txt` (3,940 lines: 1,829 AC on 1,126 rows; 1,802 (y,x)+[15,15]; 309 other Stable), `KERNEL_tools_20261006.zip` (scripts, 2,482 rules, MS id of 113 rows) | crossgraph tube R4 = best held on 14 rows; R5 spine 15/15 = R4; finish zone E1; 8 rows where (y,x) is 1 shorter (none scores at 03:15Z); MS one-sided cap 18 is INCOMPLETE |
| Bob | `HANDOFF_BOB_20261006T0330Z.md` (Drive 1kVcOdStq6WYojmSr2ISF3PK4HNPMEzIy, 18,287 B) | `BOB_handoff_bundle_20261006.zip` (2,485 AC roads on 596 rows, best-per-row 596/596 CLI ok, misses catalog with 1,303 records, scripts) | class transfer, window and cross-road splice, collapse beam; E2 one-letter collapse on 63 MS roads; E5 775 ladder rows; 5 unfinished jobs (no checkpoints) |
| Charlie | `HANDOFF_CHARLIE_20261006T0326Z_POINTER.txt` (Drive 1m5levLw1NkCTzIpUfyacyZLdL7-Uv4I4) | `HANDOFF_CHARLIE_20261006T0326Z.md` (45,505 B, sha256 bb9ee1c1…3294638), `CHARLIE_code_and_ledgers_20261006.zip` (67,098 B, sha256 bb609f88…ca1c275) | 74 roads; 142 exact cap certificates (K ≤ 36); 38 surgery certificates; 85 closed components; 46 disk-stopped runs that need 60–150 GB |

**Next step:** Jeremy uploads the five attachments to `research/acc/live/handoffs/` on this branch (GitHub web upload).

**Then UPG-H:**
- verifies every road (CLI, 400 per chunk, unique IDs);
- runs plan_offline against the board;
- files the misses in `catalog/closed_<member>.jsonl` and the open runs in `catalog/incomplete_<member>.jsonl`;
- feeds the roads to the webs.

Large files are not pulled through the Drive connector: base64 in the tool result costs as much as the file.
Orders follow-up: `ORDERS_ADDENDUM_20261006T0340Z.md`.
