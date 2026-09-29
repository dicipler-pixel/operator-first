# SCRIPT: CHARLIE_PUSH_06737 -- deeper surgery on the 36-move ac-06737 route at cap 31 (cap 29 already done)
import sys, json, os; sys.path.insert(0, '/home/claude/acc/charlie')
os.environ.setdefault('SURG_WORK', 'surgC')
import surgery as sg, charlie_run as cr
R = [1, 4, 11, 4, 7, 5, 13, 1, 4, 8, 6, 3, 8, 6, 4, 3, 7, 9, 7, 12, 9, 5, 10, 12, 11, 13, 2, 6, 8, 5, 1, 2, 5, 5, 5, 3]
c, lim = cr.load_row('ac-06737'); s0 = tuple(map(tuple, c['initial_relators']))
assert sg.replay(s0, R)[-1] == ((1,), (2,)) and cr.core.verify(c, R, 'ac-r2-v1', lim).get('ok')
K = 31
while True:
    new = sg.win_shorten(s0, R, K, 11, log=lambda m: print('  window', m, flush=True))
    if len(new) < len(R): R = new; continue
    new, tc = sg.tails(s0, R, 'x,y', K, lambda m: print(m, flush=True))
    if new: R = new; continue
    new, hc = sg.heads(s0, R, K, lambda m: print(m, flush=True))
    if new: R = new; continue
    break
v = cr.core.verify(c, R, 'ac-r2-v1', lim)
print('cap', K, 'final', len(R), 'tails<=', tc, 'heads<=', hc, 'verifier', v.get('ok'), flush=True)
print('ac-06737:', json.dumps(R), flush=True)
with open('/home/claude/acc/charlie/runs/charlie_surgery.jsonl', 'a') as f:
    f.write(json.dumps({'row': 'ac-06737', 'side': 'AC push', 'cap': K, 'final': len(R), 'tail_certified_upto': tc, 'head_certified_upto': hc, 'route': R, 'verifier_ok': v.get('ok')}) + '\n')
if len(R) <= 35 and v.get('ok'):
    open('/home/claude/acc/charlie/runs/surgery_inbox/push_ac-06737.txt', 'w').write('ac-06737: ' + json.dumps(R) + '\n')
