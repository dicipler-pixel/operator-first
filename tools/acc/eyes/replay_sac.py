"""Independent replay of Stable AC moves (sac-r8-v1, moves 0-256).

Written from competition/tools/verifier/data/stable_move_spec.json and the
published move semantics; shares no code with the official verifier.

State: tuple of freely reduced relator tuples over nonzero ints, +g / -g,
with g1 = x and g2 = y. Rank starts at 2 and stabilization may raise it to
MAX_RANK = 8. The target is the EMPTY presentation ().
"""
MAX_RANK = 8

def free_reduce(w):
    o = []
    for a in w:
        if o and o[-1] == -a:
            o.pop()
        else:
            o.append(a)
    return tuple(o)

def invert(w):
    return tuple(-a for a in reversed(w))

def _build_table():
    rows = [{"id": 0, "category": "inversion", "relator": 0},
            {"id": 1, "category": "inversion", "relator": 1}]
    rows.append({"id": 2, "category": "multiplication", "relator": 0, "other": 1, "invert_other": False})
    rows.append({"id": 3, "category": "multiplication", "relator": 0, "other": 1, "invert_other": True})
    rows.append({"id": 4, "category": "multiplication", "relator": 1, "other": 0, "invert_other": False})
    rows.append({"id": 5, "category": "multiplication", "relator": 1, "other": 0, "invert_other": True})
    for i in (0, 1):
        for c in (1, -1, 2, -2):
            rows.append({"id": 6 + i * 4 + [1, -1, 2, -2].index(c),
                         "category": "conjugation", "relator": i, "conjugator": c})
    rows.append({"id": 14, "category": "stabilize"})
    for i in range(8):
        rows.append({"id": 15 + i, "category": "destabilize", "relator": i})
    return {r["id"]: r for r in rows}

TABLE = _build_table()

def _relabel_after(word, g):
    return tuple(a - 1 if a > g else (a + 1 if a < -g else a) for a in word)

def apply_move(state, m):
    """Returns (new_state, None) or (None, reason)."""
    row = TABLE.get(m)
    if row is None:
        return None, "unsupported_move_id"      # rank>=3 ids 23..256 not modelled here
    cat = row["category"]
    k = len(state)
    if cat == "stabilize":
        if k >= MAX_RANK:
            return None, "max_rank_exceeded"
        return state + ((k + 1,),), None
    i = row["relator"]
    if i >= k:
        return None, "relator_out_of_rank"
    if cat == "destabilize":
        word = state[i]
        if len(word) != 1 or word[0] <= 0:
            return None, "destabilize_precondition"
        g = word[0]
        for j, other in enumerate(state):
            if j == i:
                continue
            if any(a == g or a == -g for a in other):
                return None, "destabilize_precondition"
        rest = state[:i] + state[i + 1:]
        return tuple(_relabel_after(w, g) for w in rest), None
    if cat == "inversion":
        return state[:i] + (invert(state[i]),) + state[i + 1:], None
    if cat == "multiplication":
        j = row["other"]
        if j >= k:
            return None, "relator_out_of_rank"
        other = state[j]
        if row["invert_other"]:
            other = invert(other)
        return state[:i] + (free_reduce(state[i] + other),) + state[i + 1:], None
    c = row["conjugator"]
    if abs(c) > k:
        return None, "generator_out_of_rank"
    return state[:i] + (free_reduce((c,) + state[i] + (-c,)),) + state[i + 1:], None

def verify(initial, moves):
    """Replay `moves` from `initial`. Returns (ok, detail)."""
    state = tuple(free_reduce(tuple(r)) for r in initial)
    for n, m in enumerate(moves):
        if not isinstance(m, int) or not (0 <= m <= 256):
            return False, f"bad move id {m!r} at index {n}"
        state, reason = apply_move(state, m)
        if state is None:
            return False, f"move {m} not applicable at index {n}: {reason}"
        if any(len(r) == 0 for r in state):
            return False, f"empty relator after move {m} at index {n}"
    if state != ():
        return False, f"ended at rank {len(state)}, not the empty presentation"
    return True, "empty presentation reached"
