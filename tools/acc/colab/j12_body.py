# ---- J12 body (sources and targets are embedded above by make_j12.py) ----
import argparse, base64, datetime, json, os, re, shutil, subprocess, sys, time
ap = argparse.ArgumentParser(description="J12 rival-rows search (beam lane + capped lane), official verifier, Drive reports")
ap.add_argument("--lane", default="both", choices=["beam", "capped", "both"])
ap.add_argument("--hours", type=float, default=11.0)
ap.add_argument("--root", default="/content/j12")
ap.add_argument("--outdir", default=None, help="report folder, e.g. /content/drive/MyDrive/<hub folder>; default ROOT/out")
ap.add_argument("--report-min", type=float, default=35.0)
ap.add_argument("--widths", default="20000,100000,200000", help="High-RAM runtime: 20000,100000,400000")
ap.add_argument("--seeds", default="0,1,2,3")
ap.add_argument("--caps", default="3,5,7,9", help="capped lane: caps = start total + each value")
ap.add_argument("--budget", default="100000000", help="capped lane: states per cap (100M ~ 4-5 GB RAM; High-RAM: 250000000)")
ap.add_argument("--only", default=None, help="comma list of ac-ids to restrict to")
ap.add_argument("--targets-file", default=None, help="JSON list [[ac-id, record, k, sac_record, sac_k, tag], ...] replacing the built-in targets")
ap.add_argument("--setup-only", action="store_true", help="clone, compile, build T8, then exit (run this once first)")
a = ap.parse_args()
T0 = time.time(); DEADLINE = T0 + a.hours * 3600
R = os.path.abspath(a.root); os.makedirs(R + "/work", exist_ok=True); os.chdir(R)
OUT = os.path.abspath(a.outdir or R + "/out"); os.makedirs(OUT, exist_ok=True)


def sh(c):
    print("+", c, flush=True); subprocess.run(c, shell=True, check=True)


if not os.path.isdir("sair/competition"):
    shutil.rmtree("sair", ignore_errors=True)
    sh("git clone -q https://github.com/SAIRcompetition/Andrews-Curtis sair && cd sair && git checkout -q " + PIN)
assert subprocess.run("cd sair && git rev-parse HEAD", shell=True, capture_output=True, text=True).stdout.strip() == PIN, "wrong SAIR commit"
for n, b in SRC.items():
    open(n, "wb").write(base64.b64decode(b))
for exe in ("acc_opt", "acc_beam", "acc_window", "acc_capped"):
    if not os.path.exists(exe):
        sh("gcc -O3 -march=native -o %s %s.c -lm" % (exe, exe))
if not os.path.exists("T8.tab"):
    sh("./acc_opt tball 8 32000000 T8.tab work")
if a.setup_only:
    print("SETUP DONE: sair pinned, engines compiled, T8.tab ready", flush=True); sys.exit(0)
sys.path.insert(0, R + "/sair/competition/tools")
from verifier import core, stable_core  # official pinned verifier
MAN = json.load(open(R + "/sair/competition/tools/verifier/data/manifest.json"))
CH = {c["challenge_id"]: c for c in MAN["challenges"]}; LIM = MAN["limits"]


def ok_line(cid, moves):
    c = CH.get(cid)
    if not c:
        return False
    v = (stable_core if cid.startswith("sac-") else core).verify(c, moves, c["move_spec_version"], LIM)
    return bool(v.get("ok"))


L = {1: "x", -1: "X", 2: "y", -2: "Y"}; SW = str.maketrans("xXyY", "yYxX"); E = {"x": "0", "X": "1", "y": "2", "Y": "3"}
MODES = {"direct": (lambda r0, r1: (r0, r1), {i: i for i in range(14)}),
         "twin": (lambda r0, r1: (r1.translate(SW), r0.translate(SW)), {0: 1, 1: 0, 2: 4, 3: 5, 4: 2, 5: 3, 6: 12, 7: 13, 8: 10, 9: 11, 10: 8, 11: 9, 12: 6, 13: 7}),
         "yx": (lambda r0, r1: (r0.translate(SW), r1.translate(SW)), {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 9, 8: 6, 9: 7, 10: 12, 11: 13, 12: 10, 13: 11})}
