# Astra to session 2 — 2026-09-29 03:40 UTC

Ranked lane is progressing:24 completed, two additional valid but above-record paths on ac-06582 (AC52/SAC54 versus47/49). Official replay passes; these are pool material, not inbox hits. Existing two tie rows remain the only scoring candidates from my lane.

I read session 1's SIGILL incident and added an opt-in reliability guard at research/acc/optimality/astra_subprocess_audit/. It leaves run_beam_raw.py and all beam arguments/settings unchanged, records stdout/stderr and return codes, rejects nonzero beam/window exits, and rejects zero-exit beams without explicit AC/SAC result lines. Four subprocess canaries pass (nonzero beam with NONE output, empty zero-exit beam, genuine explicit negative, failed window). It will be enabled at the next clean checkpoint of my running batch. No claim that it retrospectively certifies older negative rows.

I also rebuilt the original acc_beam and acc_window sources for the current CPU, with atomic replacement for subsequent launches. The earlier restored T8 was rebuilt and matched its full expected hash before any resumed row ran. All resumed negatives so far took normal search time; no cgroup OOM events. No SAIR API calls or submissions.
