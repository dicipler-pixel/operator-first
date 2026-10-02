# SOL61 temporary lead — 2026-10-02 10:50Z

Owner asked SOL61 to coordinate tonight while UPG-H is offline. This is coordination only: **no SAIR submission or challenge API call from this session. The owner remains the submitter until UPG-H returns.**

## SUBMISSIONS FIRST
No newly re-verified line is being declared ready by this handoff yet.

Immediate audit target: the late 2026-10-01 owner batches are not fully accounted for in `research/acc/live/SENT_ROWS.txt`. Examples:
- ac-03246: ledger still shows a previously sent 53 against record 34.
- ac-05264: ledger still shows a previously sent 42 against record 33.
- ac-05262: ledger still shows a previously sent 71 against record 42.
Several other batch rows have no sent entry at all.
Before any search, check the actual accepted-history/receipts and current board. If a verified record-length line was never accepted, put its plain SAIR line at the top of the owner handoff.

## TONIGHT'S COMPUTE RULE
We are short on session time. Do **small, high-value, falsifiable work only**:
1. Audit unsent verified lines / current record state.
2. Recheck Stable `(y,x)` finishes on low-k near-record roads already held.
3. Rerun recognition/height web only if genuinely new roads entered the pool since its last pass.
4. Fresh route lineage on a low-k +1 row only when no same-method road already exists.
5. No blind long capped BFS, no repeat of closed 207 SOL61 probes, no old low-distance exact work already certified.

## CLAIMS / OVERLAP
Read every current `WORKING_*.md` before starting. Treat old claims as stale unless the worker refreshed them; do not silently take a row that another live worker is actually running.

Known stale-looking files observed at takeover:
- WORKING_session1.md: last dated 2026-10-01.
- WORKING_session2.md: last dated 2026-10-01.
- WORKING_upgh.md still names t00418/t00420, but UPG-H is offline tonight.
Workers must refresh before compute.

## SOL61 STATE TO PRESERVE
Latest recovered SOL61 handoff (Drive 2026-10-02 01:55Z):
- branch head observed there: 09ca4eee504828418c13c79ff9b964cb2bb95e7d
- portable checkpoint: 207 recorded attempts; planner returned exhausted
- no active reservation, no searches launched, no submission candidate
- do not reset/replay closed probes
- missing useful input: Bob's exact 775-row ladder inventory / donor arrays and hashes

## EXACT-OPTIMALITY BRIEF
The attached full brief remains authoritative for the R=15..19 exact run. Do not redo:
- all records <=14 optimal
- no unsolved row <=12
- listed R=15 optimal controls
- <=10 window shortening and suffix screens
- dead heuristics named in that brief
The heavy T9 plan is not tonight's default unless an already-built verified T9 is locally available.

## REPORT FORMAT
Every worker reports:
- READY LINES first, plain `ac-...: [...]` / `sac-...: [...]`
- exact method and scope
- verifier status
- current record comparison
- complete / incomplete
- what should run next

Do not call a timeout or partial capped run a proof.
