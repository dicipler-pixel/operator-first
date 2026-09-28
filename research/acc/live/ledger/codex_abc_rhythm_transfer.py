"""Does training move rhythm distinguish tie roads on the crossrow atlas?"""
import collections
import json
import math
import random
import sys

INV = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)
train = [x["moves"] for x in json.load(open(sys.argv[1]))["instances"]]
roads = json.load(open(sys.argv[2]))
pair = collections.Counter((a, b) for r in train for a, b in zip(r, r[1:])
                           if b != INV[a])
uni = collections.Counter(x for r in train for x in r)
total = sum(uni.values())


def score(route):
    values = []
    for a, b in zip(route, route[1:]):
        if b == INV[a]:
            continue
        n = sum(pair[a, c] for c in range(14) if c != INV[a])
        p1 = (pair[a, b] + 1) / (n + 13)
        p0 = (uni[b] + 1) / (total - uni[INV[a]] + 13)
        values.append(math.log2(p1 / p0))
    return sum(values) / len(values) if values else 0.0


def auc(rows):
    tie = [r["rhythm"] for r in rows if r["gap"] == 0]
    trail = [r["rhythm"] for r in rows if r["gap"] > 0]
    if not tie or not trail:
        return None
    return sum((a > b) + .5*(a == b) for a in tie for b in trail) / (
        len(tie) * len(trail))


data = [{"id": x["id"], "live": x["live"], "gap": x["len"] - x["live"],
         "rhythm": score(x["ac"])} for x in roads]
observed = auc(data)
rng = random.Random(20260928)
null = []
for _ in range(1000):
    labels = [r["gap"] for r in data]
    # Shuffle tie/trail labels within 5-move live-record bins.
    for bin_id in set(r["live"]//5 for r in data):
        indexes = [i for i, r in enumerate(data) if r["live"]//5 == bin_id]
        shuffled = [labels[i] for i in indexes]
        rng.shuffle(shuffled)
        for i, label in zip(indexes, shuffled):
            labels[i] = label
    null.append(auc([dict(r, gap=label) for r, label in zip(data, labels)]))
null.sort()
low = sum(x <= observed for x in null)
high = sum(x >= observed for x in null)
print(json.dumps({"training_routes": len(train), "road_routes": len(roads),
                  "ties": sum(r["gap"] == 0 for r in data),
                  "trailing": sum(r["gap"] > 0 for r in data),
                  "metric": "AUC of training nonundo transition score, tie over trailing",
                  "observed_auc": observed,
                  "null_mean": sum(null)/len(null),
                  "null_95_interval": [null[24], null[974]],
                  "p_two_sided": min(1.0, 2*min(low+1, high+1)/1001),
                  "selected": [r for r in data if r["id"] in
                               ("ac-00766", "ac-00974")]}, indent=2))
