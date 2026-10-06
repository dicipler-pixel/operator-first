#!/usr/bin/env python3
"""Lane A2 for J5: exact meet from 00764/02598 starts (both slot orders) to Grok's collapse family
(Yx Y^(k-1) x Y^(k-1), x Y^k), k=4..12, every state of its finish [1,8,2,4]+[2]*(k-1), in all 16 frames."""
import json, os, subprocess, sys
SAIR = os.path.expanduser("~/.cache/upgh/sair"); sys.path.insert(0, SAIR + "/competition/tools")
from verifier import core
man = json.load(open(SAIR + "/competition/tools/verifier/data/manifest.json"))
CH = {c["challenge_id"]: c for c in man["challenges"]}
E = {1: 0, -1: 1, 2: 2, -2: 3}
enc = lambda s: [str(len(s[0])), *[str(E[t]) for t in s[0]], str(len(s[1])), *[str(E[t]) for t in s[1]]]
st = lambda cid: tuple(tuple(r) for r in CH[cid]["initial_relators"])
targets, bad = set(), 0
for k in range(4, 13):
    s = (tuple([-2, 1] + [-2] * (k - 1) + [1] + [-2] * (k - 1)), tuple([1] + [-2] * k))
    ch = [s]
    for m in [1, 8, 2, 4] + [2] * (k - 1): ch.append(core.apply_move(ch[-1], m))
    if ch[-1] != ((1,), (2,)): bad += 1
    maps = [{1: a * (1 if p == 0 else 2), 2: b * (2 if p == 0 else 1)} for p in (0, 1) for a in (1, -1) for b in (1, -1)]
    for c in ch:
        for mp in maps:
            img = tuple(tuple((mp[abs(t)] if t > 0 else -mp[abs(t)]) for t in r) for r in c)
            targets.add(img); targets.add((img[1], img[0]))
print("family finishes reaching (x,y):", 9 - bad, "of 9; target states:", len(targets))
srcs = [st("ac-00764"), st("ac-00764")[::-1], st("ac-02598"), st("ac-02598")[::-1]]
RA, RB = sys.argv[1], sys.argv[2]
args = ["./meet_chain", "/tmp/acc_meet", RA, RB, str(len(targets))]
for t in sorted(targets): args += enc(t)
args.append(str(len(srcs)))
for s in srcs: args += enc(s)
p = subprocess.run(args, capture_output=True, text=True)
print(p.stdout); print(p.stderr[-300:])
