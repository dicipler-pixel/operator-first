"""Adapter over the OFFICIAL SAIR move semantics.  No fallback, no local table.

Everything here delegates to the vendored verifier at the pinned commit
(`vendor/PROVENANCE.json`).  There is deliberately no locally-written move
table and no inferred index ordering: a wrong guess produces runs that
complete, report numbers and are wrong.
"""

from __future__ import annotations

import json
import os
import sys
from typing import List, Sequence, Tuple

_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_VENDOR = os.path.join(_HERE, "vendor")
if _VENDOR not in sys.path:
    sys.path.insert(0, _VENDOR)

from verifier import core as _core          # noqa: E402
from verifier.canon import move_spec_hash    # noqa: E402

Presentation = Tuple[Tuple[int, ...], ...]

ORDINARY_SPEC = os.path.join(_VENDOR, "verifier", "data", "move_spec.json")
STABLE_SPEC = os.path.join(_VENDOR, "verifier", "data", "stable_move_spec.json")

PINS = {
    "ac-r2-v1": "sha256:e13f57d82b5db1a79c1bd9d5ee1f6665ac4d96a634a3656ea20c0ada82e07643",
    "sac-r8-v1": "sha256:27ecd0ebd4af39871cbfb23ecbd8be73710e85e04d8be788c1d81117d9f4b2b0",
}


def load_spec(path: str = ORDINARY_SPEC) -> dict:
    """Load a move spec and refuse it unless it hashes to its pinned value."""
    with open(path) as fh:
        spec = json.load(fh)
    version = spec["move_spec_version"]
    computed = move_spec_hash(spec["moves"])
    if computed != spec["move_spec_hash"]:
        raise SystemExit(f"{path}: self-declared move_spec_hash does not match its moves")
    if version not in PINS:
        raise SystemExit(f"{path}: unpinned move_spec_version {version!r}")
    if computed != PINS[version]:
        raise SystemExit(f"{path}: {version} hashes to {computed}, pinned value is {PINS[version]}")
    return spec


SPEC = load_spec()
MOVES: List[dict] = SPEC["moves"]
N_MOVES = len(MOVES)
DESCRIPTIONS = {int(k): v for k, v in SPEC["descriptions"].items()}
TARGET: Presentation = tuple(tuple(w) for w in SPEC["target_relators"])

#: ``INVERSE[i]`` is the id undoing move ``i``.  The ordinary set IS closed
#: under inversion (0,1 self-inverse; 2<->3, 4<->5, 6<->7, 8<->9, 10<->11,
#: 12<->13), so forward and backward search share one table.
INVERSE: List[int] = [m["inverse"] for m in MOVES]
assert all(INVERSE[INVERSE[i]] == i for i in range(N_MOVES)), "inverse column is not an involution"


def apply_move(pres: Presentation, move_id: int) -> Presentation:
    """Official ``core.apply_move``.  Takes the move id, applies free reduction."""
    return _core.apply_move(pres, move_id)


def apply_path(pres: Presentation, path: Sequence[int]) -> Presentation:
    for move_id in path:
        pres = apply_move(pres, move_id)
    return pres


def children(pres: Presentation):
    for move_id in range(N_MOVES):
        yield move_id, apply_move(pres, move_id)


def parents(pres: Presentation):
    """Backward step.  Uses the same table via the official inverse column."""
    for move_id in range(N_MOVES):
        yield move_id, apply_move(pres, INVERSE[move_id])
