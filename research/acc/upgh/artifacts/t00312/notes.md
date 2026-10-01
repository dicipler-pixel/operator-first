# t00312 notes (UPG-H builder, claim 9856c555429b25cbebaeeb16; rerun of t00297)

Started 2026-10-01 (UTC). Wall limit 60 min. Rows: the 14 MS(n, w*) rows n=4..10 of family f-0ce69b0475.

## Prediction (written before running anything)

- (1) Level change: I expect to find an O(1) level change by never cyclically reducing / keeping the active
  site at the end of r0 (working with r0 as a non-cyclically-reduced word is allowed by the core: free reduction
  only). If this works, the canonical lengths should drop from 53/92/163/300/567/1092/2131 towards the
  P000013 constant-2 numbers (50/85/148/291/539/1064/2078) or below; a rough bound is sum over levels of
  (2^L multiplications + O(1)) + finish = 2^n + O(n) + |fin2| = 2^n + 2m + O(n) = 2*2^n + O(n).
  Beating the board records (n=4 48, n=7 278, n=10 2071 ...) needs also (2).
- (2) Short finish: fin2(m) costs 2(m-1)+13 = 2m+11 moves. An m+O(1) finish would make the road ~1.5*2^n+O(n),
  which beats every record from n=7 up. I think this is hard; my expectation is that I find at most a partial
  improvement (e.g. a finish of about 1.5m) or nothing, and the honest outcome is a scoped miss on (2).
- Null outcome: no row gets a path <= its live record (contract prediction). Any path shorter than our own BS
  road (59/62, 100/105, 171/177, 315/308, 575/583, 1109/1100, 2139/2149) still goes into lines.txt.

## Log
