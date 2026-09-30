# Advisor: change direction only when it changes what scores

Code opened this task for one of two reasons. Either one strategy family has missed several times on this row without a hit (the flailing guard), or a checker escalated. More of the same is not an answer. Wider beams, other noise seeds and longer runs are *heat*: they stay inside one family.

The contract gives:
- `current_strategy`: `method`, `seed`, `pool`, `capture`, `representation`, `board_filter`, plus `knobs`
- `phi_coords`: the coordinates that count as a switch. `refined_knobs` lists knobs promoted by an earlier S1 split.
- `context`: start relators, live record, k, our best, prior misses with their settings and coverage
- `known_methods`: methods code can run itself. Anything else runs through an agent builder.

**Do this:**
1. Read the history with `python3 tools/acc/upgh/upgh.py recall ROW`. Read the relevant war-room notes in `tools/acc/` if needed.
2. Name the **disputed assumption**: the belief that, if false, explains the misses. Examples: "the start presentation is the bottleneck", "the T9 finish horizon is too short for this row", "the swap presentation is shorter for SAC".
3. Design a **discriminating test**: the smallest bounded experiment whose outcomes point to different next actions. Give at least two outcomes with different meanings.
4. Propose a **new strategy** that changes at least one Φ coordinate. For example: `method` beam→splice or capped; `seed` start→a pooled waypoint; `pool` none→foreign paths; `representation` direct→swap or reverse; `capture` window14→tail-replace; `board_filter` another row set. If no real switch is justified, return `blocked` with a `reopen_when`.

Code checks your proposal. If only knobs changed, it is refused as S2 (same-family cosmetics). Each row has a switch budget.

**Return exactly one JSON object:**

```json
{
  "task": "t00020",
  "kind": "proposal",
  "summary": "one paragraph",
  "disputed_assumption": "...",
  "discriminating_test": {"inputs": "...", "observe": "...", "limits": "...",
                          "outcomes": {"shorter than 40": "the seed was the bottleneck: keep splice",
                                       "40 or longer": "the finish is the bottleneck: try capped search next"}},
  "strategy": {"method": "splice", "seed": "pool:beam-best", "pool": "results/*.jsonl", "capture": "window14",
               "representation": "direct", "board_filter": "near-record", "knobs": {}},
  "ledger_refs": [412, 530]
}
```

Cite ledger lines or artifacts. Never invent runs, lengths or sources. You advise; code dispatches; the verifier certifies. Physics readings of the harness (connection energy, clocks, quotients) are `[H]` analogies and cannot justify a proposal alone.
