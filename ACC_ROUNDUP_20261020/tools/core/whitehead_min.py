"""usage: python3 tools/acc/upgh/whitehead_min.py OUT.json
Whitehead-minimal forms of every SAIR row start (rank 2), to find rows related by a change of variables (automorphism).
Words are strings over xXyY. Type-2 Whitehead automorphisms for multiplier a in {x,X,y,Y}: the other generator g maps to
g a, a^-1 g, or a^-1 g a. Greedy descent on the total cyclic length reaches the minimum (Whitehead peak reduction)."""
import sys, json, gzip, glob, collections
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
INV = {"x": "X", "X": "x", "y": "Y", "Y": "y"}
def red(w):
    st = []
    for c in w:
        if st and st[-1] == INV[c]: st.pop()
        else: st.append(c)
    return "".join(st)
def cyc(w):
    w = red(w)
    while len(w) > 1 and w[0] == INV[w[-1]]: w = w[1:-1]
    return w
def inv(w): return "".join(INV[c] for c in reversed(w))
def apply(phi, w):  # phi: dict letter->word for x,y
    m = {"x": phi["x"], "y": phi["y"], "X": inv(phi["x"]), "Y": inv(phi["y"])}
    return red("".join(m[c] for c in w))
AUTS = []
for a in "xXyY":
    g = "y" if a in "xX" else "x"; other = "x" if g == "y" else "y"
    for img in (g + a, INV[a] + g, INV[a] + g + a):
        AUTS.append(({g: img, other: other}, a, img))
def total(t): return sum(len(cyc(w)) for w in t)
def minimize(t):
    t = tuple(cyc(w) for w in t); steps = 0
    while True:
        best = None
        for phi, a, img in AUTS:
            u = tuple(cyc(apply(phi, w)) for w in t)
            if total(u) < total(t) and (best is None or total(u) < total(best)): best = u
        if best is None: return t, steps
        t = best; steps += 1
if __name__ == "__main__":
    R = "/home/user/operator-first/research/acc/live/"
    new = {it["challengeId"]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(R + "boards/ac_2026101[34]*.json.gz"))[-1]))["data"]["items"]}
    out = {}
    for cid, c in SR.CH.items():
        if not cid.startswith("ac-"): continue
        r0, r1 = (SR.w2s(r) for r in c["initial_relators"])
        t0 = (cyc(r0), cyc(r1)); m, steps = minimize(t0)
        ks = SR.ccs(m[0]); kt = SR.ccs(m[1])
        key = min(min((ks[i], kt[i]), (kt[i], ks[i])) for i in range(len(SR.MAPS)))
        out[cid] = {"L0": total(t0), "Lmin": total(m), "steps": steps, "key": "|".join(key), "rec": new[cid][0], "k": new[cid][1]}
    json.dump(out, open(sys.argv[1], "w"))
    c = collections.Counter((v["L0"] - v["Lmin"]) for v in out.values())
    print("length drop distribution:", sorted(c.items())[:20])
