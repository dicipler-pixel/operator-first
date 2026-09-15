"""Map MS-1190 rows to Discovery challenge_ids using the frozen MS encoding
published in competition/tools/verifier/data/README.md:

    r0 = x^-1 y^n x y^-(n+1)      r1 = x w^-1

Encoding: 1=x, -1=x^-1, 2=y, -2=y^-1.  Match against manifest.json's
initial_relators, first exactly, then up to relator order / cyclic
rotation / inversion (the pool's own uniqueness relation).
"""
import csv, json, collections

ROOT = "/home/user/saircompetition/andrews-curtis/competition/tools/verifier/data"

def inv(w):
    return [-c for c in reversed(w)]

def freered(w):
    out = []
    for c in w:
        if out and out[-1] == -c:
            out.pop()
        else:
            out.append(c)
    return out

def cyc_red(w):
    w = freered(w)
    while len(w) >= 2 and w[0] == -w[-1]:
        w = w[1:-1]
    return w

def canon_word(w):
    """Least rotation over the word and its inverse (cyclically reduced)."""
    w = cyc_red(w)
    if not w:
        return ()
    best = None
    for v in (w, inv(w)):
        n = len(v)
        for i in range(n):
            r = tuple(v[i:] + v[:i])
            if best is None or r < best:
                best = r
    return best

def canon_pres(r0, r1):
    a, b = canon_word(r0), canon_word(r1)
    return tuple(sorted((a, b)))

# --- build MS presentations -------------------------------------------------
rows = list(csv.DictReader(open(f"{ROOT}/ms1190_metadata.csv")))
ms = []
for r in rows:
    n = int(r["n"])
    w = [int(t) for t in r["w_vector"].split()]
    r0 = freered([-1] + [2]*n + [1] + [-2]*(n+1))
    r1 = freered([1] + inv(w))
    ms.append((r, r0, r1))

# --- index the manifest -----------------------------------------------------
man = json.load(open(f"{ROOT}/manifest.json"))
chal = man["challenges"] if isinstance(man, dict) and "challenges" in man else man
if isinstance(chal, dict):
    chal = list(chal.values())

exact, canon = {}, collections.defaultdict(list)
for c in chal:
    cid = c["challenge_id"]
    if not cid.startswith("ac-"):
        continue
    a, b = c["initial_relators"]
    exact[(tuple(a), tuple(b))] = cid
    canon[canon_pres(a, b)].append(cid)

print(f"manifest: {len(chal)} challenges, {len(exact)} ac- rows")

# --- match ------------------------------------------------------------------
hits_exact = hits_canon = miss = 0
out = []
by_status = collections.Counter()
for r, r0, r1 in ms:
    cid = exact.get((tuple(r0), tuple(r1)))
    how = "exact"
    if cid is None:
        cands = canon.get(canon_pres(r0, r1), [])
        if len(cands) == 1:
            cid, how = cands[0], "canon"
        elif cands:
            cid, how = cands[0], f"canon-ambiguous({len(cands)})"
    if cid is None:
        miss += 1
        how = None
    elif how == "exact":
        hits_exact += 1
    else:
        hits_canon += 1
    if cid:
        by_status[(r["status_at_freeze"], "matched")] += 1
        out.append({"challenge_id": cid, "seq": int(r["seq"]), "n": int(r["n"]),
                    "w": r["w"], "status_at_freeze": r["status_at_freeze"],
                    "reported_class": r["reported_class"],
                    "training_id": r["training_id"],
                    "prototype_path_length": r["prototype_path_length"],
                    "ms_total_length": len(r0) + len(r1), "match": how})
    else:
        by_status[(r["status_at_freeze"], "unmatched")] += 1

print(f"exact {hits_exact}  canon {hits_canon}  unmatched {miss}  (of {len(ms)})")
for k in sorted(by_status):
    print(f"  {k[0]:12s} {k[1]:9s} {by_status[k]}")

with open("/tmp/claude-0/ms/ms1190_to_challenge_v1.jsonl", "w") as f:
    for o in sorted(out, key=lambda z: z["challenge_id"]):
        f.write(json.dumps(o) + "\n")
print("written /tmp/claude-0/ms/ms1190_to_challenge_v1.jsonl")
