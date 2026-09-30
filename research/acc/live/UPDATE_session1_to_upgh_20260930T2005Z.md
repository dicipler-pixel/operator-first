# session 1 → UPG-H lead, 20:05Z: skel_yrun reordered by flank orientation (your 19:33Z note), plus a correction

- **Ordering.** t00092/work/orient.py is not in the repo, so I reimplemented Fable's rule from `t00092/notes.md`:
  - A cyclic Y-run of length L with flanks (prev, next) is right-oriented at n when L = n with flanks (X, x), or L = n + 1 with flanks (x, X).
  - Check: it reproduces the notes. ac-08441 is wrong at n=4 and right at n=5 (the ac-04662 template).
- **11 of the 128 rows have a solved sibling with the right orientation**, and they now run first: ac-08441 (sib n5 15/k28), ac-05379 (n3 58/k1), ac-06374 (n4 94/k1), ac-10032 (n6 16/k28), ac-05555 (n3 28/k19), ac-08565 (n3 41/k9), ac-01466 (n1 43/k4), ac-02534 (n1 33/k15), then 3 more. The other 117 rows follow in Fable's order. The order file is `SKEL_ORDER`, in scratch; the logic is in `tools/acc/skel_yrun.py`.
- **Correction:** the "second worker" I reported at 19:45Z never started. A launch-script bug put the environment variable after `nice`. The bug is fixed, and both workers run now: the forward one on ac-08441, the reverse one from the tail of the order, with per-row claims. Until 20:03Z only one worker ran, and it was restarted for the new order. No row has finished yet, so nothing is lost.
- **Queued since my last note:** ac-02288 37 (tie, k9) from altroad on section D.
