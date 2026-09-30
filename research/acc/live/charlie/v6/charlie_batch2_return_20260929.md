# Charlie easy-exact batch 2 return (relayed by the user; archived 13:00Z by session 1)
Method change: each row climbs the cap ladder from start to start+14 in steps of 2 and stops at a tie or the machine limit. Batch 1's ties appeared at start+8 to start+12.

## Ties (verified by session 1 with plan_offline against the board)
- ac-00559: 27, record 27, k11. Exact shortest under cap 28.
- sac-00559: 29, record 29, k10 (the ac path + [16,15]).
- sac-04718: 35 (route surgery: held (y,x) route 34 → 33, then + [15,15]). Already sent and submitted at 11:50Z.

## Certified: no path at record length at every cap until the search outgrew the machine
| row | record | caps certified |
|---|---|---|
| ac-07521 | 36 | 19–29 (cap 29 = 505M states) |
| ac-09628 | 35 | 19–27 |
| ac-00345 | 35 | 19–31 |
| ac-09177 | 35 | 17–27 |
| ac-04499 | 36 | 17–27 |
| ac-03799 | 25 | 17–29 |

ac-04909 is still running and is clear at caps 22–32 so far.
These results are negative only within those caps. A record path would need an intermediate total relator length above the certified cap.
