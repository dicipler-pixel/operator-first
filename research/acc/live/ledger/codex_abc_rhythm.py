"""Move-rhythm test on the official 424 AC training solutions.

The null shuffles moves within each route, preserving length and exact move
counts. A held-out Markov test measures whether transitions generalize to
different routes. Usage: python codex_abc_rhythm.py training_424.json
"""
import collections
import json
import math
import random
import sys

SEED = 20260928
REPS = 1000


def category(move):
    return 0 if move < 2 else 1 if move < 6 else 2 if move < 10 else 3


def transitions(routes, mapper):
    return [(mapper(a), mapper(b)) for route in routes
            for a, b in zip(route, route[1:])]


def score(routes, mapper):
    pairs = transitions(routes, mapper)
    tally = collections.Counter(pairs)
    left = collections.Counter(a for a, _ in pairs)
    right = collections.Counter(b for _, b in pairs)
    n = len(pairs)
    mi = sum(v / n * math.log2(v * n / (left[a] * right[b]))
             for (a, b), v in tally.items())
    same = sum(a == b for a, b in pairs) / n
    inv = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4,
           6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10,
           12: 13, 13: 12}
    undo = (sum(b == inv[a] for a, b in pairs) / n
            if mapper is int else None)
    return {"mutual_information_bits": mi, "same_fraction": same,
            "undo_fraction": undo, "transitions": n}


def heldout_gain(routes, mapper, width):
    rng = random.Random(SEED)
    order = list(range(len(routes)))
    rng.shuffle(order)
    train_ids = set(order[:int(len(order) * .8)])
    train = [r for i, r in enumerate(routes) if i in train_ids]
    test = [r for i, r in enumerate(routes) if i not in train_ids]
    t = collections.Counter(transitions(train, mapper))
    left = collections.Counter(a for (a, _), v in t.items() for _ in range(v))
    uni = collections.Counter(mapper(x) for route in train for x in route)
    total = sum(uni.values())
    log_gain = 0.0
    count = 0
    for a, b in transitions(test, mapper):
        p0 = (uni[b] + 1) / (total + width)
        p1 = (t[a, b] + 1) / (left[a] + width)
        log_gain += math.log2(p1 / p0)
        count += 1
    return log_gain / count


def main(path):
    data = json.load(open(path))
    routes = [item["moves"] for item in data["instances"]]
    assert len(routes) == 424
    rng = random.Random(SEED)
    result = {"dataset": path, "routes": len(routes),
              "moves": sum(map(len, routes)), "null": "shuffle within each route",
              "seed": SEED, "repetitions": REPS, "metrics": {}}
    for name, mapper, width in [("move_id", int, 14),
                                ("move_category", category, 4)]:
        obs = score(routes, mapper)
        obs["heldout_markov_gain_bits_per_move"] = heldout_gain(
            routes, mapper, width)
        null = []
        for _ in range(REPS):
            shuffled = [rng.sample(route, len(route)) for route in routes]
            s = score(shuffled, mapper)
            s["heldout_markov_gain_bits_per_move"] = heldout_gain(
                shuffled, mapper, width)
            null.append(s)
        summary = {}
        for key in ("mutual_information_bits", "same_fraction",
                    "undo_fraction", "heldout_markov_gain_bits_per_move"):
            if obs[key] is None:
                continue
            vals = sorted(x[key] for x in null)
            # Two sided rank test with the +1 finite permutation correction.
            low = sum(x <= obs[key] for x in vals)
            high = sum(x >= obs[key] for x in vals)
            summary[key] = {
                "observed": obs[key],
                "null_mean": sum(vals) / len(vals),
                "null_95_interval": [vals[24], vals[974]],
                "p_two_sided": min(1.0, 2 * min(low + 1, high + 1) / (REPS + 1))}
        result["metrics"][name] = summary
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
