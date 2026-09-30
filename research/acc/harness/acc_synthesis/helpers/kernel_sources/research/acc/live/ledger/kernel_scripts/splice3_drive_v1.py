# SCRIPT: BOB-SPLICE3-DRIVE-01
# Loop the reach-3 C++ splice until no saving; each splice is checked with the official core
# (bridge must carry state_i exactly to state_k, full line must still reach ((1,),(2,))).
import subprocess, sys, json, time
sys.path.insert(0, '/home/claude/sair/competition/tools')
from verifier.core import apply_move, free_reduce
from block_splice_v1 import make_steps
def states(s0, p):
    S = [s0]
    for m in p: S.append(apply_move(S[-1], m))
    return S
def splice3(rel, path, lib, slack=4, timeout=1800):
    steps = make_steps(lib)
    stepsTxt = '\n'.join(' '.join(map(str, s)) for s in steps)
    s0 = (free_reduce(tuple(rel[0])), free_reduce(tuple(rel[1])))
    path = list(path); log = []
    while True:
        inp = ' '.join(map(str, s0[0])) + '\n' + ' '.join(map(str, s0[1])) + '\n' + ' '.join(map(str, path)) + '\n' + stepsTxt + '\n'
        out = subprocess.run(['./splice3', str(slack)], input=inp, capture_output=True, text=True, timeout=timeout).stdout.split()
        if not out or out[0] != 'BEST': return path, log
        sav, i, k = int(out[1]), int(out[2]), int(out[3]); bridge = list(map(int, out[4:]))
        S = states(s0, path)
        t = S[i]
        for m in bridge: t = apply_move(t, m)
        if t != S[k]:
            log.append(dict(reject=True, i=i, k=k)); return path, log   # hash collision guard
        path = path[:i] + bridge + path[k:]
        log.append(dict(i=i, k=k, bridge=bridge, saving=sav, new_len=len(path)))
