"""Independent replay of the frozen SAIR move specs (ac-r2-v1 and sac-r8-v1).

Written from the published move tables (move_spec.json, stable_move_spec.json)
and their notes, not from the official verifier's code. The official verifier
stays authoritative; this kernel is a second witness. When the two disagree the
harness refuses the path and opens a checker task (failure species S1: two
readings of one present that predict different futures).

Words are tuples of nonzero ints: 1=x, -1=x^-1, 2=y, -2=y^-1, 3..8 = g3..g8.
"""
from __future__ import annotations

import json
from pathlib import Path

AC_TARGET = ((1,), (2,))


class Spec:
    def __init__(self, data: dict):
        self.version = data["move_spec_version"]
        self.rows = {row["id"]: row for row in data["moves"]}
        self.count = len(self.rows)
        if sorted(self.rows) != list(range(self.count)):
            raise ValueError("move ids are not 0..n-1 in " + self.version)
        self.max_rank = data.get("max_rank", 2)
        target = data.get("target_relators")
        self.target = tuple(tuple(w) for w in target) if target is not None else AC_TARGET

    @classmethod
    def load(cls, path) -> "Spec":
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))


def reduce_word(letters) -> tuple:
    stack = []
    for a in letters:
        if stack and stack[-1] + a == 0:
            stack.pop()
        else:
            stack.append(a)
    return tuple(stack)


def inverse_word(word) -> tuple:
    return tuple(-a for a in word[::-1])


def step(state: tuple, row: dict, max_rank: int):
    """Apply one move row. Returns (new_state, None) or (None, reason)."""
    rank = len(state)
    kind = row["category"]
    if kind == "stabilize":
        if rank >= max_rank:
            return None, "max_rank_exceeded"
        return state + ((rank + 1,),), None
    i = row["relator"]
    if i >= rank:
        return None, "relator_out_of_rank"
    words = list(state)
    if kind == "destabilize":
        word = words[i]
        if len(word) != 1 or word[0] < 1:
            return None, "destabilize_precondition"
        g = word[0]
        rest = words[:i] + words[i + 1:]
        if any(abs(a) == g for w in rest for a in w):
            return None, "destabilize_precondition"

        def shift(a):
            if abs(a) <= g:
                return a
            return a - 1 if a > 0 else a + 1
        return tuple(tuple(shift(a) for a in w) for w in rest), None
    if kind == "inversion":
        words[i] = inverse_word(words[i])
        return tuple(words), None
    if kind == "multiplication":
        j = row["other"]
        if j >= rank:
            return None, "relator_out_of_rank"
        other = inverse_word(words[j]) if row["invert_other"] else words[j]
        words[i] = reduce_word(words[i] + other)
        return tuple(words), None
    if kind == "conjugation":
        c = row["conjugator"]
        if abs(c) > rank:
            return None, "generator_out_of_rank"
        words[i] = reduce_word((c,) + words[i] + (-c,))
        return tuple(words), None
    raise ValueError("unknown move category %r" % kind)


def replay(initial, moves, spec: Spec, limits: dict) -> dict:
    """Replay with the manifest limits. Error order follows the published spec:
    path length, then per move: id, applicability, relator length, work; then target."""
    if not isinstance(moves, list):
        return {"ok": False, "code": "E_MALFORMED"}
    if len(moves) > limits["max_path_length"]:
        return {"ok": False, "code": "E_PATH_TOO_LONG"}
    state = tuple(tuple(w) for w in initial)
    total = sum(len(w) for w in state)
    peak, work = total, total
    for index, m in enumerate(moves):
        if type(m) is not int or m not in spec.rows:
            return {"ok": False, "code": "E_BAD_MOVE_ID", "move_index": index}
        state, reason = step(state, spec.rows[m], spec.max_rank)
        if state is None:
            return {"ok": False, "code": "E_MOVE_NOT_APPLICABLE", "move_index": index,
                    "reason": reason}
        total = sum(len(w) for w in state)
        if total > limits["max_total_relator_length"]:
            return {"ok": False, "code": "E_LENGTH_LIMIT", "move_index": index}
        peak = max(peak, total)
        work += total
        if work > limits["max_work"]:
            return {"ok": False, "code": "E_WORK_BUDGET", "move_index": index}
    if state != spec.target:
        return {"ok": False, "code": "E_NOT_TARGET", "final_shape": [len(w) for w in state]}
    return {"ok": True, "length": len(moves), "peak": peak, "work": work}
