# SCOUT: low-k rows where the team has a road (2026-10-01 13:00Z)

Built by `tools/acc/upgh/scout.py` from the newest boards (ac_20261001T1239Z.json.gz, stable_ac_20261001T1239Z.json.gz; 20 min old) and the UPG-H ledger. 0 API calls.
Value: beat 1.0, tie 2^-k. `who` = the lane that claims the row (WORKING files) or `upgh (running)`. Take an unclaimed row by writing it in your WORKING file. Scoring lines go to `queue/`.

## SEND: our road is at or under the record, not held yet (next send) (0)
(none)

## LOST: we held it, a rival moved the record 1-3 below our line (5)
| row | record | k | ours | held | gap | heat | who | value |
|---|---|---|---|---|---|---|---|---|
| ac-00145 | 39 | 1 | 40 | 40 | +1 | 13 | git | 0.500 |
| ac-03060 | 27 | 1 | 28 | 28 | +1 | 2 | upgh (running) | 0.500 |
| ac-03714 | 50 | 1 | 51 | 51 | +1 | 14 |  | 0.500 |
| sac-03714 | 52 | 1 | 53 | 53 | +1 | 13 |  | 0.500 |
| ac-06969 | 38 | 3 | 39 | 41 | +1 | 1 | git | 0.125 |

## TWIN: we hold the AC record, not the Stable twin (6)
| row | record | k | ours | held | gap | heat | who | value | route |
|---|---|---|---|---|---|---|---|---|---|
| sac-02288 | 38 | 1 | 39 |  | +1 | 12 | git | 0.500 | (y,x) finish |
| sac-05378 | 43 | 1 | 44 |  | +1 | 14 | owner (never-send list) | 0.500 | (y,x) finish |
| sac-02528 | 36 | 2 | 37 |  | +1 | 6 |  | 0.250 | (y,x) finish |
| sac-04493 | 53 | 2 | 54 |  | +1 | 6 | git | 0.250 | (y,x) finish |
| sac-08078 | 34 | 2 | 35 |  | +1 | 12 | session1 | 0.250 | (y,x) finish |
| sac-08578 | 36 | 2 | 37 |  | +1 | 16 |  | 0.250 | (y,x) finish |

## NEAR: 1-3 over, k <= 3 (116)
| row | record | k | ours | held | gap | heat | who | value |
|---|---|---|---|---|---|---|---|---|
| ac-00975 | 34 | 1 | 35 |  | +1 | 13 | session1 | 0.800 |
| ac-03364 | 41 | 1 | 42 |  | +1 | 2 |  | 0.800 |
| ac-10098 | 40 | 1 | 41 |  | +1 | 13 |  | 0.800 |
| sac-00975 | 36 | 1 | 37 |  | +1 | 15 | session1 | 0.800 |
| sac-02288 | 38 | 1 | 39 |  | +1 | 12 | git | 0.800 |
| sac-03871 | 32 | 1 | 33 |  | +1 | 14 | session1 | 0.800 |
| sac-05378 | 43 | 1 | 44 |  | +1 | 14 | owner (never-send list) | 0.800 |
| sac-06045 | 38 | 1 | 39 | 50 | +1 | 14 | session1 | 0.800 |
| sac-10098 | 42 | 1 | 43 |  | +1 | 14 |  | 0.800 |
| ac-00364 | 49 | 1 | 51 |  | +2 | 0 |  | 0.650 |
| ac-00580 | 42 | 1 | 44 |  | +2 | 0 |  | 0.650 |
| ac-03719 | 35 | 1 | 37 |  | +2 | 0 |  | 0.650 |
| sac-00364 | 51 | 1 | 53 |  | +2 | 0 |  | 0.650 |
| sac-00580 | 44 | 1 | 46 |  | +2 | 1 |  | 0.650 |
| sac-02341 | 30 | 1 | 32 |  | +2 | 1 |  | 0.650 |
| sac-03364 | 42 | 1 | 44 |  | +2 | 0 |  | 0.650 |
| sac-04882 | 53 | 1 | 55 |  | +2 | 0 |  | 0.650 |
| sac-08889 | 37 | 1 | 39 |  | +2 | 1 | upgh (running) | 0.650 |
| sac-09390 | 37 | 1 | 39 |  | +2 | 0 |  | 0.650 |
| ac-04220 | 86 | 1 | 89 |  | +3 | 0 |  | 0.600 |
| ac-04780 | 38 | 1 | 41 |  | +3 | 0 |  | 0.600 |
| ac-05726 | 35 | 1 | 38 |  | +3 | 0 |  | 0.600 |
| ac-05805 | 65 | 1 | 68 |  | +3 | 0 |  | 0.600 |
| ac-06963 | 45 | 1 | 48 |  | +3 | 0 |  | 0.600 |
| ac-08445 | 53 | 1 | 56 |  | +3 | 0 |  | 0.600 |
(91 more in research/acc/upgh/cache/scout_latest.json)

## ROAD: 4-10 over, k <= 3 (shorten lanes) (336)
| row | record | k | ours | held | gap | heat | who | value |
|---|---|---|---|---|---|---|---|---|
| ac-00221 | 56 | 1 | 60 |  | +4 | 0 |  | 0.125 |
| ac-03475 | 43 | 1 | 47 |  | +4 | 0 |  | 0.125 |
| ac-06066 | 35 | 1 | 39 |  | +4 | 0 |  | 0.125 |
| ac-08367 | 76 | 1 | 80 |  | +4 | 0 |  | 0.125 |
| ac-09390 | 33 | 1 | 37 |  | +4 | 1 |  | 0.125 |
| sac-00221 | 58 | 1 | 62 |  | +4 | 0 |  | 0.125 |
| sac-01965 | 41 | 1 | 45 |  | +4 | 0 |  | 0.125 |
| sac-03475 | 45 | 1 | 49 |  | +4 | 0 |  | 0.125 |
| sac-06066 | 37 | 1 | 41 |  | +4 | 2 |  | 0.125 |
| sac-06236 | 38 | 1 | 42 | 51 | +4 | 0 |  | 0.125 |
| sac-08367 | 78 | 1 | 82 |  | +4 | 0 |  | 0.125 |
| sac-09762 | 46 | 1 | 50 |  | +4 | 0 |  | 0.125 |
| ac-00673 | 55 | 1 | 60 | 139 | +5 | 0 |  | 0.100 |
| ac-03826 | 42 | 1 | 47 |  | +5 | 0 |  | 0.100 |
| ac-04016 | 55 | 1 | 60 |  | +5 | 0 |  | 0.100 |
| ac-04766 | 50 | 1 | 55 |  | +5 | 0 |  | 0.100 |
| ac-04794 | 45 | 1 | 50 | 121 | +5 | 0 |  | 0.100 |
| ac-07541 | 42 | 1 | 47 |  | +5 | 0 |  | 0.100 |
| sac-00667 | 38 | 1 | 43 |  | +5 | 0 |  | 0.100 |
| sac-00673 | 57 | 1 | 62 | 127 | +5 | 0 |  | 0.100 |
| sac-01759 | 46 | 1 | 51 |  | +5 | 0 |  | 0.100 |
| sac-03826 | 44 | 1 | 49 |  | +5 | 0 |  | 0.100 |
| sac-04016 | 57 | 1 | 62 |  | +5 | 0 |  | 0.100 |
| sac-07541 | 44 | 1 | 49 |  | +5 | 0 |  | 0.100 |
| sac-09221 | 71 | 1 | 76 |  | +5 | 0 |  | 0.100 |
(311 more in research/acc/upgh/cache/scout_latest.json)

