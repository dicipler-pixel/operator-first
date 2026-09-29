# Astra → session 2, 2026-09-29 16:20 UTC

The first-three W200000 pilot is complete and shows no gain versus the supplied gaps. Officially verified final lengths:

| Row | AC / record | Stable / record | Supplied gaps | Final gaps |
|---|---|---|---|---|
| 04316 | 45 / 43 | 47 / 45 | +2 / +2 | +2 / +2 |
| 07194 | 47 / 44 | 49 / 46 | +3 / +2 | +3 / +3 |
| 05423 | 37 / 33 | 38 / 35 | +3 / +3 | +4 / +3 |

All routes/checks are in sweeps/astra_wide_20260929.jsonl. 05423's raw paths exactly match p2a_cap's W20000 paths. Its AC window exited0 without shortening; the swapped window exited3 and retained its officially verified original core. No hit and no within-one miss. Completed third row in1449.9s by keeping the run actively observed; between-rally processes had repeatedly disappeared without a finished receipt, and those attempts were never counted as negatives.

Following your0800 instruction, no row4 wide beam was started. First mid-route restart is now04316, cut28 of the verified45-move AC path: old suffix17, depth budget43−28=15, W200000, unchanged H1/DIV.8/P2=2/QUOTA16/ELITE5000/DUAL.75, no chain. One beam. Guarded driver is optimality/astra_subprocess_audit/midroute_one.py; it recovers audit receipts, verifies full prefixed routes, and attempts both eligible windows. Claim and source-path hash are in WORKING_astra.md. More mid-route cuts will follow the saved attempt ledger; do not restart the wide list from row4 automatically.

New window diagnostic, not a claimed fix: the same04953 control and matching source blobs produce different behavior between builds. Production gcc -O3 exits3 after recovering37; gcc -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer exits0 with FINALPATH37 in663.8s, with no sanitizer diagnostic. Both37-move paths replay officially. First B7-count difference is zero-based ball33 in pass1: native9,215,268 versus sanitized9,804,914. First33 prior ball counts match. A separate1,078-move comparison of native acc_opt against pinned Python core on all neighbours of both control routes found0 mismatches. This isolates build-sensitive behavior on one control but does not establish the cause or justify replacing production binaries. Both optimization level and instrumentation changed, so this is not a single-factor comparison. Evidence/build/source hashes: ledger/astra_window_sanitizer_20260929T1620Z.json. Production binaries unchanged.

No SAIR API reads, submissions, or duplicate inbox lines. Only team/owner submits.
