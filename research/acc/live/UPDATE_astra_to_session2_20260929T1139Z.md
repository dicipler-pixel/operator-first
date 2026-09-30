# Astra to session 2 — 2026-09-29 11:39Z

## Window diagnosis and mitigation
Your04953 report is confirmed. Rebuilding current-branch acc_window with gcc -O3 did **not** cure the fault here: input38 shortened to37, then pass2 failed with exit3, "walk to s_j failed". Probe used a separate workdir, with28GB disk free. Source hashes, commands, stdout and error tail are in ledger/astra_window_rebuild_20260929T1135Z.json. Root cause is still open; I have not installed or called the rebuild a fix.

The audit previously retained the verified original after this known failure, discarding valid intermediate PATH lines. It now verifies those intermediate full paths with the pinned core and supplies the shortest valid one through a separate CompletedProcess attribute; run_beam_raw.py consumes that attribute. Original subprocess stdout, exit3 and failure details remain intact. This is opt-in under the existing audit env; production beam settings are unchanged. Tests on three real failures recover04953 37 and01768 38, retain03068 51 where no shorter valid PATH exists, reject invalid PATH0, and refuse unrelated exit2. See ledger/astra_window_recovery_checks_20260929T1135Z.json.

Recovered routes are in sweeps/astra_recovered_windows_20260929T1135Z.jsonl:
- ac-01768 **41→38**, Stable43→40; both official-clean but still3 above records35/37. Use for junction splice; no inbox line.
- ac-04953 37/39; already queued by you, **do not duplicate**. This is your reported hit, not new exclusive Astra credit.

## Wide pilot
Completed and pushed first row ac-04316 AC45/SAC47 versus43/45, no width gain. Its finished11:12:48 beam was recovered without rerunning it. Row2 ac-07194 is running atW200000/depth46, original two-eyes flags. The resumed runner is explicitly bounded to the first3 targets; row4 will not start before the agreed gain review. Full process evidence and restart details are in WORKING_astra.md. Latest observed11:39:23Z runner597432/beam597433/watcher594443; one completed row, no hits or within-one misses.

## User-requested unsolved target scout
Read-only join, not a new lane or search claim: all2605 shortlisted rows remain unsolved on saved11:18Z board. Of231 MS catalogue classes,86 have an exact adjacent-n solved representative and **45 classes/75 rows** have a route in your946-row team bundle. All946 routes replayed cleanly on pinned official core. Full map, source IDs, lengths, certificate hashes, input provenance and reproduction script: optimality/experiments/astra_unsolved_scout/.

Examples:09310←05703(26);03390←05653(28);09194 and04413←08646(31);02412's five-row class←01784(56). Neighbourhood in n is not a short AC bridge, and canonical matching does not supply the alignment moves. These targets remain under session1/Git's family coordination; I did not duplicate Bob's11:05 generator-change transfer. Proposed complement: after owner clearance, a≤10-class pilot keeping several distinct transported-prefix states and searching for explicit connections to verified suffixes under a fixed budget. The current firstsolve script retains only one shortest prefix. No new solve is claimed, and your chain A/B remains the production decision point.

Only you submit. No SAIR API reads or submissions here.
