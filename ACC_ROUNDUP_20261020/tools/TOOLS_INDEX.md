# ACC tools index (auto-built from each file's header, 20 Oct 2026)

557 tools (third-party libraries and copied handoff bundles left out). `tools/acc/sair_api.py` is the SAIR client (uses the API key) and is NOT included in any share copy.


## SCRATCH(this session)/acc/acc_synthesis

- `SCRATCH(this session)/acc/acc_synthesis/__init__.py` — ACC Memory-First Harness: orchestration, not a search solver.
- `SCRATCH(this session)/acc/acc_synthesis/demo.py` — Exercise the complete controller with labelled toy workers and checker.
- `SCRATCH(this session)/acc/acc_synthesis/gates.py` — Exact-artifact gates for an externally supplied, pinned ACC checker.
- `SCRATCH(this session)/acc/acc_synthesis/geometry.py` — Optional finite matrix diagnostics. These never certify or prune ACC states.
- `SCRATCH(this session)/acc/acc_synthesis/harness.py` — Offline agent orchestration. Commands are configured clients, never model output.
- `SCRATCH(this session)/acc/acc_synthesis/runtime.py` — Small durable task kernel and bounded JSON subprocess transport.
- `SCRATCH(this session)/acc/acc_synthesis/selftest.py` — Run local fault tests. These do not call a model or validate real ACC routes.
- `SCRATCH(this session)/acc/acc_synthesis/tests/test_gates.py` — Gate integration tests using a TOY receipt producer, NOT an ACC checker.
- `SCRATCH(this session)/acc/acc_synthesis/tests/test_geometry.py` — (no header)
- `SCRATCH(this session)/acc/acc_synthesis/tests/test_runtime.py` — Kernel regressions: durable evidence, fencing, stop, and bounded execution.
- `SCRATCH(this session)/acc/acc_synthesis/tests/test_workflow.py` — (no header)
- `SCRATCH(this session)/acc/acc_synthesis/workers/demo_checker.py` — TOY CHECKER ONLY. One defined string transformation; not an ACC checker.
- `SCRATCH(this session)/acc/acc_synthesis/workers/demo_worker.py` — DEMONSTRATION ONLY. Deterministic role responses; no language model is called.
- `SCRATCH(this session)/acc/acc_synthesis/workers/example_bridge.py` — JSON-lines boundary example, intentionally no invented model API bindings.

## SCRATCH(this session)/acsx_run/worker.sh

- `SCRATCH(this session)/acsx_run/worker.sh` — Claims 20-key chunks of data/unsolvedM.txt (atomic mkdir) and runs the 610model beam search on each; resumable.

## SCRATCH(this session)/acsx_venv/lib


## SCRATCH(this session)/allsubs.py

- `SCRATCH(this session)/allsubs.py` — (no header)

## SCRATCH(this session)/astra_audit.py

- `SCRATCH(this session)/astra_audit.py` — (no header)

## SCRATCH(this session)/build_roads.py

- `SCRATCH(this session)/build_roads.py` — (no header)

## SCRATCH(this session)/c16pack/acc_c16.c

- `SCRATCH(this session)/c16pack/acc_c16.c` — acc_c16: ceiling finish table ("C16"). BFS from (x,y) over the states of total relator length <= CEIL (default 16), moving only through such states, layer by layer until closure (or a state/time budget), storing each sta

## SCRATCH(this session)/c16pack/acc_opt.c

