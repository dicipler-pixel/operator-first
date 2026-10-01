# SOL61 independent search scope

The solver uses all 14 frozen `ac-r2-v1` moves, exact freely reduced ordered
relator pairs, iterative depth-limited DFS, and an exact backward goal ball.
It embeds no competition row or supplied control route. Its move port was
differential checked by the parent worker on 300 synthetic states (4,200
successor comparisons and 4,200 inverse checks, zero mismatches).

A found route has a prefix constrained by `--cap`; its reconstructed backward
suffix is constrained by `--ball-cap`. If the latter is larger, the full route
may exceed `--cap`. The official verifier's peak and work outputs determine
the final accepted route's limits. A found route is a candidate until that
verifier accepts it for a manifest-derived row.

A completed unsuccessful depth D rules out paths of length at most D whose
entire relator-total peak is at most `--cap`. It does not rule out higher
peaks. If a ball layer stops at its node or time limit, only its earlier fully
completed radius supports absence pruning. Absence pruning is enabled only
when `--ball-cap >= --cap`; otherwise the ball is only a witnessed suffix
index. Runtime interruption leaves the current depth incomplete.

The exact quotient pattern databases give admissible lower bounds because
exponent reduction modulo p, and evaluation of words in SL(2,p), commute with
every move. Their maximum is used, never their sum. The total-length lower
bound uses the determinant ±1 invariant to keep each relator nonempty. From
two unit relators, one move can grow total L by at most `max(L+2, 2L-1)`.

The transposition table stores the largest remaining budget at which a state
was entered, within one fixed depth iteration. A repeated state entered with
no larger budget can be discarded. All eligible children of its earlier
entry are processed if that iteration completes. Immediate inverse pruning
removes only a return to that entry's predecessor; that predecessor was
already entered with a strictly larger remaining budget, so this cannot
remove a bounded solution. Self-loops likewise cannot improve a shortest
path. Clearing the table at its configured limit only causes extra visits;
it adds no pruning. An interrupted iteration supplies no negative claim.

`check_bounded_search.py` uses only synthetic states. It compares radius-four
ground truth from the official core against positive and negative depth
answers, with both larger and smaller ball caps and tiny table limits that
force cache clears. Its raw output and exact settings are saved alongside
its summary. This is algorithm validation, not the required competition
control; `ac-09409` remains untested until its official manifest is obtained
and the independent search and official verifier both complete.
