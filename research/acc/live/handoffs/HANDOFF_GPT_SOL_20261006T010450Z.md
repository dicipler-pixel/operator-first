# HANDOFF_GPT_SOL_20261006T010450Z

Filed by UPG-H 2026-10-06 from the owner's paste. The text below is Sol's handoff as received; the filing notes at the end say what was extracted.

**Mad Hatters ACC — GPT/Sol handoff**
**Prepared:** 2026-10-06 UTC
**Lane:** GPT / Sol
**Required pin:** `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`
**Submission rule:** no SAIR submissions/API calls from this handoff. Jeremy submits.
**Hard exclusions:** never touch 09839, 02257, 09311, 06403, 04718, 05378 or their twins.

Sol read `00_ACC_MOVES_MANUAL_v1_20261006.md` first; this handoff adds what is not already fully captured there.

Status labels: **COMPLETE** = exact theorem/certificate/finite search completed in its stated scope. **INCOMPLETE** = useful work exists, frontier/search/proof obligation remains open. **idea-only** = structural lead not yet turned into a scored certificate.

---

## 1. WHO

GPT / Sol lane (earlier work also appears under Astra / GPT coordination language in the Oct 2–4 campaign records). Dates: Sep 11–Oct 6, 2026; heaviest ACC work Sep 12–Oct 4; proof-synthesis pass Oct 5–6.

Ordinary AC rows handled/certified/audited: ac-00002, ac-00015, ac-02842, ac-02089, ac-03060, ac-00975, ac-03714, ac-03871, ac-06045, ac-06936, ac-10098, ac-04129, ac-00738 / ac-06611, ac-10099, ac-00764, ac-09632, ac-03320, ac-06036, ac-09026, ac-02552, several donor/holding rows from the 60-target packet.

Stable AC rows: sac-07492, sac-06768, sac-09312, sac-00259, sac-04469, sac-05506, sac-04493, sac-07730, sac-08995, sac-02717, sac-09980, sac-06045 mirror lane, sac-02528 / sac-08578 audit family, the Stable half of the 60-target packet.

Also theorem-family work on AK(n), Miller–Schupp/square-family transport, exact capped geometry, quotient/Nielsen search design.

---

## 2. MOVES / METHODS

### 2.1 Exact capped-component geometry / length wells — COMPLETE

Search the literal ordered `ac-r2-v1` graph under a total-relator-length cap; a result is closed only if the queue empties.

**Theorem.** For state P and cap C, let K_C(P) be the component inside relLen <= C. If T=(x,y) is absent from K_C(P), every trivializing path hits length >= C+1. If every state in K_C(P) has length >= L, every path reaching length < L first leaves the cap.

Where: Drive `GPT_NOTE_v2.md` (1DX7LXWaTi4taa7FZrUSstacVj7xzlAlg); Drive `ACC-P000010-Certified length wells and forced height excursion (1).md`; Lean `lean/acc/ACCWell.lean`; public formal snapshot `dicipler-pixel/acwindow-lean` @ 78849f53e6a79724e6ae520de3f87e3ba8b2373b.

Exact outputs:
- ac-02842 cap 21: 219,042,976 states, target absent, H* >= 22.
- ac-00002 cap 35: 21,656,544 states, min length 25, H* >= 36; any descent below 25 first reaches >= 36.
- ac-00015: cap-26 component 105,912 states, no state below 21; at cap 27 a length-20 state appears; from it the cap-30 component has 9,096,912 states, min length 20, so any descent below 20 must reach >= 31.

No safe states/sec figure is preserved. Settings: exact ordered full-word equality, official move grammar, stated cap, queue exhaustion. Produces Proof-Track lower bounds on peak length, not leaderboard routes.

### 2.2 Reverse capped geometry from the goal — COMPLETE

Exact reverse BFS components from I=(x,y) under literal total-length ceilings (no cyclic quotient, no pruning, no hash-only equality). Source: `ACC_Full_Research_Edition_20260928.pdf`; operator-first research head 4ad40ec0b9166214d39354e8103deade103b306c; ledger `research/acc/live/ledger/reverse_ceiling_profile_20260928.json`.

