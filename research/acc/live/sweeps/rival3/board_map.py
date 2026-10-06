import json, gzip, glob, sys, time
import numpy as np
R = "/home/user/operator-first/"
man = json.load(open("/root/.cache/upgh/sair/competition/tools/verifier/data/manifest.json"))
CH = {c["challenge_id"]: c for c in man["challenges"] if c["challenge_id"].startswith("ac-")}
st = sorted(glob.glob(R + "research/acc/live/boards/ac_*.json.gz"))[-1]
B = {x["challengeId"]: (x.get("currentBestLength"), x.get("kTeams")) for x in json.load(gzip.open(st))["data"]["items"]}
mine = {}
for fn in glob.glob(R + "research/acc/live/mine_2*.json") + [R + "research/acc/live/mine_recent.json"]:
    try: items = json.load(open(fn)).get("items", [])
    except Exception: continue
    for it in items:
        for r in it.get("results") or []:
            if r.get("ok"): mine[r["challenge_id"]] = min(mine.get(r["challenge_id"], 1 << 30), r["length"])
for l in open(R + "research/acc/live/submit_log.jsonl"):
    try: x = json.loads(l)
    except ValueError: continue
    for r in x.get("results") or []:
        if r.get("ok") and r.get("length"): mine[r["challenge_id"]] = min(mine.get(r["challenge_id"], 1 << 30), r["length"])
held = {}
for l in open(R + "research/acc/upgh/ledger.jsonl"):
    try: x = json.loads(l)
    except ValueError: continue
    d = x.get("data") or {}
    if d.get("cid", "").startswith("ac-") and d.get("moves"): held[d["cid"]] = min(held.get(d["cid"], 1 << 30), len(d["moves"]))
rival = {l.split()[0] for l in open(R + "research/acc/live/inbox/rivals/RIVAL3_scores_20261006T1905Z.tsv") if l.startswith("ac-")}

def runs(w): return sum(1 for i in range(len(w)) if i == 0 or w[i] != w[i - 1])
def lcs_cyc(a, b):
    # longest common substring of cyclic a (and a^-1) with cyclic b
    best = 0
    for aa in (a, [-t for t in reversed(a)]):
        A = aa + aa; Bb = b + b
        for i in range(len(aa)):
            for j in range(len(b)):
                k = 0
                while k < min(len(aa), len(b)) and A[i + k] == Bb[j + k]: k += 1
                best = max(best, k)
    return best
X, lab, ids = [], [], []
for cid, c in CH.items():
    if cid not in B or B[cid][0] is None: continue
    r = sorted((list(w) for w in c["initial_relators"]), key=len)
    f = []
    for w in r:
        f += [len(w), sum(abs(t) == 1 for t in w), sum(abs(t) == 2 for t in w), abs(sum(1 if t == 1 else -1 if t == -1 else 0 for t in w)),
              abs(sum(1 if t == 2 else -1 if t == -2 else 0 for t in w)), runs(w), max(len(list(g)) for g in [w[i:j] for i in range(len(w)) for j in [i+1]] ) ]
    f += [len(r[0]) + len(r[1]), lcs_cyc(r[0], r[1]), len(r[1]) / max(1, len(r[0]))]
    X.append(f); ids.append(cid)
    rec = B[cid][0]
    lab.append(0 if mine.get(cid, 1 << 30) <= rec else 1 if min(mine.get(cid, 1 << 30), held.get(cid, 1 << 30)) < (1 << 30) else 2)
X = np.array(X, float); X = (X - X.mean(0)) / (X.std(0) + 1e-9); lab = np.array(lab)
print("rows", len(ids), "hold", (lab == 0).sum(), "over", (lab == 1).sum(), "none", (lab == 2).sum(), flush=True)
from sklearn.manifold import TSNE
import umap
t = time.time(); ts = TSNE(n_components=2, perplexity=40, init="pca", random_state=1); Yt = ts.fit_transform(X); kl = ts.kl_divergence_
print("tsne %.0fs KL=%.3f" % (time.time() - t, kl), flush=True)
t = time.time(); Yu = umap.UMAP(n_neighbors=30, min_dist=0.2, random_state=1).fit_transform(X); print("umap %.0fs" % (time.time() - t), flush=True)
# how mixed are the labels locally? fraction of 15 nearest neighbours (in feature space) with the same label
from sklearn.neighbors import NearestNeighbors
nn = NearestNeighbors(n_neighbors=16).fit(X); _, I = nn.kneighbors(X)
same = (lab[I[:, 1:]] == lab[:, None]).mean(1)
for k, name in enumerate(["hold record", "road over record", "nothing"]):
    base = (lab == k).mean(); print("%-18s n=%5d  neighbours same label %.2f (chance %.2f)" % (name, (lab == k).sum(), same[lab == k].mean(), base))
np.savez(sys.argv[1] + "/map.npz", Yt=Yt, Yu=Yu, lab=lab, ids=np.array(ids), kl=kl)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
col = {0: "#2a78d6", 1: "#eb6834", 2: "#c9c8c0"}; name = {0: "we hold the record", 1: "we have a road, over record", 2: "no road from us"}
fig, ax = plt.subplots(1, 2, figsize=(14, 6.6), dpi=130)
riv = np.array([i in rival for i in ids])
for a_, Y, title in ((ax[0], Yt, "t-SNE  (final KL divergence = %.2f)" % kl), (ax[1], Yu, "UMAP")):
    for k in (2, 1, 0):
        m = lab == k; a_.scatter(Y[m, 0], Y[m, 1], s=4, c=col[k], label="%s (%d)" % (name[k], m.sum()), linewidths=0)
    a_.scatter(Y[riv, 0], Y[riv, 1], s=60, facecolors="none", edgecolors="#111111", linewidths=1.2, label="rival #3 rows (25)")
    a_.set_title(title, fontsize=12, color="#222"); a_.set_xticks([]); a_.set_yticks([])
    for s_ in a_.spines.values(): s_.set_color("#ddd")
ax[0].legend(loc="lower left", fontsize=8, frameon=False, markerscale=2)
fig.suptitle("ACC board map: 7,443 AC rows by 17 start-relator features (lengths, letter counts, exponent sums, runs, shared cyclic piece)", fontsize=11, color="#333")
fig.tight_layout(); fig.savefig(sys.argv[1] + "/board_map.png"); print("saved", flush=True)
