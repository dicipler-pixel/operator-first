# Height/depth search as a Pareto frontier: bounded pilot

**Status:** exploratory method test; no competition candidate or score claim.

## Source and graph boundary

Read the Drive note [ACC-P000009 — Detour width on two Andrews–Curtis graphs](https://drive.google.com/file/d/1j1cCMzxlhcy41B3mfuQmxVaLphs3hruH/view). It separates the official Lean graph, whose conjugation can use an arbitrary word, from the Discovery Track graph `ac-r2-v1`, whose conjugators are single letters. Those graphs have different height behavior; this note uses only the scored 14-move graph.

For an exact state pair, let `L` be its total freely reduced relator length. Along a solution-relevant path from a trivial rank-2 presentation, `L >= 2`: AC moves preserve the normal closure, so the two relators cannot have total length 0 or 1 and still normally generate (F_2).

- Inversion leaves `L` unchanged.
- A multiplication has `L_next <= L + length(donor) <= 2L).
- A generator-letter conjugation has `L_next <= L + 2 <= 2L).

Thus any path of at most `d` moves from an input of total length `L0` has height at most `L0 * 2^d`. This is a finite completeness cap for a fixed depth, but it becomes enormous quickly. For ac-00145, `L0=15`: depth 38 (needed to beat its recorded 39) gives `15 * 2^38 = 4,123,168,604,160`; depth 39 gives `15 * 2^39 = 8,246,337,208,320`. These bounds are mathematically finite and computationally unusable.

## Exact two-objective search

At each exact ordered state, retain nondominated labels `(g,H)`, where `g` is moves from the start and `H` is the maximum total relator length seen on that witness. A label is dominated if another label has both no greater move count and no greater peak. Dominance is safe because appending the same suffix cannot make the dominated label shorter or lower in peak.

At the target, the shortest path under cap `C` is `min(g : H <= C)`. This answers multiple cap queries from one label search. It may still use more time and memory than separate capped BFS, so the label frontier is a hypothesis about reuse, not a claimed speedup.

## Synthetic exact control

The accompanying script uses the pinned official AC move kernel. Start at `(x,y)`; apply seed `[6,4,12,4,12]` to define target `(x, y^3 x y^-1 x y^-1)`; search all paths through depth 5.

- Pareto target frontier: `(g,H) = (4,8)`.
- Separate capped BFS agrees: caps 2–7 find no route through depth 5; cap 8 finds shortest distance 4.
- Pareto pass: 40,779 states, 40,803 labels, 5,117 expanded labels, 71,638 transitions, about 0.18 s.
- Separate cap BFS for 2–8: 3,929 expanded states and 55,005 transitions in total (8,881 summed per-cap seen-state counts).

The profile is correct on this control, but Pareto used about 30% more transitions. This is a negative performance result for the small test, not evidence about hard ACC rows. Reproduction script: `pareto_height_pilot_20260928.py`.

## Search bookkeeping consequence

Keep these values separate:

- `known_route_peak`: a feasible height for one witness;
- `closed_cap_through`: a cap range actually exhausted with a complete frontier;
- `tested_depth`: the exact depth bound covered.

The ac-00145 40-move witness has peak 31, so cap 31 contains that witness. It does not mean all states below height 31 were searched. A search may skip lower caps only if its exact closure ledger records their exhaustion. The independent route replay and full trajectory are preserved in `ac-00145_route_peak_audit_20260928.json`.

## Next test

Do not replace the capped sweep on this evidence. If a non-active short row becomes available, compare the Pareto label count and transitions against the existing cap-jump scheduler at identical depth, cap, and memory limits. Keep the two graphs and all incomplete frontiers clearly labeled.
