# Run evidence — ADVANCE-port hunt, 2026-09-22

Raw output from the run recorded in `tools/acc/WARROOM_2026-09-22_hunt_*.md`.
Engines: `research/acc/engines/acc_close.c`, `acc_boundary.c`, `acc_port.c`,
each sharing kernel lines 1-132 verbatim with `ac_shared_ball_v1.c`
(ac-r2-v1, SAIR commit a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e).

| file | what it is |
|---|---|
| `t16_build.err` | depth-by-depth trace of the T_16 rebuild |
| `t16_build.out` | final line: `BALL cap=16 states_b=129247304 depth_b=101`, wall 366 s |
| `ladder_*.txt` | first-pass cap ladders (escalating 5M/20M budgets) |
| `reruns.txt` | rungs re-run at the protocol's full 50,000,000-state ceiling |
| `ladder.sh` | the ladder driver |
| `rows.json`, `rows.args` | digit encodings, derived from `config/presentations.json`, never transcribed |

The first-pass ladders are kept alongside the reruns on purpose: three rungs
hit the escalation budget rather than the 50M ceiling and are superseded by
`reruns.txt`. Wall caps quoted in the war-room files come from the reruns.
