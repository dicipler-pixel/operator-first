# Smith chart and Snell pilot on scored AC routes — 2026-09-28 14:49 UTC

This is an empirical search-feature test, not an AC invariant, physical refraction claim, shortestness proof, or SAIR submission. The four assigned two-eyes search lanes continued unchanged during the pilot.

## Smith coordinate

For a state with relators r0,r1, the path-display map uses Z=|r0|+i|r1| and positive real Z0=L_start/2, with Γ=(Z−Z0)/(Z+Z0). Its radius/phase makes a bounded chart. It cannot distinguish inversions or conjugations that preserve the two lengths. On six known optimal-path loss points in `atlas_beam_ab_20260928.json`, no dropped state entered a new coarse length-only chart sector.

An experimental structural impedance used Z=L+iC, Z0=L_start, where L=|r0|+|r1| and C is the cyclically reduced commutator length |[r0,r1]|. Four radial by four phase sectors gave one new sector at the six known beam-drop points (ac-03305 index 8); the other five remained old sectors. The chart is a diversity coordinate only. `make_smith_variant.py` creates a C beam variant with `BEAM_SMITH=0.5`: half of the existing second eye's 5,000 slots are first offered to chart sectors under equal caps, and remaining slots use the original plain eye. First eye, P2, quota, width, T8 and depth were held fixed.

| Row | Record AC/SAC | Baseline AC/SAC | Smith AC/SAC | Smith wall |
| --- | --- | --- | --- | --- |
| ac-03305 | 23/24 | 24/24 | 24/24 | 81.72 s |
| ac-05558 | 24/26 | 24/26 | 26/28 | 62.77 s |
| ac-04882 | 51/53 | 54/56 | 54/56 | target-specific pilot |

Both baseline and Smith AC paths replayed successfully through the pinned official AC core. The new diversity eye did not score, harmed ac-05558, and matched the above-record baseline on ac-04882. Do not add `BEAM_SMITH=0.5` to the production beam on these data. Raw paths/settings are in `smith_chart_trial_20260928.json`.

## Snell-style empirical channel

From 432 verified accepted AC paths (20–90 moves, filtered from `crossrow_roads_ac_20260928.json`) plus four pinned current near routes (`smith_snell_new4_20260928.jsonl`), the script replayed all 436 against the pinned official core. Smith sectors changed on 4,415 of 18,115 inner path steps; 346 crossings occurred at least five letters above starting total length.

For a *test only*, local rigidity R(s)=1+(number of the 14 legal moves that fail to lower total relator length)/14. At a radial-sector crossing, θ is the chart step's angle to the radial normal. Among 1,894 eligible interfaces, the observed next move's mean tie-aware candidate rank fraction was 0.4465 for constant-angle persistence and **0.4629 for |R_in sin²θ_in−R_out sin²θ_out|** (smaller is better, chance=0.5). The per-route mean worsening was +0.0224 with standard error 0.0027 over 432 routes with eligible interfaces. This empirical rigidity term degraded the routing signal; keep its beam weight zero. This does not test or refute a physical Snell/Clairaut law in the user's geometric papers.

## Reproduce

- Source commit baseline: `acc_beam.c` SHA-256 `5de1b5aea31e2defa0e70d6e9a0c867f66acc0ba4d613ad9821e96d489424caa`; T8 SHA-256 `38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8`; pinned SAIR `a0fd6e6`.
- Filter the crossrow file to `20 <= len <= 90` and `len(ac) == len`, save the resulting 432 JSON records to `work/smith_snell_paths.json`.
- Run `python3 research/acc/optimality/smith_snell_probe.py --manifest SAIR/competition/tools/verifier/data/manifest.json --verifier-root SAIR --paths work/smith_snell_paths.json --extra research/acc/live/ledger/smith_snell_new4_20260928.jsonl --max-routes 432`.
- Run `python3 research/acc/optimality/make_smith_variant.py`, then `gcc -O3 -march=native -I research/acc/optimality -o bin/acc_beam_smith work/acc_beam_smith.c -lm`, then `python3 research/acc/optimality/smith_trial.py`. Set `SAIR_ROOT` and `T8_PATH` if those paths differ.
- Full probe counts: `smith_snell_probe_20260928.json`. No inbox line was created.
