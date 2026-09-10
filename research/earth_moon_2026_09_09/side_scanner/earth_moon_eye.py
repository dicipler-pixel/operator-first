"""Native Compound Eye Earth-Moon observers; read-only finite graph probes.

This module is the consolidated deployment of the v1.0/v1.1 development
adapters. It uses the unchanged Compound Eye machine.Registry / execute API.
Register it in a fresh focused registry or append its versioned definitions to
an existing instrument; do not replace older eye versions. Tests and scope are
recorded in SIDE_SCANNER_REPORT.md. No unbounded search or Lean proof is claimed.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib, importlib.util, json

CORE_SHA='a51d453a7489e7272a9d0300b0a72de2e39aed77ba1bb3ae4b66b496dc41d76c'

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()

def core(runtime):
    p=Path(runtime.root)/'plugins/dependencies/em19_graph_core.py'
    if hashlib.sha256(p.read_bytes()).hexdigest()!=CORE_SHA:raise ValueError('Pinned spherical core changed')
    spec=importlib.util.spec_from_file_location('em19_pinned_core',p)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def state(payload,context,runtime):
    d=payload['candidate']
    def build():
        if type(d.get('n'))is not int or d['n']!=19:raise ValueError('Exactly 19 labelled vertices required')
        c=core(runtime);layers=[]
        if 'layers'in d:
            if len(d['layers'])!=2:raise ValueError('Supply both layers')
            for t in d['layers']:c.verify_layer(19,t)
            layers=[{tuple(sorted(e))for e in t['edges']}for t in d['layers']]
            U=layers[0]|layers[1];faces=sorted([sorted([sorted(f)for f in t['faces']])for t in d['layers']]);planar='CERTIFIED_TWO_SPHERES'
        else:
            raw=d.get('edges')
            if not isinstance(raw,list)or not all(isinstance(e,list)and len(e)==2 and all(type(v)is int and 0<=v<19 for v in e)and e[0]!=e[1]for e in raw):raise ValueError('Invalid simple graph')
            U={tuple(sorted(e))for e in raw}
            if len(U)!=len(raw):raise ValueError('Duplicate edges')
            faces=[];planar='UNKNOWN_NO_LAYER_CERTIFICATE'
        ts=c.triples_slow(19,U);o=len(layers[0]&layers[1])if layers else None
        for k,v in [('independent_triples',len(ts)),('union_edges',len(U)),('overlap',o)]:
            if k in d and d[k]!=v:raise ValueError('Cached '+k+' disagrees')
        if 'remaining_triples'in d and d['remaining_triples']!=list(map(list,ts)):raise ValueError('Cached triples disagree')
        if 'partition'in d:
            parts=[{tuple(sorted(e))for e in x}for x in d['partition']]
            if len(parts)!=2 or parts[0]&parts[1]or parts[0]|parts[1]!=U or any(not parts[i]<=layers[i]for i in range(2)):raise ValueError('Invalid disjoint partition')
        key={'n':19,'faces':faces}if faces else {'n':19,'edges':sorted(U),'layers':None}
        return {'n':19,'edges':list(map(list,sorted(U))),'triples':list(map(list,ts)),'edge_count':len(U),'overlap':o,'faces':faces,'planarity':planar,'degrees':[sum(v in e for e in U)for v in range(19)],'graph_id':sha({'n':19,'edges':sorted(U)}),'state_id':sha(key),'whole_input_sha256':sha(d)}
    return runtime.shared('em_state:'+sha(d),build)

def get(payload,context,runtime,kind,fn):
    s=state(payload,context,runtime)
    return runtime.shared('em_'+kind+':'+s['state_id'],lambda:fn(s))

def identity(payload,context,deps,spec,runtime):
    s=state(payload,context,runtime)
    return {k:s[k]for k in ['state_id','graph_id','whole_input_sha256','planarity','edge_count','overlap']}|{'same_score_is_not_same_state':True,'layer_swap_quotiented':True,'vertex_relabelling_quotiented':False}

def endpoint(payload,context,deps,spec,runtime):
    s=state(payload,context,runtime);zero=not s['triples'];planar=s['planarity']=='CERTIFIED_TWO_SPHERES'
    return {'independent_triples':len(s['triples']),'union_edges':s['edge_count'],'overlap':s['overlap'],'min_degree':min(s['degrees']),'endpoint_window_100_102':100<=s['edge_count']<=102,'window_scope':'Inherited computational necessary condition ONLY for a successful 19-vertex no-independent-triple biplanar endpoint; never a move prohibition.','alpha_at_most_two':zero,'chi_at_least_ten_from_alpha':zero,'biplanar_certificate':planar,'success':zero and planar,'missing_for_target':([]if zero else ['Eliminate all independent triples'])+([]if planar else ['Supply and verify two planar edge layers'])}

def defect_support(payload,context,deps,spec,runtime):
    s=state(payload,context,runtime);ts=[tuple(t)for t in s['triples']];byedge=defaultdict(list)
    for i,t in enumerate(ts):
        for e in combinations(t,2):byedge[e].append(i)
    vertices=sorted(set(v for t in ts for v in t));remain=set(range(len(ts)));components=[]
    while remain:
        comp={min(remain)};change=True
        while change:
            change=False;vs={v for i in comp for v in ts[i]}
            for i in sorted(remain-comp):
                if vs&set(ts[i]):comp.add(i);change=True
        remain-=comp;components.append(sorted(comp))
    return {'triples':s['triples'],'support_vertices':vertices,'hypergraph_components_by_shared_vertex':components,'missing_edge_coverage':[{'edge':list(e),'triples':inds}for e,inds in sorted(byedge.items())]}

def repair_budget(payload,context,deps,spec,runtime):
    s=state(payload,context,runtime);ts=[tuple(t)for t in s['triples']]
    if len(ts)>22:return {'available':False,'reason':'Exact current-defect hitting-set cap is 22 triples; no heuristic minimum substituted'}
    masks={e:sum(1<<i for i,t in enumerate(ts)if set(e)<=set(t))for t in ts for e in combinations(t,2)}
    @lru_cache(None)
    def solve(mask):
        if not mask:return ()
        i=(mask&-mask).bit_length()-1
        choices=[(e,cover)for e,cover in masks.items()if cover>>i&1]
        return min(((e,)+solve(mask&~cover)for e,cover in sorted(choices)),key=lambda x:(len(x),x))
    chosen=solve((1<<len(ts))-1);a=len(chosen);removals=max(0,s['edge_count']+a-102)
    return {'available':True,'minimum_new_union_edges_to_hit_current_triples':a,'one_minimum_cover':list(map(list,chosen)),'free_union_slots_below_102':102-s['edge_count'],'minimum_old_union_edges_that_must_disappear':removals,'search_DP_states':solve.cache_info().currsize,'warning':'Necessary edge-edit lower bound only. It does not make added edges planar, prevent new triples on deletion, or count diagonal flips.'}

def joint_repair(payload,context,deps,spec,runtime):
    """Exact 0/1 DP; a missing edge is used at most once in its own DP layer.

    Combine covered old-triple mask and saturated per-vertex degree demands.
    Options satisfying neither demand are irrelevant. Later deletion damage is
    omitted, so this is a relaxation and a necessary endpoint edit lower bound.
    """
    def calc(s):
        ts=[tuple(t)for t in s['triples']];U=set(map(tuple,s['edges']));vs=[v for v in range(19)if s['degrees'][v]<10];req=[10-s['degrees'][v]for v in vs]
        bound=1<<len(ts)
        for d in req:bound*=d+1
        if len(ts)>12 or bound>250000:return {'available':False,'reason':'Joint exact DP declared cap exceeded; no heuristic minimum substituted','maximum_product_states':bound}
        options=[]
        for e in combinations(range(19),2):
            if e in U:continue
            cover=sum(1<<i for i,t in enumerate(ts)if set(e)<=set(t));inc=tuple(int(v in e)for v in vs)
            if cover or any(inc):options.append((e,cover,inc))
        dp={(0,tuple(0 for _ in vs)):()};examined=0
        for e,mask,inc in options:
            for (m,counts),path in list(dp.items()):
                examined+=1;key=(m|mask,tuple(min(d,x+y)for d,x,y in zip(req,counts,inc)));proposal=path+(e,)
                if key not in dp or len(proposal)<len(dp[key]):dp[key]=proposal
        path=dp.get(((1<<len(ts))-1,tuple(req)))
        if path is None:return {'available':True,'feasible_relaxation':False,'reason':'Even all missing edges cannot meet the stated relaxation'}
        a=len(path);r=max(0,s['edge_count']+a-102)
        return {'available':True,'feasible_relaxation':True,'minimum_additions_for_old_triples_and_degree':a,'minimum_old_union_edge_removals':r,'minimum_union_symmetric_difference':a+r,'deficient_vertices':[{'vertex':v,'degree':s['degrees'][v],'needed':d}for v,d in zip(vs,req)],'one_relaxed_minimizer':list(map(list,path)),'DP_final_states':len(dp),'DP_transitions':examined,'relevant_missing_edges':len(options),'scope':'Necessary editing bound for a successful 19-vertex no-independent-triple biplanar endpoint, using degree>=10 and union<=102. Added edges are not claimed simultaneously planar. Deletion damage is omitted.'}
    return get(payload,context,runtime,'joint_repair',calc)

def moves_data(s,runtime):
    if not s['faces']:return {'available':False,'reason':'No spherical layers: local flips cannot be certified'}
    c=core(runtime);ls=[c.Triangulation(19,fs)for fs in s['faces']];oldts=set(map(tuple,s['triples']));rows=[]
    for which,t in enumerate(ls):
        other=set(ls[1-which].inc)
        for k in range(len(t.edge_list)):
            rec=t.proposal(k)
            if rec is None:continue
            _,old,new,*_=rec;V=(set(t.inc)-{old}|{new})|other;newts=set(c.triples_slow(19,V));removed=sorted(oldts-newts);created=sorted(newts-oldts)
            before=tuple(t.faces);t.apply(rec);c.verify_layer(19,t.as_dict())
            if set(t.inc)|other!=V:raise AssertionError('Flip edge calculation disagrees')
            faces=sorted([sorted(map(list,x.faces))for x in ls]);childid=sha({'n':19,'faces':faces});t.undo(rec)
            if tuple(t.faces)!=before:raise AssertionError('Undo changed parent')
            rows.append({'move':{'layer':which,'remove':list(old),'insert':list(new)},'state_id':childid,'score':len(newts),'delta':len(newts)-len(oldts),'union_edges':len(V),'kills':list(map(list,removed)),'creates':list(map(list,created)),'old_edge_covered_by_other_layer':old in other,'new_edge_already_in_other_layer':new in other})
    return {'available':True,'legal_moves':len(rows),'counts_by_delta':dict(sorted(Counter(r['delta']for r in rows).items())),'min_score':min((r['score']for r in rows),default=len(oldts)),'kills_any_old_defect':sum(bool(r['kills'])for r in rows),'neutral_changes_defect_identity':sum(r['delta']==0 and bool(r['kills'])for r in rows),'moves':rows,'scope':'Complete one-legal-diagonal-flip neighborhood in these two embeddings. No longer-path exclusion.'}

def flip_damage(payload,context,deps,spec,runtime):return get(payload,context,runtime,'flips',lambda s:moves_data(s,runtime))

def colouring(payload,context,deps,spec,runtime):
    def calc(s):
        c=core(runtime);U=set(map(tuple,s['edges']));H=c.complement(19,U);witnesses=[]
        if not s['triples']:
            matching=c.maximum_matching_dp(H);covered={v for e in matching for v in e};classes=list(map(list,matching))+[[v]for v in range(19)if v not in covered]
            return {'status':'EXACT_CHROMATIC_FROM_MATCHING','chi':19-len(matching),'matching':list(map(list,matching)),'color_classes':classes,'planarity_decided_by_this_eye':False,'reason':'No independent triples, so every color class has at most two vertices'}
        for tri in s['triples']:
            keep=[v for v in range(19)if v not in tri];ids={v:i for i,v in enumerate(keep)};hh=[sum(1<<ids[w]for w in keep if H[v]>>w&1)for v in keep];pairs=c.maximum_matching_dp(hh)
            if len(pairs)==8:
                classes=[tri]+[[keep[u],keep[v]]for u,v in pairs]
                if sorted(v for C in classes for v in C)!=list(range(19))or any(tuple(sorted(e))in U for C in classes for e in combinations(C,2)):raise AssertionError('Invalid nine-color witness')
                witnesses.append({'triple':tri,'color_classes':classes})
        return {'status':'NINE_COLORING_FOUND'if witnesses else 'UNKNOWN_NOT_A_GENERAL_COLOR_SOLVER','triple_plus_pairs_witness_count':len(witnesses),'witnesses':witnesses,'tested_all_bad_triples':True,'warning':'Positive nine-color witnesses are exact. Failure of this restricted construction is not non-nine-colorability.'}
    return get(payload,context,runtime,'colouring',calc)

def lateral(payload,context,deps,spec,runtime):
    def calc(s):
        if not s['faces']:return {'available':False,'reason':'No layers to permute'}
        c=core(runtime);ls=[c.Triangulation(19,fs)for fs in s['faces']];old=set(map(tuple,s['triples']));rows=[]
        for side,t in enumerate(ls):
            other=set(ls[1-side].inc)
            for a,b in combinations(range(19),2):
                def f(v):return b if v==a else a if v==b else v
                es={tuple(sorted((f(u),f(v))))for u,v in t.inc};U=es|other;ts=set(c.triples_slow(19,U))
                rows.append({'layer':side,'swap':[a,b],'score':len(ts),'union_edges':len(U),'killed_old':len(old-ts),'created_new':len(ts-old)})
        rows.sort(key=lambda r:(r['score'],-r['killed_old'],-r['union_edges'],r['layer'],r['swap']))
        return {'available':True,'moves_evaluated':len(rows),'min_score':rows[0]['score'],'strict_improvements':sum(r['score']<len(old)for r in rows),'neutral_new_defects':sum(r['score']==len(old)and r['killed_old']>0 for r in rows),'best_moves':rows[:12],'score_histogram':dict(sorted(Counter(r['score']for r in rows).items())),'scope':'Every relative vertex transposition in either layer; planarity preserved by relabelling. Not a diagonal-flip distance or global exhaustive search.'}
    return get(payload,context,runtime,'lateral',calc)

def structural_context(payload,context,deps,spec,runtime):
    s=state(payload,context,runtime)
    if s['triples']:return {'c5_deficit_applicable':False,'reason':'The complement has triangles. Do not apply the triangle-free C5-deficit theorem or completed-window pruning to this search intermediate.'}
    c=core(runtime);H=c.complement(19,set(map(tuple,s['edges'])));ds=list(map(int.bit_count,H));found=None
    for vs in combinations(range(19),5):
        mask=sum(1<<v for v in vs)
        if all((H[v]&mask).bit_count()==2 for v in vs):found=vs;break
    if found is None:return {'c5_deficit_applicable':False,'reason':'No induced C5 found; cannot use its chart'}
    outside=[v for v in range(19)if v not in found];mask=sum(1<<v for v in found);nc=[(H[v]&mask).bit_count()for v in outside];dc=sum(2-x for x in nc);do=sum(8-ds[v]for v in outside);no9=True;counterexample=None
    for vs in combinations(range(19),9):
        if all(not(H[u]>>v&1)for u,v in combinations(vs,2)):no9=False;counterexample=list(vs);break
    return {'c5_deficit_applicable':max(ds)<=8 and max(nc)<=2,'cycle_vertices':list(found),'D_cycle':dc,'D_outside':do,'deficit_total':dc+do,'formula_rhs':150-2*(171-s['edge_count']),'max_degree_H':max(ds),'no_independent_nine_H':no9,'independent_nine_counterexample':counterexample,'warning':'Passing this chart is not a planar partition. The inherited 8044-profile proof is referenced, not rerun by this scanner.'}

def values(deps):return {k.split('@')[0].split('.')[-1]:v['value']for k,v in deps.items()}

def invariants_set(payload,context,deps,spec,runtime):
    v=values(deps);e=v['endpoint'];findings=[]
    if e['alpha_at_most_two']and not e['biplanar_certificate']:findings.append('COLOR_REQUIREMENT_PASSES_BUT_PLANAR_PARTITION_IS_MISSING')
    if not v['structural_context']['c5_deficit_applicable']:findings.append('C5_CHART_INAPPLICABLE_DO_NOT_PRUNE_BY_IT')
    return {'set':'Identity and endpoint','findings':findings,'target':e,'identity':v['identity'],'structural':v['structural_context'],'missing':e['missing_for_target'],'independent_votes':0}

def repair_set(payload,context,deps,spec,runtime):
    v=values(deps);r=v['repair_budget'];m=v['flip_damage'];joint=v['joint_repair'];findings=[]
    if joint.get('available')and joint.get('feasible_relaxation')and r.get('available')and joint['minimum_additions_for_old_triples_and_degree']>r['minimum_new_union_edges_to_hit_current_triples']:findings.append('JOINT_DEGREE_AND_DEFECT_BUDGET_STRONGER_THAN_EITHER_SCORE')
    if r['available']and r['minimum_old_union_edges_that_must_disappear']>0:findings.append('EDGE_ADDITION_ONLY_REPAIR_CANNOT_FIT_THE_ROOF')
    if m['available']and not any(x['delta']<0 for x in m['moves']):findings.append('NO_IMPROVING_SINGLE_FLIP_IN_THIS_EMBEDDING')
    if m['available']and any(x['kills']and x['delta']>0 for x in m['moves']):findings.append('TARGETED_INSERTION_CAN_DESTROY_MORE_BY_REMOVAL')
    return {'set':'Defects and replacement cost','findings':findings,'budget':r,'joint_budget':joint,'defects':v['defect_support'],'neighborhood':{k:x for k,x in m.items()if k!='moves'},'missing':['An actual accepted multi-step planar repair, not just a hitting set']if v['defect_support']['triples']else [],'independent_votes':0}

def peripheral_set(payload,context,deps,spec,runtime):
    v=values(deps);col=v['colouring'];lat=v['lateral'];findings=[]
    if col['status']=='NINE_COLORING_FOUND':findings.append('SAVED_GRAPH_STILL_HAS_EXPLICIT_NINE_COLORINGS')
    if lat.get('strict_improvements',0):findings.append('RELATIVE_RELABEL_MOVE_IMPROVES_PRIMARY_SCORE')
    return {'set':'Coloring and lateral alternatives','findings':findings,'colouring':col,'lateral':lat,'independent_votes':0}

def whole(payload,context,deps,spec,runtime):
    v=values(deps);a,b,c=v['invariants_set'],v['repair_set'],v['peripheral_set'];e=a['target'];m=b['neighborhood'];actions=[]
    if not e['biplanar_certificate']:actions.append({'priority':1,'action':'PARTITION_TEST','reason':'Zero triples and a favorable edge count do not certify thickness two. Preserve UNKNOWN until a partition or a checked exclusion exists.'})
    elif c['lateral'].get('strict_improvements',0):actions.append({'priority':1,'action':'REPLAY_LATERAL_PROPOSAL','reason':'A verified relabelling probe lowers the score; save/recheck its actual candidate before using it.'})
    elif m.get('available')and not any(int(k)<0 for k in m['counts_by_delta']):actions.append({'priority':1,'action':'COVER_REMOVAL_BEFORE_TARGET_INSERTION','reason':'The current score gives no one-flip descent. Look for setup moves protecting edges that must disappear; score both killed and newly created triples.'})
    j=b['joint_budget']
    if j.get('available')and j.get('feasible_relaxation')and j['minimum_union_symmetric_difference']:actions.append({'priority':2,'action':'JOINT_EDGE_EDIT_BUDGET','minimum_additions':j['minimum_additions_for_old_triples_and_degree'],'minimum_removals':j['minimum_old_union_edge_removals'],'minimum_symmetric_difference':j['minimum_union_symmetric_difference'],'reason':'Combine current independent triples, degree deficits and density ceiling. This is an exact necessary bound, not a path length or realizable edit.'})
    return {'schema':'compound-eye-earth-moon-whole/1.1','state_id':a['identity']['state_id'],'graph_id':a['identity']['graph_id'],'set_outputs':[a,b,c],'findings':list(dict.fromkeys(a['findings']+b['findings']+c['findings'])),'next_actions':actions,'missing':list(dict.fromkeys(a['missing']+b['missing'])),'target_success':e['success'],'main_search_mutated':False,'independent_votes':0,'coverage':'9 scoped observer eyes, three set outputs and one whole output on one identified graph. Shared computations are not independent experiments.'}
