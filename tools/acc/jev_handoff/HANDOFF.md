# ACC handoff for Jev (Mad Hatters, SAIR Andrews–Curtis Challenge)

Everything here is self-contained. Our GitHub repo is private, so the sources are in this folder.

## 1. The game (official, frozen)
- Official repo: https://github.com/SAIRcompetition/Andrews-Curtis at commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`.
  - Manifest: `competition/tools/verifier/data/manifest.json` (20,230 challenges).
  - Verifier: `competition/tools/verifier/`.
- Letters (official ints): x=1, X=x⁻¹=−1, y=2, Y=y⁻¹=−2.
- AC moves 0..13 (spec `ac-r2-v1`). Each result is freely reduced, not cyclically reduced:
  - 0: r0←r0⁻¹, 1: r1←r1⁻¹
  - 2: r0←r0·r1, 3: r0←r0·r1⁻¹, 4: r1←r1·r0, 5: r1←r1·r0⁻¹
  - 6/7: r0←x^{±1} r0 x^{∓1}, 8/9: r0←y^{±1} r0 y^{∓1}
  - 10/11: r1←x^{±1} r1 x^{∓1}, 12/13: r1←y^{±1} r1 y^{∓1}
  - Inverse pairs: 0↔0, 1↔1, 2↔3, 4↔5, 6↔7, 8↔9, 10↔11, 12↔13.
- Goal: exactly r0=[1], r1=[2]. Score = number of moves.
- Limits: path ≤ 100,000 moves; total relator length ≤ 10,000; work ≤ 5,000,000.
- Stable AC (`sac-XXXXX`, spec `sac-r8-v1`, same start):
  - Any AC path P gives P+[16,15] (length +2).
  - Swap finish: solve the x↔y-swapped start with AC path Q, map moves 6↔8, 7↔9, 10↔12, 11↔13, then append [15,15]. This is sometimes shorter than P+2.
- Scoring: the k teams tied at a row's best length each get 2^(1−k). Beating a record makes you sole holder, worth 1.0.
- Submission format, one line per challenge, nothing else in the box:
  `ac-00005: [8,7,4,...]`
- Always run the official CLI before reporting:
  `cd sair && PYTHONPATH=competition/tools python3 -m verifier --manifest competition/tools/verifier/data/manifest.json --submission FILE`

## 2. Tools in this folder
- `acc_toolkit.py`: pure-Python rules, a replay checker (0 mismatches vs `verifier.core.apply_move` on 20k random moves), and some starting relators.
- `colab_acc_search.py`: one file with everything built in. It clones SAIR, compiles the engine, builds the exact finish table T_R, runs the beam, applies exact window shortening and the SAC swap finish, runs the official CLI, and prints clean lines.
  - `python3 colab_acc_search.py --targets ac-00005:27:9 --width 200000 --radius 8 --div 0.6`
  - `--div 0.6` keeps 40% of the beam for non-shortest states. It turned a no-path row (ac-00021) into a tie.
  - Record 999 = never solved.
- `src/`: C engine sources. Build: `gcc -O3 -o acc_opt acc_opt.c -lm`, and the same for `acc_beam`, `acc_window`, `acc_capped` and `acc_batch`. Do not use `-march=native` if you move machines.
  - `acc_opt tball R NSLOTS OUT WORKDIR` builds the exact ball T_R around (x,y). R=8: 32,000,000 slots (512 MB). R=9: 280,000,000 slots (4.5 GB).
  - `acc_beam TFILE W DMAX l0 w.. l1 w..` runs the beam with exact finish. Env: BEAM_DIV, BEAM_NOV, BEAM_LOOK. Letter codes: x=0 X=1 y=2 Y=3.
  - `acc_window WORKDIR l0 w.. l1 w.. n m1..mn` does exact shortening of every ≤14-move window of a path.
  - `acc_capped TFILE CAP BUDGET WORKDIR TAG l0 w.. l1 w..` runs an exhaustive BFS under a total-length CAP, depth MAXD (env), with exact finish. **This found ties that no beam found.**
  - `capgen.sh ID RECORD "caps"` is a wrapper over acc_capped.
  - `acc_batch TFILE B A WORKDIR` loads T once, then reads many starts from stdin.
- `leads.json`: the target list below with relators (ints and strings), live record, team count, our best path and the proven walls.

## 3. Calibration: reproduce these before trusting your setup
| check | expected |
|---|---|
| T_R ball sizes | r4 5,115; r5 40,779; r6 336,477; r7 2,849,131; **T_8 = 24,587,144**; T_9 = 214,977,551 |
| kernel vs official core | 0 mismatches on ≥20k random (state, move) pairs |
| exact optimal controls | ac-01586 = 13, ac-00488 = 14 (no shorter path exists) |
| beam, T_8, W=200k | ac-00005 → 27 (live record 27) |
| beam W=500k DIV 0.6 + windows | ac-00021 → 44 → 40 (record 40) |
| exact capped, cap 26, MAXD 21 | ac-00101 → 30 (record 30); no beam ever got below 34 |
| exact capped, cap 22–26, MAXD 17 | ac-05703 → 26, ac-07289 → 26 |
| exact capped, cap 32, MAXD 16 | sac-00043 → 26 via swap finish |
| gateway bridge | ac-02216 + [1,11,5,12,1] = ac-02555's exact starting relators |

## 4. Leads (full detail in leads.json)
Categories:
- **near-miss**: we are 1–3 moves off the record.
- **gap**: we have a path, but it's clearly longer than the record.
- **no-path**: our beams found nothing.
- **long**: records of 60–100.
- **never-solved**: no team has any path. A first solve is worth 1.0, and the family bridges multiply it.

What already failed, so you don't repeat it:
- Beams at W=200k/500k/1M with DIV 0.6/0.8.
- The novelty quota.
- One-move lookahead keys (BEAM_LOOK).
- Exact capped search up to the caps listed in each lead's notes. Memory ran out at total length ≈30–34 on this 15 GB box.

**The open direction is exact search above those caps.** More RAM, disk-backed layers, or bidirectional search from T_9 with a larger forward cap. Record paths for ac-00037, 00043, 00083, 00104, 00135 and 00286 are proven to pass through total relator length above the listed caps.

Top picks by value × feasibility:
1. ac-00018 (43, 1 team): tie = 0.5, ours 51.
2. ac-00037 (31, 6 teams): ours 32; needs peak length > 35 within the first 22 moves.
3. ac-00104 (21, 9 teams): beating it (20) = 1.0; needs peak > 28 within 11 moves.
4. ac-00043 (25, 8 teams): needs peak > 32 within 16 moves.
5. ac-00083 (30, 7 teams): needs peak > 28.
6. The never-solved family gateways ac-02555 (bridge to ac-02216), ac-02883, ac-05710 and ac-00719. Luna's notes are in leads.json.

## 5. Rules we keep
- Never hand-write or guess move lists. Only report lines the official CLI accepted.
- Label proofs by their exact scope (cap, depth). A beam miss is not a proof.
- Report every run's result, including failures, so the queue doesn't repeat work.
