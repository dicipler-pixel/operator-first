# ac/sac-09839 four-road graph map (Codex Stable, 2026-09-28 23:26Z)

Pinned SAIR verifier a0fd6e6. Source AC route is the Codex mirror worker's `inbox/20260928T230433Z_codex_ac-09839.txt`. All four full Stable paths below passed `stable_core.verify`. Board snapshots: AC 44 moves, k=1 (20:50Z); SAC 46 moves, k=1 (20:23Z). The AC44 line and the derived SAC46 line are in the inbox for Session 2; neither was submitted by this worker.

| Road | First 17 AC moves | Remainder | Rank-2 endpoint | Stable length | Peak total length | Source |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| AC mirror | Shared | 27 | (x,y) | 46 with two deletions | 38 (step 4) | Mirror worker's AC inbox |
| Letter-swap yx | Shared | 27 | (y,x) | 46 | 38 (step 4) | `sweeps/codex_sac09839_yx_W20000_20260928.jsonl` |
| Restart at step 17 | Shared | 27 | (y,x) | 46 | 38 (step 4) | `sweeps/codex_sac09839_mid_yx_20260928.jsonl` |
| Restart at step 17 | Shared | 27 | (x,y) | 46 with two deletions | 38 (step 4) | `sweeps/codex_ac09839_mid_xy_20260928.jsonl` |

The common state after 17 moves is `(xYXyx, yXXyyxYXYX)`, word lengths (5,10), total 15. This is a natural road junction: a 26-move remainder to (y,x) would give a 45-move Stable beat; a 26-move remainder to (x,y) would give a 43-move AC beat. The first restart used W20k, BEAM_H=1 DIV=.8 P2=2 QUOTA=16 ELITE=5000 DUAL=.75, DMAX26. It found another 27-move yx remainder. The matching xy restart also found a 27-move remainder: another official AC44 tie, no beat. Window11 on both restarted paths and all 0–3 move pairwise bridges between four roads found no cut. A different commutator tie-break at the junction is next.

Exact-state splices and every 0–3 move bridge between each pair of roads found no shortening. The largest ordered cyclic-class overlaps permit a five-step index gap; targeted breadth-first bridges of up to four AC moves for all eight such oriented pairs found no join. Window11 completed unchanged on the AC44 and first yx44 route. C16 queried 16 eligible swapped prefix states of AC44 and found best Stable finish 47, so that low-height tail gives no beat. These bounded searches do not establish a global 46-move optimum.

Next useful attack: change the ranker at the shared state or allow a longer relator-length climb. Keep the junction state and target endpoint explicit; the late roads differ while the first 17 moves are identical. The opposite orientation showed a new 46-move path, and the initial SAC46 inbox line remains valid.

Reproduce the junction with `tools/acc/ops/mid_route.py`: supply the pinned manifest, the mirror worker's 44-move AC path as a JSON array, `--row ac-09839 --cutoff 17 --mode yx --width 20000 --depth 26`, plus the beam binary and T8 table. The generic script replays both the source AC path and returned route using the pinned verifier.
