import json, os, sys
SAIR = os.environ.get('SAIR', '/root/.cache/upgh/sair')
sys.path.insert(0, SAIR + '/competition/tools')
from verifier import core
T = json.load(open('/home/user/operator-first/research/acc/upgh/tasks/t00115.json'))
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json'))
LET = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
def st(s): return ''.join(LET[a] for a in s[0]) + ',' + ''.join(LET[a] for a in s[1])
def tot(s): return len(s[0]) + len(s[1])
def rows():
    for row, c in T['context'].items():
        CH = [x for x in man['challenges'] if x['challenge_id'] == row][0]
        S0 = tuple(map(tuple, CH['initial_relators']))
        assert list(map(list, S0)) == c['start']
        route = c['our_best_moves']
        S = [S0]
        for m in route: S.append(core.apply_move(S[-1], m))
        yield row, CH, S0, route, S
if __name__ == '__main__':
    for row, CH, S0, route, S in rows():
        v = core.verify(CH, route, 'ac-r2-v1', man['limits'])
        print(row, len(route), v['ok'], 'final', S[-1], 'peak', max(map(tot, S)), 'start', tot(S0))
        print(' totals', [tot(s) for s in S])
