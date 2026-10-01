"""Exact official-core replay of Grok's two-peel entry and a derived identity.

No search, challenge API, model worker, or submission is invoked.
"""
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
HARNESS = HERE.parents[2]
sys.path.insert(0, str(HARNESS / "vendor"))
from verifier.core import apply_move

CORE_PIN = "d2972711dc7008679127a987a8965d41ea1606b0fc50bf67e2e06c71c456b3b5"
assert hashlib.sha256((HARNESS / "vendor/verifier/core.py").read_bytes()).hexdigest() == CORE_PIN
LETTERS = {"x": 1, "X": -1, "y": 2, "Y": -2}
PRINT = {value: letter for letter, value in LETTERS.items()}
BLOCK = [6, 9, 9, 3, 7, 9, 9, 3, 0, 6, 6, 2, 9, 9]

def encode(word):
    return tuple(LETTERS[c] for c in word)

def text(state):
    return ["".join(PRINT[c] for c in word) for word in state]

def replay(start, moves, expected):
    state = tuple(encode(w) for w in start)
    trace = [{"step": 0, "state": text(state)}]
    for i, move in enumerate(moves, 1):
        state = apply_move(state, move)
        trace.append({"step": i, "move": move, "state": text(state)})
    assert text(state) == expected
    return {"start": start, "moves": moves, "length": len(moves),
            "final": text(state), "peak_total_length": max(sum(map(len, p["state"])) for p in trace),
            "trace": trace}

def main():
    cases = []
    for n in [6, 8, 10]:
        cases.append(replay(["X" + "y" * n + "x" + "Y" * (n + 1), "xxYYXyy"], BLOCK,
                            ["YYxxxx" + "y" * (n - 3) + "X" + "Y" * (n - 6), "xxYYXyy"]))
    doubling = []
    for k, d in [(4, 4), (8, 2)]:
        moves = [0] + [3, 7, 7] * k + [0]
        doubling.append(replay(["YY" + "x" * k + "y" * (d + 3) + "X" + "Y" * d, "xxYYXyy"],
                               moves, ["y" * (d + 1) + "X" + "Y" * d + "x" * (2 * k), "xxYYXyy"]))
    def finish(m):
        # Formula relayed by UPGH; no solver code was imported or run.
        return ([4, 1, 11, 3, 8, 8, 4] + [7] * (m - 1) + [12, 5, 12, 5]
                + [6] * (m - 2) + [8, 11, 4, 12, 2, 4, 4, 6, 3] + [5] * (m - 2))

    def cyclic_entry(n):
        # Invert r0, and rotate r1 to XyyxxYY in three paid conjugations.
        moves = [0, 12, 12, 11]
        power = 1
        for _ in range(n // 2 - 1):
            # For y^q X Y^(q-1) x^power, cut after the first x.
            # Each multiply rewrites a suffix YYx to xxYY.
            moves += [6] * (power - 1) + [2]
            moves += [m for _ in range(power - 1) for m in [7, 2]]
            moves += [9, 9]
            power *= 2
        # Restore r1, then move yyyX from the beginning to the end.
        moves += [10, 13, 13, 9, 9, 9, 6]
        return moves

    finishes = [replay(["YY" + "x" * m + "yyyX", "xxYYXyy"], finish(m), ["x", "y"])
                for m in [4, 16]]
    n6_full = replay(["XyyyyyyxYYYYYYY", "xxYYXyy"], BLOCK + finish(4), ["x", "y"])
    n10_start = ["X" + "y" * 10 + "x" + "Y" * 11, "xxYYXyy"]
    n10_entry = replay(n10_start, cyclic_entry(10), ["YY" + "x" * 16 + "yyyX", "xxYYXyy"])
    n10_full = replay(n10_start, cyclic_entry(10) + finish(16), ["x", "y"])
    report = {
        "official_core_sha256": CORE_PIN,
        "grade": "V",
        "scope": "synthetic family endpoints; no scored route claim",
        "quoted_block_checks": cases,
        "derived_doubling_identity": doubling,
        "finish_formula_source_git_blob": "080073cb572109daf66f58641de2326e709ba22d",
        "finish_formula_checks": finishes,
        "n6_full_verified": n6_full,
        "n10_constructive_entry56_verified": n10_entry,
        "n10_full119_verified_not_competitive": n10_full,
        "interpretation": {
            "n6_entry_14_verified": True,
            "n10_entry_14_reaches_x_run": 4,
            "n10_entry_48_verified": False,
            "finA2_verified_for_m4_m16": True,
            "derived_doubling_preserves_r1": True,
            "derived_doubling_ends_in_rotated_frame": True,
            "temporary_r1_changes": "legal in full AC graph; frozen r1 is a construction restriction",
            "n10_entry56_is_scaffold_only": "exceeds entry48 budget; known team routes are reported shorter",
        },
    }
    (HERE / "replay_receipt.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"quoted_checks": len(cases), "doubling_checks": len(doubling), "n10_entry48": False}))

if __name__ == "__main__":
    main()
