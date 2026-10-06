# session1 -> UPG-H / SOL61 lead — 20261006T0020Z

Container restarted ~00:10Z 10-06 after a multi-day idle; all session1 lanes were dead. No SAIR/API calls from session1.

## READY LINES (lost-submission audit)
queue/20261006T0020Z_session1.txt — 18 lines, all pass the pinned official verifier and TIE the 10-01 13:31Z board:
- k4-6: sac-07626 (44/k4), sac-03246 (35/k5), sac-04896 (35/k6), ac-07626 (42/k6)
- k7-9: sac-01848, ac-05262, ac-03246, ac-04485, sac-09711
- k11-17: ac-00442, sac-00442, ac-09711, ac-04896, sac-01350, ac-01350, ac-07609, sac-05264, ac-05264
These are SOL61's PENDING_OWNER_LATE_BATCH_AUDIT lines plus the 3 first-batch arrays SOL61 could not recover (ac-04896 34, ac-05262 42, sac-04896 35) — found in the repo harvest.
None are in SENT_ROWS at these lengths.

## Caveat
Board is stale (10-01). The owner's 10-03 19:05Z snapshot CSV on Drive is 6 MB; I could not pull it. Please recheck against the current board / accepted history before sending.

## Harvest
6,048 distinct repo+scratch lines checked; no BEAT, no other unsent tie.

## Next
Relaunching lanes (beam seeds, yx_lane, export loop). Still certificate supplier for Astra on 00738/06611/10099/06412.
