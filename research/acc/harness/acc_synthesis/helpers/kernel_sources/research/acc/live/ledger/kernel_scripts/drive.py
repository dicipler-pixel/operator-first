# SCRIPT: KERNEL-DRIVE-01
# Run the C beam on a row, finish from the length-(1,1) state to ((1,),(2,)) by BFS
# under the official core, and verify the full line with verifier.core.verify.
import sys, json, subprocess, time
from collections import deque
sys.path.insert(0, '/home/claude/sair/competition/tools')
from verifier.core import apply_move, free_reduce
T = ((1,), (2,))
def run(s, p):
    for m in p: s = apply_move(s, m)
    return s
def finish(s):
    q = deque([(s, [])]); seen = {s}
    while q:
        u, p = q.popleft()
        if u == T: return p
        if len(p) >= 8: continue
        for m in range(14):
            v = apply_move(u, m)
            if len(v[0]) + len(v[1]) <= 4 and v not in seen:
                seen.add(v); q.append((v, p + [m]))
    return None
def solve(rel, W, D, L, seed, mode, timeout):
    a = ','.join(map(str, rel[0])); b = ','.join(map(str, rel[1]))
    t0 = time.time()
    try:
        out = subprocess.run(['./beam', a, b, str(W), str(D), str(L), str(seed), str(mode)], capture_output=True, text=True, timeout=timeout).stdout.strip()
    except subprocess.TimeoutExpired:
        return None, 'timeout', time.time() - t0
    if not out.startswith('PATH'):
        return None, out, time.time() - t0
    p = list(map(int, out.split()[1:]))
    s0 = (free_reduce(tuple(rel[0])), free_reduce(tuple(rel[1])))
    f = finish(run(s0, p))
    if f is None: return None, 'nofinish', time.time() - t0
    return p + f, 'ok', time.time() - t0
if __name__ == '__main__':
    rel = [list(map(int, sys.argv[1].split(','))), list(map(int, sys.argv[2].split(',')))]
    print(solve(rel, int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), 1, int(sys.argv[6]), 600))
