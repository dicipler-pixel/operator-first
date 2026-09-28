#!/usr/bin/env python3
"""Price Lisitsa's MS(3..9) archive in the pinned ac-r2-v1 move graph.

Input: the author's Zenodo v2 ZIP and the companion ms_lisitsa_replay.py.
Produces exact ordinary AC paths to the ordered target (x,y), but they
are not expected to match competition records. No stable AC is inferred.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

LETTERS = {"a": 1, "A": -1, "b": -2, "B": 2}  # a=x, b=Y
CONJ0 = {"a": 6, "A": 7, "b": 9, "B": 8}
CONJ1 = {c: m + 4 for c, m in CONJ0.items()}
PRELUDE = [8, 6, 1]  # R0 -> P1 by two conjugations; invert R1 -> P0
RECORD = {5: 80, 6: 145, 7: 275, 8: 532, 9: 1046}


def word(w):
    return tuple(LETTERS[c] for c in w)


def load_replay(path):
    spec = importlib.util.spec_from_file_location("ms_lisitsa_replay", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def conjugation_moves(z, affected):
    lookup = CONJ0 if affected == 0 else CONJ1
    return [lookup[c] for c in reversed(z)]


def generate(n, rows, audit, apply_move):
    # SAIR ordering is (fixed second Lisitsa relator, changing first).
    state = (tuple([-2, -1, -1, 2, 1]),
             tuple([-2] * (n + 1) + [-1] + [2] * n + [1]))
    path = []
    max_total = sum(map(len, state))
    work = max_total
    counts = Counter()

    def push(moves):
        nonlocal state, max_total, work
        for m in moves:
            state = apply_move(state, m)
            path.append(m)
            total = sum(map(len, state))
            max_total = max(max_total, total)
            work += total

    push(PRELUDE)
    assert state == (word(audit.SECOND), word(rows[0][0])), (n, state)
    archive_positions = [(state, len(path))]
    for i, ((u, op), (v, _)) in enumerate(zip(rows, rows[1:]), 1):
        if op == "INV":
            moves = [1]
        elif op == "MULT":
            moves = [4]
        elif op == "CONJ":
            z = audit.conjugator(u, v)
            assert z is not None, (n, i)
            moves = conjugation_moves(z, 1)
        else:
            raise ValueError((n, i, op))
        counts[op] += 1
        push(moves)
        assert state == (word(audit.SECOND), word(v)), (n, i, op, state, v)
        archive_positions.append((state, len(path)))

    archive_length = len(path)
    pair = [audit.TARGET, audit.SECOND]
    for j, op, z, expected in audit.TAIL:
        affected = 1 - j
        if op == "INV":
            moves = [affected]
        elif op == "MULT":
            moves = [2 if affected == 0 else 4]
        elif op == "CONJ":
            moves = conjugation_moves(z, affected)
        else:
            raise ValueError((j, op))
        push(moves)
        pair = list(expected)
        assert state == (word(pair[1]), word(pair[0])), (n, j, state)
    assert state == ((1,), (-2,)), (n, state)
    push([1])  # invert Y to y
    assert state == ((1,), (2,))
    return path, archive_positions, {
        "n": n, "row": {5:"ac-01950",6:"ac-02033",7:"ac-06796",
                     8:"ac-03079",9:"ac-06727"}.get(n),
        "archive_moves": sum(counts.values()),
        "archive_counts": dict(counts),
        "priced_archive_plus_prelude": archive_length,
        "total_scored_moves": len(path),
        "record": RECORD.get(n),
        "peak_total_relator_length": max_total,
        "work": work,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("zipfile", type=Path)
    p.add_argument("--replay-script", type=Path,
                   default=Path(__file__).resolve().parents[3] /
                   "tools/acc/ms_lisitsa_replay.py")
    p.add_argument("--sair-root", type=Path, required=True)
    p.add_argument("--json-out", type=Path)
    p.add_argument("--moves-out", type=Path,
                   help="optional full scored paths, for graph reuse")
    args = p.parse_args()
    audit = load_replay(args.replay_script)
    assert hashlib.md5(args.zipfile.read_bytes()).hexdigest() == audit.EXPECTED_MD5
    sys.path.insert(0, str(args.sair_root / "competition/tools"))
    from verifier.core import apply_move, verify

    result = {"source_commit": "a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e",
              "zip_md5": audit.EXPECTED_MD5, "rows": []}
    all_paths = {}
    with ZipFile(args.zipfile) as archive:
        for n in range(3, 10):
            rows = audit.replay(archive, n)
            path, states, info = generate(n, rows, audit, apply_move)
            initial = (tuple([-2, -1, -1, 2, 1]),
                       tuple([-2] * (n + 1) + [-1] + [2] * n + [1]))
            challenge = {"challenge_id": info["row"] or f"synthetic-ms-{n}",
                         "move_spec_version": "ac-r2-v1",
                         "initial_relators": initial,
                         "target_relators": ((1,), (2,))}
            verified = verify(
                challenge, path, "ac-r2-v1",
                {"max_path_length": 100000,
                 "max_total_relator_length": 10000,
                 "max_work": 5000000})
            assert verified["ok"], (n, verified)
            info["synthetic_verify"] = verified
            result["rows"].append(info)
            all_paths[n] = path
    if args.moves_out:
        args.moves_out.write_text(
            json.dumps({f"MS-{n}": path for n, path in all_paths.items()})
            + "\n")
    if args.json_out:
        args.json_out.write_text(json.dumps(result, indent=2) + "\n")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
