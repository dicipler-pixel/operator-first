# Every way we know to get a road: what we have, what is broken, what we have never tried (14 Oct 2026)

Status words:
- DONE (works, run to a fixpoint);
- RAN (tried, no gain, with scope);
- BROKEN (did not run as we thought);
- NEW (never tried).

## A. Splice: combine roads we already hold
| Way | Tool | Status |
|---|---|---|
| Overlap splice (two roads pass within 2 moves) | `tools/acc/overlap_splice.py` | DONE |
| Class splice, orientation splice | Git's tools | DONE |
| Road DP: exact shortcuts between any two states on a road | `tools/acc/ops/` (session 2) | DONE. It gave our 00071 tie |
| Tail meet: exact 13-move finish from every state, to (x,y) and (y,x) | partner, `orows/tailmeet.py` | DONE on 27 rows, 0 gains |
| Foreign meet: borrow another row's finish through a shared state | `upgh/foreign_meet.py`, partner fm2 | DONE (9 shorter, 0 ties) |
| Global webs: height, Stable, recognition, twist | `upgh/height_web.py`, `stable_web.py`, `recognition_web.py`, `twist_web.py` | DONE. Our best tool (31 ties + 1 beat). Moves only when NEW roads arrive |

## B. Extend / transfer: move a road to another row
| Way | Tool | Status |
|---|---|---|
| 16 symmetries, twin rows | `twin_lookup.py`, `crossrow.py` | DONE |
| Nielsen twist (automorphism of F2), exact transfer (P6) | `twist_web.py` | DONE |
| Join onto a known trajectory (multi-target bidirectional) | `ladder_law/join_bidi.c` | RAN on the doubling ladders (+4 over the k1 records). Not run cross-ladder |
| Ladder frame maps and frame finishes | `ladder_rows.py` | DONE (XXYxy) |

## C. Search: find a new body
| Way | Tool | Status |
|---|---|---|
| Beam: H, P2, DUAL two eyes, BAL, NOISE/SEED, CLIMB, MACROS, C16 finish | `optimality/acc_beam.c` | **BROKEN 6-14 Oct on the container.** The cached binary ignored P2/DUAL/ELITE/NOISE/SEED/CLIMB. Fixed 14 Oct 02:20Z. Re-running: the real engine now finds 00669 at 45 (the plain beam found 64) and 03975 at 50 (plain: none) |
| Exact capped BFS, rising caps | `acc_capped.c` (+ Bob's disk-backed capbfs8/9) | DONE; certificates in `catalog/` |
| Meet in the middle, capped forward and backward balls | `acc_opt` / partner MITM | DONE (scoped misses) |
| Mid-restart: beam from every state of our road | `mr_lane.py` | RAN, but on the plain binary since 6 Oct, so redo the important rows |
| Best-first, priority = length + w·depth (P000011) | `acc_bestfirst.c` | RAN, w = 8/12/16, 60M nodes: nothing <= record on 00009 / 00018 |
| **Substitution supermoves**: search over cyclic words, splicing one relator into the other wherever letters cancel; one action = many elementary moves; ~1600x more efficient greedy search | Caltech AC-SolverX (ICML 2026, `github.com/Math-AI-Caltech/acsolverx`) | **NEW.** We never searched in cyclic-word space. Our beams pay for every rotation inside the search |
| Learned policy/value (PPO + Dual-Ring Transformer, solves 610/1190 MS; 100+ previously open MS rows) | AC-SolverX `ppo_checkpoints/610model` (weights and stored solve paths) | **NEW.** Not used. Its stored paths may convert to roads |
| Datasets as donors: AC-19 (exhaustive enumeration), AC-1M (automorphism game) | AC-SolverX `data/` | PARTLY: AC-1M was matched to unsolved rows on 1 Oct, AC-19 never |

## D. Shorten: polish a road
| Way | Tool | Status |
|---|---|---|
| Window-14 exact replacement, fixpoint, commute cleanup | `acc_window.c`, `fixpoint_shorten.py`, `commute_clean.py` | DONE (gave the 2 beat pairs on constructed roads) |
| Universal move identities (P7) | Kernel | DONE |
| Stable via (y,x) + [15,15]; yx_shortcut | `yx_shortcut.py`, `stable_web.py` | DONE (299 completed misses listed) |

## E. Construct: mathematics
| Way | Tool | Status |
|---|---|---|
| BS doubling P1 (2^(n+1)), (n+1)-block P2, step-2 finA2 | `bs_doubling*.py`, `fable_build.py`, `loop_macro.py` | DONE (now beaten by memcon) |
| **memcon's construction**: records ≈ 2^n + 10·2^(n/2) on 5 ladders, partly on 2 more | — | **NEW and OPEN.** Exponent-sum bound: about 2^n multiplications are unavoidable, so their roads have almost no rotations. Matches the "plan in cyclic space, pay rotations cleverly" idea in C |

## F. Reverse-engineer from data
| Way | Status |
|---|---|
| Ladder law (affine, then 2^(n+1)+c, then memcon's 2^n + c·2^(n/2)); top-team holdings; record histories | DONE today (`TOP_TEAMS_METHODS_BESTGUESS_20261014T0030Z.md`) |
| Isospectral families (which row families moved by the same law) | DONE today: only the 5 + 2 MS ladders |
| Board-map clustering (t-SNE/UMAP) | DONE 6 Oct: solved rows cluster, 4x enrichment |

## G. Guess / random
| Way | Status |
|---|---|
| Noisy seeded beams, new lineages | **BROKEN on the container** (seeds were ignored). Session 1's seeds 13-19 ran elsewhere and worked |
| Random restarts, climb-then-collapse (Bob) | RAN, scoped |

## The obvious things we were missing (found today)
1. **The beam binary.** A week of "dual-P2 / seeded" lanes on the container were plain beams. Re-run the high-value rows with the real engine.
2. **Cyclic-space planning** (substitution supermoves) with cheapest-rotation realization. Never built. It is the best match for memcon's "almost no rotations" signature.
3. **Public learned solvers and data** (AC-SolverX weights, stored solve paths, AC-19). Not mined.
4. The ACC Drive hub has not been re-inventoried since 1 Oct (see `HUB_INVENTORY_20261014.md` once written).