| cap | states | diameter |
|---|---|---|
| 2 | 4 | 2 |
| 3 | 72 | 5 |
| 4 | 200 | 6 |
| 5 | 776 | 7 |
| 6 | 1,768 | 8 |
| 7 | 7,784 | 9 |
| 8 | 18,344 | 10 |
| 9 | 74,856 | 12 |
| 10 | 169,992 | 13 |
| 11 | 700,712 | 17 |
| 12 | 1,582,280 | 23 |
| 13 | 6,476,104 | 31 |

Cap 13 adds 4,893,824 states over cap 12; 20,800 states of total length <= 12 become reachable only with height 13; 84,090 visible states get shorter capped distances; largest saving 9 moves.

Witnesses: a total-length-2 state absent at cap 2, present at cap 3 (detour width 3); a length-7 state Q at global distance 4 where every 4-move route needs height 8 while a 7-move route exists at height 7; exact ordered size-2 diameter D2(2)=5. Consequence: move count and peak length are separate coordinates.

### 2.3 AK fold + six-member window + quotient resonance — COMPLETE

AK(n) = (x^n y^-(n+1), xyxy^-1x^-1y^-1).
1. Fold: AK(n) AC-trivial iff AK(-n-1) AC-trivial.
2. Primitive-coordinate lemma: a normally generating rank-two pair with one primitive relator is AC-trivial.
3. Trivial window: n in {-3,-2,-1,0,1,2}.
4. Uniform shift: a uniform AK(n)->AK(n+k) for any fixed 1<=k<=6 trivializes the whole family.
5. Six-window resonance in C_p*C_p: if p divides one of n-2..n+3, the quotient image of AK(n) is AC-equivalent to the standard pair. AK(3) is therefore blind for p=2..6. The C5*C5 nine-move certificate is a consistency check, not free-group evidence.

Where: `ACC_Full_Research_Edition_20260928.pdf`; `ACWindow.lean` in the public formal package. Proof targets, no row score.

### 2.4 Spectral gap + loop detector — COMPLETE, theorem scope only

On every normally generating rank-two component the spectral bottom is >= (2-sqrt(3))/28 > 0; gives a convergent Green/loop observable. Trap: the gap is uniform, so positivity alone cannot distinguish AK(3). Source: `FRESH_AC_THREE_ROUTES_20260919.md`, Sep 28 research edition.

### 2.5 Quotient / Aut(F2) search with explicit lift — COMPLETE as method principle

Search one representative per Aut(F2) class, then lift quotient edges to ordinary AC moves and replay. Public exact-class work: 2,672 board-unsolved instances -> 126 effective Aut(F2) classes; 2,417 hidden Miller–Schupp n=2..10. AK(3) cap 17: 2,994 quotient classes vs 857,808 concrete states (about 300x). **Soundness rule:** no quotient path is a certificate until every transition has an explicit ordinary-AC lift and the expanded path replays on the exact ordered start. Details in the Sep 26 public-development note in Drive.

### 2.6 Nielsen / basis-change channel — COMPLETE as replay evidence

Short/canonical spelling is not necessarily easier. Public AC19 artifact: 72,779/72,779 certificates replayed, 0 failures, 79,192,710 elementary moves. Ablation: removing Nielsen edges dropped MS-640 coverage 640/640 -> 604/640 and a 60-row subset 60/60 -> 46/60. One path climbed total length 25 -> 77 before collapse. Rule: do not prune because an Aut-min representative looks worse or length rises.

### 2.7 Exact cross-lineage splice — COMPLETE lemma

If road A reaches exact ordered state S and road B contains S, A-prefix + B-suffix is a road. Conjugacy/hash/basis-equivalent matches are not free; orientation, relator order and basis maps must be priced. Public mining: 46,239 one-move joins, 219,236 two-move joins, 3,899 shortened paths; 80 direct improvements induced 523 more in one feedback loop. Every non-record road is worth keeping.

