import json,subprocess,os,sys
C2P={1:0,-1:1,2:2,-2:3}
ENG=os.path.abspath("./bidir2")
N={i["challengeId"]:i for i in json.load(open("snapshot_items.json"))}
O={i["challengeId"]:i for i in json.load(open("snapshot_items_prev.json"))}
# rows that produced a MEET this session, with the cap they met at
TIES=[("ac-00742",23),("ac-01411",23),("ac-04631",23),("ac-10029",25),("ac-06225",26),
      ("ac-00977",26),("ac-04275",25),("ac-06823",25),("ac-10115",22),("ac-01059",25)]
out=[]
for cid,cap in TIES:
    rel=O[cid]["initialRelators"]
    a=[C2P[c] for c in rel[0]]; b=[C2P[c] for c in rel[1]]
    args=[ENG,str(cap),"20000000",str(len(a))]+[str(x) for x in a]+[str(len(b))]+[str(x) for x in b]+["1","0","1","2"]
    p=subprocess.run(args,capture_output=True,text=True,timeout=900)
    so=p.stdout
    if not so.startswith("MEET"): print(cid,"NO MEET",so.split(chr(10))[0]); continue
    L=int(so.split("len=")[1].split()[0])
    moves=so.split("MOVES")[1].split()
    rec=N[cid]["currentBestLength"]
    out.append({"challengeId":cid,"cap":cap,"length":L,"boardRecord":rec,
                "kTeams":N[cid]["kTeams"],"relation":("BEATS" if L<rec else "TIE" if L==rec else "WORSE"),
                "initialRelators":rel,"moves":[int(m) for m in moves]})
    print(f"{cid} cap={cap} len={L} board={rec} k={N[cid]['kTeams']} {out[-1]['relation']} moves={len(moves)}")
json.dump(out,open("PRIVATE_ties_20260916.json","w"),indent=1)
print("captured",len(out))
