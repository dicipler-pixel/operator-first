#!/usr/bin/env python3
"""Meat left on the bone: AC lines hidden inside Stable lines.

For every Stable path the team holds or has on file (harness best, team road files, ACC_*.txt, submission downloads) that ends
with [16, 15] (destabilize r1, destabilize r0) and whose prefix uses only ordinary moves (ids 0-13), the prefix is an AC path for
the same presentation. When that prefix reaches ((x),(y)) on the official AC core and is <= the live AC record, it is an AC
line (tie or beat) we may not have sent. Uses only cached boards (0 API reads); `send` re-checks live before posting.

usage: python3 tools/acc/upgh/sac_to_ac.py [--out FILE]"""
import argparse
import glob
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import twin_lookup as T  # noqa: E402
from harvest import extract  # noqa: E402
from sources import load_board  # noqa: E402

REPO = T.REPO


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    A = load_board(sorted(glob.glob(str(REPO / "research/acc/live/boards/ac_2026*.json.gz")))[-1])
    st = T.h.state()
    held = {}
    for obj in (T.h,):
        try:
            held = obj.held(st)
        except Exception:
            pass
    sac = {}
    for cid, b in st.best.items():
        if cid.startswith("sac-"):
            sac.setdefault(cid, set()).add(tuple(b["moves"]))
    files = list((REPO / "research/acc/live").rglob("*.txt")) + list(REPO.glob("ACC_*.txt"))
    for f in files:
        if f.stat().st_size > 30_000_000:
            continue
        for cid, moves, _ in extract(f):
            if cid.startswith("sac-"):
                sac.setdefault(cid, set()).add(tuple(moves))
    never = set(T.h.cfg["gates"].get("never_rows", []))
    hits = []
    for scid, paths in sac.items():
        acid = scid[1:]
        if acid not in T.CH or acid.split("-")[1] in never:
            continue
        rec = A.get(acid, {}).get("record")
        if rec is None:
            continue
        mine = held.get(acid)
        best = None
        for p in paths:
            if len(p) < 3 or tuple(p[-2:]) != (16, 15) or any(m > 13 for m in p[:-2]):
                continue
            q = list(p[:-2])
            if len(q) > rec or (mine is not None and len(q) >= mine):
                continue
            if T.core.verify(T.CH[acid], q, "ac-r2-v1", T.man["limits"])["ok"] and (best is None or len(q) < len(best)):
                best = q
        if best:
            k = A[acid].get("k")
            hits.append((len(best) - rec, -(2.0 ** (1 - k)) if k else 0, acid, len(best), rec, k, mine, best))
    hits.sort()
    for d, _, acid, L, rec, k, mine, _p in hits:
        print("%s AC %d vs record %d (k %s) -> %s; we hold AC %s" % (acid, L, rec, k, "BEAT" if L < rec else "tie", mine))
    print("AC lines hidden in Stable paths: %d" % len(hits))
    if a.out and hits:
        Path(a.out).write_text("# UPG-H sac_to_ac: AC prefix of a Stable path ending [16,15]; official AC core ok\n"
                               + "".join("%s: [%s]\n" % (h[2], ", ".join(map(str, h[7]))) for h in hits))
        print("wrote", a.out)


if __name__ == "__main__":
    main()
