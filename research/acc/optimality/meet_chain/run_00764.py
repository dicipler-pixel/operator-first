#!/usr/bin/env python3
"""Lane A1 for J5 (Grok's lead): exact meet between balls around 00764/02598 starting points and the whole ac-00766 road."""
import json, os, subprocess, sys
SAIR = os.path.expanduser("~/.cache/upgh/sair"); sys.path.insert(0, SAIR + "/competition/tools")
from verifier import core
man = json.load(open(SAIR + "/competition/tools/verifier/data/manifest.json"))
CH = {c["challenge_id"]: c for c in man["challenges"]}
E = {1: 0, -1: 1, 2: 2, -2: 3}; L = "xXyY"
st = lambda cid: tuple(tuple(r) for r in CH[cid]["initial_relators"])
word = lambda r: "".join(L[E[t]] for t in r)
enc = lambda s: [str(len(s[0])), *[str(E[t]) for t in s[0]], str(len(s[1])), *[str(E[t]) for t in s[1]]]
R766 = [1,6,5,9,11,5,8,8,3,9,7,11,5,8,4,6,9,13,10,3,12,11,13,10,4,1,8,2,4,2,2,2,2,2]
chain = [st("ac-00766")]
for m in R766: chain.append(core.apply_move(chain[-1], m))
print("00766 road ends at", [word(r) for r in chain[-1]])
swap = lambda s: (s[1], s[0])
sources, labels = [], []
for cid in ("ac-00764", "ac-02598"):
    s0 = st(cid); print(cid, "start", [word(r) for r in s0])
    for frame, s in (("plain", s0), ("swap", swap(s0))):
        cur, pre = s, []
        for k in range(0, 9):
            sources.append(cur); labels.append((cid, frame, list(pre)))
            if k < 8:
                cur = core.apply_move(cur, R766[k]); pre.append(R766[k])
        if cid == "ac-00764" and frame == "swap":
            print("S8 =", [word(r) for r in cur], "total", sum(map(len, cur)))
args = ["./meet_chain", "/tmp/acc_meet", sys.argv[1] if len(sys.argv) > 1 else "7", sys.argv[2] if len(sys.argv) > 2 else "6", str(len(chain))]
for s in chain: args += enc(s)
args.append(str(len(sources)))
for s in sources: args += enc(s)
os.makedirs("/tmp/acc_meet", exist_ok=True)
p = subprocess.run(args, capture_output=True, text=True)
print(p.stdout); print(p.stderr[-600:])
out = p.stdout.split("\n"); hits = []
for i, line in enumerate(out):
    if line.startswith("MEET"):
        s, dS, dT, j = map(int, line.split()[1:]); path = list(map(int, out[i + 1].split()[1:]))
        cid, frame, pre = labels[s]
        road = pre + path + R766[j:]
        hits.append((cid, frame, road))
json.dump([{"cid": c, "frame": f, "road": r} for c, f, r in hits], open("hits_00764.json", "w"))
print("hits:", [(c, f, len(r)) for c, f, r in hits])