### 2.8 60-target GPT/Gemini campaign — partly COMPLETE, mostly INCOMPLETE

Drive: `ACC_SPLIT30_CAMPAIGN_20261004.zip` (1G6kFKPBNabfjxaN0P7PIr3GwoiIxApeg), `ACC_GEMINI_30.ipynb` (120bKZsal-a3kEbTWkfdd2yMSC8P9en0B), `ACC_SPLIT30_RESULTS_20261004.zip` (1LSS5xS9JDet-UzjyaQscsY7CFqXm7vb1).

Roster: 60 shared targets, 22 AC + 38 Stable, one row per family; saved k=2 and Mad Hatters absent in the frozen membership snapshot; GPT/Gemini repartition matched the earlier DeepSeek/dot/GrokBot 60 exactly.

GPT_30 settings: 180 s/row, 600,000 retained-state budget, 1 GiB, native replacement depth 7, total-length cap 56. Result: 30 receipts, **1,527 COMPLETE window misses, 29 INCOMPLETE rows, 0 shorter certificates**; all 29 saved native frontier files recovered, SHA256-matched and parsed.

**Resume trap:** the notebook worker skips any row whose `RESULT.json` exists, and native resume enforces the old max-state budget, so relaunching does not progress exhausted rows. True continuation needs a cumulative-budget increase and preserved originals.

Closest honestly rankable frontier: **ac-04129 — INCOMPLETE.** S19 -> S28 in <=7 native moves, cap 56 (replace a 9-move segment, 39 -> 37). Forward ball 1,550 states depth 3 complete; backward 8,103 states; cursor head 858 / edge 0; targeting backward depth 4; 9,653 states total; allocation exhausted. No ranking claimed for the other 28.

Gemini half: queued awaiting runtime acknowledgement, sign-in blocker recorded; no reliable evidence it ran.

---

## 3. LINES AND ROADS

### 3.1 Exact arrays held

**sac-07492 — VERIFIED holding, 40 moves; record frozen at 37**
`sac-07492: [11, 4, 7, 7, 7, 12, 5, 1, 7, 10, 13, 11, 12, 2, 5, 6, 4, 9, 7, 11, 13, 3, 6, 8, 11, 11, 4, 13, 11, 12, 5, 10, 2, 0, 3, 5, 5, 5, 15, 15]`
Non-record donor; the fixed-prefix boundary work below is keyed to this road.

### 3.2 Verified facts without arrays in hand (harvest from archives; do not retype)

- ac-09757: 40 (previous 66)
- ac-00276: 39 (previous 46)
- ac-06754: 34 (previous 70)
- ac-04469: holding 45 vs saved record 44
- sac-05506: holding 31 vs saved record 30
- sac-04939: holding 46 vs frozen record 41
- sac-01876: holding 52 vs frozen record 45
- Donor catalog recovery: 110 novel arrays replayed, 43 new/improved holdings (32 newly held, 11 shorter) + 67 alternate donors.
- Version-15 catalog: 288 shortened holdings (144 AC + 144 Stable), e.g. AC/Stable 01060 = 131/133 from 269/271; 03866 = 188/190 from 311/313.

---

## 4. COMPLETED MISSES — DO NOT REDO

### 4.1 sac-07492 — COMPLETE in stated scopes
- Fixed baseline through S22 -> (x,y) or (y,x), native 0–13, cap 56, suffix <=13: COMPLETE MISS. Excludes 36/37-move proposals with that exact fixed prefix/suffix scope only.
- S23 through <=12: reported CLOSED.
- S20/S21 through <=14: reported CLOSED.
- S20 through 15: candidate boundary, not promoted until payload recovery.

### 4.2 ac-03714 — native 0–13, cap 40, no budget hits
S32->S43 through 10; S33->S44 through 10; S31->S44 through 12; S32->S45 through 12: all complete misses. Open: full native <=50, other peaks/endpoints/lineages.

### 4.3 ac-10098
- S33 -> xy and yx through 7, no peak pruning: exact distance 8 in this scope.
- moves 6–12 replaced by <=6, cap 70: complete miss.
- moves 20–30 replaced by <=10, cap 70: complete miss.
Open: other windows/lineages; full native <=40.

