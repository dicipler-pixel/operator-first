# Astra → session 2 — easy rows 37–42 and safe restart (2026-09-29 08:57 UTC)

Six rows completed. Two tied both snapshot boards and were absent from fresh `SENT_ROWS`: `ac/sac-05871` 35/37 and `ac/sac-09663` 33/35. Both inbox files are pushed. `ac-06904` is the first one-move near miss in this lane: AC36 vs35 and Stable38 vs37. `ac-01874` was +3/+3, `ac-01768` +6/+6, and `ac-03454` bounded nopath.

All available paths pass pinned official SAIR `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`. Checks and restart evidence: `ledger/astra_easy_checks_rows37_42_restart_20260929T0857Z.json`. Sweep is 42/171 at `f5eaef2`. Fresh `fe_cap` has34 rows with no collision.

The prior runner and watcher were absent at08:55:38Z; the stop cause is not established. Its last incomplete row `ac-01815` had an exit0 beam and completed AC window but no sweep entry. No completed row was repeated. The exact guarded v2 command restarted from the42-row JSONL checkpoint after full T8 checksum verification. Actual runner PID435218 and one beam are live on `ac-01815`; watcher PID435551 is restored from offset42. Only session2 submits; no SAIR API reads or submissions.
