# Reverse AC graph under complete length ceilings — 2026-09-28 stop checkpoint

We grew the component of the ordered identity pair `I = ([1], [2])` by exact breadth-first search with all 14 `ac-r2-v1` moves in the pinned SAIR core `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`. The ceiling is the **sum** of freely reduced relator lengths, not the maximum individual relator length in Bowman–McCaul. We use literal ordered states: no cyclic quotient, canonicalization, heuristic pruning, or hash-only equality. A cap is complete only if its queue empties. Inverse moves make the paths reversible.

| Total length cap | Complete states | Diameter within cap | Old states whose shortest capped distance fell |
| ---: | ---: | ---: | ---: |
| 2 | 4 | 2 | — |
| 3 | 72 | 5 | 0 |
| 4 | 200 | 6 | 0 |
| 5 | 776 | 7 | 12 |
| 6 | 1,768 | 8 | 8 |
| 7 | 7,784 | 9 | 22 |
| 8 | 18,344 | 10 | 124 |
| 9 | 74,856 | 12 | 528 |
| 10 | 169,992 | 13 | 1,038 |

Cap 11 hit the 500,000-state guard with 177,256 states still queued. Its 500,001 seen states are **incomplete**; we make no diameter or barrier claim there.

## Three separate coordinates, witnessed

1. **Minimum height barrier.** `P=([-2],[-1])` has total length 2 but is absent from the complete cap-2 component. It first enters at cap 3. The route `I→P: [2,0,4,3]` peaks at 3; the reverse `P→I: [2,5,0,3]` replays in the official move core. Thus its minimum total-length route height is exactly 3.
2. **Minimum height versus shortest route.** `Q=([1,2,-1,2,1],[-2,-1])` has total length 7. Its shortest cap-7 route is seven moves, `[1,5,2,0,6,3,7]`, peak 7. Its shortest cap-8 route is **four** moves, `[2,11,2,5]`, peak 8. Complete unrestricted breadth-first search to depth 5 finds Q at depth 4. Thus its unrestricted shortest distance is exactly 4, but every four-move route rises above length 7. A longer route avoids that climb. Both witness paths were separately replayed against the pinned core.
3. **Longest shortest path at size two.** The abelianization determinant is ±1 under each AC move. Hence a reachable total-length-two ordered pair must be one of eight signed, distinct-generator pairs. Unrestricted BFS through depth 5 reached all eight, with distances `0,1,1,2,4,4,4,5`; the swapped pair `([2],[1])` has distance 5. Therefore `D_2(2)=5` for this exact ordered 14-move convention.

Another cap comparison: `([2,2,1,-2,1],[-1,-1,-2,-1])` has distance 12 within cap 9 and 9 within cap 10, with validated paths peaking at those respective caps. Its **unrestricted** distance may be lower than 9; no global shortestness claim is made.

These synthetic witnesses are not challenge rows and produce no submission. Within-cap diameters are not unrestricted `D_2(L)`. A larger cap can introduce new short routes or connect low-length states unseen below it.

## Reproduce

```
python3 research/acc/optimality/reverse_ceiling_probe.py \
  --verifier-root helperB/SAIR \
  --manifest helperB/SAIR/competition/tools/verifier/data/manifest.json \
  --first 2 --last 11 --max-states 500000 --max-seconds-per-cap 60
```

`reverse_ceiling_profile_20260928.json` stores every depth histogram, cap count, height and shortcut witness, unrestricted radius counts, and independent replay peaks. Core SHA-256: `d2972711dc7008679127a987a8965d41ea1606b0fc50bf67e2e06c71c456b3b5`. Probe SHA-256: `300e9a1d844e5fa2975f7bb774eb8f1c9f8c02f82e5b90f75fd736e80d96c074`.

## Search consequence

A reverse map can serve as an exact endgame table and can show when a deliberately longer, lower-height path is easier to find than a shortest one. This pilot reaches only total length 10. The assigned record-41–52 beam rows sit far beyond it; applying this map to them needs a larger or quotient-aware meet-in-the-middle table and must keep height and distance labels separate.
