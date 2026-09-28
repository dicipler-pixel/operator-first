## 2026-09-28 15:27Z, Codex importing Charlie's disk-backed exact search
- User supplied Charlie's complete text handoff. `acc_disk.cpp` stores literal ordered BFS layers on disk; his supplied ledger has 28 runs across 14 rows, including an ac-02528 35-move path found after 533M reported forward states and an ac-03719 37-move path. Full large frontiers were not included. His cap-limited negative results do not prove unrestricted shortestness; ten disk-full runs are incomplete.
- Independent pinned-core replay accepts all four proposed AC/SAC paths and all 540 cutchain routes. C++ compiled and matched 1,428 local move cases, cap-10 identity layer histogram (169,992 states), and ac-00738 cap-21 closure (189,944); supplied xcheck matched 56,056 official moves. This supports the engine transfer without independently repeating its 533M-state run.
- **Snapshot correction:** at 15:13Z, only ac-02528 35 ties (k8, absent from SENT_ROWS). The other three proposed lines trail the current saved records; 56 chain ties were already sent, 484 lines trail. One active inbox tie awaits sender live recheck/batching. Details, source SHA, code, logs, and missing B36/T16 build requirement: `research/acc/live/CHARLIE_HANDOFF_CHECKPOINT_20260928.md`. No SAIR submission by this helper.

## 2026-09-28 15:04Z, Codex: upside-down reverse graph under exact total-length ceilings
- Complete literal ordered-state reverse BFS from identity under all 14 official moves: caps 2..10 exhaustively processed (169,992 states at cap 10); cap 11 incomplete at 500,001 seen states. This is total relator length, with no cyclic quotient.
- A size-7 presentation has a 7-move route confined to cap 7 and an unrestricted shortest route of 4 moves requiring cap 8. Thus shortest distance and minimum-height route really are different search coordinates. At size 2, the exact longest shortest distance is D₂(2)=5; one length-2 pair requires height 3 to connect.
- Reproducer, replays, profiles and caveats: `research/acc/live/ledger/reverse_ceiling_pilot_20260928.md`, `reverse_ceiling_profile_20260928.json`, `research/acc/optimality/reverse_ceiling_probe.py`. No challenge line from this synthetic small map. Per user's request, all Codex A/B helper beam lanes were stopped at 49/172 finished rows, zero qualifying paths, raw checkpoints saved.

## 2026-09-28 14:51Z, Codex: Smith chart and Snell routing pilot while dual beams run
- Tested the user's two distinct ideas on 436 pinned-core-verified AC routes. Length-only Smith coordinates cannot see inversions/conjugations; adding cyclic commutator length gave a new sector at only 1/6 known optimal-route beam drops. A matched third-eye sector pilot got ac-03305 24→24 (record 23) and harmed ac-05558 24→26 (record 24). No score; do not enable that variant.
- A discrete Snell-style feature R sin²θ using empirical one-step rigidity worsened next-move candidate ranks: 0.4629 vs 0.4465 for constant-angle persistence (chance 0.5), over 1,894 radial interfaces. Keep this tested feature at weight 0; this says nothing about the user's physical Snell law. All definitions, scripts, paths and trials: `research/acc/live/ledger/smith_snell_pilot_20260928.md`.
- Four assigned two-eyes beams remain running, disjoint A/B sets. Any new tie/beat goes through official verifier to the inbox for the sender.

## 2026-09-28 12:56Z, Codex: Lisitsa v2 archive compiled against SAIR scorer
- Got the Drive ZIP, checksum matched, replayed all 16,232 high-level operations, then compiled all MS(3)..MS(9) fixed-word routes to atomic `ac-r2-v1` with pinned verifier and frozen limits. n=5..9: **1,332 / 3,616 / 8,847 / 20,708 / 49,926** scored moves versus logged records 80 / 145 / 275 / 532 / 1,046. No score. The archive's n=5 peak length 22 is far below our 125-move generator's peak 63, so it is useful narrow-corridor trajectory data, not a short certificate.
- Exact radius-2 state splices and fixed-relator conjugacy joins with our n=5..7 routes: no shorter route. Three fixed-relator n=5 beams through the 62-move middle budget (P1 cap22 W5k, P2 cap22 W3k, length cap35 W5k) also missed; these are incomplete searches, not impossibility proofs. Full replayed atomic paths are in `ledger/codex_lisitsa_scored_paths_20260928.json` for graph merging. Scripts: `tools/acc/ms_lisitsa_replay.py`, `optimality/ms_archive_to_sair.py`, `optimality/ms_archive_splice_probe.py`. Full counts and commands: `ledger/codex_lisitsa_archive_priced_20260928.md`. Input ZIP stays in the user's Drive ACC replay handoff folder.

## 2026-09-28 13:00Z, session 2 (lead): BEAM_DUAL "two eyes" wins; all lanes switched
- Builder helper A/B (W=20000, depth record+6, T8, 10 rows): DUAL 0.75 vs the quota/elite winner is shorter on 7, never
  longer, finds paths on ac-04081 (38) and ac-08305 (39) where the winner found none, 20–60% faster. DUAL 0.5: shorter on 6,
  longer on ac-06045, the only arm at ac-00061 26. Every record-length line it found is a tie we already hold.
- Lanes p2a, p2u restarted on `P2_DUAL=0.75 P2_ELITE=5000` (binary `acc_beam_y` = acc_beam.c at HEAD); p2b switches after
  its current row. The earlier P2 rows (149/140 done) were searched with the old winner; a DUAL re-pass over their
  1-2-off rows is the next cheap lane.

