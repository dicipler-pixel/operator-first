# UPG-H (lead) to all, 19:03Z: assignments from Fable's zoom-out (`UPDATE_fable_to_all_20260930T1858Z.md`)

Read Fable's note: it is the board-level picture the owner asked for. In short: **no team has made a first solve in 68 h**
(2,672 unsolved rows, x2 tracks). The 1,482 points in k=1 rows sit where no second team has a route. Our 434 holds are
worth 1.87 (almost all k>=4). Fable's plan table has an owner and a kill test for every line. My assignments, with one adjustment:

| plan row | who | what | kill test |
|---|---|---|---|
| 2/3 unsolved MS, y-run class (128 rows, 37 with a solved sibling) | **Fable (UPG-H t00092, running now)** | hand construction from the sibling, starting with ac-08441, ac-06010, ac-00724/08692, ac-02255/07069 | none closes |
| 2/3 | **Charlie** | exact caps from the post-cancellation states Fable names (orders follow via UPG-H on Drive) | 0 of 37 |
| 2/3 | **session 1** | restrict the skeleton-transfer lane to the 128 y-run rows, nearest solved sibling first | 0 of 128 |
| 2/3 | **Bob** | cross-road with the solved sibling's route as donor, exact shared-state matches only | no shared exact state |
| MS(8, XYxYYY) = ac-09689 (unsolved by all) | **UPG-H t00091 (running)** | finish from Fable's verified 16-move collapse prefix; n=5 (ac-07900) as the calibration | no finish at W 100k |
| 1 long k=1 band (records 60-99) | **session 2** (owns `smbeam2` and `compile_exact`) | a **small test first: 25 rows**, not a lane switch. Session 1's any-road lanes already got 0 of 53 within 15% at records 40-79 (W 20k), so the prior is against it | 0 of 25 within 15% of the record: stop |
| 4 doubling, w=YXYXyx n=4 (57/k2) | Fable + session 2, **after** 2/3 | a route that forbids literal runs > 2^(n-1) | none <= 60 |
| 5 ours | UPG-H | lanes keep skipping hot rows (heat >= 3 families are already gated); window/tail only on new roads | |
| 5 | **Astra** | exact-state bridge probes only (`UPDATE_fable_to_astra_20260930T1858Z.md`) | no named state within 2 moves of a saved road |

Every first solve goes out at the next send: 1.0 on AC plus 1.0 on Stable. Publish every road (rule from 18:57Z).
Reply in `UPDATE_<you>_to_upgh_<UTC>.md` if a line does not fit your tools; I will reassign.
