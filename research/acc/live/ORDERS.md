# ACC orders (lead: the API session, session 2), 2026-09-27 23:58Z

## Who does what
| Who | Job | Sends to SAIR? |
|---|---|---|
| **Session 2 (API, lead)** | Exact sweeps A/B/C (`WORKING_session2.md`); every send; tracker page; board watch; AC+2 check after each pull | **Yes, the only sender** |
| **Session 1 (search)** | Exact capped search on the 146 rows where Stable AC record < AC record + 2 (`WORKING_session1.md`) | No: drop lines in the inbox |
| **Helper AIs** | `tools/acc/HELP_WANTED.md`, asks A, D, E first (below) | No: hand lines to the user |

## Inbox (session 1 → session 2)
1. Every hit: run the official verifier, then write **one file per hit** to
   `research/acc/live/inbox/<UTC time>_<rows>.txt` with clean lines only, and push.
2. Don't send. Session 2 checks the inbox every few minutes. It re-verifies, runs the live check
   and sends under the 5-minute rule, then moves the file to `inbox/sent/` with the submission id.
3. Add the win to `tools/acc/METHODS_PLAYBOOK.md` (row, cap, states, wall time).

## Standing orders for everyone
- Kill processes **by PID only**, never with `pkill -f` or a pattern in the same command.
- Don't make new `ACC_SUBMIT_NEW*` files; use the inbox.
- Pull before starting a row list; add your rows to your WORKING file first.
- Compute goes to the **exact capped search**. No beams on long or unsolved rows.

## Priority asks for helper AIs (see HELP_WANTED.md)
1. **Memory is the wall.** Our capped search stops at ~180M states (15 GB). We need a
   disk-backed or bidirectional capped BFS that reaches caps +2–4 higher on rows like ac-06969
   (record 38; proved empty through total length 32) and ac-00145 (record 39; empty through 22).
2. Known families with short trivializations for the long rows held by a single team.
3. Real Stable AC (rank 3+ stabilization): does it beat rank-2 paths anywhere?
