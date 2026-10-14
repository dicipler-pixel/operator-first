"""Change-of-variables transfer onto Stable-gap rows (Stable record >= AC + 3): for each such row B and every row A sharing its
Whitehead key with a verified road, transfer A's road to B (cov_transfer.transfer) and test AC road + [16,15] against the Stable record.
Inputs: the ranked Stable-gap list (scratch stable_gap_ranked.json, copy in research/acc/live/sweeps/rival3/stable_gap_ranked_20261014.json)."""
import sys, json, gzip, collections
sys.argv = ["x"]; sys.path.insert(0, "tools/acc/upgh")
import cov_transfer as CT
SR = CT.SR; core = CT.core
from verifier import stable_core
S = "/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad"
wh = json.load(gzip.open("research/acc/live/sweeps/cov/whitehead_min_20261014.json.gz"))
gap = {"ac-" + x[1]: x for x in json.load(open("research/acc/live/sweeps/rival3/stable_gap_ranked_20261014.json"))}  # (slack,row,A,k,S,sk,need,ours)
best = {}
for cid, m in SR.load_roads():
    if cid in wh and (cid not in best or len(m) < len(best[cid])):
        if core.verify(SR.CH[cid], m, "ac-r2-v1", SR.LIM)["ok"]: best[cid] = m
g = collections.defaultdict(list)
for cid, v in wh.items(): g[v["key"]].append(cid)
pairs = []
for B in gap:
    for A in g[wh[B]["key"]]:
        if A != B and A in best: pairs.append((len(best[A]), A, B))
print("stable-gap rows", len(gap), "rows with a mate holding a road", len(set(p[2] for p in pairs)), "pairs", len(pairs), flush=True)
hits = []
for la, A, B in sorted(pairs):
    try: r = CT.transfer(A, best[A], B)
    except Exception as e: print("ERR", A, B, e); continue
    if r[0] is None: print("skip", A, B, r[1]); continue
    full, status, info = r; need = gap[B][6]; Srec = gap[B][4]
    tag = ""
    if status == "ok" and len(full) <= need:
        sl = full + [16, 15]
        ok = stable_core.verify(SR.CH["s" + B], sl, "sac-r8-v1", SR.LIM).get("ok")
        tag = "STABLE BEAT %d < %d (ok=%s)" % (len(sl), Srec, ok)
        if ok: hits.append((B, sl, A))
    print(A, la, "->", B, len(full), "AC rec", gap[B][2], "Stable rec", Srec, "need <=", need, status, info[3], tag, flush=True)
with open(S + "/sg_cov_hits.txt", "w") as f:
    for B, sl, A in hits: f.write("# s%s Stable %d (AC road from %s via change of variables + [16,15])\ns%s: [%s]\n" % (B, len(sl), A, B, ", ".join(map(str, sl))))
print("hits", len(hits))
