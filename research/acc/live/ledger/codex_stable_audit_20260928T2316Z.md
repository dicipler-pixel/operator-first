# Codex Stable audit — 2026-09-28 23:16Z

Input: `sweeps/codex_mirror_20260928T230855Z.jsonl` (80 rows, 36 AC routes). Board snapshots: AC 20:50Z, SAC 20:23Z. Pinned verifier: a0fd6e6.

For every one of the 36 AC routes, I checked its AC prefix + legal rank-2 destabilization finish, including inversion of a negative singleton relator, and verified any at-record Stable finish. Only sac-05818 (36, already sent in submission 2701) and **sac-09839 (46, snapshot record46 k1)** tie. The latter is in `inbox/20260928T2312Z_codex_sac-09839.txt`, derived from the mirror worker's AC line, with stable certificate sha256:f1cdec4711f7d4ae0be2ac42b2d302c87a2fa0f71dfe93461a6939e6a27a58c4.

Exact local checks on the new ac-09839 44-move AC route: window8 and window11 completed without a cut (45? no: 44 unchanged). C16 reverse query on the 16 eligible swapped-prefix states found best Stable finish 47, above the 46 record. On the sac-02257 verified 47-move (y,x) road, window11 completed without a cut; all exact internal 0–3 move bridges also failed to shorten. These bounded negative checks do not prove global optimality.

The W40k (y,x) beam is still trying to beat sac-02257 at 46; do not repeat this exact run until its output is logged.
