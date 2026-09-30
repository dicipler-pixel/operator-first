# ACC Memory-First Harness — start here

One selected setup for Jeromie's ACC work. Sol builds, an independent Sol reviews, Astra selects discriminating tests and changes of direction, Luna retrieves witnessed history, and ordinary code controls execution and exact-result gates.

**Built:** a runnable Python controller, durable task/evidence ledger, bounded worker transport, four role prompts, failed-attempt reopening, strategy-change gate, checker integration, private result artifacts, source map, and a complete toy demonstration.

**Not connected in this workspace:** the real Sol/Astra/Luna host clients, your authorized ACC research tool, the pinned real checker, exact target manifest, or a fresh offline board snapshot. The default configuration reports these gaps. No real search, submission, paid model call, or background watch was started. The demo calls deterministic fixture programs, not models.

## Run the setup now

Requires Python 3.10+; standard library only. Extract the ZIP and open its `acc_synthesis` directory. On Windows, substitute `python` if that is your Python 3 command.

```sh
python3 selftest.py
python3 demo.py
python3 harness.py status
```

The demonstration runs six real controller tasks with simulated worker replies: Luna context → Sol bounded miss → Astra changed direction → Luna updated context → Sol toy candidate → independent Sol toy review → exact toy checker. The report explicitly identifies every simulated component. It writes only to a new temporary demo directory and never to the real `ready` folder.

## The selected live arrangement

| Role | Intended model | Effort | Runs when |
|---|---|---|---|
| `sol_builder` | `gpt-6.1-sol` | high | A bounded experiment is ready |
| `sol_checker` | Separate `gpt-6.1-sol` context | high | A candidate or repair needs independent examination |
| `astra_advisor` | `gpt-6-astra` | xhigh | A bounded miss or unresolved review requires a distinguishing test |
| `luna_memory` | `gpt-6-luna` | medium | A task starts, changes direction, or is reopened by evidence |

These are intended host model identifiers, not a claim that every API accepts those strings. Bind each role to a supported authenticated client in that host. A single local controller dispatches tasks sequentially by default; external hosts may claim independent rows concurrently. One row cannot have two active leases in this database. Coordination with other chats' existing row claims is a deployment integration, not an automatic cross-chat lock.

## Connect the existing agent host

In `config.json`, each role's `command` is an argument array for a trusted bridge executable. The bridge reads one request JSON from stdin and writes one result JSON to stdout; logs go to stderr. `workers/example_bridge.py` documents the boundary and deliberately reports blocked until replaced with a real host call. `{python}` and `{root}` are the only controller command substitutions.

The request includes `model`, `reasoning_effort`, `instruction`, `task`, `memory`, `workspace`, `limits`, and lease identity. The bridge runs the host's supported model/tool loop and returns the role's documented result. Commands are configuration-owned; model responses cannot change executable commands. The bridge/host must enforce tool access, allowed paths, network policy, memory quotas, and provider spending limits. This controller is not an OS sandbox and does not pretend to enforce those capabilities.

For a host that already manages agents, use the file handoff instead:

```sh
python3 harness.py add examples/work.json
python3 harness.py export
python3 harness.py heartbeat TASK_ID LEASE_TOKEN
python3 harness.py accept TASK_ID LEASE_TOKEN result.json
```

Replace the example's placeholders with the selected task first. `export` returns the request path. Use the returned task ID/token; heartbeat before its lease expires. `accept` validates referenced files and advances the workflow. Expired or stopped workers cannot commit. `run` uses configured bridges and stops at the batch/task limits or an empty runnable queue. It never schedules itself as a background service.

## Connect exact challenge evidence

Configure these in a copy of `config.json`, with its parent folder as the working artifact root:

