# Rival activity, 2026-09-30 07:11Z → 14:02Z (board diff, 0 API calls)

Source boards: `research/acc/live/boards/{ac,stable_ac}_20260930T0711Z.json.gz` (team pull) and
`research/acc/upgh/cache/boards/*_20260930T1402*Z.json.gz` (UPG-H pull, sha256 in the ledger). Grade C (SAIR data), analysis V.

| | AC | Stable AC |
|---|---:|---:|
| Record dropped | 50 | 51 |
| New solves | 0 | 0 |
| Rows whose team count rose (new ties) | 1,235 | 134 |

- Record drops sit mostly on long rows: AC old records 40–79 hold 42 of the 50 drops; SAC 40–79 hold 42 of 51.
- Drop size is small: AC 28× −1, 15× −2; SAC 33× −1, 14× −2. The new holders are single teams (k = 1).
- Reading `[H]`: leaders are shortening long paths by one or two moves (local window or tail rewriting), plus a broad AC tie campaign. Stable AC ties grew ten times more slowly.

What UPG-H does with it:
1. A fresh k = 1 record is worth 0.5 to tie. Rows where we are within 1–3 moves stay in the near-record targets.
2. Stable AC is less crowded, so SAC twins are grouped with their AC row (one beam serves both), and every checked AC path also yields P + [16,15].
3. An advisor switch toward long-path shortening (`capture`: window → tail rewrite, on rows with records 40–70 where we are behind by 1–2) is the natural next Φ move. It must name its discriminating test.
