# Rows the first (search) session is working on (updated 23:44Z)

Exact capped search (acc_capped), one row at a time, on rows where the live **Stable AC** record is at most the AC record + 1.
On these rows AC+[16,15] can't tie, so the SAC path is found directly. Ordered best first (low SAC k).
The other session: skip these rows to avoid duplicate work. Hits are verified here and written to ACC_SUBMIT_* files.

ac/sac-02341 ac/sac-04566 ac/sac-04718 ac/sac-04908 ac/sac-02528 ac/sac-06973 ac/sac-08429 
ac/sac-08578 ac/sac-08889 ac/sac-02288 ac/sac-02057 ac/sac-02226 ac/sac-04716 ac/sac-07461 
ac/sac-01234 ac/sac-02921 ac/sac-03771 ac/sac-04431 ac/sac-07302 ac/sac-08945 ac/sac-09995 
ac/sac-06936 ac/sac-04081 ac/sac-05487 ac/sac-07119 ac/sac-04070 ac/sac-03719 ac/sac-08094 
ac/sac-08862 ac/sac-09628 ac/sac-09834 ac/sac-00380 ac/sac-01514 ac/sac-02000 ac/sac-02331 
ac/sac-02394 ac/sac-03868 ac/sac-04459 ac/sac-00259 ac/sac-02199 ac/sac-05353 ac/sac-08174 
ac/sac-09980 ac/sac-04485 ac/sac-06208 ac/sac-06540 ac/sac-07031 ac/sac-08705 ac/sac-04586 
ac/sac-07738 ac/sac-08777 ac/sac-09116 ac/sac-09709 ac/sac-09973 ac/sac-00487 ac/sac-05441 
ac/sac-06872 ac/sac-09857 ac/sac-04906 ac/sac-06456 ac/sac-02214 ac/sac-04624 ac/sac-05835 
ac/sac-08275 ac/sac-09736 ac/sac-03048 ac/sac-03789 ac/sac-05410 ac/sac-00356 ac/sac-01252 
ac/sac-09177 ac/sac-09916 ac/sac-01698 ac/sac-01855 ac/sac-06608 ac/sac-01860 ac/sac-06903 
ac/sac-08353 ac/sac-01859 ac/sac-02018 ac/sac-06192 ac/sac-06366 ac/sac-09173 ac/sac-06207 
ac/sac-10071 ac/sac-04197 ac/sac-04415 ac/sac-06122 ac/sac-06455 ac/sac-04051 ac/sac-06644 
ac/sac-02375 ac/sac-05067 ac/sac-05189 ac/sac-07849 ac/sac-00921 ac/sac-03905 ac/sac-04437 
ac/sac-09794 ac/sac-06707 ac/sac-01213 ac/sac-02606 ac/sac-00983 ac/sac-05400 ac/sac-01441 
ac/sac-06321 ac/sac-01639 ac/sac-02446 ac/sac-09469 ac/sac-00737 ac/sac-03246 ac/sac-08592 
ac/sac-01970 ac/sac-06373 ac/sac-06948 ac/sac-07920 ac/sac-09564 ac/sac-05127 ac/sac-08151 
ac/sac-01962 ac/sac-07550 ac/sac-09703 ac/sac-01918 ac/sac-04896 ac/sac-04194 ac/sac-01196 
ac/sac-02440 ac/sac-06137 ac/sac-03952 ac/sac-06186 ac/sac-07456 ac/sac-01474 ac/sac-01945 
ac/sac-07084 ac/sac-01293 ac/sac-07199 ac/sac-02150 ac/sac-07864 ac/sac-00974 ac/sac-05668 
ac/sac-08425 ac/sac-05937 ac/sac-04278 ac/sac-09437 ac/sac-05091 ac/sac-00654


## Helper side task — 2026-09-28 01:28Z

- Reserved `ac/sac-06095` for an endpoint-preserving exact path-shortening pass. Current ledger line: `ac-06095 47 42 1 behind`; the matching Stable row is `sac-06095 49 44 1 behind`.
- The pair was absent from both worklists when checked. This is a separate window-shortening lane; it does not change the existing 146-row Stable AC capped-search list.
- Input route: `ACC_CANDIDATE_06095_20260926.txt` (AC and SAC lines; official replay passed before reservation). Exact window tool: `acc_window.c`, gaps at most 14, radius 7 on each side, no relator cap. Verify any splice with the pinned official core; do not submit.
- Status update (2026-09-28): the 47-move AC route remains unchanged. Exact fingerprint-table searches found no replacement in peak-crossing windows of 15 moves (all six through effectively uncapped radius 7; cap 4096) or 16 moves (all six through cap 50). At cap 60 for gap 16, only windows [0,16], [1,17], [2,18] completed before the shell environment disconnected; no conclusion for the other three. Full counts and caveats: `research/acc/optimality/ac-06095_peak_window_audit_20260928.json`.
- Next: resume with gap-16 cap 60 on [3,19], [4,20], [5,21], then test longer windows only if the compute environment returns.


