"""verify_full.py MOVES_JSON_LIST [--append out.txt] : replay moves on the pinned official core (SAIR=/root/.cache/upgh/sair)."""
import sys, json, os
SAIR = os.environ.get('SAIR', '/root/.cache/upgh/sair')
sys.path.insert(0, SAIR + '/competition/tools')
from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json'))
ch = [c for c in man['challenges'] if c['challenge_id'] == 'ac-00145'][0]
def check(moves):
    r = core.verify(ch, moves, ch['move_spec_version'], man['limits'])
    return r
if __name__ == '__main__':
    moves = json.loads(sys.argv[1]); r = check(moves); print(json.dumps(r))
    if r.get('ok') and '--append' in sys.argv:
        with open(sys.argv[sys.argv.index('--append') + 1], 'a') as f: f.write('ac-00145: ' + json.dumps(moves) + '\n')
