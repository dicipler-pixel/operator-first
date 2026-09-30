# SCOUT: low-k rows where the team has a road (2026-09-30 20:47Z)

Built by `tools/acc/upgh/scout.py` from the newest boards (ac_20260930T2043Z.json.gz, stable_ac_20260930T2043Z.json.gz; 4 min old) and the UPG-H ledger. 0 API calls.
Value: beat 1.0, tie 2^-k. `who` = the lane that claims the row (WORKING files) or `upgh (running)`. Take an unclaimed row by writing it in your WORKING file. Scoring lines go to `queue/`.

## SEND: our road is at or under the record, not held yet (next send) (0)
(none)

## LOST: we held it, a rival moved the record 1-3 below our line (5)
| row | record | k | ours | held | gap | heat | who | value |
|---|---|---|---|---|---|---|---|---|
| ac-00145 | 39 | 1 | 40 | 40 | +1 | 13 | bob | 0.500 |
| ac-03714 | 50 | 1 | 51 | 51 | +1 | 12 | bob | 0.500 |
| ac-04086 | 34 | 1 | 35 | 35 | +1 | 13 | bob | 0.500 |
| sac-03714 | 52 | 1 | 53 | 53 | +1 | 13 | bob | 0.500 |
| ac-06969 | 38 | 3 | 39 | 41 | +1 | 0 |  | 0.125 |

## TWIN: we hold the AC record, not the Stable twin (8)
| row | record | k | ours | held | gap | heat | who | value | route |
|---|---|---|---|---|---|---|---|---|---|
| sac-02288 | 38 | 1 | 39 |  | +1 | 12 | session1 | 0.500 | (y,x) finish |
| sac-02528 | 36 | 1 | 37 |  | +1 | 6 | session2 | 0.500 | (y,x) finish |
| sac-05378 | 43 | 1 | 44 |  | +1 | 13 |  | 0.500 | (y,x) finish |
| sac-08078 | 34 | 1 | 35 |  | +1 | 14 | session1 | 0.500 | (y,x) finish |
| sac-01514 | 37 | 2 | 38 |  | +1 | 0 | charlie_batch7 | 0.250 | (y,x) finish |
| sac-04493 | 53 | 2 | 54 |  | +1 | 5 | session2 | 0.250 | (y,x) finish |
| sac-08578 | 36 | 2 | 37 |  | +1 | 15 | session2 | 0.250 | (y,x) finish |
| sac-07119 | 34 | 3 | 35 | 50 | +1 | 5 |  | 0.125 | (y,x) finish |

## NEAR: 1-3 over, k <= 3 (86)
| row | record | k | ours | held | gap | heat | who | value |
|---|---|---|---|---|---|---|---|---|
| ac-00975 | 34 | 1 | 35 |  | +1 | 14 | bob | 0.800 |
| ac-08995 | 45 | 1 | 46 |  | +1 | 12 | bob | 0.800 |
| ac-10098 | 40 | 1 | 41 |  | +1 | 12 | bob | 0.800 |
| sac-00975 | 36 | 1 | 37 |  | +1 | 14 | bob | 0.800 |
| sac-02288 | 38 | 1 | 39 |  | +1 | 12 | session1 | 0.800 |
| sac-02528 | 36 | 1 | 37 |  | +1 | 6 | session2 | 0.800 |
| sac-03871 | 32 | 1 | 33 |  | +1 | 13 | bob | 0.800 |
| sac-05378 | 43 | 1 | 44 |  | +1 | 13 |  | 0.800 |
| sac-06045 | 38 | 1 | 39 | 50 | +1 | 13 | bob | 0.800 |
| sac-08078 | 34 | 1 | 35 |  | +1 | 14 | session1 | 0.800 |
| sac-08995 | 47 | 1 | 48 |  | +1 | 13 | bob | 0.800 |
| sac-10098 | 42 | 1 | 43 |  | +1 | 13 | bob | 0.800 |
| ac-03719 | 35 | 1 | 37 |  | +2 | 0 | bob | 0.650 |
| ac-03913 | 46 | 1 | 48 |  | +2 | 0 | upgh (running) | 0.650 |
| sac-02341 | 30 | 1 | 32 |  | +2 | 0 | session2 | 0.650 |
| sac-02717 | 38 | 1 | 40 |  | +2 | 12 | session1 | 0.650 |
| sac-08889 | 37 | 1 | 39 |  | +2 | 0 | session2 | 0.650 |
| sac-09390 | 37 | 1 | 39 |  | +2 | 0 |  | 0.650 |
| ac-00580 | 42 | 1 | 45 |  | +3 | 0 | bob | 0.600 |
| ac-04581 | 47 | 1 | 50 |  | +3 | 0 |  | 0.600 |
| ac-05726 | 35 | 1 | 38 |  | +3 | 0 | bob | 0.600 |
| ac-08445 | 53 | 1 | 56 |  | +3 | 0 |  | 0.600 |
| sac-00580 | 44 | 1 | 47 |  | +3 | 0 | bob | 0.600 |
| sac-04780 | 40 | 1 | 43 |  | +3 | 0 |  | 0.600 |
| sac-04882 | 53 | 1 | 56 |  | +3 | 0 |  | 0.600 |
(61 more in research/acc/upgh/cache/scout_latest.json)

