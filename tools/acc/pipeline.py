"""descent -> loop removal -> window shortening. Wires the deep search to the
shortener idea from research/acc/shorten_path.py, against the verified replay."""
import subprocess,sys,json
sys.path.insert(0,"/home/user/operator-first/tools/acc/eyes")
from replay import apply_move, TARGET
INV=[0,1,3,2,5,4,7,6,9,8,11,10,13,12]

def states(r0,r1,moves):
    a,b=list(r0),list(r1); out=[(tuple(a),tuple(b))]
    for m in moves:
        a,b=apply_move(a,b,m); out.append((tuple(a),tuple(b)))
    return out

def peephole(mv):
    o=[]
    for m in mv:
        if o and INV[o[-1]]==m: o.pop()
        else: o.append(m)
    return o

def dedup(r0,r1,mv):
    """Exact loop removal: if state i == state j (j>i), delete moves i..j-1."""
    while True:
        st=states(r0,r1,mv)
        first={}; cut=None
        for i,s in enumerate(st):
            if s in first: cut=(first[s],i); break
            first[s]=i
        if not cut: return mv
        i,j=cut; mv=mv[:i]+mv[j:]
        mv=peephole(mv)

def ball(center,radius,cap):
    out={center:[]}; frontier=[(center,[])]
    for _ in range(radius):
        nxt=[]
        for s,p in frontier:
            for m in range(14):
                a,b=apply_move(list(s[0]),list(s[1]),m)
                if len(a)+len(b)>cap: continue
                t=(tuple(a),tuple(b))
                if t not in out:
                    out[t]=p+[m]; nxt.append((t,p+[m]))
        frontier=nxt
    return out

def window(r0,r1,mv,radius=3,cap=200,lookahead=40,passes=30):
    for _ in range(passes):
        st=states(r0,r1,mv); n=len(mv); improved=False; i=0
        while i<n:
            b=ball(st[i],radius,cap)
            bj=bg=bp=None
            for j in range(min(n,i+lookahead),i,-1):
                h=b.get(st[j])
                if h is not None and len(h)<j-i:
                    g=(j-i)-len(h)
                    if bg is None or g>bg: bj,bg,bp=j,g,h
            if bj is not None:
                mv=mv[:i]+bp+mv[bj:]; mv=peephole(mv)
                st=states(r0,r1,mv); n=len(mv); improved=True
                i+=max(1,len(bp))
            else: i+=1
        if not improved: break
    return mv

def ok(r0,r1,mv):
    st=states(r0,r1,mv); return st[-1]==TARGET

if __name__=="__main__":
    C2P={1:0,-1:1,2:2,-2:3}
    O={i["challengeId"]:i for i in json.load(open("snapshot_items_prev.json"))}
    N={i["challengeId"]:i for i in json.load(open("snapshot_items.json"))}
    cid=sys.argv[1]; seed=sys.argv[2] if len(sys.argv)>2 else "12345"
    restarts=sys.argv[3] if len(sys.argv)>3 else "400"
    rel=O[cid]["initialRelators"]
    r0=[C2P[x] for x in rel[0]]; r1=[C2P[x] for x in rel[1]]
    rec=N[cid]["currentBestLength"] or 10**9
    args=["./descent",seed,restarts,"20000",str(rec),str(len(r0))]+[str(x) for x in r0]+[str(len(r1))]+[str(x) for x in r1]
    r=subprocess.run(args,capture_output=True,text=True,timeout=1200)
    if "HIT len=" not in r.stdout: print(f"{cid}: NOHIT"); sys.exit(1)
    blocks=r.stdout.strip().split("HIT len=")
    best=None
    for blk in blocks[1:]:
        mv=[int(x) for x in blk.split("MOVES")[1].split()]
        if best is None or len(mv)<len(best): best=mv
    raw=len(best)
    mv=peephole(best);   p1=len(mv)
    mv=dedup(r0,r1,mv);  p2=len(mv)
    mv=window(r0,r1,mv); p3=len(mv)
    v=ok(r0,r1,mv)
    print(f"{cid}: raw={raw} peephole={p1} dedup={p2} window={p3} record={rec} verified={v} "
          f"{'*** BEATS ***' if v and p3<rec else ('ties' if v and p3==rec else '')}")
    if v and p3<=rec:
        json.dump({"challengeId":cid,"length":p3,"record":rec,"moves":mv},
                  open(f"HIT_{cid}.json","w"))
