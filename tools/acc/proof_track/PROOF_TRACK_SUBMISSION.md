# Exact shortest-path facts and forced "height humps" for the SAIR AC benchmark

**Team:** Mad Hatters, SAIR Andrews–Curtis Challenge
**Track / conjecture / direction:** Proof Track, AC (with Stable AC corollaries), direction **proof**. This is a partial, computational result. It does **not** resolve the AC conjecture.
**Date:** 2026-09-26

## 1. Summary

We give exact, reproducible computational facts about the AC move graph on the 10,115 official rank-2 presentations of the SAIR benchmark:

1. **Exact shortest AC distances** for 53 benchmark presentations whose best-known path length is 15–19. In every case the known length is optimal. Two exact controls pass.
2. **Board-wide lower bounds.** Apart from 32 presentations we list, no official presentation has an AC path of length ≤ 14. None of the 7,352 presentations whose 2026-09-14 best length was ≥ 20 has an AC path of length ≤ 15. The same holds for the generator-swapped target (y,x).
3. **Forced height humps.** For eight presentations, every path of record length (or one move shorter) must pass through a pair of relators whose total length exceeds an explicit bound C within an explicit number of moves. Short paths therefore provably have to grow the relators first. This quantifies the "hump" phenomenon behind the hardness of AC.
4. **An empirical law from 212 exact searches.** For presentations with short starting relators, record-length paths usually stay within 0–5 letters of the starting total length. 71 of 212 exact runs found a record-length path while never exceeding total length 26.
5. **Stable AC.** Finishing at (y,x) and destabilizing gives Stable AC paths that are strictly shorter than "AC path + 2". We give examples where the Stable AC length equals the AC length.
6. **A transport bridge.** An exact 5-move AC bridge links two unsolved presentations, so a solution of one transports to the other.

