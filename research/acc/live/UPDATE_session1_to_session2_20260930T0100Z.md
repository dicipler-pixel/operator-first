# session 1 → session 2, 01:00Z: FIX, mine_recent.json broke SENT_ROWS and plan_offline (repaired, please keep)
- **Symptom:** SENT_ROWS.txt shrank from 1,345 rows (00:02Z) to 426 (00:08Z). Session 1's road cycle then flagged 398 "new" lines. All 398 were already sent.
- **Cause:** `sorted(glob('mine_*.json'))[-1]` picks the newest file by name. `mine_recent.json` (from pull_recent.py, only the newest 20 submissions) sorts after `mine_20260927T2239Z.json`, so dashboard_data.py, plan_offline.py and `sair_api.py changes` all used 20 submissions as our whole history.
- **Fix (this commit):**
  - dashboard_data.py and sair_api.py use `mine_2*.json` (dated full pulls). They already merge submit_log.jsonl, which pull_recent appends to.
  - plan_offline.py now merges ALL mine_*.json plus submit_log.jsonl. Before this it read only the 09-27 pull and missed every later send.
  - SENT_ROWS/dashboard rebuilt offline (1,350 rows, no API call).
- **Please check** OWNER_SUBMIT_20260930_0026Z.txt: any lines stacked from a plan_offline or SENT_ROWS read between 00:08 and 01:00Z may be repeats. The fixed plan_offline marks them "already sent".
