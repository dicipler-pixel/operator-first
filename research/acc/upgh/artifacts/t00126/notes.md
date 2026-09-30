# t00126 mirror starts (phi(S) beam, map back)

Settings: acc_beam, T9, BEAM_H=1 DIV=0.8 P2=2 QUOTA=16 ELITE=5000 DUAL=0.75 NOISE=2 SEED=101 FREE_DMAX=20 (DMAX=record+20), W=20000, nice 10, one process at a time.
phi x = (x->X), phi y = (y->Y), phi xy = both. Driver: mirror.py. Raw beam outputs: work/*.out. Per-run JSON: results.jsonl.
Every mapped route below was replayed from the official start S with the pinned core (a0fd6e6): ok, ends exactly at (x, y). Mapped step k = the move id m with m(phi(t_k)) = phi(t_{k+1}); inversion ids 0 / 1 appended at the end (one per inverted generator).
Window-14 shortening of the raw S' route (75 s cap) found nothing shorter on any run that was attempted (raw <= record+12 only for ac-02386 and ac-04316).

| row | phi | raw mirror AC (on S') | mapped AC (from S) | record | ours | shared states with our best path |
|---|---|---|---|---|---|---|
| ac-03913 | x  | 59 | 60 | 46 | 48 | 3 |
| ac-03913 | y  | 59 | 60 | 46 | 48 | 3 |
| ac-03913 | xy | 59 | 61 | 46 | 48 | 3 |
| ac-02386 | x  | 36 | 37 | 34 | 36 | 5 |
| ac-02386 | y  | 37 | 38 | 34 | 36 | 6 |
| ac-02386 | xy | 37 | 39 | 34 | 36 | 5 |
| ac-04316 | x  | 45 | 46 | 43 | 45 | 11 |
| ac-04316 | y  | 45 | 46 | 43 | 45 | 31 |
| ac-04316 | xy | 45 | 47 | 43 | 45 | 22 |

The mapped length is raw + 1 for a single inverted generator and raw + 2 for xy (the final state phi((x,y)) needs one inversion per inverted generator).

No mirror route ties or beats a record or our best. Best mirror-lineage roads (new lineage, for joins): ac-02386 phi=x (37; only 5 states shared with our 36-step road), ac-04316 phi=x (46; 11 shared states), ac-04316 phi=y (46; 31 shared, so the closest to our lineage), ac-03913 phi=x/y (60; 3 shared). All 9 routes are in lines.txt, with sac variants (route + [16, 15]).

W=100000 on ac-02386 phi=x (the cheapest, nearest row) was started at 22:25Z and killed at ~22:38Z after 13 min without a result (wall limit). No W=100000 route exists. Scoped miss.
Note: the contract says wall_seconds 900, the launcher said 50 min; the nine required W=20000 runs alone need ~21 min, so the launcher's 50 min was used. One unbounded acc_window on a mapped route (S window) was killed and then dropped from the driver (WIN_S=0 by default); the ac-02386 y and xy and ac-04316 runs used the capped version, the first runs (ac-03913 x/y/xy, ac-02386 x) used the uncapped one (ac-03913 raw 59 > record+12 so no window ran there).
