# Session 2 to UPG-H (lead), 01:40Z: W100k free-depth swapped-start on the 8 shortest rows: one near-miss (sac-07333 +2)

Same lane as the 00:22Z note, but W 100,000, free depth (target + 20), seed 17. Routes are in `sweeps/session2/swapstart_yx_routes_W100k_20261001.txt`.

| row | Stable rec | k | Stable via (y,x) + 2 | gap | s |
|---|---|---|---|---|---|
| sac-07302 | 40 | 2 | no route | - | 1072.3 |
| sac-02623 | 41 | 1 | 52 | +11 | 867.6 |
| sac-03084 | 42 | 2 | 51 | +9 | 635.8 |
| sac-07333 | 42 | 1 | 44 | +2 | 1354.1 |
| sac-03961 | 43 | 1 | 64 | +21 | 1098.1 |
| sac-10040 | 45 | 1 | 54 | +9 | 1016.1 |
| sac-02680 | 45 | 1 | no route | - | 1068.5 |
| sac-04880 | 46 | 2 | no route | - | 1215.4 |

**sac-07333 (k1): (y,x) route 42 -> Stable 44 vs 42.** W 20k gave 51, so width paid on this row. Running now: mid-restart along that S' route
(target 40), at W 20k and W 100k in parallel. The other 7 rows stay 6-21 over or have no route, so width is not the limit there.
Claimed: sac-07333 (WORKING_session2.md). Two cores are still free; name rows if you have them.

-- Session 2
