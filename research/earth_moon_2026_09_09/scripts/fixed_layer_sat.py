#!/usr/bin/env python3
"""Finite fixed-planar-layer completion; PySAT + NetworkX.

--encoding lazy uses independently checked Kuratowski-subdivision cuts.
--encoding order uses three total vertex orders (Schnyder criterion).
The encoded domain is fixed first layer + an edge-edit radius of the supplied
second layer after removing overlaps. A timeout is UNKNOWN. A planar satisfying
assignment is a candidate; fewer than five triples is not by itself chi>=10.
"""
from __future__ import annotations
import argparse,itertools,json,time,threading,hashlib,subprocess
from pathlib import Path
import networkx as nx
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType
from pysat.solvers import Solver

def edge(a,b):return tuple(sorted((a,b)))
def get_edges(fs):return {e for f in fs for e in itertools.combinations(sorted(f),2)}
def triples(n,U):return [t for t in itertools.combinations(range(n),3) if not any(e in U for e in itertools.combinations(t,2))]
def graph(n,es):
    g=nx.Graph();g.add_nodes_from(range(n));g.add_edges_from(es);return g

def kuratowski(es):
    """Certificate check by suppressing degree-two vertices, no planarity oracle."""
    adj={}
    for a,b in es:
        if a==b:raise ValueError('loop')
        adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
    while True:
        v=next((v for v in adj if len(adj[v])==2),None)
        if v is None:break
        a,b=adj.pop(v);adj[a].remove(v);adj[b].remove(v)
        if a==b or b in adj[a]:raise ValueError('not a simple subdivision core')
        adj[a].add(b);adj[b].add(a)
    if len(adj)==5 and all(len(z)==4 for z in adj.values()):return 'K5'
    if len(adj)==6 and all(len(z)==3 for z in adj.values()):
        colors={next(iter(adj)):0};todo=list(colors)
        while todo:
            u=todo.pop()
            for v in adj[u]:
                if v in colors:
                    if colors[v]==colors[u]:raise ValueError('nonbipartite cubic core')
                else:colors[v]=1-colors[u];todo.append(v)
        if len(colors)==6 and sum(colors.values())==3:return 'K33'
    raise ValueError('not a K5/K33 subdivision')

def build(n,fixed,old,bad,radius,encoding):
    pool=IDPool();options=sorted(set(itertools.combinations(range(n),2))-fixed);ev={e:pool.id(('e',e)) for e in options};clauses=[];slacks=[]
    for tri in triples(n,fixed):
        c=[ev[e] for e in itertools.combinations(tri,2)]
        if bad:
            y=pool.id(('bad',tri));slacks.append(y);c.append(y)
        clauses.append(c)
    if bad:clauses+=CardEnc.atmost(slacks,bad,vpool=pool,encoding=EncType.seqcounter).clauses
    clauses+=CardEnc.atmost(list(ev.values()),3*n-6,vpool=pool,encoding=EncType.seqcounter).clauses
    if radius<len(ev):
        differences=[-ev[e] if e in old else ev[e] for e in options]
        clauses+=CardEnc.atmost(differences,radius,vpool=pool,encoding=EncType.seqcounter).clauses
    if encoding=='order':
        order={(i,a,b):pool.id(('order',i,a,b)) for i in range(3) for a,b in itertools.combinations(range(n),2)}
        def lt(i,a,b):return order[i,a,b] if a<b else -order[i,b,a]
        for i in range(3):
            for a,b,c in itertools.combinations(range(n),3):
                x,y,z=lt(i,a,b),lt(i,b,c),lt(i,a,c);clauses.extend([[-x,-y,z],[x,y,-z]])
        for a,b in itertools.combinations(range(n),2):
            xs=[lt(i,a,b) for i in range(3)];clauses.extend([xs,[-x for x in xs]])
        # Orders themselves may be permuted; this does not relabel fixed graph vertices.
        clauses.extend([[lt(0,0,1)],[-lt(2,0,1)]])
        for (a,b),e in ev.items():
            for c in range(n):
                if c in (a,b):continue
                zz=[]
                for i in range(3):
                    z=pool.id(('above',a,b,c,i));x,y=lt(i,a,c),lt(i,b,c)
                    clauses.extend([[-z,x],[-z,y],[z,-x,-y]]);zz.append(z)
                clauses.append([-e]+zz)
    return clauses,pool,ev