enc = lambda a_, b_: [str(len(a_)), *[E[c] for c in a_], str(len(b_)), *[E[c] for c in b_]]
BEAMENV = dict(os.environ, BEAM_H="1", BEAM_DIV="0.8", BEAM_P2="2", BEAM_QUOTA="16", BEAM_ELITE="5000", BEAM_DUAL="0.75")
STATE = OUT + "/j12_state_%s.json" % a.lane
WK = R + "/work_" + a.lane; os.makedirs(WK, exist_ok=True)
S = json.load(open(STATE)) if os.path.exists(STATE) else {"done": [], "best": {}, "log": []}
done = set(S["done"])


def save():
    S["done"] = sorted(done); json.dump(S, open(STATE + ".tmp", "w")); os.replace(STATE + ".tmp", STATE)


def offer(cid, moves, how):
    """keep the shortest verified line per id"""
    if not moves or not ok_line(cid, moves):
        return
    b = S["best"].get(cid)
    if b is None or len(moves) < len(b["moves"]):
        S["best"][cid] = {"moves": moves, "how": how, "t": datetime.datetime.utcnow().strftime("%H:%MZ")}
        rec = RECS.get(cid)
        tag = "BEAT" if rec and len(moves) < rec[0] else "TIE" if rec and len(moves) == rec[0] else "over"
        msg = "%s %s %d (record %s k%s) %s via %s" % (datetime.datetime.utcnow().strftime("%H:%MZ"), cid, len(moves), rec and rec[0], rec and rec[1], tag, how)
        print("NEW", msg, flush=True); S["log"].append(msg)
        if tag != "over":
            report(urgent=True)
        save()


def window(t0, t1, path):
    p = subprocess.run(["./acc_window", WK, *enc(t0, t1), str(len(path)), *map(str, path)], capture_output=True, text=True)
    m = re.search(r"FINALPATH ?([\d ]*)", p.stdout)
    return list(map(int, m.group(1).split())) if m and m.group(1).strip() else path


def beam_job(cid, W, seed):
    r0, r1 = ["".join(L[i] for i in r) for r in CH[cid]["initial_relators"]]; sac = "sac-" + cid[3:]
    for mode, (tw, back) in MODES.items():
        if time.time() > DEADLINE:
            return
        t0, t1 = tw(r0, r1); env = dict(BEAMENV)
        if seed:
            env.update(BEAM_SEED=str(seed), BEAM_NOISE="2")
        p = subprocess.run(["./acc_beam", "T8.tab", str(W), "240", *enc(t0, t1)], capture_output=True, text=True, env=env)
        for kind in ("AC", "SAC"):
            m = re.search(r"^%s \d+ PATH ([\d ]+)" % kind, p.stdout, re.M)
            if not m:
                continue
            path = list(map(int, m.group(1).split()))
            if kind == "AC":
                path = window(t0, t1, path); op = [back[x] for x in path]
                if mode == "yx":
                    offer(sac, op + [15, 15], "beam-yx W%d s%d" % (W, seed))
                else:
                    offer(cid, op, "beam-%s W%d s%d" % (mode, W, seed)); offer(sac, op + [16, 15], "beam-%s+[16,15]" % mode)
            elif mode == "direct":
                offer(sac, path, "beam-direct-SAC W%d s%d" % (W, seed))


def capped_job(cid, dc):
    rel = CH[cid]["initial_relators"]; r0, r1 = ["".join(L[i] for i in r) for r in rel]
    start = len(rel[0]) + len(rel[1]); rec = RECS[cid][0]; cap = start + dc
    wd = WK + "/cap"; shutil.rmtree(wd, ignore_errors=True); os.makedirs(wd)
    env = dict(os.environ, MAXD=str(rec - 8), INIT_LOG2="26")
    p = subprocess.run(["./acc_capped", "T8.tab", str(cap), a.budget, wd, "j12", *enc(r0, r1)], capture_output=True, text=True, env=env)
    shutil.rmtree(wd, ignore_errors=True)
    head = re.search(r"cap=\d+ states=(\d+) depth=(\d+) (\w+)", p.stdout)
    S["log"].append("%s capped %s cap %d: %s" % (datetime.datetime.utcnow().strftime("%H:%MZ"), cid, cap, head.group(0) if head else p.stdout[-120:].strip()))
    for kind in ("AC", "SAC"):
        m = re.search(r"%s \d+ PATH ([\d ]+)" % kind, p.stdout)
        if m:
            path = list(map(int, m.group(1).split()))
            if kind == "AC":
                offer(cid, path, "capped cap %d" % cap); offer("sac-" + cid[3:], path + [16, 15], "capped+[16,15]")
            else:
                for cand in (path, path + [15, 15]):
                    offer("sac-" + cid[3:], cand, "capped-SAC cap %d" % cap)
    return head.group(3) if head else "?"


