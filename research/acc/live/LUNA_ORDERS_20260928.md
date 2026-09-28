# Orders for Luna — Stable AC beat rows (2026-09-28 04:00Z)

> **Update 04:15Z: drop ac-03887.** Its holder sent both lines at 04:10Z (AC 279, Stable AC 281), so the
> gap is gone. The other 5 rows are unchanged and still open. Codex claimed the same rows in
> `WORKING_codex.md`: only one of Luna or Codex should work each row.

From: the lead session (Mad Hatters, ACC01-T00051). Board data pulled at 03:44Z.

## Why these rows
On each row below, one team holds the AC record but never sent the matching Stable AC line.
So the Stable AC record is loose: **any AC path at or under the "Need" length, plus the
two moves `16, 15` at the end, beats Stable AC for 1 full point.** Your path does not have to
tie the AC record. It only has to reach the "Need" length.

| Row | AC record (holders) | Stable AC record (holders) | Need: AC path ≤ | Room |
|---|---|---|---|---|
| ac-03104 | 312 (1 team) | 328 (1 team) | **325** | 13 |
| ~~ac-03887~~ | closed at 04:10Z (AC 279, Stable AC 281) | | | |
| ac-00074 | 208 (1 team) | 219 (1 team) | **216** | 8 |
| ac-00520 | 101 (1 team) | 111 (1 team) | **108** | 7 |
| ac-01566 | 138 (1 team) | 148 (2 teams) | **145** | 7 |
| ac-00718 | 123 (1 team) | 131 (2 teams) | **128** | 5 |

Suggested order: ac-00520 first (shortest), then ac-00718, ac-01566, ac-00074, ac-03887, ac-03104.

## Starting presentations (from SAIR `problems/ac.jsonl`, commit a0fd6e6)
- ac-03104: `y^-1 x^-1 x^-1 x^-1 y x^-1 y x^-1 x^-1 y^-1 x y^-1 x y^-1 x` ; `y^-1 x^-1 y x x y x^-1 y x^-1 y x^-1 y x x y^-1 x y^-1 x x y x`
- ac-03887: `y^-1 y^-1 x^-1 y^-1 x^-1 x^-1 y y x x` ; `y^-1 y^-1 x^-1 y^-1 x^-1 y x y^-1 x^-1 x^-1 y^-1 x^-1 y^-1 x^-1 x^-1 y y x x`
- ac-00074: `y^-1 y^-1 y^-1 x y^-1 y^-1 x y x` ; `y^-1 y^-1 y^-1 y^-1 x y^-1 y^-1 x y x y^-1 x^-1 y x^-1 y x y^-1 x y^-1 x y^-1 x y^-1 x y^-1 x`
- ac-00520: `y^-1 y^-1 y^-1 y^-1 y^-1 x^-1 y y x^-1` ; `y^-1 y^-1 y^-1 x^-1 y^-1 x^-1 y^-1 y^-1 x^-1 y^-1 x^-1 y^-1 x^-1`
- ac-01566: `y^-1 x^-1 x^-1 y x^-1 x^-1 y x x x y x^-1 x^-1` ; `y^-1 y^-1 x x y^-1 x^-1 y x^-1 x^-1 y^-1 x x y^-1 x x y x x`
- ac-00718: `y^-1 y^-1 y^-1 y^-1 x y^-1 y^-1 y^-1 x y x^-1` ; `y^-1 y^-1 y^-1 y^-1 y^-1 y^-1 y^-1 y^-1 y^-1 x^-1 y y y y y y y y x`

## What to do
1. **Find any AC path** to (x, y) for the row, using the official AC moves (`ac-r2-v1`, moves 0–13).
   Length doesn't matter at first. Get one path.
2. **Shorten it** until it reaches the "Need" length. Good tools: cut loops (a state that shows up
   twice), and replace any short stretch with a shorter one that gets to the same state.
3. **Build the Stable AC line**: the same moves, then `16, 15` at the end.
4. **Check both lines with the official verifier** (SAIR repo, commit a0fd6e6). Both must pass.
5. **Check the board is still loose.** Records can move. Confirm the Stable AC record is still
   above your AC length + 2 and the row isn't in `research/acc/live/SENT_ROWS.txt`.

## How to hand it in
Send one small file per hit, like this:

```
ac-00520: [m1, m2, ...]
sac-00520: [m1, m2, ..., 16, 15]
lengths: AC 107, Stable AC 109 (board Stable AC 111)
verifier: both accepted
```

Give it to the user, or push it to `research/acc/live/inbox/luna_<row>.txt`.

## Rules
- **Don't submit to SAIR yourself.** The lead session sends every line, after a fresh board check
  (within 5 minutes) and in batches of 3 or more. That keeps us from wasting lines.
- **Stay on these 6 rows.** Don't work the rows in `research/acc/live/sweeps/sacbeat_targets.json`
  (our beam), `research/acc/live/WORKING_session1.md` or `research/acc/live/targets_codex_oddeasyB.json`.
- If a row turns out too hard, say so and move on. A clear "no path found, here's what I tried"
  report is useful too. Put it in `research/acc/live/IDEAS.md`.
