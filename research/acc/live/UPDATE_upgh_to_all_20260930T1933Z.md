# UPG-H (lead) to all, 19:33Z: plan row 2/3 (y-run first solves): Fable's hand construction fails, and it says why

Fable (t00092, `research/acc/upgh/artifacts/t00092/notes.md`) tried the y-run cancellation on ac-08441, ac-06010, ac-00724,
ac-08692, ac-02255 and ac-07069. **It does not start on any of them.** The MS relator gives exactly two shortening rewrites
(X y^L x -> y^(L+1) needs L = n; x y^L X -> y^(L-1) needs L = n+1). In all six rows the matching y-run sits in the
**opposite flank orientation**, so no single multiplication shortens w. The solved siblings (e.g. ac-04662, n=5, record 15)
have the right orientation.
**Over all 128 y-run rows: 102 are wrong-orientation only; the other 26 land on a wrong-orientation core after one rewrite.**
Exact BFS (ac-08441, caps 22/24) and beams (W 20k-80k, climb, H) found no route on any of the six.

What changes:
- **Charlie, Bob:** do not start the sibling-state work from my 19:04Z hub note; there are no post-cancellation states to seed from.
- **Session 1:** your skeleton-transfer lane (skel_yrun) is a different method (donor routes, not the one-step rewrite), so keep it
  running to its kill test (0 of 128). Put the rows whose donor has the *same* flank orientation first; `t00092/work/orient.py`
  classifies them.
- Still live: **ac-09689** (MS(8, XYxYYY), unsolved by all). UPG-H t00091 finishes from Fable's 16-move collapse state. The same finish
  already works on the n=5 sibling (ac-07900: 68, a first route of ours, not scoring).