## Added 2026-09-28: unsolved "odd easy" rows (longest single-letter run <= 3), half A
ac-00413 ac-03467 ac-05932 ac-00568 ac-00738 ac-01657 ac-02216 ac-02422 ac-02576 ac-02828 ac-02923 ac-03471 ac-03772 ac-04967 ac-05710 ac-05762 ac-06349 ac-06576 ac-06785 ac-07128 ac-07653 ac-08168 ac-08892 ac-08984 ac-09827 ac-10066 ac-00066 ac-00491 ac-00927 ac-01632 ac-02178 ac-02414 ac-02698 ac-03293 ac-03545 ac-03706 ac-03949 ac-04095 ac-04411 ac-04516 ac-04661 ac-04888 ac-05037 ac-05499 ac-05856 ac-06194 ac-06734 ac-07064 ac-08223 ac-09138 ac-09545 ac-09920 ac-10099 ac-01314 ac-01760 ac-02282 ac-02370 ac-02554 ac-02922 ac-03476 ac-04172 ac-04559 ac-04947 ac-05379 ac-05512 ac-05618 ac-06022 ac-06743 ac-06789 ac-07258 ac-07507 ac-07938 ac-08044 ac-08765 ac-09081 ac-09242 ac-09822 ac-00998 ac-02029 ac-04764 ac-06008 ac-07205 ac-08166 ac-08627 ac-00035 ac-01138 ac-01905 ac-02247 ac-02763 ac-02854 ac-03183 ac-03920 ac-04578 ac-06616 ac-07856 ac-08089 ac-08524 ac-08870 ac-09399 ac-09969 ac-04113 ac-08915 ac-00595 ac-00958 ac-01020 ac-01982 ac-03238 ac-03726 ac-04919 ac-05875 ac-06398 ac-06896 ac-07237 ac-08065 ac-08354 ac-09860 ac-07245 ac-00825 ac-01184 ac-02249 ac-03648 ac-04328 ac-04471 ac-04591 ac-05385 ac-06145 ac-07568 ac-08545 ac-08828 ac-03331 ac-07406 ac-00294 ac-01484 ac-02425 ac-03085 ac-03166 ac-03387 ac-05462 ac-06064 ac-06447 ac-07087 ac-07963 ac-08863 ac-09498 ac-03410 ac-00067 ac-02707 ac-04553 ac-05317 ac-06211 ac-06328 ac-07615 ac-08707 ac-09295 ac-09809 ac-00940 ac-01033 ac-02541 ac-03004 ac-03973 ac-04968 ac-05882 ac-07257 ac-08169 ac-00501 ac-02074 ac-03574 ac-03650 ac-03788 ac-06017 ac-06824 ac-07895 ac-08972 ac-08724 ac-05066 ac-06554 ac-08436 ac-08848 ac-10075 ac-07677 ac-00562 ac-01800 ac-03496 ac-04243 ac-05159 ac-06783 ac-07883 ac-09478 ac-00419 ac-01024 ac-01753 ac-02691 ac-04022 ac-05203 ac-05601 ac-06052 ac-06354 ac-07081 ac-07594 ac-08015 ac-08867 ac-06568 ac-01192 ac-01650 ac-02175 ac-02681 ac-03110 ac-04119 ac-05509 ac-05827 ac-06387 ac-07442 ac-08090 ac-08669

Half B belongs to Codex: research/acc/live/targets_codex_oddeasyB.json

## 2026-09-28 07:45Z: P2=2 beam lane "p2c": AC records 46-60, k 1-3, not tied by us, not in any sweeps/*_targets.json
(session 2 has records <= 45). List: sweeps/p2c_targets.json. Unsolved half-A beam stopped (44 rows, 0 solves).

## 2026-09-28 15:30Z: session 1 resumes the helpers' stopped two-eyes lanes
Helpers stopped at 49/172 (15:04Z). Session 1 runs the rest on its machine: lanes dualAr (58 rows) and dualBr (58 rows)
= targets_dual_helper{A,B} minus sweeps/dual{A,B}_codex_20260928.jsonl. Same flags (BEAM_DUAL=0.75 etc.), T9 finish.
Hits go to research/acc/live/inbox/. Also resumes the reverse-ceiling probe at ceiling 11 (6M-state limit).

## 2026-09-28 19:45Z claims
- family-lane rows of TARGETS_RANKED.json (254): family transfer (tools/acc/family_transfer.py), work/family.jsonl
- Stable-AC gap rows (see ORDERS_charlie_v2): low caps here; Charlie high caps
- first solves: 100 unsolved MS rows (tools/acc/firstsolve.py)
- dualAr/dualBr (resumed helper rows) finishing; cyclers q_near and hunt3 continue

## 2026-09-28 21:45Z claim: long rows nobody runs
1,126 AC rows with records 61-90, held by 1-2 teams, not tied by us, not on TARGETS_RANKED or any targets/sweeps list
(board 20:50Z). List: sweeps/long_session1_targets.json. Two-eyes beam (dual flags, W 20k, record+2, window shortener),
lanes longA/longB, one-team rows first. Hits -> inbox.
- 18:50Z (session 1) claims **Git shape list 1** (targets_git_shape_20260929T1830Z.json, 192 rows). Lane shapeG: two-eyes beam, DMAX = record+2, BEAM_NOISE=2 seed 11. Order: not on an active list first, then gap 1 to 5, then value. Output: scratch work/shapeG_cap.jsonl. Other lanes can take seeds 12–14 on the same list.
