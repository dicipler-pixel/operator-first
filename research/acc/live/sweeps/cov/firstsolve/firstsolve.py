#!/usr/bin/env python3
"""First solves on UNSOLVED rows through the Whitehead-minimal frame (orows partner, 2026-10-14, owner-approved lane).
For each unsolved key (rows with the same Whitehead-minimal form up to letter maps / relator swap / rotation / inversion):
  M = descend(rep start) (cov_transfer.descend), beam the real dual-P2 engine on M in the direct, twin and (y,x) modes
  (rival3/rival_beam.py settings), take any AC road for M (replayed exactly from M on the official kernel), then transfer it to
  every row of the key with psi (cov_transfer.find_psi; prefix rel_bfs, body with conjugations by psi(g), finish_greedy).
  Each row road is replayed with core.verify ac-r2-v1 and stable_core.verify sac-r8-v1 (road + [16,15]) within SR.LIM.
usage: firstsolve.py plan                      -> plan.json (ranked keys)
       firstsolve.py run SHARD NSHARDS NKEYS W D"""
import csv, datetime, glob, gzip, json, os, re, subprocess, sys, time
R = "/home/user/operator-first/"
sys.path.insert(0, R + "tools/acc/upgh")
import symmetry_recog as SR
import cov_transfer as CT
import twin_lookup as TL
from whitehead_min import red, cyc, inv, apply, total, INV
from verifier import stable_core
core = SR.core
HERE = os.path.dirname(os.path.abspath(__file__))
BIN = "/root/.cache/acc_beam_bin"
FORBID = {"09839", "02257", "09311", "06403", "04718", "05378"}
AK3 = {"00137", "00399", "06194", "06279", "06945"}
SW = str.maketrans("xXyY", "yYxX"); E = {"x": "0", "X": "1", "y": "2", "Y": "3"}
MODES = {
    "direct": (lambda r0, r1: (r0, r1), {i: i for i in range(14)}),
    "twin": (lambda r0, r1: (r1.translate(SW), r0.translate(SW)), {0: 1, 1: 0, 2: 4, 3: 5, 4: 2, 5: 3, 6: 12, 7: 13, 8: 10, 9: 11, 10: 8, 11: 9, 12: 6, 13: 7}),
    "yx": (lambda r0, r1: (r0.translate(SW), r1.translate(SW)), {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 9, 8: 6, 9: 7, 10: 12, 11: 13, 12: 10, 13: 11}),
}
ENV = dict(os.environ, BEAM_H="1", BEAM_DIV="0.8", BEAM_P2="2", BEAM_QUOTA="16", BEAM_ELITE="5000", BEAM_DUAL="0.75")
def ms_open_starts():
    out = set()
    for r in csv.DictReader(open("/root/.cache/upgh/sair/competition/tools/verifier/data/ms1190_metadata.csv")):
        if r["status_at_freeze"] != "open": continue
        n = int(r["n"]); wv = [int(t) for t in r["w_vector"].split()]
        r0 = core.free_reduce(tuple([-1] + [2] * n + [1] + [-2] * (n + 1)))
        r1 = core.free_reduce(tuple([1] + [-t for t in reversed(wv)]))
        out.add(TL.key((r0, r1)))
    return out
def plan():
    wh = json.load(gzip.open(R + "research/acc/live/sweeps/cov/whitehead_min_20261014.json.gz"))
    ms = ms_open_starts()
    keys = {}
    for cid, v in wh.items():
        keys.setdefault(v["key"], []).append(cid)
    rows = []
    for k, cids in keys.items():
        if any(wh[c]["rec"] is not None for c in cids): continue          # only fully unsolved keys
        if any(c[-5:] in FORBID or c[-5:] in AK3 for c in cids): continue
        msopen = any(TL.key(tuple(tuple(r) for r in SR.CH[c]["initial_relators"])) in ms for c in cids)
        drop = max(wh[c]["L0"] - wh[c]["Lmin"] for c in cids); lmin = wh[cids[0]]["Lmin"]
        rows.append({"key": k, "rows": sorted(cids), "drop": drop, "Lmin": lmin, "ms_open": msopen})
    rows.sort(key=lambda r: (r["ms_open"], -r["drop"], r["Lmin"]))
    json.dump(rows, open(HERE + "/plan.json", "w"))
    print("unsolved keys", len(rows), "non-MS", sum(1 for r in rows if not r["ms_open"]), "first 10:", [(r["rows"][0], r["drop"], r["Lmin"], r["ms_open"]) for r in rows[:10]])
def beam(t0, t1, W, D):
    a = [str(len(t0)), *[E[c] for c in t0], str(len(t1)), *[E[c] for c in t1]]
    p = subprocess.run([BIN + "/acc_beam", BIN + "/T8.tab", str(W), str(D), *a], capture_output=True, text=True, env=ENV)
    m = re.search(r"^AC \d+ PATH ([\d ]+)", p.stdout, re.M)
    lens = [int(x) for x in re.findall(r"len\[(\d+)\.\.", p.stderr)]
    beam.closest = min(lens) if lens else None          # min total length of the kept beam, sampled every 10 depths
    return list(map(int, m.group(1).split())) if m else None
