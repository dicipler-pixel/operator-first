#!/usr/bin/env python3
"""Leader patterns: attribute board changes to the top teams from saved snapshots, then profile them (0 API calls).

The boards give each row's record and k (teams holding it), not who holds it. The leaderboards give each team's
currentBestCount and score. Between two consecutive time points that have both a board and a leaderboard, if exactly
one team other than ours gained records, every record event on the boards in that window is theirs: a new record
(beat or first solve: the record drops or appears, k resets to 1) or a tie (same record, k grows). Our own events in the
window come from submit_log.jsonl and are removed first. Mixed windows are counted as unattributed.

Profile per team: events by kind and track, record lengths, cut sizes (old - new), k at tie time, share of
Miller-Schupp rows (and n), repeat rows (the team shortening its own record again), and the hour-of-day cadence.
Writes research/acc/live/LEADER_PATTERNS.md and research/acc/upgh/cache/leader_events.json.

usage: python3 tools/acc/upgh/leader_patterns.py [--teams 2]"""
import argparse
import collections
import csv
import glob
import gzip
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
B = REPO / "research/acc/live/boards"
SAIR = Path.home() / ".cache/upgh/sair/competition/tools/verifier/data"


def items(f):
    d = json.load(gzip.open(f))
    d = d.get("data", d)
    return next(v for v in d.values() if isinstance(v, list))


def stamp(f):
    return re.search(r"(2026\d{4}T\d{4}Z)", f.name).group(1)


def board(f):
    return {r["challengeId"]: (r.get("currentBestLength"), r.get("kTeams") or 0) for r in items(f)}


def lboard(f):
    out = {}
    for r in items(f):
        t = r["team"]
        out[t["teamName"]] = (r.get("currentBestCount") or 0, float(r.get("score") or 0), r.get("rank"))
    return out


def ms_rows():
    """challenge id -> (n, w) for rows that are exactly Miller-Schupp MS(n,w) up to rotation/inversion of each relator."""
    man = json.load(open(SAIR / "manifest.json"))
    rel = {c["challenge_id"][c["challenge_id"].index("-") + 1:]: c["initial_relators"] for c in man["challenges"]}

    def forms(w):
        s = set()
        for v in (tuple(w), tuple(-t for t in reversed(w))):
            s |= {v[i:] + v[:i] for i in range(len(v))}
        return frozenset(s)
    idx = {}
    for num, (a, b) in rel.items():
        idx.setdefault(frozenset([forms(a), forms(b)]), []).append(num)
    out = {}
    for m in csv.DictReader(open(SAIR / "ms1190_metadata.csv")):
        n = int(m["n"])
        wv = [int(t) for t in m["w_vector"].split()] if m["w_vector"].strip() else []
        key = frozenset([forms([-1] + [2] * n + [1] + [-2] * (n + 1)), forms([-1] + wv)])
        for num in idx.get(key, []):
            out[num] = (n, m["w"])
    return out


