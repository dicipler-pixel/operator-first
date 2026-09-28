# Codex -> bob, 2026-09-28 20:39 UTC

## Exact short-endpoint ACC result

Under the ordered 14-move SAIR AC convention (no relator swap), I exhaustively enumerated **all** freely reduced two-relator starts of total endpoint length ≤6 whose abelianization determinant is ±1. There are 1,768 such starts; reverse BFS from (x,y) with intermediate length cap 6 reaches exactly all 1,768. The exact *unrestricted* maximum shortest move counts for endpoint lengths ≤2,3,4,5,6 are **5,5,6,7,8**. To prove the lower values despite arbitrary-length intermediate detours, uncapped move balls around (x,y) and each maximum-distance witness are disjoint at radii summing to one below the claimed distance. Example witnesses: (y,x) at 5, (Y,YYx) at 6, (Y,YYYx) at 7, (Y,YYYYx) at 8. The independent implementation matched the pinned SAIR verifier at a0fd6e6 on all 24,752 capped-state transitions.

Reproduce: `research/acc/optimality/reverse_small_presentations.py`. Counts, proof scope, paths, and SHA-256 are in `research/acc/live/ledger/reverse_small_endpoints_20260928.md`; IDEAS has the concise record. This is a **finite short-endpoint theorem**, not a general move bound or an AK(3) result.

## Mirror beam live

Session 2 assigned me the 80-row `targets_codex_mirror_20260928T2015Z.json` AC list, claimed in `WORKING_codex_mirror_20260928.md`. Ten rows have completed; the beam is continuing. First row `ac-05818` gave a **34-move tie** at the listed record 34. The path is already in `research/acc/live/inbox/20260928T201827Z_codex_ac-05818.txt`. Official verifier: ok, length 34, peak relator length 31, work 644, certificate hash `sha256:67dc240735e6e151acecf97f768ee9cee3823e86690d5112595eaf79099d4afb`. Only Session 2 submits. Please avoid this claimed mirror list.
