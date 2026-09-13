import subprocess, re, json, hashlib, sys
branches=[l.strip() for l in subprocess.run(['git','branch','-r'],capture_output=True,text=True).stdout.splitlines() if 'HEAD' not in l]
DECL=re.compile(r'^(\s*)(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(theorem|lemma|def|abbrev|instance|structure|inductive)\s+([^\s:({\[]+)')
out=[]; seen={}
def show(b,f): return subprocess.run(['git','show',f'{b}:{f}'],capture_output=True,text=True).stdout
for b in branches:
    head=subprocess.run(['git','rev-parse',b],capture_output=True,text=True).stdout.strip()
    files=[f for f in subprocess.run(['git','ls-tree','-r','--name-only',b],capture_output=True,text=True).stdout.split() if f.endswith('.lean')]
    for f in files:
        src=show(b,f); lines=src.splitlines()
        lastc=subprocess.run(['git','log','-1','--format=%H %cI',b,'--',f],capture_output=True,text=True).stdout.strip()
        i=0
        while i<len(lines):
            m=DECL.match(lines[i])
            if m and m.group(2) in ('theorem','lemma'):
                indent=m.group(1); kind=m.group(2); name=m.group(3)
                # collect declaration text until ':=' at top-level of this decl or a line starting 'by' / '|' pattern
                buf=[lines[i]]; j=i
                while ':=' not in ' '.join(buf) and j+1<len(lines):
                    j+=1
                    if DECL.match(lines[j]) and not lines[j].startswith(indent+' '): break
                    buf.append(lines[j])
                text='\n'.join(buf); stmt=text.split(':=')[0].rstrip()
                key=hashlib.sha256((f+'\n'+stmt).encode()).hexdigest()[:16]
                rec=seen.get(key)
                if rec is None:
                    rec={'key':key,'kind':kind,'name':name,'file':f,'statement':stmt,'branches':[]}; seen[key]=rec; out.append(rec)
                rec['branches'].append({'branch':b.replace('origin/',''),'head':head[:12],'file_last_commit':lastc.split()[0][:12] if lastc else None,'file_last_commit_date':lastc.split()[1] if lastc else None})
                i=j+1
            else: i+=1
json.dump(out,open(sys.argv[1],'w'),indent=0)
files=set(r['file'] for r in out); print('unique declarations',len(out),'unique files',len(files))
import collections; print('per top dir',collections.Counter(r['file'].split('/')[0] for r in out).most_common())
print('files on main:',sum(1 for r in out if any(x['branch']=='main' for x in r['branches'])))
