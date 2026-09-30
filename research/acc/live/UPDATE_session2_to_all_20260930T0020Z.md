# session 2 → all, 00:20Z 2026-09-30: owner's schedule for pulls and sends

- **Pulls:** every 30 min at :10 and :40 (session 2, `tools/acc/ops/pull_recent.py`, ONE API call). Results:
  research/acc/live/RECENT_SUBMISSIONS.md (uploads used today /40, API calls left /360, last 30 min + 24 h with per-line results).
- **Sends:** once an hour at :25 (session 2, `sair_api.py send FILE --yes --lean`, ~8 API calls: board snapshots only + newest
  history page + local log). FILE = the newest repo-root OWNER_SUBMIT_2026*.txt (now OWNER_SUBMIT_20260930_0005Z.txt).
- Budget/day: 48 pulls + ≤24 sends × ~8 ≈ 240 of 360 calls; ≤24 of the team's 40 uploads.
- Everyone else: **no sends, no API calls**. Verify offline and stack into the current OWNER_SUBMIT file (with a # comment line:
  row, source, length, record, k). Session 1's 01461 pair is in and verified.
