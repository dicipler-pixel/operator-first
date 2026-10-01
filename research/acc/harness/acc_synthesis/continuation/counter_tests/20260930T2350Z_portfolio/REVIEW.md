# Eight-way geometry and clock comparison: ac-00009

**Outcome: the independently verified saved best remains 78 paid moves.** Both eight-arm batches completed their declared record ceilings normally. There was no crash, kill, wall-time timeout or candidate to send. No live scoring claim.

| Arm | First retained states | Cycle-free retained states | Best paid length |
|---|---:|---:|---:|
| length | 217 | 231 | 78 |
| toward | 235 | 268 | 78 |
| away | 235 | 370 | 78 |
| fixed_heading | 235 | 290 | 78 |
| local_heading | 240 | 257 | 78 |
| local_heading_reverse | 249 | 285 | 78 |
| layer_clock_heading | 228 | 262 | 78 |
| reverse_toward | 394 | 667 | 78 |

The first experiment retained removable exact-state cycles in 69–87% of its beam labels. The complete successor forbids revisiting an exact state on the current prefix and keeps that ancestor set in the history identity. All other scores, ceilings and beam settings are unchanged. Exact loop deletion preserves endpoints and lowers paid cost; no global optimality follows from either beam.

The pooled graphs contain 1027 and 1462 exact states, a 42.4% increase in count. Their shortest witnessed paths are both 78. Pool-only discoveries would have been attributed to the pool, rather than a single score.

Code execution: 2.608s and 3.339s; peak RSS 34.28 MiB. These are computation times, excluding implementation, audit and GitHub persistence. Records charged: 482533 and 483217, each below 600,000.

Independent audit replayed 6706 pooled primitive edges and 35358 retained labels using pinned official moves. The second batch has zero exact-state cycles in retained prefixes.

The tested feature map is an explicit Sanov matrix/Cayley representation. It does not instantiate a physical Maxwell/gravity law. Fixed versus moving chart heading, shared versus relator clock, reverse heading and reverse search are separate hypotheses. Every comparison uses exact states for junctions and the official paid metric.

Decision: retain the improved trace and loop controls; no score wins on route length. Park both keys. A next experiment needs fresh useful path data or a separately justified bridge mechanism; increasing width or renaming a score is not justified by this miss.

All inputs, source snapshots, per-layer states/paths/history, budgets, exact graphs and result hashes are preserved in the two run directories listed in comparison.json. Both experimental registry entries are disabled after this explicit comparison; other continuation lanes remain unchanged.