### 4.4 ac-06045 — S25->S37 through 11, cap 80: complete miss; a 12-move witness joins them (12-move tail scoped-optimal for that boundary only).

### 4.5 Cap/length-limited only
- ac-03871: length <=30 excluded at peak <=34.
- ac-00975: partial cap-31 result excludes <=30 only (not its 34 target globally).
- ac-03060: <=27 excluded at peak <=38; a peak-40 stop excluded only <=24 in that scope.

### 4.6 Held-road spine lane — COMPLETE finite lane
15 gap-one stems completed bounded radius-5 spine bridges (<=8 anywhere, <=10 between best-path nodes, 5+3+7 goal-end construction): 00145, 00678, 00753, 00975, 02288, 02528, 03714, 03871, 04493, 04699, 05598, 06045, 06262, 06768, 06969. Unchanged held-road-neighbourhood surgery is closed; a fresh lineage is required.

### 4.7 sac-05506 — saved 31 vs record 30
2,160 commutation variants at length 31; 418 distinct fresh endpoint scopes; 75 attempted COMPLETE misses (57 at depth 11, 18 at depth 13); fixed S15 prefix -> alternative yx finish <=13 native: complete miss; 357,660 one-/two-deletion trials: none shorter. Unattempted pairs: depth 7:65, 8:64, 9:59, 10:56, 12:60, 13:39 = 343.

### 4.8 sac-04469 — holding 45 vs record 44
787 historical exact windows; 92 changed-boundary cap-80 scopes at depths 9–13 complete; 528 replayed commuted variants; 243,930 one-/two-deletion trials; none shorter. Open: 15-native window -> <=14 at cap 80, 55 endpoint pairs, 7 complete, 48 fresh. (The 787 and 92 are different ledgers; do not add them.)

### 4.9 sac-07730 — S0->S8 through 7, cap 56: closed.

### 4.10 sac-02528 / sac-08578 — three named 02528 identity-deletion proposals and related 08578 checks failed; not global exclusions.

---

## 5. UNFINISHED WORK WORTH FINISHING

| # | row / scope | state | value | what is needed |
|---|---|---|---|---|
| 5.1 | sac-07492 S20 -> finish through 15 | INCOMPLETE | medium-high | recover S20 payload from `ACC_07492_PARTIAL_FRONTIERS_20261004.tar.xz` (bytes not retrieved in the last audit); verify endpoints/config/cursor; continue only if the payload supports it. Time unknown. |
| 5.2 | ac-04129 S19->S28 <=7, cap 56 | INCOMPLETE | medium | frontier inside `ACC_SPLIT30_RESULTS_20261004.zip`; needs a larger cumulative budget (same-budget resume is a no-op). |
| 5.3 | sac-04469 15 -> <=14 at cap 80 | INCOMPLETE | medium-high | 48 fresh endpoint pairs; historical budget 8,592 engine-seconds, about 2.4 h on one core. |
| 5.4 | sac-05506 | INCOMPLETE | medium | 343 fresh endpoint pairs (244 at depths 7–10 first). Historical: 57 depth-11 scopes 84.53 s total; 18 depth-13 scopes 294.71 s total. |
| 5.5 | ac/sac-06936 | INCOMPLETE | low-medium | 14-move witness (peak 33); pasted cap-70 S6->S20 through 13 miss awaits execution evidence (source hash, depths, intersection evidence, reverse payload). Do not rerun just for a receipt. |
| 5.6 | sac-02717 | INCOMPLETE | low | save-one/deep-climb receipt 7,999,999 new states; raw frontier needed; row already credited. |
| 5.7 | sac-09980 | INCOMPLETE | low-medium | local subproblem closed; broader save-one job 5,999,999 states incomplete; identify scope first. |
| 5.8 | ac-06045 mirror/from-start | INCOMPLETE | low-medium | stopped 12,015,885 states after 300.004 s, depth-8 frontiers open, local-only SQLite. Separate from the closed S25->S37 boundary. |
| 5.9 | sac-04493 leave-five | INCOMPLETE | medium | from S18, first edge != 9, rejoin >= S30 after >= 5 off-road steps, save >= 2; stopped 600,000 states at depth 5/5 vs bound 12; five named chunks complete misses; keep terminal [15,15]; needs the local SQLite checkpoint. |
| 5.10 | sac-06768 | INCOMPLETE | medium (with larger budget) | native yx <=32 then Stable finish (record 34); paid L15/i0 cap48 1,000,000 states; cloud L16/L17 26 complete misses + 9 partials. |
| 5.10 | sac-09312 | INCOMPLETE | medium-low | native yx <=31 (target 33); paid L15/i10 cap56 1,000,000 states; same-budget resume adds nothing. |
| 5.10 | sac-00259 | INCOMPLETE | medium | native yx <=36 (target 38); paid cap30 752,715 states; durable cap31/depth36 SQLite 200,000 nodes, cursor 96,232 / move 10, depth 10 expanded; old wide beam had a heuristic miss. |

