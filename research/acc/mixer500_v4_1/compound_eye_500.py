#!/usr/bin/env python3
"""
Compound Eye 500 v4.1 — raw-first generic retina engine (per-column eyes, target excluded)
Jeromie N. Beasley research instrument

Order is enforced:
1. parse and freeze raw numeric input
2. run every compatible v4 generic eye independently
3. save all eye traces
4. compute redundancy/novelty/stability statistics
5. combine only after the raw-eye ledger exists

The 191 inherited eyes stay in the catalog but are NOT falsely executed by this
generic engine. Their original adapters/kernels remain separate.
"""
from pathlib import Path
import argparse, csv, json, math, hashlib, statistics, random

ROOT = Path(__file__).resolve().parent
REGISTRY = json.loads((ROOT/"catalog"/"eyes_500.json").read_text(encoding="utf-8"))

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20), b""): h.update(b)
    return h.hexdigest()

def isnum(x):
    try:
        y=float(x); return math.isfinite(y)
    except Exception:
        return False

def load_matrix(path):
    path=Path(path)
    suf=path.suffix.lower()
    rows=[]
    headers=None
    if suf==".csv":
        with path.open(newline="",encoding="utf-8-sig") as f:
            rr=list(csv.reader(f))
        if not rr: return [],[]
        # header if any first-row item is nonnumeric
        if any(not isnum(x) for x in rr[0]):
            headers=rr[0]; rr=rr[1:]
        for r in rr:
            vals=[float(x) if isnum(x) else float("nan") for x in r]
            rows.append(vals)
    elif suf in (".json",".jsonl"):
        if suf==".jsonl":
            data=[json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        else:
            data=json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data,dict):
                # choose first list-like payload
                for v in data.values():
                    if isinstance(v,list): data=v; break
        if data and isinstance(data[0],dict):
            keys=sorted({k for d in data for k,v in d.items() if isnum(v)})
            headers=keys
            rows=[[float(d.get(k,float("nan"))) if isnum(d.get(k)) else float("nan") for k in keys] for d in data]
        elif data and isinstance(data[0],(list,tuple)):
            rows=[[float(x) if isnum(x) else float("nan") for x in r] for r in data]
        else:
            rows=[[float(x)] for x in data if isnum(x)]
    else:
        for line in path.read_text(encoding="utf-8",errors="ignore").splitlines():
            toks=re_split(line)
            nums=[float(t) for t in toks if isnum(t)]
            if nums: rows.append(nums)
    if not rows: return [],[]
    width=max(len(r) for r in rows)
    for r in rows: r.extend([float("nan")]*(width-len(r)))
    if headers is None: headers=[f"c{i}" for i in range(width)]
    else:
        headers=list(headers)+[f"c{i}" for i in range(len(headers),width)]
    return headers,rows

def re_split(line):
    out=[]; cur=""
    for ch in line:
        if ch in ",\t ;":
            if cur: out.append(cur); cur=""
        else: cur+=ch
    if cur: out.append(cur)
    return out

def finite_col(rows,j):
    return [r[j] if j<len(r) and math.isfinite(r[j]) else float("nan") for r in rows]