1. `target_manifest` and its actual SHA-256. Format: `{ "ruleset_sha256": "...", "targets": [{ "row_id": "...", "track": "AC", "start": ["..."], "goal": ["..."] }] }`.
2. `checker.path`, its SHA-256, and `checker.command`. The command must run that pinned executable directly, or the current Python followed immediately by the pinned script, with `{candidate}` and `{receipt}` arguments. Use a self-contained trusted checker or independently pin/verify its dependency bundle; this adapter pins the named file only.
3. The checker receipt: `{ "candidate_sha256": "...", "checker_sha256": "...", "ruleset_sha256": "...", "valid": true, "exact_endpoint": ["..."], "cost": 1, "peak_length": 4 }`. Hash candidate JSON with sorted keys, no whitespace, UTF-8, and no nonfinite numbers (`gates.canonical_hash`).
4. `board_snapshot`: `{ "observed_at": 1790000000, "ruleset_sha256": "...", "rows": [{ "row_id": "...", "track": "AC", "record": 1, "held_by_us": false }] }`. Supply an authorized offline export. The controller checks freshness and fields, not the external origin's authentication. Missing, stale, future-dated, or ambiguous eligibility is withheld.

Do not bind `demo_checker.py` for real work. No default targets, record scores, challenge move IDs, or checker rules have been invented. Historical ACC-specific regressions in `DESIGN.md` still need their actual archived fixtures at integration; the local tests cover controller behavior and toy checker contracts.

## Run, stop, and recover

```sh
python3 harness.py run
python3 harness.py stop --reason "user stop"
python3 harness.py status
python3 harness.py resume
python3 harness.py recover
python3 harness.py wake examples/wake.json
```

`resume` clears the persistent stop but does not start a process or retry interrupted tasks. `recover` marks expired leases interrupted. A new bounded task must explain a retry and use a new idempotency key. The CLI currently exposes such retries through a changed work contract passed to `add`. A matching `wake` event carries hashed evidence and reopens a parked attempt; repeated identical events cannot duplicate the task. `distinguish witness.json` records two exact states and different observed outputs under a declared shared probe; it retains an empirical witness, not a complete predictive quotient.

The database is authoritative. `state/ready` contains historical exports admitted by code, with an admission event and check time. Readiness admission and STOP serialize through the same SQLite transaction: STOP first prevents admission; admission first remains a historical fact. Existing exports are not permission to submit and may go stale. `withheld` retains rejected/unknown results. Checker receipts live under the selected state directory. To back up an active database use SQLite's backup API; copying only the `.sqlite3` file while WAL writes are active can omit recent events. A stopped, closed controller can be backed up with its entire state directory and referenced artifacts.

## Implemented limits and deliberate boundaries

The controller enforces worker and checker deadlines, finite batch duration, task count, output size, repair/switch counts, leases, same-row exclusion, board age, and persistent stop. An exact checker is allowed to finish its bounded gate after the batch dispatch deadline; that does not authorize another worker. Host memory, provider-token/currency quotas, search-state caps, real process heartbeats inside a remote host, and cross-chat claims require the configured host/tool adapter. A local worker heartbeat establishes client-process liveness, not mathematical progress. POSIX subprocess groups are terminated on stop/timeout; Windows stops the direct child only, so a Windows bridge must own descendant cleanup or run in WSL/container supervision.

The signature gate detects declared changes supported by referenced artifacts. It cannot prove a renamed family is mathematically new; independent review and the discriminating experiment must establish that meaning. Memory refinement currently records and retrieves separating witnesses; it does not compute a complete predictive quotient or automatically learn an optimal classifier. Astra's deep-investigation mode is expressed as a bounded advisor task, not a separate permanent worker.

No dsh installation, Claude configuration change, external scheduler, public repository mutation, or submission endpoint is included. The source-inspired memory and switching rules are operational designs, not newly proved physics. Read `DESIGN.md` and `source_map.json` for the precise synthesis and corrections to Grok's map.

## Files

- `harness.py`: selected workflow and command interface.
- `runtime.py`: durable tasks, leases, stop, process transport.
- `gates.py`: pinned checker receipts and separate scoring eligibility.
- `geometry.py`: optional finite matrix diagnostics, never a scoring gate.
- `prompts/`: exact role contracts.
- `tests/`, `selftest.py`, `demo.py`: focused validation and labelled demonstration.
- `DESIGN.md`, `source_map.json`, `VALIDATION.json`: design, provenance, and this build's measured checks.