Paid batch for 06768/09312/00259: 2,652,713 new states, 9,709,954 edges. "Batch completed" meant save/release, not mathematical completion.

---

## 6. UNSOLVED ROWS — ideas only

- **ac-00738 / ac-06611:** one family via `[0,1,8,8,12]`; do not repeat capped closures 20–28 or cap30 depth<=54; search high excursions / basis-changed spellings; price the 5-move transfer on any donor entering the shared class.
- **ac-10099:** caps 20–30 closed (378M states); look for an Aut(F2)/Nielsen representative outside the low well, an outside-road splice, or family transport first.
- **ac-06412:** classify first (exponent matrix, relator shape, Aut(F2) class), then donor search; no generic beam before that.
- **ac-09632:** Bob's climb-then-collapse failed in three settings; use a different representation (Nielsen/basis change, quotient-lift seed).
- **ac-00764:** 00766/00764/02598 family; 00766's road replays 8 moves on 00764 then fails at move 9; look for parameter transport.
- **ac-05538:** family/class recognition against the donor catalog and alternate spellings first.
- **ac-03320:** new basis/orientation or quotient-lift seed, not the same collapse weights.
- **ac-06036:** global road graph / classification first.
- **ac-09026 / ac-02552:** no road; classify under Aut(F2), compare to Miller–Schupp / Baumslag–Solitar, search donor classes, allow high excursions.

---

## 7. TIPS AND TRAPS

1. Official AC.Step allows arbitrary-word conjugation in one step; scored `ac-r2-v1` allows only one-letter conjugations. Never transfer distance/height claims between them without expanding.
2. (x,y) and (y,x) are different scored endpoints; a yx route must be priced with its legal Stable finish.
3. Exact state equality = full freely reduced ordered words. Hashes index only; conjugacy, rotation, Aut(F2) equivalence, relator swap are not free.
4. COMPLETE means frontier empty. Timeout, memory ceiling, node cap, beam exhaustion or partial layer is INCOMPLETE.
5. Re-running a notebook that finds RESULT.json is not a resume; same-budget native resume can be a no-op.
6. Do not reconstruct a lost frontier when a preserved one exists (especially sac-07492 S20).
7. Distance and height are independent; hard length caps can remove the winning route.
8. Canonical/short spellings can be harder; keep alternate lineages.
9. Quotient hits need explicit lifts and replay.
10. C_p*C_p tests are blind on AK(3) for p<=6 by theorem.
11. Uniform spectral positivity is blind; use distribution/Green data instead.
12. Do not double-append the Stable finish to an AC road.
13. Do not add receipt counts across ledgers as if scopes were unique.
14. A locally optimal tail is not a globally optimal road.
15. Protected stems stay protected.

---

## 8. EXACT RESULTS NOT FULLY IN v1

