# SOL61 swapped-target Stable work — 2026-10-02 11:04Z

## READY LINES FIRST
None. Two exact (y,x) roads recovered, each still one move short of a Stable tie.

## ac-06768
Stable snapshot from UPG-H/Kernel: record 34, k2. Need route to (y,x) of length 32, then [15,15].

Recovered exact route to (y,x), length 33:
ac-06768 yx: [8,8,7,9,11,5,9,4,10,2,5,12,12,10,13,7,3,9,5,7,9,9,7,9,4,13,0,11,3,3,5,3,5]

Recovery method: exact radius-7 ball from (y,x) intersected with all 5 verified held AC roads for this row. Best meet = prefix 26 + tail 7. Replayed under pinned ac-r2-v1 semantics; endpoint exactly (y,x).

New bounded test (not a proof):
- seeds: every prefix state of the 5 held AC roads plus the recovered yx33 route;
- neutral plateau: up to 8 moves, every step preserves total relator length;
- then up to 4 arbitrary bridge moves back to the local held-road web;
- local web uses exact road edges and exact radius-7 (y,x) end ball;
- target: total route <=32.
Result: MISS. No yx route <=32 in this scope.
Counts: 17,486 plateau (state,depth) entries; local bridge neighborhood about 1.16M states.

## ac-09312
Stable snapshot from UPG-H/Kernel: record 33, k3. Need route to (y,x) of length 31, then [15,15].

Recovered exact cross-row height-web route to (y,x), length 32:
ac-09312 yx: [11,2,5,9,7,2,7,9,2,10,8,6,6,3,8,5,12,10,2,8,11,11,3,7,2,5,5,5,5,5,3,3]

Recovery method: rebuilt the 429-road UPG-H/Kernel height web from KERNEL_priority_roads parts 1+2. Each saved AC start was reconstructed exactly by reversing its verified road from (x,y); 8,239 base junctions generated 117,464 exact symmetry nodes. BFS from (y,x) recovered distance 32 for the reconstructed ac-09312 start. Replayed endpoint exactly (y,x).

New bounded local plateau test (not a proof):
- seeds: every prefix state of the 5 held ac-09312 AC roads plus the recovered yx32 route;
- neutral plateau up to 8;
- up to 4 arbitrary bridge moves back to the local row-road web + exact radius-7 (y,x) ball;
- target <=31.
Result: MISS. No yx route <=31 in this scope.
Counts: 23,116 plateau (state,depth) entries; local bridge neighborhood about 1.03M states.

A stronger full-429-web plateau + bridge-3 run was attempted after recovery, but the orchestration call timed out before a verdict. Treat that as INCOMPLETE, not a negative.

## Interpretation / next cheap work
This confirms the user's two-target Stable plan is the right lane, but these two specific rows need a new middle lineage, not another <=4 local splice around the currently held roads.

Next cheapest targets are the 13 global Stable +1 rows from UPG-H's 13:45Z note:
sac-00172, 01028, 02147, 02302, 02419, 03235, 03246, 05137, 06901, 07288, 07466, 07920, 08244.
Before searching, audit current accepted history because some records/our roads moved later on 2026-10-01.

No SAIR submission/API call from SOL61.
