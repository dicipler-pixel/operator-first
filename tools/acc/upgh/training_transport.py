#!/usr/bin/env python3
"""Carry the 424 official training roads (competition/examples/training_424.json, public) onto every scored row whose
start matches any state of a training road up to the 16 frames, cyclic rotation and inversion of each relator.
Every carried road is replayed on the pinned official core. Outputs:
  research/acc/live/inbox/upgh_training_transport_<UTC>.txt   AC roads + Stable (AC + [16,15])
  research/acc/colab_kit/roads_training_shared.jsonl          rows where the carried road EQUALS a record shared by k >= 2
                                                               teams: shortening it by one move beats the record outright
usage: python3 tools/acc/upgh/training_transport.py
"""
import collections, datetime, glob, gzip, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import symmetry_recog as S  # noqa: E402
core = S.core

REPO = S.REPO
T = json.load(open(S.SAIR / "competition/examples/training_424.json"))["instances"]


def main():
    t0 = datetime.datetime.now(datetime.timezone.utc)
    REC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(str(REPO / "research/acc/live/boards/ac_*.json.gz")))[-1]))["data"]["items"]}
    SREC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(str(REPO / "research/acc/live/boards/stable_ac_*.json.gz")))[-1]))["data"]["items"]}

    def canon(st):
        A, B = S.ccs(st[0]), S.ccs(st[1])
        return min(min((p, q), (q, p)) for p, q in zip(A, B))

    need = collections.defaultdict(list)
    for cid in S.CH:
        if cid.startswith("ac-") and cid[-5:] not in S.FORBID:
            s0 = tuple(S.w2s(r) for r in S.CH[cid]["initial_relators"])
            need[canon(s0)].append((cid, s0))
    donors = collections.defaultdict(list)
    for t in T:
        st = tuple(tuple(r) for r in t["initial_relators"])
        chain = [st]
        for m in t["moves"]:
            chain.append(core.apply_move(chain[-1], m))
        assert chain[-1] == ((1,), (2,)), t["training_id"]
        for i, s in enumerate(chain[:-1]):
            ws = (S.w2s(s[0]), S.w2s(s[1]))
            k = canon(ws)
            if k in need:
                donors[k].append((t["training_id"], ws, t["moves"][i:], chain[-1]))
    print("training roads %d; scored start keys %d; matched keys %d" % (len(T), len(need), len(donors)), flush=True)
    goal = ((1,), (2,))
    fix, frontier = {goal: []}, [goal]
    for _ in range(8):
        nxt = []
        for s in frontier:
            for m in range(14):
                n = core.apply_move(s, m)
                if n not in fix and sum(map(len, n)) <= 4:
                    fix[n] = fix[s] + [m]
                    nxt.append(n)
        frontier = nxt
    INVM = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12}
    inv_fix = {s: [INVM[m] for m in reversed(p)] for s, p in fix.items()}
    found = {}
    for k, ds in donors.items():
        for cid, s in need[k]:
            for tid, dws, rest, dend in ds:
                for mp in S.MAPS:
                    for swap in (False, True):
                        t = S.frame_state(dws, mp, swap)
                        if S.cc(t[0]) != S.cc(s[0]) or S.cc(t[1]) != S.cc(s[1]):
                            continue
                        m0, m1 = S.slot_moves(s[0], t[0], 0), S.slot_moves(s[1], t[1], 1)
                        if m0 is None or m1 is None:
                            continue
                        end = tuple(S.s2w(x) for x in S.frame_state((S.w2s(dend[0]), S.w2s(dend[1])), mp, swap))
                        if end not in inv_fix:
                            continue
                        road = m0 + m1 + S.frame_moves(rest, mp, swap) + inv_fix[end]
                        if (cid not in found or len(road) < len(found[cid][0])) and core.verify(S.CH[cid], road, "ac-r2-v1", S.LIM).get("ok"):
                            found[cid] = (road, tid)
    stamp = t0.strftime("%Y%m%dT%H%M%SZ")
    out = REPO / ("research/acc/live/inbox/upgh_training_transport_%s.txt" % stamp)
    shared, lines, tally = [], [], collections.Counter()
    for cid, (road, tid) in sorted(found.items()):
        r = cid[-5:]
        rec, k = REC.get(r, (None, 0))
        srec, sk = SREC.get(r, (None, 0))
        L = len(road)
        tag = "first" if rec is None else ("beat" if L < rec else ("at_record" if L == rec else "over"))
        tally[tag] += 1
        lines.append("%s: [%s]\nsac-%s: [%s]\n" % (cid, ",".join(map(str, road)), r, ",".join(map(str, road + [16, 15]))))
        gain = (1 - 2.0 ** (1 - k) if rec == L and k >= 2 else 0) + (1 - 2.0 ** (1 - sk) if srec == L + 2 and sk >= 2 else 0)
        if gain > 0:
            shared.append({"id": cid, "record": rec, "k": k, "srecord": srec, "sk": sk, "moves": road, "gain": round(gain, 3), "training": tid})
    out.write_text("# training transport %s: %d rows (AC + Stable = AC + [16,15]); official core ok\n" % (stamp, len(found)) + "".join(lines))
    shared.sort(key=lambda x: (-x["gain"], -len(x["moves"])))
    with open(REPO / "research/acc/colab_kit/roads_training_shared.jsonl", "w") as f:
        for x in shared:
            f.write(json.dumps(x) + "\n")
    print("carried roads: %d rows %s" % (len(found), dict(tally)))
    print("rows where the carried road equals a shared record: %d (gain if each is beaten by one move: %.1f)" % (len(shared), sum(x["gain"] for x in shared)))
    for x in shared[:25]:
        print("  %s len %d | AC rec %s k%s | ST rec %s k%s | gain %.2f (%s)" % (x["id"], len(x["moves"]), x["record"], x["k"], x["srecord"], x["sk"], x["gain"], x["training"]))
    print("wrote %s" % out.relative_to(REPO))


if __name__ == "__main__":
    main()
