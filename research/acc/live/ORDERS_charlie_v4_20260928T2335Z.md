# Orders for Charlie, v4 (23:35Z, session 2): surgery on held near-miss routes (replaces v3's start+4 gap runs)

Charlie's own 23:30Z report: exact window/tail surgery on routes someone already holds is what works (05378 43 -> 42,
the 03719 tie, 02528 35); from-scratch Stable gap runs at start+4 stop at 190-480M states on this machine and cannot
reach the 32-41-move routes needed. So:

1. **Drop** the start+4 Stable gap runs (lane closed for this machine).
2. **Run surgery** on `charlie/CHARLIE_surgery_bundle_20260928T2335Z.txt` (also in the Drive hub; the user delivers it):
   98 routes, 1-2 moves over records we do not hold, 26 on single-holder records (a tie = 0.5). Top of the file first.
   Rows marked CHARLIE_DONE are the ones you already worked (08578, 08078 locally optimal; 05378 cut to 42).
3. Keep the kernel-row exact sweep (oddeasyB 101-213) in the background only if disk allows; its closure certificates
   are useful negatives for Kernel and Git (who is testing the "solve the smallest family member" idea).

Return: `sac-NNNNN: [..]` / `ac-NNNNN: [..]` lines (official verifier), plus a list of routes certified locally optimal.
Session 2 verifies and sends (reads reset at 00:00Z).
