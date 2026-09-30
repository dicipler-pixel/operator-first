import gzip,json,re,sys,glob
def rows(f):
    d=json.load(gzip.open(f))["data"]; lst=next(v for v in d.values() if isinstance(v,list))
    return {r["challengeId"]:(r["currentBestLength"],r["kTeams"]) for r in lst}
A=rows(sorted(glob.glob("research/acc/live/boards/ac_2026*.json.gz"))[-1]); B=rows(sorted(glob.glob("research/acc/live/boards/stable_ac_2026*.json.gz"))[-1]); A.update(B)
tot=0
for f in sys.argv[1:]:
    for l in open(f):
        if ":" not in l or not re.match(r"\s*s?ac-\d+",l): continue
        cid,p=l.split(":",1); cid=cid.strip(); p=json.loads(p); rec,k=A[cid]
        v=0 if rec is not None and len(p)>rec else (1 if rec is None or len(p)<rec else 2**-k); tot+=v
        print(cid,len(p),"board",rec,"k",k,"%.4f"%v)
print("total %.4f"%tot)
