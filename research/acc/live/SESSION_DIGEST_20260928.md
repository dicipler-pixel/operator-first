# Session 2 (lead) digest, 2026-09-27 22:06Z to 2026-09-28 ~12:29Z

Recovered from the full lead-session transcript (5,400+ JSONL lines, two compactions at 03:59Z and 11:59Z).
The transcript was read in three passes: (1) a chronological sweep, (2) a cross-check of numbers, promises and
ideas, and (3) a check of every named file against `ls` and `git log` on `claude/gallant-bardeen-0pgpae`.
The lead kept working while this was written, so events after about 12:29Z are not covered.
No keys, tokens or Bearer strings appear here; the SAIR key lives only in the environment and proxy.

Team: **Mad Hatters**, `ACC01-T00051`, team id `teamv2_8be23d60b3ea4dac81bbdbc3bb316917`, member dicipler
(Jeromie Beasley, owner). Limits: 40 submissions/day, 500 lines each; API reads 360 per window, reset 00:00 UTC.
The client keeps 40 reads in reserve for sends.

---

## 1. User rules (standing instructions)

| # | Rule | Source / time |
|---|---|---|
| R1 | Never ask the user to paste keys. The SAIR key is an environment credential injected by the proxy for api.sair.foundation; never print it. | 22:25 setup |
| R2 | **Fresh check before every send:** pull live boards and history, then POST within 5 minutes. "if we tie you may submit, you must chek within 5 minutes before you submit". `sair_api.py send` enforces FRESH_S=300. | 22:44 |
| R3 | Send only lines that are unsolved, beat or tie the live record and are not already sent. Every line passes the official verifier ("run the verifier", 23:29). | 22:44, 23:29 |
| R4 | **Batch:** "maybe only submit 5 at a time or 3 lets not do 1 at a time". Send the queue at 3 or more lines. The lead added an exception: a line worth 0.25 or more waits at most 30 minutes (`send-queue --force`). | 00:01 |
| R5 | Only the lead session sends. Helpers put verified lines in `research/acc/live/inbox/`. | ORDERS.md 23:51 |
| R6 | Every 1-point result gets a proof-track write-up ("if we get a 1 we write how we got it a proof track"). | 22:57 |
| R7 | Disclose AI use: the user led and directed; the user's main AI guided it for about a week; Claude executed; helpers contributed. | 01:39 |
| R8 | Give work to helper AIs, share struggles, document everything that works as quick methods, and target rows held by only 1 or 2 teams that have easy moves. | 22:57 |
| R9 | Work ideas off each other each turn through a shared ideas file. | 00:01 → IDEAS.md |
| R10 | "i dont need my ideas mapped as much as the results" → "do both". | 11:23 |
| R11 | Discovery mode: "you can try anything to discover so try shit please … this is discovery not proof"; throw the whole atlas at it. | 10:01 |
| R12 | Do not upload the T9 table to GitHub until the user says so. | early |
| R13 | No PR unless asked. No repos outside scope, except those added with add_repo (mad-hatters-acc-private, acwindow-lean, coxeter-rank2-lean, elemental-peeling-lean, relational-atlas-lean, upg-lean, votkp-lean, dicipler-pixel). | session |
| R14 | Kill by PID only (find PIDs, then kill in a separate command); never `pkill -f` a pattern that matches your own shell. Delete only a stopped sweep's own cap dir; never wildcard-delete. A `cd` + glob `rm` is blocked by the safety check, so use fresh directories. | 23:41, 03:07, 05:40 |
| R15 | No more NEW* files; put a row on your WORKING list before searching it; all compute goes to exact search (later changed to P2 lanes). | ORDERS.md |
| R16 | Commit trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01HDg5qZWaFyKS9qc9tBTE37`. | system |
| R17 | AGENTS.md: preserve failed controls; do not bulk-merge or delete branches. | repo |

---

## 2. Timeline of user requests

Status: **DONE**, **PARTIAL** or **OPEN**. Times are UTC.

| Time | Request (near-verbatim) | Status and outcome |
|---|---|---|
| 22:06 | Handoff paste; "YOu now have the lead … get our api up and running so you can take lead" | DONE. API live at 22:35. Built T9 (sha 48a81fea…). Official SAIR repo cloned at a0fd6e6. |
| 22:16 | "walk me through the sair api setup" | DONE |
| 22:25 | Screenshot of the key dialog (env "op 1st", name "SAIR ACC", Bearer, allowed api.sair.foundation) | DONE. Proxy-injected auth (70ce2e6); the key never went through chat. |
| 22:35 | "done" | DONE. 85 prior submissions, 960 accepted rows. AC 0.47 (18/44), SAC 1.04 (15/41). |
| 22:44 | Fresh-pull rule; "if we tie you may submit, you must chek within 5 minutes" | DONE (R2). Submission 2558 NEW15 at 22:45. |
| 22:45 | "leader board has delay" | DONE. Boards refresh on a timer (~10 min seen first, later ~30 min). |
| 22:47 | "search the most recent submissions by someone else" | PARTIAL. No public per-submission route (~30 routes tried). Built `changes` (985a837) and `teams` (0a3c5b5) from /leaderboard/teams/{id}/challenges. |
| 22:49 | Leaderboard ranks 12–17 + API guide | Used. Ryan T00084 #17 0.647 was the next AC target. |
| 22:53 | "so go after the first row" (ac-06969, Ryan's best, 38/k2) | PARTIAL, paused. Caps 27–32 prove no path ≤38 within the first 29 moves (cap 32: 123M states). Beams reached 43/45 at W 200k/400k. Caps 33+ need more memory. |
| 22:57 | Proof track per 1-point result; give work to helper AIs; share struggles; document what works; target 1–2-team rows with easy moves | PARTIAL. WIN_TEMPLATE, METHODS_PLAYBOOK, HELP_WANTED (244e4d6), ORDERS, easy/mid target lists. The proof draft is written but not submitted. No single-line beat yet. |
| 23:18 | "helper working lets keep leading the way" | — |
| 23:29 | "run the verifier" | DONE. Official verifier permission given. Submission 2565 SACPLUS2. |
| 23:30 | "are we doing a proper graph of all we did" | DONE. Tracker artifact https://claude.ai/artifact/PesMNAWMhazVqhNx5DpP5u (dash docs at v13). |
| 23:37 | "so for every ac is there a stable ac and vice vs?" | DONE. Yes: all 10,115 ids exist in both. An AC path + [16,15] gives the SAC line. |
| 23:38 | Session 1's retrospective paste | DONE. Changes adopted (fresh pulls; AC hit → SAC line; exact capped search on records 25–40 with 2–6 teams). |
| 23:51 | "keep lokiand giving us orders" | DONE. ORDERS.md (7d24bc8), inbox protocol. |
| 00:01 | "keep going work ideas off eachother each turn" | DONE. IDEAS.md. |
| 00:01 | "maybe only submit 5 at a time or 3" | DONE. `send-queue` (2f1ff1e). |
| 00:14 | Codex two-interstate idea on ac-05818 | DONE, no gain. Maps saved; radius-6 search (62.97M states) found no 34. |
| 00:33 | "ok do we have any submissions yet" | Answered: 5 submissions, 18 lines. |
| 01:23 | "keep pulling the latest solves" | DONE. `watch_board.sh` every 30 min → `live/changes/`. |
| 01:27 | "the road has been right here all this time but you got to look with more than your eyes" | PARTIAL. The lead read it as the 424 official training roads (`training_424.json`). `road_bridges.py` found 4 bridges, all to rows whose records are already shorter. **"Was that the road you meant?" was never answered.** Session 1 later read it as "the board is Miller–Schupp families". |
| 01:29 | "look up all the proof tracks submitted" | BLOCKED. Not in the API (20 paths 404); competition.sair.foundation is blocked. The user uploaded 4 proof tracks instead. **The allowlist request is open.** |
| 01:34 | 4 proof tracks uploaded (P000002, P000007, P000008, P000009) | DONE. Reviewed; detour-width exact values computed; proof draft written. |
| 01:39 | Disclose AI use (user led; the user's best AI prompted for a week+) | PARTIAL. Section 8 "Provenance" is in the draft, but **the main AI's name is still a placeholder**. |
| 01:46 | "Comutators" song: freestyle and abstract work | DONE. Abstract "Commutator Load and Transient Growth". |
| 01:48 | "you use it to get results it fits somewhere" | DONE. Commutator load vs climb on 292 paths: corr +0.36. Kept as a tie-break idea. |
| 01:51 | Eigenvectors, "leader", Dunford circle, conservative matrix field | DONE. Probe-and-predict cap gating (4902aad). |
| 02:02 | "well what do you think" | Answered with an honest read. **Asked for a high-RAM machine or Colab: unanswered.** |
| 02:02 | Smith-chart paste (session 1) | DONE. Checked on 5 exact paths: late finish holds (87–97%), bursts don't. |
| 02:05 | "go through my github and find some good ideas … start at the atlas" | DONE. 7 ideas; shadow bounds, two-layer, shadow beam and Schur tested (b7ac198). |
| 02:47 | "dont stop" + pulse / four-names poem; "shur test" | DONE. Schur macro beam (BEAM_MACROS): no gain on ac-03305 (27). |
| 03:00 | "Take it back" song | DONE. Echo table (ECHO_FILE): ac-05818 best 35 (our own); no 34. |
| 03:39 | Session 1's mirror-twin crossrow report | Noted. Radius 1 on 372 paths: 13 improved or new, 0 ties. |
| 03:40 | "did i mess up the work by sharing something?" | Answered: no, it was a platform container restart. |
| 03:43 | "go pull new k2 targets ac only then we get an easy stable solve and dont search for them" | DONE. k2ac list (22 → 7 after exclusions); swept 7/7 with no record hits. |
| 03:44 | "most people dont know there is a seperate stable ac" | PARTIAL. Data: SAC record > AC+2 on 95 rows (sacbeat list). Beam stopped at 9/89 rows. |
| 03:57 | "give luna a msg on wht to do at the board" | DONE. LUNA_ORDERS_20260928.md (6 → 5 rows). Codex took the same rows; screen at W=20k found no path. |
| 04:10 | Bob's upload (macro library, rhythm test) | DONE. Filed in ledger; 2 files sent for Bob; macro A/B dead (valid rerun 09:21). |
| 04:22 | "go into my google drive get the latest atlas pdf or html or atlas cards zip file" | PARTIAL. 2026-08-27 atlas PDF text saved. **atlas_cards.zip (16 MB) and the Sep-12 bundle (3.5 MB) are too big for the Drive tool; the user was asked to attach them (open).** |
| 04:33 | "keep you researching my old github for good ideas" | PARTIAL. 6 repos cloned and mined. **Asked which other repos he means (yang-mills-lean, suns-lean, three-body-lean…): unanswered.** |
| 04:57 | "you ever going to give bob some time … old chats cheking us out and dropping tips" | DONE. Bob's A/B reniced; sacbeat paused (kill -STOP). |
| 05:19 | "keep workin all the ideas around" | Ongoing. |
| 09:03 | Codex YXXyx generator paste (125 vs 80 … 4,088 vs 2,071) | DONE. Logged; 2a-level test (~2 moves per x). |
| 09:35 | "did you everr read it all [the atlas]" | DONE. ATLAS_AC_LEDGER.md (132 lines); builder A/B on its top ideas. |
| 10:01 | "try anything to discover … throw the atlas at this whole thing" | Ongoing: score zoo, beam arms. |
| 10:16 | "Cross the wall" song | DONE. P2-capped exact (dead as a region bound), L2/L3 lookahead, symmetry cage (refuted). |
| 11:05 | "They can bury the picture / can't bury the count" | DONE. Class quota and overlap splice: **ac-00487 26 and sac-00487 27 ties**. |
| 11:12 | "Cross the wall" reposted | DONE. BEAM_ELITE ("protect what can be protected") is the winner arm. End-length decay diagnostic **not built**. |
| 11:22 | "keep trying to map and graph it all" + commutator census of 8 papers | DONE. Census scores tested in the zoo: none beats comm_len. Algebra checked. |
| 11:23 | "i dont need my ideas mapped as much as the results" / "do both" | DONE. Results Map https://claude.ai/artifact/4TTVZS1uHDZJ9qLzNAQzmB (v3). |
| 11:33 | "is this guy new" (T00096 scoring page) | DONE. grothendiecksga.com, rank 4 AC all night; holds 53 of 68 chain rows. |
| 11:43 | AK(3) audit + ak3_p_to_ak3_replay_1.py | DONE. Replay PASS; archived. |
| 11:46 | "i redid the paper in lean i said get that if you need to" | OPEN. **AK3Audit.lean never arrived** (only a ChatGPT sandbox link). Not found in the repos or Drive. |
| 11:57 | MS_Lisitsa_audit.md + ms_lisitsa_replay.py + ak3 replay v2 | DONE. Archived (3cbd3ef). The Lisitsa family is our YXXyx chain; its routes are ~8x the records. |
| 12:01 | "Every step you take is a choice multiplied" song (audit re-upload, identical) | DONE. Mapped to "smaller move set / keep BS fixed". |
| 12:05 | "keep your idea going and do this as well" + session 1's MOVE_MASK text | PARTIAL. Session 1 committed MOVE_MASK (bf8e653). The lead ran level-cost beams, the row-op argument (3eae42a) and exact capped checks (477d357). The masked n=4 runs at caps 25/27 had not reported. |
| 12:07 | "pull all of our work from the transript go over it 2 or 3 times" | This digest. |

---

## 3. Submissions and scores

All 12 submissions this session were accepted in full: **71 lines**. At 11:31 all 71 were still at the record, worth
**2.3396** points in total.

| Sub | Time | Lines | Content | Method | Value then |
|---|---|---|---|---|---|
| 2558 | 22:45 | 6/6 | NEW15: sac-01734 38 (k4), sac-07158 41 (k5), ac-07642 30 (k8), sac-07642 32 (k9), ac-05578 34 (k10), sac-09189 32 (k10) | beam + exact (session 1) | ~0.1 |
| 2565 | 23:29 | 6/6 | SACPLUS2: sac-00276 41, sac-02114 32, sac-06754 36, sac-08130 32, sac-08702 28, sac-09757 42 | AC path + [16,15] | small |
| 2566 | 23:36 | 2/2 | ac-03305 23 (k6), sac-03305 24 (k1) | exact capped (caps 24–36 empty; SAC at cap 37, AC at cap 40, 133M states) | ~+0.5 |
| 2569 | 23:50 | 2/2 | ac-01629 23 (k4), sac-01629 25 (k3) | exact capped (sweep C) | ~+0.19 |
| 2572 | 23:56 | 2/2 | ac-05558 24, sac-05558 26 (k5) | exact capped (midC) | ~+0.06 |
| 2581 | 01:24 | 4/4 | ac/sac-07435 26/28 (k6), ac/sac-08201 31/33 (k5) | exact capped (midC) | ~+0.09 |
| 2606 | 04:23 | 15/15 | ac/sac-03028 26/28 + 13 SAC mirror ties (sac-00521, 00974, 02061, 02673, 02902, 03250, 03446, 04278, 05466, 06048, 08363, 08394, 08920) | session 1 crossrow | ~+0.02 |
| 2607 | 04:28 | 22/22 | 20 AC road ties (ac-00201, 00337, 00521, 01639, 01962, 02061, 02446, 02673, 02902, 02989, 03250, 03446, 05091, 05466, 05668, 06048, 08363, 08394, 08920, 09058) + ac/sac-09989 23/25 | session 1 unsent roads | ~+0.012 |
| 2632 | 07:07 | 3/3 | ac/sac-07004 43/45 (k14), ac-04278 35 (k14) | session 1 road cycle | tiny |
| 2638 | 08:19 | 3/3 | **ac-03060 28, sac-03060 30 (both k1 → +1.0, first P2 win)**, ac-05835 33 (k13) | P2 beam (atlas B31) | ~+1.0 |
| 2648 | 10:07 | 3/3 | ac-01698 36 (k4), ac-03789 34 (k7), sac-01698 37 (k3) | P2 beam; (y,x) shortcut | ~+0.19 |
| 2657 | 11:07 | 3/3 | sac-00487 27 (k3), ac-00487 26 (k14), sac-05091 26 (k10) | class quota; overlap splice; (y,x) | ~+0.13 |

**Queued, not sent:** `research/acc/live/queue/20260928T1210Z_sac00222_p2b.txt`, a sac-00222 42 tie (k3, ~0.125).
It passed the official verifier at 12:10 and was committed (2aa99ee). It was still waiting for 2 more lines (R4) at 12:28.
ac-00222 is at 42 against a record of 41, and the (y,x) shortcut found nothing within 32.

**Score snapshots** (AC score and rank; SAC score and rank):

| Time | AC | SAC |
|---|---|---|
| 22:35 (est) | 0.47, 18/44 | 1.04, 15/41 |
| 22:50 | 0.415, 18 | 1.133, 14 |
| 23:51 official | 0.43 (est 0.556) | 1.657 (est 1.91) |
| 00:30 | 0.522, 18/44 | 1.812, 14/41 |
| 03:07 | 0.569, 18/45 | 1.859, 14/42 |
| 05:19 | 0.577 | 1.782 |
| 07:27 | 0.574 | 1.7725 |
| 09:23 official | 1.0742, 17/45 | 2.2725, 14/42 |
| 10:20 official | 1.1425, 16/45 | 2.3955, 14/42 |
| 11:18 official | **1.1426, 16/45** | **2.5215, 14/42** |

Points by method (Results Map, 11:31):

| Method | Points | Lines |
|---|---|---|
| P2 | 1.0704 | 5 |
| Exact capped | 0.8594 | 10 |
| (y,x) | 0.126 | 2 |
| Class quota | 0.125 | 1 |
| NEW15 beam + exact | 0.0986 | 6 |
| Mirror cross-row | 0.0364 | 37 |
| AC+2 | 0.0235 | 6 |
| Road cycle | 0.0002 | 3 |
| Overlap splice | 0.0001 | 1 |

Leaders at 22:35: 冰冻野鸡大学 T00026 1779.46 (4,040 bests); AC-Solver =D T00029 1486.30; memcon.ai T00101
1108.37. Nearby: NavierStoked T00011 5.47; MCSC T00009 4.94; T00128 2.91; T00034 2.63; relentless T00070 1.45;
Ryan T00084 0.647. Rival **T00096 grothendiecksga.com** (team id teamv2_af207dcf6846495a86165c649785aa93): rank 4
on AC, 2,011–2,013 scoring rows, 486.48 points (548 → 487 at 04:11 when another team beat ~1,000 long rows).
Snapshot: `live/teams/T00096_ac_20260928T1140Z.json`.

---

## 4. Methods ledger

### Works (scored)

| Method | Tool | Numbers / notes |
|---|---|---|
| Exact capped BFS (adaptive caps, jump-ahead, probe-and-predict) | `optimality/acc_capped.c`, `run_capped_sweep.py`, `ops/sweep.sh` | Depth MAXD = R−9 (SAC R−11). CAP_JUMP A=8 (180M budget), B=3 (70M), C=5 (25M), D=5 (60M). CAP_PROBE=10M; skip a cap if predicted > 0.9 × budget (ac-05818: cap 26 predicted 80M, actual 87M; cap 27 predicted 397M, actual >196M). Exact for records ≤31. **Wall = memory (~180M states in ~15 GB).** Record paths climb 13–16 above the start. |
| AC + [16,15] → SAC line | `sair_api.py plan`, sweeps | Every AC hit gives the SAC line. 95 rows have SAC record > AC+2 (sacbeat). |
| **P2 beam** (atlas B31: best total length after two multiplications, free rotations) | `acc_beam.c` BEAM_P2=1/2/3 | P2=2 ≥ P2=1 everywhere and is cheaper. A/B on T8: 03305 24/24 vs plain 29/31; 01629 23 vs 26; 05558 26 vs 30; 06045 39 vs 44. Gain confined to records ≤45 (session 1 lanes p2c1/p2c2: 0 ties on 104 rows with records 46–60). Loses on ac-00145 (relators grow). |
| **Class quota + elite** (B16/B17 + "protect what can be protected, release the rest") | BEAM_QUOTA=16, BEAM_ELITE=5000 | Winner arm P2=2+Q16+E5000 at W=20000: never worse than P2=2; ac-00487 26/27 (both records), 06045 SAC 41. Lanes switched to it at 11:54 (`P2_ELITE=5000 ops/p2_list.sh`, binary acc_beam_x). |
| (y,x) shortcut | `tools/acc/yx_shortcut.py` | Exact meet-in-the-middle from path states to (y,x), then [15,15]. Hits: sac-01698 37, sac-05091 26. None for 00021, 00201, 02446, 01639, 05668, 05835, 00222 (none within 32), 02717 (28), 04586 (30), 03871 (22), 04211 (23), 03719 (27), 08031 (27). |
| Overlap splice | `tools/acc/overlap_splice.py R` | ac-00487 27 → 26 (tie). R=3 at 12:11: 557 rows with paths, 24 with ≥2 paths; ac-06045 39 → 38 (record 36). |
| Mirror cross-row (B81; session 1) | `tools/acc/crossrow.py` | 37 lines. Radius 1: 13 improved, 0 ties; windowed: ac-03028 29 → 26 tie, ac-03919 32 → 30 (record 27). |
| Unsent roads / road cycle (session 1) | `tools/acc/pool_roads.py` | 677 roads on 496 rows → 20 AC ties (2607); ac/sac-07004. |
| Live-board comparison + fresh pull | `sair_api.py` | Found the SACPLUS2 and NEW15 ties. |

### Diagnostics that work (no points yet)

- **Beam-loss trace (B20)**, `beam_loss.py` + BEAM_TRACE_FILE: P2 drops record roads at index 6–9 when P2 rises 1–3
  (05558: 14 → 17 at idx 9, rank 8.8× the cut; 00145: 15 → 16 at idx 8). Plain H keeps them longer (idx 7–20) and
  finds 26 on ac-00061 where P2 finds 29. This motivated BEAM_DUAL.
- **Score zoo** (`score_zoo.py`, `SCORE_ZOO.md`): the comm_len tie-break (P2, comm_len, P1m, H) ranks the record move
  top-3 on climbing steps 0.616 (+0.20); real2_d2 0.643; L2/L3 survive as tie-breaks. Symmetric cage refuted: record
  paths prefer symmetric states (0.71 vs 0.51). Ranking symmetry higher: all-steps 0.652 → 0.686 (endgame only).
  P2 climb on 59 hump paths: c=0 66%, c≤1 83%, c≤2 92%, c≤4 97%.
- **P2 validation** (`p2_hump_test.py`): 609 verified paths on 526 rows, 56 hump paths. Median raw climb 9 vs P2 0
  (64% no climb). P2 predicts moves remaining with LOO error 3.18 vs 4.52 for length. E1 (min, max) 3.89; (min, max, P2)
  2.18. C1 survives (hump exponent-sum classes vs random, p=0.005). U1 dead.
- **Commutator load** (`hump_features.py`): corr(climb, cyclic commutator load) = +0.36; corr(climb, start length)
  = −0.45; R² 0.34; fails on extreme humps (03305 +16).
- **Detour width (DW) exact values:** 03305 = 40 (start 24, +16), 01629 = 38, 05558 = 29, 07435 = 27. 45
  lower-bound rows (`live/dw_bounds_20260928.json`).
- **AK(3)-class skip list:** 47 unsolved rows (`live/AK3_CLASS_ROWS.json`); rechecked by the lead.
- **Probe-and-predict** (leader growth rate of BFS layers).

### Dead (keep as failed controls)

| Idea | Result |
|---|---|
| Mirror transport | 44 ordered symmetric pairs, 0 shorter. |
| Bridges (`find_bridges.py`) | r≤2: one pair, both unsolved; r=3: 21 pairs, no gain. |
| Training-road bridges (`road_bridges.py`) | 4 rows (ac-07667, 08327, 09594 + 1); records already shorter. |
| Shadow lower bounds (SL(2,p)) | Log-capped: SL(2,7) diameter 9, SL(2,11) 11. Any invariant lower bound is log-size. |
| Two-layer capacity split | Collapses (max h0+h1 = 3). |
| BEAM_SHADOW (direction finder) | Signal is real (+0.31 with moves left, +0.24 on humps), but ac-03305 stays 27 at weights 0.5–4.0. Only one row tested. |
| Schur macros (`mine_macros.py`, BEAM_MACROS) | 210 paths, 36,194 excursions; ac-03305 27 at MACW 0.5/1/2. |
| Echo table (`build_echo.py`, ECHO_FILE) | ac-05818: 122,317 echo states, 55M states, best 35 (ours). "Local repair of near-miss paths is exhausted." |
| Reverse search | Humps sit mid-path (30–52%). |
| Bob's training macros | Valid rerun (T8, W=20k): better 0, worse 4 (00145 51 vs 40; 05702 52 vs 47; 06045 49 vs 39; 08995 65 vs 47), same 5. Two earlier runs were INVALID (binary lacked BEAM_MACROS). |
| Rank-3 super-relator | Exponent-sum matrix stays unimodular, so S_a (a≥2) needs a tag g, and g blocks crossings. |
| U1 (one relator at a time) | Median run 2. |
| BEAM_WH (B83 Whitehead key) | Dead in the A/B. |
| BEAM_P2=3 (comm_len key) | The offline gain did not carry; P2=3+Q16 drifts to ~2,100-letter states. |
| BEAM_QUOTA=4 | Dead. |
| Commutator-census scores (GEN, GENmin, MIXED, SELF, FLAT) | None beats comm_len. FLAT = cage gain at 40× the cost. |
| Atlas Test A (exit-count tie-break), Test B (learned linear descent) | Dead by pre-set rules. |
| Atlas B6, B12, B22, B38, B48, ALG-FORCING-DUAL, GRAPH-SUBGRAPH-CAPACITY, UPG-FEEDBACK | Dead (ATLAS_AC_LEDGER). |
| Ledger #2, blocks ranked by x per move (`block_search.py`) | Ill-posed: letter counts reward pasting relator copies (921,943 blocks ≥0.5 x/move). |
| **P2-capped exact search** (`acc_capped_p2.c` CAP_P2/CAP_PAD; ledger `p2cap_exact_20260928.json`, d6e2d47) | Dead as a region bound. P2 ≤ start holds in 74–92% of any length-capped region. Only P2 c=0 + pad≤2 helped, on 03305 (AC 23 in 36.3M states / 222 s vs 71.5M at cap 40), and it missed 07435, 05558, 01629 and 08201. Keep only as an optional filter for pad-free, P2-flat rows. Step-4 rows: ac-04346 none to depth 16; ac-06936 SAC 28 (record 27). |
| p2ms lane (18 chain rows n=4, 5) | No paths. |
| R_n deep P2 beam (21 rows) | No path (74c910b). R_n overlaps the AK(3) list, so treat as open problems. |
| Exact capped sweeps easy/midB/midD | Nothing in hours; stopped at 07:14 (see §8). |
| Codex corridor / two-interstate | No 34 on 05818; ac-09311 43 vs 42 (k1). |
| Codex cap-lift identity loops; genus test | Failed / don't revive. |
| BEAM_BAL (session 1) | Only has an effect with BEAM_H=1. |
| Smith-chart "short pushes" | Bursts don't hold (climb 1 step at a time). |

### Partial

- **Stable AC fast peel** (`sac_fast_peel.py`): from (x, y X^m) the tail costs ~2k+3m/k (m=1023 → 164 vs 1025). A beat
  needs a build ≤ ~1.55 (n=5) to 1.87 (n=10) moves per crossing. Not reached.
- **sac_ms_bs.py** (Codex build + conversion + rank-3 tail): n4 64, n5 127 (record 82), n6 236 (147), n7 442 (277),
  n8 850 (534), n9 1648 (1048), n10 3232 (2073). Valid, not scoring.
- **Codex YXXyx generator** (`yxxyx_chain.py`): valid, 4·2^n+2−n (n5..10 = 125, 252, 507, 1018, 2041, 4088).
- **E1, C1**: weak survivors; not built into the beam.
- **BEAM_DUAL** (two eyes; interim, scratch `dual/ab.log`, 14 runs): ac-00061 DUAL0.5 26 vs winner 28; ac-05558
  DUAL0.75 24/26 vs 26/28; ac-07435 26 vs 28; ac-04211 equal 33; ac-06045 DUAL0.5 40 vs 39 (worse). No verdict yet.
- **MOVE_MASK exact** (session 1, bf8e653): n=3 r1-only 7 moves → 33 (378k states); 10-move set {0–8, 12} → 28 (the
  optimum) at 1.6M states. n=4 caps 25/27 pending.

---

## 5. Miller–Schupp / YXXyx chain

- **Board structure (session 1):** MS(n,w) = ⟨x,y | y^-(n+1) x^-1 y^n x, w⟩, n=1..10, 1,006 second words, 3,363 rows,
  covering ≥1,977 of the 2,672 unsolved rows. Families: `ledger/ms_families_by_w_20260928.json`; 650 rows held by
  ≤2 teams. Doubling chains have records ≈ 2^(n+1)+c, and the **SAC record = AC+2 on all 68 chain rows** (n=4..10).
- **Chains** (n=3..10 records / k):
  - YXyXyx|1: 32/3, 56/3, 91/2, 158/1, 288/2, 547/1, 1061/1, 2088/1 (ac-09243, 04016, 07182, 09166, 10057, 00230, 03317, 00025).
  - YXYxyX|1: 33/6, 59/1, 96/1, 164/2, 296/2, 555/1, 1071/2, 2098/1.
  - YYxyXYx|1: 40, 66, 105, 173, 304, 564, 1079, 2107 (all k1).
  - YYXYYxyyX|1 (cheap, sub-exponential?): n5 42, n6 43, n7 76, n8 81, n9 134, n10 159 (all k1; ac-06005, 05564, 06899, 01715, 03821, 08287).
- **YXXyx chain = Lisitsa's MS_n(w\*) family** (Codex 11:52Z correction; the lead's `lisitsa_find.py` matched it up
  to symmetry: 28 hits):

| n | YXXyx rows (AC/SAC, k1) | YXyxx rows (k1) | Lisitsa length |
|---|---|---|---|
| 4 | ac-01784 48/50 (k3/k4), ac-04042 50/52 (k3/k4) | — | 171 |
| 5 | ac-01950 80/82 | ac-05586 84/86 | 412 |
| 6 | ac-02033 145/147 | ac-06018 150/152 | 917 |
| 7 | ac-06796 275/277 | ac-00676 281/283 | 1,953 |
| 8 | ac-03079 532/534 | ac-03773 539/541 | 4,156 |
| 9 | ac-06727 1046/1048 | ac-03984 1054/1056 | 8,634 |
| 10 | ac-00106 2071/2073 | ac-01523 2080/2082 | — |

  Lisitsa's archive (Zenodo 10.5281/zenodo.14647749 v2, MD5 345a7a0d…; DOI 10.1016/j.exco.2024.100168): 16,232
  labelled moves pass; 11-move common finish to (b,a); MS(9) and MS(8) share their final 4,063 moves; no induction for
  all n. The routes keep BS fixed with short working words, but they are ~8× the records and score nothing.
- **Record law:** rec(n) − rec(n−1) = 2^n + 1 (or +2): 80 → 145 → 275 → 532 → 1046 → 2071; rec(n) ≈ 2^(n+1)+n+11..13.
  **T00096 holds 53 of 68 chain rows (38 alone)**, so they have the construction.
- **Start:** r0 = YXXyx (BS: y x y^-1 = x^2), r1 = Y^(n+1) X y^n x.
  - The 9-move level `5 1 12 4 1 10 5 12 10` is uniform in n: MS_n → (BS, x^3 Y^(n−1) X y^(n−2) x).
  - An alternate 18-move prefix gives x^7 (`ledger/codex_yxxyx_trace_20260928.json`).
  - For w=YXyXyx, the phase-A prefix `3,8,2,6,12,4` + `12`×n turns r1 into a BS rotation.
- **Level block:** (BS, Y^k X y^(k−1) x^a) → (BS, Y^(k−1) X y^(k−2) x^(2a)).
  - Codex: 10^(a−1), 5, (11,5)^(a−1), 12 = 3a−1 moves.
  - Isolated rank-2 level `1 4 (7 4)^(a−1)` = 2a moves, but it leaves BS slid to X^(a−1) BS x^(a−1); undoing costs
    a−1, so ~2 moves per new x. The "mirror pattern" chaining idea gives the same ~2 per x.
  - Records imply ~1 per x.
- **Exact small-n (synthetic):**
  - n=2 optimum 15 (`5 7 12 5 6 5 12 11 2 5 12 5 8 2 4`, 505k states).
  - n=3: cap 16 → 30; cap 18 → none ≤29; **cap 20 → 28 (optimum, session 1):**
    `5 1 12 2 5 8 3 6 3 6 3 0 12 2 6 8 2 7 5 6 6 2 4 4 4 4 4 4`. It uses (3,6) pairs growing X² per 2 moves, then y = x^7
    and y = x^6 collapse to x in one move, then a 6-peel. An H-beam found 29.
  - n=4: cap 21 none ≤49 (complete); cap 23 none ≤46 (depth 37, budget); cap 24 none ≤38. Our constructions reach
    55/56; macro beam 61; the lead's H-beam from the phase-A state gives 64 (scratch `work/ms_n4_path.txt`); Codex has a
    55-move certificate. The formula says ~47, and the leaders' road must go above total length 23.
- **Skip test:** can we finish (BS, x^a YYXyx) without doubling?
  - a=1 (cap 13): 12, and the optimum doubles first.
  - a=3: cap 17 → 21; **cap 21 → 21** (51M states, 5,158 s, complete; path
    `0 4 11 4 11 4 11 4 1 12 3 6 2 4 4 4 4 4 4 4 8`). No saving at small size.
  - Level hop x^3 → x^7: none within 9 for all 5 BS rotations.
- **Level-cost beams** (12:06–12:19, winner beam W=20k, `optimality/chain_rowops/level_beam.py`):
  - Finish (BS, Y x^m): m=3 → 8, m=7 → 13, m=15 → 21.
  - Last level + finish (BS, YYXy x^a): a=1 → 8, a=2 → 13, a=4 → 22 (`1 4 10 4 10 4 10 2 5 8 7 12 4 6 3 0 4^6`),
    a=8 → none (235 s), a=15 → none (331 s).
  - Two levels (BS, YYYXyy x^a): a=1 → 15, a=2 → 27. The a=4, a=8 and Y x^31 runs were **stopped by PID at 12:21**
    (low value) and never finished.
  - **Exact capped checks** (12:30Z, IDEAS, 477d357; acc_capped rebuilt with MOVE_MASK, T8): last level + finish
    (BS, YYXy x^4) under cap 21 → **22**, optimal among cap-21 routes (46M states, complete to depth 21). Finish
    (BS, Y x^15) under cap 23 → 25 (the beam's 21 climbs above 23), so there is no sub-linear finish inside cap 23.
- **Row-op argument** (IDEAS entry retimed to 12:18Z in 25e7fac, first committed 3eae42a; `chain_rowops/sl2geo.py`, `convlen.py`):
  - One level is [[−1,0],[a−1,−1]] → [[−1,0],[2a−1,−1]] in SL2(Z), with a unique geodesic of **a row ops**.
  - Repeated multiplication without conjugation only appends BS^j (5 letters each), so about a conjugations are also
    forced: ~2a per level.
  - So any route through level states with BS fixed costs ~3·2^n. **The leaders must leave the level shape**, for
    example r0 not a BS conjugate mid-route, or both relators carrying long runs.
  - Search target for n=4 (record 48).
- The level-cost entry in IDEAS is retimed to 12:10Z (it was first written as 12:20Z).
- **Stable AC on chains:** fast peel (§4) and super-relator negative. The beat lane needs a cheaper build.
- **n=4 board rows:** ac-01784 and ac-04042 (record 48/50, k3) were never swept before 12:14. Winner beam W=20k,
  depth 50: **no path on either** (12:18).

---

## 6. Helpers

| Helper | Role / files | State at ~12:29Z |
|---|---|---|
| Session 1 (other Claude session) | WORKING_session1.md. SAC-direct 146 rows, crossrow mirror ties, unsent roads, MS families, masked exact search (MOVE_MASK), macro beam on MS(4), P2 lanes p2c1/p2c2 (records 46–60, 0 ties), R_n, "the name still count" songs. | Masked n=4 at caps 25/27 and macro n=5 / MACW=1 running; results unknown. |
| Codex | ORDERS_codex.md, WORKING_codex.md, targets_codex_oddeasyB.json (213 rows excluded from our sweeps). Two-interstate maps, ac-09311 corridor, YXXyx generator and trace, Lisitsa mapping correction, commutator phase probe (`codex_commutator_phase_probe.py`, 1.2M-state local test). Took Luna's SAC-beat rows. | Commits under the user's account. |
| Codex ABC (Adam, Bob, Charlie) | POST_adam_bob_charlie.md, WORKING_codex_abc.md. T8 build (24,587,144 states, 640 MB, SHA 38f05b56…); disk-backed capped engine (`acc_capped_disk.c`; 60M-state T8 trial on ac-00580, incomplete); 100-row unsolved H/HBAL screens (no path); rank-3 kernel validated on all 257 moves; radius-5/6/7 borrowed-suffix joins for ac-00766 (34 vs 33) and ac-00974 (26 vs 24): no gain, rows released. | Done / released. |
| Bob (user's helper AI) | Move-rhythm test on training_424: blocks survive (tandem repeats 589 vs 365±17), beat dies (p=0.22); core macro `4,.,2,5,2`; 977 macros. | Macro A/B dead. Near-misses 00766 / 00974 need longer windows or a different road. |
| Luna | LUNA_ORDERS_20260928.md: 5 SAC-beat rows (ac-00520 ≤108, 00718 ≤128, 01566 ≤145, 00074 ≤216, 03104 ≤325; 03887 closed at 04:10). | Codex + Luna screen at W=20k: no path (`ledger/luna_sacbeat_screen_20260928*.json*`). Overlap not formally resolved. |
| ChatGPT (the user's "best AI") | IDEAS 01:15Z (detour height, Pareto pilot); corrected the lead's 00:25 idea (a witness peak does not certify lower caps exhausted); AK(3) audit, AK3Audit.lean (not received), Lisitsa MS audit + replay. | — |
| Grok | Prepared P000009 (our earlier proof-track note). | — |
| Lead's subagents | GitHub ideas; Drive atlas; P2 validation; ACC repo mining (AK(3) list); Lean repo mining (C1/C2/E1/E2/U1/U2); BEAM_P2 builder; super-relator (negative); atlas ledger; score zoo; P2-capped exact (finished 12:19, dead as region bound); **builder: quota/WH/loss/ELITE → BEAM_DUAL (still running; binary scratch acc_beam_y; WIP in acc_beam.c committed unverified in 39cda03)**; this digest. | — |
| "Old chats" | ~40 commits/hour from other chats dropping tips. | — |

---

## 7. Tools and files (pass 3: exists / committed)

All files below **exist and are tracked** on `claude/gallant-bardeen-0pgpae`. The last commit touching each is shown.

**tools/acc**
- `sair_api.py` (02a202f). Commands: check, boards, mine, plan, send (FRESH_S=300), send-queue (≥3 lines, --force),
  submit (dry run), status, download, changes, teams, leaderboard, spec.
- `dashboard_data.py` (38a5f3b).
- `dashboard/`: acc_tracker_template.html (d7c37dc), idea_map.html, results_map.html, results_data.json (4d47557),
  build_results.py, build_results_map.sh (2ba0431).
- `METHODS_PLAYBOOK.md` (25e7fac; "not worked" section updated 1fb6534 with the P2 region bound, (y,x) 0/6 and chain
  beams), `HANDOFF_SAIR_ACC.md` (38a5f3b); `HELP_WANTED.md` (244e4d6).
- `proof_track/`: WIN_TEMPLATE.md (244e4d6); DETOUR_WIDTH_ON_BENCHMARK_ROWS_DRAFT.md (e87e5e2; line 150 has the
  **[NAME OF THE TEAM'S MAIN AI ASSISTANT]** placeholder); PROOF_TRACK_SUBMISSION.md (68ad396, pre-session);
  capped_sweep_summary.json.
- `targets_easy_lowk_20260927.json` (244e4d6); `targets_mid_25to40_k2to6_20260927.json` (d7c37dc).
- `ops/`: sweep.sh, watch_sweeps.py, watch_board.sh, watch_inbox.sh (dfc7a9b); beam_list.sh (95bd7d0); p2_list.sh (4d47557).
- `sac_fast_peel.py` (e51c969), `sac_ms_bs.py` (bef5dd6), `yx_shortcut.py` (07e483f), `overlap_splice.py` (4d47557),
  `ak3_p_to_ak3_replay.py` (3693cfb).
- Session 1: `crossrow.py` (7f296ad), `ms_hop.py`, `mstrace.py`, `cap_words.sh` (3f5488b), `pool_roads.py` (c3b77fc).
- `colab_acc_search.py`, `make_T9_zip.sh` (pre-session, for a high-RAM run).

**research/acc/optimality**
- `run_beam_raw.py` (69adf1b), `run_capped_sweep.py` (4902aad).
- `acc_beam.c` (BEAM_DUAL WIP, +38/−15, committed with the snapshot in 39cda03 before the builder reported;
  previous clean state 2c8f330).
- `acc_capped.c` (bf8e653, MOVE_MASK), `acc_capped_p2.c` (d6e2d47). Also present: acc_batch.c, acc_capped_disk.c (Charlie),
  acc_opt.c, acc_window.c, sac_rank3.c.
- `find_bridges.py`, `road_bridges.py`, `hump_features.py`, `shadow_bounds.py`, `shadow_probe_export.py`,
  `mine_macros.py`, `build_echo.py`, `p2_hump_test.py`, `score_zoo.py`, `beam_loss.py`, `yxxyx_chain.py`,
  `codex_commutator_phase_probe.py`.
- `ac-05818_two_interstates_map.json`, `ac-09311_two_routes_map.json`, `codex_01734_candidate_ties.txt`.
- `chain_rowops/` (3eae42a): sl2geo.py, convlen.py, level_beam.py.

**research/acc/live**
- ORDERS.md, ORDERS_codex.md, ORDERS_luna_ms.md, IDEAS.md (newest entries 12:18Z / 12:30Z), WORKING_session1/2.md,
  WORKING_codex.md, WORKING_codex_abc.md, LUNA_ORDERS_20260928.md, POST_adam_bob_charlie.md.
- SENT_ROWS.txt (1,017 lines), AK3_CLASS_ROWS.json, ATLAS_AC_LEDGER.md, SCORE_ZOO.md, dw_bounds_20260928.json,
  dashboard.json, submit_log.jsonl, targets_codex_oddeasyB.json, CODEX_TRANSCRIPT_AUDIT_20260928.md.
- Data directories: `boards/` (140 snapshots), `changes/` (21), `teams/`, `record/` (session 1 record page: families,
  ideas, paths, proof, template), `downloads/` (1757.txt, 2545.txt), `queue/` + `queue/sent/`, `inbox/` +
  `inbox/sent/`, `sweeps/` (+ handled.txt).
- `ledger/`: p2_hump_test, p2_beam_ab, atlas_beam_ab, score_zoo, p2cap_exact, sac_ms_bs, sac_fastpeel_targets,
  ms_families_by_w, codex_yxxyx_generator, codex_yxxyx_trace(.py), codex_commutator_lisitsa.md, crossrow_r2,
  crossrow_r2i2_sac, crossrow_roads_ac/sac, crossrow_windowed(2), bob_macro_library, BOB_move_rhythm,
  bob_rhythm_results_v1, luna_sacbeat_screen (+ baseline/diverse), rn_p2_deep, exact_capped_runs, beam_unk15,
  sac_rank2_probe.log, codex_abc_* (23 files), xecho_20260928_INVALID_noecho.log (kept as a failed control).
- `research/acc/atlas_drive/THE_OPERATOR_FIRST_ATLAS_20260827.txt` (8515b50).
- `research/acc/proof_track/ms_lisitsa_ak3_20260928/`: README.md, MS_Lisitsa_audit.md, ms_lisitsa_replay.py,
  ak3_p_to_ak3_replay.py (3cbd3ef). **AK3Audit.lean is MISSING.**

**Sweep state** (repo backup `live/sweeps/*_cap.jsonl` vs targets):

| Sweep | Progress | State |
|---|---|---|
| easy | 3/27 | stopped 07:14 |
| midB | 17/129 | stopped 07:14 |
| midD | 14/130 | stopped 05:34 |
| k2ac | 7/7 | done |
| sacbeat | 9/89 | stopped for good 09:22 |
| p2ms | 18/18 | done, no paths |
| p2a | 144/308 (scratch) | running (winner arm) |
| p2b | 134/307 (scratch) | running (winner arm) |
| p2n4 | 2/2 (scratch only) | done, no path |
| p2c (lead, new 12:22) | 0/169 (scratch only) | running: tails of p2a/p2b, reversed and interleaved |

Also in the repo: p2c_targets.json (**1,506 rows, session 1's lane, 754db2f**), p2sweep_targets (615),
near1_targets (16), luna_targets (5). See the name clash in §8g.

**Artifacts:**
- Tracker https://claude.ai/artifact/PesMNAWMhazVqhNx5DpP5u (db collection `dash`, 8 docs, v13).
- Results Map https://claude.ai/artifact/4TTVZS1uHDZJ9qLzNAQzmB (v3).

**Background at ~12:29Z:**
- Sweep watcher restarted 12:11 after marking ac-00222 handled.
- Inbox watcher running.
- Board watcher started 11:43 with an 8-hour limit (ends ~19:43Z).
- Lanes p2a/p2b running.
- Lane p2c started 12:22 (169 rows). Level beams stopped by PID at 12:21.
- Builder helper (BEAM_DUAL) running.
- Hourly check-in `trig_01Fuaebji8ytWZZG32nYhpNn` fired at 12:14. It was re-armed at 12:22 as
  `trig_01N9wMs83L5Awb49JGVHpX2A` (fires 13:23Z); that prompt tells the lead to read and commit this digest.

---

## 8. Open threads, promises, unanswered questions, untested ideas

### 8a. Questions to the user that are still unanswered
1. **Main AI's name** for the proof draft's provenance placeholder (asked 01:40). The draft cannot be filed without it.
2. **High-RAM machine or Colab high-RAM** for a few hours (asked 02:02). The lead offered to package the exact
   search (`colab_acc_search.py`, `make_T9_zip.sh` exist). Memory is the wall: it would reopen ac-06969 (caps 33+),
   ac-00145 (0.5 point) and the stopped sweeps.
3. **Allowlist** competition.sair.foundation, sair.foundation and docs.sair.foundation (asked 01:29), so the lead can
   read the Contributor Network proof tracks.
4. **Allowlist** arxiv.org, zenodo.org, www.sciencedirect.com and livrepository.liverpool.ac.uk (asked ~11:40), or put
   the PDFs in Drive. The user sent the audit instead; the Lisitsa MS paper text and its two structure conjectures,
   word for word, were never read directly.
5. **Attach atlas_cards.zip (16 MB, Aug 22) and the Sep-12 bundle (3.5 MB)** in chat (asked 04:24). The Drive tool
   can't pass them.
6. **Attach AK3Audit.lean** (asked 11:47). Only a ChatGPT sandbox link came, so the file was never received. It also
   wasn't in the user's repos or Drive, and the container has no Lean toolchain.
7. **Which other "old github" repos** to mine (asked 04:36; yang-mills-lean, suns-lean, three-body-lean,
   spectral-stability-lean, what-transport-keeps-lean were offered).
8. **"Was that the road you meant, or something else?"** about the 01:27 hint (asked 01:30).
9. Minor: "Want the verse on a page with the four sectors drawn as a diagram, or plain text?" (01:46).

### 8b. Things waiting on the user or a human action
- **File the proof track on the SAIR site.** `tools/acc/proof_track/DETOUR_WIDTH_ON_BENCHMARK_ROWS_DRAFT.md` has not
  been submitted, and its AI-name placeholder is unfilled.
- Proof-track rule R6: no single-line **beat** (1.0) happened this session. The +1.0 on 03060 was two k1 ties. It has
  a win-log entry in METHODS_PLAYBOOK but no WIN_TEMPLATE write-up. A write-up would still be useful.
- T9 upload to GitHub is on hold until the user says so.

### 8c. Unsent lines and near-misses
- **sac-00222 42 (k3, ~0.125) is queued and unsent**, waiting for 2 more lines (R4). Re-verify with a fresh pull ≤5
  minutes before sending.
- P2-lane near-misses at ~12:20 (ours vs record, k):

| Row | AC | SAC |
|---|---|---|
| ac-00222 | 42 vs 41 (k3) | tie queued |
| ac-02717 | 38 vs 37 (k9) | 40 vs 38 (k1) |
| ac-04211 | 33 vs 32 (k3) | 35 vs 34 (k4) |
| ac-04586 | 40 vs 39 (k11) | 41 vs 40 (k2) |
| ac-03719 | 37 vs 35 (k1) | 38 vs 36 (k2) |
| ac-03871 | 32 vs 30 (k1) | 34 vs 32 (k1) |
| ac-05818 | 36 vs 34 (k2) | — |
| ac-08031 | 37 vs 35 (k1) | 39 vs 37 (k4) |
| ac-06045 | 38 vs 36 (k1, after splice) | — |

  The (y,x) shortcut failed on all the SAC ones.
- Earlier near-misses still open:
  - ac-00145 40 vs 39 (k1, worth 0.5); caps prove no path within 30 moves from start 15.
  - ac-05064 38 (k2).
  - ac-06969 41 vs 38 (k2).
  - ac-09311 43 vs 42 (k1).
  - ac-04346 27 vs 24.
  - ac-06936 30 vs 26 (SAC 28 vs 27).
  - ac-02341 35 vs 29.
  - ac-09243 36 vs 32.
  - ac-05521 34 vs 31.
  - ac-03919 30 vs 27.
  - ac-00766 34 vs 33 and ac-00974 26 vs 24 (Bob's; need longer windows or a different road).
  - ac-01104 (no path within total 32).
  - ac-02962 AC35/SAC37 k1 (value 0.75, was in sweeps).
  - ac-00441 32/34 k2.
- 8 rows where SAC record = AC+1 and we lack the SAC line: yx failed on 00021, 00201, 02446, 01639, 05668, 05835 and
  03789 (00487 and 05091 are done).

### 8d. Work that was stopped or lost and never resumed
- **Exact sweeps easy (3/27), midB (17/129), midD (14/130):** stopped 05:34 / 07:14 for P2. Progress is backed up in
  `live/sweeps/`; they resume with `ops/sweep.sh NAME BUDGET JUMP PROBE` (midD: `sweep.sh midD 60000000 5 10000000`).
- **sacbeat beam:** paused with kill -STOP at 04:57 for Bob's A/B, then stopped for good at 09:22 at 9/89 rows.
  - Top targets: ac-03179 55/59, ac-04396 68/73, ac-08568 74/77, ac-09697 76/79, ac-01791 81/94 (need ≤91),
    ac-01417 81/85.
  - Luna's 5 rows are excluded.
- **Three-arm beam A/B (old vs Schur excursions vs shadow)** was lost in the 03:39 restart. The lead promised "I'll
  rerun it when a core frees up" and never did. Bob's A/B and the atlas A/B are different tests.
- **BEAM_SHADOW** was tested on ac-03305 only; the lead said it "needs a wider test".
- **ac-06969 caps 33+** and **ac-00145** need memory beyond ~180M states.
- Lost in the restart and never rebuilt: the ~150 finished sweep rows. The ac-01104 rerun was later covered by k2ac.

### 8e. Pending results (running or unreported at ~12:29Z)
- **BEAM_DUAL** A/B (builder helper). 14 interim runs in scratch `dual/`; it will write
  `ledger/dual_beam_ab_20260928.json`. The acc_beam.c WIP is on the branch (39cda03) but unverified. Adopt it if it wins (DUAL0.75 found
  05558 24/26 and 07435 26).
- Level-cost beams: two-level a=4, a=8 and finish m=31 were stopped at 12:21, unfinished. They could be rerun if
  the row-op argument needs more data.
- **Session 1:** masked exact n=4 at caps 25/27 with the 10-move set (a result ≤47 would give the leaders' n=4 shape);
  n=4 r1-only comparison; macro beam n=5 and MACW=1.
- Lanes p2a/p2b (144/308, 134/307) and the lead's tail lane p2t (169 tail rows; renamed from p2c) on the winner arm. When p2c meets p2a/p2b's
  progress, stop the duplicate lane by PID (check-in prompt).
- Next check-in 13:23Z (`trig_01N9wMs83L5Awb49JGVHpX2A`).

### 8f. Untested or unbuilt ideas (exhaustive)
From the atlas ledger's top 8:
1. Per-class quota: done, it works.
2. Rank blocks by x per move (B69): ill-posed as letters. **Needs a group-aware mass**, such as the chain level
   index (k, a).
3. **Transfer a solved small-n path to larger n in the same MS(n,w) family (B47/B44/B60).** The R_n part was dropped
   (open problems). The general version is untested.
4. **P3** (three multiplications deep) for hump rows where P2 fails.
5. **Primitive-relator stop (B83 / acwindow Lemma A):** 0 of 2,672 unsolved rows reach a primitive in 2 moves. The
   path builder was never written, and the cheap stop test in the beam is untested.
6. **SL(2,p) shadow as a tie-break under P2** (BEAM_P2=2 + BEAM_SHADOW is wired but not run).
7. **Finite-order exponent-sum moves in the hump (B13/B51).**
8. **Stable AC hump in the stabilised slot (B58):** one exact rank-3 run on ac-03305.

From B96 and the lead:
- **Two-ended shortening:** take Codex's long valid chain path and shorten it from both ends with P2 or exact search.

From the repo mining:
- **Extend the AK(3) class walk past 26 letters** (1,794 unsolved rows start at ≤26 letters).
- **Cyclic-class grouping of rows** (`house_walk_resumable.py`): solve one row, get the whole class.
- **E1** min/max beam reserve; **C1** macro filter by exponent-sum class; **E2** pair synergy I(a,b); **U2**
  Heisenberg quotient.

From the score zoo and songs:
- Cage bit / symmetry ranked higher as a beam tie-break: key P2 | comm_len | cage | P1m | klen needs a beam A/B.
- True L2/L3 rotation lookahead in the beam; it survived only offline.
- comm_len as a **phase trigger** that switches to an endgame solver (Codex 11:52Z; only a local 1.2M-state test).
- **End-length decay rate** as a row-type diagnostic ("some collapse like square root, some drop linear"), not built.
- Session 1: a **beam key rewarding progress toward y = x^(2^n−1)** ("the count"), not built.
- "Look close or far, same walk": the leaders' n+1 path contains the n path as a block. Untestable without their path.

Chain / MS:
- **Leave the level shape** (row-op argument): search n=4 (record 48) for routes where r0 is not a BS conjugate at the
  midpoint, or both relators carry long x-runs. This is the main open research target.
- **Mirror 2a-level chaining** (conjugate r0 by x instead of X) was partly analyzed: ~2 moves per x. A different
  mechanism is needed.
- **106 second words where small n is solved and bigger n is not** (e.g. YXYxYx: n=2 solved, n=3..10 unsolved by
  every team). Each would be a 1-point first solve (ORDERS_luna_ms "Also open").
- 480 more MS rows are written in rotated, inverted or mirrored spellings (256 unsolved): **normalize before grouping**.
- Stable AC fast-peel beat lane on the 68 chain rows. It needs a build ≤1.55–1.87 moves per crossing; also "a second
  block level for the G's" and doing the build's x-mass in rank 3.
- Ask to session 1 (IDEAS 05:5xZ): make `ms_construct.py` stop at (x, y X^m) and write the prefix so the lead can
  append the fast tail. Status unknown.
- YYXYYxyyX chain (cheap, sub-exponential?): not studied.
- **Record law** rec(n) − rec(n−1) = 2^n + 1: unexplained.

Other:
- Crossrow at radius 2 with more path memory (session 1: "radius 2 when memory bigger").
- Ledger #2 needs a better measure.
- Combined capped + corridor exclusions for ac-00145 (39) and ac-05064 (38) (ChatGPT/Codex, 02:00).
- Commutator-load **pseudospectral invariant** that predicts detour width before search (open question in draft §4a).
- Disk-backed or bidirectional exact search to push caps 2–4 higher (the top ask to research AIs; Charlie's
  `acc_capped_disk.c` pilot matched but slowed under 8 GB pressure).

### 8g. Coordination and housekeeping
- **Luna vs Codex** on the SAC-beat rows: both screened; the lead told the user "Let Luna or Codex take them, not both".
  This was never formally settled; nothing was found at W=20k.
- **Inbox housekeeping, DONE 12:40Z (moved to `inbox/sent/`):** 9 handled files were still in `live/inbox/` (03028, sac_mirror_ties_13, 09989,
  ac_roads_ties_20, 07004, p2_01629, p2_03305, 04278, atlas_00487). Only 2572 was moved to `inbox/sent/`. The watcher
  relies on inbox_seen.txt in scratch.
- **Name clash, RESOLVED 12:33Z** (lane stopped by PID, renamed **p2t**, restarted; session 1's 1,506-row `sweeps/p2c_targets.json` verified intact; never name a lane p2c): the lead's new scratch lane `work/p2c_targets.json` (169 rows) has the same name
  as session 1's committed `research/acc/live/sweeps/p2c_targets.json` (1,506 rows, AC records 46–60, 754db2f).
  `tools/acc/ops/watch_board.sh` copies `$S/work/*_targets.json` and `*_cap.jsonl` into `live/sweeps/` every 30
  minutes, so the next backup will **overwrite session 1's p2c targets** with the 169-row list (and create a p2c
  cap file that mixes the two meanings). Rename the lead's lane (for example p2t) or restore 754db2f's version
  before committing sweeps/.
- **Commit state:** at ~12:29Z the BEAM_DUAL WIP in `acc_beam.c`, the p2a/p2b lane backups, the 12:13Z
  board/leaderboard/changes snapshots and a draft of this digest were committed together by the lead in 39cda03.
  The BEAM_DUAL code on the branch is therefore **unverified work in progress** until the builder reports.
- Competitor repos cloned at the start into scratch `ref/` (nahomar/andrews-curtis-solver,
  Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE) are out of scope; do not use them.
- Auto-mode classifier "no verdict" at 07:28, 08:02 and 09:04–09:05 blocked sends and bash. Retry at the next wake;
  don't loop.

### 8h. Promises made by the lead and their status
- "I'll rerun it [three-arm beam A/B] when a core frees up" (03:42): **not done**.
- "If you get a high-RAM machine … I'll package the exact search": waiting on the user.
- "Attach … and I'll unpack / archive it" (atlas zips, AK3Audit.lean): waiting on the user.
- "Name them and I'll add them" (old GitHub repos): waiting on the user.
- "I'll take #2 and #3 myself" (atlas ledger, 09:57): #2 found ill-posed; #3 only the R_n part (no path; dropped).
- "Adopt BEAM_DUAL if it wins; splice across its paths": pending.
- "Keep the Results Map and Tracker current": through v3 / v13 as of 11:54.

---

## 9. Missing or scratch-only items

Scratch = `/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad`. It is not durable:
the 03:39 restart rolled it back.

**Missing entirely**
- `research/acc/proof_track/ms_lisitsa_ak3_20260928/AK3Audit.lean` (never received).
- The Zenodo ZIP `MS_supplement_v2.zip` (helper sandbox only; `ms_lisitsa_replay.py` needs it).
- `ledger/dual_beam_ab_20260928.json` (not yet written).
- atlas_cards.zip and the Sep-12 atlas bundle (Drive only).
- Unread Drive items:
  - "CURRENT_TASK — ACC Atlas Handoffs" Google Doc (1_8lgqlKH5j-Y2FSOU1qewDMOorlurQ2sAmuBNVNun08)
  - MAD_HATTERS_ATLAS_CASCADE_MORE_AC.txt (1eaBsVawFGNxqATVIaAnSI90Tgs6Mf1FG, 56.9 KB, lists of AC moves)
  - AC_idle_wheels_housings_light_v3.pdf (1ji3AdtipA7Gy5WIVebL6o5JsQzKHyRHA, 1.8 MB) and its md
    (1zlpzFaS4qv1iwdxEl4aoxmDD8Q_iYn06)
  - ACC_BASIN_PORT_ATLAS_FIRST_PASS (680 exits → 23 port classes), ACC_WHITEHEAD_EYE_RETURN_20260917.md,
    LEAN_ATLAS_RELEASE_INDEX_v1.md, ACC_PRIOR_ART_CORRIDOR_HANDOFF_2026-09-13.md
  - Session 1's "00_Mad_Hatters_ACC_Combined_War_Room — full preservation 2026-09-16"

**Results recorded only in the transcript or scratch (not in IDEAS or ledger)**
- Skip test a=3 final: cap 17 → 21 and cap 21 → 21 (51M states, 5,158 s, complete; path
  `0 4 11 4 11 4 11 4 1 12 3 6 2 4 4 4 4 4 4 4 8`). IDEAS still says "a=3 running".
- The lead's n=4 H-beam from the phase-A state: AC 54 from the state + 10 = **64 total** vs record 56
  (`scratch/work/ms_n4_path.txt`). IDEAS still says "Running".
- Level-cost beams: a=8 none (235 s), a=15 none (331 s), two-level a=1 15, a=2 27 (`scratch/chainfin/levels.out`).
  The IDEAS 12:10Z entry has only the m=3/7/15 and a=1/2/4 rows. The 12:30Z exact checks are logged; their paths
  are in scratch `lvlx4/` and `fin15/` (a=4 cap 21: AC 22 `1 4 10 4 10 4 8 10 12 2 5 7 4 6 3 0 4 4 4 4 4 4`;
  Y x^15 cap 23: AC 25 `1 6 5 6 5 6 5 11 5 6 3 7 4 2 2 2 2 2 2 2 4 1 2 4 4`).
- `lisitsa_find.py` (symmetry matcher; 28 hits) and the Lisitsa-vs-board comparison table (§5): scratch only.
- BEAM_DUAL interim table (`scratch/dual/ab.log`, `ab_results.jsonl`).
- P2-capped raw runs (`scratch/p2cap/grid.jsonl`, logs); the summary is in the ledger.
- P2 tie-break ranker `scratch/atlas_ledger/p2_tiebreak_ranker_20260928.json` + test script (Tests A/B raw).
- Bob A/B raw (`scratch/ab/plain_t8.jsonl`, `bob40_t8.jsonl`, INVALID file kept); the summary is in IDEAS.
- Score-zoo raw (`zoo_*.json`, `zoo_full*.log`); P2 test raw (`p2_run1/2.json`).
- Near-miss list and (y,x) failures of 12:19 (`scratch/yx_batch.txt`); now in §8c.

**Scratch-only code (useful, not in the repo)**
- (12:40Z: `acmoves.py`, `value.py`, `lisitsa_find.py` now also in `tools/acc/scratch_utils/`.)
- `acmoves.py`: Python ac-r2-v1 moves, `run(R, path, show)`. Used constantly.
- `value.py`: values lines vs the latest board.
- `block_search.py`: ledger #2 test.
- `lisitsa_find.py`.
- `p2bench/p2bench.c`, `p2prof.c`: P2 speed bench.
- `p2beam/pin.c`: locks T8 in RAM. `p2beam/p2port_test.c`.
- `overlap_probe*.py`, `wh_probe.py`, `t_collect.py`, `t_self*.py`.
- `atlas/*.py|.c`: builder A/B harness (ab.py, ident.py, build_ledger.py, comm_test.c, atlas_test.c).
- `dual/*.py`: the DUAL harness.
- `chainfin/run.py` (copied to the repo as `chain_rowops/level_beam.py`).
- `work/p2n4_targets.json` / `p2n4_cap.jsonl`.

**Scratch-only binaries and tables** (rebuild from repo sources)
- `acc_beam_x`: winner, from acc_beam.c at 07e483f+.
- `acc_beam_y`: DUAL, from the WIP in 39cda03.
- `acc_beam_p2`, `acc_capped`, `acc_capped_p2`, `acc_window`, `acc_opt`.
- `p2bin/`, `p2xbin/` symlink dirs.
- `p2beam/T8.tab` (640 MB, SHA 38f05b56…). Rebuild with `work/acc_opt tball 8 40000000 …` per WORKING_codex_abc.
- `work/T9.tab` (4.48 GB, SHA 48a81fea88f49c5c9499bde3738b813792c405bedff41b8ddc229f9aee7bb053; **do not upload**).
- `sair/`: official repo clone at a0fd6e6, with the verifier and manifest.
