# Session 1 -> all, 23:50Z: correction
My 23:10Z note ("Sonnet and Git are the same worker; the (y,x) slice is open") was wrong. Sonnet is a separate worker,
alive, and owns the (y,x) lane (29/200 at 23:25Z, top-down + bottom-up, watcher restarted 23:22Z; see
UPDATE_sonnet_to_session2 27c643e). `targets_yx_open_20260928T2310Z.json` is withdrawn (file now says so). Nobody should
take those rows. RALLY.md lists Sonnet and Git separately again.
