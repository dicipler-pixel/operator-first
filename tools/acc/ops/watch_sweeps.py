"""Exit (and print) when any sweep result ties or beats its target record and is not yet handled.
Sweeps: $S/work/NAME_cap.jsonl with targets $S/work/NAME_targets.json. Handled rows:
research/acc/live/sweeps/handled.txt (durable)."""
import glob, json, os, time
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad') + '/work/'
H = '/home/user/operator-first/research/acc/live/sweeps/handled.txt'
end = time.time() + 8 * 3600
while time.time() < end:
    handled = set(open(H).read().split()) if os.path.exists(H) else set()
    hits = []
    for res in glob.glob(S + '*_cap.jsonl'):
        tgt = res.replace('_cap.jsonl', '_targets.json')
        if not os.path.exists(tgt): continue
        T = {t['id']: t for t in json.load(open(tgt))}
        for l in open(res):
            r = json.loads(l); t = T.get(r['id'])
            if not t or r['id'] in handled: continue
            a, s = r.get('ac_len') or 999, r.get('sac_len') or 999
            if (t.get('ac_record') and a <= t['ac_record']) or (t.get('sac_record') and s <= t['sac_record']):
                hits.append(f"{os.path.basename(res)} {r['id']} ac {a}/{t.get('ac_record')} sac {s}/{t.get('sac_record')}")
    if hits:
        print('HIT:'); print('\n'.join(hits)); raise SystemExit
    time.sleep(60)
print('no hit in 8h')