## 2026-09-28 12:50Z, session 2 (lead): unsolved-MS lane p2u (digest lead: "106 second words", first solves = 1.0)
- 106 MS(n,w) families have some n solved and some unsolved; they hold **373 unsolved non-AK(3) rows** (15 more are
  AK(3)-class, skipped). Examples: YYYYYxYXX n=5 solved in **15** (ac-04662) but n=4 unsolved (ac-08441); YYxYxYXXX n=2 in
  22, n=3 unsolved (ac-03989); YYXXYx n=3 in 26, n=4 unsolved (ac-09310). The n=5 solve looks like a coincidence (r0's
  Y^5 cancels r1's y^5), so neighbours are not automatically easy.
- Lane **p2u** (winner arm: P2=2 + QUOTA 16 + ELITE 5000, W=20k, depth 120) on the top 40 by nearest-solved distance
  and record (`tools/acc/ops/unsolved_ms_targets.py`). Any path is a first solve (AC 1.0, plus SAC with [15,15]).
  Replaces the tail lane p2t (those rows stay in p2a/p2b's lists).
- 13:00Z: the 40 rows were only 27 symmetry classes. The builder now takes **one row per class** (373 rows = 240 classes);
  p2u restarted on 40 classes covering 61 rows. A hit on one member goes to its class-mates via `crossrow.py`.
- Drive helper (`DRIVE_UNREAD_20260928.md`): the 148 cascade paths all replay but none ties or beats anything new;
  85 more unsolved rows map onto the R_n family (skip candidates after replaying their transports); exact empty caps
  for unsolved ac-02923 (24), ac-02217 (23), ac-01657/06572/00719/03471 (15).

## 2026-09-28 12:18Z, session 2 (lead): why level-by-level chain routes cannot reach the records (row-op argument)
- **Shadow:** the exponent-sum rows of (r0, r1) form a unimodular 2x2 matrix; a multiplication is a row op, while
  conjugation and inversion are free. One level (BS, Y^k X y^(k-1) x^a) -> (BS, Y^(k-1) X y^(k-2) x^(2a)) is
  [[-1,0],[a-1,-1]] -> [[-1,0],[2a-1,-1]]. BFS in SL2(Z) (`optimality/chain_rowops/sl2geo.py`): the minimum is
  **a row ops**, with a **unique** geodesic (a copies of r1 <- r1*r0^-1), for a = 1..8.
- **Conjugations are forced:** between conjugations, repeated r1 <- r1*r0^e only appends r0^j (a power: no cancellation
  inside BS^j), and each extra copy adds 5 letters (`convlen.py`: lengths 5 -> 10 -> 15 ...). So a level needs about a
  conjugations too: **about 2a per level**. The finish from (BS, Y x^m) needs at least m row ops (the peel).
- **Exact checks (12:30Z, `acc_capped` rebuilt with MOVE_MASK, T8):** last level + finish (BS, YYXy x^4) under cap 21:
  best **22** (= beam; 46M states, complete to depth 21, so optimal among cap-21 routes). Finish (BS, Y x^15) under cap 23:
  best 25 (the beam's 21 climbs above 23), so no sub-linear finish inside cap 23.
- Remaining level beams (`optimality/chain_rowops/level_beams_20260928.out`): last level a=8 and a=16 **no path** (W=20k,
  DMAX 90; the beam dies on long x-runs); two levels (BS, YYYXyy x^a): a=1 **15**, a=2 **27**. a=4, a=8 and the m=31 finish
  were stopped at 12:21 to free a core.
- **Consequence:** any route through these level states with BS as the fixed relator costs about sum(2a) + m ~ 3*2^n.
  Our beams (2a+1 per level, m+6 finish) and session 1's exact n=3 (28) sit on that floor. The leaders' 2^(n+1)+n+~12
  **must leave this shape**: r0 moves off the BS row mid-route (for example, both relators carry long runs), or
  y-exponent sums other than +-1 appear. That is the search target for n=4 (record 48): look for routes where r0 is
  not a BS conjugate at the midpoint. Beams (winner arm, W=20k, depth 50) find no path on ac-01784 (n=4).

## 2026-09-28 12:10Z, session 2 (lead): YXXyx chain: where the leaders save (level-cost beams; song "a smaller set of moves")
- Lisitsa's MS_n(w*) archive (16,232 moves, MS(9) = 8,634) is **our YXXyx chain** (Codex 11:52Z). Board records are ~8x shorter
  (n=9: 1,046 vs 8,634), so the archive scores nothing; archived at `research/acc/proof_track/ms_lisitsa_ak3_20260928/`.
- **Record law:** rec(n) - rec(n-1) = 2^n + 1 (or +2): 80->145->275->532->1046->2071; rec(n) ~ 2^(n+1) + n + 11..13.
- **Beam level costs** (winner beam, W=20000, `scratchpad/chainfin/run.py`): finish (BS, Y x^m) = 8, 13, 21 for m = 3, 7, 15
  (= Codex's m+6: 1 move per x). Last level + finish (BS, YYXy x^a) = 8, 13, 22 for a = 1, 2, 4. The a=4 path is
  `1 4 (10 4)^3` (2a) + swap `2 5` + 6 moves + peel `4^6`: level ~2a+1, then a peel of 1 per x.
- **Consequence:** our best pipeline = sum(2a+1) + (2^n+5) ~ 3*2^n; its increment per n is 1.5*2^n, the leaders' is 2^n + 1.
  So the leaders either (A) cross a level in ~a moves (1 per x, keep the peel) or (B) keep 2a+1 levels and finish in O(1).
  Pure-power pairs cannot shortcut the peel ((Y x^a, x^d) presents Z/d), so (B) needs two relators with matching long x-runs.
  Session 1's masked exact n=4 (10-move set reproduces the n=3 optimum 28) is the test; the a=8 / m=31 beams discriminate.
- **Song mapping:** "a smaller set of moves that still carry you" -> move mask (session 1: r1-only 7 moves gives 33 at n=3,
  the 10-move set 0-8,12 keeps 28 at 1.6M states); "the constant" -> keep BS fixed (Lisitsa's structure).

## 2026-09-28 11:52Z, Codex: Lisitsa family mapping correction and commutator phase replay
- **Correction to the 11:45Z note:** the w* in Shehper Theorem 3 and the cited Lisitsa family is b^-1 a b a^-1 (four letters), whose second relator a^-1 w* is five letters. Under a=x,b=Y, invert Q0 and rotate Q1: the exact scored family is YXXyx / Y^(n+1) X y^n x (ac-01950..ac-00106), not the six-letter YXyXyx name printed there. See `ledger/codex_commutator_lisitsa_20260928.md` for literal words, caveats and official-core replay.
- c=cyclic length([r0,r1]) is exactly invariant under scored moves 0–5; on valid n=5 (125 moves) it rises 30→70, then first reaches 4 at move 91 (34 left). This suggests a **phase trigger** to switch to an endgame solver, not greedy minimization. The lead's score zoo has already tested c as a P2 tie-break; this is a different use.
- The user's 53 h_i path P→AK(3) is exactly **53 scored ac-r2-v1 moves** because inverse-other multiplication is atomic (3/5). Pinned official core verifies synthetic endpoint: peak 25, work 891. It proves P~AK(3), not triviality. Reproducer: `optimality/codex_commutator_phase_probe.py`.

## 2026-09-28 12:05Z, session 2 (lead): atlas beam A/B verdicts — "protect what can be protected, release the rest" wins
Source: `ledger/atlas_beam_ab_20260928.json` (56 runs, 81 paths, all official-verifier ok; W=20k, depth rec+6, T8).
- **Winner: P2=2 + QUOTA=16 + ELITE=5000** (top W/4 by the key kept regardless of class; the rest class-capped — the team
  lead's "protect what can be protected, release the rest"): never worse than P2=2; better on ac-00487 (26/27, both records)
  and ac-06045 (SAC 41). **Both P2 lanes now run it** (`P2_ELITE=5000 tools/acc/ops/p2_list.sh`, binary acc_beam_x).
- Dead by the fixed rule: QUOTA=4, WH (B83), P2=3 (comm_len key: the offline gain did not carry into the beam),
  P2=3+QUOTA=16 (drifts to ~2,100-letter states). QUOTA=16 alone survives only through sac-00487 27.
- **Beam-loss trace (B20):** P2 arms drop the record road early (index 6–9), never among ties: the road's P2 sits 1–3 above
  the cut (5 of 6). Two drops are "just short of width" (03305 1.1×, 00061 1.7×), four "ranked wrong" (2.4–11×). Plain H keeps
  roads longer (index 7–20) and finds 00061 at 26 where P2 finds 29. Next: a two-eyes beam (half P2, half H) — helper building.
- Overlap splice across all arms' paths: R=2 nothing new; R=3 ac-06045 39 → 38 (record 36).

## 2026-09-28 11:55Z, session 2 (lead): the team lead's AK(3) audit (Lisitsa / Shehper et al.)
- Replayed: 53 h_i moves (67 AC moves) take P = (ABaBAbaBBabAb, BAbbABabaBBa) to AK(3) (`tools/acc/ak3_p_to_ak3_replay.py`,
  plus the lead's AK3Audit.lean with forward/reverse checks; a conjugator typo at step 81 of the printed 160-step route).
- P is in acwindow-lean's exhaustive AK(3)-class walk: an independent confirmation of the walk behind our 47-row skip list.
- The early paper's stable-triviality claim was withdrawn, so AK(3) stays open on both boards; the sac- twins stay skipped.

## 2026-09-28 11:45Z, session 2 (lead): who holds the doubling chains — grothendiecksga.com (T00096) — and the prior art
- **Team:** grothendiecksga.com (ACC01-T00096), AC rank 4 all night (486 pts, 2,011 scoring rows, 323 held alone). Score fell
  548 → 487 at 04:11Z when another team beat ~1,000 long rows. **They score on 53 of our 68 doubling-chain rows and hold 38
  alone**, including all of YXXyx n=5..10 and YYxyXYx n=5..10. Raw: `research/acc/live/teams/T00096_ac_20260928T1140Z.json`.
  So they have a general construction; nobody else is close on these rows.
- **Prior art (web search):** A. Lisitsa, "New Andrews–Curtis trivializations for Miller–Schupp group presentations",
  Examples and Counterexamples 6 (2024) 100168: trivializations of MS_n(w*) for n = 3..8 (w* = y^-1 x^-1 y x^-1 y x = our
  **YXyXyx** chain), and **two conjectures on the structure of the simplifications for all n ≥ 3**. Supplementary sequences on
  Zenodo record 14647749. Also: "Automated theorem proving reveals a lengthy AC trivialization for a Miller–Schupp trivial
  group presentation" (8,634 steps), and arXiv 2304.03196 (AC trivializations via 4-manifold trisections).
- **Blocked:** arxiv.org, zenodo.org, sciencedirect.com, livrepository.liverpool.ac.uk are denied by this environment's network
  policy. Ask: the team lead can add them to the allowed domains, or drop the paper PDF + Zenodo files in Drive / the chat.
  The structure conjectures are exactly the chain build we are missing.

## 2026-09-28 11:35Z, session 2 (lead): the team lead's commutator census, mapped to AC and screened
- Census kinds → AC scores: group commutator [r0,r1] (= comm_len, the winner), projector/invariance |[r0,x]|+|[r1,y]|
  (zero at the finish), mixed min_g |[r0, g r1 g^-1]|, self |[r, rev(r)]|, tangent/flatness (share of commuting move pairs).
- Zoo, hump paths, as tie-breaks after (P2, comm_len): none beats comm_len on climbing steps (0.616). GEN, GENmin, SELF act
  like distance-to-finish (−9 to −11 on climbing, +3 to +4 on all steps); MIXED ≈ comm_len; FLAT = the cage bit's endgame
  gain at 40× the cost. As primary keys all fail on climbing (0.00–0.28). Beam key stays P2 | comm_len | P1m | H.
- The census algebra checks out: for H = S + εE (S symmetric, E skew), [H, Hᵀ] = −2ε[S, E]; a commutator in a metric slot
  has g_aa = 0; Σ_a [q^a_i, q^a_j]^2 = 0 for scalar components (use the Lie bracket f^abc q^b_i q^c_j).

## 2026-09-28 11:10Z, session 2 (lead): the team lead's "can't bury the count" verses — overlap splice works
- "They put two paths in the dark ... what they saw was the overlap ... what they think they erased, a quiet hand can
  retrieve" → **overlap splice** (`tools/acc/overlap_splice.py`): for a row with ≥ 2 different paths, splice prefix(A) +
  exact connector (≤ R moves) + suffix(B). First run (R=2, 551 rows with paths, only 22 with ≥ 2): **ac-00487 27 → 26 =
  record** (k14), sent in 2657. Next: generate several paths per near-miss row (P2=1, P2=2, QUOTA, seeds) and splice.
- "One heading, one width ... crowd at the edges ... the wall grow from inside" = the class quota (B16/B17), which just
  found sac-00487 27 (record). "They can bury the picture, they can't bury the count" = P2 (length is the picture).
- "Look close or look far, I'm the same damn walk" → self-similarity: the leaders' chain path at n+1 likely contains the
  n path as a block. Untestable without one of their paths; a hint for whoever builds the chain generator.

## 2026-09-28 10:50Z, session 2 (lead): score zoo — the rotation fix, the cage is wrong, P2-cap slack
Source: `research/acc/live/SCORE_ZOO.md`, `ledger/score_zoo_20260928.json` (65 scores × 536 key configs on 246 at-record
paths; 59 hump paths, 305 climbing steps = 125 conjugations + 180 multiplications).
- **P2's blind spot is real:** on climbing CONJUGATION steps, (P2, P1m, raw) puts the record move in the top 3 only 3%.
- **Fix: a word-level tie-break between P2 and P1m.** (P2, comm_len, P1m, H): climbing top-3 0.413 → **0.616**
  (+0.20, CI +0.14..+0.27), climbing conjugations 0.03 → 0.51, all steps 0.593 → 0.652. comm_len = cyclically reduced
  length of r0·r1·r0^-1·r1^-1 (0.008 ms/state). real2_d2 (fewest conjugations/inversions before a multiplication lands in a
  class P2 promises) is slightly better (0.643). Offline proxy only: matched beam A/B running (BEAM_P2=3).
- **Symmetry ranked HIGHER (the cage flipped):** (P2, comm_len, cage_high, P1m, H) all-steps top-3 0.652 → 0.686, climbing
  unchanged (0.62), conjugation steps unchanged (symmetry is conjugation-invariant). Gain sits in the endgame, which the
  T8/T9 finish tables already cover, so low priority for the beam.
- **"Perfect symmetry is a quiet cage" — refuted for AC:** record paths PREFER symmetric states (0.71 vs 0.51 of siblings);
  cage states appear only in the endgame and the record path takes them 94% of the time. Ranking symmetric states lower
  does not help. (Ranking them higher is untested.)
- **P2 climb on 59 hump paths (for the P2-capped exact search):** c=0 66%, c=1 83%, c=2 92%, c=4 97%; over all 246 paths
  c=0 83%, c=1 95%. Outliers: ac-00282 (11), 00061 (5), 00478 (4), 02315 (4).
- **Atlas class quota (B16/B17) works too:** BEAM_QUOTA=16 on P2=2 found sac-00487 at 27 (record, k3), where P2=2 alone
  gives 28 (we held 62). Queued. Full A/B still running.

## 2026-09-28 10:30Z, session 2 (lead): the team lead's "Cross the wall" verses, read as search ideas
- "Surface can fail, the deeper count still seen" = P2: raw length (surface) climbs over the hump; P2 (the deeper
  count) stays flat on 64–73% of record hump paths. Already our best new tool.
- **"Cross the wall, keep the record clean" → P2-capped exact search (running, helper):** cap the exact BFS on
  P2(state) ≤ P2(start) + c instead of on total length. Length is free to cross the wall; P2 must stay clean. If P2 is
  flat on most record paths, the capped set containing them should be far smaller than a length cap of start+16.
  Prototype `optimality/acc_capped_p2.c`, tests on 03305/01629/05558/07435/08201 vs the length-capped state counts.
- **"Rotation ... lifted the floor that kept every path pinched"** → P2 can't rank conjugations (it's rotation-free), so
  climbing rotations sit at rank 8–9. Score what a rotation unlocks: a true 2–3-move lookahead over real moves (L2, L3),
  added to the score zoo, reported separately on conjugation steps.
- **"Perfect symmetry is a quiet cage"** → test whether record paths avoid symmetric states (r1 a rotation/inverse/mirror
  image of r0); if so, rank symmetric states down. In the score zoo.
- **"What needed a licence is gone with the pairing"** = bounds that rely on definiteness (monotone length, positive
  metrics) fail at the wall, exact counts survive — the same lesson as B94 and our dead invariant lower bounds.

## 2026-09-28 10:05Z, session 2 (lead): the whole atlas thrown at AC — ledger, score zoo, beam ideas
- **Full atlas ledger:** `research/acc/live/ATLAS_AC_LEDGER.md` — every plate and card (21 plates, 93 cards B1–B96,
  18 repo cards; 132 lines): 23 METHOD, 20 DIAGNOSTIC, 18 PROCESS, 71 NONE. Working methods so far: B31/Plate IV (P2),
  B81 (mirror transport in cross-row). Dead: B6, B12, B22, B38, B48 and three repo cards. Two quick tie-break tests
  under P2 (exit counts; learned descent) are dead (ledger appendix).
- **R_n caution:** R_n = (x^2 y X y, x y^n X Y^(n+1)) is the classic Miller–Schupp potential-counterexample family.
  Two of its rows (ac-02842, ac-06556) are on our AK(3)-class list, so R_3 is AK(3)-equivalent (open). Treat the
  21 unsolved R_n rows as open problems, not targets.
- **Ledger #2 as written is ill-posed:** counting x letters rewards pasting relator copies (move 2 "gains" 9 x per move
  with no progress). Needs a group-aware mass (e.g. the level index (k, a) of the chain form), not letter counts.
- **Running (discovery mode, per the team lead):** score zoo (`optimality/score_zoo.py`): 20+ atlas-derived state
  scores screened on the 609 record paths by how well they rank the record move, especially on hump steps, alone and
  as tie-breaks under P2. Winners go into the beam like P2 did. Separately: BEAM_QUOTA (B16/B17), BEAM_WH (B83), and
  the B20 beam-loss trace, A/B against P2=2.

## 2026-09-28 09:25Z, session 2 (lead): Bob's training macros as beam supermoves — DEAD (valid rerun)
- Matched A/B, T8, W=20k, depth live+6, BEAM_H=1 DIV=0.8, top-40 macros (len ≥ 4) from `ledger/bob_macro_library_20260928.json`,
  on the macro-capable binary (checked "macros: 40"):
| row (live) | plain | + Bob40 |
|---|---|---|
| ac-00145 (39) | 40 | 51 |
| ac-09189 (30) | 31 | 31 |
| ac-05702 (39) | 47 | 52 |
| ac-06045 (36) | 39 | 49 |
| ac-08995 (45) | 47 | 65 |
| ac-00147, 04276, 09091, 00037 | none | none |
- Macros better on 0 rows, worse on 4, same on 5. Kill condition met: the training rhythm (real in the 424 training
  routes, p = 0.001) does not transfer as supermoves at MACW=1; it crowds the beam. Matches Codex's transfer test
  (AUC 0.588, p = 0.567). A lower MACW or a few macros only is the one variant left untried.
- Also: the sacbeat beam (long Stable AC beat rows, T9) is stopped for good; P2 shows no signal above record ~45
  (session 1), and T9 thrashing slowed the P2 lanes. New P2 lane `p2ms`: the 18 doubling-chain rows with n = 4, 5.

## 2026-09-28 08:30Z, session 2 (lead): Bob's macro A/B was invalid until now — rerunning
- The scratch `acc_beam` binary (rebuilt from the repo after the container restart) has **no BEAM_MACROS code**, so
  the "macro" arm silently ran the plain beam (identical lengths and times on 5 rows). Any macro result from that
  binary is void. `acc_beam_p2` (current `acc_beam.c`) loads them ("macros: 40") and is byte-identical to plain
  when BEAM_P2 is unset. The macro arm is rerunning on it (T8, W=20k, depth live+6); the plain arm stands.
- Lesson for every helper: check the beam's stderr for "macros: N" / "p2:" before trusting an option A/B.

## 2026-09-28 07:58Z, session 2 helper: MS(n,BS) super-relator doubling — blocked by the helper generator; verified fallback, no beat
- **Where g gets stuck.** (1) Exponent matrix stays unimodular, and S_a's row is divisible by a, so S_a (a>=2) can never be a relator without a stabilization letter g. (2) If g occurs once, two inverse uses of that tool whose g's cancel equal the part between them (free-group identity), so g cannot be cancelled by the same tool; an exhaustive tag-position check found 0 clean arrangements. (3) Doubling needs the X^a-conjugate of a tagged copy. The conjugation carries g into X^(2a), the X|Y seam, the output block, or the y x^a|X^a Y junction. Each position blocks the next crossing or needs a second, differently tagged copy, whose own g has the same problem one level later. Tags at a tool's end are harmless to use (1 move to r1's front) but such a tool cannot be the conjugated factor.
- **BFS facts.** An isolated rank-2 level costs 2a moves: `1 4 (7 4)^(a-1)` (a=2: 4, a=4: 8) instead of 3a-1. It leaves BS slid to X^(a-1) BS x^(a-1). From that state no next level completes within 10 moves (a clean start needs 8), so no chained saving was found.
- **Verified fallback** `tools/acc/sac_ms_bs.py`: Codex rank-2 build, then `6 2 10 10 5 7 0 8`, then the rank-3 fast tail. Official CLI ok. n=5..10: 127/236/442/850/1648/3232 against records 82/147/277/534/1048/2073, so **no submission line**. Ledger: `ledger/sac_ms_bs_20260928.json`. A beat needs a build at <=1.55-1.87 moves per crossing. The leaders' ~1 move per crossing rank-2 mechanism is still unknown.

## 2026-09-28 07:20Z, session 2 (lead): P2 BEAM WORKS — record-length paths on hump rows; now sweeping 615 rows
- Matched A/B at W=20,000, depth record+6, BEAM_H=1 BEAM_DIV=0.8, T8 table (helper; raw `S/p2beam/ab_results.jsonl`):
| row (AC/SAC record) | plain | P2=1 | **P2=2** |
|---|---|---|---|
| ac-03305 (23/24) | 29/31 | 24/26 | 24/**24** |
| ac-01629 (23/25) | 26/28 | **23**/26 | **23**/26 |
| ac-05558 (24/26) | 30/32 | 26/28 | 26/28 |
| ac-07435 (26/28) | 29/32 | 28/29 | 28/29 |
| ac-06045 (36/38) | 44/46 | 44/46 | 39/42 |
| ac-00145 (39/41) | 40/43 | timeout | timeout |
- P2=2 (P2 then H priority) ≥ P2=1 everywhere. The hump rows that needed 133M exact states and cap 37–40
  fall to a 1-minute P2 beam. Cost: ~4–20× the plain beam per row.
- **Running now:** two P2=2 lanes (`tools/acc/ops/p2_list.sh p2a|p2b 20000`) over 615 rows with record ≤ 45,
  k = 1–3, that we don't tie (AK(3) rows excluded), shortest records first. The exact easy/midB/midD sweeps
  are stopped (progress saved in `live/sweeps/`); P2 is far more productive per core.
- Helpers with spare CPU: run P2=2 on your own lists (build `acc_beam.c` with `-O3`; set `BEAM_P2=2`).

## 2026-09-28 06:35Z, session 2 (lead): rank-3 super-relator build for MS(n, BS) (claimed, helper working)
- Building on Codex's generator (3a−1 per level because BS is re-conjugated between single crossings):
  the super-relator **S_a = X^a Y x^(2a) y** crosses y over the whole block x^a in ONE multiplication
  (r1 = P y x^a → r1·S_a = P x^(2a) y), and it doubles exactly: **S_(2a) = (X^a S_a x^a)·S_a** (free-reduces to
  X^(2a) Y x^(4a) y). S_1 = XYxxy = r0^-1. Rank 2 has no room for the second copy; Stable AC's stabilized slot
  does, if the helper generator g can be kept at a harmless end. Cost per level ≈ a (the X^a conjugation) + O(1),
  so the whole build ≈ 2^(n-1) + O(n), then the fast peel. That would beat every doubling-chain Stable AC record
  by a wide margin. **Claimed by session 2's helper** (`tools/acc/sac_ms_bs.py`); others please don't duplicate.

## 2026-09-28, Codex ABC: complete constructive generator for MS(n, YXXyx)
- `research/acc/optimality/yxxyx_chain.py` builds an ordinary AC certificate for every n>=2 and checks it with pinned official `core.verify`. At level j (a=2^j, k=n+1-j), `(YXXyx, Y^k X y^(k-1) x^a)` becomes `(YXXyx, Y^(k-1) X y^(k-2) x^(2a))` by `10^(a-1), 5, (11,5)^(a-1), 12`. This is an exact primitive-move identity, checked at every level n=2..10. The remaining `Yx^(2^n-1)` finishes via `6 2 10 10 5, 3^(2^n-3), 5 11 2`.
- Length is `4*2^n+2-n`. Scored n=5..10 all **pass the official verifier** and limits: 125, 252, 507, 1018, 2041, 4088 moves; peaks 63..2047, max work 1,961,556 (<5M). Snapshot records 80,145,275,532,1046,2071; thus **no submission line**. Metadata, hashes and exact command in `ledger/codex_yxxyx_generator_20260928.json`. The script emits the full move arrays for every n.
- Bottleneck is now explicit: rotating `a-1` trailing x's into place plus `(11,5)^(a-1)` costs 3a-1 per level. To tie the leaders, replace the rotation/crossing schedule with a block closer to a moves per level, or avoid a full final expansion. H-beam n=5 from the forced 18-move prefix found no finish at W=80,000/depth 70; bounded miss only.

## 2026-09-28, Codex ABC: YXXyx chain trace (official replay)
- `ledger/codex_yxxyx_trace.py` and `ledger/codex_yxxyx_trace_20260928.json` verify two uniform prefixes for synthetic MS(n, YXXyx), n=3..10: nine moves `5 1 12 4 1 10 5 12 10` give `(BS, x^3 Y^(n-1) X y^(n-2) x)`; an alternate 18 moves give `(BS, x^7 Y^(n-2) X y^(n-3) x)`. In both formulas the product is freely reduced; BS=`YXXyx`.
- An H-beam found an **officially verified 29-move n=3 path** (peak total length 19); the lead's 30-move path stays within cap 16, so this is an unrestricted shortening, not a cap-16 contradiction. Another found a **verified 55-move n=4 path** (peak 31). Both are synthetic/training instances, not submission lines. The n=4 certificate shows last build `5 [11,5]^7 12` (16 moves) from `x^7 YYXyx` to `Yx^15`, then 21 moves to `(x,y)`. The last build is the factor-of-two bottleneck; the same finish cannot be pasted into n=5 because the extra Y/y layer remains.
- n=5 H-beam from the original start found no path with T8 at W=20,000/depth 100 or W=80,000/depth 105 (the latter used DIV=.75, BAL=.2). These are beam misses, not bounds. A forced 18-move-prefix continuation is being tested separately.

## 2026-09-28 06:05Z, session 2 (lead): STABLE AC FAST PEEL — a beat lane on every doubling-chain row
- **Every doubling-chain Stable AC record is exactly the AC record + 2** (68 rows, n = 4..10, 10 chains). Nobody
  uses rank ≥ 3 on them (the team lead's point: most teams treat Stable AC as AC + 2). A shorter SAC road is a
  **beat = 1 point whatever k is.**
- **Fast peel** (`tools/acc/sac_fast_peel.py`, official `stable_core`, self-tested to the empty presentation):
  from (x, y X^m): stabilize g, make r2 = g X^k (k moves), swap each X^k block of r1 for one G (2 moves:
  r1 ← r1·r2^-1, conjugate r1 by G), peel the rest, reduce r2 to g, peel the G's, destabilize all.
  Cost ≈ 2k + 3m/k: m=63 → 44 (plain 65), 127 → 61 (129), 255 → 84 (257), 511 → 117 (513), **1023 → 164 (1025)**.
- **Build budget for a beat** (reach (x, y X^(2^n−1)) within this many moves, then append the fast peel):
  n=6 102–133 (slack 21 over the leaders' estimated build), n=7 215–247 (68), n=8 449–487 (173),
  n=9 930–968 (396), **n=10 1908–1952 (861)**. Per row: `ledger/sac_fastpeel_targets_20260928.json`.
  So our build may be ~1.85·2^n at n=10 and still beat. The naive build (2 moves/crossing, ~2^(n+1)+17) just
  misses; session 1's level construction (~1.5–2·2^n) should clear n = 8..10 on all 10 chains (~30 rows).
- **Ask, session 1:** make `ms_construct.py` stop at the state (x, y X^m) (or any r0 = x, r1 = y·X^m spelling) and
  write the prefix; I append the tail, verify the full `sac-` line with the official verifier, and send.
- Further gains: a second block level for the G's, and doing the build's x-mass in rank 3 as well.

## 2026-09-28 05:50Z, session 2 (lead): MS(n, YXXyx) — the level move is uniform in n; skip test
- The exact 9-move level path MS_3 → (BS, x^3 YYXyx) is `5 1 12 4 1 10 5 12 10`. **The same 9 moves on MS_4 give
  (BS, x^3 YYYXyyx)**: the level step does not depend on n. It alternates inversion (move 1) with
  multiplications, so one relator is worked from both ends without paying a conjugation per crossing. Move 4
  is the BS substitution y → x^-2 y x on the trailing y. Hypothesis: the leaders' ~1 move per x comes from this
  invert-and-multiply rhythm, applied at every level including the last (where our doubling pays 2 per x).
- **Skip test** (can we finish from (BS, x^a YYXyx) without doubling to YY x^(2a+1) y?): exact, a=1 (cap 13,
  complete): 12 moves, and the optimum *does* double first (5 11 5 12 → Yxxx, then an 8-move finish). a=3 (added 12:40Z
  from the transcript digest): cap 17 → 21 and cap 21 → 21 (51M states, 5,158 s, complete), path
  `0 4 11 4 11 4 11 4 1 12 3 6 2 4 4 4 4 4 4 4 8`: it also doubles first; no skip.
- Exact n=3 of MS(n, YXXyx) under cap 16: 30 moves (`5 1 12 4 1 10 5 12 7 5 6 5 11 5 11 5 1 6 12 3 10 4 2 2 2 2 2 4 1 2`),
  = the leaders' formula 2^(n+1)+n+11. Its finish gets r1 = X (x = 1) and peels r0 = xYx^5 with move 2.
- Exact n=2: 15 (`5 7 12 5 6 5 12 11 2 5 12 5 8 2 4`), finish steps down y=x^3 → y=x^2 → y=x (descent, not a peel).

## 2026-09-28, Codex ABC: borrowed-road joins through radius 7 remained behind
- Expanded the state-keyed suffix atlas of 478 officially valid AC roads (13,092 suffix states) with fresh prefixes. At radius 6/cap 35: ac-00766 visited 388,785 states, ac-00974 visited 581,530; best 34 and 26. At radius 7/cap 40: 3,035,716 and 4,578,426; best still 34 versus record 33 and 26 versus record 24. This tests joins into this particular atlas, not arbitrary new finish roads or global optimality. Code `ledger/codex_abc_crossjoin.py`; four raw JSON results `ledger/codex_abc_crossjoin_r{6,7}_{00766,00974}_20260928.json`. Do not spend more on the same small-radius atlas without new suffix roads.

## 2026-09-28, Codex ABC: T8/fixed visited passes a real stopped row, but no score
- On ac-00580 at total-length cap 28, the earlier T9 ledger stopped after depth 23 at 48,220,955 states. The T8/fixed-visited engine reproduced **exactly** that depth-23 count and continued into depth 24, stopping at a 60M-state budget after 95.61 seconds. No AC/SAC meet. This is a repeatable memory/scope improvement, not a complete search or proof. Full command, raw logs, and explicit incomplete status: `ledger/codex_abc_capped_trial.py`, `ledger/codex_abc_capped_trial_00580_20260928.*`.
- On Bob's ac-00766 near miss, cap 28 already had 426,246 states at depth 7; the next layer paged under shared 8 GB pressure. The run was interrupted and marked incomplete. A radius-8 goal ball plus a 25-step prefix could tie record 33, but this broad BFS is unlikely to reach such depth within our budget. Shift to route-specific joins or a different road, not a higher broad cap. `ledger/codex_abc_capped_trial_00766_20260928.*`.

## 2026-09-28 05:45Z, session 2 (lead): Miller–Schupp families — scale, the clean BS case, and the crux
- **650 rows in the MS families are held by 1–2 teams** (by n: n=5 115, n=6 105, n=8 77, n=7 71, n=4 67, n=1 65,
  n=3 56, n=9 52, n=10 36). Source: `ledger/ms_families_by_w_20260928.json`.
- **Cleanest case: first relator already BS.** 80 rows have r0 = YXXyx (y^-1 x^-2 y x, i.e. y x y^-1 = x^2);
  about 40 are held by one team. For w = YXXyx, r1 = Y^(n+1) X y^n x: BS gives y^n x = x^(2^n) y^n, so r1 is
  equivalent to **y = x^(2^n − 1)**. Path = push x left through y^n (2^n − 1 crossings "y x → x x y", each one
  multiplication by r0^-1 = XYxxy at the END of r1) → setup → peel 2^n − 2 (one x per move with r0 ≡ x).
  Records n=5..10: 80, 145, 275, 532, 1046, 2071 = 2^(n+1) + n + ~11, all k=1.
- **The crux:** a crossing only acts at the end of r1, and after one the word ends "…x x y", so the next x
  must be rotated in (1 conjugation): 2 moves per crossing → ~3·2^n total. The records need ~1 move per
  crossing. Whoever finds how to chain crossings without a rotation unlocks the whole family set.
- Running: exact capped search on the n=2 BS case (y = x^3) to see the optimal crossing pattern; H-beam
  from the n=4 BS stage of w = YXyXyx (record 56).
- Also worth a look: w = YYXYYxyyX has slowly growing records 42, 43, 76, 81, 134, 159 (n=5..10, all k=1):
  a different, non-doubling mechanism, and short enough for our beam.

## 2026-09-28 05:30Z, session 2 (lead): P2 SURVIVES; Miller–Schupp doubling chain, first phase is general
**P2 test** (`optimality/p2_hump_test.py`, `ledger/p2_hump_test_20260928.json`): 609 verified paths on 526 rows,
240 at the live record, 56 of them hump paths.
| score | median climb | climbing moves in top 3 |
|---|---|---|
| raw length | 9 | 0.00 |
| P1 | 2 | 0.22 |
| P1m (rotate the multiplier only) | 1.5 | 0.41 |
| P2 (cut 8) | 0 | 0.22 |
| P2 cut 8, then P1m, then raw | 0 | 0.41 |
- Kill conditions not met: P2 survives. Its ranking gain is on multiplication moves only (conjugations leave it
  unchanged). P2 predicts moves remaining better than length (leave-one-out error 3.18 vs 4.52).
- C cost: P2 cut 8 is 15–97 µs per state; only the 4 multiplication children need it. About 1–5 min per row at
  W=20,000, depth 40. **Next: `BEAM_P2` in `acc_beam.c` (P2 cut 8 → P1m → raw) and a matched A/B on hump rows.**
- Add-ons: E1 weak survive (min relator length rises on 96% of humps, but (min,max,P2) predicts best: 2.18);
  U1 dead (median same-relator run 2); C1 survives (humps: fewer hyperbolic, more finite-order transfers, p=0.005).

**Miller–Schupp doubling chain (building on session 1's find), w = YXyXyx, r1 = Y^(n+1) X y^n x:**
- Our n=3 path (ac-09243, 36; record 32) has 4 phases: reduce (18) → build r0 = Y x^7 (6) → set up r1 = X^6 y (5)
  → peel one x per move (6) + 1.
- **The reduce phase's first part is general:** moves `3,8,2,6,12,4` then `12` × n turn every n into
  r0 = y X Y^(n-1) x Y X y^n, r1 = XyxYX (the Baumslag–Solitar relator y x y^-1 = x^2). Checked n = 3..6.
- In the group, the target is r0 = Y x^(2^n − 1) (n=4: Y x^15), then the peel.
- **The crux is the build:** our build costs ~2 moves per new x (1 multiplication + 1 conjugation to rotate).
  The records (2^(n+1) + 16..40) imply ~1 move per x in build and peel. 2 per x gives ~3·2^n (n=10: ~3,100 vs 2,088).
- H-beam from the n=4 BS-stage state (10 moves in), W=50k, depth 46: AC 54 from the state = **64 total** vs record 56
  (result added 12:40Z from the digest; path in scratch `work/ms_n4_path.txt`). No gain.

## 2026-09-28, Codex ABC: smaller goal ball for constrained memory
- Built T8 with `work/acc_opt tball 8 40000000 work/T8.tab work/abc_t8`: 24,587,144 goal states, 640,000,000 bytes, SHA-256 `38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8`. T9 has 214,977,551 states and 4,480,000,000 bytes. The smaller map removes 3.84 GB of table footprint while requiring up to one additional forward move for the same meet length.
- On a known ac-00236 15-move path at cap 25, the disk-backed capped engine found an officially accepted AC 15 and SAC 17 with both tables. T9 first saw AC 15 at forward depth 6 (2,561 cumulative states); T8 first saw it at depth 7 (7,615 cumulative). Same depth-7 final state count in the benchmark; wall times are confounded by file cache, so no speed claim. Code and raw results: `ledger/codex_abc_ball_split.py` and `ledger/codex_abc_ball_split_20260928.json`.
- Adam's first 100 unsolved rows, width 2,000/depth 80, yielded no AC or SAC path under either `BEAM_H=1` or `BEAM_H=1 BEAM_BAL=1` with T8; 200 complete bounded rows total. The T9 H pass reached 88 no-path rows and six 45-second timeouts before contention made the remaining six impractical. No inbox line. Stop these 100 rows per the handoff rule. The next useful test is T8 on a specific memory-limited capped row at a fixed budget, measuring whether the extra forward frontier is cheaper than keeping T9 resident.

## 2026-09-28, Codex helper: reserved high-slack Stable AC beat beam screen (no hits)

- Screened the six rows removed from the main sacbeat list: ac-00520, ac-00718, ac-01566, ac-00074, ac-03887, ac-03104. Target AC ceilings were SAC live record minus 3, so AC + [16,15] would strictly beat the Stable AC record.
- Baseline: pinned T9 finish table, `BEAM_H=1 BEAM_DIV=1.0 BEAM_BAL=0`, width 20,000, depth through each target ceiling + 2. All six returned `nopath`.
- Different second pass on the three loosest rows (ac-03104, ac-03887, ac-00074): `BEAM_H=1 BEAM_DIV=0.6 BEAM_BAL=0.75 BEAM_NOV=1 BEAM_NOISE=1 BEAM_SEED=20260928`, width 20,000, same depth policy. All three returned `nopath`.
- These are bounded beam misses, not proofs. No candidate path or verifier receipt was produced. Exact timings and thresholds: `research/acc/live/ledger/luna_sacbeat_screen_20260928.json`. Official SAIR commit: `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`; T9 SHA-256 matches the expected build.
- Follow-on: resume only after refreshing exclusions and worklists; do not interpret this screen as an exhaustive search.

## 2026-09-28, Codex ABC ledger correction
- `ledger/exact_capped_runs.jsonl` has 76 entries, 52 marked incomplete. Their median state count is 48,936,404.5; only one incomplete entry is at least 180M, with max 211,651,126. They stopped at different row budgets or limits. The shorthand “52 stopped at ~210M” is misleading; prioritize by actual budget, cap, and depth before rerunning with the disk-backed pilot.

## 2026-09-28, Codex ABC follow-up: rhythm transfer failed and BAL flag dependency
- On 478 real borrowed routes (237 ties, 241 trailing), the training nonundo transition score has tie-vs-trailing AUC 0.588. Shuffling tie/trail labels within 5-move record bins gives mean 0.577 and p = 0.567. No evidence this score ranks better roads in the current atlas; do not inject it into the beam without a stronger transfer test. Reproduce with `ledger/codex_abc_rhythm_transfer.py` and `ledger/codex_abc_rhythm_transfer_20260928.json`.
- Code inspection: `BEAM_BAL` contributes only inside `hprio`, which `acc_beam.c` calls only when `BEAM_H=1`. A standalone `BEAM_BAL=1` is identical to the vanilla length beam. The second unsolved sweep must set both `BEAM_H=1 BEAM_BAL=1`. A bounded width-2,000/depth-80 screen is in progress after width-20,000 runs paged under concurrent load. `run_beam_abc.py` records that width explicitly and skips expensive window work for a first unsolved hit.

## 2026-09-28, Codex ABC: short alternate joins, move rhythm, and visited-table memory
- **Bob join idea:** Replay all 478 officially valid borrowed AC paths to form a 13,092-state suffix atlas. Search exact distinct states to radius 5 from ac-00766 and ac-00974 (total relator length cap 60), then join any atlas suffix. Reached 124,740 and 130,399 states; best verified routes remain 34 (record 33) and 26 (record 24). Prior window-14 checks were already negative. Scope is radius 5 plus this atlas, not a global bound. Code/data: `ledger/codex_abc_crossjoin.py`, `ledger/codex_abc_crossjoin_20260928.json`.
- **Bob rhythm idea:** The 424 official training routes (all Miller–Schupp) have held-out one-step move prediction gain 0.482 bits/move versus within-route shuffle mean -0.0056 (1,000 shuffles, p < 0.002). Conditioning out immediate inverse moves leaves 0.401 versus -0.0052 bits/move. This is a real sequence pattern in training, but transfer to other challenge families is untested. Code/results in `ledger/codex_abc_rhythm.py` and `ledger/codex_abc_rhythm_20260928.json`.
- **Charlie memory idea:** Built `research/acc/optimality/acc_capped_disk.c`, an optional file-backed, fixed-size visited table sized from the state budget, preserving the existing 123-bit fingerprint convention. The cap-24 radius-7 pilot on ac-00974 matched original at 299,177 states. Wall time was unstable (disk repeat 73 s versus original 7 s under shared 8 GB pressure), so no large-row improvement claimed. Also piloted rank <=3 radius 5+5 on ac-00520/ac-00718: no meet; the latter had two word-cap overflows and no valid negative bound. Details in `ledger/codex_abc_disk_benchmark*.json` and `ledger/codex_abc_rank3_probe_20260928.json`.

## 2026-09-28 05:00Z, session 2 (lead): the team lead's older ACC repos (mad-hatters-acc-private, acwindow-lean)
- **47 unsolved AC rows are in the AK(3) class** (open problem). List and provenance:
  `research/acc/live/AK3_CLASS_ROWS.json`. Found by matching every start against acwindow-lean's exhaustive
  AK(3)-class walk (≤ 26 letters, 1.28M members); rechecked independently by the lead. **Skip them.**
  Next: extend the class walk past 26 letters to catch longer AK(3)-class rows (1,794 unsolved rows start ≤ 26).
- No old path ties or beats a live record (only ac-00276 at 52/104; record 39, we already tie it).
- **Primitive-relator finish** (acwindow-lean `evidence/genus/primitive.py`, Lemma A in `notes/ACWindow_note.md`): a state
  where one relator is primitive can always be finished, and the proof builds the path, so it is a much
  larger finish target than T9. Screen: 0 of 2,672 unsolved rows reach one within 2 moves or one multiplication
  at any rotation, so no shortcut now. It could still be a cheap stop test inside the beam. O(L) pre-filter: a
  primitive cyclic word has a letter that appears with only one sign. Path builder not written.
- Cyclic-class walk (`evidence/genus/house_walk_resumable.py`): groups rows into AC classes (solve one, get all). Not a valid
  relaxation for pruning the capped search. Its 5-minute pickle checkpoints are worth copying.
- Failed before, don't revive: genus/thickenability test (primitive appears at depth 2, genus 0 only at 6);
  cap-lift identity loops (Codex; no gain on 00037, 00313).
- acwindow-lean's Lean proofs: AK(n) → AK(−n−1) fold; a 9-move path for AK(3)'s image in C5*C5; `ACCWell`
  (the formal shape of our capped proofs, but it needs a move-count version). No new pruning rule.
- Prior art list worth reading: mad-hatters-acc-private `ACC_PRIOR_ART_CORRIDOR_HANDOFF_2026-09-13.md` (Carreras 2607.23611,
  Two-Hump, Myasnikov–Myasnikov–Shpilrain).

## 2026-09-28 04:55Z, session 2 (lead): ideas from the team lead's older Lean repos
Read: coxeter-rank2-lean, elemental-peeling-lean, upg-lean, relational-atlas-lean (no data in any; Lean + build checkers).
Being tested now on all known hump paths, together with P2:
- **E1, keep the two lengths separate** (elemental-peeling `resolvedLedger_le_commonFloor`,
  `no_common_record_predictor`). Does min(|r0|,|r1|) stay at or below its start while the total climbs?
  If so, reserve ~20% of the beam for the smallest min. Kill: min rises on most humps and (min,max)
  explains no more of the moves-remaining spread than L.
- **U1, one relator at a time** (upg `UPGFeedback`, `UPGBlockFeedback`: a block runs independently when its
  coupling is zero). Hold r1 fixed and search r0 with its 7 moves, then swap. Branching ~6 instead of 13, so
  exact BFS reaches ~10–11 plies in 180M states instead of ~7. Kill: median same-relator run under 3.
- **C1, exponent-sum class of humps** (coxeter-rank2 `Uaff_iterate`): T = M_end·M_start⁻¹ over each hump;
  ±I / finite / parabolic / hyperbolic. Filters Bob's macros by class. Kill: hump class mix = random segments.
- **E2, pair synergy** I(a,b) = L(abs) − L(as) − L(bs) + L(s), free inside P2. Tiebreak on flat P2 plateaus.
- Dropped: finite-quotient distances (dihedral, Heisenberg): their ceiling is ~log, same as invariant bounds.
  relational-atlas-lean: nothing usable for AC.

## 2026-09-28 04:45Z, session 2 (lead): the team lead's atlas (Drive PDF, 2026-08-27) applied to AC
Source: `research/acc/atlas_drive/THE_OPERATOR_FIRST_ATLAS_20260827.txt` (Plates I–XXI, bridges B1–B84, full text).
Quick checks on 7 known paths (exact: 03305, 01629, 05558, 07435, 08201; ours: 00145, 05064):
- **Dead first:** humps are not conjugation padding. The cyclically reduced total climbs as much as the raw
  total (03305 +16/+16, 05064 +14/+14). Ranking by cyclic length alone is out.
- **1. P2 lookahead (B31 + Plates XII, XIV).** Conjugations stay inside a conjugacy class; only
  multiplications change class. P_k = best total after k multiplications with free cyclic rotations.
  On 03305's exact path: raw climbs +16, P1 +10, **P2 climbs 0**; the two climbing moves rank 11th/10th of
  14 by raw length but tied-best by P2. Caveat: P2 is flat (ties 9–13 of 13 siblings), so use P2 first,
  length second. **Being validated on every known hump path now** (`optimality/p2_hump_test.py`).
  Kill: P2 median climb ≥ half the raw climb, or climbing moves not ranked better than by length.
- **2. Per-class beam quota (B16, B17, L4):** overflow piles into a few classes; give each class its own
  slots. Class = pair of cyclic conjugacy classes (finer than `BEAM_NOV`). Kill: the record path's class
  is still in the plain beam when the path is lost, or no gain at matched width.
- **3. Macro rate extrapolation (B69, Plate XV):** apply a macro once and twice, extrapolate, expand
  (macro, best repeat count) as one child. Pairs with Bob's library.
- **4. Whitehead-minimal frame (B83, Plate XVIII):** climbs +12 on 03305 (weaker than P2), 0 on the other
  four exact paths. It reaches a basis pair 8 moves before the end on 03305, so an exact Nielsen finish
  could reach past the 9-move table.
- **5. Where the beam loses the path (B20, Plate XI):** at each depth, the record-path state's rank and tie
  count in the beam at W and 2W. Lost among ties → add an axis (1 or 4); rank ≫ W → wrong score; saved by
  2W → only width.
- Knots, volumes, geometric tensors: invariants only, and invariant bounds are already ruled out.
- The 2026-09-12 bundle (atlas book) exists on Drive only as a 3.5 MB zip; needs a manual upload to read.

## 2026-09-28 04:20Z, session 2 (lead): Bob's macros go into the beam (test running)
- Bob's library plugs straight into `acc_beam` (`BEAM_MACROS`, `BEAM_MACW`): macros are official
  AC move indices 0–13 with length ≤ 8. File: top 40 by solution count with length ≥ 4
  (`2 5 2 8`, `4 1 2 0`, `0 2 5 2 8`, ...).
- A/B at matched width (W=20000, depth = live + 6, `BEAM_H=1 BEAM_DIV=0.8`): plain vs + Bob40, on
  the 9 near-miss rows of session 1's BAL test (ac-00145, 09189, 00147, 04276, 05702, 06045, 08995,
  09091, 00037). Kill condition: macros never shorter than plain and never find a path where plain
  finds none. Note: the macro arm evaluates (14 + 40) children per node, not 14, so it spends more
  work per kept state.
- Result goes here when done.

## 2026-09-28 — Bob — move rhythm (training_424)
Tested: repeated macros vs permutation and pair-preserving (doublet) shuffles, 1000 each, kill = no stat beats doublet at p<0.01.
Result: SURVIVES as blocks — tandem repeats 589 vs 365±17, shared 6-grams 326 vs 36±4 (p=0.001 floor); DIES as a beat — conjugation periodogram p=0.22.
Core macro: 4,·,2,5,2 (r1*=r0, r0*=r1, r1*=r0^-1, r0*=r1), across 20-43 distinct w. Library: ledger/bob_macro_library_20260928.json (977 macros).
Next (untested): top macros as acc_beam supermoves on stalled rows vs plain beam at matched budget.
Record: ledger/BOB_move_rhythm_20260928.md

## 2026-09-28 03:50Z, session 2 (lead): the team lead's Stable AC insight
- **Idea (the team lead):** many teams only do AC and never send the Stable AC line, so Stable AC is
  thinner.
- **Board check (7,443 rows solved on both):**
  - Average teams on a record: AC 3.05, Stable AC 2.85. Stable AC has fewer teams on 1,148 rows and
    more on 530.
  - **95 rows have a Stable AC record longer than AC record + 2.** All of them are held on AC by one
    team that never sent AC + [16,15].
  - On those rows, any AC path of length ≤ SAC record − 3 **beats** Stable AC (1 point), even if it is
    above the AC record. Slack above the AC record: 0 on 42 rows, 1 on 22, 2 on 10, ≥ 3 on 21 (e.g.
    ac-03179: AC 55, any AC ≤ 59 beats SAC 62; ac-04396: AC 68, ≤ 73 beats 76).
- **Running:**
  - `sacbeat`: H-beam W = 200k over the 95 rows, slack ≥ 3 first, shortest first. `tools/acc/ops/beam_list.sh`.
  - `k2ac`: AC rows held by 2 teams, record ≤ 36, AC only, with the SAC tie taken for free via + [16,15].
    7 new rows (another 15 are already in sweeps A/B); then sweep D resumes.
- For the helpers: the sacbeat list is `research/acc/live/sweeps/sacbeat_targets.json`. A route map that
  gets any AC path under `record` on one of these rows is worth a full point on Stable AC.

## 2026-09-28 03:10Z, session 2 (lead): reverse search? No, the humps sit mid-path
- **Idea** (the lead's "look in the glass"): search from the finish backwards, so the uncapped 9-move ball
  sits at the start. It would help if record paths climb near the start.
- **Checked on the 5 exact paths:** the peaks come at 30–52% of the way (03305 step 7 of 23, 01629 12/23,
  05558 12/24, 07435 12/26, 08201 11/31). A reverse search needs the same cap as the forward one.
  Closed.
- **ChatGPT's ac-06095 windows (gap 15–16, empty):** one more local repair coming back empty, which fits
  "the record paths are different roads". Suggestion for the helpers: stop local repair on near-misses
  and put helper time on unsolved rows that are close to solved ones, or on the deep 1–2-team rows with a
  fresh route (not a repair).
- **Ops:** sweep C finished its 77 rows (no new ties). Sweep B's remaining 261 rows are split: B keeps 130,
  new sweep D takes 131 (60M budget).
- **My mistake:** a cleanup `rm -rf cap_ac-0*` also deleted sweep A's live layer files (ac-01104, cap 31
  → FATAL, recorded as incomplete, so no false bound). Rule: only delete the work dir of the row whose
  sweep you stopped. Re-run ac-01104 at cap 31 later.

## 2026-09-28, ChatGPT helper: ac-06095 exact peak-window screen
- **Target:** reserved helper lane, ac-06095 47 vs record 42 (k=1); matching SAC is 49 vs 44 (k=1). No submission line found.
- **Input replay:** the candidate route reaches exact (x,y); its maximum total relator length is 31, first at state P[5]. Move set is the pinned ac-r2-v1 moves 0-13.
- **Gap 15:** checked windows [0,15] through [5,20], using radius 7 from each endpoint. Caps 31, 33, 35, 37, 40, 43, 46, 50, 60, 70, 80, 90 all had zero intersections. Cap 4096 was also empty and is effectively uncapped for these radius-7 balls: each endpoint has L<=31 and one move has L_next<=2L, so L<=3968 through depth 7. At cap 4096 the largest sides had 10,885,023 and 10,842,301 states.
- **Gap 16:** checked windows [0,16] through [5,21] with radii 7+8. All six were empty at caps 31, 40, and 50; largest B-side: 1,326,497, 8,802,044, and 18,151,396 states respectively. At cap 60, windows [0,16], [1,17], [2,18] were empty (largest side 30,320,682 states); the runtime disconnected before I captured the remaining three windows, so cap 60 is incomplete.
- **Result:** no shorter splice. The path remains 47. This is window-local, not a global optimality result. The table deduplicates 123-bit fingerprints, so record these as completed fingerprint searches rather than collision-free formal certificates.
- **Drive cross-check:** `ACC_WARROOM_ARCHAEOLOGY_LIVE_ROUTES_20260922.md` reports 73 H3(F5)-stationary, full-state-changing macros from 116 occurrences, but no shortening yield; these are recorded-state-specific and must be replayed at each use. Its higher-yield direction is to start from a certified ADVANCE port and meet the larger solved-side region T14/T16, not just (x,y). The first-pass basin atlas covers ac-02842 and root families, not ac-06095. The `ACWindow_note` is a proof-track note, not a path-shortening method.
- **Next macro experiment (not yet run):** mine short move strings from verified paths where total length rises then returns near its prior level. Treat each string as a beam supermove with cost equal to its actual move count, retain its full expansion for official replay, and keep a reserved high-height beam band so intermediate hump states do not have to survive ranking. Use the 73 recorded-state macros only as training examples; only the move strings are portable, and every application must be replayed from its new source state. A/B against the current score on exact hump controls ac-03305/ac-01629 plus a held-out row at equal node budgets. Success criterion: a verified path at or below live record, not just lower relator length.
- **Audit:** `research/acc/optimality/ac-06095_peak_window_audit_20260928.json`. Next exact action: finish cap 60 on the last three gap-16 windows after compute reconnects, then consider gap 17.
## 2026-09-28 03:15Z, session 2 (lead): Schur macros and the echo ("take it back")
- **Schur elimination as macro-moves** (atlas UPG-FEEDBACK). `mine_macros.py` mines up-and-back-down
  excursions (2–6 moves) from 210 known paths, expanded by the 16 move symmetries: 36,194 distinct.
  `acc_beam` now takes `BEAM_MACROS=file BEAM_MACW=w`. Each macro is one extra child and carries its
  true path length. Identical output with no macros. On ac-03305 (exact 23, beam 27), with macros mined
  leave-one-out: 27 at w = 0.5, 1, 2. A 4-row A/B on near-miss rows is running (old / macros / shadow).
- **Echo table** (the lead's verse: "the echo from the back is still talking to you"). States on or
  within r moves of our known routes, each with a known remaining distance, become extra targets for the
  exact capped search (`acc_capped` `ECHO_FILE=`, `build_echo.py`). A capped BFS state that meets the echo
  at depth d gives a path d + remaining, and the known tail completes it.
  - ac-05818 (record 34, ours 35): 7 routes (Codex map + ours), 122,317 echo states (r = 3).
  - Cap 25, depth 25, 55M states: best echo path 35 (our own route). No 34 exists whose first part stays
    within total length 25 and then joins a radius-3 neighbourhood of our routes. This complements
    Codex's corridor result (no 34 inside the radius-6 union).
- **Takeaway:** local repair of our near-miss paths (windows, corridors, echo, macros) keeps coming back
  empty. The record paths for these rows are different roads, not repairs of ours.

## 2026-09-28 02:45Z, session 2 (lead): the team lead's atlas, tested on AC
Seven ideas were read from the repo (atlas cards, UPG, Kakeya frontier, compound-eye originals). Tested:
- **Probe shadows as certified lower bounds** (OBS-PROBE-SPAN, ALG-FORCING-DUAL). Map words into
  SL(2,p) and BFS the finite shadow G×G. Correct, but capped by the shadow's diameter, which grows
  only logarithmically: 9 at p = 7 (113k states), 11 at p = 11 (1.7M). The mean bound/record is 0.11,
  which is inside T9's exact range, so there's nothing new to prune. General lesson: invariant-based lower
  bounds are log-scale, because one multiplication can double a word.
  Code: `research/acc/optimality/shadow_bounds.py`.
- **Two-layer capacity split** (GRAPH-SUBGRAPH-CAPACITY): charge only r0-moves, then only r1-moves,
  and add. It collapses to ≤ 2 per layer, since free moves on one word can prepare any multiplier for the
  other. The layers aren't independent. (The card's own failure mode warns about this.)
- **Probe shadows as a guide** (exterior probe of the hidden interior). A real signal: on 4,429 states
  ≥ 10 moves from the finish along known paths, corr(moves left, shadow sum over 4 probes) = +0.31, while
  word length gives +0.02. On hump states, shadow +0.24 and length −0.24 (length points the wrong
  way). Built into the beam as `BEAM_SHADOW=w BEAM_SHADOW_FILE=probes.bin` (off by default;
  identical output at w = 0). The first test, ac-03305 at W = 100k, stayed at 27 for w = 0.5–4 (exact
  23). Needs a broader A/B.
  Code: `shadow_probe_export.py`, `acc_beam.c`.
- **Next, the most promising: Schur elimination of the hump (UPG-FEEDBACK).** Remove the high states
  and replace them by effective macro-moves between low states. In practice: mine "up-and-back-down"
  segments from exact and known paths and let the beam take each as one step, so hump states never
  compete on length.

## 2026-09-28 02:45Z, session 2 (lead): checking the Smith-chart findings on beam-free paths
- **Why:** the 163 charted paths mostly came from our beam, so they carry its habits. The exact
  capped hits are BFS-shortest within their cap and have no scoring at all, so they're the fair check.
- **Result on 5 exact paths (ac-03305, 01629, 05558, 07435, 08201):**
  - The first word reaches length 1 at 87–97% of the way. **Confirmed**, though these last moves
    are inside T9 anyway.
  - Balance at the midpoint: 0.71–0.93 on flat rows, but **0.38 and 0.44 on the big-hump rows**
    (ac-03305 +16, ac-01629 +4). Balance holds only where the row is easy.
  - Climb shape: the big hump climbs in **single steps, zig-zagging** (longest climb run 1 on
    03305), not in 1–3-move bursts.
- **Orders for the beam change (session 1):** keep balance as a *mild* term. Add a reserved band of
  beam slots for states 5–16 letters above the start (slow zig-zag climbers). A/B test before switching:
  1. Old vs new scoring, same 3 seeds per row.
  2. Two groups: flat rows (known record, our beam 1–2 over) and hump rows (ac-03305, ac-01629,
     whose exact paths are known).
  3. Adopt the new scoring only if it doesn't lose on the hump rows.

## 2026-09-28 01:17Z, Codex helper: ac-09311 one-over corridor
- **Idea:** on k=1 rows with a 42-move record, use a larger H beam to reach a one-over witness and merge its route with a divergent finish.
- **Checked:** ac-09239, ac-09165, ac-09317 at width 100k gave no finish. ac-09311 gave verified AC 44 at width 100k and verified AC 43 at width 180k. These share 24 initial states, then diverge; the map is `research/acc/optimality/ac-09311_two_routes_map.json`.
- **Result:** neither is a score against record 42. Exact local windows through 14 found no shortcut. Radius-6 union had 54,987,511 states, 48,227,459 reached within 42 moves, no tie. No inbox line or SAIR POST. Only paths within this corridor are excluded.
- **Next:** seek a third finish that leaves the first 24-state shared opening, or return to exact sweep hits when they arrive. Always check `SENT_ROWS.txt` and fresh board before queueing.

## 2026-09-28 01:15Z, ChatGPT helper: detour height and a Pareto pilot
- **Drive research read:** `ACC-P000009 — Detour width on two Andrews–Curtis graphs` distinguishes arbitrary-word Lean conjugation from scored `ac-r2-v1` letter conjugation.
- **Derived bound:** on solution-relevant states, `L>=2`; each scored move gives `L_next<=2L`. Therefore a depth-`d` path from initial total `L0` has height at most `L0*2^d`. For ac-00145 (`L0=15`), even depth 38 has a finite but unusable cap of 4,123,168,604,160.
- **New idea tested:** keep nondominated exact-state labels `(moves, peak total length)`; target labels answer shortest-distance queries for every cap. On a synthetic five-step control, the Pareto profile `(4,8)` matched separate capped BFS (no path at caps 2–7 through depth 5; shortest 4 at cap 8).
- **Negative result:** the Pareto pilot used 71,638 transitions versus 55,005 for the separate cap searches (about 30% more) on this small case. Do not replace the current sweep on this evidence. The test and graph-bound analysis are in `research/acc/optimality/detour_height_pareto_note_20260928.md`; runnable script is `research/acc/optimality/pareto_height_pilot_20260928.py`.
- **Cap discipline:** this independently supports keeping witness peak separate from exact `closed_cap_through`. The ac-00145 31-height witness does not certify exhaustion below 31.
- **Outcome:** method test only; no scored path. Next step is a matched-cost comparison on a non-active short row if one opens.

## 2026-09-28 00:57Z, Codex helper: state exclusion and four-route corridor on ac-00145
- **Idea:** ban exact ordered states from a known route at selected depths in the H beam to discover a second path with a different middle or opening, then search the union of route neighborhoods for any number of lane switches.
- **Checked:** three new official-CLI-verified AC 40 routes (all already covered by our accepted 40). A single-state ban at depth 24 gave a lower-peak finish; banning depths 5–22 gave a route with 23 new states before rejoining around state 24. The [four-route graph](../optimality/ac-00145_four_routes_map.json) has 85 nodes/88 labeled edges. Radius-5 union: 6,682,338 states, no ≤39 path; radius-6 union: 59,899,612 states, 55,165,741 reached within 39, no path. This is a corridor bound, not a global shortestness proof.
- **Next:** ac-05064, our accepted 40 versus record 38 (k=2), starts with the same first relator and one sign difference in the second. A verified beam 40 has no shortcut in 429 windows of lengths 2–14. An uncapped depth-4 exact bridge check from all 40 route states found 16 joins near the shared goal (503,190 source-local states), but the best combined line is 40, so no ≤38 bridge. The phase beam found no finish; the 400k H beam found another AC 40. Banning route states 5–22 produced an independent AC 41 with peak 33. Both routes resisted local windows through 14; their radius-6 union had 51,512,374 states and no ≤39 route (48,681,575 visited). Map: `research/acc/optimality/ac-05064_two_routes_map.json`. Next: try low-k AC 42–43 records from the user's ac-09xxx list, beginning ac-09239.
- **Duplicate gate:** neither 40-move line is a new submission. Check `SENT_ROWS.txt` and official verifier on any shorter candidate before inboxing.

## 2026-09-28 00:52Z, ChatGPT helper: ac-00145 route-peak audit and cap distinction
- **Target status:** `SENT_ROWS.txt` has ac-00145 at 40 vs live 39, k=1; it is already active in Sweep B, so I did not launch another search.
- **Replay:** independently ran the candidate from `ACC_CANDIDATE_00145_20260926.txt` through the pinned official core (commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`). It reaches exact `(x,y)` in 40 moves; work 620; receipt hash `sha256:bbfbb1176ddd44ec9eb509086c7a677f560a50b1ba1f5a784b82331adfe51dd4`.
- **Height:** total relator lengths by state are in `research/acc/optimality/ac-00145_route_peak_audit_20260928.json`. Peak is 31, first reached after move 24. Cap 31 contains the known route; cap 32 does too.
- **Cap correction to the 00:25 proposal:** a witness path's peak is not an exhaustive-search boundary. The 41 states on this route do not show that every state below total length 31 was searched. Track `known_route_peak` separately from `closed_cap_through`; skip a lower cap only when the exact run ledger certifies that cap is exhausted. For ac-00145, the peak gives a feasible ceiling for this witness, not a proof that lower caps are covered.
- **Outcome:** no new candidate or score; only the route-height audit. Full evidence: `research/acc/optimality/ac-00145_route_peak_audit_20260928.json`.

## 2026-09-28 02:30Z, session 2 (lead): replies to the helpers, and combined exclusions
- **ChatGPT's cap correction is right.** My 00:25 "start above our path's peak" idea was wrong: a
  witness peak doesn't certify that lower caps are exhausted. The live sweep doesn't rely on it.
  Jump-ahead uses only the fact that a cap-C search contains every lower cap, and each run records
  `complete` per cap (= `closed_cap_through`). Probe-and-predict skips only caps it has not claimed.
- **Combined exclusions (exact capped search + Codex corridors):**
  - ac-00145 (record 39): every ≤ 39 path peaks at ≥ 23 (capped, closed through 22), **and** leaves
    the radius-6 union of four known routes (60M states).
  - ac-05064 (record 38): every ≤ 38 path peaks at ≥ 23 (capped), **and** leaves the radius-6 union
    of two routes (51M states).
  Neither is a global shortestness proof. Together they say the record paths are high and far
  from ours.
- **Suggestion for Codex:** start the next corridor from a state of the capped search's last closed
  layer that is *outside* the known-route union, since the record path must pass through one.
- **Pareto labels (ChatGPT):** noted. At 30% more transitions they won't replace the sweep.

# ACC ideas log (both sessions add one idea per turn; newest first)

Format: date/time, session, idea, what was checked, result, next step. Read the other session's
latest entry before starting your turn, and build on it when you can.

## 2026-09-28 02:20Z, session 2 (lead): "the leader controls the family" (team lead's riff)
- **Idea:** in a matrix family, the dominant eigenvalue governs long-run behaviour and the rest is
  noise (a Dunford/Riesz projection pulls it out). Capped BFS layers are powers of the capped
  transfer operator, so after the noisy first layers the growth follows a smooth "leader" curve.
- **Checked (ac-05818, cap 25):** layer growth ×2.4, 2.1, 2.0, 1.9, … 1.34. log(growth) decays
  almost linearly as the capped region fills.
- **Test:** fit that decay on the last 6 layers of a cheap 10M-state probe and extrapolate to depth
  MAXD. Cap 26: predicted 80M, actual 87M (completes). Cap 27: predicted 397M, actual > 196M
  (blows the budget). The prediction is right on both.
- **Change:** `run_capped_sweep.py` now probes each cap first. If the probe finishes, that's the
  answer. If the prediction is above 90% of the budget, the cap is skipped (`SKIPPED_PREDICTED`).
  No more full budget-sized runs that fail at the end. A step-down also always tries the start cap.
- **Also:** conservative matrix fields (Ramanujan Machine group) are path-independent matrix grids
  behind formulas for ζ(3), π and Catalan's constant. They're not used here yet.

## 2026-09-28 02:00Z, session 2 (lead): "Comutators" (the team lead's track, turned into a test)
- **Idea:** the lyric's measure of non-normality is the commutator. Measure how badly r0 and r1 fail
  to commute, and use it to predict the hump before searching.
- **Checked:** 292 verified known AC paths (climb = path peak − start). Cyclic commutator load is
  min over rotations of |[r0, r1]| / (2·start). Tool: `research/acc/optimality/hump_features.py`.
- **Result:** corr(climb, cyclic load) = **+0.36** (plain load +0.20; start length −0.45). The
  least-commuting quarter of rows climbs about 75% higher (7.9 vs 4.5). A linear model (start,
  length, load) reaches R² 0.34 but misses the extreme humps: ac-03305 needs +16 and the model
  predicts +3.6. On 27 of the 45 bounded rows, the proven climb is already above the model.
- **Where it fits:** triage, not caps. Within a value tier, sweep low-load rows first. The
  empirical correlation also goes into the Proof Track draft as an observation, not a theorem.

## 2026-09-28 01:35Z, session 2 (lead): the training roads (user hint)
- **Idea:** `competition/examples/training_424.json` in the official repo holds 424 known
  trivializations of Miller–Schupp MS(n,w) presentations. Every state on those paths has a known
  distance to (x, y), so they're ready-made roads. A scored start near a road state gets
  bridge + rest of the road.
- **Checked:** `research/acc/optimality/road_bridges.py`. It replays all 424 paths with the
  official kernel formulas and hashes every state, plus its relator-and-generator-swap image. Then
  it runs BFS to radius 2 from all 10,115 scored starts.
- **Result:** 4 scored starts sit within 1–2 moves of a road, but the roads are long (27–140) and the
  records are shorter already (ac-08327: 27 vs 17, ac-09594: 33 vs 15, ac-09868: 63 vs 25,
  ac-07667: 140 vs 45). No gain as they stand.
- **Next:**
  1. The scored pool looks like scrambled MS(n,w). If the scored starts are MS(n,w) instances after
     random moves, then identifying (n, w) for each row lets the training path for the same (n, w)
     plus an exact bridge solve it. Test: canonical MS form per row.
  2. Shorten the 4 road paths with window-14 and the capped search from the road states.
- **Proof track:** submissions are published in the SAIR Contributor Network. It isn't in the
  public API (probed 20 paths), and the website is blocked here.

## 2026-09-28 00:40Z, session 2 (lead): jump-ahead caps
- **Observation (38 finished rows):** a cap-C search already contains every lower cap. Climbing
  one cap at a time cost 2–3.5× the final cap's states (ac-03305: 556M total vs 160M for the last
  cap). All hits so far came 1–13 above the start (most within +4): 07435 +1, 05558 +2, 01629 +4,
  03305 +13.
- **Change:** `run_capped_sweep.py` now starts at start + CAP_JUMP and climbs. If that first cap
  runs out of budget, it steps down by 2 until one completes. Jumps: 8 for A (180M), 3 for B (70M,
  deep rows), 5 for C (25M). Expect about 2× the rows per hour.
- **ac-05818:** proved empty only through cap 26 (budget hit at 27, depth 25). The helper's routes
  reach 29, so the capped search can't cover this row. **Helper: keep the corridor/route method
  for rows with deep records (≥ 34).** The capped search is best at depth ≤ 22.
- **ac-09365:** the hit was sac 31, which we already tie. No gain.
- **Next idea:** give each tool the depth it's good at. Capped for records ≤ 31, corridor/route
  merging (helper) for 32–40, and nothing on ≥ 41 until the memory problem is solved.

## 2026-09-28 00:25Z, session 2 (lead), building on the helper's ac-05818 map
- **Helper result:** seven verified 35–36 routes for ac-05818 and a radius-6 corridor search
  (63M states) found no 34-move path.
- **Build-on:** every one of those routes stays at total length ≤ 29 (the start is 25). The record
  34 path (2 teams) probably climbs higher. The exact capped search covers that directly: raise the
  cap from 25 until the budget runs out. **ac-05818 is now first in sweep A (180M budget).**
- **Bridges r = 3:** 21 distinct pairs. The records of each pair differ by no more than the bridge
  length, so there's no gain. Bridges and mirrors are both closed.
- **Helper lines for 01734:** both (ac 36, sac 38) were already accepted from us (sac-01734 38 in
  submission 2558). To avoid repeats, check `research/acc/live/SENT_ROWS.txt` (every row SAIR
  accepted from us, with the live record) before preparing a line.
- **Next idea:** a route's peak total length tells the capped search which cap to use. For each
  row, run the first capped search just above our best path's peak. Everything below that peak is
  already covered by our own path's search.

## 2026-09-28 00:12Z, session 2 (lead)
- **Idea:** near-mirror bridges (built on the mirror idea below): pairs of starts at most r moves
  apart.
- **Checked:** r ≤ 2 across all 10,115 starts (`research/acc/optimality/find_bridges.py`).
- **Result:** one pair, ac-03765 ↔ ac-07258 (2 moves), and both rows are unsolved. No gain yet.
  r = 3 is running on the spare core.
- **Also:** sweep C found ac-07435 26 and sac-07435 28 (ties, k 6). Both are verified and queued
  (2 lines; the batch goes at 3).
- **Next:** if r = 3 also only links unsolved rows, treat each such cluster as one target. Solving any
  one row solves all of them (+1 each). Pick the cluster with the shortest start words and give it the
  big budget.

## 2026-09-28 00:05Z, session 2 (lead)
- **Idea:** mirror transport. If row A is an exact mirror of row B (swap x/y, invert x or y, swap
  the relators), a path for B becomes a path for A at 0–2 extra moves (Stable AC: +2 finish).
- **Checked:** all 10,115 starts under the 15 non-trivial symmetries.
- **Result:** 22 mirror pairs exist, and none gives a shorter path than the live records. The
  leaders already cover them. Dead end.
- **Next (session 2, spare core):** near-mirror bridges. If A's start is within r ≤ 3 moves of
  B's start, then path(A) ≤ r + path(B). Look for rows where record(A) > r + record(B), and for
  unsolved rows next to solved ones (1 point each). One BFS of radius 3 per start, hashed across
  all starts.
- **Question for session 1:** which of your 146 rows finished without a hit, and at what cap? If
  the direct Stable AC paths need caps 12+ above the start, say so and I'll put the big budget
  (180M) on the best ones.

## Standing results worth remembering
- The exact capped search found every tie since 23:30 (sac-03305 +0.5, ac/sac-01629 +0.19,
  ac/sac-05558 +0.06). The beam found none of them.
- Every AC hit also produces its Stable AC line (AC + [16,15]). It's automatic in the sweep.

## 2026-09-28 session 1: is rank 3 behind the short Stable AC records? (checked)
At rank 2 the only 2-move Stable AC finishes are from (x,y) and (y,x) (destabilize needs a relator equal to one
positive generator that appears nowhere else). So an exact rank-2 SAC optimum = min(d(x,y), d(y,x)) + 2.
Exact check (acc_capped, cap 400, fingerprints) on the 9 shortest rows with SAC record <= AC record + 1:
00894, 05911, 03448, 04860 so far all match their SAC record at rank 2 through (y,x) + [15,15].
Result: on short rows the "SAC gap" is the swap finish, not rank 3. Rank 3 is still untested on long rows.
Log: ledger/sac_rank2_probe_20260928.log

## 2026-09-28 session 1: cross-row lookup, radius 2, 467 own paths + 424 SAIR training paths
478 rows got a verified borrowed path, 17 new or shorter than ours, 0 ties. Nearest: ac-00766 34 (record 33,
via ac-03562), ac-00974 26 (record 24, via ac-01077). Exact window shortening on those is running.
Raw: ledger/crossrow_r2_20260928.json

## 2026-09-28 session 1: borrow a road, then shorten the joins (WORKED once)
ac-03028 had no path of ours. crossrow.py found start -> 1 move -> a state on ac-09650's path under mirror 5
(swap x<->y with signs), total 29. Exact window shortening (acc_window, all windows <= 14) cut it to 26 = record
(13 teams). SAC = AC + [16,15] = 28 = record. Official verifier: both accepted. In the inbox.
Why it works: the borrowed road was never tuned for this start, so the joins have slack that windows can remove.
Next: index radius (tools/acc/crossrow.py --iradius N) puts every state N moves off a known road in the index;
row radius 2 + index radius 2 reaches as far as row radius 4, at a fraction of the cost. Running on all rows.
Adam/Bob/Charlie: any new path you find, even a long one, feeds this. Put it in a jsonl with {"id","ac"} and tell us.
Window results on borrowed roads (acc_window, every window <= 14 moves, exact; raw in ledger/crossrow_windowed_20260928.jsonl):
ac-00766 34 -> 34 (record 33), ac-00974 26 -> 26 (record 24), ac-03028 29 -> 26 (TIE), ac-03919 32 -> 30 (record 27).
Bob: 00766/00974 need windows longer than 14 or a different road; short windows are done.

## 2026-09-28 session 1: mirrored roads give free Stable AC ties (WORKED: 13 new SAC ties + ac/sac-03028)
Stable AC can finish from (x,y) with [16,15] or from (y,x) with [15,15]. A mirror that switches x and y turns a road
to (x,y) into a road to (y,x) with no fix moves, so it can beat "AC path + 2". crossrow.py --slive now builds
both and verifies SAC with the official stable kernel. Row radius 2 + index radius 2 over all rows:
498 rows got a borrowed SAC path; 13 were at the live record and never sent (k 6-20). In the inbox.
Raw: ledger/crossrow_r2i2_sac_20260928.json
Next (running): cross-row echo. tools/acc/build_xecho.py puts all 21k road states x 16 mirrors (255k) in an
acc_capped ECHO_FILE so the exact capped BFS can meet another row's road deep in the search, not just 2 moves from
the start. First rows: ac-09989, 03919, 04251, 06903.
Stopped: unk15 beam (helper's 15 unsolved L0 16-18 rows; BEAM_H=1 DIV=1.0 BAL=1, width 200000, depth 600):
8 rows done in 3.5 h, 0 solutions (ac-00008 00066 00137 00254 00392 00045 00095 00164). Incomplete; rows 9-15 not run.
Raw: ledger/beam_unk15_20260928.jsonl

## 2026-09-28 session 1: unsent roads (WORKED: 20 AC ties to inbox, + ac/sac-09989)
Pooled every verified road we hold: repo lines, graph-map archive (60 AC routes), route maps, scratch runs:
677 roads on 496 rows (tools/acc/crossrow.py keeps extra roads per row as "id#n"). Lookup (row r2 + index r2):
20 AC rows where we hold a road at the live record that is not in our accepted history (16 never sent,
3 behind). Lesson: before new search, diff every road we hold against the accepted history.
Borrowed road + exact window also tied ac-09989 (24 -> 23 = record, via ac-01229).
Raw: ledger/crossrow_roads_{ac,sac}_20260928.json

## 2026-09-28 session 1: the board is Miller–Schupp families; the leaders have a 2^n construction (BIG)
- **Families.** 2,937 rows are exact MS(n,w): one relator is y^-(n+1) x^-1 y^n x (written Y^(n+1) X y^n x), n = 1..10,
  the other is a short word w. They hold **1,977 of the 2,672 unsolved rows**. The other 7,178 rows have no MS relator
  in plain form (695 unsolved). Borrowed roads work because rows in a family share one relator exactly.
- **Doubling chains.** For 10 second words w, every n = 3..10 is solved and the record is 2^(n+1) + small:
  w = YXyXyx: 32, 56, 91, 158, 288, 547, 1061, 2088 (= 2^(n+1) + 16, 24, 27, 30, 32, 35, 37, 40).
  **68 of those rows are held by at most 2 teams, most by 1.** A k=1 tie is worth a full point (our AC total is 0.565).
- **Mechanism (from our own n=3 path, ac-09243, 36 moves):** the words collapse to a Baumslag–Solitar relation
  YXXyx (y^-1 x^2 y = x) and y^-1 x^(2^n - 1); the power is built one letter at a time, then peeled one letter per
  move with r1 <- r1·r0. So the path must carry a word of length ~2^n; build + peel = 2^(n+1).
- **Running:** H-beam on the 28 chain rows with n = 4..6 (depth record + 20). If it solves n = 4, 5, the paths
  should show a repeated block; the template prefix + block^(2^n - c) + suffix then gives every n up to 10 directly.
- **Also open:** 106 second words where some n is solved and other n are not, e.g. w = YXYxYx: n=2 solved (24),
  n=3..10 all unsolved. A construction that works there is worth 1 point per row.
- Raw: ledger/ms_families_by_w_20260928.json ({"w|pos": {n: [record, teams, id]}}).
**CORRECTION 06:40Z: INVALID as an echo test.** My acc_capped binary predated ECHO_FILE support and ignored the echo; these are plain capped searches only (still valid as such). Rerunning with a rebuilt binary.
Cross-row echo result (session 1): exact capped BFS meeting 255k mirrored road states, 4 near-miss rows, no meet:
ac-09989 cap 29 complete (35M states), cap 31 incomplete; ac-03919 caps 18/20/22 complete; ac-04251 caps 21/23 complete;
ac-06903 caps 22/24 complete (52M). Scope: first REC-10 moves under the cap, then a road tail. Raw: ledger/xecho_20260928.log
Disk note: a Stable AC probe (ac-01962, cap 400, depth 9) wrote 20 GB of layer files and filled the disk; it was stopped
(incomplete) and the window queue and MS-chain beam died with ENOSPC. Keep a length cap on exact runs.

## 2026-09-28 session 1: what the unsolved rows are
- 2,672 unsolved rows. About 2,190 contain a Miller–Schupp relator (any spelling). The other 481 also repeat a few
  relators: (y^-1 x^-1)^m (yx)^(m-1) shapes appear in 38-50 rows each (m = 4..8), plus short words like YYYXyxyyx.
  These look like Akbulut–Kirby-type presentations (the AK(3) kind from the proof track), i.e. famous open cases.
- Consequence: blind beams on unsolved rows (Adam's lane, my half A: 118 rows, 0 solves) are unlikely to pay.
  The paying lane is the doubling chains, where the leaders have a construction and we can match it.
- Doubling engine arithmetic (MS(n, YXXyx)): in phase B, r1 = x^a Y^2 x^b y and each pair (5,11) maps (a,b) to
  (a-1, b+2), so 2a+b is fixed at 2^n - 1. Phase B only converts; the mass 2^n - 1 is created in phase A.
  Our n=4 path pays for the mass twice (A builds x^7 at ~1 move per x, B spends 2 moves per x converting).
  The leaders' ~2^(n+1) + 1.5n + 8.5 suggests they create the right-hand run directly. Exact n=4 search at caps
  21 (complete, no path <= 49 under cap 21), 23, 24, 25 is running to find it.
MS(4, YXXyx) exact facts (session 1, 05:40Z): see ORDERS_luna_ms.md "Update 05:40Z". Our construction is
~3*2^n; records ~2*2^n; the leaders' n=4 road must exceed total length 23 early. Road cycle: ac/sac-07004 ties (k14).

## 2026-09-28 06:10Z, session 1: MS(3, YXXyx) in 28 (exact, cap 20): the 1-move-per-x build
`5 1 12 2 5 8 3 6 3 6 3 0 12 2 6 8 2 7 5 6 6 2 4 4 4 4 4 4`. The build pairs (3, 6) grow X^2 in r0 per 2 moves;
the conjugation by x cancels a leading X, so there is no rotation cost. Then y = x^7 and y = x^6 collapse to x in one
move, and the peel is 6. Answers session 2's crux for n=3. n=4 needs more leading X's (details in ORDERS_luna_ms.md).
Other exact n=3 results: cap 16 -> 30, cap 18 -> AC none <= 29 (SAC 31), cap 20 -> 28. n=4: cap 21 none <= 49
(complete), cap 23 none <= 46 (depth 37, budget), cap 24 none <= 38 (depth 29, budget).
Echo reruns with the rebuilt binary (valid, 06:55Z):
- Cross-row echo: ac-09989 best 23 (= record, already ours), ac-03919 30 (record 27), ac-04251 38 (record 37), all complete
  at their caps; ac-06903 running. No improvement over existing roads.
- MS(4, YXXyx) build search against our own finish (8,665 echo states from moves 20-55 and radius 3 around 28-36):
  best 55 at caps 21 and 23, complete to depth 31. So no route whose first 30 moves stay <= 23 joins our finish
  region sooner. The leaders' n=4 road differs in the finish too, or climbs above 23 early.

## 2026-09-28 08:55Z, session 1: P2=2 beam on AC records 46-60 (k 1-3): no signal
104 rows (lanes p2c1/p2c2, W=20,000, depth record+2, T9 finish): 0 ties, 1 path (ac-08410 55 vs 46), 103 nopath.
P2's gain looks confined to short hump rows (session 2's <= 45 list). Switched both lanes to depth record+15 so
they produce roads for the cross-row pool (road cycle), not direct ties. Raw: scratch work/p2c*_cap.jsonl.
Also: P2 on made-up MS(4, YXXyx): none within 60 moves (W 20k and 100k); n=3 gives 29 (exact cap-20 path is 28).

## 2026-09-28 09:30Z, session 1: leads from the user's old work (Drive "dicipler downloads")
Read: "00_Mad_Hatters_ACC_Combined_War_Room — full preservation 2026-09-16" and "Idle Wheels, Housings and Light" (Sept 2026).
1. **R_n = (x^2 y x^-1 y, x y^n x^-1 y^-(n+1))**, the old War Room's priority family ("R7 then R6"). On today's board:
   n=2 solved (ac-00104, 21, k10); **n = 3..10: 21 rows, all unsolved by every team** (ac-02842, 06556, 01440, 06388,
   01223, 09596, 02799, 02968, 05297, 06364, 00945, 05233, 06242, 06865, 07712, 01696, 06290, 01834, 04293, 04027,
   04310). Each first solve = 1 AC + 1 SAC point. The old plan: an exponent-substitution eye (detect u^-1 v^a u = v^b)
   and Euclid-style reduction of the (n, n+1) exponent pair. Note: the doubling chains we found today reduce to exactly
   such a relation (BS(1,2): y^-1 x^2 y = x). R_n is an MS family with w = x^2 y x^-1 y, so the same engine may apply
   if w can be turned into a BS relator. Open; worth a helper lane.
2. **External construction lane:** Robby955/ac-square-divisibility (public GitHub, v0.1.0) proves a parametric rank-2
   AC construction for G(p,s) when p | s or p | s+1, with Lean-backed "exact transports" (doubling, pinch, mirror/sign,
   complementary-height, parameter shear) and official-verifier replay. Different family, but its doubling transport is
   the kind of macro the MS chains need. Not yet read here (outside this session's repo scope).
3. **Primitive-relator recipe** (paper Lemma A.1: a normally generating pair with a primitive relator is AC-trivial,
   constructively). Board: 104 rows have a primitive relator (rank-2 test), 0 unsolved, **15 held by one team**:
   ac-00225 51, 01353 57, 01463 46, 02134 61, 02433 73, 03060 28, 03710 58, 04011 46, 05178 62, 05463 50, 05804 48,
   06085 60, 06516 151, 07308 74, 08340 57. The paper's archive mentions 362-move certificates for r1 = x y^m.
   Turning the recipe into letter moves needs conjugation by long words, so its length vs these records is unknown.

## 2026-09-28 10:40Z, session 1: the song ("Same pulse underneath") read against the MS chains
- "Two pitches meet ... count the throb": the 28-move n=3 path already does this. It builds y = x^7 and y = x^6 and
  one move (r0 <- r0·r1) leaves x. The beat replaces a peel.
- "The twin on the far side of the cut": the (y,x) Stable AC finish (13 SAC ties today).
- **"You measure a tick with a tick" -> recursion T(n) = 2·T(n-1) - c.** Evidence: our exact small cases 8, 15, 28
  (n = 1, 2, 3) and the YXXyx chain records 80, 145, 275, 532, 1046, 2071, each = 2 x previous - (15..21).
  That is the signature of "level step + the n-1 solution used twice", not of a single linear build.
- Test: the n=3 28-move recipe applied to MS(4, YXXyx) keeps its shape move for move with one extra y-level.
  After 17 moves it sits at (x^6 YYXyxx, yXYxx) (BS relator intact, doubling-ready). Finish from there: H-beam 39
  (P2 none within 45), total 56. After 21 moves: r0 = x^7 YYXyx. So the recipe transfers, but the finish still costs
  ~2^(n+1); the saving has to come from a recursion that avoids the full-size run. Open for the helpers.

## 2026-09-28 11:00Z, session 1: the 10 doubling chains are one construction ("who stays close when names get stripped?")
Record gap to the YXXyx chain, n = 5..10 (from ledger/ms_families_by_w_20260928.json):
YXyxx 4 5 6 7 8 9 | YXYXyx 10 12 12 14 14 16 | YXyXyx 11 13 13 15 15 17 | YXyxYx 12 15 16 19 20 23 |
YXYxyX 16 19 21 23 25 27 | YYXyxYX 22 25 26 29 30 33 | YYxyXYx 25 28 29 32 33 36 | YYxYXyx 25 29 31 35 37 41 |
YYXYxyX 28 32 35 38 41 44.
The 2^(n+1) part is identical; each chain adds a setup (4-28 moves) plus 1-3 moves per level. So solving
MS(n, YXXyx) at the record for every n unlocks all 10 chains via a per-chain setup. Priority stays: n=4/n=5 of
YXXyx at or near the formula (47 / 80), then the per-chain setups (Luna's lane).

## 2026-09-28 11:40Z, session 1: two more songs ("the name still count", "cross the wall") -> four tests
User's lines and what each became (all on made-up rows MS(n, YXXyx), official kernel):
1. "Look close or look far, I'm the same damn walk" (self-similarity) -> **macro beam**: 110 move blocks (2-8 moves)
   mined from our exact n=1, 2, 3 paths, fed to acc_beam (BEAM_MACROS, H=1, W=50k). n=4: **61** at MACW=0.3
   (vs our 55). Structure: level step `5 1 12 4 1 10 5 12 10`, then the block `5 12 7 5 6 5 13 11` four times,
   then a short finish: a clean repeating unit, but a long one. MACW=1 and n=5 running. Macros: scratch ms_macros.txt.
2. "They put two paths in the dark ... what they saw was the overlap" -> **splice** our two n=4 routes (55 and 56)
   within radius 2 of any state: best 55. No gain.
3. "You can measure the kick, you can't measure the name" / "surface can fail, the deeper count still seen" ->
   the invariant is the count: MS(n, YXXyx) forces y = x^(2^n - 1) whatever the words look like. Proposed (not yet
   built): a beam key that rewards progress toward that count instead of short words.
4. "Perfect symmetry is a quiet cage, keeps you rank-one flat ... rotation lifted the floor" -> **go up a rank**:
   on the chains the Stable AC record is exactly AC + 2 (1 team), so a rank-3 detour that builds the run more cheaply
   would be a Stable AC beat. Exact check on MS(2, YXXyx): rank 2 has no Stable AC path <= 15 (answer 17; complete,
   387 cap-hits noted). Rank 3 at radii 8+7 was killed for memory here (257 moves/state). **Helper ask (Charlie's
   rank-3 lane): run sac_rank3 3 8 8 on "MS2 5 -2 -1 -1 2 1 7 -2 -2 -2 -1 2 2 1" (stdin) on a bigger machine;
   a meet <= 16 means rank 3 beats AC + 2 on this family.**
Note: sac_rank3 reads starts from stdin ("tag l0 w.. l1 w.."), not argv.

## 2026-09-28 12:10Z, session 1: commutator census (helper) checked; family map added to the record page
- Core identity checked: H = S + K (S symmetric, K skew) gives [H, H^T] = -2[S, K] (error ~1e-15 at n = 3, 6, 10).
  It is the identity behind the paper's "non-normality energy = move Dirichlet form". No new search move for ACC; the
  search-side commutator remains the relator load |[r0, r1]| (hump predictor, +0.36). The physics-paper notes
  (K vs A in black hole v2, the commutator in the metric slot, the abelian gauge term) stay with those papers.
- Record page now has a Family map: 48 second words x n = 1..10, each cell = AC record, coloured by unsolved /
  1 team / 2-3 / 4+, outlined where we tie. Data: record/families.json (rebuilt by tools/acc/build_record.py).

## 2026-09-28 12:30Z, session 1: the helper's commutator and mapping result (ledger/codex_commutator_lisitsa_20260928.md)
- The published MS family (Shehper et al. Thm 3, Lisitsa 2024) **is the YXXyx chain** (a = x, b = y^-1, invert and
  rotate). Board rows: ac-01950 n5 (AC 80, SAC 82), ac-02033 n6 (145/147), ac-06796 n7 (275/277), ac-03079 n8
  (532/534), ac-06727 n9 (1046/1048), ac-00106 n10 (2071/2073); **all k = 1 on both boards: 12 full points** if
  matched. Our made-up MS(n, YXXyx) test rows are exactly these rows. Lisitsa's n=9 sequence is 8,634 moves, so the
  leaders' construction is far better than the published one.
- Commutator length |cyc [r0,r1]| is exactly invariant under moves 0-5; only conjugations change it. Use it as an
  endgame trigger (c = 4), not a per-move score. Helper's n=5 generator route: 125 moves (record 80), c rises to 70.
- Macro beam (session 1): n=4 61 at MACW 0.3 and 1; n=5 none within 100.
R_n deep P2 beam (session 1, 12:00Z): all 21 unsolved R_n rows (n = 3..10), BEAM_P2=2 H=1 DIV=0.8, W=20,000, depth 152, T9: no path on any row. Raw: ledger/rn_p2_deep_20260928.jsonl

## 2026-09-28 12:50Z, session 1: Lisitsa archive audit (helper) -> what it changes
- Archived: research/acc/proof_track/ms_lisitsa_ak3_20260928/ (audit note, replay checker, AK(3) P-route replay:
  PASS here, 53 moves; equivalence only). AK3Audit.lean and the Zenodo zip did not arrive (sandbox links).
- Lisitsa's MS(n, w*) routes (= our YXXyx chain) keep the BS relator fixed and the working word short (peak 11-28
  letters even at n = 9), but are long (n=5: 412 incl. finish; n=9: 8,634). So **a long x-run is not required**; it is
  a choice. The records (~2^(n+1)) sit between our x-run routes (~3*2^n) and Lisitsa's low routes (~2^(n+4)).
  Exact n=4 facts still hold: nothing <= 49 stays under total length 21; nothing <= 46 under 23 (depth 37).
- Neighbouring archive files share long tails (MS(9)/MS(8): 4,063 moves), joining at different states: a finite
  merge pattern, not an induction.
- Exact grid d(a,k) from (YXXyx, x^a Y^(k+1) X y^k x): (0,1) = 8, (1,1) = 12; rest running (ak_grid.log).

## 2026-09-28 13:10Z, session 1: "a smaller set of moves that still carry you" -> move-masked exact search
acc_capped now takes MOVE_MASK (bit m = move m allowed in the capped BFS; default all 14; T9 finish unchanged).
MS(3, YXXyx), cap 20:
- mask 0x3C32 (only moves on r1: 1, 4, 5, 10-13; BS relator fixed, Lisitsa-style): 33 moves, 378k states.
- mask 0x11FF (moves 0-8 and 12, the set our 28-path uses): **28 = the optimum**, 1.6M states.
So dropping moves 9, 10, 11, 13 loses nothing at n = 3 and cuts the branching from 14 to 10. Running on n = 4 at caps 25
and 27 (where the full 14-move search runs out of budget), plus r1-only at cap 26 (mask4.log).

## 2026-09-28 13:40Z, session 1: exact d(a,k) grid and masked n=4 results
Exact distance to (x,y) from (YXXyx, x^a Y^(k+1) X y^k x) (cap = start + 8, MAXD 22):
k=1: a=0 8, a=1 12, a=2 17, a=3 21 | k=2: a=0 15, a=1 26, a=2,3 none <= 31 | k=3: a=0 28, a=1 none <= 31.
Each extra x in front of level k costs ~2^(k+1) (k=1: +4.3/x, k=2: +11): an x ahead of level k gets doubled k
times. So a good route never parks x's in front of a deep level; our x^7-before-YY route overpays.
Masked n=4 (MS(4, YXXyx)):
- moves {0-8, 12} (mask 0x11FF), cap 25: **complete**: no path <= 47 whose first 38 moves stay <= 25.
- same mask, cap 27: budget stop at depth 30 (none <= 39).
- r1-only (0x3C32), cap 26: budget stop at depth 45 (none <= 54).
=> the leaders' n=4 road uses moves 9/10/11/13 or climbs above total length 25. Raw: ledger/ms_ak_grid_20260928.log,
ledger/ms4_masked_20260928.log.

## 2026-09-28 13:05Z, session 1: four MS lanes running (no waiting)
1. Full 14-move exact search on MS(4, YXXyx), disk-backed visited table (acc_capped_disk), caps 26 then 28, 250M states.
2. Move-set sweep, n=4 cap 25: the 10-move set {0-8, 12} plus one of 9 / 10 / 11 / 13.
3. **Chain setups (done, negative):** for all 9 other chains at n = 5, no route of <= 13 moves turns w into YXXyx while
   the MS relator stays exactly Y^6 X y^5 x (meet in the middle, cap start + 6). So the chains' extra cost is not a
   simple in-place rewrite of w; the setup works on both relators.
4. Deeper exact grid d(a,k) for (2,2), (3,2), (1,3), MAXD 32.
Also noted: any route through (BS, x^7 YYXyx) costs >= 38 from there (grid, k=1), and our 55 = 17 + 38; the leaders' ~47
cannot pass through that state.
13:30Z results (session 1):
- Move-set sweep n=4 cap 25: +10 (mask 0x15FF) complete, none <= 47; +11 (0x19FF) complete, none <= 47;
  +9 (0x13FF) budget stop at depth 30 (inconclusive); +13 running.
- Deeper grid: d(2,2) = 38 (cap 22); d(3,2) > 41 (cap 23, complete to depth 33); d(1,3) > 41 (cap 23, complete).
  k=2 row: 15, 26, 38 (+11, +12 per x: twice the k=1 rate, as 2^(k+1) predicts). Since MS_4 -> x·MS_3-shape is 3 moves,
  a 47-move n=4 road cannot go through (1,3) under cap 23. Raw: ledger/ms_ak_grid2_20260928.log.

## 2026-09-28 13:55Z, session 1
- Helper priced Lisitsa's archive in SAIR moves (ledger/codex_lisitsa_scored_paths_20260928.json, ..._priced_...md):
  valid but far above records: MS(5) 1,332 vs 80; MS(9) 49,926 vs 1,046. Splices with our n=5-7 routes: no gain.
- Move-set sweep n=4 cap 25, +13 (0x31FF): budget stop at depth 37 (none <= 46); inconclusive.
- New lane "cont": exact continuations from the n=4 states where the n=3 recipe stalls (after 5/7/9/11 moves), caps
  +4/+6, depth 36. Target: <= 36 from move 11 (total <= 47).
- New hunt lanes hunt1/hunt2 (P2=2, W 20k): the user's 21 listed rows (ac-00003 ... ac-00074), one-team rows first:
  ac-00022 45, 00011 48, 00030 76, 00038 179, 00074 208; then k=2: 00052 49, 00041 54, 00057 55, 00016 79, 00031 93,
  00069 101. None had a path of ours before.

## 2026-09-28 14:15Z, session 1: idea cycler (never give up after one approach; always try the opposite)
`tools/acc/idea_cycler.py`: per row, cycles 8 beam ideas, each next to its opposite (greedy length vs hump H vs P2
lookahead; balanced; novelty; noise; 200k wide; deep road record+15) across 4 twins of the row (as-is, relators
swapped, x<->y swapped, letters inverted). Twin paths are mapped back by exact move permutations (derived and checked
on random states) and replayed through the official core before logging. Ledger: scratch work/cyc_hunt.jsonl; no
(row, idea, twin) repeats. Running now on the user's 21 listed rows (lanes cyc1/cyc2; P2 as-is already counted).
First pass (P2, as-is, depth record+2): no path on ac-00022, 00052, 00057, 00016, 00011, 00041, 00030.

Height view of the AC graph (user's note, Bowman-McCaul delta/gamma; Bridson; Lishak): distance, climb height, and the
height needed to return are different coordinates. Our capped exact searches already measure the second one:
"no path <= L under ceiling C" is a lower bound on the ceiling a short route needs. MS(4, YXXyx): a 47-move route
needs ceiling > 21 (complete) and, with moves {0-8,12}/+10/+11, > 25 (complete). Lisitsa's MS(9) route stays at
21-28 letters but is 8,623 moves: low ceiling, long distance. The records sit in between (short, but must climb).
Next test in this frame: find the first ceiling at which MS(3), MS(4) connect to (x,y) within their optimum length.
14:35Z (session 1): standing job queue. `tools/acc/job_runner.sh` starts the next line of work/jobqueue.txt whenever < 4
heavy search processes run and disk > 5 GB. Queue: (1) near misses through the cycler (17 rows at record +1/+2, k <= 3,
led by ac-00975 35/34 k1, ac-05149 34/33 k1, ac-00145 40/39 k1, ac-08995 46/45 k1; started now), (2) MS(3) first-
ceiling test (caps 14-18), (3) 737 one-team rows with records 41-60 that we don't tie, through the cycler.

## 2026-09-28 15:00Z, session 1: Smith-chart reading of paths (rotate = phase, cut = stub), learned from ac-03719
- Charlie's ac-03719 37 is **not a tie**: live record 35 (k1, T00096), SAC 36 (k2). Official verifier accepts both
  paths (37 / 39); plan_offline: +2 / +3. Not inboxed. Charlie's other certified rows match live records.
- Move classes (tools/acc/smith_read.py): ROT = length-preserving conjugation (turn a word in place), CUT = length
  down, CLIMB = length up. ac-03719 37: 19 ROT, 11 CUT, 5 CLIMB, 2 INV; max length never above start (35). Charlie's
  exact run proves nothing <= 36 under cap 35, so the 35 record must climb above the start.
- **Pool profile (716 held paths, 249 at record):** median rotation share 0.29 at record vs 0.38 above record.
  Climb above start at record, by record/start ratio: < 0.9: 14/97 climb (median 0); 0.9-1.1: 28/39 (median 2);
  1.1-1.5: 54/73 (median 2); >= 1.5: 40/40 (median 7, max 16). => exact searches must set cap by this table,
  not at the start length.
- **Rotation compressor** (tools/acc/rotcomp.py): replace each run of pure rotations of r_i between moves that read
  or change r_i by the shortest arc; replayed with the official core. Shortens 29 of 467 above-record held paths by
  2-11 moves (none to record yet). Now a step in every road cycle (work/rotcomp_paths.jsonl feeds the pool).
- Queued at the front: exact capped runs on 9 near-miss rows (k <= 2) at cap = start + predicted climb (+2 more),
  e.g. ac-00975 caps 34/36, ac-05149 31/33, ac-00145 23/25, ac-03719 38/40 (log: ceil_near.log).
14:47Z check-in (session 1): cycler 66 attempts on the user's 21 rows + 17 near misses: no path within record+2 on any
(all 'nopath', every idea tried so far on as-is and twins). Rotation compressor in the road cycle: 44 roads shortened,
pool 1,144 verified roads / 711 rows, no new line. n=4 stall continuations: after 5, 7 moves none <= 36-37 under caps
22-25 (budget stops at depth 27-36); after 9 moves running. Disk n=4 cap 26 still running (1h50m). Climb-then-match on
ac-00975 running.

## 2026-09-28 15:10Z, session 1: rank-2 height profile of MS(n, YXXyx) (the "upside down" measurement)
Shortest AC route whose first <= 60 moves stay under the ceiling (exact capped BFS + T9 finish; all runs complete):
- MS(2), start 12: ceiling 12 -> 17; 13..17 -> 15 (= optimum). Barrier 0.
- MS(3), start 14: 14 -> 34; 15 -> 31; 16-18 -> 30; 19-20 -> 28 (optimum known). Barrier 0; length falls with height.
- MS(4), start 16: **ceilings 16-19: no route at all** (components 32k-3.4M states, exhausted to depth 60);
  ceiling 20 -> 69; 21+ running. **Height barrier for MS(4) = +4 above the start**, and the ~47 record needs > 25.
- Disk-backed full n=4 at cap 26: budget stop at depth 21 (250M states), inconclusive; cap 28 stopped (shallower).
Raw: ledger/ms_height_profile_20260928.log.
15:30Z (session 1): climb-then-match on ac-00975 (756 climbing openings, top 30 seeds x 2 beams): no path <= 34.
Idea cycler gains a 9th idea "two-eyes" (BEAM_DUAL=0.75 set); acc_beam rebuilt from current source.
Helpers' dual lanes resumed here (58 + 58 rows). Reverse-ceiling probe resumed at ceiling 11 with a 6M limit.
15:45Z (session 1): user's second list (25 rows). Already tied by us: ac-00005, 00021, 00064, 00101, 00104. Hunting
the other 20 in cycler lane hunt3 (value order: ac-00013 k1 96; k2: 00130 59, 00091 62, 00010 68, 00111 70, 00113 72,
00069 101; then k3-k11). Pool near misses get ceiling-aware exact runs: ac-00037 32/31 (caps 34, 36), ac-00147 35/34
(caps 24, 26), ac-00123 33/31 (caps 34, 36). Move-9 disk run on MS(4) stopped (incomplete) to free a core; job runner
limit raised to 6 heavy processes so queued exact runs start.
15:50Z check-in (session 1):
- Reverse ceiling probe, **ceiling 11 complete** here: 700,712 states in the identity component (cap-10: 169,992),
  diameter within cap 17, one board row inside (ac-08491, 8). Raw: ledger/reverse_ceiling_11_session1_20260928.log.
  Ceilings 12-13 running (12M limit).
- MS(4, YXXyx) height profile: ceilings 16-19 no route (complete to depth 60); 20 -> 69; 21 -> 65; 22 -> 62.
  Every +1 of ceiling saves 3-4 moves here.
- Dual lanes (resumed helper rows): 8 rows so far, 0 ties (best ac-06990 55 vs 50, ac-06107 53 vs 46).
- Cyclers: near misses (two-eyes on ac-00975 gives 35 again, record 34); hunt3 on the user's second list started at
  ac-00013. Exact near-miss ceiling runs started (ac-00037 cap 34 first).
16:30Z (session 1): reverse ceiling probe complete through 13 (this machine): cap 11: 700,712 states, diameter 17;
cap 12: 1,582,280, diameter 23; cap 13: 6,476,104, diameter 31. Board rows inside, with shortest distance within the
cap vs live record: ac-08491 8/8, ac-07445 15 (cap 12), 13 (cap 13)/13, ac-06500 16/15, ac-09594 18/15,
ac-04359 19/17, ac-08327 19/17. All already tied by us; every record beats the in-cap distance, i.e. records climb
above 13 (same height-for-length trade as MS(4): ceilings 20/21/22 give 69/65/62). Raw: ledger/reverse_ceiling_*.
MS(4) height profile finished (HEIGHT_DONE). Paused cyc1/cyc2 cyclers restarted on the freed cores.
16:50Z (session 1): the container restarted during the user's usage-limit pause (between 16:12Z and 16:34Z); all
background lanes except two just-restarted cyclers were lost. Relaunched via new `tools/acc/restart_all.sh` (every
lane under its own flock; rerunning it does not duplicate). All lanes resume from their ledgers (cycler: per
(row, idea, twin); dual/beam runner: per row). Nothing in progress was committed as a result, so nothing to redo.

## 2026-09-28 17:30Z, Fable (helper): MS(n, YXXyx) — a counting bound that rules out the literal-run road, and what it forces
Official kernel a0fd6e6, made-up rows MS(n, YXXyx). All exact runs below complete unless marked.
1. **Separator fact (proved by cases, all 10 rotations of BS^±1).** A "cell" = one application of the BS relation = a
   multiplication of the worked relator by the other relator while that one is a BS rotation. Two consecutive cells on
   the same relator with the other fixed are impossible (the second multiplication is the same or the inverse of the
   first: BS rotations are cyclically reduced). Cells cannot alternate between r0 and r1 either (both would have to be BS
   rotations at once). So every cell after the first costs >= 1 extra move (a conjugation, an inversion, or a
   non-cell multiplication). Build cost >= 2*cells - 1.
2. **Area fact.** Weighted mass t = sum over x-letters of ±2^h (h = y-height to the left) is invariant under cells;
   MS_n has one x at height -1 and one X at height -(n+1); any literal-run word in its class needs the x pushed down
   n levels: 2^n - 1 cells, and the run has 2^n - 1 letters. Peel from (x, y X^(m-1)) is m-1 moves (type-A/B states
   force |a-b| = 1, checked: (xx,yX^5), (xxx,yX^7), (x^4,yX^7) have no route <= 16).
3. **Consequence.** Any road that passes through (BS-rotation, literal y = x^(2^n - 1)) or its mates costs
   >= 2(2^n - 1) - 1 + (2^n - 2) + ~5 = 3*2^n - O(1): n=4: 48, n=5: 96 > record 80. **The leaders' road for n >= 5
   never contains a literal run of length 2^n next to a BS relator.** Our 55 (x^7 fuel -> x^15 -> peel) and Lisitsa's
   routes are both literal-run roads; that is the phase to skip. The records 2^(n+1) + 1.5n + 8.5 are consistent with
   two structures only: (a) area ~2^(n-1) at 2 moves/cell + a 2^n-move finish, or (b) both relators long and pure
   (x^A Y^k, x^B Y^j) with a fast Euclid finish (unit cost per subtraction; e.g. (15,4),(11,3) finishes in 5). The
   collapse config (x^m Y x^(m-1) Y, x^(m-1) Y) [y^2 = x^(2m-1), y = x^(m-1)], m = 2^(n-1), has finish m+3 (half peel)
   and is one multiplication from the level-(n-1) mates. Recursion to test next: MS_n -> level-(n-1) mates in
   2^n + O(1) moves (records give T(n) - T(n-1) = 2^n + 1 or 2 exactly).
4. **Negatives (exact, this session).** From the level-step state (BS, x^3 YYYXyyx): no route with <= 4 non-mult
   moves reaches any (BS-rot, run >= 13) state within 16 moves under cap 22; <= 6 non-mults, cap 24: none within 16
   (frontier dies at depth 15). From MS_4 with <= 7 non-mults, cap 24: no (BS-rot, |mass| >= 12) state within 30
   (frontier dies at 17). Exact hops: MS_4 -> (BS, xYYYYXyyyx) = 3 [5 12 10]; -> (BS, xxxYYYXyyx) 7 more
   [5 11 5 12 10 10 10] under cap 22; (BS, xxxYYYXyyx) -> (BS, x^7 YYXyx): none <= 10 at cap 24; MS_4 -> x^7YYXyx:
   none <= 13 at caps 22 and 24 (the ledger's 13 must be a different rotation). Naive transfer of path(n-1) to MS_n
   explodes (peaks 50-143): the passenger idea is dead in that form.
5. Scripts: scratch only (ms.py replay with affine readout, multbfs.py/massbfs.py bounded-non-mult BFS); nothing
   committed to tools/.
17:52Z check-in (session 1): restart_all found every lane alive. No ties.
- Dual lanes (resumed helper rows): 57 rows, 0 ties; closest ac-01078 45/43, ac-02142 45/42, ac-06990 55/50.
- Cyclers (285+ attempts): near misses ac-00145 best 40 (record 39), ac-08995 47 (45); ac-00022 64 (45); rest nopath.
- Exact ceiling runs: ac-00147 cap 24 (start 16) complete: shortest 37 (record 34), so the record climbs above 24;
  ac-00037 cap 34 budget stop at depth 23 (inconclusive); cap 36 running. Raw: ledger/ceil_near_20260928.log.

## 2026-09-28 19:00Z, session 1: "what did we miss" review
1. **Stale board in session 1's targeting:** live_all_ac/sac.txt dated from 04:13Z; 856 AC and 867 Stable records
   have dropped since. No wrong line was sent (plan_offline reads fresh data), but target lists were stale. Fixed:
   `refresh_live.py` rebuilds both from the newest boards/*.json.gz at the start of every road cycle.
2. **Stable-AC gap rows:** 9 rows where we tie AC but not Stable AC; on 8 the Stable record is AC + 1, reachable only
   via the (y,x) finish, which the cyclers never score. Two are one-team (sac-08078 34, sac-02528 36). Split with
   Charlie (ORDERS_charlie_v2_20260928.md): session 1 low caps in memory, Charlie cap >= start+4 on disk.
3. **First solves:** 100 unsolved MS rows sit next to a solved n-1 row in the same family, and we hold a path for the
   solved neighbour on nearly all. New lane `firstsolve.py`: replay the n-1 path on the n row, pick the shortest prefix
   states, deep beams (depth 250) from there; plain deep beam as the control. Any length is a full point on each board.
4. Checked and clean: Stable lines from held AC paths (0 new); Charlie's 540 cutchain lines (0 scoring).
5. Job queue was starved (6 heavy lanes always running); cyc1/cyc2 (user's first list, 400 attempts, nothing within
   record+2) stopped and removed from restart_all so the gap runs and first-solve lane can start.
18:55Z check-in (session 1): **ac-04191 47 and sac-04191 49 TIE (k4 each)** from the resumed helper dual lane B
(two-eyes beam, T9 finish); official verifier accepted, plan_offline TIE on both; our old lines were 115 / 119.
Inboxed. Dual lanes: A 38 rows (0 ties), B 39 rows (1 tie). sac-02528 cap 31 (started before the dequeue): budget
stop at depth 24, no Stable path <= 36. sac-08078 cap 33 running. restart_all: all 6 lanes alive.
19:58Z check-in (session 1): all lanes alive. Dual lanes (resumed helper rows) 49/50 rows done: 1 tie (ac/sac-04191,
sent in 2694), 12 above, rest nopath. First solves: ac-02842, ac-03989 no path (replay + depth-250 beams).
sac-08078 exact cap 33 still running. Road cycle: 782 rows with a verified borrowed path, 0 new lines.
Family transfer (254 family-lane rows) retuned to ~10 min/row (two-eyes + H, start + best transfer seed, 150 s beams)
and split into two shards.

## 2026-09-28 20:10Z, session3: MCSC families YYXYYXyyx / YYXYYxyyX, pulse opening and first paths
- **Pulse opening, MS(n, YYXYYXyyx):** `6 10 12` + `9`×(n−3) + `3 9 7 3 6 12 4` (n+9 moves) sends every n to
  r0 = Y^(n−2) x y^(n−1) XYX, **r1 = yyxYYXYX (fixed for all n)**. Checked by replay n = 5..10 (peak 4n+6).
  Found by comparing beam paths for n=5 and n=6: they differ by one extra move 9. All n-dependence then sits in r0.
- Verified paths (official core, not at record): ac-07790 59 (rec 40), ac-09762 78 (rec 44), ac-06005 67 (rec 41).
  Moves in exchange/session3/mcsc_family_paths_20260928.json. Found by layered beam (W=20000, per-relator cap 22,
  best W states per move number) + exact (x,y) finish.
- Other opening: `8 8 12 12` + `5 12 12` rounds shrinks r1 of YYXYYXyyx one letter per round; clean at odd n, leaves
  xYX at even n (parity again). Does nothing on YYXYYxyyX or YYXyyXyyx.
- Negatives (exact scope): (1) greedy best-first (gsc, per-relator cap 14–22) always returns 132 at n=5: short routes
  climb (session 1's 52-path peaks at total 31). (2) Tube shortening of the 132 path, radius ≤ 4, per-relator cap
  ≤ 18: stalls at 97 (different valley). (3) No step of ≤ 14 moves between exact level shapes k=4 → k=3 of the
  pulse family (two-sided BFS depth 7+7, per-relator cap 26, complete within those bounds). (4) A bridge from the
  n=6 opening into a radius-3 tube of the n=5 path exists (repeating block `7 9 2 0` ×5) but totals 86 > 78.

## 2026-09-28 Codex: exact short-endpoint distances through six letters

- Complete candidate scope: all 1,768 ordered, freely reduced relator pairs of total length ≤6 with abelianization determinant ±1; 14 SAIR ac-r2-v1 moves. They exactly equal the capped-length-6 component of (x,y), proving every such endpoint is AC-trivial.
- Exact **unrestricted** maximum shortest moves for endpoint length ≤2,3,4,5,6: **5,5,6,7,8**. Upper bounds by complete length-6 BFS; lower bounds by disjoint *uncapped* balls around (x,y) and witnesses (y,x), (Y,YYx), (Y,YYYx), (Y,YYYYx), respectively. This is a finite endpoint result, not a general bound.
- Reproduce: `research/acc/optimality/reverse_small_presentations.py`; full proof scope, counts, paths, hashes, and pinned verifier 24,752-transition cross-check in `research/acc/live/ledger/reverse_small_endpoints_20260928.md`. No challenge rows run or submitted for this result.

## 2026-09-28 20:30Z session 2: stabilization census, P2 cache size, mirror twin payoff
- **Real stabilization is rare on the board.** Board 18:56Z, SAC record minus AC record over all rows: +2 on 6,540,
  +1 on 660 (the (y,x) finish), +3 on 44, and <= 0 on only 108 (mostly long rows held by 1 team, e.g. ac-03395 317 / 308).
  So stabilization moves (ids 14-256) are not where Stable-AC points are; the +1 rows are, and the yx lanes cover them.
- **P2 cache size is not the bottleneck.** acc_beam two-eyes at W=20000 on ac-06262: 2.34M P2 calls, 72% cache hits with
  2^18 slots, 75% with 2^22; identical output, 4% faster. Misses are first-time pairs; P2 eval is ~70% of beam time.
- **Mirror twin + two eyes hit on the first row.** Codex's first mirror-twin row, ac-05818: 34 (tie, k2, + SAC 36), submission 2701.
  Our best stored path was 36 (plain P2 beam, p2b; 52 was only our last *sent* line), and this row had no two-eyes run, so
  the 36 -> 34 gain is mirror and DUAL together, not the mirror alone. Session 2 started lane `mir` (120 top-ranked rows we
  are above, not in Codex's 80) and will compare mirror vs plain two-eyes on rows both lanes run.

20:40Z (session 1): family transfer (neighbour replay, record+2) on 20 family-lane rows: 3 paths, 0 within +2 of
record (e.g. ac-01553 49/43, ac-01974 52/42). Opposite approach now: the same lane at depth record+15 (FAM_EXTRA=15,
work/family_deep.jsonl) so long roads feed the pool, where rotation compression, cross-row borrowing and the window
queue shorten them. First solves: 6 rows, no path yet. sac-08078 cap 33 still running (in memory).

20:45Z (session 2): **solo-held long rows are out of our beam's reach (negative).** Board 20:23Z has ~3,300 rows whose AC
record (>= 50) is held by one team (1,139 at 50-74, 766 at 75-99, 408 at 100-124, ...); we hold a path on almost none.
Probe: two-eyes beam, W=2000, DMAX = record + 2, on 12 random such rows (records 55-85): 0/12 found any path. Opposite
check on ac-01262 (record 55): W=20000, DMAX=160, no depth ceiling: **no path at all** (frontier lengths 21-149 at
d=160, 556 s in P2). So these records come from methods our beam lacks (family constructions / Nielsen-edge search per
RIVAL_METHODS_FULL). The reachable pool is the solo rows at 42-49 never tried (141): 42 in session 2 lane `solo`
(W=4000 screen), 75 to Astra, the rest in Luna's list and session 2's queues.

20:55Z (Codex, mirror twin): assigned 80-row AC mirror list, BEAM_H=1 BEAM_DIV=.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=.75, W=20k, DMAX=each AC record, T8. First 3 complete: ac-05818 AC34 officially verified, already accepted by us per SENT_ROWS (also SAC36), so no duplicate; ac-04586 AC41 vs39; ac-02304 nopath through depth44. Run continues on ac-06969. Raw first-three ledger: sweeps/codex_mirror_20260928T2015Z.jsonl. Earlier C16 full reverse graph and bounded negative splices: ledger/CODEX_C16_REVERSE_20260928.md. No new score from these three.
21:00Z check-in (session 1): all lanes alive. Deep family lane: 15 rows with roads (41-65 vs records 41-43), no tie;
roads feed the pool. First solves: 8 rows, none. sac-08078 exact cap 33 still running. Dual lane A 51/58 rows.
Road cycle: 782 rows with borrowed paths, no new line. Team: Codex back on a mirror-twin lane (inbox ac-05818,
ac-04718); new helper Astra on rk2 bottom-up; Sonnet onboarded 20:50Z (no progress line yet).
Note: ac-05818 was also in session 1's near-miss cycler list; Codex's inbox line supersedes it.

21:11Z (Codex, user's Snell/Smith chart): five-path chart suggests slow length 20-24. Controlled ac-00975 W20k dual P2+C16 A/B changing only H tie-break at L20-24: +20 penalty AC35/SAC37 (identical baseline); -20 reward AC43/SAC45 (worse); all official replay clean, no score. Smith/Cayley radius of exponent matrix M (reflect det<0) on 9 saved paths, 326 steps: chosen-move top3 24.5% overall vs raw length39.3%, on 43 climbs Smith20.9% vs raw length0%. Too small and biased to adopt. Exact scope and source: ledger/CODEX_SNELL_SMITH_PILOT_20260928.md and optimality/experiments/. Mirror assignment continues separately.

## 2026-09-28 21:25Z, session3: three eyes alone, then mixed in Mixer 5.2 beside the known eyes
- New eyes, each built alone and scalable (pooled, re-learned from all recordings): SNELL (medium speed at the
  current total length), PLANAR (pooled height = fewest known moves to trivial, radius-2 lookup; Mazur X), SMITH
  abelian (ledger on the Poincare disk), SMITH per line (rho: x->[[0,-1],[1,1]], y->XZ into SL2(Z); hyperbolic
  distance of r0 from x and r1 from y; sees word order). 12 recordings x 20 channels, Mixer 5.2 import checked.
  Files: exchange/session3/master_mixer_studies_v1/.
- Tracking true progress (Spearman vs pooled height, pooled / median within path): length +0.72/+0.90, SMITH per line
  +0.59/+0.76 and +0.55/+0.74, image distance +0.46/+0.56, Snell +0.29/+0.41, SMITH abelian +0.07 (blind).
- Planar splice (jump onto the lowest known route within radius 2): ac-09762 78 -> 76 (official ok; record 44).
- Negatives: Snell-keyed beam (lam 1: 57, lam 2: none) and Bob's 30 macros (58 = plain 58, W=8000) do not beat the
  plain layered beam (56) on ac-07790. Cross-row progress regression fails (held-out error ~33 moves).
- MS(5, YYXXYx) unsolved descent 19 -> 15: per-line Smith shows r1 closing 7.2 -> 1.8 while r0 stays 1.8 -> 1.9.

## 2026-09-28 21:55Z, session3: eye table for all 10,115 rows; faithful Smith eye; YYXXYx descents
- exchange/session3/unsolved_data_v1/eye_table_all_rows.csv: every eye at every row's start state, with record/teams.
- Unsolved rows start shorter (median 24 vs 29). Separators (AUC for unsolved): faithful Smith r1 (Sanov) 0.12,
  i.e. 0.88 inverted, the best single eye; Smith abelian 0.18; longest run in r1 0.76; image distance 0.47 (none).
- The order-6 rho used for per-line Smith has blind spots (both lines 0 at total 17 on MS(5,YYXXYx), not solved).
  Sanov (x->[[1,2],[0,1]], y->[[1,0],[2,1]]) is faithful on F2: distance 0 iff the relator equals x (or y).
- Record model trained on solved rows: held-out Spearman 0.42 (median error 20 moves). Its "easiest" unsolved rows
  are BS-type pairs (ac-05932 etc., session 1's list) and AK(3)-class rows: shortness is not easiness here.
- MS(n, YYXXYx) recorded descents n=4..10 (beam W=8000, depth 80): odd n drop by 2, even n none (parity again).
