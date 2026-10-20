import os, re, json, gzip, glob, sys, collections, csv, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core, stable_core
O = "/home/user/operator-first/ACC_ROUNDUP_20261020/"; S = "/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/"
pat = re.compile(r"\b(s?ac-\d{5})\"?\s*:\s*\[([0-9,\s]+)\]")
roads = collections.defaultdict(set); src = {}
roots = ["/home/user/operator-first/research/acc", "/home/user/operator-first/tools/acc", "/home/user/ext_upload", S]
t0 = time.time(); nfiles = 0
for root in roots:
    for dp, dn, fn in os.walk(root):
        if "/.git" in dp: continue
        for f in fn:
            p = os.path.join(dp, f)
            if not re.search(r"\.(txt|json|jsonl|md|csv|out|log|tsv)(\.gz)?$", f): continue
            try:
                if os.path.getsize(p) > 80_000_000: continue
                t = (gzip.open(p, "rt", errors="replace") if p.endswith(".gz") else open(p, errors="replace")).read()
            except Exception: continue
            nfiles += 1
            for c, mv in pat.findall(t):
                m = tuple(int(x) for x in mv.split(",") if x.strip())
                if m and (c, m) not in src: roads[c].add(m); src[(c, m)] = os.path.relpath(p, "/home/user")
# ledger moves (structured)
for l in open("/home/user/operator-first/research/acc/upgh/ledger.jsonl"):
    try: d = json.loads(l).get("data") or {}
    except ValueError: continue
    c, m = d.get("cid"), d.get("moves")
    if isinstance(c, str) and isinstance(m, list) and m:
        c = ("sac-" if c.startswith("s") else "ac-") + c[-5:]; m = tuple(m)
        if (c, m) not in src: roads[c].add(m); src[(c, m)] = "operator-first/research/acc/upgh/ledger.jsonl"
print("scanned files", nfiles, "candidate roads", sum(len(v) for v in roads.values()), "rows", len(roads), "%.0fs" % (time.time() - t0), flush=True)
ok = collections.defaultdict(list); bad = 0
for c, ms in roads.items():
    if c not in SR.CH or c[-5:] in SR.FORBID: continue
    for m in ms:
        try: v = stable_core.verify(SR.CH[c], list(m), "sac-r8-v1", SR.LIM).get("ok") if c.startswith("s") else core.verify(SR.CH[c], list(m), "ac-r2-v1", SR.LIM)["ok"]
        except Exception: v = False
        if v: ok[c].append(m)
        else: bad += 1
# AC road + [16,15] is a Stable road
for c in [k for k in ok if k.startswith("ac-")]:
    s = "s" + c; best = min(ok[c], key=len) + (16, 15)
    if best not in ok.get(s, []) and stable_core.verify(SR.CH[s], list(best), "sac-r8-v1", SR.LIM).get("ok"):
        ok[s].append(best); src[(s, best)] = "derived: best AC road + [16, 15]"
nall = sum(len(v) for v in ok.values())
print("verified roads", nall, "rejected", bad, "| AC rows", sum(1 for k in ok if k.startswith("ac-")), "Stable rows", sum(1 for k in ok if k.startswith("sac-")), "%.0fs" % (time.time() - t0), flush=True)
with open(O + "moves/BEST_ROADS_AC.txt", "w") as fa, open(O + "moves/BEST_ROADS_STABLE.txt", "w") as fs:
    for f, tag in ((fa, "AC (ac-r2-v1)"), (fs, "Stable (sac-r8-v1)")):
        f.write("# Mad Hatters best verified road per row, %s. Every line replays ok on the official SAIR core. Built %s.\n" % (tag, time.strftime("%Y-%m-%d %H:%MZ", time.gmtime())))
    for c in sorted(ok):
        b = min(ok[c], key=len); (fs if c.startswith("s") else fa).write("%s: [%s]\n" % (c, ", ".join(map(str, b))))
with gzip.open(O + "moves/ALL_VERIFIED_ROADS.txt.gz", "wt") as fh:
    fh.write("# every distinct verified road we hold (official core ok), shortest first per row; '# source' = first file it was found in\n")
    for c in sorted(ok):
        for m in sorted(ok[c], key=len):
            fh.write("# %d moves, source %s\n%s: [%s]\n" % (len(m), src.get((c, m), "?"), c, ", ".join(map(str, m))))
json.dump({c: sorted(len(m) for m in v) for c, v in ok.items()}, open(S + "roundup_lengths.json", "w"))
# submissions history with moves
lib = {(c, len(m)): m for c, v in ok.items() for m in sorted(v, key=len, reverse=True)}
rows = list(csv.reader(open(S + "MH_ALL_SUBMISSIONS_20261020.csv")))
out = [rows[0][:6] + ["moves", "moves_source"]]; ex = lb = 0
for r in rows[1:]:
    if r[6]: out.append(r[:6] + [r[6], "stored copy of the sent file"]); ex += 1
    elif (r[2], int(r[4])) in lib: out.append(r[:6] + ["[" + ", ".join(map(str, lib[(r[2], int(r[4]))])) + "]", "verified library road of the same length (may differ from the exact sent moves)"]); lb += 1
    else: out.append(r[:6] + ["", "not held locally (download the submission to recover)"])
csv.writer(open(O + "moves/SUBMISSION_HISTORY_WITH_MOVES.csv", "w", newline="")).writerows(out)
print("history lines", len(out) - 1, "exact sent moves", ex, "same-length library road", lb, "missing", len(out) - 1 - ex - lb)