## ROAD: 4-10 over, k <= 3 (shorten lanes) (228)
| row | record | k | ours | held | gap | heat | who | value |
|---|---|---|---|---|---|---|---|---|
| ac-03475 | 43 | 1 | 47 |  | +4 | 0 |  | 0.125 |
| ac-09390 | 33 | 1 | 37 |  | +4 | 0 |  | 0.125 |
| sac-00034 | 42 | 1 | 46 |  | +4 | 0 |  | 0.125 |
| sac-03475 | 45 | 1 | 49 |  | +4 | 0 |  | 0.125 |
| sac-04566 | 34 | 1 | 38 |  | +4 | 0 |  | 0.125 |
| sac-06066 | 37 | 1 | 41 |  | +4 | 0 |  | 0.125 |
| ac-02593 | 55 | 1 | 60 |  | +5 | 0 |  | 0.100 |
| ac-03364 | 41 | 1 | 46 |  | +5 | 0 |  | 0.100 |
| ac-04794 | 45 | 1 | 50 | 121 | +5 | 0 |  | 0.100 |
| sac-00667 | 38 | 1 | 43 |  | +5 | 0 |  | 0.100 |
| sac-01759 | 46 | 1 | 51 |  | +5 | 0 |  | 0.100 |
| sac-01965 | 41 | 1 | 46 |  | +5 | 0 |  | 0.100 |
| sac-09221 | 71 | 1 | 76 |  | +5 | 0 |  | 0.100 |
| ac-00667 | 36 | 1 | 42 |  | +6 | 0 |  | 0.083 |
| ac-00786 | 41 | 1 | 47 |  | +6 | 0 |  | 0.083 |
| ac-01759 | 44 | 1 | 50 |  | +6 | 0 |  | 0.083 |
| ac-04478 | 41 | 1 | 47 |  | +6 | 0 |  | 0.083 |
| ac-04676 | 68 | 1 | 74 |  | +6 | 0 |  | 0.083 |
| ac-05418 | 38 | 1 | 44 |  | +6 | 0 |  | 0.083 |
| ac-06339 | 44 | 1 | 50 |  | +6 | 0 |  | 0.083 |
| ac-06419 | 45 | 1 | 51 |  | +6 | 0 |  | 0.083 |
| ac-06717 | 38 | 1 | 44 |  | +6 | 0 |  | 0.083 |
| ac-09221 | 69 | 1 | 75 |  | +6 | 0 |  | 0.083 |
| sac-00786 | 43 | 1 | 49 |  | +6 | 0 |  | 0.083 |
| sac-03364 | 42 | 1 | 48 |  | +6 | 0 |  | 0.083 |
(203 more in research/acc/upgh/cache/scout_latest.json)

