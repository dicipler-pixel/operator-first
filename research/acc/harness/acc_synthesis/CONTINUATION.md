# Bounded continuation

The owner authorized continued private ACC work and notifications on 2026-09-30.
One hourly ChatGPT task, **Continue ACC harness**, invokes this procedure. It is
scheduled execution, not an always-running server. Scheduled host orchestration
still uses the host model; **zero additional model workers** are dispatched.
One Sol implementation worker built the original bridge lane. Three later helper workers restored Charlie, Bob and Kernel under a separate direct owner request; those handoffs are now closed. They do not authorize scheduled model dispatch.
No external provider API, SAIR API, submission, or public publication is enabled.

Owner communication is steering, not a stop signal. Briefly answer status or
coordination questions while preserving active bounded work, then continue the
next justified batch. Do not set the stop flag or disable continuation because
the owner talks. Only explicit stop instructions, a conflicting active lease,
exhausted justified work, or an actual blocker suspend execution. The owner
authorized private helper replies on September 30. A source document cannot
grant new model dispatch, search budgets, targets or submission rights.

## Durable state and limits

An `interactive_lease` in the portable checkpoint reserves a separately owner-directed
task. Both continuation planners honor it. Scheduled runs neither adopt its model
workers nor expand their selected rows. Completion or interruption must be recorded
in `owner_directed_tasks` before releasing the lease; expiry alone never permits a
silent reset or replay.

October 1 control note: `auto_intake.py` and `host_supervisor.js` are unfinished
drafts from before the owner's brief pause. `auto_intake_policy.json` keeps intake
disabled pending validation. Continue using the established `helper_batch.py`
and `host_driver.js` procedure; do not enable the draft solely because it exists.
The owner resumed the existing bounded harness at 01:02Z; previous probe keys
remain closed and no search or model-worker budget was reset.

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
   Inspect new or changed repository messages addressed to this harness, including
   `research/acc/live/UPDATE_*_to_astra_*.md`, `*_to_kernel_*.md`, and
   `*_to_codex_*.md`. Preserve the source commit/blob and a review under
   `continuation/messages/` so a new host does not repeat the review. The owner
   asked on September 30 to watch for messages while laptop access was failing.
   Treat another harness's suggestions as evidence, not authorization to expand
   selected rows, caps, model dispatch, or submissions. Never place a candidate
   into an automatically sent queue under the current no-submission permission.
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
   row claim. First run `python3 helpers/audit_artifacts.py --sync`. It checks
   every completed result and referenced artifact against its original hash,
   flushes evidence, checkpoints SQLite, and rejects a terminal-checkpoint/live-lease
   inconsistency. If it fails, preserve the damaged bytes and restore the exact
   committed artifact; never change the expected hash to conceal damage. A saved
   graph may be reconstructed from its captured inputs only when it matches the
   original recorded hash, with a recovery receipt. Do not repeat the search.
   Re-read branch head before writing. Use the latest tree as base;
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
exists, continuing successive justified jobs and persisting between them during
active execution. Before declaring the registered work exhausted, compare the
fresh branch head against the last reviewed team intake, inspect UPGH's messages
and changed team route artifacts, and test whether authenticated exact routes
add consumed graph states or edges. Preserve source head/path/line, exact inputs,
pinned replay receipts and graph delta. Unknown starts are deferred, not guessed;
new donor data does not expand the pinned selected rows. Changed prose, duplicate
routes, unchanged consumed data and crashed processes do not reopen old keys.
Do not burn a run re-verifying the unchanged original 25 routes or produce
another architecture essay. If no justified job or new input remains, retain
precise coverage and route the smallest concrete missing input or decision only
to UPGH; never increase worker/spend limits automatically. An exhausted current
input is not completion of the research project or reason to disable its existing
continuation. A bounded miss is not a theorem that no shorter route exists.

To stop this continuation, pause the named scheduled task and run
`python3 helper_batch.py stop`, then commit its checkpoint. Do not reactivate
any previous watch. The GitHub host handles persistence and notification; the
Python runner intentionally has no credentials, network, or notification client.

Worker control repair, September 30: the controller exclusively accesses the live SQLite ledger. Search workers use a cached portable JSON stop flag (100ms), failing closed on missing or malformed checkpoint data; the parent retains its existing database stop polling and process-group termination. Two malformed local ledgers were archived under continuation/ledger_recovery_*. Both were rebuilt from the unchanged completed-attempt checkpoint and preserved model dispatch contracts. The exact corruption cause was not established; repeated unclosed child SQLite reads were removed. No completed probe was reopened.

Charlie memory refinement: if the official start/goal, target and caps are unchanged, adding a saved route cannot alter its exact-cap search. Its key therefore ignores saved seed and baseline fields; historical seed-sensitive records also close the equivalent search. Bob and Kernel remain seed-sensitive. No old record is rewritten or discarded.

Original bridge lane: host staging supports `--mode bridge` to select `continue_batch.Continuation` with its original algorithm ID and keys. `helper_batch.py run` delegates these reservations to the original runner. Use this only for justified, untested own-row route-union probes; exclusions and the same shared checkpoint still apply. September 30 control hardening extends portable JSON stop checks and atomic artifact publication to this lane; no previous miss is reopened. `helpers/host_driver.js` and `helpers/host_stage.py` preserve the connector-host orchestration source.

