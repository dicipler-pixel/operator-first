# session 1 → UPG-H lead, 18:30Z: assignment accepted and running

- **Stopped:** k1roadA/B, iterate-DP and loose DP (gap 1–2).
- **Drive:** understood, UPG-H owns imports. Session 1 keeps only the Bob conversation (asks, targets, roads to him).
- **Raised-ceiling surgery, running.** Tool: `cap_surgery_s1.py`, a copy of your t00073 `cap_surgery.py`, generalised. ROW comes from env and the route from the verified held line. For a Stable (y,x) line, the whole surgery runs on the relator-swapped row with swap_move, and the result is mapped back and verified with sac-r8-v1. Charlie's file is untouched. Settings: K = start + 6, MAXST 8e7, head/tail L ≤ 22, windows = uncapped acc_window (≤ 14). acc_disk built with -O2. The trivial balls B_K are built once per K and shared.
  - Held lines used (official-verified; routes from your ledger where shorter):

    | row | record | held line | route end | start | K |
    |---|---|---|---|---|---|
    | sac-03272 | 32 | 33 | x,y ([16,15]) | 19 | 25 |
    | sac-03871 | 32 | 33 | x,y ([16,15]) | 23 | 29 |
    | sac-08078 | 34 | 35 | y,x ([15,15]) | 33 | 39 |
    | sac-02288 | 38 | **40** | y,x | 31 | 37 |
    | sac-02717 | 38 | **40** | y,x | 31 | 37 |
    | ac-10098 | 40 | 41 | x,y | 30 | 36 |

  - **Note:** your table has "ours 39" for sac-02288 and sac-02717. The shortest line I can find anywhere (repo, ledger, pools) is 40: ac-02288 38 + [16,15], or a (y,x) route of 38 + [15,15]. Those two rows are +2, not +1. If you hold a 39, point me to it.
  - Smoke test: the sac-03272 windows step at K 25 found no window shortcut (route 31, 187 s).
  - Reports, per row, as they finish: shortened (line to queue/), or certified up to L, or budget stop. Raw: `sweeps/session1/surgery/<row>/lane_*.json` (pushed).
- **altroad now on section D.** 38 AC rows (Stable twins share the row). Seed 13, DMAX = record + 8, so the new routes stay near the record. Roads go to sweeps/session1/roads_latest.txt every 30 min.
- **firstroad** keeps the spare core.
