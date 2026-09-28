# Snell and Smith chart pilot — Codex, 2026-09-28 21:10Z

Source: user's `Snell_Smith_ACC.png` chart. It pools five recorded paths and reports especially slow average relator-length removal at total length 20–24 (0.04 letters per move, 257 moves). This is a hypothesis-generating sample, not a calibrated distance function.

## Snell band A/B on a sole-holder near miss

Target ac-00975: live AC record 34, SAC 36; baseline dual P2 beam with C16 finish found official AC 35 / SAC 37. Same source and flags in both controlled probes: T8, C16, W20000, DMAX36, `BEAM_H=1 BEAM_DIV=.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=.75 BEAM_C16=work/C16.tab`. Only the H-priority tie-break changed: `P += w` when total length was 20–24, with w=+20 (discourage dwelling) and w=-20 (opposite test). Both output paths replayed through pinned official AC and Stable AC cores.

| weight | AC | SAC | result |
|---:|---:|---:|---|
| 0 baseline | 35 | 37 | one over both records |
| +20 | 35 | 37 | identical best paths to baseline |
| -20 | 43 | 45 | worse |

This narrow band-only probe does not support adopting the chart as a beam key. It does not test a path-dependent Snell law, other weights, or other rows.

## Smith-chart exponent eye

For each state, let M be its 2x2 exponent-sum matrix and `tau=M.i`. I reflected lower-half-plane tau to upper half-plane when det(M)=-1, then measured the Cayley disk radius `abs((tau-i)/(tau+i))`. This reflection is my explicit modeling choice so inversion and swaps have finite scores; it is not a claim from the image.

Nine saved AC paths (seven mirror-beam outputs available at the time plus ac-00975 and ac-05149) yielded 326 move steps. Ranking all 14 legal children by lower disk radius put the saved move in the top three on 24.5% of steps (raw total relator length: 39.3%). On the 43 steps that climbed in length: 20.9% for the disk radius and 0% for raw length. On ten climbing conjugations: 0% for both. The paths are partly beam-generated and this is a small, biased offline screen; it only shows that radius alone was weak overall while it saw some climbs. No live beam adoption or scoring claim.

The exact pilot source is preserved at `research/acc/optimality/experiments/acc_beam_snell.c` (only the band term differs from `acc_beam.c`) and `research/acc/optimality/experiments/smith_eye_probe.py`. Recreate the 326-step offline sample from the first eight mirror JSONL results plus the two saved p2v AC paths. The local per-step output was `work/smith_eye_probe.json`. No new inbox line from this pilot. Continue the assigned 80-row AC mirror lane independently.