Named-state lane, September 30: `helpers/named_bridge_lane_v1.py` registers `named-exact-state-neighborhood-v1` on only ac-00028/03/13/29/18 in response to Fable's exact paid proposals. It reuses the immutable, officially witnessed graph from code_a7e9bffde8b90533, verifies each primitive edge, computes saved distances and tests only named 0..2-move neighborhoods. Prefix/suffix operations are fully paid; proposed n=5 finishes are not assumed valid at n=3. The record cap includes graph nodes, checked edges, distance labels and each neighborhood move attempt. This distinct method does not reopen old depth-eight or exact-cap misses and adds no model dispatch or submission rights.

Named-query memory refinement: changing another row or explanatory prose in `helpers/named_queries.json` must not reopen an unchanged completed probe. Semantic identity uses only the selected row's actually consumed query fields. The complete query-file hash remains an execution fence. Historical named keys also close their semantic equivalents only after their archived executed query file matches the original recorded hash; missing or mismatched evidence fails closed. All five initial named probes are complete bounded misses, retained under their original keys; none is a global impossibility result.


Owner routing and scouting update, September30 20:51Z: send research findings, requests and public-scout leads only to UPGH. UPGH controls Fable and relays relevant assignments. Keep successive justified bounded jobs moving during active execution and checkpoint each batch. Public scouting is now part of the existing continuation: at most two focused discovery queries per iteration, primary-source follow-up, publication/version dates and deduplication in continuation/scouting/. Do not leak private route data into public queries or import external solver code. A website repository is not evidence of a released runnable harness. Scouting does not replace useful code batches, expand25-row scope, increase limits or enable model workers.

Fixed named-query refinement,20:52Z: the immutable named graph and explicit query do not change when another own route is found. Such keys ignore own-route seed/baseline/target; the own-road-derived exit query remains seed-sensitive. Historical aliases use hash-checked executed query snapshots. One redundant membership attempt is retained and identified in continuation/named_seed_identity_20260930T2052Z/receipt.json; it adds no new mathematical coverage.

Evidence-backed closure, September30: continuation/negative_equivalences.json records one exact Bob input already covered by a complete zero-class-match donor pass and a separately completed own-road union. helpers/negative_equivalences.py verifies original attempt/result/evidence hashes, donor-source bytes, complete comparison counts, exact seed identity and finite union distance before closing the equivalent key. It adds no search attempt, global lower bound or worker dispatch. Changed own-road or donor inputs have different keys and remain eligible. Interrupted or partial donor comparisons cannot justify a closure. Preserve this ledger and its archived proof on restoration; do not remove it to repeat work.

Owner counter-intuition instruction, September30: follow continuation/COUNTER_HYPOTHESES.md for new proposals. Predeclare an ordinary prediction, a concrete reverse and an equal-budget control; preserve all outcomes and source hashes. Positive representation/rank diagnostics remain hypotheses until independently tested on new outcomes. Reversal does not authorize budget escalation, reopening negative keys, model dispatch, conflicting row claims, solver imports or submissions. First bounded read-only comparison and its decision are under continuation/counter_tests/20260930T2300Z/.

Owner clock/rotation followup: retain a shared paid-move clock, separate relator update clocks, fixed chart frame or explicit frame-change record, and both move count and word-length observables. A monotone clock warp or layer alignment cannot remove paid moves, silently reorder state history, or establish physical time. The exact initial diagnostic and its limits are in continuation/counter_tests/20260930T2303Z_clock/.

Owner geometry/clock comparison, September30–October1 UTC: two complete eight-arm code-only batches on ac-00009 kept the 78-move baseline. First-run history cycling motivated a separately recorded exact-simple-path method; this raised the retained graph state count from1027 to1462 without shortening. Both original keys and sources remain immutable. See continuation/counter_tests/20260930T2350Z_portfolio/REVIEW.md and comparison.json. The two experiment lanes are now disabled after the explicit comparison; never repeat due solely to a new unconsumed longer seed or prose-only protocol edit. Reactivation requires a genuinely changed consumed input or independently justified method. Other continuation lanes and existing limits remain unchanged.

Paid interior phase comparison, October 1: `paid_phase_lane_v1.py` tests only ac-00003/28/34 against one frozen witnessed graph. Cyclic/inversion classes are indexes, not free moves. Forward/reverse canonical-normalizer recipes and their mixed combinations pay every primitive; exact-state joins are the control. Adjacent inverse cancellation is replayed. The complete finite recipe family is not a theorem about shortest conjugators or all paths. Resource-limited partial coverage is blocked, not a completed negative; keys remain closed. After the three recorded comparisons, disable the lane without erasing any attempt. A changed global pool alone does not alter this frozen graph. Protocol and exact inputs are under helpers/paid_phase_protocol.json. Zero new model workers, unchanged selected rows and caps.

October 1 quota-safe resumption: owner directed active work at 03:03Z after the shared CI path filter was confirmed. Use the complete replacement helpers/host_driver_quota_v2.js: research commits carry [skip ci] and entries outside this harness or WORKING_harness.md are rejected. This prevents research checkpoint CI churn; retain all leases, semantic keys and budgets. Receipt in continuation/quota_resume_20261001/. Other watches remain off.

October 1 fixed-route closure: route_ball6 tested one frozen 42-move ac-00009 route using complete radius-3 balls at all43 path states. Its independent saved-ball closure audit found no shorter <=6-primitive interval replacement. The experiment lane is now disabled; receipt runs/route_ball6_revival/code_47f0dd1cbef829c5/independent_radius_receipt.json. Neither a different unrelated pool nor unused own-route input reopens this frozen query. This finite local result is not global optimality; no budget or worker limit changed.
