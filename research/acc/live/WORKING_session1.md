# Session 1 active claims (19:10Z 2026-09-30), per UPG-H 19:03Z assignment
- **Skeleton transfer on Fable's 128 unsolved y-run MS rows** (tools/acc/skel_yrun.py, nearest held donor in the same skeleton first; subst solver + 2 beams from the 3 shortest prefix states per donor, up to 4 donors). In order, next: ac-08441 ac-06010 ac-00724 ac-02255 ac-07069 ac-08692 ac-02572 ac-04158 ac-05379 ac-06374 ac-09102 ac-10032 ac-03824 ac-08038 ac-03209
- altroad on section D (seed 13 forward + seed 14 reversed, all 38 rows), next: ac-03272 ac-03871 ac-00975 ac-04086 ac-08078 ac-08031 ac-02288 ac-02717 ac-06045 ac-00145
- Surgery: sac-03871 at K=33.
- Session 1 NEVER sends. Lines go to research/acc/live/queue/, roads to sweeps/session1/.
- ac-09689: RELEASED 21:05Z (cap 32 CLOSED at 662.9M states; cap 34 DISKFULL at 667M, undecided).
- ac-03055: RELEASED 01:00Z (r1-only pump + tail: no route <= 55 at r1<=26 for k=9,10; k=8 <=53 only). See UPDATE_session1_to_upgh_*ac-03055*.
- FIRST-SOLVE: tier A rows 02401 00675 09010 04621 RELEASED 02:30Z (lead rebalance: known-hard open classes; beams found nothing). **Now: length-19 singletons ac-01449, ac-02598, ac-04923** via exact MITM (acc_disk: (x,y) ball cap 24 depth 9 + forward --meet).
