# Astra evaluation and handoff — 2026-09-28 23:12 UTC

**PAUSED at the user's request. Do not restart without new authorization.**

The retained execution session exited with code 130 after interruption. A fresh process scan at 23:12:11 UTC found neither ranked runner host PID 716632 nor its beam child PID 746263, and no other search from this workspace. The Astra hourly rally automation is disabled. The kernel relay search had already exited normally. No other worker's process was signalled.

## Delivered results

| Item | Result | Evidence / limitation |
|---|---|---|
| Ranked list | 17 / 149 actual entries finished (orders say 150): 2 tie rows, 3 above-record rows, 12 bounded misses | Exact assigned W=20000 settings; original binary unchanged |
| ac-06403 | AC 22 and Stable AC 24 | Both tie the supplied snapshot records; pinned official verifier accepted; inboxed |
| ac-09311 | AC 42 and Stable AC 44 | Both tie the supplied snapshot records; pinned official verifier accepted; inboxed |
| ac-09219 | AC 45 versus 43; Stable 47 versus 45 | Both verified; two-move miss handed to session 2 for twin escalation |
| Other above-record paths | ac-08328 AC47 versus37; ac-01443 AC30/SAC32 versus24/26 | Preserved in the sweep; not hits |
| Kernel relay, rows 101–213 | All 113 rows completed; 226 attempts; zero AC or Stable paths | Two modes per row, W=2000, depth80; all exited normally at depth80, zero timeouts/errors |

This is **four officially verified snapshot-tie lines on two rows, zero outright record beats, and no confirmed scoreboard points claimed**. I made no SAIR API reads or submissions. Only session 2 submits.

The two hit inbox files are:
- `inbox/20260928T221036Z_astra_ac-06403.txt` (commit `89bc2776a7e08172115e7697f50043490f6bb08f`).
- `inbox/20260928T2238Z_astra_ac-09311.txt` (commit `59a865b921f325d2476f35bc486a11c0632caaae`).

Verifier checkout: SAIR `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`. New +2-miss checks: `ledger/astra_rank_checks_20260928T2301Z.json`.

## Most reusable contribution: identical decisions with less P2 computation

I replaced the quadratic least-rotation comparison in P2 canonicalization with the linear algorithm already used elsewhere in the engine. This is an isolated proposed patch, not a new scoring heuristic.

- 374,101 rotation-index comparisons: zero mismatches.
- 14,581 archived-state P2 score comparisons from 526 paths: zero mismatches.
- Twelve matched W=2000 beam pairs: identical returned paths and printed frontier data after removing elapsed time; returned paths passed official replay.
- Three repeated-control medians: 10.9%, 16.1%, and 15.0% less elapsed time.
- One additional W=20000 control: 83.194 seconds versus 116.853 seconds, 28.8% less elapsed time, identical AC22/SAC24 paths and frontiers.

Timing came from a machine running concurrent work; the single 28.8% result is not a general speed guarantee. The benchmark and patch are ready for another worker to inspect. Package: `research/acc/optimality/experiments/astra_p2_linear/`; original package commit `a9673d14b47e0fc40607d657eef0eda7a5a2c03f`, production-width control `dc697c7ab2ed2ee21fb3f526822439136c205d75`.

## Ideas tested and what they taught us

1. **All eight signed finishing bases:** audited 526 archived paths / 14,581 distinct states; 3,338 AC/Stable tails replayed successfully. Extra lookup coverage: 190 states over direct AC, 151 over both positive Stable targets. Six row/board routes improved beyond the existing target scan, but none supplied a new qualifying scoring line. All 11 ties from the full scan were already sent. This was an archive audit, not a live-beam win.
2. **Generalized Stable multiplication-block shortcut:** a construction with cost `2k + 3 floor(m/k) + (m mod k) + 4` first saves moves at m=35. The 526-path archive had maximum repeated multiplication block18; seven stored Lisitsa constructions had maximum2. This particular shortcut had no target here, so no large search was spent on it. This does not rule out other stabilization methods.
3. **Kernel odd-easy relay:** dual P2/H and balanced H both failed on all113 rows under the recorded limits. This is a clean bounded negative, not an impossibility proof. No dead ends were skipped. Every literal relay start matched the official manifest and assigned slice.
4. **Coordination finding:** the same113 relay was also sent to Claude Kernel, Charlie and Bob using different methods. My ZIP identifies this run as Astra (ChatGPT Work Mode), and its counts are separate. The overlap limits how much independent row coverage this assignment added.
5. **Review of existing team work:** older Snell/Smith primary-score proposals had already been tested or corrected by other workers. I did not count them as new discoveries or rerun them as a fresh idea. Abelian/geometric diagnostics alone do not establish a useful search ranking.

Unrun ideas retained for evaluation: a controlled minority-slot literal-access-cost eye (`real2_d1`), and constructive primitive-relator/Nielsen endpoint methods for difficult long rows. Neither is a result, and neither is now running.

## Preserved handoff and unfinished work

Final kernel ZIP in Mad Hatters ACC Shared Hub:
https://drive.google.com/file/d/11PYMy8bgrTqLYczOwLC7ja5oRD0n8nhU/view

It contains ledger/, raw logs, exact settings, executed source, checksums and an empty inbox/. Final size229353 bytes; SHA-256 `53e320a1b7798ca9ab9231c4ac613533156368181e436946b413a8a61a3c1ff7`.

Ranked checkpoint: `research/acc/live/sweeps/astra_rank_cap.jsonl`, now17 complete rows. Row18, ac-08247, was interrupted and is **not** recorded as a completed negative. The 75-row solo list has not been started. Any authorized resumption must first re-read the fresh rk2 collision boundary; the last read had33 completed rk2 rows and no overlap with my completed prefix.

Local setup is preserved: pinned verifier, original binaries, isolated speed-test binaries, 640MB T8 reverse table, raw output and experiment data. T8 SHA-256: `38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8`.

For evaluation: my demonstrated value is the four verified tie lines plus a reproducible throughput patch. The broad relay produced no solve, the other two shortcut audits produced no new points, and I have no proof breakthrough to claim. All search work is paused.
