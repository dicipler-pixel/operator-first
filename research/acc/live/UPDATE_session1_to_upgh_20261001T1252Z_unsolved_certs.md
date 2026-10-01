# session 1 -> UPG-H, 20261001T1252Z: BUILD on the unsolved rows (exact acc_disk BFS, target (x,y))

RESULT cert ac-00738 CLOSED at cap 28: no route to (x,y) with every intermediate total <= 28 (180,878,128 states). Also CLOSED at caps 20/22/24/26.
RESULT cert ac-06611 CLOSED at cap 28 (180,878,128 states). Also CLOSED at 20-26.
RESULT cert ac-10099 CLOSED at cap 28 (61,380,856 states). Also CLOSED at 20-26.

Observation: ac-00738 and ac-06611 give IDENTICAL reachable-state counts at every cap from 20 to 28 (59760 / 405296 / 2512808 / 15026984 / 180878128). They are almost certainly the same component (the starts are equivalent under the moves), so one road solves both: a first solve is worth 2 x 2.0. Builders: treat them as one target.
Next: cap 30 on ac-00738 and ac-10099 is running (disk floor 5 GB; a DISKFULL is reported as such, never as CLOSED). Scope: finite exact certificates at the given caps, not a proof of non-triviality.
