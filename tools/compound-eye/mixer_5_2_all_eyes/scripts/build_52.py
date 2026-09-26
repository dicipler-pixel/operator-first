# SCRIPT: MIXER-5-2-ALL-EYES-BUILD-01
"""Build Compound Eye Matrix Mixer 5.2 (All Eyes) from the canonical 5.1 a1 page.

Rules this build keeps, and how each is enforced:
- The 5.1 engine is not edited. Only the embedded data tables (eyes,
  recoveryBranches, adapterRecoverySummary) and the header/tab count text change.
  The script asserts that everything outside those spans is byte-identical.
- Append-only. Every one of the 550 existing records keeps every field it had;
  the 37 late records only GAIN implementation references (checked below).
- Nothing is invented. Each new record copies what its source states; where a
  source gives no registry ID (the Whitehead eye), the record says so.
"""
import hashlib, json, re, subprocess, sys, collections, os

S = '/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'
REPO = '/home/claude/operator-first'
OUTDIR = S + '/mixer52'
os.makedirs(OUTDIR + '/implementations', exist_ok=True)
page = open(S + '/eyesrc/mixer51_a1.html', encoding='utf-8').read()
dec = json.JSONDecoder()


def span(name):
    m = re.search(r'const\s+' + name + r'\s*=\s*', page)
    obj, end = dec.raw_decode(page, m.end())
    return m.end(), end, obj


e0, e1, eyes = span('eyes')
b0, b1, branches = span('recoveryBranches')
a0, a1, summary = span('adapterRecoverySummary')
assert len(eyes) == 550
orig = json.loads(json.dumps(eyes))
union = json.load(open(S + '/eye_union.json'))
sources = json.load(open(S + '/eye_sources.json'))
have = {f"{e['id']}@{e['version']}" for e in eyes}


