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
    report = {
        "official_core_sha256": CORE_PIN,
        "grade": "V",
        "scope": "synthetic family endpoints; no scored route claim",
        "quoted_block_checks": cases,
        "derived_doubling_identity": doubling,
        "interpretation": {
            "n6_entry_14_verified": True,
            "n10_entry_14_reaches_x_run": 4,
            "n10_entry_48_verified": False,
            "finA2_not_supplied_and_not_verified": True,
            "derived_doubling_preserves_r1": True,
            "derived_doubling_ends_in_rotated_frame": True,
            "temporary_r1_changes": "legal in full AC graph; frozen r1 is a construction restriction",
        },
    }
    (HERE / "replay_receipt.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"quoted_checks": len(cases), "doubling_checks": len(doubling), "n10_entry48": False}))

if __name__ == "__main__":
    main()
