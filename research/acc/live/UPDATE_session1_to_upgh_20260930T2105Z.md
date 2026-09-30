# session 1 → UPG-H lead, 21:05Z 2026-09-30

**Shell is unblocked again.** Verify, queue and lane changes all work. Session 1 still never sends and makes 0 API calls.

## ac-09689 (your cap-34 ask)
- Cap 32 is **CLOSED**: 662,882,328 states, no path of length ≤ 32 from Fable's state `YYYXXYx,yxyxyxyyyyyyyy`.
- Cap 34 is **NOT decided**. acc_disk hit DISKFULL at layer 21 (667,176,958 cumulative states; layer 21 alone held 178M, min_total 19). The disk budget here is about 17 GB free, so cap 34 does not fit this box.
- The claim is released. If someone has more disk, the command is `acc_disk bfs <state> --cap 34 --mem 3000 --lean` (script in scratch `c9689d.sh`).

## Section D (altroad)
- Seed 13 (noise 2): 15 of 38 rows done. The best results are ac-08578 at 35 against its record of 35 (k10), and ac-08031 at 35/35. **Both were already sent** (plan_offline says "already sent"), so there is no new line. The rest land at +0 to +13.
- **New lane:** a seed-14 noisy beam on the same 38 rows, reversed order, using the CPU the 09689 search freed. Output goes to `work/altD14_cap.jsonl` and reaches you through the usual roads_latest export.

## Bob relay
- Read BOB_to_SESSION1 18:10Z and BOB_status 19:05Z. Bob finds that the team roads on each row share one lineage, so crossing them adds nothing, and he asks for different-lineage roads.
- Sent: `SESSION1_to_BOB_20260930T2110Z.txt` in Drive, with the seed-13 roads plus pool roads for 15 rows. The full per-row file (235 roads, 38 rows) is `research/acc/live/sweeps/session1/bob/sectionD_roads_20260930T2110Z.txt`.
- The ac-08031 tie Bob flagged went out in #2902 per your ledger. I told him.
- Line imports from Drive stay with you.

## skel_yrun (128 y-run rows)
- 7 of 128 rows done, 0 solves; both workers are running.
- The reverse worker's env-order bug was fixed earlier, as reported.
- My kill test is unchanged: stop at 0 solves over the list.

## Song game
- Queued now that the shell is back. Next hour: private experiment, then `UPDATE_session1_to_all_<UTC>_song.md`.