def our_events():
    """Rows we sent, by send time (submit_log.jsonl 'post' events with accepted lines are not itemised per row, so use
    ACC_SUBMIT_API_* files named by time)."""
    ev = []
    for f in sorted(REPO.glob("ACC_SUBMIT_API_*.txt")) + sorted(REPO.glob("ACC_QUEUE_*.txt")):
        t = re.search(r"(2026\d{4}T\d{4})", f.name)
        if not t:
            continue
        for line in f.read_text().splitlines():
            m = re.match(r"\s*((?:ac|sac)-\d{5}):", line)
            if m:
                ev.append((t.group(1) + "Z", m.group(1)))
    return ev


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--teams", type=int, default=2)
    a = ap.parse_args()
    us = "Mad Hatters"
    ms = ms_rows()
    ours = our_events()
    events, windows = [], collections.Counter()
    leaders = None
    for track, bpat, lpat in (("ac", "ac_2026*.json.gz", "leaderboard_ac_2026*.json.gz"),
                              ("sac", "stable_ac_2026*.json.gz", "leaderboard_stable_ac_2026*.json.gz")):
        bf = {stamp(f): f for f in map(Path, glob.glob(str(B / bpat)))}
        lf = {stamp(f): f for f in map(Path, glob.glob(str(B / lpat)))}
        times = sorted(set(bf) & set(lf))
        last_lb = lboard(lf[times[-1]])
        if leaders is None:
            leaders = [n for n, _ in sorted(last_lb.items(), key=lambda kv: kv[1][2] or 999)[:a.teams]]
        prev_b, prev_l = board(bf[times[0]]), lboard(lf[times[0]])
        for t0, t1 in zip(times, times[1:]):
            cur_b, cur_l = board(bf[t1]), lboard(lf[t1])
            gain = {n: cur_l[n][0] - prev_l.get(n, (0, 0, 0))[0] for n in cur_l}
            gainers = [n for n, g in gain.items() if g > 0 and n != us]
            mine = {r for (ts, r) in ours if t0 < ts <= t1}
            ch = []
            for cid, (L, k) in cur_b.items():
                pL, pk = prev_b.get(cid, (None, 0))
                if cid in mine:
                    continue
                if L is not None and (pL is None or L < pL):
                    ch.append({"row": cid, "kind": "first" if pL is None else "beat", "old": pL, "new": L, "k_before": pk})
                elif L is not None and L == pL and k > pk:
                    ch.append({"row": cid, "kind": "tie", "old": pL, "new": L, "k_before": pk})
            if ch:
                # the team that made >= 75% of the positive count gains in the window (a batch dominates its window)
                tot = sum(max(gain[n], 0) for n in gainers)
                top = max(gainers, key=lambda n: gain[n]) if gainers else None
                who = top if top and gain[top] >= 0.75 * tot else None
                windows["attributed" if who else "mixed"] += 1
                for c in ch:
                    c.update({"track": track, "t": t1, "team": who, "window_gainers": len(gainers)})
                    num = c["row"].split("-")[1]
                    if num in ms:
                        c["ms"] = ms[num]
                    events.append(c)
            prev_b, prev_l = cur_b, cur_l
    json.dump({"leaders": leaders, "events": events}, open(REPO / "research/acc/upgh/cache/leader_events.json", "w"))

    out = ["# Leader patterns (from saved snapshots, 0 API calls)", "",
           "Built by `tools/acc/upgh/leader_patterns.py`. Record events on the boards are attributed to a team when it made at least 75%% of the "
           "record-count gains (besides ours) in that window. Windows: %s." % dict(windows), ""]
    for team in leaders:
        ev = [e for e in events if e["team"] == team]
        kinds = collections.Counter((e["track"], e["kind"]) for e in ev)
        cuts = [e["old"] - e["new"] for e in ev if e["kind"] == "beat"]
        own = collections.Counter(e["row"] for e in ev if e["kind"] == "beat")
        msn = collections.Counter(e["ms"][0] for e in ev if "ms" in e)
        lens = sorted(e["new"] for e in ev)
        hours = collections.Counter(e["t"][9:11] for e in ev)
        tie_k = collections.Counter(min(e["k_before"], 9) for e in ev if e["kind"] == "tie")
        q = lambda xs, p: xs[int(p * (len(xs) - 1))] if xs else None
        out += ["## %s" % team, "",
                "- attributed events: %d; by track/kind: %s" % (len(ev), dict(kinds)),
                "- record length of their lines: min %s, median %s, 90%% %s, max %s" % (q(lens, 0), q(lens, .5), q(lens, .9), q(lens, 1)),
                "- beat size (old - new): %s" % dict(sorted(collections.Counter(min(c, 20) for c in cuts).items())),
                "- rows beaten more than once in the window set (shortening again): %d" % sum(1 for v in own.values() if v > 1),
                "- ties by k before the tie: %s" % dict(sorted(tie_k.items())),
                "- Miller-Schupp rows among their events: %d (by n: %s)" % (sum(msn.values()), dict(sorted(msn.items()))),
                "- events by UTC hour: %s" % dict(sorted(hours.items())), ""]
        big = sorted((e for e in ev if e["kind"] in ("beat", "first")), key=lambda e: -((e["old"] or 0) - e["new"]))[:15]
        if big:
            out += ["Largest cuts / first solves:", "", "| row | kind | old | new | when | MS |", "|---|---|---|---|---|---|"]
            out += ["| %s | %s | %s | %s | %s | %s |" % (e["row"], e["kind"], e["old"], e["new"], e["t"], e.get("ms", "")) for e in big]
            out.append("")
    (REPO / "research/acc/live/LEADER_PATTERNS.md").write_text("\n".join(out) + "\n")
    print("\n".join(out[:60]))


if __name__ == "__main__":
    main()
