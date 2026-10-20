#!/usr/bin/env python3
"""Turn AC-SolverX (Caltech, ICML 2026) beam-search paths into official SAIR roads.

The 610model beam (beam/beam_search.py in github.com/Math-AI-Caltech/ACSolverX) outputs substitution moves
[i, j, k1, k2]: rotate relator 0 by k1 and relator 1 (inverted if j) by k2, multiply, store in slot i. This script
  1. replays each solved path with the repo's own s_move (exact state sequence, max_length 24);
  2. realises every step with SAIR moves on exact words: cyclic reduction and rotations of each relator by single-letter
     conjugations (moves 6-13), inversion (0/1) when the orientation must flip, then one multiplication (2-5), choosing the
     cheapest rotation/orientation pair whose product is cyclically the env's new relator;
  3. finishes from the final pair of single letters to (x, y) by exact BFS;
  4. maps the road from the solved presentation M to every SAIR row of its Whitehead key (cov_transfer: psi, prefix,
     body, finish) and replays AC on core (ac-r2-v1) and Stable (AC + [16, 15]) on stable_core (sac-r8-v1).
Run with the venv that has jax/flax (it imports the ACSolverX repo for s_move):
  VENV/bin/python tools/acc/upgh/ppo_convert.py --repo ACSOLVERX_DIR --data DATA.txt --meta META.json --csv OUT1.csv [...] --out LINES.txt
META.json: one entry per dataset line, either {"cid": "ac-NNNNN"} (the line is that row's start) or {"key": ..., "rows": [...]}
(the line is the key's minimal form M; roads are transferred to each row)."""
import argparse, ast, csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cov_transfer as CT
SR = CT.SR; core = CT.core
from verifier import stable_core
from whitehead_min import red, cyc, inv, INV

C2I = {"x": 1, "X": -1, "y": 2, "Y": -2}; I2C = {v: k for k, v in C2I.items()}
CONJ = CT.CONJ  # (slot, letter g) -> move id for r <- g r g^-1


def w2s(t): return "".join(I2C[a] for a in t if a)
def s2t(s): return tuple(C2I[c] for c in s)


class Realiser:
    """keeps the exact SAIR state and the emitted moves; every move is applied with core.apply_move"""
    def __init__(self, a, b):
        self.st = (s2t(a), s2t(b)); self.moves = []

    def word(self, slot): return w2s(self.st[slot])

    def apply(self, m):
        self.st = core.apply_move(self.st, m); self.moves.append(m)

    def cyc_reduce(self, slot):
        w = self.word(slot)
        while len(w) > 1 and w[0] == INV[w[-1]]:
            self.apply(CONJ[(slot, INV[w[0]])]); w = self.word(slot)

    def make(self, slot, target):
        """turn the (cyclically reduced) slot word into exactly target = a rotation of it or of its inverse"""
        self.cyc_reduce(slot); w = self.word(slot)
        if w == target: return
        if target not in w + w:
            self.apply(slot)  # inversion move id equals the slot index
            w = self.word(slot)
        assert target in w + w, (w, target)
        n = len(w); k = (w + w).index(target)
        if k <= n - k:
            for _ in range(k):
                w = self.word(slot); self.apply(CONJ[(slot, INV[w[0]])])
        else:
            for _ in range(n - k):
                w = self.word(slot); self.apply(CONJ[(slot, w[-1])])
        assert self.word(slot) == target, (self.word(slot), target)


def rot_cost(cur, target):
    """moves to turn cyclically reduced cur into target (a rotation of cur or of inv(cur))"""
    n = len(cur)
    if target in cur + cur:
        k = (cur + cur).index(target); return min(k, n - k)
    ci = inv(cur)
    if target in ci + ci:
        k = (ci + ci).index(target); return 1 + min(k, n - k)
    return None


def step(R, i, newc):
    """realise one env step: slot i becomes (cyclically, up to inversion) newc; the other slot is unchanged"""
    o = 1 - i
    R.cyc_reduce(i); R.cyc_reduce(o)
    wi, wo = R.word(i), R.word(o)
    target = cyc(newc)
    best = None
    rots = lambda w: {w2[k:] + w2[:k] for w2 in (w, inv(w)) for k in range(max(1, len(w2)))}
    for p in rots(wi):
        cp = rot_cost(wi, p)
        for q in rots(wo):
            cq = rot_cost(wo, q)
            for mul, prod in ((2 + 2 * i, red(p + q)), (3 + 2 * i, red(p + inv(q)))):
                pc = cyc(prod)
                if len(pc) == len(target) and (pc in target + target or inv(pc) in target + target):
                    c = cp + cq + 1
                    if best is None or c < best[0]: best = (c, p, q, mul)
    if best is None: raise ValueError("no realisation for step slot %d -> %s from %s / %s" % (i, newc, wi, wo))
    _, p, q, mul = best
    R.make(i, p); R.make(o, q); R.apply(mul)


