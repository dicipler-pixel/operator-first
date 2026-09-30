# ACC harness 1.3 — connected offline

The owner's exact 25 selected AC rows are now connected to their exact starts and the pinned official checker. Routine import, replay, receipts and dispatch limits run as code. Model-host commands remain unbound and worker dispatch budgets default to zero.

## Run from the repository root

```sh
python3 research/acc/harness/acc_synthesis/selftest.py
python3 research/acc/harness/acc_synthesis/harness.py status
python3 research/acc/harness/acc_synthesis/replay_saved.py
```

Python 3.10+ and the standard library suffice. No network or model account is needed for these commands. Replay writes durable events and receipts to `state/` and a report to `integration/real_replay_report.json`. A repeat invocation repeats this bounded replay; it is not a scheduled watcher. For a new candidate use `harness.py check PATH_TO_CANDIDATE.json`.

## What is connected

- All 25 exact starts and goals from the official manifest at `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`, the version pinned by the owner's repository handoff. The complete source manifest was checked against Git blob `accdb626ee08a06beea3f88dc7f351514c99eb27`; every selected instance hash was recomputed.
- The unchanged official checker under `vendor/verifier/`. The adapter pins its dependencies, move specs, selected instances and limits, and checks dependencies before and after replay. No SAIR solver or search recipe is imported.
- Owner evidence at `d3351066a05bf6262cacc30fdcb055d2e0942a94`: send ledger, archived acceptance logs, both 161-record pool files, the larger route archive and the 2,781-path known-roads export. Original files were checked against their Git blob hashes before extraction.
- The saved AC board generated at 07:10Z and pulled at 07:11Z September 30. Its original timestamp is retained. Eligibility expires after 300 seconds; import time does not manufacture freshness. The user's later pasted records and team counts remain separate in `selected_rows.json`.

## Actual validation

**57 local tests pass; the official checker passes all 63 upstream conformance cases. All 25 recovered routes across 10 selected rows replay correctly.**

| Row | Best recovered length | Pasted record |
| --- | ---: | ---: |
| ac-00037 | 32 | 31 |
| ac-00034 | 44 | 41 |
| ac-00012 | 52 | 47 |
| ac-00018 | 51 | 43 |
| ac-00022 | 56 | 44 |
| ac-00028 | 58 | 44 |
| ac-00003 | 92 | 40 |
| ac-00009 | 112 | 34 |
| ac-00005 | 27 | 27 |
| ac-00021 | 40 | 40 |

The last two are already ledger-reported accepted ties and need improvements. The other 15 starts are connected but have no recovered route in the inspected sources. This is limited source coverage, not a whole-repository absence claim. Accepted lengths 829 on ac-00010 and 999 on ac-00024 remain ledger evidence; their move lists were not recovered here.

A bounded check for exact repeated-state loops across these 25 paths found no shortening. This does not exclude other shortcuts. No new scoring line, live challenge API request, submission or model-worker call occurred. Historical board freshness withholds readiness while preserving exact replay results.

`integration/offline_plan.json` is the current target/seed map. `target_status.json` preserves the earlier narrower intake; it does not override the later recovered-route evidence. Replay reports include full official receipts and certificate hashes.

## Cost and model control

Automatic Luna retrieval and second-Sol candidate review are disabled by default. Candidates go straight to code replay; explicit `requires_model_review` work may request independent review. Intended roles are Sol for bounded implementation, a separate Sol for disputed code or reasoning, Luna for small interpretation tasks, and Astra for justified escalation.

Total and per-role dispatch caps are zero. `run` and `export` reserve a dispatch before launch or handoff. Reservations survive restart, and failed launches consume one. These are worker-launch caps, not dollar/token limits: the host bridge must enforce provider spending limits and account for multiple provider calls inside one worker.

To bind a host, configure each role's trusted argument-array `command`, reading one JSON request on stdin and returning one result on stdout. `workers/example_bridge.py` documents the boundary. Model names are intended host selections, not a claim that an external API supports those strings. Alternatively use the bounded file handoff: `export`, `heartbeat`, `accept`.

## Operational boundaries

The exact 25-row selection is hash-pinned. Other rows, including old queued tasks, cannot dispatch. Exact validity and board eligibility are separate. Improvements on already-held rows may pass; a previously accepted length or longer cannot pass when accepted-history evidence is supplied. There is no submission transport.

`stop --reason TEXT` persists and revokes leases. `resume` clears the stop without restarting tasks. Scoped failures retain their explicit reopening condition. The host must enforce its own memory, sandbox, network and spending limits. A local heartbeat proves process liveness, not mathematical progress. POSIX process groups are stopped on timeout; Windows hosts must supervise descendant cleanup.

The SQLite ledger is authoritative. Use SQLite backup for active databases rather than copying a WAL database file alone. Previous watches remain off. Model clients still need binding for agent work; code-only replay works now.

`scan_saved.py --targets integration/selected_rows.json --repo /path/to/operator-first --output integration/target_status.json` repeats the narrow saved-ledger import without network or models. Broader recovered routes are preserved separately with original source references.

`DESIGN.md` and `source_map.json` preserve the paper synthesis and its mathematical limits. The demo is explicitly a toy, separate from the real replay above. Third-party checker attribution and its Apache license are under `vendor/`.