def replay_to_xy(M, road):
    s = tuple(CT.w(x) for x in M)
    for m in road: s = core.apply_move(s, m)
    return s == ((1,), (2,))
def transfer_pres(SA, roadA, cidB):
    """cov_transfer.transfer with donor = presentation SA (strings) and its road."""
    SB = tuple(SR.w2s(r) for r in SR.CH[cidB]["initial_relators"])
    got = CT.find_psi(SA, SB)
    if not got: return None, "no psi"
    psi, swap = got
    roadA2 = [SR.SW[m] for m in roadA] if swap else list(roadA)
    SAf = (SA[1], SA[0]) if swap else SA
    tgt = tuple(apply(psi, x) for x in SAf)
    pre = []
    for slot in (0, 1):
        p = CT.rel_bfs(SB[slot], tgt[slot], slot, cap=40)
        if p is None: return None, "prefix bfs failed"
        pre += p
    body = []
    for m in roadA2:
        if m in CT.MOVE_CONJ:
            slot, g = CT.MOVE_CONJ[m]; body += CT.conj_moves(slot, apply(psi, g))
        else: body.append(m)
    endA = ("y", "x") if swap else ("x", "y")
    endB = tuple(apply(psi, x) for x in endA)
    fin = CT.finish_greedy(endB, maxsteps=4000)
    if fin is None: return None, "finish failed (|psi x|=%d |psi y|=%d)" % (len(endB[0]), len(endB[1]))
    full = pre + body + fin
    ver = core.verify(SR.CH[cidB], full, "ac-r2-v1", SR.LIM)
    return full, ("ok" if ver["ok"] else "verify failed: %s" % ver.get("code", ver))
def run(sh, ns, nkeys, W, D):
    P = json.load(open(HERE + "/plan.json"))[:nkeys]
    donef = HERE + "/done_%d.txt" % sh; done = set(open(donef).read().split()) if os.path.exists(donef) else set()
    for i, k in enumerate(P):
        if i % ns != sh: continue
        rep = k["rows"][0]
        if rep in done: continue
        t0 = time.time()
        S0 = tuple(SR.w2s(r) for r in SR.CH[rep]["initial_relators"])
        M, chain = CT.descend(S0)
        road, how = None, None; close = []
        for mode, (tw, back) in MODES.items():
            a, b = tw(M[0], M[1]); tb = time.time()
            out = beam(a, b, W, D)
            got = None
            if out:
                rd = [back[m] for m in out]
                if replay_to_xy(M, rd):
                    got = len(rd)
                    if road is None or len(rd) < len(road): road, how = rd, mode
            close.append(beam.closest if beam.closest is not None else 999)
            print("  %s %s W%s D%s -> %s, closest total length %s (%.0fs)" % (rep, mode, W, D, got, beam.closest, time.time() - tb), flush=True)
        res = []
        if road:
            for cid in k["rows"]:
                full, status = transfer_pres(M, road, cid)
                sac_ok = False
                if full is not None and status == "ok":
                    sac_ok = bool(stable_core.verify(SR.CH["sac-" + cid[3:]], full + [16, 15], "sac-r8-v1", SR.LIM).get("ok"))
                    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                    with open(R + "research/acc/live/inbox/upgh_firstsolve_%s.txt" % stamp, "a") as f:
                        f.write("# FIRST SOLVE (row unsolved on the 20261014T0013Z board): %s AC %d moves; Whitehead-min beam (%s, W %s) on key rep %s + psi transfer; official core ok; Stable (+[16,15]) %s\n" % (cid, len(full), how, W, rep, "ok" if sac_ok else "FAILED"))
                        f.write("%s: [%s]\n" % (cid, ", ".join(map(str, full))))
                        if sac_ok: f.write("sac-%s: [%s]\n" % (cid[3:], ", ".join(map(str, full + [16, 15]))))
                    print("FIRST SOLVE", cid, len(full), flush=True)
                res.append("%s:%s%s" % (cid, (len(full) if full else "-"), "" if status == "ok" else "(" + status + ")"))
        line = "- %s key %s... Lmin %d drop %d rows %s MS-open %s | beam on M (W %s, D %s, direct/twin/yx): %s | transfer: %s | %ds\n" % (
            datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%MZ"), k["key"][:40], k["Lmin"], k["drop"], ",".join(c[3:] for c in k["rows"]),
            k["ms_open"], W, D, ("road %d (%s)" % (len(road), how)) if road else "no road (closest total length on M: %s, start %d)" % ("/".join(map(str, close)), total(M)), "; ".join(res) if res else "-", time.time() - t0)
        with open(R + "research/acc/live/sweeps/cov/FINDINGS_unsolved.md", "a") as f: f.write(line)
        print(line, end="", flush=True)
        with open(donef, "a") as f: f.write(rep + "\n")
if __name__ == "__main__":
    if sys.argv[1] == "plan": plan()
    else: run(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6])