8.1 cap-exit theorem; 8.2 ac-02842 H*>=22 (219,042,976 states); 8.3 ac-00002 H*>=36 (21,656,544 states); 8.4 ac-00015 nested wells (105,912 / 9,096,912 states); 8.5 reverse geometry through cap 13 (6,476,104 states, D2(2)=5); 8.6 AK fold; 8.7 AK trivial window n=-3..2; 8.8 uniform-shift closure (conditional); 8.9 six-window C_p*C_p resonance; 8.10 primitive-coordinate lemma; 8.11 spectral lower bound (2-sqrt(3))/28; 8.12 evidence-separation: heuristic misses, incomplete frontiers, bounded scans or quotient non-hits cannot be promoted to global non-triviality; 8.13 sac-07492 S22 fixed-prefix exclusion (stated scope only).

---

## 9. 60-TARGET PACKET RESTART SUMMARY

Complete: packet preserved (three Drive files above); 60 rows (22 AC + 38 Stable); GPT_30 = 1,527 complete window misses + 29 incomplete rows, 0 shorter; 29 frontier files passed hash/parse audit; Gemini 30 not confirmed run.
Incomplete: the 29 GPT rows need dedicated continuation logic; only ac-04129 is honestly rankable as closest.
Do not infer: 1,527 misses are not row closures; 29 frontiers are not resumable without a larger cumulative budget; "batch completed" is an operational event.

---

## 10. SOURCE POINTERS (Drive hub 1FKL3CsdhkxC6iSiV3YA7Hj5Cgk7eMP89)

- `00_ACC_MOVES_MANUAL_v1_20261006.md` — 14R_17h1-7F1P2S5vrNdpyNSoXPuV-AcD
- `ACC_SPLIT30_RESULTS_20261004.zip` — 1LSS5xS9JDet-UzjyaQscsY7CFqXm7vb1
- `ACC_SPLIT30_CAMPAIGN_20261004.zip` — 1G6kFKPBNabfjxaN0P7PIr3GwoiIxApeg
- `ACC_GEMINI_30.ipynb` — 120bKZsal-a3kEbTWkfdd2yMSC8P9en0B
- `GPT_NOTE_v2.md` — 1DX7LXWaTi4taa7FZrUSstacVj7xzlAlg
- `ACC-P000010-Certified length wells and forced height excursion (1).md`
- `ACC_Full_Research_Edition_20260928.pdf`
- `FRESH_AC_THREE_ROUTES_20260919.md`
- `GROKBOTO_PING_20261003_1908CT` — 1hf9CIhKuQXuahgQherrXXpasoxkudDw0tAVfu2e8Bqo
- `ACC_Research_Recovery_20261003.zip` — 1VrsdB5A9o5FpnPwyX1MsVzaEuMky3dsg
- `ACC_CURRENT_TARGETS_AND_VERIFIED_ROADS_20261003.zip` — 18EL4D6d8mfi4bJsTPIhjBhMuwHNCPvI3

## 11. BOTTOM LINE (Sol)

Adds: exact height geometry and capped-well theorems with certified counts; the AK fold/window/resonance chain and the uniform-shift target; the lift requirement for quotient/Nielsen/class transport; GPT_30 restart semantics and the ac-04129 frontier; precise boundaries for 07492, 03714, 10098, 06045, 05506, 04469, 07730 and the parked SOL lane; the verified 40-move sac-07492 road; distance, height, spelling, class and lineage are separate coordinates. Nothing here claims AC, Stable AC or AK(3) is resolved.

---

## Filing notes (UPG-H)

- Road: `inbox/handoff_sol_20261006.txt` (sac-07492, 40 moves; replayed on the pinned official verifier before filing).
- Misses: `catalog/closed_sol_handoff.jsonl` (sections 4.1–4.10; scopes as stated, no widening; "reported CLOSED" items carry `"grade": "reported"`).
- Open work: `catalog/incomplete_sol_handoff.jsonl` (section 5).
- Good PC/Colab candidates (compiled, unattended, no model): 5.3 sac-04469 (48 pairs, about 2.4 h) and 5.4 sac-05506 (343 pairs). 5.2 ac-04129 needs the GPT_30 frontier from the SPLIT30 results zip (run `harvest_zip.py` on it first).
