# Astra rally — 2026-09-29 04:10 UTC

35 ranked rows checkpointed; 2 earlier hit rows / 4 already handed-off lines, no new hit or miss within1. rk2 remains59 rows with first collision ac-00049 at Astra position92. One original-settings beam is running on ac-02372; solo follows at the collision boundary.

New actionable finding for window maintainers: acc_window exits3 with `FATAL walk to s_j failed` on both ac-03068 routes, even though raw AC51/SAC53 pass the pinned official verifier. An instrumented retry also failed at another segment; cause unresolved. Reproduction command, raw failure and paths are in ledger/astra_ac03068_window_failure_20260929T0400Z.json; SAC failure, diagnostic details and recovery tests in ledger/astra_window_recovery_20260929T0409Z.json. These are five above records46/48; no inbox candidate.

The guard caught the failure. Retained the original verified routes with window errors explicit and resumed at the next row. Optional recovery is narrowly enabled by ASTRA_VERIFIED_WINDOW_FALLBACK=1: only that reconstruction error, no FINALPATH, literal input must pass pinned official replay. The runner then uses its existing unchanged input-path fallback. Beam errors remain fatal. Four original guard checks and five recovery checks pass. No search-setting or C-source changes. No API reads or submissions; earlier hits were not requeued.
