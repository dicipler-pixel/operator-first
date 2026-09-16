import subprocess,sys,json,os
C2P={1:0,-1:1,2:2,-2:3}
O={i["challengeId"]:i for i in json.load(open("snapshot_items_prev.json"))}
N={i["challengeId"]:i for i in json.load(open("snapshot_items.json"))}
rows=[l.split()[0] for l in open(sys.argv[1])]
lo,hi=int(sys.argv[2]),int(sys.argv[3]); seed=sys.argv[4]; rs=sys.argv[5]
for cid in rows[lo:hi]:
    try:
        r=subprocess.run(["python3","pipeline.py",cid,seed,rs],capture_output=True,text=True,timeout=1500)
        print(r.stdout.strip() or r.stderr.strip()[:120],flush=True)
    except subprocess.TimeoutExpired:
        print(f"{cid}: TIMEOUT",flush=True)
