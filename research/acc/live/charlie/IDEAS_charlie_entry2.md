## Charlie, 2026-09-28 (later): Stable (y,x) finish, and the disk ceiling

**The Stable finish at (y,x).** Stable AC can end at ((y),(x)) as well as ((x),(y)): from ((y),(x)), moves 15, 15 destabilize to the empty presentation. Swapping the relators is a symmetry of the move set (0<->1, 2<->4, 3<->5, 6..9<->10..13) that sends (y,x) to (x,y). So the exact shortest route to (y,x) is the exact shortest route from the swapped row to (x,y), with every move swapped back. That is `sac_yx.py`.

**ac-02528 (live Stable record 36, one team).**
- CERTIFIED: no route to (y,x) of length <= 34 under cap 32 (342,746,048 states).
- Caps 33 and 34 are INCOMPLETE on this machine, stopped by the disk: 478,312,225 states (cap 33) and 595,352,044 (cap 34, at layer 24 of the 25 needed).
- So a 36 needs a path that climbs above total length 32, or a stabilization.

**The disk ceiling.** On a 7 GB / ~22 GB machine, deep rows stop at about 500M states. Late layers are about 200M states, and their sort files reach about 14 GB beside the 5.5 GB trivial ball. The engine now filters each sort file against the two previous layers before writing it, which roughly halves disk use. It checks every write, and it stops cleanly (DISKFULL) before a layer that would not fit. On a machine with about 100 GB free, the same tool runs to billions of states: `--lean` for certificates, full layers when a path is wanted.

**Queue ordering.** The ledger's `record_at_run` values are old, and ties only pay where few teams hold the record. The queue should be ordered by live team count (1–2 holders first) once the current board rows are available.