def sha_file(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def git_show(branch, path, dest):
    data = subprocess.run(['git', '-C', REPO, 'show', f'origin/{branch}:{path}'], capture_output=True, check=True).stdout
    open(dest, 'wb').write(data)
    return hashlib.sha256(data).hexdigest()


impl_index = {}


def keep_impl(label, branch=None, path=None, local=None):
    dest = OUTDIR + '/implementations/' + label
    if local:
        data = open(local, 'rb').read(); open(dest, 'wb').write(data)
        h = hashlib.sha256(data).hexdigest(); origin = local.split('/scratchpad/')[-1]
    else:
        h = git_show(branch, path, dest); origin = f'operator-first@{branch}:{path}'
    impl_index[label] = {'sha256': h, 'origin': origin}
    return h


# ---- 1. recover code for the 37 late eyes --------------------------------------
late_files = {
    'earth_moon_eye.py': ('research/earth-moon-2026-09-09', 'research/earth_moon_2026_09_09/side_scanner/earth_moon_eye.py'),
    'em_graph_core.py': ('research/earth-moon-2026-09-09', 'research/earth_moon_2026_09_09/side_scanner/graph_core.py'),
    'em_machine.py': ('research/earth-moon-2026-09-09', 'research/earth_moon_2026_09_09/side_scanner/machine.py'),
    'ym_eyes.py': ('formal/yang-mills-allocation-floor-2026-09-13', 'research/yang_mills_2026_09_09/cross_theorem/native/ym_eyes.py'),
    'ym_energy_bins.py': ('formal/yang-mills-allocation-floor-2026-09-13', 'research/yang_mills_2026_09_09/cross_theorem/native/ym_energy_bins.py'),
    'ym_forcing_eye.py': ('formal/yang-mills-allocation-floor-2026-09-13', 'research/yang_mills_2026_09_09/cross_theorem/native/ym_forcing_eye.py'),
}
for label, (br, p) in late_files.items():
    keep_impl(label, br, p)
funcs = {}
for label in late_files:
    for n in re.findall(r'^def ([a-z_0-9]+)\(', open(OUTDIR + '/implementations/' + label).read(), re.M):
        funcs.setdefault(n, label)
recovered = 0
for e in eyes:
    if e.get('recovery_status') and e.get('implementation') is None:
        fn = e['id'].split('.')[-1]
        fam = e['id'].split('.')[1]
        pool = [l for l in late_files if (l.startswith('ym') if fam == 'ym' else not l.startswith('ym'))]
        label = next((l for l in pool if re.search(r'^def ' + fn + r'\(', open(OUTDIR + '/implementations/' + l).read(), re.M)), None)
        assert label, e['id']
        e['implementation_recovered'] = {
            'path': 'implementations/' + label, 'function': fn,
            'sha256': impl_index[label]['sha256'], 'source': impl_index[label]['origin'],
            'note': 'Recovered in 5.2 from the branch that produced this eye; the registered contract above is unchanged.'}
        recovered += 1
assert recovered == 37, recovered

# ---- 2. the 26 defined eyes missing from 5.1 ------------------------------------
H = keep_impl('compound_eye_harness_acc_v2.py', 'claude/confident-fermi-09rd02', 'tools/acc/harness/compound_eye_harness_acc_v2.py')
for f in ['acc_image_distance.py', 'acc_donor_trace.py', 'acc_parity_component.py']:
    keep_impl(f, local=S + '/unz/acc_dispatch/engines/acc_eyes/' + f)
new = []
for key in sorted(k for k in union if k not in have):
    r = dict(union[key]); src = sources.get(key, [])
    if r.get('stage'):  # harness v2 registry entry
        rid = r['id']
        r = {'id': rid, 'version': r['version'],
             'title': rid.split('.', 2)[2].replace('.', ' / ').replace('_', ' ').title(),
             'family': 'ACC harness v2 (' + r['stage'] + ')', 'status': r['status'],
             'inputs': {'state': 'balanced two-relator presentation or verified path'},
             'depends_on': [], 'assumptions': ['Official ordinary AC moves 0..13; exact replay only.'],
             'output_meaning': r.get('meaning', ''),
             'evidence_class': 'exact_computation' if r['stage'] in ('exact', 'census', 'deep', 'path', 'frontier') else 'routing_heuristic',
             'limits': 'Heuristic signatures route work; only exact replay, closure or certified obstructions may prove or prune.',
             'implementation': {'path': 'implementations/compound_eye_harness_acc_v2.py', 'sha256': H, 'function': 'EYE_REGISTRY / stage ' + r['stage']}}
    elif r['id'].startswith('ce.acc.'):
        base = r['id'].split('.')[-1]
        r.setdefault('implementation', {})
        r['implementation'] = {'path': f'implementations/acc_{base}.py', 'sha256': impl_index[f'acc_{base}.py']['sha256'], 'function': 'run'}
    for k in ['id', 'version', 'title', 'family', 'status', 'inputs', 'depends_on', 'assumptions', 'output_meaning', 'evidence_class', 'limits', 'implementation']:
        r.setdefault(k, None if k == 'implementation' else ([] if k in ('depends_on', 'assumptions') else ({} if k == 'inputs' else '')))
    r['recovery_sources'] = src
    r['added_in'] = 'Mixer 5.2 All Eyes'
    new.append(r)
assert len(new) == 26, len(new)

# ---- 3. Phase Playground companion eyes ------------------------------------------
pp = open(S + '/eyesrc/phase_playground.html', encoding='utf-8').read()
m = re.search(r'<script[^>]*type="application/json"[^>]*>', pp)
data, _ = dec.raw_decode(pp, m.end())
pp_sha = sha_file(S + '/eyesrc/phase_playground.html')
defs = {}
for study in data:
    for res in study['run']['native']['results']:
        defs.setdefault(res['eye'], res)
for ref, res in sorted(defs.items()):
    rid, ver = ref.split('@')
    if rid.endswith('_set') or '.whole_' in rid:
        continue
    new.append({'id': rid, 'version': ver,
                'title': rid.split('.')[-1].replace('_', ' ').title(),
                'family': 'Phase Playground (coupled-waveguide phase)', 'status': 'implemented',
                'inputs': {'model': 'coupled-waveguide-phase-v1 configuration'},
                'depends_on': res.get('dependencies', []), 'assumptions': res.get('assumptions', []),
                'output_meaning': 'Scoped computed diagnostic of the synthetic coupled-rail phase model.',
                'evidence_class': res.get('evidence_class', ''), 'limits': res.get('limits', ''),
                'implementation': {'path': 'Compound_Eye_Phase_Playground.html (embedded kernel 1.0.0)', 'sha256': pp_sha,
                                   'definition_sha256': res.get('definition_sha256')},
                'recovery_sources': ['Compound_Eye_Phase_Playground.html (2026-09-10)'],
                'added_in': 'Mixer 5.2 All Eyes'})
n_pp = sum(1 for r in new if r['id'].startswith('companion.phase.'))
assert n_pp == 12, n_pp

# ---- 4. Whitehead eye (named in the 2026-09-17 return; no registry id existed) --
W = keep_impl('whitehead.py', 'claude/confident-fermi-09rd02', 'tools/acc/whitehead.py')
new.append({'id': 'ce.acc.whitehead_minimization', 'version': '1.0.0',
            'title': 'Whitehead minimization', 'family': 'ACC harness v2 (frontier)', 'status': 'implemented',
            'inputs': {'state': 'balanced two-relator presentation'}, 'depends_on': [],
            'assumptions': ['Cyclically reduce the tuple; evaluate the finite rank-2 Type-II shear family exactly.'],
            'output_meaning': 'Best cyclic total and the shortening transforms; graph connectivity and cut data kept as a cheaper structural signal, not an if-and-only-if minimality theorem.',
            'evidence_class': 'exact_computation',
            'limits': 'Routes attention only. Cannot certify AC equivalence or cyclic-length minimality by itself; closed-cap statements stay on the ordinary-AC ledger.',
            'implementation': {'path': 'implementations/whitehead.py', 'sha256': W, 'function': 'main'},
            'recovery_sources': ['ACC_WHITEHEAD_EYE_RETURN_20260917.md', 'operator-first@claude/confident-fermi-09rd02:tools/acc/whitehead.py'],
            'id_note': 'The return names this eye but gives no registry id; this id is assigned by the 5.2 union and marked as such.',
            'added_in': 'Mixer 5.2 All Eyes'})

# ---- 5. assemble -----------------------------------------------------------------
for r in new:
    assert f"{r['id']}@{r['version']}" not in have
eyes_out = eyes + new
for a, b in zip(orig, eyes_out[:550]):          # append-only check
    for k, v in a.items():
        assert b[k] == v, (a['id'], k)
total = len(eyes_out); domain = total - 309
summary_out = dict(summary)
summary_out.update({'domain_eye_count': domain, 'union_views': total,
                    'added_in_5_2': len(new),
                    'added_breakdown_5_2': dict(collections.Counter(r['family'].split(' (')[0] for r in new)),
                    'late_implementations_recovered_5_2': recovered,
                    'implementation_note_5_2': 'All 37 late eyes now carry the code recovered from the branches that produced them (implementations/). Their registered contracts are unchanged.'})
branches_out = branches + [
    {'name': 'ACC harness v2', 'date': '2026-09-16', 'eyes': 16, 'role': '16 ACC eyes: exact replay, ledger, Magnus 2/3, ordered transport, fiber holonomy, frontier channels, collision ladder, search adapters', 'source': 'operator-first claude/confident-fermi-09rd02 tools/acc/harness/compound_eye_harness_acc_v2.py'},
    {'name': 'ACC dispatch adapters', 'date': '2026-09-16', 'eyes': 3, 'role': 'image distance, donor trace, parity component', 'source': 'ACC_DISPATCH.tar.gz engines/acc_eyes'},
    {'name': 'ACC Whitehead eye', 'date': '2026-09-17', 'eyes': 1, 'role': 'exact rank-2 Whitehead minimization as a frontier routing eye', 'source': 'ACC_WHITEHEAD_EYE_RETURN_20260917.md + tools/acc/whitehead.py'},
    {'name': 'Elemental Foundations', 'date': '2026-09-08/12', 'eyes': 6, 'role': 'foundation graph/response pair + Gram, ladder, relaxation, singular-angle reductions', 'source': 'operator-first research/elemental-foundations(-v4)'},
    {'name': 'Phase Playground', 'date': '2026-09-10', 'eyes': 12, 'role': 'companion.phase coupled-rail eyes: norm balance, transfer, currents, skin, gauge guard, flux, vortex, knot scope and more', 'source': 'Compound_Eye_Phase_Playground.html'},
    {'name': 'Late-eye code recovery', 'date': '2026-09-26', 'eyes': 37, 'role': 'implementations for the 15 Earth-Moon side-scanner and 22 Yang-Mills cross-theorem eyes', 'source': 'operator-first research/earth-moon-2026-09-09 and formal/yang-mills-allocation-floor-2026-09-13'},
]


def js(x):
    return json.dumps(x, ensure_ascii=False, separators=(',', ':'))


out = page[:e0] + js(eyes_out) + page[e1:b0] + js(branches_out) + page[b1:a0] + js(summary_out) + page[a1:]
# header and tab text
out = out.replace('<h1>Compound Eye<br>Matrix Mixer 5.1</h1>', '<h1>Compound Eye<br>Matrix Mixer 5.2 · All Eyes</h1>', 1)
out = out.replace('<div class="stat"><b>550</b>versioned views retained</div><div class="stat"><b>241</b>domain eye versions</div>',
                  f'<div class="stat"><b>{total}</b>versioned views retained</div><div class="stat"><b>{domain}</b>domain eye versions</div>', 1)
out = out.replace('<button data-tab="catalog">All 550 views</button>', f'<button data-tab="catalog">All {total} views</button>', 1)
t = re.search(r'<title>(.*?)</title>', out)
out = out.replace(t.group(0), '<title>Compound Eye Matrix Mixer 5.2 · All Eyes</title>', 1) if t else out
assert out.count(f'<b>{total}</b>') >= 1

# engine unchanged: compare everything except the replaced spans and the three text edits
def strip(s):
    for pat in [r'const\s+eyes\s*=\s*', r'const\s+recoveryBranches\s*=\s*', r'const\s+adapterRecoverySummary\s*=\s*']:
        m = re.search(pat, s); _, end = dec.raw_decode(s, m.end()); s = s[:m.end()] + 'X' + s[end:]
    s = re.sub(r'<title>.*?</title>', '', s); s = re.sub(r'<h1>Compound Eye<br>Matrix Mixer[^<]*</h1>', '', s)
    s = re.sub(r'<b>\d+</b>(versioned views retained|domain eye versions)', r'\1', s)
    s = re.sub(r'All \d+ views', 'All views', s)
    return s
assert strip(out) == strip(page), 'engine changed'

name = 'Compound_Eye_Matrix_Mixer_5_2_All_Eyes.html'
open(OUTDIR + '/' + name, 'w', encoding='utf-8').write(out)
json.dump(eyes_out, open(OUTDIR + '/ALL_EYES_CATALOG.json', 'w'), indent=1, ensure_ascii=False)
ledger = {f"{r['id']}@{r['version']}": sorted(set(r.get('recovery_sources') or []) | set(sources.get(f"{r['id']}@{r['version']}", []))) for r in eyes_out}
json.dump(ledger, open(OUTDIR + '/EYE_SOURCE_LEDGER.json', 'w'), indent=1, ensure_ascii=False)
json.dump(impl_index, open(OUTDIR + '/implementations/INDEX.json', 'w'), indent=1)
print(json.dumps({'total_views': total, 'domain_eyes': domain, 'retina_views': 309, 'added': len(new),
                  'added_breakdown': summary_out['added_breakdown_5_2'], 'late_code_recovered': recovered,
                  'html_bytes': len(out.encode()), 'html_sha256': hashlib.sha256(out.encode()).hexdigest()}, indent=1))