def replay_env(repo, x0, path, L=24):
    """exact env state sequence via the repo's own s_move"""
    sys.path.insert(0, repo)
    import jax.numpy as jnp
    from envs.ac_moves import setup_s_actions
    from envs.ac_s import EnvParams
    params = EnvParams(n_gen=2, max_length=L, max_steps_in_episode=1000)
    acts = setup_s_actions(params)
    x = jnp.array(x0, dtype=jnp.int32); out = [x]
    for i, j, k1, k2 in path:
        x = acts[i](x, jnp.array([j, k1, k2], dtype=jnp.int32)); out.append(x)
    return [(w2s([int(v) for v in s[:L]]), w2s([int(v) for v in s[L:]])) for s in out]


def road_for(repo, x0, path):
    """SAIR road from the exact start (x0's two words) to (x, y)"""
    states = replay_env(repo, x0, path)
    R = Realiser(*states[0])
    for (i, j, k1, k2), nxt in zip(path, states[1:]):
        step(R, i, nxt[i])
        for slot in (0, 1):
            assert cyc(R.word(slot)) in (cyc(nxt[slot]) * 2) or inv(cyc(R.word(slot))) in (cyc(nxt[slot]) * 2), "state drift"
    fin = CT.finish_bfs((R.word(0), R.word(1)), cap=10, extra=6)
    if fin is None: raise ValueError("finish failed from %s" % (R.st,))
    for m in fin: R.apply(m)
    assert R.st == ((1,), (2,)), R.st
    return states[0], R.moves


def transfer_from(SA, road, cidB):
    """cov_transfer.transfer with a donor presentation SA (strings) instead of a donor row"""
    SB = tuple(SR.w2s(r) for r in SR.CH[cidB]["initial_relators"])
    got = CT.find_psi(SA, SB)
    if not got: return None, "no psi"
    psi, swap = got
    roadA = [CT.SWID[m] for m in road] if swap else list(road)
    SAf = (SA[1], SA[0]) if swap else SA
    tgt = tuple(CT.apply(psi, x) for x in SAf)
    pre = []
    for slot in (0, 1):
        p = CT.rel_bfs(SB[slot], tgt[slot], slot, cap=40)
        if p is None: return None, "prefix bfs failed"
        pre += p
    body = []
    for m in roadA:
        if m in CT.MOVE_CONJ:
            slot, g = CT.MOVE_CONJ[m]; body += CT.conj_moves(slot, CT.apply(psi, g))
        else: body.append(m)
    endA = ("y", "x") if swap else ("x", "y")
    fin = CT.finish_greedy(tuple(CT.apply(psi, x) for x in endA))
    if fin is None: return None, "finish failed"
    return pre + body + fin, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True); ap.add_argument("--data", required=True); ap.add_argument("--meta", required=True)
    ap.add_argument("--csv", nargs="+", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    X = [ast.literal_eval(l) for l in open(a.data) if l.strip()]
    meta = json.load(open(a.meta))
    lines = []
    for cf in a.csv:
        for r in csv.DictReader(open(cf)):
            if r["solved"] != "True": continue
            idx = int(r["presentation_idx"]); path = ast.literal_eval(r["path_decoded"])
            try:
                start, road = road_for(a.repo, X[idx], path)
            except Exception as e:
                print("CONVERT FAIL idx %d: %s" % (idx, e), flush=True); continue
            m = meta[idx]
            targets = [m["cid"]] if "cid" in m else m["rows"]
            for cid in targets:
                if "cid" in m:
                    full, status = road, "ok"
                else:
                    full, status = transfer_from(start, road, cid)
                if full is None: print("TRANSFER FAIL", cid, status, flush=True); continue
                okA = core.verify(SR.CH[cid], full, "ac-r2-v1", SR.LIM)["ok"]
                sl = full + [16, 15]
                okS = bool(stable_core.verify(SR.CH["s" + cid], sl, "sac-r8-v1", SR.LIM).get("ok"))
                print("idx %d %s: PPO %d steps -> M road %d -> row road %d | AC ok %s | Stable ok %s" % (idx, cid, len(path), len(road), len(full), okA, okS), flush=True)
                if okA:
                    lines.append("# %s from ACSolverX 610model beam (idx %d, %d substitution steps), official core ok\n%s: [%s]\n" % (cid, idx, len(path), cid, ", ".join(map(str, full))))
                if okS:
                    lines.append("s%s: [%s]\n" % (cid, ", ".join(map(str, sl))))
    open(a.out, "w").write("".join(lines))
    print("wrote", a.out, len(lines), "lines")


if __name__ == "__main__":
    main()
