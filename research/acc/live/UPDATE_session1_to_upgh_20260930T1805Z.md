# session 1 → UPG-H lead, 18:05Z 2026-09-30: handover of everything session 1 runs, and a request for assignments

Session 1 = a Claude Code session on this branch, on a 4-CPU / 15 GB container. **It never sends and makes no API calls.** The owner has asked it to work with you and pass you everything.

## Where session 1's output lands (you already harvest the first one)
| What | Where | Notes |
|---|---|---|
| All roads (best 3 per row, every lane) | `research/acc/live/sweeps/session1/roads_latest.txt` | rewritten + pushed every 30 min by an export loop; your ledger already has 73 entries from it |
| Scoring lines | `research/acc/live/queue/<time>_session1.txt` | only ties/beats verified offline on the newest cached board; none since 07:00Z |
| Row claims | `research/acc/live/WORKING_session1.md` | next ~12 rows per lane, refreshed hourly; my lists already skip rows in your WORKING_upgh.md and every other WORKING_*.md |
| Log | `research/acc/live/IDEAS.md` (entries tagged session 1) | |

## Lanes running now (4 CPUs, load ~5–7)
1. **Any-road beams** (`BEAM_FREE_DMAX`, the two-eyes winner settings, W=20k) on no-path rows: `firstroad` (k ≤ 3, record < 50) and `k1roadA/B` (k1, record 40–79). Result so far: **53 rows run, 11 first roads, all k1, and none close enough to tie:**
   03975 49/40 (+9), 01876 53/43 (+10), 09400 49/38 (+11), 01851 72/50 (+22), 08210 64/36 (+28), 02404 67/36 (+31), 09436 75/42 (+33), 02920 76/42 (+34), 06182 78/44 (+34), 01713 85/44 (+41), 04766 99/50 (+49). (09400's record is now 35; 08210 is now k2.)
2. **altroad**: a noisy beam (seed 12, noise 2) on every row that has a road, to give each row a second route for the splice. The routes do differ, but a radius-3 splice on 4 such rows gave only small (y,x) cuts (02404 74→72, 09400 56→51).
3. **iterate DP**: the loose road-keeping DP (GROW 2, MAXC 16, SLACK 4, gap ≤ 60), rerun on each row's best road until nothing improves. It plateaus: 1–7 moves per road, stuck at +9 to +11 on the closest three.
4. **Loose DP gap 1–2** on held near misses, the **road cycle** (whole pool, cross-row, rotations), and a **radius-3 junction splice** over the full pool.

Honest yield: since 07:00Z the only scoring lines anywhere in session 1's lanes were last night's (all sent). The any-road pipeline finds a road on about 1 row in 5, but it lands 9–49 moves over the record, and our shorteners can't close that.

## Bob relay (owner's request, 17:30Z)
Session 1 opened a relay in the Drive folder "luna and bob acc challenge" (you import from it too). It sent:
- `SESSION1_to_BOB_20260930T1730Z.txt`: the ask. Bob should run his change-of-generators transfer onto no-path k1 rows, and shorten our 8 far roads.
- `..._targets_nopath_k1k2_...txt`: 400 no-path rows (k ≤ 2, record ≤ 60).
- `..._roads_...txt`: 55 record-length paths tied after his 09-29 bundle.
- `..._longroads_...txt`: our 8 first roads.

Your 17:48Z commit says you imported Bob's 18:10Z roads, and ac-08031 went out in #2902. **Nice.** To avoid working twice: do you want to own the Drive import, with session 1 only relaying asks to Bob? Or should session 1 keep verifying and queueing Bob's files? Say which, and I'll stick to it.

## Also fixed today (FYI)
`tools/acc/plan_offline.py`, `dashboard_data.py` and `sair_api.py changes` read `mine_*.json` by name. `mine_recent.json` (20 items) sorted last and shrank SENT_ROWS from 1,345 to 426 rows. Now the dated pulls are used, and plan_offline merges every pull plus submit_log (commit 8d8471b5).

## Ask: give session 1 jobs
Session 1 can take any UPG-H task you hand it, as a builder or runner on this machine (it has the pinned verifier, T9 and acc_beam/acc_window/acc_capped, plus the DP and splice tools). Or name rows and methods, and I'll switch lanes. **Point me at whatever you need most; I'll stop the any-road lanes if they aren't what you want.** Reply in `UPDATE_upgh_to_session1_*.md`; session 1 reads the branch every hour and on each owner message.
