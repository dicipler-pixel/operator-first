#!/usr/bin/env python3
"""Idea cycler: for each target row, try a fixed list of beam ideas (each paired with its opposite) on the row and on its
symmetric twins, until one reaches the record. Every attempt is logged, so no (row, idea, variant) repeats.

usage: idea_cycler.py TARGETS.json OUT.jsonl [--beam BIN] [--table T9.tab] [--sair SAIR_ROOT] [--timeout 300]
TARGETS.json: [{"id": "ac-00022", "record": 45, "k": 1}, ...]
Paths found on a twin are mapped back to the original row by exact move permutations (derived and checked on random
states) and replayed through the official verifier core before they are written. A hit still needs the normal
inbox checks (plan_offline.py) before sending."""
import argparse, json, os, random, subprocess, sys, time

IDEAS = [  # (name, env, width, extra depth)  opposites sit next to each other
    ("greedy-len",   {"BEAM_H": "0"},                                          50000, 2),
    ("hump-H",       {"BEAM_H": "1", "BEAM_DIV": "1.0"},                       50000, 2),
    ("p2-look",      {"BEAM_P2": "2", "BEAM_H": "1", "BEAM_DIV": "0.8"},       20000, 2),
    ("balanced",     {"BEAM_BAL": "1", "BEAM_H": "1"},                         50000, 2),
    ("novelty",      {"BEAM_NOV": "1", "BEAM_H": "1"},                         50000, 2),
    ("noise-seed7",  {"BEAM_H": "1", "BEAM_NOISE": "3", "BEAM_SEED": "7"},     50000, 2),
    ("wide-200k",    {"BEAM_H": "1", "BEAM_DIV": "1.0"},                      200000, 2),
    ("deep-road",    {"BEAM_H": "1", "BEAM_DIV": "1.0"},                       50000, 15),
]
VARIANTS = ["as-is", "swap-relators", "swap-xy", "invert-letters"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets"); ap.add_argument("out")
    S = os.environ.get("ACC_SCRATCH", ".")
    ap.add_argument("--beam", default=f"{S}/acc_beam_p2"); ap.add_argument("--table", default=f"{S}/work/T9.tab")
    ap.add_argument("--sair", default=f"{S}/sair"); ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--ideas", default="", help="comma list of idea names to run (default all)")
    a = ap.parse_args()
    sys.path.insert(0, a.sair + "/competition/tools")
    from verifier import core
    man = json.load(open(a.sair + "/competition/tools/verifier/data/manifest.json"))
    CH = {c["challenge_id"]: c for c in man["challenges"]}

    def tw(s, v):  # twin of a state
        r0, r1 = s
        if v == "as-is": return (r0, r1)
        if v == "swap-relators": return (r1, r0)
        f = {1: 2, -1: -2, 2: 1, -2: -1} if v == "swap-xy" else {1: -1, -1: 1, 2: -2, -2: 2}
        return (tuple(f[t] for t in r0), tuple(f[t] for t in r1))

    rng = random.Random(1)
    def rand_state():
        def w():
            out = []
            while len(out) < rng.randint(3, 9):
                t = rng.choice((1, -1, 2, -2))
                if out and out[-1] == -t: continue
                out.append(t)
            return tuple(out)
        return (w(), w())

    PERM = {}  # move on twin -> move on original
    for v in VARIANTS:
        p = {}
        for m in range(14):
            cands = set(range(14))
            for _ in range(40):
                s = rand_state()
                want = tw(core.apply_move(s, m), v)
                cands = {c for c in cands if core.apply_move(tw(s, v), c) == want}
            assert len(cands) >= 1, (v, m)
            p[min(cands)] = m  # twin move min(cands) corresponds to original move m
        assert len(p) == 14, v
        PERM[v] = p

    done = set()
    if os.path.exists(a.out):
        for l in open(a.out):
            try: r = json.loads(l); done.add((r["id"], r["idea"], r["variant"]))
            except Exception: pass
    E = {1: 0, -1: 1, 2: 2, -2: 3}
    ideas = [i for i in IDEAS if not a.ideas or i[0] in a.ideas.split(",")]
    for t in json.load(open(a.targets)):
        cid, rec = t["id"], t["record"]
        start = tuple(tuple(r) for r in CH[cid]["initial_relators"])
        solved = False
        for name, env, W, extra in ideas:
            if solved: break
            for v in VARIANTS:
                if (cid, name, v) in done: continue
                s = tw(start, v)
                enc = [str(len(s[0]))] + [str(E[x]) for x in s[0]] + [str(len(s[1]))] + [str(E[x]) for x in s[1]]
                t0 = time.time(); rec_out = {"id": cid, "record": rec, "idea": name, "variant": v}
                try:
                    out = subprocess.run([a.beam, a.table, str(W), str(rec + extra)] + enc, capture_output=True, text=True,
                                         timeout=a.timeout, env={**os.environ, **env}).stdout
                except subprocess.TimeoutExpired:
                    out = ""; rec_out["timeout"] = True
                for line in out.splitlines():
                    if line.startswith("AC ") and "PATH" in line:
                        mv = [PERM[v][int(x)] for x in line.split("PATH")[1].split()]
                        st = start
                        for m in mv: st = core.apply_move(st, m)
                        if st == ((1,), (2,)):
                            rec_out["ac"] = mv; rec_out["ac_len"] = len(mv)
                        else:
                            rec_out["map_fail"] = True
                rec_out["wall_s"] = round(time.time() - t0, 1)
                n = rec_out.get("ac_len")
                rec_out["verdict"] = "nopath" if n is None else ("BEAT" if n < rec else "TIE" if n == rec else "above")
                with open(a.out, "a") as f: f.write(json.dumps(rec_out) + "\n")
                print(cid, name, v, rec_out["verdict"], n, flush=True)
                if n is not None and n <= rec: solved = True; break

if __name__ == "__main__":
    main()
