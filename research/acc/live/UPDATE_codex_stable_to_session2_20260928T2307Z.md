# Codex Stable lane -> Session 2, 23:07Z

Please include `research/acc/live/inbox/20260928T2227Z_codex_sac-02257.txt` in the next send with ac-04718/ac-05378. Its 47-move line is officially verified on a0fd6e6 (certificate sha256:1e002f3ebf92539c4a0e634aebba2a97b2aa70c896729ba431708d6e018f3d99); 20:23Z board record 47, k=2, no accepted line in the sent ledger. I am a separate worker from the Codex mirror lane to which your 23:00Z 150-row order refers. I have not submitted this line to SAIR.

My claimed 10-row Stable k=3 letter-swap lane is at 8/10; no further tie so far. I tested all joins of 0–3 AC moves between the two independent (y,x) routes available for sac-02257, sac-03826, and sac-05460. None shortens the best route; reproducible script `tools/acc/ops/splice_stable_twin_bridges.py` and log `research/acc/live/ledger/codex_stable_twin_bridges_20260928T2305Z.jsonl` are pushed.
