import subprocess, re, json, sys, os
def show(b,f): return subprocess.run(['git','show',f'{b}:{f}'],capture_output=True,text=True).stdout
branches=[l.strip() for l in subprocess.run(['git','branch','-r'],capture_output=True,text=True).stdout.splitlines() if 'HEAD' not in l]
mapping={}   # branch -> file -> [workflow paths]
for b in branches:
    tree=subprocess.run(['git','ls-tree','-r','--name-only',b],capture_output=True,text=True).stdout.split()
    wfs=[f for f in tree if f.startswith('.github/workflows/') and f.endswith(('.yml','.yaml'))]
    leans=[f for f in tree if f.endswith('.lean')]
    wftext={w:show(b,w) for w in wfs}
    # imports of OperatorFirst.lean (root lake target checked by ci.yml leanchecker OperatorFirst)
    root_imports=set()
    if 'OperatorFirst.lean' in leans:
        for m in re.finditer(r'^import\s+([\w.]+)',show(b,'OperatorFirst.lean'),re.M): root_imports.add(m.group(1))
    # lake libraries declared at the repo root: `lake build` in ci.yml builds their default targets
    libs=set()
    for lf in ('lakefile.toml','lakefile.lean'):
        if lf in tree:
            lt=show(b,lf)
            libs|=set(re.findall(r'lean_lib\s+«?([\w.]+)»?',lt))|set(re.findall(r'name\s*=\s*"([\w.]+)"',lt))
            # a lean_lib may declare extra module roots; `lake build` compiles each of them
            for rootlist in re.findall(r'roots\s*=\s*\[([^\]]*)\]',lt):
                libs|=set(re.findall(r'"([\w.]+)"',rootlist))
            libs|=set(re.findall(r'roots\s*:=\s*#\[([^\]]*)\]',lt))
    bm={}
    for f in leans:
        mod=f[:-5].replace('/','.'); base=os.path.basename(f)[:-5]; hits=[]
        for w,t in wftext.items():
            dirs=[ '/'.join(f.split('/')[:k]) for k in range(len(f.split('/'))-1,1,-1) ]   # directory prefixes, deepest first, at least 2 levels
            if f in t or (base+'.lean') in t or re.search(r'(?<![\w.])'+re.escape(mod)+r'(?![\w])',t) or any(d in t for d in dirs): hits.append(w)
            elif w.endswith('/ci.yml') and (f=='OperatorFirst.lean' or mod in root_imports or f.split('/')[0] in libs or base in libs): hits.append(w)
        bm[f]=sorted(set(hits))
    mapping[b.replace('origin/','')]=bm
json.dump(mapping,open(sys.argv[1],'w'),indent=0)
tot=sum(len(v) for v in mapping.values()); cov=sum(1 for v in mapping.values() for w in v.values() if w)
print('branch-file pairs',tot,'with >=1 workflow',cov)
m=mapping['main']; print('main uncovered:',[f for f,w in m.items() if not w])
