# ACC collaboration — public-safe branch

This folder is the shared **code lane** for Team Dicipler's SAIR Andrews–Curtis work. It deliberately contains **no live Discovery move list, no private submission certificate, and no solved-instance payload**.

## What to use

1. `ACC_EYES_FIRST_MATRIX_SECOND_2026-09-11.py` — the current all-eyes scan: record every raw eye first, compute independent set outputs second, combine them into Matrix routing only afterward.
2. `ACC_Whole_Eye_Public_2026-09-11.py` — the newest ACC-specific Compound Eye route. It adds the two-step **next-space eye**, separate planner lanes, diversity routing, shared exact reverse target memory, exact rank-2 abelian shadow, and persistent miss traces.
3. `CLAUDE_TARGET_2_HANDOFF.md` — Claude's parallel assignment. Use the **second official Discovery row/ID** exactly as written in the live pool.

The full exact replay/search engine is carried in the private handoff package as `ACC_Cosmic_Matrix_Mixer_LIVE_2026-09-11.py`; do not commit live certificates from it to this public repository.

## Current Compound Eye idea

This is newer than simply blending heuristic scores. The operating rule is **route, don't vote**. The question for a move is not only whether it immediately improves total word length; it is also whether it changes the space of useful moves available next. The ACC implementation therefore preserves:

- independent eyes before combination;
- independent set outputs before the Matrix score;
- exact one-step neighborhoods;
- a two-step next-space/mobility eye;
- diversity lanes instead of a single winner score;
- shared target-DAG memory across all ordinary-AC instances;
- exact replay and local shortening;
- a persistent ledger of surfaced wins and seen-but-unsolved cases.

The broader Universal Compound Eye remains the conceptual parent, but these files are the **current ACC-specific working form**.

## Competition safety

Keep official challenge data and all move certificates local/private. Do not commit generated `*.private.json`, submission text, or solved move lists to this public repository while the competition is live.
