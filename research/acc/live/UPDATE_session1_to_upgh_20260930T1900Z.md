# session 1 → UPG-H lead, 19:00Z: raised-ceiling surgery, first pass on all 6 rows

Settings: K = start + 6, MAXST 8e7, head/tail L ≤ 22, windows = uncapped acc_window (≤ 14). Stable (y,x) routes ran on the relator-swapped row.
Raw lane JSONs and the tool: `research/acc/live/sweeps/session1/surgery/<row>/` (cap_surgery_s1.py, run_rows.sh).

| row (record, k) | route/line now | windows ≤14 | head certified to | tail certified to |
|---|---|---|---|---|
| sac-03272 (32, k1) | 33 | none | L=22 (finished) | L=22 (finished) |
| sac-03871 (32, k1) | 33 | none | L=21 (budget stop at 22) | L=22 (finished) |
| sac-08078 (34, k1) | 35 | none | L=19 (budget stop at 20) | L=20 (disk stop at 21) |
| sac-02288 (38, k1) | **39** (was 40; windows cut 1) | cut 1, then none | L=19 (budget) | L=19 (budget) |
| sac-02717 (38, k1) | 40 | none | L=2: route above cap at step 3 | L=20 (budget stop at 21) |
| ac-10098 (40, k1) | 41 | none | L=3: route above cap at step 4 | L=22 (finished) |

- **No row reached its record.** sac-02288 is now +1 (39 vs 38). The line is official-verified but not scoring, so it goes to sweeps, not the queue.
- **Scoped misses:** "certified to L" means no shorter replacement exists for the first or last L moves of the held route under cap K. A budget stop is scoped at that L.
- **Finding:** sac-02717 and ac-10098 have held routes with a single multiplication spike above start + 6 in the first moves: totals 31,31,31,**50**,31 and 30,30,30,30,**45**,33. Your t00073 lane stops the head at the first root above the cap. Every later root is an independent exact search, so I patched my copy to skip roots above the cap instead of stopping. The head lanes for those two are rerunning now.
- **Also running:** sac-03272 again at K = 29 (start + 10). It is the cheapest row, and its K = 25 pass was fully certified at both ends.
- Next unless you say otherwise: sac-03871 at K = 33, then the budget-stopped rows at MAXST 1.5e8. Disk here is the limit (14 GB free, balls about 3 GB each).
