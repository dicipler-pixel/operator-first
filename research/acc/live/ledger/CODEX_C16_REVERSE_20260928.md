# Codex reverse-finish and crossover checkpoint — 2026-09-28

Owner: Codex Helper A. Branch: `claude/gallant-bardeen-0pgpae`. Pinned official verifier: SAIR `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`. Board comparison: snapshot `20260928T1856Z`; refresh before preparing a submission. **No new scoring line from these experiments.**

## Complete reverse graph inside total relator length 16

Built `acc_c16` from `research/acc/optimality/acc_c16.c` with `C16_TMAX=1200`, ceiling 16, 268435456 build slots and 236000000 state budget. The BFS **closed**, with 129247304 reachable states and maximum cap-restricted distance 100, in 350.5 s; compacted table 1.48 GB in 359.3 s. Local `work/C16.tab` SHA-256: `3a396a42ecf63390275b2c0110bc816fae6767e2dd1a67945969c609565f2df4`. This is distance inside the ceiling graph, not an unrestricted shortest-path certificate.

Validation: `acc_c16 sample work/C16.tab 1000 1734 work/C16_sample.txt` checked 6567 in-ceiling neighbors: zero closure or distance inconsistencies and zero failed descents. `c16_verify_sample.py` replayed all 1000 descents with the pinned official AC verifier; all reached (x,y) at their recorded distances, and none exceeded length 16. No OOM in the 8 GiB container.

Rebuild:
```sh
gcc -O3 -march=native -o work/acc_c16 research/acc/optimality/acc_c16.c
C16_TMAX=1200 work/acc_c16 build work/C16.tab 16 268435456 236000000
work/acc_c16 sample work/C16.tab 1000 1734 work/C16_sample.txt
python3 research/acc/optimality/c16_verify_sample.py SAIR/competition/tools work/C16_sample.txt 16
```
The resident `acc_c16 batch TABLE INPUT OUTPUT` command now supports multiple lookups without loading 1.48 GB for every query. `c16_splice_path.py`, `c16_scan_starts.py`, and `c16_scan_sac_swaps.py` are pushed next to it.

## Scored-row probes

- All 254 AC starts with initial total length <=16: 57 are in the reverse component. Officially verified paths tied five existing records: ac-01635 (8, k40), ac-04359 (17, k20), ac-06500 (15, k26), ac-07445 (13, k32), ac-08491 (8, k42). No beat or unsolved-row solve.
- The swapped finish plus two stable deletions checked 254 SAC starts; 57 in the component. Officially verified ties: sac-01635 (10, k35), sac-07445 (15, k31), sac-08327 (19, k20), sac-08491 (10, k40). No beat or unsolved-row solve.
- Spliced every eligible state of seven saved one/two-move misses from `sweeps/p2v_cap.jsonl`: ac-05149, ac-00975, ac-10098, ac-02341, ac-08889, ac-06737, ac-04286. None shortened.
- The same W20000 two-eyes beam, now with `BEAM_C16=work/C16.tab`, produced: ac/sac-00975 35/37 vs records 34/36; ac/sac-05149 34/37 vs AC record 33; ac/sac-02341 30/32 vs AC record 29; ac/sac-00145 47/50 vs AC record 39. Every output was replayed through the pinned official AC/Stable verifier. On ac-00975 the C16 finish generated a **different** 35-move route, but did not tie; it had 94377 C16 lookups and 2 intermediate AC/1 SAC improvements. The other three beams did not score.
- On ac-00975, exact `acc_window` examined all 36 path states, each possible pair no more than 14 moves apart, and repeated states; one pass, 207.6 s, **no shortcut**. An exact B6/B7 bridge between its states 12 and 24 also failed. Two additional exact bridges across the ac-05149 hump (states 12→24 and 13→26) failed.
- `acc_window_cross.c` tested the two distinct ac-00975 paths: exact B6(A_i) intersection B7(B_j) at (i,j)=(12,24),(10,24),(12,25),(13,26),(16,28),(17,28). None gives a path <35. A separate depth-3 crossover scanned 52829 nearby states and found no gain. These tests cover the named windows only; they do not prove the unrestricted 35-move path optimal.

Helper A two-eyes assigned list: 32 of the refreshed 82 rows complete when this note was written, no tie or beat in the local cap log. Process continues in `work/dualA_resumed_20260928.jsonl`; only session 2 sends. This note does not add any line to the sender inbox.

## Next search direction

The early ac-00975 states at moves 12, 16, 17 (total relator length 16) are **outside** the cap-16 identity component; at move 24 the path re-enters it. A shorter route must alter the excursion, or use a ceiling above 16. The short internal windows and the six named crossovers are already covered. Use a different bridge, rank/heuristic, or higher ceiling, and record the exact scope; do not claim global optimality from the closed ceiling graph.

## Commutator tie-break follow-up

The offline `SCORE_ZOO.md` identified `comm_len` as a useful word-level tie-break. Matched beam settings on the two sole-holder one-move misses were `BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=3 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 BEAM_C16=work/C16.tab`, W20000; only the `BEAM_P2` mode differed from the prior C16 beam (`2`). On ac-00975 it found a distinct official-verified AC35/SAC37, still above 34/36. On ac-05149 it found no path within depth 35, worse than mode 2's AC34. Thus the offline ranking gain did not translate to these two scored rows. Across all three AC35 ac-00975 paths, a directed depth-3 crossover scan of 318538 local states found no route of 34 or less. This is a bounded negative test, not an optimality proof.
