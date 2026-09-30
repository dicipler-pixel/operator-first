# SCRIPT: CHARLIE_SAC_YX -- exact shortest route to the Stable finish (y,x) for a row, then two destabilizes.
# Stable AC ends at the empty presentation; from ((x),(y)) OR ((y),(x)) two destabilize moves finish it
# (at ((y),(x)): destabilize r0 = y first, then the relabelled r0 = x, i.e. moves 15, 15;
#  at ((x),(y)): destabilize r1 then r0, i.e. moves 16, 15).
# Swapping the relators is a symmetry of the ac-r2-v1 move set (0<->1, 2<->4, 3<->5, 6..9<->10..13)
# that sends (y,x) to (x,y). So the shortest route from the row to (y,x) under cap K is the
# shortest route from the SWAPPED row to (x,y), with every move swapped back. That route is found
# exactly with acc_disk (forward to depth D, meeting the trivial ball of radius 9; first meeting layer
# a plus the smallest ball depth t gives the exact shortest length a + t under the cap).
# Usage: python3 sac_yx.py ROW_ID CAP MAXLEN   (MAXLEN = longest route to (y,x) worth finding)
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import charlie_run as cr
sys.path.insert(0, cr.SAIR)
from verifier import stable_core
BIN = cr.BIN; BALL = os.path.join(HERE, 'runs', 'B36'); UNION = os.path.join(BALL, 'union9.bin')
SW = {0: 1, 1: 0, 2: 4, 4: 2, 3: 5, 5: 3}
def swap_move(m): return SW[m] if m < 6 else (m + 4 if m <= 9 else m - 4)

def main():
    cid, cap, maxlen = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    c, limits = cr.load_row(cid); r0, r1 = c['initial_relators']
    start_sw = cr.sstr(r1, r0)
    rdir = os.path.join(HERE, 'runs', 'sac', '%s_yx_cap%d' % (cid, cap)); subprocess.run(['rm', '-rf', rdir])
    t0 = time.time()
    out = cr.run([BIN, 'bfs', rdir, start_sw, str(cap), '--mem', os.environ.get('MEM', '3000'), '--meet', UNION,
                  '--maxlayer', str(maxlen - 9), '--minfree', '4'] + (['--lean'] if os.environ.get('LEAN') == '1' else []))
    res = [l for l in out.splitlines() if l.startswith('RESULT')][-1]
    rec = {'row': cid, 'mode': 'route to (y,x) via swapped start', 'cap': cap, 'maxlen': maxlen, 'result': res, 'secs': round(time.time() - t0, 1)}
    if ('MEET' in res or 'TARGET' in res) and os.environ.get('LEAN') == '1':
        rec['verdict'] = 'MEET in lean mode: route to (y,x) exists; recover the path with a two-ended search to the state in RESULT'
    elif 'MEET' in res or 'TARGET' in res:
        a = int(res.split('layer=')[1].split()[0]); La = os.path.join(rdir, 'L_%04d.bin' % a)
        for t in range(10):
            o = cr.run([BIN, 'intersect', La, os.path.join(BALL, 'L_%04d.bin' % t)])
            if not o.startswith('first'): continue
            key = o.split()[1]
            sw_path = cr.moves_to(rdir, key) + [cr.INV[m] for m in reversed(cr.moves_to(BALL, key))]
            ac_to_yx = [swap_move(m) for m in sw_path]
            sac_id = 'sac-' + cid[3:]
            M = json.load(open(os.path.join(cr.SAIR, 'verifier/data/manifest.json')))
            sc = [x for x in M['challenges'] if x['challenge_id'] == sac_id][0]
            path = ac_to_yx + [15, 15]
            v = stable_core.verify(sc, path, 'sac-r8-v1', M['limits'])
            rec.update(route_to_yx=len(ac_to_yx), sac_length=len(path), path=path, ok=v.get('ok'))
            if v.get('ok'): rec['line'] = '%s: %s' % (sac_id, json.dumps(path))
            break
    elif 'MAXLAYER' in res:
        rec['verdict'] = 'CERTIFIED: no route to (y,x) of length <= %d under cap %d' % (maxlen, cap)
    elif 'CLOSED' in res:
        rec['verdict'] = 'CERTIFIED: component under cap %d closed, (y,x) not in it' % cap
    else:
        rec['verdict'] = 'INCOMPLETE (%s)' % res
    with open(os.path.join(HERE, 'runs', 'charlie_sac_yx.jsonl'), 'a') as f: f.write(json.dumps(rec) + '\n')
    print(json.dumps({k: v for k, v in rec.items() if k != 'path'}))
    if rec.get('line'): print(rec['line'])
    subprocess.run(['rm', '-rf', rdir])

if __name__ == '__main__':
    main()