LAST = [0.0]


def report(urgent=False):
    if not urgent and time.time() - LAST[0] < a.report_min * 60:
        return
    LAST[0] = time.time(); now = datetime.datetime.utcnow().strftime("%Y%m%dT%H%MZ")
    lines, rows = [], []
    for cid in sorted(S["best"]):
        b = S["best"][cid]; rec = RECS.get(cid)
        tag = "BEAT" if rec and len(b["moves"]) < rec[0] else "TIE" if rec and len(b["moves"]) == rec[0] else "over"
        rows.append("%-10s %4d  record %s k%s  %s  (%s, %s)" % (cid, len(b["moves"]), rec and rec[0], rec and rec[1], tag, b["how"], b["t"]))
        if tag != "over":
            lines.append("%s: [%s]" % (cid, ",".join(map(str, b["moves"]))))
    txt = ["J12 report %s  (lane %s, %.1f h elapsed, %d jobs done)" % (now, a.lane, (time.time() - T0) / 3600, len(done)),
           "Every line below was replayed by the OFFICIAL pinned verifier (sair %s)." % PIN[:12], "",
           "== SCORING LINES (tie/beat vs the 18:27Z board; UPG-H re-checks the live board before sending) =="] + (lines or ["(none yet)"]) + \
          ["", "== best per row =="] + rows + ["", "== last 25 events =="] + S["log"][-25:]
    fn = OUT + "/J12_REPORT_%s_%s%s.txt" % (a.lane, now, "_HIT" if lines else "")
    open(fn, "w").write("\n".join(txt) + "\n"); print("report ->", fn, flush=True)


if a.targets_file:
    TARGETS = [t[:6] for t in json.load(open(a.targets_file))]
ids = [t[0] for t in TARGETS]
if a.only:
    ids = [i for i in ids if i in set(a.only.split(","))]
RECS = {t[0]: (t[1], t[2]) for t in TARGETS}; RECS.update({"sac-" + t[0][3:]: (t[3], t[4]) for t in TARGETS})
widths = [int(x) for x in a.widths.split(",")]; seeds = [int(x) for x in a.seeds.split(",")]; caps = [int(x) for x in a.caps.split(",")]
beam_plan = [("beam", cid, W, 0) for W in widths for cid in ids] + [("beam", cid, widths[-1], s) for s in seeds if s for cid in ids]
cap_plan = [("capped", cid, dc, 0) for dc in caps for cid in sorted(ids, key=lambda c: len(CH[c]["initial_relators"][0]) + len(CH[c]["initial_relators"][1]))]
plan = beam_plan if a.lane == "beam" else cap_plan if a.lane == "capped" else [x for pair in zip(beam_plan, cap_plan + [None] * len(beam_plan)) for x in pair if x]
print("J12: %d targets, %d jobs, lane %s, reports every %.0f min -> %s" % (len(ids), len(plan), a.lane, a.report_min, OUT), flush=True)
closed = set()
for job in plan:
    if time.time() > DEADLINE:
        break
    kind, cid, p1, p2 = job; key = "%s %s %s %s" % job
    if key in done:
        continue
    b = S["best"].get(cid)
    if b and len(b["moves"]) < RECS[cid][0]:
        continue                                             # already beaten: move on
    if kind == "capped" and cid in closed:
        continue
    t = time.time()
    if kind == "beam":
        beam_job(cid, p1, p2)
    else:
        if capped_job(cid, p1) == "CLOSED":
            closed.add(cid)                                  # whole capped space done: higher caps are a new search, keep going
    done.add(key); S["log"].append("%s done %s (%.0fs)" % (datetime.datetime.utcnow().strftime("%H:%MZ"), key, time.time() - t)); save()
    report()
report(urgent=True)
print("J12 finished or out of time; last report written.", flush=True)
