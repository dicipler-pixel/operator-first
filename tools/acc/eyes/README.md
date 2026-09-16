# ACC eyes

An ACC eye is a deterministic function of a search TRAJECTORY (state sequence + move sequence),
recorded per step, per run. It is never a group invariant of the presentation: all pool
presentations present the trivial group, so any AC-invariant quantity is constant along every
path and cannot see a path, a rediscovery, or a dead end. Eyes are telemetry and indexing only;
they never prune a search and never certify anything. Only verifier replay certifies.

---

## Input provenance — what this repo actually has

The brief names five corpora. Checked at build time:

| brief input | status in this repo |
|---|---|
| (a) competition/examples training 424 | **present** — `tools/acc/finisher_v1/training_424_finished.txt`, 424 lines, each re-verified by the finisher |
| (b) `ACC_VERIFIED_SEARCH_PASS_20260915.zip` (922 paths) | **absent** — no such file |
| (c) hub `candidates.jsonl` / `verified_certificates.txt` (GPT/Grok/Gemini) | **absent** — no such files |
| (d) FAILED / PARTIAL runs | **partially present** — this session's cap-ladder and shared-ball runs, recorded as bounded misses |
| `ACC_UNSOLVED_CLASSES_0916.json` (Phase 6 targets) | **absent** — the brief says it will be placed in the hub; target IDs were taken from the brief text and checked against the 09-16 board |
| pinned SAIR verifier at `competition/tools/verifier` | **absent** — there is no `competition/` directory |

Nothing here was recorded from a corpus that does not exist. Counts in every report are
counts of what was actually read.

## Replay authority

The pinned SAIR verifier is not in this repo, so replay is done by `replay.py` — an
independent Python implementation of the 14 ordinary AC moves (`ac-r2-v1`, moves 0–13),
written from the move definitions and sharing no code with the C search engines. It is the
same replayer that independently confirmed the 19 submitted tie certificates.

**This is not the pinned verifier.** Every artifact produced here is marked
`replay_authority: "eyes/replay.py"`, never `official_verify_ok`. Anything destined for
submission must be re-replayed against the pinned verifier when that is available.

## Move set

    0  invert r0                 1  invert r1
    2  r0 <- r0*r1               3  r0 <- r0*r1^-1
    4  r1 <- r1*r0               5  r1 <- r1*r0^-1
    6..9   conjugate r0 by x, x^-1, y, y^-1
    10..13 conjugate r1 by x, x^-1, y, y^-1

Letters: `0=x 1=x^-1 2=y 3=y^-1`; inverse is XOR 1. Target is `(x, y)`.