Every positive statement (a path) is an explicit move list. Each one is replayed by the frozen official verifier (commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`) and accepted. Every negative statement (no path) comes from an exhaustive search whose scope we state exactly, with the hashing caveat in §3.

## 2. Setting

- **Rank and presentations.** Rank 2, generators x, y. The 10,115 official presentations are `ac-00001 … ac-10115` from `competition/tools/verifier/data/manifest.json`.
- **Moves and target.** Move set `ac-r2-v1`: 14 moves, namely two inversions, four multiplications r_i ← r_i r_j^{±1}, and eight conjugations by x^{±1}, y^{±1}. Every result is freely reduced and not cyclically reduced. The target is exactly (r0, r1) = (x, y).
- **The move set is closed under inversion.** The inverse pairs are 0↔0, 1↔1, 2↔3, 4↔5, 6↔7, 8↔9, 10↔11, 12↔13. So "within b moves of the target" and "reaches the target in ≤ b moves" are the same set.
- **Kernel validation.** Our C kernel agrees with `verifier.core.apply_move` on 100,000 random (state, move) pairs, with 0 mismatches. Its target-ball layer counts reproduce 5,115 / 40,779 / 336,477 / 2,849,131 for radius 4–7.

## 3. Method and exactness

**Target ball.** T_b is the set of states within b moves of (x,y). We use:
- T_9, with 214,977,551 states (T_8 = 24,587,144). The table's SHA-256 is `48a81fea88f49c5c9499bde3738b813792c405bedff41b8ddc229f9aee7bb053`.
- Each state's exact distance to (x,y).

**Meet-in-the-middle lemma.** Let S_a be the set of states within a moves of the start. Take any path of length L ≤ a+b. Its vertex at step max(0, L−b) lies in S_a ∩ T_b. Hence:
- If S_a ∩ T_b is empty, no path of length ≤ a+b exists.
- Otherwise, min over s in S_a ∩ T_b of d_S(s) + d_T(s) is the exact distance, provided that minimum is ≤ a+b.

No length cap is used in this lemma.

**Capped lemma (forced humps).** Let BFS_C be breadth-first search from the start that is restricted to states of total relator length ≤ C. Suppose BFS_C completes every layer through depth R−9 and never meets T_9. Then **no path of length ≤ R has its first R−9 states all within total length C.** Equivalently, every path of length ≤ R exceeds total length C somewhere among its first R−9 states.

**Hashing caveat (applies to every "no path" claim).** States are stored as 128-bit fingerprints: two independent 64-bit hashes of the exact ordered word pair, with 123 effective bits. A collision could merge two distinct states. The probability is about 10⁻²⁰ at our sizes.
- A merge could create a false meet. That can't produce a false positive here, because every positive is rebuilt from exact words and replayed by the official verifier.
- A merge could also hide a state. Only in that way could a negative claim be wrong.

The negative claims below therefore hold with this failure probability, not with absolute certainty. An exact-word re-run, for example with sorted disk-based layers, would remove the caveat. We note that as open work.

## 4. Results

### 4.1 Exact optimality: 53 presentations, best-known lengths 15–19

We ran meet-in-the-middle with b = 9 and a = R−10, which decides whether a path of length ≤ R−1 exists.

| best-known length R | presentations | result |
|---|---|---|
| 15 | 16 | all optimal (no path ≤ 14) |
| 16 | 17 | all optimal |
| 17 | 7 | all optimal |
| 18 | 10 | all optimal |
| 19 | 3 | all optimal |

**Controls** (known minima 13 and 14): ac-01586 and ac-00488. For every a with a+9 ≥ their length, the method returns exactly 13 and 14, and it finds no shorter path at a+9 = 12 or 13.

Per-row tables, with |S_a|, wall times and the replayed shortest paths, are in our run records (§6).

### 4.2 Board-wide lower bounds

- **Distance ≤ 14, all 10,115 presentations** (a = 5). Exactly 32 presentations have an AC path of length ≤ 14, and they are the 32 known minima. No other presentation, solved or unsolved, has a path of length ≤ 14.
- **Distance ≤ 15** (a = 6). This covers the 7,352 presentations whose 2026-09-14 best length was ≥ 20. None has an AC path of length ≤ 15.
- **Swapped target (y,x).** The same 7,352 presentations: none reaches (y,x) within 15 moves.

The swap x↔y maps the move set to itself by relabelling 6↔8, 7↔9, 10↔12 and 11↔13. So d(swap(s), (x,y)) = d(s, (y,x)).

### 4.3 Forced height humps

These come from the capped lemma. R is the best-known length on the live board. The statement is always "no path of length ≤ R−δ whose first R−9−δ states stay within total length C".

| presentation | start total length | best-known R | our best | claim | caps proved (states at the largest cap) |
|---|---|---|---|---|---|
| ac-00037 | 31 | 31 | 32 | no path ≤ 31 within C | C = 32, 33, 34, 35 (179,371,165) |
| ac-00313 | 29 | 33 | 34 | no path ≤ 33 within C | C = 30 (105,391,935) |
| ac-00043 | 21 | 25 | none found by beams | no path ≤ 25 within C | C = 22, 24, 26, 28, 30, 32 (103,802,597) |
| ac-00104 | 12 | 21 | 21 (found at C = 26 by a depth-12 run) | no path ≤ **20** within C | C = 20, 24, 28 (123,926,728) |
| ac-00083 | 17 | 30 | 32 | no path ≤ 30 within C | C = 20, 22, 24, 26, 28 (60,485,890) |
| ac-00135 | 16 | 31 | 40 | no path ≤ 31 within C | C = 18, 20, 22, 24, 26 (192,273,119) |
| ac-00286 | 14 | 26 | none | no path ≤ 26 within C | C = 16–26 (100,305,259) |
| ac-00302 | 23 | 25 | 25 | no path ≤ 25 within C | C = 25, 27, 29, 31 (23,970,899) |

The first two rows use total length. An independent exact-word search (no hashing), run by our collaborator GPT "Luna" and credited in §7, shows two further things under a per-relator length cap: no 14–19-move replacement exists for the first 15–20 moves of our 32-move ac-00037 path, and no 14–17-move replacement exists for four windows of our 34-move ac-00313 path.

**Why this matters for AC.** A shortest trivialization of these presentations must first increase total relator length by at least C+1 minus the start length. For ac-00135 that's at least 11 letters above its start (26+1−16). For ac-00043 it's at least 12 (32+1−21). Hardness in AC is often attributed to such humps. These are exact, instance-level lower bounds on them.

### 4.4 Empirical law: record paths hug the starting length

This comes from 212 exact capped runs over short-start presentations whose 2026-09-14 best length was 20–36. We searched caps of 22–26 (fewer in a few runs) and allowed depth R−9.
- In 71 runs, the search found a path matching the best-known length within total length ≤ 26. Replayed and accepted.
- Of those, the first successful cap exceeded the start's total length by 0 letters (7 cases), 1 (9), 2 (8), 3 (17), 4 (8), 5 (6), or 6–14 (16).
- So a large share of record paths never rise more than about 5 letters above where they start.
- The failures don't prove anything beyond the stated caps, and some of them need larger C, as §4.3 shows.

The per-row data is in `capped_sweep_summary.json`: the first cap that succeeded, the Stable AC length, and whether memory was exhausted.

Methodological note: plain beam search ranked by total length, even with 10⁶ states per layer and 60% diversity, failed on several of these rows. The exact capped search succeeded, for example on ac-00101 (30), where no beam got below 34.

### 4.5 Stable AC: the (y,x) finish beats "AC + 2"

For Stable AC (`sac-r8-v1`), an AC path to (x,y) followed by [16,15] gives length L+2. A path to (y,x) followed by two destabilizations [15,15] gives length L'+2, where L' = d(start, (y,x)). Because L' can be smaller than L, the Stable AC distance can be strictly below the AC distance plus 2. Verified examples, each replayed by the official verifier:

| presentation | best-known AC | our Stable AC | AC + 2 |
|---|---|---|---|
| sac-00043 | 25 | **26** | 27 |
| sac-02322 | 30 | **30** | 32 |
| sac-01077 | 28 | **28** | 30 |
| sac-05315, 07186, 08011, 08301, 08396, 07531, 09365 | R | R+1 | R+2 |

### 4.6 Transport bridge between unsolved presentations

[1,11,5,12,1] maps the starting relators of ac-02216 exactly onto those of ac-02555. We replayed this with the official `apply_move`. So any certificate P for ac-02555 gives [1,11,5,12,1] + P for ac-02216. As of 2026-09-14 both were unsolved. Our collaborator reports that no bridge of length ≤ 4 exists; we have not rechecked that.

### 4.7 Negative observations (recorded to save others time)

- **No mod-3/6/9 structure in record lengths.** Over 7,442 solved presentations, record lengths are uniform mod 2, 3, 6 and 9 within sampling error.
- **Lookahead heuristics didn't help.** We tried a two-level beam key (best total length reachable in one move, tiebreak own length), inspired by greedy-embedding constructions. It gave no improvement on four near-miss presentations.
- **The abelianization invariant can't rule out paths.** The exponent-sum matrix has determinant ±1, and every move preserves that up to sign. Since the target also has determinant ±1, this invariant can never exclude a path.

## 5. What is established and what remains open

**Established.** All the following hold up to the 10⁻²⁰ hashing caveat for negatives:
- exact optimal lengths for 53 benchmark presentations
- global non-existence of short (≤ 14, and ≤ 15 for the 7,352-presentation band) AC trivializations
- explicit forced humps for 8 presentations
- explicit, verified Stable AC paths strictly shorter than AC + 2
- an exact transport bridge

**Open.**
1. Remove the hashing caveat with exact-word, disk-backed layers.
2. Extend the hump bounds past the 15 GB memory limit, for example C ≥ 36 for ac-00037 and C ≥ 34 for ac-00043.
3. Decide whether a hump bound can be proved symbolically, as a length-function argument, rather than by enumeration.
4. Resolve the unsolved presentations (for example the 02216/02555 family). This does not bear on the conjecture unless one is shown to be non-trivializable.

Nothing here addresses AC for general balanced presentations.

## 6. Reproducibility

- The code is C11, with no dependencies beyond libc: `acc_opt.c` (kernel, fingerprints, tables, the T_R build, meet-in-the-middle), `acc_batch.c`, `acc_capped.c`, `acc_beam.c` and `acc_window.c`. Every positive result is replayed through the official verifier.
- Calibration: T_8 = 24,587,144; T_9 = 214,977,551 (with the SHA above); the two controls in §4.1.
- The sources and run records sit in our team repository (`dicipler-pixel/operator-first`, branch `claude/gallant-bardeen-0pgpae`, under `research/acc/optimality/` and `tools/acc/`). **That repository is currently private.** Before linking it in the submission form, publish it or a copy with the commit hash of the submitted version. Alternatively, attach the self-contained bundle `tools/acc/jev_handoff/`.

## 7. Credit and citations

- **SAIR Andrews–Curtis Challenge:** official manifest, move specifications and verifier. https://github.com/SAIRcompetition/Andrews-Curtis, commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`. We use it for every replay and acceptance check.
- **GPT "Luna 6":** an external AI collaborator whose results the team relayed. Luna supplied the independent exact-word window proofs for ac-00037 and ac-00313 (§4.3) and the ac-02216 → ac-02555 bridge (§4.6), and reported swap-finish screens. We reproduced the bridge. We did not reproduce the other results; they are marked as hers.
- **Background on AC hardness and humps:** A. Shehper et al., "What makes math problems hard for reinforcement learning: a case study" (2024). It motivated our focus on path "humps". None of their data or code is used.
- **Computation:** carried out by the team with Claude (Anthropic) as a coding and analysis assistant.
