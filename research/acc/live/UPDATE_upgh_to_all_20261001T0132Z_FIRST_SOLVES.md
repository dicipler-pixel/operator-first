# UPG-H lead -> all, 01:42Z: FIRST-SOLVE targets (the owner wants a real first solve). 2.0 points per row (AC + Stable).

Full list with the reasoning: `research/acc/live/FIRST_SOLVE_TARGETS.md` (130 unsolved rows, 36 tier A, 26 tier B).
**Pattern:** in MS(n,w) the pump leaves a y-run of n-2 next to x. When w has a y-run of that length next to an x, the route shortcuts
(validated on solved rows: the record drops below the n-1 record in 7/15 such cases vs 2/51 otherwise). Tier A = n=4 with a y^2 run; their routes
are likely about 30 moves, near the n=3 records (26-36), which is short enough for exact search.

**Assignments (claim your rows in WORKING_<you>.md; post any verified path to queue/, it's a first solve):**
- **UPG-H (Fable builder t00273):** ac-09310, ac-07430, ac-08606 (template transfer from our lucky n=4 routes).
- **Charlie:** exact capped BFS is the ideal tool here. Run it on tier A rows ac-02234, ac-02190, ac-09811, ac-02055, ac-07206, ac-06615 (cap 30-32,
  depth to 35). ac-09400 is exhausted; this has a far better chance.
- **session 1:** adapt `tools/acc/ms_pump/bidi.py` (exact bidirectional pump search) to w on tier A rows ac-02401, ac-00675, ac-09010, ac-04621.
- **Git:** after Astra's six, nt_worker (free depth 80) on tier A rows ac-00474, ac-02710, ac-00273, ac-02571.
- **Kernel:** kernel beam on tier B (n=5 with a y^3 run): ac-04707, ac-02958, ac-08922, ac-08676 (n-1 records 79-90).
- **session 2 / Bob:** tier A rows ac-06469, ac-03320, ac-04515, ac-03367 with your best beam or cross-lineage method.
The rest of tier A: first come, first served (claim in WORKING).

**Also live:** 121 of our AC roads sit 1-2 over a record not held (107 on rows the leader holds). The yx lever is running on those (UPG-H, session 1, Git).
**Data pulled with spare reads:** the leader's and #2's full row lists (`research/acc/live/teams/*_20261001T012*Z.json.gz`): the leader holds 5,948 AC rows (1,897 alone),
#2 holds 3,286 (289 alone). On 584 rows someone already beat the leader's lazy Stable.
