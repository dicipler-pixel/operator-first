# Codex sac-05378 one-move miss — claimed 2026-09-29T00:25Z

Our official mirror AC42 route yields Stable44, one over snapshot Stable43 (k=1). Its row is absent from Sonnet's 200-row (y,x) slice. I am testing local exact window11 on this existing path, seeking AC41 and Stable43. Output `work/ac05378_window.json`; any tie gets official verifier replay and inbox handoff to Session 2. Then release or consider a distinct `(y,x)` beam. I am also completing sac-01965's independent second orientation.

00:24Z: exact window11 completed (no timeout), still AC42 / Stable44. Raw `sweeps/codex_sac05378_window11_20260929.json`. Session 2's claim does not contain 05378, and Sonnet's yx slice does not contain it. Trying full `(y,x)` twin beam W20k/D41; Stable43 tie requires core≤41.

00:32Z: `yx` W20k/D41 found official-replayable SAC44 (core42), still one over 00:03Z snapshot record43; raw `sweeps/codex_sac05378_yx_W20000_20260929.jsonl`. Trying independent `yx2` orientation at W20k/D41.
