# Codex archived at-record exact-window lane — claimed 2026-09-28 21:40 UTC

Nine AC rows whose accepted paths tie a recent live record, k=4..8, length<=80, and do not occur in current explicit worker claims: ac-06094 ac-00313 ac-01734 ac-04191 ac-01373 ac-04213 ac-09595 ac-08646 ac-09391. Exact input paths and sources are in `targets_codex_window8_20260928T2140Z.json`.

Method: `research/acc/optimality/acc_window8.c` checks every endpoint pair within eight moves via radius-3 and radius-4 balls and removes repeated states. Every input and shortened output gets replayed by pinned official verifier. Save all raw outputs and settings to ledger. Any path below live record goes immediately to inbox for Session 2 to submit. This is a path optimization lane independent of the running mirror beams.
