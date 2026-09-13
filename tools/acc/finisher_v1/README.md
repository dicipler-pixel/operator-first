# acc_finisher v1 — mandatory final stage before any ACC submission

`python3 tools/acc/acc_finisher_v1.py --submission <file> --out <new file>` (or `--candidates <jsonl>`, or
`--training` for the 424 official solutions). Never overwrites: the output path must not exist.

What it does to every path: official replay → earliest corridor state (exactly one relator a single
letter) → exact BFS to the target with total length capped at L_entry + 2, using only
`verifier.core.apply_move` → splice only if strictly shorter → official `verify()` on the spliced path →
write only accepted paths. The corridor mathematics is elementary and known (see
`../PRIOR_ART_2026-09-13.md` §3); the measured effect on the official solutions is ours.

## Controls (this directory)

| input | paths | shortened | kept | rejected | unknown id | moves saved | seconds |
|---|---:|---:|---:|---:|---:|---:|---:|
| `--training` (424 official solutions) | 424 | 359 | 65 | 0 | 0 | 950 | 3.6 |
| `competition/examples/sample_submission.txt` | 2 | 1 (ms-train-0160: 7 → 6, `[6,4,2,9,5,11]`) | 0 | 0 | 1 | 1 | 0.0 |
| `competition/examples/invalid_submission.txt` | 1 | 0 | 0 | 1 (original fails verify; not written) | 0 | 0 | 0.0 |

Each `*.report.json` beside the output lists per-path action, entry step, entry length, original tail,
exact tail, BFS nodes and the verifier's accepted length and peak.

Why it matters: the competition's efficiency leaderboard scores the shortest accepted path per
presentation (Tao/Fagan announcement, 11 Sep 2026). Cap 2 is conservative; a larger cap can only find
equal-or-shorter finishes at more BFS cost (max 11,205 nodes at cap 2 over the training set).
