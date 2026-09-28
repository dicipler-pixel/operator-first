# Codex Stable sac-09839 beat attempt — 2026-09-28 23:17Z

Another Codex worker's 44-move AC road gave a verified Stable 46-move tie (inbox/20260928T2312Z_codex_sac-09839.txt), snapshot Stable record46 k1. I am running a separate `TWIN_MODE=yx` two-eyes beam W20,000, DMAX43, BEAM_H=1 DIV=.8 P2=2 QUOTA=16 ELITE=5000 DUAL=.75, seeking a 45-move Stable beat. Source AC row is not being beam-searched again. The 44-move AC road had no window11 cut and its C16 low-length prefixes gave best yx finish47. Avoid duplicating this exact Stable orientation attempt; Session 2 sends verified hits.

23:23Z first yx beam finished with independent verified 46-move tie (certificate sha256:e4a494d2f4d461d8c45bfb25bb1b9dd91e4c363e1330e5fee9d0a3470efab7cf); sweep `sweeps/codex_sac09839_yx_W20000_20260928.jsonl`. It shares states 0..17 with the AC-derived 46 route; a 0–3 move bridge found no cut. Now restarting beam at their common state after move 17, aiming for a 26-move remainder to (y,x), which would produce a 45-move Stable beat. This row remains claimed for that exact restart.

23:27Z: both P2=2 junction restarts ended with 27-move suffixes (one yx, one xy), still ties. Testing P2=3 at the same state: commutator-length tie-break after P2, W20k, target suffix26. This is a distinct ranker, not a rerun.

23:34Z: P2=3 low-comm tie-break returned 46; high-comm returned 48. Experimental length-triggered tie-break now running from the shared state: P2 primary, high comm preference when total relator length >=20, low comm below 20, W20k/D26/DUAL=.75. All returned paths are officially replayed; this is a heuristic, not a proof.
