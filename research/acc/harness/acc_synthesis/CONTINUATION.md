# Bounded continuation

The owner authorized continued private ACC work and notifications on 2026-09-30.
One hourly ChatGPT task, **Continue ACC harness**, invokes this procedure. It is
scheduled execution, not an always-running server. Scheduled host orchestration
still uses the host model; **zero additional model workers** are dispatched.
One Sol implementation worker built the original bridge lane. Three later helper workers restored Charlie, Bob and Kernel under a separate direct owner request; those handoffs are now closed. They do not authorize scheduled model dispatch.
No external provider API, SAIR API, submission, or public publication is enabled.

## Durable state and limits

`continuation/checkpoint.json` is the portable continuation index and stop flag.
`continuation/routes.json` contains exact seed paths plus independently verified
improvements. `runs/` contains bounded-search artifacts. The SQLite ledger in
`state/` controls leases on a live host. A fresh host creates a new local ledger
and retains the committed portable index; it must not recreate old model budget
or retry old probes. A reservation belonging to another host is not transferable.
An expired reservation is explicitly recorded as interrupted, never retried by
merely discarding the checkpoint.

Each batch runs one registered helper command from `helpers/lanes.json`: Charlie's exact-cap ladder, Bob's paid generator transfers, or Kernel's exact foreign-road overlay. `helper_batch.py` is the complete new continuation entry point. The original `continue_batch.py` and its two misses remain intact. Lanes share one portable ledger and rotate fairly, choosing near-record unheld rows first. All 25 pinned starts are supported; an absent saved route is an absent baseline, not a fabricated path.

Limits remain 180 search seconds, 600,000 admitted records/comparisons, and 1,024 MiB address space. The parent has a 255-second process-group timeout for search plus replay and persistence. Search commands enforce their own declared limits and official checker pins; unsupported hosts refuse rather than silently omit a limit. No model-generated command, provider API, challenge API or solver import occurs inside a batch.

A probe key contains the mathematical algorithm ID, helper, selected row, donor input fingerprints, own-row seed move arrays, baseline, target and bounds. Exact source hashes fence execution but are excluded from memory identity: cosmetic changes and boundary hardening cannot erase a miss. Own seeds are fingerprinted per row so improvement elsewhere does not repeat every row. Never rename an algorithm or increase caps to bypass negative memory. An interrupted key also remains closed; reopening needs genuinely new evidence or an explicitly justified method. Protocol files describe archival provenance; immutable run snapshots describe what actually executed.

## One scheduled iteration

1. Read the current branch head of private `dicipler-pixel/operator-first`, branch
   `claude/gallant-bardeen-0pgpae`. Restore this entire harness folder if needed;
   retain exact bytes for pinned files. Inspect this file and the checkpoint.
   Honor the portable stop flag, active reservations and current user directions.
2. Read current `research/acc/live/WORKING_*.md` row claims. Separate dated history
   from current named lanes. Run `python3 helper_batch.py plan`, supplying
   `--exclude-row ac-NNNNN` for rows with an active competing claim. If all rows
   are blocked, report the concrete conflict once; do not broaden beyond the
   pinned user-selected 25 rows. Only exclude genuinely active claims; dated
   historical rows are not current reservations. Each lane can use an exact
   official start without a saved route; no candidate is accepted without replay.
3. For the proposed key, run `python3 helper_batch.py reserve --key KEY
   --repo-head FRESH_HEAD_SHA` (repeat the same exclusions). Commit the resulting
   checkpoint and a narrowly scoped `research/acc/live/WORKING_harness.md` claim
   privately **before** launching the search. Use a fast-forward update with no
   force. If the head changed, reload and reconcile; do not overwrite a competing
   reservation. After a failed claim commit, do not launch locally.
4. Run `python3 helper_batch.py run --key KEY --reservation-commit COMMIT_SHA`.
   This uses a `code_search` task in the harness, renews its lease, honors stop,
   checks artifact hashes, independently replays candidates and records the
   bounded result. It performs no model dispatch. If the scratch host was lost
   after reservation, wait for expiry, run `recover`, and preserve the interrupted
   key. Do not adopt the foreign lease or silently re-run the same probe.
5. Commit the changed portable checkpoint, routes, run artifacts and completed
   row claim. Re-read branch head before writing. Use the latest tree as base;
   compare changed paths with the originally read versions. Preserve other
   sessions' changes. If checkpoint or routes changed concurrently, reconcile
   by full attempt key and exact move arrays; never use last-write-wins. After
   updating the ref without force, fetch it and verify the commit is reachable.
6. A candidate is useful only if the pinned official replay independently passes
   and it improves the best saved length. Notify with exact old/new lengths and
   the private commit. Distinguish reaching the user's pasted target from live
   scoring: the saved board is stale, so eligibility remains withheld. Deduplicate
   using a candidate-move hash or concrete blocker key in checkpoint.notifications;
   `python3 helper_batch.py ack --key NOTIFICATION_KEY` records delivery intent.
   Quiet misses and routine heartbeats do not merit a notification. Record a
   concrete execution/access/persistence blocker once if the work cannot run.

Every scheduled iteration should do useful new bounded code work if a valid job
exists. Do not burn a run re-verifying the unchanged original 25 routes or produce
another architecture essay. If all registered probes are exhausted, retain their
precise coverage and request the smallest justified next input or strategy
decision; never increase worker/spend limits automatically. A bounded miss is
not a theorem that no shorter route exists.

To stop this continuation, pause the named scheduled task and run
`python3 helper_batch.py stop`, then commit its checkpoint. Do not reactivate
any previous watch. The GitHub host handles persistence and notification; the
Python runner intentionally has no credentials, network, or notification client.

Worker control repair, September 30: the controller exclusively accesses the live SQLite ledger. Search workers use a cached portable JSON stop flag (100ms), failing closed on missing or malformed checkpoint data; the parent retains its existing database stop polling and process-group termination. Two malformed local ledgers were archived under continuation/ledger_recovery_*. Both were rebuilt from the unchanged completed-attempt checkpoint and preserved model dispatch contracts. The exact corruption cause was not established; repeated unclosed child SQLite reads were removed. No completed probe was reopened.
