# SCRIPT: EYE-UNION-EXTRACT-01
"""Harvest every Compound Eye definition (id@version) from every available source.

Why this finds everything a source holds: every eye in every build is stored as a
JSON object carrying both an "id" and a "version" field (catalog files, the Mixer's
embedded tables, the 500-view catalog). The scanner decodes EVERY JSON object that
starts with {"id": anywhere in a file (HTML, JS, JSON), and keeps the ones that also
carry "version". Nothing depends on a particular variable name or layout, so a build
that stores its eyes differently is still read. Python-defined registries (harness v2)
are read with the Python parser. Each eye keeps the list of every source it was seen in.
"""
import ast, glob, hashlib, json, os, re, sys, collections

S = '/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'
dec = json.JSONDecoder()
START = re.compile(r'\{\s*"id"\s*:\s*"')

union = {}              # key id@version -> best record
seen = collections.defaultdict(set)   # key -> sources
defhash = collections.defaultdict(set)


def richness(rec):
    return len(rec) + (10 if 'implementation' in rec else 0) + (5 if 'assumptions' in rec else 0)


def add(rec, source):
    if not isinstance(rec, dict):
        return
    i, v = rec.get('id'), rec.get('version')
    if not isinstance(i, str) or not isinstance(v, str):
        return
    if not re.fullmatch(r'[A-Za-z0-9_.\-:]+', i) or not re.fullmatch(r'[0-9A-Za-z.\-+]+', v):
        return
    if 'eyes' in rec and isinstance(rec['eyes'], list) and 'title' in rec and 'family' not in rec:
        return  # a set definition, not an eye
    if i.startswith('ce.set.'):
        return
    key = f'{i}@{v}'
    seen[key].add(source)
    core = {k: rec[k] for k in sorted(rec) if k in ('id', 'version', 'title', 'family', 'inputs', 'assumptions', 'implementation')}
    defhash[key].add(hashlib.sha256(json.dumps(core, sort_keys=True, default=str).encode()).hexdigest()[:12])
    if key not in union or richness(rec) > richness(union[key]):
        union[key] = rec


def scan_text(text, source):
    n = 0
    for m in START.finditer(text):
        try:
            obj, _ = dec.raw_decode(text, m.start())
        except Exception:
            continue
        before = len(seen)
        add(obj, source)
        n += 1
    return n


sources = []
for p in sorted(glob.glob(S + '/eyesrc/*.html')):
    sources.append((os.path.basename(p), p))
for p in sorted(glob.glob(S + '/unz/**/*.json', recursive=True)):
    top = p.split('/unz/')[1].split('/')[0]
    sources.append((top + '.zip', p))
for p in sorted(glob.glob(S + '/unz/**/*.html', recursive=True)) + sorted(glob.glob(S + '/unz/**/*.js', recursive=True)):
    top = p.split('/unz/')[1].split('/')[0]
    sources.append((top + '.zip', p))

# repo branches
blobmap = collections.defaultdict(set)
for line in open(S + '/repo_eye_blobs.tsv'):
    h, path, br = line.rstrip('\n').split('\t')
    blobmap[h].add(br)
for h, brs in blobmap.items():
    sources.append(('repo:' + ('main' if 'main' in brs else sorted(brs)[0]), S + '/repo_eyes/' + h))

per_source = collections.Counter()
for name, path in sources:
    try:
        text = open(path, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    if path.endswith('.py') or 'EYE_REGISTRY' in text[:200000] and 'def ' in text:
        # Python registry (harness v2)
        mver = re.search(r'^VERSION\s*=\s*"([^"]+)"', text, re.M)
        m = re.search(r'^EYE_REGISTRY\s*=\s*(\[.*?^\])', text, re.M | re.S)
        if m and mver:
            src = m.group(1).replace('VERSION', repr(mver.group(1)))
            for rec in ast.literal_eval(src):
                add(rec, name if not name.startswith('repo:') else name + ':harness_v2')
            continue
    before = {k: len(v) for k, v in seen.items()}
    scan_text(text, name)
    per_source[name] = sum(1 for k, v in seen.items() if name in v)

json.dump({k: union[k] for k in sorted(union)}, open(S + '/eye_union.json', 'w'))
json.dump({k: sorted(v) for k, v in seen.items()}, open(S + '/eye_sources.json', 'w'), indent=0)
json.dump({k: sorted(v) for k, v in defhash.items() if len(v) > 1}, open(S + '/eye_conflicts.json', 'w'), indent=0)

src_counts = collections.Counter()
for k, v in seen.items():
    for s in {x.split(':harness')[0] for x in v}:
        src_counts[s] += 1
print('TOTAL distinct eye versions (id@version):', len(union))
print('distinct ids:', len({k.split('@')[0] for k in union}))
print('\nper source:')
for s, c in sorted(src_counts.items(), key=lambda x: -x[1]):
    print(f'  {c:5d}  {s}')
m51 = {f"{e['id']}@{e['version']}" for e in json.load(open(S + '/eyesrc/m51_eyes.json'))}
missing = sorted(set(union) - m51)
print('\nNOT in Mixer 5.1:', len(missing))
fam = collections.Counter(union[k].get('family', '?') for k in missing)
print(fam.most_common())
print('\ndefinition conflicts (same id@version, different definitions):', sum(1 for v in defhash.values() if len(v) > 1))
