# UPDATE Charlie -> session 2 (relayed by the user via session 1)

Status: Charlie runs in a chat sandbox (2 CPU, 7 GB RAM, ~20 GB disk) and cannot pull the repo; the user relays files.
Charlie's lane (per RALLY.md): high-ceiling Stable AC gap runs. Orders: ORDERS_charlie_v3_20260928.md.

Tools Charlie has, all controlled against the official verifier (moves: 0 mismatches on 56,056 applications;
trivial component to cap 12 exact; ac-03467 cap 23 = 158,016,512 exact):
- acc_disk: exact disk-backed capped BFS, two-sided against a trivial ball (radius 9, cap 36, 183,402,071 states).
  First meeting layer gives the EXACT shortest length under the cap, or a certificate that none exists.
- sac_yx.py: exact shortest route to (y,x) via the relator-swap symmetry; Stable line = route + [15, 15].
- window.py: exact window shortening of a given path (bidirectional, both ends, windows up to ~13 here).
Ceiling on this machine: about 500M states per run (about 23-25 forward layers on 29-33-letter rows).

Results already delivered (charlie_acc_v1.zip / v2.zip): ac-03719 37 (optimal under cap 35; live record 35, so +2);
ac-02528 35 (now 8-9 teams); 13 ledger rows certified no path <= record under the board cap; sac-02528 no route to
(y,x) <= 34 under cap 32.

Asks: (1) orders with the gap-run rows (done: ORDERS_charlie_v3); (2) best (y,x) routes for the one-move-short rows
sac-08578, sac-08078, sac-05378 so window.py can try the one-move cut (included in ORDERS_charlie_v3).
