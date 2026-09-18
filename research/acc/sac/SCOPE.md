# ACC session scope — 18 September 2026

Full accounting of this session: what was recovered, built, found, delivered,
and what failed. Written so none of it needs to be reconstructed again.

## 0. How the session started

The conversation was auto-compacted and the summary was wrong: it recorded the
only user message as "hello" and dropped the entire ACC thread. The real
history was recovered from the on-disk transcript
(`~/.claude/projects/.../134a87db-....jsonl`, 21,213 lines, 467 user messages).

Four outstanding asks were recovered. Three had been answered; the fourth —
a paste of the full Stable AC board — arrived 11 seconds before `/compact`
and had never been read.

## 1. The central correction

`sac-NNNNN` and `ac-NNNNN` are the **same presentation**. All 19 held AC
certificates replay to `(x, y)` against the SAC relators, 19/19. All 276
submitted SAC paths reach `(x, y)` using only moves 0-13; the trailing
`[16, 15]` does no search work.

The earlier claim that these were different problems was wrong.

## 2. Official specification recovered

The competition repo `SAIRcompetition/Andrews-Curtis` was already cloned in
this container; the compaction erased that fact. From it:

- move 14 = stabilize, 15..22 = destabilize `r_i`
- `target_relators: []` — Stable AC targets the **empty presentation**
- `[16, 15]` from `(x, y)` is the canonical two-move finish
- limits: 500 lines/file, 40 submissions/day, 100,000 moves, 10,000 letters,
  5,000,000 work, 8 generators, 10 MB
- scoring: the `k` teams tied for shortest each get `2^(1-k)`; sole shortest
  is a full point

`tools/acc/eyes/replay_sac.py` implements moves 0-22 from that spec
independently. Cross-validated: all 276 externally accepted paths replay
clean, so it agrees with the official verifier on data we did not produce.

The official verifier itself could not be executed (sandbox blocks running
external repo code). `build/private/` on their prep branch was left unread
deliberately.

## 3. What was built

| file | what it does |
|---|---|
| `sweep.py` | meet-in-the-middle against a fixed ball around the trivial presentation |
| `compress.py` | exact bidirectional re-search of every 6-move window of a path |
| `minimality.py` | exhaustive proof that a path is the shortest that exists |
| `climb.py` | best-first on abelianised distance, for rows with no length gradient |
| `transport.py` | splice an unsolved row into a path we already hold |
| `eyes_census.py` | 12 independent theorem-eyes, recorded per target before mixing |
| `canon8.py` | canonical form under the 8 signed generator permutations, plus path transport |
| `check_limits.py` | submission file against every published limit |

## 4. Results delivered

238 verified submissions (`BEST.txt`): 20 AC + 218 Stable AC.
Of the Stable AC rows, 188 are strictly shorter than the previously
submitted path and 30 were never submitted. 736 moves saved. No duplicate
ids; nothing longer than what was already held; 0 replay failures; passes
every limit.

Compression was the engine: 177 of 276 held paths shortened, 52% hit rate,
in under seven minutes. Largest gains `sac-03576` 41->23, `sac-03855` 38->22,
`sac-09868` 42->27.

Minimality proved 10 paths shortest-possible and found 5 strict improvements
(`sac-00343` 20->17, `sac-09846` 19->16, `sac-02761` 17->16, `sac-03812`
17->16, `sac-05532` 18->17).

## 5. What failed, stated plainly

Against the AC board records we hold **0 first solves and 0 beats**: 39 ties
and 185 rows longer than the standing record. Every row we hold was already
solved by someone else.

The board is 7,443 solved / 2,672 open. We solve **none** of the open rows.
The full-board sweep, the plateau climber and the transport splice have all
returned zero on them.

## 6. Why, measured rather than guessed

The harness profiled all 2,672 open rows: **every one has zero
length-reducing moves and zero collapse gain**. They sit at a local minimum
of total relator length, so a search keyed on length has no gradient at all.
That is a property of the target set, not a tuning failure.

The eye census over all 10,115 targets, against a 73.6% base solve rate:

| eye | hits | solved | lift |
|---|---|---|---|
| DOWNHILL | 1,052 | 100.0% | 1.36 |
| CHILD-COLLIDE-SOLVED | 141 | 100.0% | 1.36 |
| ABEL-DM1 | 125 | 96.0% | 1.30 |
| DET-UNIMOD | 10,115 | 73.6% | 1.00 |
| BALANCED-LEN | 240 | 50.8% | 0.69 |
| SHORT-TOTAL | 254 | 42.5% | 0.58 |

Short and balanced are markers of **difficulty**, not ease. Combined shapes
beat any single eye: `BALANCED+SHORT` is 86% unsolved, `ABEL-DM1+SHORT` is
100% unsolved.

Named hardest rows: `sac-00008`, `sac-06194`, `sac-09571` (abelian-close and
short); `sac-00413`, `sac-02089`, `sac-03467`, `sac-04376`, `sac-05932`,
`sac-08126` (balanced and short).

## 7. Symmetry structure

Under the 8 signed generator permutations the board collapses from 10,115 to
8,711 classes. **No open row collides with a solved row**, so the open set is
not disguised duplicates. But the open rows collapse among themselves from
2,672 to 1,655 classes: 821 classes hold more than one open row, covering
1,017 duplicates, with classes as large as 6.

Path transport across the symmetry was tested, not assumed. A relabelling
sends the target `(x, y)` to a signed permutation of itself, so 8 of the 16
symmetries are usable once 0-2 correction moves are appended: **1,744
transports, 0 failures**.

Consequence: search 1,655 representatives instead of 2,672, and one solve in
a 6-row class yields all six at worst +2 moves.

## 8. Still missing

Stable AC records (`currentBestLength`, `kTeams`) are authenticated-only and
this container's proxy refuses every `sair.foundation` host. Without them the
238 are verified and internally ranked but unpriced: we know they are shorter
than the previously submitted paths, not whether each takes sole shortest.