- `SCRATCH(this session)/c16pack/acc_opt.c` — ACC exact-optimality meet engine, ac-r2-v1 (SAIR Andrews-Curtis commit a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e, competition/tools/verifier/core.py, 14 moves). NO LENGTH CAP. Letters: 0=x 1=x^-1 2=y 3=y^-1 (inverse = c^1

## SCRATCH(this session)/c16pack/c16_table.inc

- `SCRATCH(this session)/c16pack/c16_table.inc` — ---- ceiling finish table ("C16"), shared by acc_c16.c (builder) and acc_beam.c (BEAM_C16) ---- Contents: every state reachable from (x,y) through states of total relator length <= CEIL, with its BFS distance inside that

## SCRATCH(this session)/cats.py

- `SCRATCH(this session)/cats.py` — (no header)

## SCRATCH(this session)/chk.py

- `SCRATCH(this session)/chk.py` — (no header)

## SCRATCH(this session)/claims/descend.py

- `SCRATCH(this session)/claims/descend.py` — Iterated mid-road restarts on claimed rows. A pass beams from every state s_c of the current best road with depth = best - 1 - c; the shortest strict improvement found is adopted, verified on the official core, and the n

## SCRATCH(this session)/claims/descend2.py

- `SCRATCH(this session)/claims/descend2.py` — Iterated mid-road restarts, v2. Row spec CID:AC_TARGET:MODE[:CUTHI[:LINK]] MODE xy = beam aims at (x,y) (AC tails, plus the beam's own SAC tails); yx = beam on the letter-swapped state, so the search aims at (y,x): Stabl

## SCRATCH(this session)/claims/peephole.py

- `SCRATCH(this session)/claims/peephole.py` — Peephole shortener for AC roads: radius-R balls around every state of the road, meet in the middle, replace any segment s_i..s_j by a shorter connection; repeat to a fixpoint. Every result replays on the official core. u

## SCRATCH(this session)/claims/reorder_tube.py

- `SCRATCH(this session)/claims/reorder_tube.py` — Bob/Cass method on our rows: many same-length reorderings of a road (swap neighbouring moves only where both orders reach the identical state), then one BFS inside the tube = all states within radius R of any reordered r

## SCRATCH(this session)/claims/tiewatch.sh

- `SCRATCH(this session)/claims/tiewatch.sh` — exits only when a claimed row reaches its record (tie or beat) on either board, or the driver stops

## SCRATCH(this session)/cov/transfer.py

- `SCRATCH(this session)/cov/transfer.py` — Change-of-variables (automorphism) transfer web. For rows A, B whose starts have the same Whitehead-minimal form (up to the 8 letter maps, relator swap, cyclic rotation and inversion), B ~ psi(A) for an automorphism psi 

## SCRATCH(this session)/cov/whitehead.py

- `SCRATCH(this session)/cov/whitehead.py` — Whitehead-minimal forms of every SAIR row start (rank 2), to find rows related by a change of variables (automorphism). Words are strings over xXyY. Type-2 Whitehead automorphisms for multiplier a in {x,X,y,Y}: the other

## SCRATCH(this session)/coverage_run.py

- `SCRATCH(this session)/coverage_run.py` — Mad Hatters ACC coverage run (UPG-H, 6 Oct): first team roads AT the record on rows held by a single team where we have no accepted line. Beam (W 100k) + exact finish table T8 + exact window shortening + Stable via (y,x)

## SCRATCH(this session)/dbl/run_ff.sh

- `SCRATCH(this session)/dbl/run_ff.sh` — (no header)

## SCRATCH(this session)/dbl/run_fin.sh

- `SCRATCH(this session)/dbl/run_fin.sh` — (no header)

## SCRATCH(this session)/dbl/run_junction.sh

- `SCRATCH(this session)/dbl/run_junction.sh` — (no header)

## SCRATCH(this session)/dbl/run_n3.sh

- `SCRATCH(this session)/dbl/run_n3.sh` — (no header)

## SCRATCH(this session)/edit_ra.py

- `SCRATCH(this session)/edit_ra.py` — (no header)

## SCRATCH(this session)/ext/acsolver


## SCRATCH(this session)/fable/beam_runner.sh

- `SCRATCH(this session)/fable/beam_runner.sh` — Bounded any-road beams: one core, <=240 s each, sequential. Output: beam_<row>.out

## SCRATCH(this session)/fable/bsdetect.py

- `SCRATCH(this session)/fable/bsdetect.py` — Detect: relator r_i equals (cyclically, up to inversion) a b a^-1 b^-2 for signed generators a,b (a in {x,X,y,Y}, b in {x,X,y,Y}, b != a^±1)

## SCRATCH(this session)/fable/fam.py

- `SCRATCH(this session)/fable/fam.py` — 1) MS families for MS-shape rows (identity automorphism only, plus y-sign flip which keeps the MS relator form)

## SCRATCH(this session)/fable/ms_match.py

- `SCRATCH(this session)/fable/ms_match.py` — (no header)

## SCRATCH(this session)/fable/replay.py

- `SCRATCH(this session)/fable/replay.py` — (no header)

## SCRATCH(this session)/fable/rowstruct.py

- `SCRATCH(this session)/fable/rowstruct.py` — (no header)

## SCRATCH(this session)/fable_zoom/census.py

- `SCRATCH(this session)/fable_zoom/census.py` — Q1: where are the points. Latest boards + our best (ledger) + held (history).

## SCRATCH(this session)/fable_zoom/families.py

- `SCRATCH(this session)/fable_zoom/families.py` — Q3: structure of all 10,115 starts, joined with the board and our ledger.

## SCRATCH(this session)/fable_zoom/families2.py

- `SCRATCH(this session)/fable_zoom/families2.py` — (no header)

## SCRATCH(this session)/fable_zoom/moves.py

- `SCRATCH(this session)/fable_zoom/moves.py` — Q2: what moves on the board. All snapshots -> per-row event list (time, record, k) on change.

## SCRATCH(this session)/fable_zoom/moves_analysis.py

- `SCRATCH(this session)/fable_zoom/moves_analysis.py` — (no header)

## SCRATCH(this session)/fable_zoom/ours.py

- `SCRATCH(this session)/fable_zoom/ours.py` — Q4: our own pattern from the ledger: which sources produced our best paths, task methods/outcomes, heat, parked rows.

## SCRATCH(this session)/fable_zoom/prefix_law.py

- `SCRATCH(this session)/fable_zoom/prefix_law.py` — (no header)

## SCRATCH(this session)/fable_zoom/probe_state.py

- `SCRATCH(this session)/fable_zoom/probe_state.py` — (no header)

## SCRATCH(this session)/fin/climb.sh

- `SCRATCH(this session)/fin/climb.sh` — (no header)

## SCRATCH(this session)/fin/cyc_level.py

- `SCRATCH(this session)/fin/cyc_level.py` — One-sided BFS from a loop level's start: fewest moves to reach the level END state up to cyclic rotation/inversion of each relator (any conjugate, either order). If < canonical, rotations can be deferred (paid once, at t

## SCRATCH(this session)/fin/fin_beam.sh

- `SCRATCH(this session)/fin/fin_beam.sh` — finish probe: beam from the BS-doubling pre-finish state P_m = (Y x^m y y X, x x Y X y) to (x,y)

## SCRATCH(this session)/fin/level_cap.py

- `SCRATCH(this session)/fin/level_cap.py` — Does relaxing the length cap shorten one level of the canonical BS-doubling loop? (n=5, segments between level boundaries)

## SCRATCH(this session)/five_reads.py

- `SCRATCH(this session)/five_reads.py` — (no header)

## SCRATCH(this session)/grok/mini_ac.py

- `SCRATCH(this session)/grok/mini_ac.py` — Reference replay of the 14 SAIR AC moves (ac-r2-v1) for self-checks. The official SAIR verifier is still the judge: Mad Hatters replays every route on it before anything is sent. Words: strings over x, X (= x^-1), y, Y (

## SCRATCH(this session)/haiku_trial/check_accepted.py

- `SCRATCH(this session)/haiku_trial/check_accepted.py` — usr/bin/env python3 Read history

## SCRATCH(this session)/haiku_trial/gather_candidates.py

- `SCRATCH(this session)/haiku_trial/gather_candidates.py` — usr/bin/env python3

## SCRATCH(this session)/handoff_bob_cass/tools

- `SCRATCH(this session)/handoff_bob_cass/tools/cov_transfer.py` — Change-of-variables (automorphism) transfer web. For rows A, B whose starts have the same Whitehead-minimal form (up to the 8 letter maps, relator swap, cyclic rotation and inversion), B ~ psi(A) for an automorphism psi 
- `SCRATCH(this session)/handoff_bob_cass/tools/crossroad_join.py` — Join roads that pass through the same exact state (same row or different rows): for row A with road P and any verified road Q (of any row) that visits state s_i(P) at position j, P[:i] + Q[j:] is a road for A. Keeps the 
- `SCRATCH(this session)/handoff_bob_cass/tools/descend2.py` — Iterated mid-road restarts, v2. Row spec CID:AC_TARGET:MODE[:CUTHI[:LINK]] MODE xy = beam aims at (x,y) (AC tails, plus the beam's own SAC tails); yx = beam on the letter-swapped state, so the search aims at (y,x): Stabl
- `SCRATCH(this session)/handoff_bob_cass/tools/peephole.py` — Peephole shortener for AC roads: radius-R balls around every state of the road, meet in the middle, replace any segment s_i..s_j by a shorter connection; repeat to a fixpoint. Every result replays on the official core. u
- `SCRATCH(this session)/handoff_bob_cass/tools/reorder_tube.py` — Bob/Cass method on our rows: many same-length reorderings of a road (swap neighbouring moves only where both orders reach the identical state), then one BFS inside the tube = all states within radius R of any reordered r
- `SCRATCH(this session)/handoff_bob_cass/tools/whitehead_min.py` — usage: python3 tools/acc/upgh/whitehead_min.py OUT.json Whitehead-minimal forms of every SAIR row start (rank 2), to find rows related by a change of variables (automorphism). Words are strings over xXyY. Type-2 Whitehea

## SCRATCH(this session)/handoff_x/bob


## SCRATCH(this session)/handoff_x/charlie


## SCRATCH(this session)/handoff_x/kernel


## SCRATCH(this session)/kt2/kit

- `SCRATCH(this session)/kt2/kit/acc_opt.c` — ACC exact-optimality meet engine, ac-r2-v1 (SAIR Andrews-Curtis commit a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e, competition/tools/verifier/core.py, 14 moves). NO LENGTH CAP. Letters: 0=x 1=x^-1 2=y 3=y^-1 (inverse = c^1
- `SCRATCH(this session)/kt2/kit/acc_window.c` — ACC exact window shortening, ac-r2-v1 (Colab kit copy: ACC_ANY_END allows road pieces; end state kept fixed) Original: (SAIR a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e). Kernel, fingerprint and table are shared verbatim wi
- `SCRATCH(this session)/kt2/kit/commute_clean.py` — Commuting-pair cleanup (UPG-H song-4 rule, own implementation): a move m and a later inverse(m) cancel when every move between them commutes with m (neither writes a relator the other reads or writes). Repeats until no p
- `SCRATCH(this session)/kt2/kit/run_longrows.py` — Long-row shortener for Colab or the owner's PC (no model, no API, no repo pull).

## SCRATCH(this session)/kt4/kit

- `SCRATCH(this session)/kt4/kit/acc_opt.c` — ACC exact-optimality meet engine, ac-r2-v1 (SAIR Andrews-Curtis commit a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e, competition/tools/verifier/core.py, 14 moves). NO LENGTH CAP. Letters: 0=x 1=x^-1 2=y 3=y^-1 (inverse = c^1
- `SCRATCH(this session)/kt4/kit/acc_window.c` — ACC exact window shortening, ac-r2-v1 (Colab kit copy: ACC_ANY_END allows road pieces; end state kept fixed) Original: (SAIR a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e). Kernel, fingerprint and table are shared verbatim wi
- `SCRATCH(this session)/kt4/kit/commute_clean.py` — Commuting-pair cleanup (UPG-H song-4 rule, own implementation): a move m and a later inverse(m) cancel when every move between them commutes with m (neither writes a relator the other reads or writes). Repeats until no p
- `SCRATCH(this session)/kt4/kit/run_longrows.py` — Long-row shortener for Colab or the owner's PC (no model, no API, no repo pull).

## SCRATCH(this session)/ladder/descend_ladder.py

- `SCRATCH(this session)/ladder/descend_ladder.py` — Iterated mid-road restarts, v2. Row spec CID:AC_TARGET:MODE[:CUTHI[:LINK]] MODE xy = beam aims at (x,y) (AC tails, plus the beam's own SAC tails); yx = beam on the letter-swapped state, so the search aims at (y,x): Stabl

## SCRATCH(this session)/law_scope.py

- `SCRATCH(this session)/law_scope.py` — (no header)

## SCRATCH(this session)/lists.py

- `SCRATCH(this session)/lists.py` — (no header)

## SCRATCH(this session)/long_rows.py

- `SCRATCH(this session)/long_rows.py` — (no header)

## SCRATCH(this session)/mitm.py

- `SCRATCH(this session)/mitm.py` — (no header)

## SCRATCH(this session)/moves.py

- `SCRATCH(this session)/moves.py` — count which tools / engines / scripts my own Bash commands invoked (names only; no transcript text is printed)

## SCRATCH(this session)/orows/ab

- `SCRATCH(this session)/orows/ab/ab_runs.py` — Song idea 2b runs: repo-current acc_beam with the abelian-shadow term (acc_beam_ab), dual-P2 settings, W, depth = SAC record. Configs per row: control (term off), AB=1 (plain key), ABP=2 (P2 field); target J (ending (y,x
- `SCRATCH(this session)/orows/ab/acc_beam_ab.c` — Beam search + exact finish. Forward beam from the start keeps the W states of smallest total relator length per depth (ties broken by fingerprint), deduplicated across all depths. Every generated state is looked up in T_

## SCRATCH(this session)/orows/abel.py

- `SCRATCH(this session)/orows/abel.py` — Song idea 2a (count the throb): exponent-sum matrix E of a state; exact row-op distance to I ((x,y)) and J ((y,x)) by BFS over |entries| <= M. Compare with the number of non-conjugation moves in our roads.

## SCRATCH(this session)/orows/collect.py

- `SCRATCH(this session)/orows/collect.py` — Collect every road we hold for the orows target numbers (ac- and sac- lines), verify on the official cores, write best per row.

## SCRATCH(this session)/orows/collect2.py

- `SCRATCH(this session)/orows/collect2.py` — Collect every road we hold for the orows target numbers (ac- and sac- lines), verify on the official cores, write best per row.

## SCRATCH(this session)/orows/famxfer.py

- `SCRATCH(this session)/orows/famxfer.py` — Family transfer with exact alignment: for target row T, step i on our road, and donor row U whose class meets T's road, BFS (depth R, all 14 moves) from s_i to ANY exact image g(u_j) (16 symmetries) of the first J states

## SCRATCH(this session)/orows/fm2.py

- `SCRATCH(this session)/orows/fm2.py` — Foreign meet v2 (orows): like tools/acc/upgh/foreign_meet.py, but (a) the donor roads may end at (x,y) OR (y,x), (b) the finish after relabelling goes to (x,y) for AC lines and to (x,y)+[16,15] or (y,x)+[15,15] for Stabl

## SCRATCH(this session)/orows/fold

- `SCRATCH(this session)/orows/fold/fold_beam.py` — Song idea 1 (FOLD): rotation-folded multiplication beam. One step = rotate r0 by a and r1 by b with real conjugation moves (|a|,|b| <= R, each rotation step = 1 move), then one multiplication (moves 2-5); or a single inv
- `SCRATCH(this session)/orows/fold/plain_beam.py` — Control for song idea 1: plain Python beam, layers by move count, all 14 moves, W best by total length (seeded tie-break), same exact finish balls as fold_beam.py. usage: plain_beam.py ROW W MAXD [SEED]

## SCRATCH(this session)/orows/mitm_05598_sweep.sh

- `SCRATCH(this session)/orows/mitm_05598_sweep.sh` — (no header)

## SCRATCH(this session)/orows/mitm_sweep2.sh

- `SCRATCH(this session)/orows/mitm_sweep2.sh` — tie-scope MITM sweeps: ROW A caps...; stop a row at the first cap that does not complete depth A or that finds something

## SCRATCH(this session)/orows/mitm_sweep3.sh

- `SCRATCH(this session)/orows/mitm_sweep3.sh` — tie-scope MITM sweeps: ROW A caps...; stop a row at the first cap that does not complete depth A or that finds something

## SCRATCH(this session)/orows/mitm_test.py

- `SCRATCH(this session)/orows/mitm_test.py` — (no header)

## SCRATCH(this session)/orows/stop_fp.sh

- `SCRATCH(this session)/orows/stop_fp.sh` — stop fixpoint_shorten (PID 2777) after its 4th road finishes; kill by PID only

## SCRATCH(this session)/orows/tailmeet.py

- `SCRATCH(this session)/orows/tailmeet.py` — Tail meet: for every state on every road we hold for a row (AC roads to (x,y) and AC-move prefixes of Stable lines), take the shortest prefix index p at which we reach it, and compute the EXACT distance to (x,y) and to (

## SCRATCH(this session)/orows/tailmeet_r3.py

- `SCRATCH(this session)/orows/tailmeet_r3.py` — Tail meet: for every state on every road we hold for a row (AC roads to (x,y) and AC-move prefixes of Stable lines), take the shortest prefix index p at which we reach it, and compute the EXACT distance to (x,y) and to (

## SCRATCH(this session)/orows/yx_mitm.c

- `SCRATCH(this session)/orows/yx_mitm.c` — yx_mitm (orows, 2026-10-14): exact capped meet in the middle, AC (x,y) and Stable via (y,x)+[15,15]. Kernel/fingerprint/table: acc_opt.c verbatim (included). Backward ball TB: BFS from (x,y) over states with total length

## SCRATCH(this session)/poll_score.py

- `SCRATCH(this session)/poll_score.py` — (no header)

## SCRATCH(this session)/pool.py

- `SCRATCH(this session)/pool.py` — Helpers to merge member song ideas into SONG_IDEAS_POOL.md: add(song, row_md, member) / replace(song, member_prefix, row_md).

## SCRATCH(this session)/pool_vs_repo.py

- `SCRATCH(this session)/pool_vs_repo.py` — For Astra's 25 rows: every route in the repo (any length) vs her pool; verify repo-only ones.

## SCRATCH(this session)/pug.py

- `SCRATCH(this session)/pug.py` — (no header)

## SCRATCH(this session)/pull_ranks.py

- `SCRATCH(this session)/pull_ranks.py` — (no header)

## SCRATCH(this session)/pull_teams.py

- `SCRATCH(this session)/pull_teams.py` — (no header)

## SCRATCH(this session)/pull_us.py

- `SCRATCH(this session)/pull_us.py` — (no header)

## SCRATCH(this session)/r3/tab.py

- `SCRATCH(this session)/r3/tab.py` — (no header)

## SCRATCH(this session)/r9/bf.sh

- `SCRATCH(this session)/r9/bf.sh` — P000011-style best-first, f = L + w*d (our acc_bestfirst: f = 4L + W4*d, W4 = 4w), T8 finish

## SCRATCH(this session)/r9/probe.sh

- `SCRATCH(this session)/r9/probe.sh` — beam-setting probe on ac-00009 (record 34, k7): which setting finds the short road?

## SCRATCH(this session)/recognition_web.py

- `SCRATCH(this session)/recognition_web.py` — Recognition web (song 12, "Individual faces come and they go, / but the recognition between us is what make us whole.").

## SCRATCH(this session)/roundup_moves.py

- `SCRATCH(this session)/roundup_moves.py` — (no header)

## SCRATCH(this session)/run_here.sh

- `SCRATCH(this session)/run_here.sh` — Long-row kit on the cloud container: 4 single-holder constructed rows; commits progress every 20 min (no model use).

## SCRATCH(this session)/scan_all.py

- `SCRATCH(this session)/scan_all.py` — Broad scan: every file in the repo (not .git), any extension, nested JSON, gz. Compare with ledger best/board/held.

## SCRATCH(this session)/sg_cov.py

- `SCRATCH(this session)/sg_cov.py` — (no header)

## SCRATCH(this session)/sol61/official

- `SCRATCH(this session)/sol61/official/competition/tools/verifier/__init__.py` — Discovery Track reference verifier — Python, standard library only (D-10).
- `SCRATCH(this session)/sol61/official/competition/tools/verifier/__main__.py` — (no header)
- `SCRATCH(this session)/sol61/official/competition/tools/verifier/canon.py` — Canonical serialization and hashing (DESIGN.md §3.2, §3.3).
- `SCRATCH(this session)/sol61/official/competition/tools/verifier/cli.py` — ``verifier`` command line interface (DESIGN.md §4.4).
- `SCRATCH(this session)/sol61/official/competition/tools/verifier/core.py` — Deterministic verifier core for AC, move spec ``ac-r2-v1``.
- `SCRATCH(this session)/sol61/official/competition/tools/verifier/golden.py` — Golden-vector conformance runner (DESIGN.md §9.2, acceptance rows 5 and 15).
- `SCRATCH(this session)/sol61/official/competition/tools/verifier/specs.py` — Move-spec registry: ``move_spec_version`` -> the semantics that implement it.
- `SCRATCH(this session)/sol61/official/competition/tools/verifier/stable_core.py` — Deterministic verifier core for Stable AC, move spec ``sac-r8-v1``.
- `SCRATCH(this session)/sol61/official/competition/tools/verifier/submission.py` — Parse TXT submissions and dispatch paths to the official move verifier.

## SCRATCH(this session)/sol61/sol61

- `SCRATCH(this session)/sol61/sol61/check_bounded_search.py` — Synthetic bounded-search correctness experiment; no competition rows.
- `SCRATCH(this session)/sol61/sol61/check_moves.py` — Differential check of the independent C++ move implementation on synthetic states.
- `SCRATCH(this session)/sol61/sol61/run_control.py` — Rediscover only ac-09409 from the exact pinned manifest, then verify locally.

## SCRATCH(this session)/sol_ib/integer_bound.py

- `SCRATCH(this session)/sol_ib/integer_bound.py` — Exact lower bounds in the integer exponent projection of capped AC paths.

## SCRATCH(this session)/state_audit.py

- `SCRATCH(this session)/state_audit.py` — (no header)

## SCRATCH(this session)/targets.py

- `SCRATCH(this session)/targets.py` — (no header)

## SCRATCH(this session)/team_rows.py

- `SCRATCH(this session)/team_rows.py` — (no header)

## SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis

- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/__init__.py` — ACC Memory-First Harness: orchestration, not a search solver.
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/demo.py` — Exercise the complete controller with labelled toy workers and checker.
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/gates.py` — Exact-artifact gates for an externally supplied, pinned ACC checker.
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/geometry.py` — Optional finite matrix diagnostics. These never certify or prune ACC states.
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/harness.py` — Offline agent orchestration. Commands are configured clients, never model output.
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/runtime.py` — Small durable task kernel and bounded JSON subprocess transport.
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/selftest.py` — Run local fault tests. These do not call a model or validate real ACC routes.
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/tests/test_gates.py` — Gate integration tests using a TOY receipt producer, NOT an ACC checker.
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/tests/test_geometry.py` — (no header)
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/tests/test_runtime.py` — Kernel regressions: durable evidence, fencing, stop, and bounded execution.
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/tests/test_workflow.py` — (no header)
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/workers/demo_checker.py` — TOY CHECKER ONLY. One defined string transformation; not an ACC checker.
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/workers/demo_worker.py` — DEMONSTRATION ONLY. Deterministic role responses; no language model is called.
- `SCRATCH(this session)/tmp.8cnAW4WHRU/acc_synthesis/workers/example_bridge.py` — JSON-lines boundary example, intentionally no invented model API bindings.

## SCRATCH(this session)/top_rows.py

- `SCRATCH(this session)/top_rows.py` — (no header)

## SCRATCH(this session)/trace.py

- `SCRATCH(this session)/trace.py` — (no header)

## SCRATCH(this session)/verify_cands.py

- `SCRATCH(this session)/verify_cands.py` — (no header)

## SCRATCH(this session)/verify_lines.py

- `SCRATCH(this session)/verify_lines.py` — verify_lines.py OUT SRC... : every distinct 'ac-/sac-NNNNN: [..]' line in SRC files, official CLI (<=400 per file, unique ids), forbidden rows dropped.

## SCRATCH(this session)/viz/board_map.py

- `SCRATCH(this session)/viz/board_map.py` — (no header)

## SCRATCH(this session)/yxfin/run.sh

- `SCRATCH(this session)/yxfin/run.sh` — exact finish distance from P_m to (x,y) and to (y,x), cap = fin2 peak + 2 (join_bidi, all 14 moves)

## research/acc/live

- `research/acc/live/sweeps/beam_clusters/run.sh` — First-solve beam on Bob's unsolved clusters: one representative per class, production beam flags (Git's nt lane), W 100k, depth 80 + exact T8 finish. A road on any member carries to its whole cluster (Bob's bridges + sym
- `research/acc/live/sweeps/beam_k1short/run.sh` — Beam + exact finish (T8) + window shortening on the 6 single-holder rows with no road from us and records <= 40.
- `research/acc/live/sweeps/cov/firstsolve/closest_pass.py` — Closest-approach pass for pilot keys that ran before the driver logged it: direct mode only, same W/D, min total length of the kept beam (sampled every 10 depths) on M. usage: closest_pass.py W D REP [REP ...]
- `research/acc/live/sweeps/cov/firstsolve/firstsolve.py` — First solves on UNSOLVED rows through the Whitehead-minimal frame (orows partner, 2026-10-14, owner-approved lane). For each unsolved key (rows with the same Whitehead-minimal form up to letter maps / relator swap / rota
- `research/acc/live/sweeps/gap1_fresh/run_gap1.py` — Fresh gap-1 lane (UPG-H, 6 Oct): exact window-14 shortening (acc_window, end state kept fixed) on our best (x,y) and (y,x) roads for single-holder rows nobody has worked. Writes verified shorter roads to inbox/upgh_gap1_
- `research/acc/live/sweeps/git/handoff_tools/commute_clean.py` — SCRIPT: COMMUTE_CLEAN  UPG-H's song-4 rule, own implementation: two AC moves commute when neither writes a relator the other reads or writes. A move m and a later inverse(m) with only m-commuting moves between them cance
- `research/acc/live/sweeps/git/handoff_tools/harvest_git.py` — SCRIPT: HARVEST_GIT  collect every road Git (session 3) produced, replay each on the official ac-r2-v1 core, compare to the 6 Oct 03:15Z boards, write one line per distinct verified road.
- `research/acc/live/sweeps/git/handoff_tools/nt_run.sh` — SCRIPT: NEWTARGET_BEAM  team beam rebuilt from current source; production flags; free depth record+20; W 100000
- `research/acc/live/sweeps/git/handoff_tools/nt_worker.py` — SCRIPT: NEWTARGET_WORKER  runs rows from a list one at a time (free-depth P2 dual beam W 100000, DMAX record+20), then: replays the AC route on the official core, runs the tight road DP on it, writes the shortest checked
- `research/acc/live/sweeps/git/handoff_tools/skel_dp_fixed.py` — tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_SKELETON_DP  Keep a path's road (its sequence of conjugacy-class states: each relator up to rotation, conjugation and inversion; the pair 
- `research/acc/live/sweeps/git/handoff_tools/skel_dp_loose_fixed.py` — tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_SKELETON_DP  Keep a path's road (its sequence of conjugacy-class states: each relator up to rotation, conjugation and inversion; the pair 
- `research/acc/live/sweeps/git/handoff_tools/splice_bob.py` — SCRIPT: CLASS_SPLICE_BOB  Song line: "Two faces can wear the same quiet disguise ... add a color, add a depth, and the twins come apart." States that are the same up to rotation/conjugation/inversion (one class = one dis
- `research/acc/live/sweeps/git/handoff_tools/splice_scout.py` — SCRIPT: CLASS_SPLICE_SCOUT  song 2 line: 'Two different drums can sing the same set of quotes' -- class splice onto the scout's LOST/NEAR rows (8 junctions per row) States that are the same up to rotation/conjugation/inv
- `research/acc/live/sweeps/git/handoff_tools/splice_yx.py` — SCRIPT: SPLICE_THEN_YX  the combination that tied sac-05598: (1) class-level cross-row splice makes new-lineage roads at or near our best, (2) the team's yx_shortcut.py tries a (y,x) finish with target = Stable record. R
- `research/acc/live/sweeps/git/handoff_tools/yx_ball.py` — SCRIPT: YX_BALL  DP keeps our class road but stores EVERY orientation state it reaches in every class (with cost); a backward ball around (y,x) (depth BD) meets them. Stable line = DP prefix + ball route to (y,x) + [15,1
- `research/acc/live/sweeps/git/handoff_tools/yx_ball2.py` — SCRIPT: YX_BALL  DP keeps our class road but stores EVERY orientation state it reaches in every class (with cost); a backward ball around (y,x) (depth BD) meets them. Stable line = DP prefix + ball route to (y,x) + [15,1
- `research/acc/live/sweeps/git/handoff_tools/yx_dp.py` — SCRIPT: YX_DP  keep each road's class sequence, but have the DP end at (y,x) instead of (x,y). Stable line = DP route to (y,x) + [15,15]. Tight and loose settings.
- `research/acc/live/sweeps/git/held.py` — SCRIPT: HELD  team held length per row id (ac-* and sac-* separately): min over accepted submissions (all mine_*.json) and the ledger snapshot. Rule (UPG-H 11:01Z): queue only if length < held AND <= live record.
- `research/acc/live/sweeps/git/rank3_catalyst.py` — SCRIPT: RANK3_CATALYST  UPG-H job (a): mid-route stabilization on sac-08078. Take our (y,x)-ending Stable line (route t_0..t_L, L=33, then [15,15] = 35). At t_i stabilize (move 14 -> (r0,r1,(3,))), search rank 3 under th
- `research/acc/live/sweeps/git/splice_orient.py` — SCRIPT: SPLICE_ORIENT  class splice that respects slot orientation. Finding: our failed joins were SWAPPED (donor holds our relators in the other slots); inner moves can never swap slots. Fix: on a swapped join, relabel 
- `research/acc/live/sweeps/ladder_law/dump_rows.py` — Dump per-row ladder roads (canonical macro + exact prefix join with KMAX 13 + frame finish) for the XXYxy rows n=NMIN..NMAX into rows_roads.jsonl ({"id","ac"}), for fixpoint_shorten. usage: dump_rows.py NMIN NMAX
- `research/acc/live/sweeps/ladder_law/join_bidi.c` — join_bidi: cheapest join of a start state S0 onto a known trajectory (ac-r2-v1 kernel of acc_opt.c, restricted move mask): minimise dist(S0, traj[k]) + off_k over trajectory states (off_k = remaining offset given by the 
- `research/acc/live/sweeps/ladder_law/join_bidi.py` — Cheapest join of a row start S0 onto a known trajectory traj[0..L] (restricted moves, total length <= cap): minimise dist(S0, traj[k]) + (L - k) over k, by a bidirectional BFS whose backward side starts from every traj[k
- `research/acc/live/sweeps/ladder_law/join_run.py` — Driver for join_bidi (C): per-row join of the row start onto the canonical macro trajectory, then the per-row road. usage: join_run.py N CID [KMAX] [SLACK] [VARIANTS]
- `research/acc/live/sweeps/ladder_law/ladder_rows.py` — Per-row doubling roads on the MS(n, w*) ladder 'XXYxy' (n = 4..10), built from the canonical macro loop (loop_macro.py): 1. map the row start into the canonical frame (symmetry g with g(MS canonical) = row up to cyclic w
- `research/acc/live/sweeps/ladder_law/loop_beam.c` — loop_beam: layered beam over a restricted AC move set (ac-r2-v1 kernel of acc_opt.c) from START to the exact GOAL state. Keeps the W states of each depth with the best progress score of the multiplied relator (slot): sco
- `research/acc/live/sweeps/ladder_law/loop_beam.py` — Beam version of the BS-doubling loop search (restricted model of loop_bidi.py: the w*-relator is never multiplied). Layered by depth; keeps the W states with the best progress score (#x letters - 2 #y letters) of the MS 
- `research/acc/live/sweeps/ladder_law/loop_beam_run.py` — Driver for loop_beam (C): canonical MS(n, w*) doubling loop -> pre-finish, + fin2. usage: loop_beam_run.py N W [SLACK]
- `research/acc/live/sweeps/ladder_law/loop_bidi.py` — Bidirectional exact BFS for the BS-doubling loop (same restricted model as loop_opt.py: r1 never multiplied). The move graph is undirected (each move has an inverse move in the allowed set), so the backward search uses t
- `research/acc/live/sweeps/ladder_law/loop_greedy.py` — Greedy-with-lookahead BS-doubling loop (restricted model: the w*-relator is never multiplied). From the current state, BFS (depth <= D) for the nearest state reached by a GOOD move: a multiplication of the MS relator tha
- `research/acc/live/sweeps/ladder_law/loop_macro.py` — Macro BS-doubling loop for MS(n, w*) (r1 = x x Y X y), read off the exact optima for n = 3..5 (loop_bidi.py): L1 [6, 9, 3] Y X y -> X X (a = 1) L2 (normal) [7, 12, 3, 6, 3] r1 -> y x x Y X once; rule Y X -> X X Y (move 3
- `research/acc/live/sweeps/ladder_law/loop_opt.py` — Exact optimum of the BS-doubling LOOP of tools/acc/upgh/bs_doubling.py in the restricted model (r1 never multiplied: moves 0,1,2,3,6..13 only), from the MS(n, w*) start to the exact pre-finish state (Y x^m y y X, x x Y X
- `research/acc/live/sweeps/ladder_law/loop_rows.py` — Per-row exact BS-doubling roads on the MS(n, w*) ladder (rows of the 'XXYxy' family), searched in each row's OWN frame: for every symmetry g that carries the canonical MS(n, w*) onto the row (up to cyclic words), the goa
- `research/acc/live/sweeps/ladder_law/run_targets.sh` — (no header)
- `research/acc/live/sweeps/mid_restart_lane/mr_lane.py` — Mid-restart lane (Moves Manual trick #2, session 2's beat-maker; tools/acc/ops/mid_restart.py extended to Stable): for each row 1 move over an AC or Stable record (best tie value first), restart the production beam from 
- `research/acc/live/sweeps/mid_restart_lane_v2/mr_lane.py` — Mid-restart lane v2 (W 60000; rows 1 over a k<=2 record or 2 over a k1 record, live board).\nMid-restart lane (Moves Manual trick #2, session 2's beat-maker; tools/acc/ops/mid_restart.py extended to Stable): for each row
- `research/acc/live/sweeps/mid_restart_lane_v3/mr_lane.py` — Mid-restart lane v3 (W 60000; Always Ready k1/k2 rows where we hold a road, gap <= 11).\nMid-restart lane (Moves Manual trick #2, session 2's beat-maker; tools/acc/ops/mid_restart.py extended to Stable): for each row 1 m
- `research/acc/live/sweeps/mr_upgh/mr_lane.py` — orows mid-restart lane on the NEW engine (2026-10-14 round 4; /root/.cache/acc_beam_bin/acc_beam = repo build since 02:20Z, so BEAM_P2/DUAL/ELITE are really read). Hits go to hits_SHARD.txt here.\nMid-restart lane (Moves
- `research/acc/live/sweeps/mr_upgh2/mr_lane.py` — orows mid-restart lane on the NEW engine (2026-10-14 round 4; /root/.cache/acc_beam_bin/acc_beam = repo build since 02:20Z, so BEAM_P2/DUAL/ELITE are really read). Hits go to hits_SHARD.txt here.\nMid-restart lane (Moves
- `research/acc/live/sweeps/orows/capped/capped_run.py` — orows exact capped sweep (song-7 recipe: acc_capped + T8 finish, INIT_LOG2=26, budget per cap). acc_capped checks both endings: AC (x,y) and Stable via (y,x) + [15,15] (its swap lookup) or AC + [16,15]. Scope of a miss: 
- `research/acc/live/sweeps/orows/capped/guarded_cap.sh` — run one capped job; kill its acc_capped child by PID if the root disk falls below 1.5 GB free (layer files)
- `research/acc/live/sweeps/orows/mr_lane/mr_lane.py` — orows mid-restart lane (copied from v3 on 2026-10-14; jobs.json hand-written for the orows targets; hits go to hits_SHARD.txt here).\nMid-restart lane (Moves Manual trick #2, session 2's beat-maker; tools/acc/ops/mid_res
- `research/acc/live/sweeps/orows/mr_lane_new/mr_lane.py` — orows mid-restart lane on the NEW engine (2026-10-14 round 4; /root/.cache/acc_beam_bin/acc_beam = repo build since 02:20Z, so BEAM_P2/DUAL/ELITE are really read). Hits go to hits_SHARD.txt here.\nMid-restart lane (Moves
- `research/acc/live/sweeps/orows/mr_lane_new2/mr_lane.py` — orows mid-restart lane on the NEW engine (2026-10-14 round 4; /root/.cache/acc_beam_bin/acc_beam = repo build since 02:20Z, so BEAM_P2/DUAL/ELITE are really read). Hits go to hits_SHARD.txt here.\nMid-restart lane (Moves
- `research/acc/live/sweeps/orows/mr_lane_new3/mr_lane.py` — orows mid-restart lane on the NEW engine (2026-10-14 round 4; /root/.cache/acc_beam_bin/acc_beam = repo build since 02:20Z, so BEAM_P2/DUAL/ELITE are really read). Hits go to hits_SHARD.txt here.\nMid-restart lane (Moves
- `research/acc/live/sweeps/orows/queue_r2.sh` — orows round 2, one heavy slot, sequential: waits for fixpoint (PID 2777) to stop, then cap 23 -> yx beams seed 0 -> cap 25 -> yx beams seed 7 -> cap 27 (sac-09501 caps start+3/+5/+7, budget 150M, MAXD 21).
- `research/acc/live/sweeps/orows/tools/ab_runs.py` — Song idea 2b runs: repo-current acc_beam with the abelian-shadow term (acc_beam_ab), dual-P2 settings, W, depth = SAC record. Configs per row: control (term off), AB=1 (plain key), ABP=2 (P2 field); target J (ending (y,x
- `research/acc/live/sweeps/orows/tools/abel.py` — Song idea 2a (count the throb): exponent-sum matrix E of a state; exact row-op distance to I ((x,y)) and J ((y,x)) by BFS over |entries| <= M. Compare with the number of non-conjugation moves in our roads.
- `research/acc/live/sweeps/orows/tools/collect.py` — Collect every road we hold for the orows target numbers (ac- and sac- lines), verify on the official cores, write best per row.
- `research/acc/live/sweeps/orows/tools/famxfer.py` — Family transfer with exact alignment: for target row T, step i on our road, and donor row U whose class meets T's road, BFS (depth R, all 14 moves) from s_i to ANY exact image g(u_j) (16 symmetries) of the first J states
- `research/acc/live/sweeps/orows/tools/fm2.py` — Foreign meet v2 (orows): like tools/acc/upgh/foreign_meet.py, but (a) the donor roads may end at (x,y) OR (y,x), (b) the finish after relabelling goes to (x,y) for AC lines and to (x,y)+[16,15] or (y,x)+[15,15] for Stabl
- `research/acc/live/sweeps/orows/tools/fold_beam.py` — Song idea 1 (FOLD): rotation-folded multiplication beam. One step = rotate r0 by a and r1 by b with real conjugation moves (|a|,|b| <= R, each rotation step = 1 move), then one multiplication (moves 2-5); or a single inv
- `research/acc/live/sweeps/orows/tools/plain_beam.py` — Control for song idea 1: plain Python beam, layers by move count, all 14 moves, W best by total length (seeded tie-break), same exact finish balls as fold_beam.py. usage: plain_beam.py ROW W MAXD [SEED]
- `research/acc/live/sweeps/orows/tools/tailmeet.py` — Tail meet: for every state on every road we hold for a row (AC roads to (x,y) and AC-move prefixes of Stable lines), take the shortest prefix index p at which we reach it, and compute the EXACT distance to (x,y) and to (
- `research/acc/live/sweeps/orows/tools/yx_mitm.c` — yx_mitm (orows, 2026-10-14): exact capped meet in the middle, AC (x,y) and Stable via (y,x)+[15,15]. Kernel/fingerprint/table: acc_opt.c verbatim (included). Backward ball TB: BFS from (x,y) over states with total length
- `research/acc/live/sweeps/orows/yx_beam/yx_beam.py` — orows (y,x) beam (2026-10-14; adapted from sweeps/rival3/rival_beam.py, same dual-P2 beam + T8 finish and env). Default mode "yx": beam the letter-swapped start (x<->y, relator order kept), so a road to (x,y) there is a 
- `research/acc/live/sweeps/ppo/worker.sh` — Claims 20-key chunks of data/unsolvedM.txt (atomic mkdir) and runs the 610model beam search on each; resumable.
- `research/acc/live/sweeps/rival3/audit_submissions.py` — Audit our recent SAIR submissions: per line, was it accepted, a duplicate of what we already held, an improvement, and does it score on the live board (our length == record; per-team points 2^(1-k))? usage: audit_submiss
- `research/acc/live/sweeps/rival3/board_map.py` — (no header)
- `research/acc/live/sweeps/rival3/p000011_bestfirst_probe.sh` — P000011-style best-first, f = L + w*d (our acc_bestfirst: f = 4L + W4*d, W4 = 4w), T8 finish
- `research/acc/live/sweeps/rival3/rival_beam.py` — Rival #3 lane: dual P2 beam (the 'two eyes' winner) + T8 finish on the rows the new #3 player holds, in three orientations (direct; mirror twin x<->y with relators swapped; (y,x) twin for Stable). Every road is replayed 
- `research/acc/live/sweeps/session1/stepping_stone/scripts/make_targets.py` — Write targets_g1.csv (k_teams<=2, gap 1..8, longest record first) and targets_g2.csv (unsolved ac rows with initial relator total <= 16, shortest first). Never-rows are excluded. The CSV has CRLF line ends.
- `research/acc/live/sweeps/session1/stepping_stone/scripts/run_all.sh` — usr/bin/env bash Rerun the whole stepping-stone experiment without a model (about 1-2 h on 3 cores). usage: bash run_all.sh /path/to/sair-checkout     (run from the repo root: /home/user/operator-first)
- `research/acc/live/sweeps/session1/stepping_stone/scripts/stones_lib.py` — Stepping-stone library (self-contained; only needs the official SAIR verifier checkout for final replay).
- `research/acc/live/sweeps/session1/stepping_stone/scripts/stones_search.py` — Idea A (stepping stones) and the lookup half of idea B.
- `research/acc/live/sweeps/session1/stepping_stone/scripts/walks.py` — Idea B: blind guesses with known roads. Random walks BACKWARD from the goal (x,y). Every state on a walk has a known road to the goal (the reversed walk, each move replaced by its inverse; INV = 0,1,3,2,5,4,7,6,9,8,11,10
- `research/acc/live/sweeps/session1/surgery/cap_surgery_s1.py` — session 1 copy of UPG-H t00073 cap_surgery.py, generalised: ROW, route (from routes.json), finish and cap K from env; Stable (y,x) routes run on the relator-swapped row. t00073 builder adapter around Charlie's surgery.py
- `research/acc/live/sweeps/session1/surgery/run_rows.sh` — session 1: raised-ceiling surgery (UPG-H assignment 18:00Z). Per row: windows, head, tail at K = start + 6; after any shortening the new line replaces the row's route in routes.json and the lanes restart on it, until no 
- `research/acc/live/sweeps/song_lane/song5_drop_prefix.py` — Song 5 ("The universe reorganizes what no longer serves", session 1's idea): drop the prefix that no longer serves. For each high-value row of mid_restart_lane_v2/jobs.json (1 over a k<=2 record, or 2 over a k1 record), 
- `research/acc/live/sweeps/song_lane/song7_minpeak.sh` — Song 7 ("the vertical amplification", session 1's idea): exact capped BFS + T8 finish (acc_capped) from the start of each short k<=2 row we do not hold, rising caps start+3 / start+5; MAXD = record - 8, budget 150M state
- `research/acc/live/sweeps/window_lane/window_lane.py` — Window lane (UPG-H, 6 Oct): exact window-14 shortening (acc_window, end kept fixed) on every distinct road we hold that is 1-2 moves over a record (AC to (x,y); Stable via (x,y)+[16,15] or (y,x)+[15,15]), new team lineag

## research/acc/optimality

- `research/acc/optimality/acc_batch.c` — Batch meet: load T_B once, then for each start line "tag l0 w.. l1 w.." compute min dS+dT over S_A ∩ T_B (exact distance if <= A+B), rebuild and print the path. Same kernel/fingerprint/table as acc_opt.c (included verbat
- `research/acc/optimality/acc_beam.c` — Beam search + exact finish. Forward beam from the start keeps the W states of smallest total relator length per depth (ties broken by fingerprint), deduplicated across all depths. Every generated state is looked up in T_
- `research/acc/optimality/acc_bestfirst.c` — Cap-free best-first search, ac-r2-v1 (kernel, fingerprint and goal table shared verbatim with acc_opt.c). Priority f = 4*L + W4*d (L = total relator length of the state, d = moves from the start, W4 = 4*w), popped lowest
- `research/acc/optimality/acc_c16.c` — acc_c16: ceiling finish table ("C16"). BFS from (x,y) over the states of total relator length <= CEIL (default 16), moving only through such states, layer by layer until closure (or a state/time budget), storing each sta
- `research/acc/optimality/acc_capped.c` — Capped exhaustive BFS + exact finish: BFS from the start over states with total relator length <= CAP (uncapped T_9 lookups on every state). The first depth d at which min(d + dT) can no longer improve gives the shortest
- `research/acc/optimality/acc_capped_disk.c` — File-backed fixed visited-table pilot; same 123-bit fingerprint semantics. Positive paths require official verification; negative bounds retain the fingerprint caveat. Set VISITED_FILE=/path/visited.tab for MAP_SHARED, s
- `research/acc/optimality/acc_capped_p2.c` — Capped exhaustive BFS + exact finish, restricted by P2 ("cross the wall, keep the record clean"). Copy of acc_capped.c (left unchanged, in use) with one extra admission rule. With CAP_P2=c a state is expanded and stored 
- `research/acc/optimality/acc_opt.c` — ACC exact-optimality meet engine, ac-r2-v1 (SAIR Andrews-Curtis commit a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e, competition/tools/verifier/core.py, 14 moves). NO LENGTH CAP. Letters: 0=x 1=x^-1 2=y 3=y^-1 (inverse = c^1
- `research/acc/optimality/acc_window.c` — ACC exact window shortening, ac-r2-v1 (SAIR a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e). Kernel, fingerprint and table are shared verbatim with acc_opt.c (included). For path states s_0..s_n: for every pair i<j with j-i <=
- `research/acc/optimality/acc_window11.c` — ACC exact window shortening, ac-r2-v1 (SAIR a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e). Kernel, fingerprint and table are shared verbatim with acc_opt.c (included). Low-memory variant of acc_window.c. For path states s_0.
- `research/acc/optimality/acc_window8.c` — ACC exact window shortening, ac-r2-v1 (SAIR a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e). Kernel, fingerprint and table are shared verbatim with acc_opt.c (included). Low-memory variant of acc_window.c. For path states s_0.
- `research/acc/optimality/acc_window_cross.c` — ACC exact crossover between two paths, ac-r2-v1 (SAIR a0fd6e6). Finds a route of at most j-i-1 moves from path A's state i to path B's state j, using B6(A_i) intersect B7(B_j). Both paths must have the same length and en
- `research/acc/optimality/analyze_board.py` — Rank full-board batch results (xy- = AC to (x,y), yx- = swapped start, i.e. AC to (y,x)). Every candidate path is replayed by the official verifier (ac core / stable core) before listing. usage: analyze_board.py SAIR boa
- `research/acc/optimality/astra_subprocess_audit/check_guard.py` — Check failure handling with tiny stub executables, without running a search.
- `research/acc/optimality/astra_subprocess_audit/midroute_one.py` — One lead-authorized mid-route restart, gated by the completed wide pilot.
- `research/acc/optimality/astra_subprocess_audit/recover_07194_20260929.py` — Recover the completed audited beam; no API calls and no beam launch.
- `research/acc/optimality/astra_subprocess_audit/recovery_20260929T1402/continue_first3.py` — Wait for this identified recovery, then resume only the final pilot row.
- `research/acc/optimality/astra_subprocess_audit/recovery_20260929T1402/prelaunch.py` — Resume only row three after receipt recovery and existing controls.
- `research/acc/optimality/astra_subprocess_audit/sitecustomize.py` — Opt-in subprocess audit for run_beam_raw.py.
- `research/acc/optimality/astra_subprocess_audit/watch_batch.py` — Observe the running Astra batch and verify new paths; never launch a search.
- `research/acc/optimality/astra_subprocess_audit/window_sanitizer_probe.py` — Offline sanitizer diagnostic of the known positive window control.
- `research/acc/optimality/beam_loss.py` — Beam-loss diagnostic (atlas B20 + Plate XI: "is the road lost among ties, ranked wrong, or just short of width?").
- `research/acc/optimality/build_echo.py` — Build the echo table for acc_capped (ECHO_FILE): states on or within R moves of our known routes for one row, each with an upper bound on its remaining distance to (x, y) and the tail of moves that achieves it. Routes: c
- `research/acc/optimality/c16_scan_sac_swaps.py` — Check the swapped rank-two reverse finish plus two stable deletions.
- `research/acc/optimality/c16_scan_starts.py` — Check all short-start AC rows against a completed ceiling reverse table. Usage: python c16_scan_starts.py MANIFEST BOARD_GZ TABLE BINARY OUT_PREFIX
- `research/acc/optimality/c16_splice_path.py` — Query a C16 reverse table at every eligible state of a known AC path.
- `research/acc/optimality/c16_table.inc` — ---- ceiling finish table ("C16"), shared by acc_c16.c (builder) and acc_beam.c (BEAM_C16) ---- Contents: every state reachable from (x,y) through states of total relator length <= CEIL, with its BFS distance inside that
- `research/acc/optimality/c16_verify_sample.py` — Replay the C16 sample descents (acc_c16 sample output) with the official SAIR verifier.
- `research/acc/optimality/chain_rowops/convlen.py` — How many consecutive r1<-r1*r0^e moves (no conjugation between) can do useful work? Enumerate r0 = conjugates of BS^{+-1} by words w (|w|<=L) and r1 = chain-level word, and see whether a run r1*r0^e1*r0^e2... (same r0) c
- `research/acc/optimality/chain_rowops/level_beam.py` — (no header)
- `research/acc/optimality/chain_rowops/sl2geo.py` — Row-op geometry of a chain level: rows = exponent-sum vectors of (r0, r1). Moves: r1 += +-r0 (E21), r0 += +-r1 (E12); inversions (row sign) and conjugations are free here. Count shortest row-op words taking M0=[[-1,0],[a
- `research/acc/optimality/codex_commutator_phase_probe.py` — Check Lisitsa/MS mapping and cyclic commutator phases with pinned SAIR core.
- `research/acc/optimality/experiments/acc_beam_snell.c` — Beam search + exact finish. Forward beam from the start keeps the W states of smallest total relator length per depth (ties broken by fingerprint), deduplicated across all depths. Every generated state is looked up in T_
- `research/acc/optimality/experiments/astra_p2_linear/benchmark.py` — Reproduce the isolated Astra least-rotation benchmark; does not alter acc_beam.c.
- `research/acc/optimality/experiments/astra_p2_linear/check_minrot.c` — include <stdio.h> include <stdint.h> include <string.h> include <stdlib.h>
- `research/acc/optimality/experiments/astra_p2_linear/signed_finish_probe.c` — define ACC_NO_MAIN include "acc_opt.c"
- `research/acc/optimality/experiments/astra_paper_transfer_20260929/review_checks.py` — Reproduce offline paper-transfer checks; no search lane, network, or submission.
- `research/acc/optimality/experiments/astra_snell_smith_chain/build_report.py` — Render this bundle's deliberately simple Markdown using the standard library.
- `research/acc/optimality/experiments/astra_snell_smith_chain/p2_chain_probe.py` — Fixed follow-up: test the chain behind the actual production P2/H key.
- `research/acc/optimality/experiments/astra_snell_smith_chain/run_chain_probe.py` — Private, reproducible Snell/Smith/ordered-word diagnostic; never submits.
- `research/acc/optimality/experiments/astra_snell_smith_chain/score_kernel.c` — Read-only score probe: includes the production implementation, no beam run. define main unused_production_beam_main include "../../acc_beam.c" undef main
- `research/acc/optimality/experiments/astra_snell_smith_chain/slater_geom.py` — SCRIPT: SNELL-PEEL-01-GEOMETRY  (Slater-rule orbital geometry on the (Z,q) onion; no ionization energies used)
- `research/acc/optimality/experiments/astra_unsolved_scout/resume_wide_recovery_20260929.py` — Recover finished wide row 1, then run only the first-three-row pilot. No SAIR API calls or submissions. Run with the existing subprocess audit env.
- `research/acc/optimality/experiments/astra_unsolved_scout/scout.py` — Read-only unsolved target triage. No beam, networking or submission calls.
- `research/acc/optimality/experiments/smith_eye_probe.py` — Offline Smith-chart eye on saved AC paths, with 14-sibling ranks.
- `research/acc/optimality/find_bridges.py` — Find short AC bridges between benchmark starts: pairs (A, B) with d(start A, start B) <= R. A path for B then gives a path for A of length <= R + len(path B). Moves are invertible, so one BFS of radius R from each start,
- `research/acc/optimality/hump_features.py` — Hump features of a start presentation ("Comutators" idea, 2026-09-28).
- `research/acc/optimality/make_records.py` — Write WARROOM optimality records (one per R band) from part1.jsonl + controls.jsonl.
- `research/acc/optimality/make_sac.py` — ACC_SAC_<date>.txt: Stable AC lines that improve on what the team already holds. Sources: swap-finish paths (sac_swap.jsonl, < R+2) and exact-optimal AC paths + [16,15] (ties.jsonl, = R+2). Also rewrites the AC tie file 
- `research/acc/optimality/make_smith_variant.py` — (no header)
- `research/acc/optimality/make_ties.py` — Build ACC_TIES_<date>.txt from ties.jsonl (only official-verified paths of exactly the record length) and replay it with the official CLI.
- `research/acc/optimality/meet_chain/meet_chain.c` — meet_chain: exact meet between radius-RA balls around SOURCE states and the union of radius-RB balls around every state of a known road (TARGET chain). Any meet gives source -> chain state j; the rest of the road finishe
- `research/acc/optimality/meet_chain/meet_yx.c` — meet_chain: exact meet between radius-RA balls around SOURCE states and the union of radius-RB balls around every state of a known road (TARGET chain). Any meet gives source -> chain state j; the rest of the road finishe
- `research/acc/optimality/meet_chain/run_00764.py` — Lane A1 for J5 (Grok's lead): exact meet between balls around 00764/02598 starting points and the whole ac-00766 road.
- `research/acc/optimality/meet_chain/run_a2.py` — Lane A2 for J5: exact meet from 00764/02598 starts (both slot orders) to Grok's collapse family (Yx Y^(k-1) x Y^(k-1), x Y^k), k=4..12, every state of its finish [1,8,2,4]+[2]*(k-1), in all 16 frames.
- `research/acc/optimality/meet_chain/run_longjump.py` — Long-range shortcut probe on one held road: exact meets (radius RA+RB) from road states SRC to road states CHAIN. A meet from state i to state j with d moves saves j - i - d. usage: run_longjump.py ROW i0 i1 j0 [RA RB]
- `research/acc/optimality/meet_chain/run_yx_batch.py` — (y,x) finish hunting at scale (Moves Manual trick #4): for every row where our Stable best is 1-3 over the Stable record, take our 2 best (x,y) roads and test every state s_i for an exact route to (y,x) of <= RA+RB moves
- `research/acc/optimality/mine_macros.py` — Schur elimination of the hump, step 1: mine "excursions" (macro-moves). An excursion is a segment of a known AC path, 2..KMAX moves long, whose interior climbs above both endpoints (total relator length) and comes back d
- `research/acc/optimality/ms_archive_splice_probe.py` — Compare scored Lisitsa archive routes with Codex YXXyx routes (n=5..7).
- `research/acc/optimality/ms_archive_to_sair.py` — Price Lisitsa's MS(3..9) archive in the pinned ac-r2-v1 move graph.
- `research/acc/optimality/ms_fixed_beam_probe.py` — Bounded scored search for MS(5) with the Lisitsa second relator fixed.
- `research/acc/optimality/p2_block.inc` — ---- P2 begin ---- BEAM_P2=1: rank children by P2 (level-1 cut BEAM_P2CUT, default 8; 0 = no cut), then P1m, then the existing key (hprio when BEAM_H=1, else length, with the SHADOW/MACROS/NOISE terms). BEAM_P2=2: P2, th
- `research/acc/optimality/p2_hump_test.py` — P2 hump test (B31 hypothesis) + lead's E1 / U1 / C1 checks, 2026-09-28.
- `research/acc/optimality/pareto_height_pilot_20260928.py` — Small exact pilot for Pareto labels (moves, maximum total relator length).
- `research/acc/optimality/reverse_ceiling_probe.py` — Exact ordered-state reverse AC components under complete total-length ceilings.
- `research/acc/optimality/reverse_small_presentations.py` — Exact small-endpoint AC distances under the SAIR ac-r2-v1 move table.
- `research/acc/optimality/road_bridges.py` — Use the official training trivializations (competition/examples/training_424.json) as known roads. Every state on a training path has a known number of moves left to (x, y). A scored start within R moves of any road stat
- `research/acc/optimality/run_beam.py` — For each target row: beam+exact finish (AC and Stable AC via (y,x)), official verify, then exact window-14 shortening of the AC path; the swap-finish SAC path is shortened too by shortening its swapped AC counterpart. us
- `research/acc/optimality/run_beam_abc.py` — Codex ABC bounded unsolved screen: configurable UNSOLVED_W, no window pass on first solution.\n\nFor each target row: beam+exact finish (AC and Stable AC via (y,x)), official verify, then exact window-14 shortening of th
- `research/acc/optimality/run_beam_raw.py` — run_beam.py without the official-verifier import: beam + exact finish, then window-14 shortening. Paths are saved raw ("checked": false). Check them later with `tools/acc/sair_api.py plan` (official verifier) before any 
- `research/acc/optimality/run_beam_raw_dualB_timeout.py` — run_beam.py without the official-verifier import: beam + exact finish, then window-14 shortening. Paths are saved raw ("checked": false). Check them later with `tools/acc/sair_api.py plan` (official verifier) before any 
- `research/acc/optimality/run_capped_sweep.py` — Exact capped sweep over a list of rows: for each row, run acc_capped with rising total-length caps (start length upward, until the state budget stops a cap before depth MAXD) and depth MAXD = max(AC record - 9, SAC recor
- `research/acc/optimality/run_meet.py` — Driver: run acc_opt meet for rows, parse results, replay any path with the official verifier core. usage: run_meet.py BIN SAIR TFILE B WORKDIR OUTJSONL row:a [row:a ...]
- `research/acc/optimality/run_sac_swap.py` — Stable AC via the swapped finish. For row s with exact AC distance R (proved), test whether (y,x) is reachable in <= R-1 AC moves, using T_9 around (x,y) and the generator swap sigma (x<->y): d(s,(y,x)) = d(sigma s,(x,y)
- `research/acc/optimality/run_window.py` — Driver for acc_window: run a row's path, replay every PATH/FINALPATH with official core.verify. usage: run_window.py BIN SAIR WORKDIR OUTJSONL row=[moves]json ...
- `research/acc/optimality/runs/2026-09-27/scripts/autobackup.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/autobackup2.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/cap.sh` — usage: cap.sh ROW RECORD "caps..."   exact capped BFS (depth RECORD-9) + T9 finish, one cap at a time
- `research/acc/optimality/runs/2026-09-27/scripts/cap00043.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/cap00043b.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/cap00043c.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/cap00104.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/cap35.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/capgen.sh` — usage: capgen.sh ID RECORD "caps..."   exact capped search for AC paths <= RECORD (MAXD = RECORD-9)
- `research/acc/optimality/runs/2026-09-27/scripts/capped_near.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_78.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_behind.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_behind_H.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_cap43b.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_cap43c.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen12.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen13.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen14.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen2.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen3.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen4.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen5.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen6.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen7.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen8.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_capgen9.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_live2.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_memcon.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_near.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_splice.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_splice_h.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_unsolved.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_unsolved2.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_wide.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_wide2.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_wide5.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/chain_wide6.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver2.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver3.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver4.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_k1.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_live1.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_live2.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_sac.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_sac_rev.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_unsolved.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_wide.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_wide2.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_wide3.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_wide4.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_wide5.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_wide6.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_wide7.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_wide8.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/driver_wide9.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/emit.sh` — usage: emit.sh ID "ac sac" MSG
- `research/acc/optimality/runs/2026-09-27/scripts/emitH.sh` — usage: emitH.sh ID   (emit AC/SAC lines for ac-ID from any beam_*.jsonl result (first TIE/BEAT) via emitcap.sh)
- `research/acc/optimality/runs/2026-09-27/scripts/emitcap.sh` — usage: emitcap.sh ID "ac moves space-separated" ["sac moves space-separated"] keep the shorter of the searched SAC path and AC+[16,15]
- `research/acc/optimality/runs/2026-09-27/scripts/htest.sh` — compare plain length key vs ACSolverX priority on memcon rows
- `research/acc/optimality/runs/2026-09-27/scripts/hunt.sh` — usage: hunt.sh WORKER ROW RECORD   loops seeded H-beam restarts on one row until stopped results: work/hunt_ROW_WORKER_SEED.jsonl, one line per run in work/hunt_ROW_summary.log
- `research/acc/optimality/runs/2026-09-27/scripts/launch_live1.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/looktest.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/mkbundle.py` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/mon_k1.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/mon_sac.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/novtest.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/queue2.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/queue3.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/queue_sac.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/run_live.sh` — usage: run_live.sh NAME   (targets in work/NAME_targets.json, results in work/beam_NAME.jsonl)
- `research/acc/optimality/runs/2026-09-27/scripts/run_live_seed.sh` — usage: run_live.sh NAME   (targets in work/NAME_targets.json, results in work/beam_NAME.jsonl)
- `research/acc/optimality/runs/2026-09-27/scripts/runshort.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/seedsplice.sh` — seed each row's pool with a BEAM_H=1 div=1.0 path, then splice with BEAM_H=1
- `research/acc/optimality/runs/2026-09-27/scripts/stop_after_02217.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/tail313.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/tail37.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/tail_ac-00034.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/tail_ac-00170.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/tail_ac-00267.sh` — (no header)
- `research/acc/optimality/runs/2026-09-27/scripts/watchdog.sh` — kill any acc_beam running longer than 45 min (2700 s) so one hard row can't stall the queue
- `research/acc/optimality/runs/2026-09-27/scripts/yx15.sh` — (no header)
- `research/acc/optimality/sac_rank3.c` — Exact Stable AC (sac-r8-v1) meet restricted to rank <= MAXR, mirroring stable_core.py. Forward BFS from the start (radius A), backward BFS from the empty presentation (radius B) using exact predecessors (the graph is dir
- `research/acc/optimality/score_zoo.py` — Score zoo: a fast screen of cheap state scores against record-length AC paths, 2026-09-28.
- `research/acc/optimality/shadow_bounds.py` — Homomorphic shadows of the AC graph: certified lower bounds on AC distance.
- `research/acc/optimality/shadow_probe_export.py` — Export SL(2,p) shadow probes for acc_beam (BEAM_SHADOW / BEAM_SHADOW_FILE). Binary layout (little-endian): b'SHDW', uint32 K; then per probe: uint32 n, uint16 one, uint16 img[4] (images of the letter codes 0=x, 1=x^-1, 2
- `research/acc/optimality/smith_snell_probe.py` — Exploratory Smith-coordinate and Snell-style routing tests on AC paths.
- `research/acc/optimality/smith_trial.py` — (no header)
- `research/acc/optimality/supermove/compile_direct.py` — Compile an smbeam supermove road into official ac-r2-v1 moves directly: for each step, cyclically reduce both relators by conjugation, find the substitution (x <- rot(x)*rot(y^s)) that reaches the next class, realize the
- `research/acc/optimality/supermove/compile_exact.py` — Replay an smbeam2 actual-state road as official ac-r2-v1 moves (rotations by single conjugations, one multiplication, cyclic reduction), finish to (x,y) by BFS, verify with the official core. usage: compile_exact.py ROW 
- `research/acc/optimality/supermove/compile_road.py` — Compile an smbeam class road into official ac-r2-v1 moves with Git's road-keeping DP, verify with the official core, then window-shorten (acc_window). usage: compile_road.py ROW ROADFILE
- `research/acc/optimality/supermove/skel_dp_local.py` — tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_SKELETON_DP  Keep a path's road (its sequence of conjugacy-class states: each relator up to rotation, conjugation and inversion; the pair 
- `research/acc/optimality/supermove/sm_lane.py` — Solve-first lane: supermove class beam (smbeam) -> direct compile to official moves -> official verify. Routes go to OUT (jsonl) with the raw path; shortening runs separately. usage: sm_lane.py TARGETS OUT W DMAX LCAP TM
- `research/acc/optimality/supermove/smbeam.c` — Supermove (substitution) beam search in conjugacy-class space, after ACSolverX (MIT, Math & AI Lab at Caltech, 6a12515). State: two cyclically reduced words, each canonical up to rotation and inversion; the pair is unord
- `research/acc/optimality/supermove/smbeam2.c` — Cost-aware supermove beam (after ACSolverX s_move, MIT, Math & AI Lab at Caltech, 6a12515). State: the ACTUAL relators r0, r1 (cyclically reduced, specific rotation) plus g = official ac-r2-v1 moves spent so far. Supermo
- `research/acc/optimality/tail_replace.py` — Long-window tail replacement: for each state s_i on a path, exact capped search from s_i to (x,y) (capped BFS prefix + exact uncapped T_9 finish). If found length d < n-i, splice. Repeats until no gain. usage: tail_repla
- `research/acc/optimality/validate_kernel.py` — Validate acc_opt's C kernel against the official core.apply_move on N random (state, move) pairs.
- `research/acc/optimality/validate_sac.py` — Validate sac_rank3 apply against official stable_core.apply_move on N random (state, move) pairs, ranks 0..8.
- `research/acc/optimality/yxxyx_chain.py` — Construct ordinary AC certificates for the YXXyx Miller–Schupp chain.

## tools/acc/acc_toolkit.py

- `tools/acc/acc_toolkit.py` — Mad Hatters ACC toolkit for Gemini/Colab — pure Python, no dependencies.

## tools/acc/ak3_p_to_ak3_replay.py

- `tools/acc/ak3_p_to_ak3_replay.py` — Independently replay the 53 h_i transformations from Shehper et al.

## tools/acc/bs_family_transfer.py

- `tools/acc/bs_family_transfer.py` — BS-family transfer (x^-1 y^n x = y^(n+1), n=2,3,4): the same second relator is solved at one n and unsolved at another. Replay our path for the solved partner on the unsolved row, take the shortest prefix states, and sea

## tools/acc/build_T9.sh

- `tools/acc/build_T9.sh` — usr/bin/env bash Rebuild the T_9 lookup table (every presentation within 9 official moves of (x,y), with its distance). Output: T9.tab, 4,480,000,000 bytes (280,000,000 slots x 16 bytes), 214,977,551 states. Expected SHA

## tools/acc/build_record.py

- `tools/acc/build_record.py` — Build the ACC Field Record page from research/acc/live/record/{template.html,ideas.json,paths.json} and the score history in research/acc/live/dashboard.json. usage: build_record.py OUT.html

## tools/acc/build_xecho.py

- `tools/acc/build_xecho.py` — Cross-row echo table for acc_capped (ECHO_FILE): every state on every known AC road of every row, plus the SAIR training roads, under all 16 mirrors (signed letter permutations x word switch), optionally with states IRAD

## tools/acc/cap_words.sh

- `tools/acc/cap_words.sh` — exact capped search from arbitrary words: cap_words.sh R0 R1 CAP MAXD [BUDGET]

## tools/acc/capgen.sh

- `tools/acc/capgen.sh` — usage: capgen.sh ID RECORD "caps..."   exact capped search for AC paths <= RECORD (MAXD = RECORD-9)

## tools/acc/charlie

- `tools/acc/charlie/charlie_run.py` — SCRIPT: CHARLIE_RUN -- one row through acc_disk, two-sided, verified by the official verifier. Usage: python3 charlie_run.py ROW_ID CAP [--meet-cap C] [--mem MB] [--work DIR] [--maxlayer N] [--below T] Start side: exact 
- `tools/acc/charlie/cores.py` — SCRIPT: CHARLIE_CORES -- apply the cheapest big cut to every pool row; group rows by the reduced core (cyclic words up to rotation, relator inversion, relator swap, and the 8 letter automorphisms)
- `tools/acc/charlie/cutchain.py` — SCRIPT: CHARLIE_CUTCHAIN -- the rotate-and-cut pattern repeated, then a lookup in T16. For each pool row: apply the cheapest cut that lowers the total, repeat while it keeps lowering; after every step look the exact stat
- `tools/acc/charlie/cutfirst.py` — SCRIPT: CHARLIE_CUTFIRST -- the rotate-and-cut pattern, used as a presolve for acc_disk. Pattern (from the ac-03719 tie): when one relator contains a rotated copy of the other (or of its inverse), a few rotations (length
- `tools/acc/charlie/ledger_run.py` — SCRIPT: CHARLIE_LEDGER_RUN -- finish the board's stalled exact capped runs with acc_disk. For a row with board record R under cap K (from ledger/exact_capped_runs.jsonl): forward: exact frontier BFS from the row under to
- `tools/acc/charlie/ref_bfs.py` — SCRIPT: ACC_REF_BFS -- plain in-memory BFS with the official kernel, for controls
- `tools/acc/charlie/rows.py` — SCRIPT: ACC_ROWS -- official initial relators for a challenge id, as acc_disk state strings
- `tools/acc/charlie/sac_yx.py` — SCRIPT: CHARLIE_SAC_YX -- exact shortest route to the Stable finish (y,x) for a row, then two destabilizes. Stable AC ends at the empty presentation; from ((x),(y)) OR ((y),(x)) two destabilize moves finish it (at ((y),(
- `tools/acc/charlie/twins.py` — SCRIPT: CHARLIE_TWINS -- carry a verified path to every pool row that is an exact image of its row under a letter automorphism (signed permutation of x, y: 8 maps) and/or relator swap (x2). The moves transform exactly: s
- `tools/acc/charlie/xcheck_moves.py` — SCRIPT: ACC_DISK_XCHECK_MOVES -- every move of acc_disk against official verifier/core.py apply_move

## tools/acc/colab

- `tools/acc/colab/colab_j12_gpt_reverse_tube.py` — usr/bin/env python3 include <bits/stdc++.h>
- `tools/acc/colab/colab_j12_rival.py` — J12 (Mad Hatters ACC): rival-rows search for Colab. Self-contained: clones the official SAIR repo at the pinned commit, compiles our engines, builds the T8 finish table, runs a dual-P2 beam (3 orientations) and an exact 
- `tools/acc/colab/j12_body.py` — ---- J12 body (sources and targets are embedded above by make_j12.py) ----
- `tools/acc/colab/make_j12.py` — Build the self-contained Colab bundle colab_j12_rival.py: embeds our C engines (acc_opt, acc_beam with P2/dual, acc_window, acc_capped) and the target list (records from the latest board snapshot). usage: make_j12.py OUT

## tools/acc/colab_acc_search.py

- `tools/acc/colab_acc_search.py` — Mad Hatters ACC search bundle for Colab / any Linux box (self-contained).

## tools/acc/cross_lineage.py

- `tools/acc/cross_lineage.py` — SONG9 (session 1): exact all-pairs lineage crossing. For one row, take every distinct verified road (session 1 seeds + pool). Fwd ball: from state i of road A, all states within R moves -> best i+d. Bwd ball: from state 

## tools/acc/crossrow.py

- `tools/acc/crossrow.py` — Cross-row lookup with mirror twins.

## tools/acc/dashboard

- `tools/acc/dashboard/build_results.py` — Results data for the idea/results map: every line accepted since the session start, its value then and now, the method that found it, and the score history. Writes tools/acc/dashboard/results_data.json.
- `tools/acc/dashboard/build_results_map.sh` — Rebuild the results map: fresh dashboard data -> results_data.json -> results_map.html (publish this file).

## tools/acc/dashboard_data.py

- `tools/acc/dashboard_data.py` — Build the ACC dashboard data (one JSON object per dashboard doc) from local files only; no API calls.

## tools/acc/exact_ledger.py

- `tools/acc/exact_ledger.py` — Turn capgen.sh logs into one ledger line per exact capped run.

## tools/acc/family_transfer.py

- `tools/acc/family_transfer.py` — Family transfer for tied/untied rows in MS families: replay our path for a same-family neighbour (n-1 or n+1) on the target row, take the 2 shortest prefix states as seeds, and beam from them (plus the start) to record+2

## tools/acc/fast_sweep.py

- `tools/acc/fast_sweep.py` — Fast sweep of every solved AC row against the live board.

## tools/acc/firstsolve.py

- `tools/acc/firstsolve.py` — First solves on unsolved MS rows: replay our path for the solved MS(n-1,w) on MS(n,w), pick prefix states where the pair is shortest, and run deep beams from them (any length scores). Plain deep beam from the start is th

## tools/acc/firstsolve_twins.py

- `tools/acc/firstsolve_twins.py` — Opposite approach for first solves: deep two-eyes beams from the three twins of each unsolved row (relators swapped, x<->y, letters inverted); paths mapped back by exact move permutations and replayed with the official c

## tools/acc/idea_cycler.py

- `tools/acc/idea_cycler.py` — Idea cycler: for each target row, try a fixed list of beam ideas (each paired with its opposite) on the row and on its symmetric twins, until one reaches the record. Every attempt is logged, so no (row, idea, variant) re

## tools/acc/inbox_watch.sh

- `tools/acc/inbox_watch.sh` — SCRIPT: TEAM_INBOX_WATCH  team standard (owner, 2026-09-30): every member watches for messages addressed to them. Usage: bash tools/acc/inbox_watch.sh NAME   (git, upgh, astra, kernel, bob, charlie, session2, luna, fable

## tools/acc/jev_handoff

- `tools/acc/jev_handoff/acc_toolkit.py` — Mad Hatters ACC toolkit for Gemini/Colab — pure Python, no dependencies.
- `tools/acc/jev_handoff/colab_acc_search.py` — Mad Hatters ACC search bundle for Colab / any Linux box (self-contained).
- `tools/acc/jev_handoff/coverage_run.py` — Mad Hatters ACC coverage run (UPG-H, 6 Oct): first team roads AT the record on rows held by a single team where we have no accepted line. Beam (W 100k) + exact finish table T8 + exact window shortening + Stable via (y,x)
- `tools/acc/jev_handoff/src/acc_batch.c` — Batch meet: load T_B once, then for each start line "tag l0 w.. l1 w.." compute min dS+dT over S_A ∩ T_B (exact distance if <= A+B), rebuild and print the path. Same kernel/fingerprint/table as acc_opt.c (included verbat
- `tools/acc/jev_handoff/src/acc_beam.c` — Beam search + exact finish. Forward beam from the start keeps the W states of smallest total relator length per depth (ties broken by fingerprint), deduplicated across all depths. Every generated state is looked up in T_
- `tools/acc/jev_handoff/src/acc_capped.c` — Capped exhaustive BFS + exact finish: BFS from the start over states with total relator length <= CAP (uncapped T_9 lookups on every state). The first depth d at which min(d + dT) can no longer improve gives the shortest
- `tools/acc/jev_handoff/src/acc_opt.c` — ACC exact-optimality meet engine, ac-r2-v1 (SAIR Andrews-Curtis commit a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e, competition/tools/verifier/core.py, 14 moves). NO LENGTH CAP. Letters: 0=x 1=x^-1 2=y 3=y^-1 (inverse = c^1
- `tools/acc/jev_handoff/src/acc_window.c` — ACC exact window shortening, ac-r2-v1 (SAIR a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e). Kernel, fingerprint and table are shared verbatim with acc_opt.c (included). For path states s_0..s_n: for every pair i<j with j-i <=
- `tools/acc/jev_handoff/src/capgen.sh` — Exact capped search: finds every AC path <= RECORD whose first RECORD-9 moves keep total relator length <= CAP, finishing exactly through the T table. A clean run at a cap is a PROOF of "none within that cap". usage: cap
- `tools/acc/jev_handoff/src/run_beam.py` — For each target row: beam+exact finish (AC and Stable AC via (y,x)), official verify, then exact window-14 shortening of the AC path; the swap-finish SAC path is shortened too by shortening its swapped AC counterpart. us

## tools/acc/job_runner.sh

- `tools/acc/job_runner.sh` — Starts the next queued job whenever fewer than 4 heavy jobs run and disk has > 5 GB. Log: work/jobqueue.log

## tools/acc/make_T9_zip.sh

- `tools/acc/make_T9_zip.sh` — usr/bin/env bash Package the T_9 lookup table as one zip cut into decimal 29 MB pieces. usage: bash tools/acc/make_T9_zip.sh PATH/TO/T9.tab [OUTDIR] no T9.tab yet? build it first: bash tools/acc/build_T9.sh work Output i

## tools/acc/ms_exact.py

- `tools/acc/ms_exact.py` — Exact shortest AC path for a custom MS(n,w) start via acc_capped (cap, MAXD). usage: ms_exact.py WORD N CAP MAXD

## tools/acc/ms_hop.py

- `tools/acc/ms_hop.py` — Exact shortest route between two given states (meet in the middle, length cap). usage: ms_hop.py R0 R1 T0 T1 FWD BWD CAP

## tools/acc/ms_lisitsa_replay.py

- `tools/acc/ms_lisitsa_replay.py` — Audit Lisitsa's MS(3)..MS(9) fixed-second-relator sequences.

## tools/acc/ms_pump

- `tools/acc/ms_pump/bidi.py` — Balanced exact bidirectional search for the r1-only pump on MS(n, YXYXyx) rows (UPG-H 21:03Z job; song line "The echo from the back is still talking to you"). r0 = YXYXyx fixed; r1-only moves {1,4,5,10..13}, invertible u
- `tools/acc/ms_pump/bidi_all.py` — Exact balanced bidirectional search over ALL 14 moves (each has an inverse: 0,1 self; 2<->3; 4<->5; 6<->7; 8<->9; 10<->11; 12<->13). State = (r0, r1) freely reduced; cap = total relator length. Forward from START, backwa
- `tools/acc/ms_pump/common.py` — (no header)

## tools/acc/mstrace.py

- `tools/acc/mstrace.py` — (no header)

## tools/acc/ops

- `tools/acc/ops/auto_splice_loop.py` — Every 15 min: (1) junction splice over the whole route pool (junction_splice.py, R=2); (2) yx_mid on every row where we hold an AC path at the record (or 1 over) and the Stable record = AC record + 1, not yet run and not
- `tools/acc/ops/beam_list.sh` — usage: beam_list.sh NAME W   H-beam (+window) over $S/work/NAME_targets.json ('record' = length to reach) -> $S/work/NAME_cap.jsonl (named *_cap.jsonl so watch_sweeps.py sees hits: ac_len <= ac_record).
- `tools/acc/ops/commute_clean.py` — Commuting-pair cleanup (UPG-H song-4 rule, own implementation): a move m and a later inverse(m) cancel when every move between them commutes with m (neither writes a relator the other reads or writes). Repeats until no p
- `tools/acc/ops/compare_boards.py` — env CB_CLEAN=1: apply the commuting-pair cleanup (commute_clean.py) to every route first. Song 2 (session 2): 'a second body started ticking against mine ... we compared'. Every route the team holds (UPG-H ledger, repo p
- `tools/acc/ops/fixpoint_shorten.py` — Fixpoint shortener (session 2): commute_clean (tools/acc/ops/commute_clean.py) + acc_window (window-14), repeated until neither shortens. It took the step-2 BS roads ac-05698 128 -> 110 (BEAT 111) and ac-06792 137 -> 119
- `tools/acc/ops/free_ties.py` — Find scoring lines we already hold paths for but never sent: AC paths at or under the live AC record, and SAC lines = AC path + [15,15] (or a stored SAC path) at or under the live SAC record. Writes candidate lines to OU
- `tools/acc/ops/junction_splice.py` — Junction splice over every route the team holds, toward both targets. For each row, pool all verified routes from the start: AC paths (end (x,y)) and Stable routes (end (y,x), i.e. Stable lines minus a trailing [15,15]).
- `tools/acc/ops/k12_targets.py` — Offline target list: every row whose record is held by 1 or 2 teams (AC and Stable), joined with what we hold.
- `tools/acc/ops/mid_restart.py` — Restart the beam from every state along our best path of a row; report prefix + new finish when it beats the path. usage: python3 tools/acc/ops/mid_restart.py ROW TARGET_LEN [W] [CUTS] (env BEAM_* passed to the beam; BIN
- `tools/acc/ops/mid_route.py` — Restart an AC beam at a selected prefix and target either (x,y) or (y,x).
- `tools/acc/ops/near_escalate.py` — Automatic 'opposite approach' on near misses: every lane result that is exactly 1 over a record held by 1-2 teams (AC or SAC) gets, once each: the mirror-twin beam (AC), and the two (y,x)-aimed beams (SAC: TWIN_MODE=yx, 
- `tools/acc/ops/p2_list.sh` — usage: p2_list.sh NAME W   P2 beam (BEAM_P2=2: P2 lookahead, then H priority) + window-14 over $S/work/NAME_targets.json -> $S/work/NAME_cap.jsonl (watch_sweeps.py sees hits: ac_len <= ac_record or sac_len <= sac_record)
- `tools/acc/ops/pull_and_send.sh` — Owner's 06:50Z 09-30 rule: pull boards with every 30-min pull, and send verified lines as soon as they are ready. One run = pull_recent (1 API call) + board snapshots (2 calls) + offline rebuilds + (if the newest ready f
- `tools/acc/ops/pull_recent.py` — 30-minute submission tracker (ONE SAIR API call per run).
- `tools/acc/ops/song_climb.py` — Song experiment (session 2): 'the shine goes up before it goes down / bump before the ground'. ac-09400 (record 35): Charlie certified no path <= 35 with relator-total peak <= 34. So climb first: every distinct state 1..
- `tools/acc/ops/splice_stable_twin_bridges.py` — Join two independent Stable AC roads with zero to three AC moves.
- `tools/acc/ops/stable_finish_watch.py` — Check a beam JSONL for scoreable Stable AC finishes of its AC paths.
- `tools/acc/ops/sweep.sh` — usage: sweep.sh NAME BUDGET JUMP [VLIMIT_KB]   targets: $S/work/NAME_targets.json -> $S/work/NAME_cap.jsonl/.log Durable copy: research/acc/live/sweeps/NAME_cap.jsonl (the board watcher syncs it every 30 min).
- `tools/acc/ops/target_rank.py` — One ranked target list for all rows: expected points per unit of search time. score = value * p(gap) * p(len), where value = 2^-k for the AC tie we do not hold + 2^-k for the SAC tie we do not hold (a beat would be 1.0 e
- `tools/acc/ops/twin_beam.py` — Opposite-orientation beam: run the beam on the exact mirror twin of a row (swap letters x<->y AND swap the two relators; this symmetry fixes the target (x,y)), then map the path back move by move and replay it on the ori
- `tools/acc/ops/twin_list.sh` — Run twin_beam.py over a target list, resumable. usage: bash tools/acc/ops/twin_list.sh LIST.json OUT.jsonl MODE [W] MODE: mirror (AC; swap letters and relators) | yx (SAC, letter swap) | yx2 (SAC, relator swap) Needs ACC
- `tools/acc/ops/unsolved_ms_targets.py` — Targets for an unsolved-MS lane: rows unsolved by every team whose MS(n,w) family has a solved n. Ordered by distance to the nearest solved n, then that solved record. AK(3)-class rows are skipped (open problems). usage:
- `tools/acc/ops/watch_board.sh` — Every 30 min: pull live boards (4 API reads), log changes, and copy sweep progress into the repo (durable across restarts). Exit to wake the lead on "LOST OUR TIE" or a newly solved row.
- `tools/acc/ops/watch_inbox.sh` — Wake the lead when a session pushes a new inbox or exchange file (or a non-API ACC_SUBMIT_* file). Private ref only.
- `tools/acc/ops/watch_sweeps.py` — Exit (and print) when any sweep result ties or beats its target record and is not yet handled. Sweeps: $S/work/NAME_cap.jsonl with targets $S/work/NAME_targets.json. Handled rows: research/acc/live/sweeps/handled.txt (du
- `tools/acc/ops/yx_mid.py` — (y,x) mid-restart: from every state s_i of a given AC path of a row, beam the letter-swapped state (x<->y) toward (x,y) with DMAX = TARGET - i, map the tail back (conjugations by x and y trade places), and keep prefix + 
- `tools/acc/ops/yx_window.py` — Window-14 shortening (acc_window, exact for windows <= 14) of a (y,x) route, run in the letter-swapped twin space where the route ends at (x,y). usage: python3 tools/acc/ops/yx_window.py ROW '[route to (y,x), AC moves]' 

## tools/acc/overlap_splice.py

- `tools/acc/overlap_splice.py` — "Two paths in the dark ... what they saw was the overlap": for each row with >= 2 distinct AC paths, splice prefix(A up to state a) + connector(a -> b, exact, <= R moves) + suffix(B from state b). Official core replay.

## tools/acc/path_memory.py

- `tools/acc/path_memory.py` — Build path memory: one quick BEAM_H beam per AC row (no depth cap tied to the record), keep every path that reaches (x,y), even if longer than the record. The states on these paths are what the cross-row lookup (crossrow

## tools/acc/plan_offline.py

- `tools/acc/plan_offline.py` — Offline version of `sair_api.py plan` for a session with no SAIR network access. Uses the newest pulled boards and mine_*.json in research/acc/live, plus the official verifier. usage: plan_offline.py FILE... --sair DIR -

## tools/acc/pool_roads.py

- `tools/acc/pool_roads.py` — Pool every verified AC road we hold into one jsonl ({"id","ac"}), keeping distinct roads per row. Sources: ac- lines and {"id","ac"} records in tracked repo files, the graph-map archive, route maps, and any extra jsonl/t

## tools/acc/refresh_live.py

- `tools/acc/refresh_live.py` — (no header)

## tools/acc/restart_all.sh

- `tools/acc/restart_all.sh` — Relaunch every standing lane; each runs under its own flock, so a lane that is already running is not duplicated.

## tools/acc/rotcomp.py

- `tools/acc/rotcomp.py` — Rotation compressor (Smith-chart 'shortest arc'): between two moves that read or change relator i, the pure rotations of r_i (length-preserving conjugations) only matter through their net cyclic shift. Replace each such 

## tools/acc/sac_fast_peel.py

- `tools/acc/sac_fast_peel.py` — Stable AC fast peel: finish (x, y X^m) -> empty presentation in about 2k + 3m/k moves instead of m + 2.

## tools/acc/sac_ms_bs.py

- `tools/acc/sac_ms_bs.py` — Stable AC (sac-r8-v1) generator for MS(n, BS) = (YXXyx, Y^(n+1) X y^n x), any n >= 2.

## tools/acc/sac_rank_probe.sh

- `tools/acc/sac_rank_probe.sh` — Exact rank-2 Stable AC check: is there an AC-move path to (x,y) or (y,x), then the 2-move finish, of length <= SAC record? usage: sac_rank_probe.sh ID SACREC   (cap 400 = effectively uncapped at these depths)

## tools/acc/sair_api.py

- `tools/acc/sair_api.py` — Mad Hatters client for the SAIR Andrews-Curtis Challenge API (standard library only).

## tools/acc/scratch_utils

- `tools/acc/scratch_utils/acmoves.py` — Official ac-r2-v1 moves on letter strings (x,X,y,Y), free reduction only.
- `tools/acc/scratch_utils/lisitsa_find.py` — Find competition rows AC-equivalent-by-symmetry to Lisitsa MS_n(w*) = (X y^n x Y^(n+1), XYxyX)
- `tools/acc/scratch_utils/value.py` — (no header)

## tools/acc/session1_lost_audit.py

- `tools/acc/session1_lost_audit.py` — Lost-submission audit (session 1 method, Moves Manual 2.3). Plain script, no model, no API. Harvests every `s?ac-NNNNN: [...]` line (and {"id","ac","sac"} jsonl records) under research/acc plus any extra dirs given, keep

## tools/acc/skel_yrun.py

- `tools/acc/skel_yrun.py` — Skeleton transfer restricted to Fable's 128 unsolved y-run MS rows (UPG-H assignment 19:03Z, UPDATE_upgh_to_all_20260930T1903Z.md). Targets: research/acc/live/sweeps/fable/zoom_20260930T1858Z.json 'soft_unsolved_yrun_row

## tools/acc/skeleton_transfer.py

- `tools/acc/skeleton_transfer.py` — Skeleton-family transfer (after Viaclovsky 2609.33785 §6.3: vary a parameter, keep the combinatorial type). Rows with the same syllable skeleton (letter pattern, exponents abstracted) form a family. For each unsolved row

## tools/acc/smith_read.py

- `tools/acc/smith_read.py` — Smith-chart reading of an AC path: each move is ROT (conjugation, length unchanged), CUT (length down), CLIMB (length up), or INV. Also the 'phase table' of a state: for every rotation of each relator (and inverse), how 

## tools/acc/sol61

- `tools/acc/sol61/check_bounded_search.py` — Synthetic bounded-search correctness experiment; no competition rows.
- `tools/acc/sol61/check_moves.py` — Differential check of the independent C++ move implementation on synthetic states.
- `tools/acc/sol61/run_control.py` — Rediscover only ac-09409 from the exact pinned manifest, then verify locally.

## tools/acc/song12

- `tools/acc/song12/links.py` — (no header)
- `tools/acc/song12/roadset.py` — SONG12 (session 1): every state on every known road (plus 8 symmetric images) -> sorted acc_disk .set. A forward BFS from an open row with --meet on this set finds a state that some known road passes through, which links

## tools/acc/splice

- `tools/acc/splice/splice.py` — Path pool + splicing + waypoint restarts for one AC row.

## tools/acc/subst_solver.py

- `tools/acc/subst_solver.py` — Relator-substitution (Dehn-style) solver for first solves.

## tools/acc/upgh

- `tools/acc/upgh/adapters/splice_rows.py` — UPG-H adapter: join saved roads (cross-road splice) with tools/acc/splice/splice.py.
- `tools/acc/upgh/adapters/tail_replace_rows.py` — UPG-H adapter: run research/acc/optimality/tail_replace.py on each row of jobs.json and write harvestable JSON lines {"row": ..., "final_path": [...], "start_len": n}.
- `tools/acc/upgh/adapters/yx_rows.py` — UPG-H adapter: Stable AC through the (y,x) orientation.
- `tools/acc/upgh/autopilot.py` — Autopilot: the team's cheapest scorers, run unattended on the owner's PC (no model, no API calls, no ledger writes).
- `tools/acc/upgh/bridge_library.py` — Bridge library: every time one of our roads got shorter, the improvement replaced a middle segment X by a shorter Y (old and new road share a prefix and a suffix). Collect every such (X, Y) pair from the ledger's path.be
- `tools/acc/upgh/bs_doubling.py` — Baumslag-Solitar doubling roads for MS(n, w*), w* = y^-1 x y x^-1 (r1 = x x Y X y).
- `tools/acc/upgh/bs_doubling2.py` — Step-2 Baumslag-Solitar doubling roads: MS(n, w) with r1 = x x Y Y X y y (y^-2 x y^2 = x^2), even n = 2L.
- `tools/acc/upgh/checker.py` — Exact evidence: pinned official verifier, plus the independent kernel as a second witness.
- `tools/acc/upgh/collapse_scan.py` — Collapse-ridge scan (Grok's idea 2, 1 Oct): the pair C_k = (Y x Y^(k-1) x Y^(k-1), x Y^k) reaches ((x),(y)) in exactly k+3 moves, [1, 8, 2, 4] + [2]*(k-1) (ac-00766 steps 25-34 are k=6). For k >= 7 that finish is longer 
- `tools/acc/upgh/commit_state.sh` — usr/bin/env bash Commit and push the harness state (ledger, artifacts, plans, queue, WORKING_upgh.md) to the current branch. Serialised with flock so lanes, the cycle loop and a person never collide. In an ephemeral cont
- `tools/acc/upgh/comms.py` — Team comms sweep for the UPG-H lead: what changed in the repo's message spots since the last sweep.
- `tools/acc/upgh/cov_transfer.py` — Change-of-variables (automorphism) transfer web. For rows A, B whose starts have the same Whitehead-minimal form (up to the 8 letter maps, relator swap, cyclic rotation and inversion), B ~ psi(A) for an automorphism psi 
- `tools/acc/upgh/diagnostics.py` — Finite matrix diagnostics from the papers. Optional. Never a scheduling gate.
- `tools/acc/upgh/fable_build.py` — FABLE first-road builder for the Miller-Schupp / Baumslag-Solitar rows where the ACC-P000013 condition (T) fails.
- `tools/acc/upgh/foreign_meet.py` — Foreign meeting: a state on our road for row A may equal, up to the 16 symmetries and per-relator rotation/inversion, a state on a road the team holds for a DIFFERENT row B. From there B's remaining suffix, relabelled by
- `tools/acc/upgh/harness.py` — UPG-H v2 controller. Code decides dispatch; models advise; the pinned verifier certifies.
- `tools/acc/upgh/harvest.py` — Find every move path already sitting in files, so none stays unwritten (S4).
- `tools/acc/upgh/harvest_zip.py` — Pull every road and every finished (COMPLETE) miss out of a team results zip or folder, e.g. the Colab ACC_SPLIT30_RESULTS_20261004.zip, without unpacking it to disk. Runs on the owner's PC; no model, no API.
- `tools/acc/upgh/height_web.py` — Height web: one global height map (exact distance to the goal) over every road the team holds, on every row, under the 16 symmetries, with 1-move junction edges, and optional 2-move junctions. Each row's best road in the
- `tools/acc/upgh/kernel.py` — Independent replay of the frozen SAIR move specs (ac-r2-v1 and sac-r8-v1).
- `tools/acc/upgh/ladder_law.py` — Ladder law (VOTKP "column rhythm" test on Miller-Schupp ladders). Every scored row with a relator X y^n x Y^(n+1) (up to the 8 letter maps, rotation, inversion) is put on a ladder keyed by its OTHER relator (same map). A
- `tools/acc/upgh/lanes.sh` — usr/bin/env bash Run N parallel code-runner lanes. Each task runs in a fresh process, so code fixes apply from the next task on. A lane ends when nothing is runnable or the harness is stopped. T9 is mmap-shared. usage: b
- `tools/acc/upgh/leader_patterns.py` — Leader patterns: attribute board changes to the top teams from saved snapshots, then profile them (0 API calls).
- `tools/acc/upgh/ledger.py` — Z, the ledger register: an append-only, hash-chained JSON Lines file.
- `tools/acc/upgh/lineage/astra_v1/__init__.py` — ACC Memory-First Harness: orchestration, not a search solver.
- `tools/acc/upgh/lineage/astra_v1/demo.py` — Exercise the complete controller with labelled toy workers and checker.
- `tools/acc/upgh/lineage/astra_v1/gates.py` — Exact-artifact gates for an externally supplied, pinned ACC checker.
- `tools/acc/upgh/lineage/astra_v1/geometry.py` — Optional finite matrix diagnostics. These never certify or prune ACC states.
- `tools/acc/upgh/lineage/astra_v1/harness.py` — Offline agent orchestration. Commands are configured clients, never model output.
- `tools/acc/upgh/lineage/astra_v1/runtime.py` — Small durable task kernel and bounded JSON subprocess transport.
- `tools/acc/upgh/lineage/astra_v1/selftest.py` — Run local fault tests. These do not call a model or validate real ACC routes.
- `tools/acc/upgh/lineage/astra_v1/tests/test_gates.py` — Gate integration tests using a TOY receipt producer, NOT an ACC checker.
- `tools/acc/upgh/lineage/astra_v1/tests/test_geometry.py` — (no header)
- `tools/acc/upgh/lineage/astra_v1/tests/test_runtime.py` — Kernel regressions: durable evidence, fencing, stop, and bounded execution.
- `tools/acc/upgh/lineage/astra_v1/tests/test_workflow.py` — (no header)
- `tools/acc/upgh/lineage/astra_v1/workers/demo_checker.py` — TOY CHECKER ONLY. One defined string transformation; not an ACC checker.
- `tools/acc/upgh/lineage/astra_v1/workers/demo_worker.py` — DEMONSTRATION ONLY. Deterministic role responses; no language model is called.
- `tools/acc/upgh/lineage/astra_v1/workers/example_bridge.py` — JSON-lines boundary example, intentionally no invented model API bindings.
- `tools/acc/upgh/observe.py` — R, the observation: what code can see about a row, and the verdict that follows.
- `tools/acc/upgh/official_driver.py` — Run the pinned official SAIR verifier on JSON lines from stdin.
- `tools/acc/upgh/offline_send_file.py` — Low-read-budget send file: when the API read budget is near its floor, `upgh plan` cannot refresh boards (its stale-clock gate is deliberate), so build the candidate file offline instead: - every SEND row in research/acc
- `tools/acc/upgh/ppo_convert.py` — Turn AC-SolverX (Caltech, ICML 2026) beam-search paths into official SAIR roads.
- `tools/acc/upgh/quiet_wake.py` — Quiet wake: reopen parked misses whose row received a NEW team road that did not improve our best.
- `tools/acc/upgh/recognition_web.py` — Recognition web (song 12, "Individual faces come and they go, / but the recognition between us is what make us whole.").
- `tools/acc/upgh/rhythm.py` — Rhythm compression: long roads often contain a steady rhythm, one short block of moves repeated r times (e.g. [3,9,9,7] x 9, [10,5] x 8, [11] x 15). For every such run (period 1..6, r >= 3) in our best road on near-recor
- `tools/acc/upgh/sac_to_ac.py` — Meat left on the bone: AC lines hidden inside Stable lines.
- `tools/acc/upgh/scout.py` — Scout: low-team-count rows where the team already has a road, ranked by what a few moves would pay.
- `tools/acc/upgh/sources.py` — Read-only SAIR data: the live boards and our full submission history.
- `tools/acc/upgh/stable_web.py` — Stable height web: heights toward (y, x) instead of (x, y).
- `tools/acc/upgh/stablegap_cov.py` — Change-of-variables transfer onto Stable-gap rows (Stable record >= AC + 3): for each such row B and every row A sharing its Whitehead key with a verified road, transfer A's road to B (cov_transfer.transfer) and test AC 
- `tools/acc/upgh/state.py` — M, the memory register: harness state is a fold over the ledger.
- `tools/acc/upgh/stop_gate.py` — Claude Code PreToolUse hook: while UPG-H is stopped, block search and submit commands.
- `tools/acc/upgh/symmetry_recog.py` — Symmetry recognition (Git's untested idea from the 6 Oct handoff, generalised).
- `tools/acc/upgh/tests/test_upgh.py` — UPG-H v2 tests. Run: python3 -m unittest discover -s tools/acc/upgh/tests -v
- `tools/acc/upgh/training_transport.py` — Carry the 424 official training roads (competition/examples/training_424.json, public) onto every scored row whose start matches any state of a training road up to the 16 frames, cyclic rotation and inversion of each rel
- `tools/acc/upgh/twin_lookup.py` — Twin lookup: for given AC rows, list every other row that is the same presentation up to a symmetry, and transfer the team's roads from each twin as fully paid witnesses (0 API calls, no model).
- `tools/acc/upgh/twist_web.py` — Twist web: carry height-web roads across automorphisms of F2 that are NOT length-preserving.
- `tools/acc/upgh/upgh.py` — UPG-H v2 (Claude edition): memory-first harness for the SAIR Andrews-Curtis work.
- `tools/acc/upgh/whitehead_min.py` — usage: python3 tools/acc/upgh/whitehead_min.py OUT.json Whitehead-minimal forms of every SAIR row start (rank 2), to find rows related by a change of variables (automorphism). Words are strings over xXyY. Type-2 Whitehea

## tools/acc/yx_shortcut.py

- `tools/acc/yx_shortcut.py` — For an AC path of length L, find i and a route s_i -> (y, x) of length <= L-i-1 (exact meet in the middle), giving a Stable AC line of length <= L+1 (route to (y,x) + destabilize twice). Official core replays.
