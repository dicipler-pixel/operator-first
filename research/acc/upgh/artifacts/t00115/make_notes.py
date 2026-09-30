import json, glob, os, collections
ART = os.path.dirname(os.path.abspath(__file__))
out = []
def rng(xs):
    xs = sorted(xs); return ', '.join(map(str, xs)) if xs else 'none'
for f in sorted(glob.glob(os.path.join(ART, 'res_*.json'))):
    r = json.load(open(f)); P = r['pairs']
    c = collections.Counter(p['result'] for p in P)
    out.append('## %s cap K=%d (route %d moves, %d over record; per-ball budget %d states, radius max %d)' % (r['row'], r['cap'], r['route_len'], r['over'], r['maxst_ball'], r['rmax']))
    out.append('- ended_by: %s, wall %ss; eligible endpoint states (3 <= i <= L-3, total <= K): %s' % (r.get('ended_by'), r.get('wall_s'), r['eligible_states']))
    out.append('- pairs (gap 15..24, both ends eligible): %d; tested %d; result counts %s; shortcuts found: %d' % (r['n_pairs'], len(P), dict(c), len(r['shortened'])))
    cert = [p for p in P if p['result'] == 'CERTIFIED_NO_SHORTER_BRIDGE']
    byg = collections.defaultdict(list)
    for p in cert: byg[p['gap']].append((p['i'], p['j']))
    out.append('- certified (no bridge of <= g-%d moves at cap %d), by gap:' % (r['over'], r['cap']))
    for g in sorted(byg, reverse=True): out.append('  - gap %d: %d pairs: %s' % (g, len(byg[g]), ' '.join('(%d,%d)' % x for x in sorted(byg[g]))))
    nr = [p for p in P if p['result'] != 'CERTIFIED_NO_SHORTER_BRIDGE' and p['result'] != 'SHORTCUT']
    out.append('- not reached (budget stops, scoped misses): %d' % len(nr))
    for p in nr: out.append('  - (%d,%d) gap %d: %s' % (p['i'], p['j'], p['gap'], p.get('why')))
    out.append('- pairs never tested (deadline): %d' % (r['n_pairs'] - len(P)))
    bs = {k: v for k, v in r['balls'].items() if v['stop'] != 'finished'}
    out.append('- balls stopped by budget/disk (radius reached): ' + ', '.join('s_%s r=%d (%s)' % (k, v['radius'], v['stop'][:22]) for k, v in sorted(bs.items(), key=lambda kv: int(kv[0]))))
    for s in r['shortened']: out.append('- SHORTCUT (%d,%d): bridge %d moves, new route %d moves, replay ok=%s' % (s['i'], s['j'], len(s['bridge']), s['new_len'], s['verify_ok']))
    out.append('')
open(os.path.join(ART, 'notes_results.md'), 'w').write('\n'.join(out))
print('\n'.join(out))