def augment(n,es):
    g=graph(n,es)
    for a,b in itertools.combinations(range(n),2):
        if g.has_edge(a,b):continue
        g.add_edge(a,b)
        if not nx.check_planarity(g)[0]:g.remove_edge(a,b)
    good,emb=nx.check_planarity(g);assert good and g.number_of_edges()==3*n-6
    seen=set();faces=[]
    for a,b in emb.edges():
        if (a,b) in seen:continue
        f=emb.traverse_face(a,b,seen);assert len(f)==3;faces.append(sorted(f))
    assert len(faces)==2*n-4
    return {'edges':sorted([list(edge(a,b)) for a,b in g.edges()]),'faces':sorted(faces)}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--side',type=int,choices=[0,1],default=0);p.add_argument('--bad',type=int,default=4);p.add_argument('--radius',type=int,default=8);p.add_argument('--encoding',choices=['lazy','order'],default='lazy');p.add_argument('--seconds',type=float,default=240);p.add_argument('--models',type=int,default=20000);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    fs=[list(map(int,l.split())) for l in a.input.read_text().splitlines() if l.strip()];assert len(fs)==68 and all(len(f)==3 for f in fs)
    n=19;layers=[get_edges(fs[:34]),get_edges(fs[34:])];assert all(nx.check_planarity(graph(n,s))[0] and len(s)==51 for s in layers)
    fixed=layers[a.side];old=layers[1-a.side]-fixed
    # Independent positive and negative theory controls.
    assert kuratowski(list(nx.complete_graph(5).edges()))=='K5';assert kuratowski(list(nx.complete_bipartite_graph(3,3).edges()))=='K33'
    try:kuratowski(list(nx.cycle_graph(6).edges()))
    except ValueError:pass
    else:raise AssertionError('planar false witness accepted')
    clauses,pool,ev=build(n,fixed,old,a.bad,a.radius,a.encoding);base=len(clauses);cuts=[];start=time.monotonic();status='UNKNOWN_LIMIT';models=0;candidate=None
    CNF(from_clauses=clauses).to_file(str(a.out/'initial.cnf'))
    with Solver(name='g4',bootstrap_with=clauses) as solver:
        solver.set_phases([v if e in old else -v for e,v in ev.items()]);timer=threading.Timer(a.seconds,solver.interrupt);timer.daemon=True;timer.start()
        try:
            while models<a.models and time.monotonic()-start<a.seconds:
                sat=solver.solve_limited(expect_interrupt=True)
                if sat is None:break
                if sat is False:status='UNSAT_SOLVER';break
                models+=1;model=set(v for v in solver.get_model() if v>0);es={e for e,v in ev.items() if v in model};missing=triples(n,fixed|es)
                assert len(missing)<=a.bad and len(es)<=51 and len(old^es)<=a.radius
                good,witness=nx.check_planarity(graph(n,es),counterexample=a.encoding=='lazy')
                if good:
                    aa=augment(n,fixed);bb=augment(n,es);U={tuple(x) for x in aa['edges']}|{tuple(x) for x in bb['edges']};ts=triples(n,U)
                    candidate={'n':19,'layers':[aa,bb],'independent_triples':len(ts),'remaining_triples':ts,'union_edges':len(U),'overlap':len(aa['edges'])+len(bb['edges'])-len(U),'metadata':{'fixed_side':a.side,'bad_bound':a.bad,'edit_radius':a.radius,'encoding':a.encoding,'partial_second_edges':sorted(es),'edit_distance':len(es^old)}}
                    (a.out/'candidate.json').write_text(json.dumps(candidate,indent=2)+'\n');status='SAT_PLANAR';break
                if a.encoding=='order':raise AssertionError('order SAT assignment not planar')
                ws=sorted(edge(x,y) for x,y in witness.edges());assert set(ws)<=es
                core=kuratowski(ws);cut=[-ev[e] for e in ws];solver.add_clause(cut);clauses.append(cut);cuts.append({'edges':ws,'core':core})
                if models%100==0:
                    print('models',models,'cuts',len(cuts),'seconds',time.monotonic()-start,flush=True)
                    (a.out/'partial.json').write_text(json.dumps({'models':models,'cuts':len(cuts),'status':'RUNNING'}))
        finally:timer.cancel()
        stats=solver.accum_stats()
    CNF(from_clauses=clauses).to_file(str(a.out/'final.cnf'));(a.out/'cuts.json').write_text(json.dumps(cuts,separators=(',',':'))+'\n')
    proof_lines=0
    if status=='UNSAT_SOLVER':
        # Re-solve the final, fixed formula so every theory cut is an explicit input.
        with Solver(name='g4',bootstrap_with=clauses,with_proof=True) as check:
            timer=threading.Timer(90,check.interrupt);timer.daemon=True;timer.start()
            try:again=check.solve_limited(expect_interrupt=True)
            finally:timer.cancel()
            if again is False:
                pr=check.get_proof();proof_lines=len(pr);(a.out/'proof.drup').write_text('\n'.join(pr)+'\n');status='UNSAT_PROOF_LOGGED'
    report={'status':status,'scope':'fixed supplied planar layer, second-layer symmetric-edge-difference radius after overlaps removed','fixed_side':a.side,'bad_bound':a.bad,'radius':a.radius,'encoding':a.encoding,'edge_variables':len(ev),'all_variables':pool.top,'base_clauses':base,'models_tested':models,'verified_Kuratowski_cuts':len(cuts),'proof_lines':proof_lines,'proof_checked':False,'seconds':time.monotonic()-start,'stats':stats,'zero_candidate':candidate is not None and candidate['independent_triples']==0,'global_earth_moon_unsat':False,'input_sha256':hashlib.sha256(a.input.read_bytes()).hexdigest()}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
