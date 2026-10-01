import sys, itertools
sys.path.insert(0,'/home/user/operator-first/research/acc/upgh/artifacts/t00312')
sys.path.insert(0,'/home/user/operator-first/tools/acc/upgh')
import bs_alt as B
core=B.core
INV={0:0,1:1,2:3,3:2,4:5,5:4,6:7,7:6,8:9,9:8,10:11,11:10,12:13,13:12}
def expand(frontier, seen, cap):
    nxt={}
    for s,p in frontier.items():
        for mv in range(14):
            t=core.apply_move(s,mv)
            if len(t[0])+len(t[1])>cap: continue
            if t in seen: continue
            seen[t]=p+[mv]; nxt[t]=p+[mv]
    return nxt
def mitm(src,dst,depth,cap):
    if src==dst: return []
    fs={src:[]}; bs={dst:[]}; ff={src:[]}; bf={dst:[]}
    for d in range(depth):
        ff=expand(ff,fs,cap)
        for t in ff:
            if t in bs: return fs[t]+[INV[m] for m in reversed(bs[t])]
        bf=expand(bf,bs,cap)
        for t in bf:
            if t in fs: return fs[t]+[INV[m] for m in reversed(bs[t])]
    return None
n=int(sys.argv[1]); depth=int(sys.argv[2])
m=2**(n-1)
for orient in (1,2):
    body,s=B.alt_loop(n,orient)
    f=B.fin2(m)
    # states along fin2 from FIN_ENTRY
    st=B.FIN_ENTRY(m); states=[st]
    for mv in f:
        st=core.apply_move(st,mv); states.append(st)
    cap=sum(map(len,s))+12
    print("n=%d orient %d loop-end %s %s; bridge(rot)=%s"%(n,orient,B.W(s[0]),B.W(s[1]),B.bridge(s,B.FIN_ENTRY(m))))
    for k in range(0,8):
        br=mitm(s,states[k],depth,max(cap,sum(map(len,states[k]))+6))
        print("  loop-end -> fin2 state %d: mitm %s (vs %d)"%(k, br, len(B.bridge(s,B.FIN_ENTRY(m)))+k))
    # across the rotation: state 6 -> state 6+(m-1)
    k0=6; k1=6+(m-1)
    br=mitm(states[k0],states[k1],depth,sum(map(len,states[k0]))+8)
    print("  rotation shortcut state %d -> %d: %s (rotation costs %d)"%(k0,k1,br,m-1))
    # also: state 6 -> each later state up to 6+m-1+7
    for k in range(k1, k1+8):
        br=mitm(states[k0],states[k],depth,sum(map(len,states[k0]))+8)
        if br is not None: print("  state 6 -> state %d: %d moves vs %d"%(k,len(br),k-k0))
    break
