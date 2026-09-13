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
| `acc_finisher_sac_v1.py --stable-training` (424 official stable solutions) | 424 | 370 | 53 (+1 BFS node limit, kept) | 0 | 0 | 1320 | 183.5 |

Each `*.report.json` beside the output lists per-path action, entry step, entry length, original tail,
exact tail, BFS nodes and the verifier's accepted length and peak.

Why it matters: the competition's efficiency leaderboard scores the shortest accepted path per
presentation (Tao/Fagan announcement, 11 Sep 2026). Cap 2 is conservative; a larger cap can only find
equal-or-shorter finishes at more BFS cost (max 11,205 nodes at cap 2 over the training set).

## Upload rule and scope (adopted 2026-09-13)

- Official submission rule (`competition/examples/README.md`, lines 48–52): a challenge ID may repeat; the
  **first** path that verifies is selected and later lines for that ID are skipped **even if shorter**;
  later uploads can improve the record. So a shortened path goes in a **new upload**. Never append it
  under the old line. This tool always writes a fresh file and refuses to overwrite.
- Scoring is winner-take-all per challenge on the shortest verified path, so every candidate gets the
  exact tail pass before upload, and every already-uploaded path is worth re-running.
- Everything measured here is on training paths (near-monotone descents). No scored ac- candidate has
  been through the finisher yet; that remains untested until a real candidate exists.
- Stable AC: `acc_finisher_sac_v1.py` (257 moves, target `()`, corridor = some relator a single letter).
