# Onboarding: SAIR Andrews–Curtis Challenge team (Mad Hatters)

Read this first. Written by session 1 on 2026-09-30. Ask session 1 (or the owner) if anything is unclear.

## 1. The game in five lines
- Each row `ac-NNNNN` is a two-relator presentation. A **line** is `ac-NNNNN: [moves]`, a list of AC moves (0–13) that reaches (x,y).
  `sac-NNNNN` is the Stable board: the same row, ending in (y,x) plus `[15,15]`, or the AC path plus `[16,15]`.
- A line scores only if its length **ties or beats** the live record. A tie on a row held by k teams earns 2^-(k-1) of a point after you
  join (k1 → 0.5, k2 → 0.25, k3 → 0.125, k8 → under 0.01). A **beat** takes the whole point. First solves (unsolved rows) are worth 1.
- **Where the points are:** rows held by few teams (k ≤ 3), and rows where we have **no path at all** (6,211 solved AC rows on 09-30).
  Ties on rows held by 8+ teams are worth almost nothing.

## 2. Hard rules (the owner's; do not break them)
1. **Only the UPG-H session sends to SAIR.** Nobody else submits, ever. Put verified lines in the queue (below) and stop there.
2. **40 uploads a day for the whole TEAM** (resets 00:00Z). The owner's API read budget applies to you too; do not poll the API.
3. **Never send or stack:** ac-09839, sac-02257, ac-09311, ac-06403, ac-04718, ac-05378 (or their sac twins). The owner handles those.
4. **Verify every line with the official verifier** before it goes anywhere (`tools/acc/plan_offline.py`, see §4).
5. **Claim rows before searching them:** list them in `research/acc/live/WORKING_<you>.md`. The harness skips claimed rows, so
   keep claims short (the next ~6 hours) and clear them when you stop.
6. **Stop background processes by exact PID only.** Never use `pkill -f` or `pgrep -f` patterns that also match your own shell.

## 3. How the team is wired
| Piece | Where | What it does |
|---|---|---|
| Branch | `claude/gallant-bardeen-0pgpae` | everything; pull before you read, push after you write |
| UPG-H harness | `.claude/skills/upgh/SKILL.md`, `tools/acc/upgh/`, ledger `research/acc/upgh/ledger.jsonl` | harvests every path in the repo, plans what scores, hands out bounded tasks, sends the queue (~every 40 min) |
| Send queue | `research/acc/live/queue/*.txt` | put verified scoring lines here, one `row: [moves]` per line, with a `#` comment (source, length, record, k) |
| Harvest | any `ac-NNNNN: [...]` line in `research/acc/**/*.txt/.jsonl` | UPG-H re-verifies it and keeps the best; push ALL your roads, not only ties (see `sweeps/`) |
| Boards (cached) | `research/acc/live/boards/{ac,stable_ac}_*.json.gz` | live records and k; use the newest; do not pull the API yourself |
| Sent history | `research/acc/live/SENT_ROWS.txt`, `submit_log.jsonl` | what we already hold; never re-queue those |
| Team news | `RALLY.md` (top = newest), `IDEAS.md` (running log), `UPDATE_*`, `ORDERS_*` | read RALLY first each time you start |

## 4. First hour checklist
1. `git pull`; read `RALLY.md` top, the newest `ORDERS_*.md`, and `.claude/skills/upgh/SKILL.md`.
2. Set up the verifier: the SAIR repo pinned at `a0fd6e6`. `python3 tools/acc/upgh/upgh.py doctor` checks it, and `upgh.py setup --t9` builds it.
3. Pick work: the owner or the UPG-H lead assigns it; open lists sit in `targets_*.json` / `ORDERS_*.md`. Claim it in `WORKING_<you>.md`.
4. Verify any candidate: `python3 tools/acc/plan_offline.py FILE --sair <sair checkout> --out OUT.txt`. It prints TIE / BEAT /
   "already sent" per line and writes only the scoring lines to OUT.txt.
5. Scoring lines go to `research/acc/live/queue/<time>_<you>.txt`. Every other road goes to `research/acc/live/sweeps/<you>/`. Push both.

## 5. Methods that produced points (09-29/30), and ones that did not
Produced ties:
- **Road cycle** (pool every road, cross-row transfer, rotations, windows): the most ties, including ac-05659 (k1) and sac-05659.
- **Loose road-keeping DP** (Git's tool with GROW 2, MAXC 16, SLACK 4) on paths 1–4 over the record: 07337 (k2), 00345 (k3),
  09758 (k4), 04157, 01461, 04493, 01196. Chained with the road cycle it gave 05659: DP cut 42 → 40, the cycle cut 40 → 38.
- **Junction splice** (`tools/acc/ops/junction_splice.py`) over all roads; radius 3 found 08259 (k3) where radius 2 missed.
- **Exact capped search** (Charlie's ladder): ties when the record is within about 4 of the start length.

Did not produce ties:
- Grinding the same ~15 rows that sit +1 over a k1–2 record, all night, with every tool.
- Beams capped at record + 2 on rows where we had no path. Use **any-road-then-shorten** instead: `BEAM_FREE_DMAX` in
  `research/acc/optimality/run_beam_raw.py`, then DP, window and splice.
- Exact search on rows whose record is 12 or more above the start length. It runs out of disk; the disk guard kills it.

## 6. Leaders
- Point people at **value**, not at the rows we already touch: check the scoring formula against the target list before assigning.
- Give each member a **separate list** (no overlaps) and a way to report (queue/ plus sweeps/).
- Watch the output rate hourly. If a lane has produced nothing in 2–3 hours, change the method or the rows; do not keep grinding.
- Post short notes in `RALLY.md`, and keep `ORDERS_*.md` current.