def median(vals):
    a=sorted(v for v in vals if math.isfinite(v))
    if not a: return 0.0
    n=len(a); return a[n//2] if n%2 else 0.5*(a[n//2-1]+a[n//2])

def preprocess(x,kind):
    vals=[v for v in x if math.isfinite(v)]
    mu=sum(vals)/len(vals) if vals else 0.0
    sd=(sum((v-mu)**2 for v in vals)/max(1,len(vals)-1))**0.5 if len(vals)>1 else 0.0
    med=median(vals)
    out=[]
    prev=float("nan"); prev2=float("nan")
    ranks={}
    if kind=="rank":
        ss=sorted(set(vals))
        ranks={v:(ss.index(v)/(max(1,len(ss)-1))) for v in ss}
    for v in x:
        if not math.isfinite(v): out.append(float("nan")); continue
        if kind=="identity": y=v
        elif kind=="center": y=v-mu
        elif kind=="zscore": y=(v-mu)/(sd if sd>0 else 1.0)
        elif kind=="abs": y=abs(v)
        elif kind=="square": y=v*v
        elif kind=="signed_sqrt": y=math.copysign(math.sqrt(abs(v)),v)
        elif kind=="rank": y=ranks[v]
        elif kind=="local_residual": y=v-med
        elif kind=="log1p_abs": y=math.copysign(math.log1p(abs(v)),v)
        elif kind=="first_difference":
            y=(v-prev) if math.isfinite(prev) else 0.0
        elif kind=="second_difference":
            y=(v-2*prev+prev2) if math.isfinite(prev) and math.isfinite(prev2) else 0.0
        else: y=v
        out.append(y); prev2,prev=prev,v
    return out

def window_vals(x,i,w):
    a=max(0,i-w+1)
    return [v for v in x[a:i+1] if math.isfinite(v)]

def summarize_trace(x,w,kind):
    out=[]
    for i,v in enumerate(x):
        a=window_vals(x,i,w)
        if not a: out.append(float("nan")); continue
        if kind=="value": y=v
        elif kind=="rolling_mean": y=sum(a)/len(a)
        elif kind=="rolling_std":
            m=sum(a)/len(a); y=(sum((q-m)**2 for q in a)/max(1,len(a)-1))**0.5
        elif kind=="rolling_min": y=min(a)
        elif kind=="rolling_max": y=max(a)
        elif kind=="rolling_l1": y=sum(abs(q) for q in a)
        elif kind=="rolling_l2": y=math.sqrt(sum(q*q for q in a))
        elif kind=="rolling_range": y=max(a)-min(a)
        elif kind=="slope": y=(a[-1]-a[0])/max(1,len(a)-1)
        elif kind=="curvature": y=(a[-1]-2*a[-2]+a[-3]) if len(a)>=3 else 0.0
        elif kind=="sign_balance": y=sum(1 if q>0 else -1 if q<0 else 0 for q in a)/len(a)
        elif kind=="zero_crossing":
            y=sum(1 for u,z in zip(a,a[1:]) if u*z<0)/max(1,len(a)-1)
        elif kind=="lag1_product":
            y=sum(u*z for u,z in zip(a,a[1:]))/max(1,len(a)-1)
        else: y=v
        out.append(y)
    return out

def pearson(a,b):
    pairs=[(x,y) for x,y in zip(a,b) if math.isfinite(x) and math.isfinite(y)]
    if len(pairs)<3: return 0.0
    xs=[p[0] for p in pairs]; ys=[p[1] for p in pairs]
    mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
    vx=sum((x-mx)**2 for x in xs); vy=sum((y-my)**2 for y in ys)
    if vx<=0 or vy<=0: return 0.0
    return sum((x-mx)*(y-my) for x,y in pairs)/math.sqrt(vx*vy)

def roughness(a):
    q=[x for x in a if math.isfinite(x)]
    if len(q)<2:return 0.0
    return sum(abs(b-a) for a,b in zip(q,q[1:]))/(len(q)-1)

def run(inp,outdir,target_column=None):
    inp=Path(inp); out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
    headers,rows=load_matrix(inp)
    if not rows: raise SystemExit("No numeric data found.")
    raw_manifest={"source":str(inp),"sha256":sha256(inp),"rows":len(rows),"columns":len(headers),"headers":headers}
    (out/"RAW_INPUT_MANIFEST.json").write_text(json.dumps(raw_manifest,indent=2),encoding="utf-8")

    target=None
    if target_column:
        if target_column in headers:
            target=finite_col(rows,headers.index(target_column))
        else:
            try: target=finite_col(rows,int(target_column))
            except: raise SystemExit("target column not found")

    generic=[e for e in REGISTRY if e.get("execution_status_v4")=="implemented" and "generic_spec" in e]
    # v4.1 repair (2026-09-13): eyes are emitted per (view, feature column); the target column is
    # never part of an eye's input; each trace records its exact source column for provenance.
    target_idx=None
    if target_column:
        target_idx=headers.index(target_column) if target_column in headers else int(target_column)
    feature_cols=[j for j in range(len(headers)) if j!=target_idx]
    led=[]
    traces={}
    generic_instances=[]
    raw_path=out/"EYES_ALL_RAW.jsonl"
    resumed=False
    if raw_path.exists() and (out/"INDIVIDUAL_EYE_SUMMARY.json").exists():
        try:
            prev=json.loads((out/"INDIVIDUAL_EYE_SUMMARY.json").read_text(encoding="utf-8"))
            for line in raw_path.read_text(encoding="utf-8").splitlines():
                d=json.loads(line); traces[d["id"]]=d["trace"]
            if all(x["id"] in traces for x in prev) and prev and "source_column" in prev[0]:
                led=prev; generic_instances=[{k:x[k] for k in ("id","view_id","kernel_group","source_column","source_column_index")} for x in prev]
                resumed=True; print(f"resumed {len(led)} eye instances from {raw_path}")
        except Exception as ex:
            print("resume failed, recomputing:", ex); led=[]; traces={}; generic_instances=[]
    for e in ([] if resumed else generic):
        spec=e["generic_spec"]
        for j in feature_cols:
            x=preprocess(finite_col(rows,j),spec["preprocess"])
            tr=summarize_trace(x,spec["window"],spec["summary"])
            eid=f'{e["id"]}@{headers[j]}'
            inst={"id":eid,"view_id":e["id"],"kernel_group":e["kernel_group"],"source_column":headers[j],"source_column_index":j}
            generic_instances.append(inst)
            traces[eid]=tr
            vals=[v for v in tr if math.isfinite(v)]
            rec=dict(inst)
            rec.update({"n_finite":len(vals),
                "mean":sum(vals)/len(vals) if vals else None,
                "std":statistics.pstdev(vals) if len(vals)>1 else 0.0,
                "roughness":roughness(tr),
                "target_abs_correlation":abs(pearson(tr,target)) if target is not None else None})
            led.append(rec)
    generic=generic_instances

    # Authority point: write all individual traces before any mixer statistics.
    if not resumed:
        with (out/"EYES_ALL_RAW.jsonl").open("w",encoding="utf-8") as f:
            for e in generic:
                f.write(json.dumps({"id":e["id"],"kernel_group":e["kernel_group"],"trace":traces[e["id"]]},separators=(",",":"))+"\n")
        (out/"INDIVIDUAL_EYE_SUMMARY.json").write_text(json.dumps(led,indent=2),encoding="utf-8")

    # Redundancy/novelty mixer statistics (v4.1): computed with numpy over the full
    # instance set when available; exact all-pairs, NaN-aware via pairwise-complete rows.
    mix=[]
    ids=[e["id"] for e in generic]
    try:
        import numpy as np
        X=np.array([traces[i] for i in ids],dtype=float)          # eyes x rows
        ok=np.isfinite(X)
        Xz=np.where(ok,X,0.0)
        cnt=ok.astype(float)@ok.astype(float).T
        sx=Xz@ok.astype(float).T; sy=ok.astype(float)@Xz.T
        sxx=(Xz*Xz)@ok.astype(float).T; syy=ok.astype(float)@(Xz*Xz).T
        sxy=Xz@Xz.T
        with np.errstate(invalid="ignore",divide="ignore"):
            cov=sxy-sx*sy/np.maximum(cnt,1)
            vx=sxx-sx*sx/np.maximum(cnt,1); vy=syy-sy*sy/np.maximum(cnt,1)
            R=np.abs(cov/np.sqrt(vx*vy))
        R[~np.isfinite(R)]=0.0; R[cnt<3]=0.0
        np.fill_diagonal(R,0.0)
        best=R.argmax(axis=1); bestv=R.max(axis=1)
        for i,a in enumerate(generic):
            score=led[i]["target_abs_correlation"] if target is not None else None
            mix.append({"id":a["id"],"view_id":a["view_id"],"source_column":a["source_column"],"kernel_group":a["kernel_group"],
                "max_abs_correlation_to_other_eye":float(bestv[i]),
                "most_redundant_partner":ids[int(best[i])] if bestv[i]>0 else None,
                "novelty":1.0-float(bestv[i]),
                "target_abs_correlation":score})
        _R=R
    except ImportError:
        _R=None
        for i,a in enumerate(generic):
            best_red=0.0; best_partner=None
            for j,b in enumerate(generic):
                if j==i: continue
                r=abs(pearson(traces[a["id"]],traces[b["id"]]))
                if r>best_red: best_red=r; best_partner=b["id"]
            score=led[i]["target_abs_correlation"] if target is not None else None
            mix.append({"id":a["id"],"view_id":a["view_id"],"source_column":a["source_column"],"kernel_group":a["kernel_group"],
                "max_abs_correlation_to_other_eye":best_red,
                "most_redundant_partner":best_partner,
                "novelty":1.0-best_red,
                "target_abs_correlation":score})
    (out/"MIXING_STATS.json").write_text(json.dumps(mix,indent=2),encoding="utf-8")

    # Greedy diverse panel: target-aware if target supplied, otherwise novelty-first.
    remaining=mix[:]; panel=[]
    remaining.sort(key=lambda z: ((z["target_abs_correlation"] or 0.0) if target is not None else z["novelty"]),reverse=True)
    for cand in remaining:
        if len(panel)>=32: break
        if not panel:
            panel.append(cand); continue
        maxr=max((float(_R[ids.index(cand["id"]),ids.index(p["id"])]) if _R is not None else abs(pearson(traces[cand["id"]],traces[p["id"]]))) for p in panel)
        utility=(cand["target_abs_correlation"] or 0.0) if target is not None else cand["novelty"]
        if maxr<0.97 or (utility>0.95 and maxr<0.999):
            x=dict(cand); x["max_abs_corr_to_selected"]=maxr; panel.append(x)
    (out/"DIVERSE_PANEL.json").write_text(json.dumps(panel,indent=2),encoding="utf-8")

    inherited_count=sum(1 for e in REGISTRY if e["origin"].startswith("Compound Eye Universal"))
    report={
        "registered_eyes":len(REGISTRY),
        "inherited_catalog_entries":inherited_count,
        "new_generic_executable_views":len({e["view_id"] for e in generic}),
        "generic_eye_instances_per_column":len(generic),
        "feature_columns":[headers[j] for j in range(len(headers)) if j!=target_idx],
        "new_unique_kernel_groups":len(set(e["kernel_group"] for e in generic)),
        "raw_rows":len(rows),"raw_columns":len(headers),
        "target_column":target_column,
        "order_enforced":["RAW_INPUT_MANIFEST","EYES_ALL_RAW","INDIVIDUAL_EYE_SUMMARY","MIXING_STATS","DIVERSE_PANEL"],
        "warning":"500 registered views do not equal 500 independent experiments. Kernel groups are reported explicitly."
    }
    (out/"RUN_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("outdir")
    ap.add_argument("--target-column",default=None,help="optional CSV/JSON numeric target column name or index")
    a=ap.parse_args()
    run(a.input,a.outdir,a.target_column)
