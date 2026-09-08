"""Earth-Moon structural eyes and explicit finite certificates.

NetworkX produces planar embeddings; verify_rotation independently checks the
rotation-system Euler characteristic using integer combinatorics.
"""
from itertools import combinations
from math import ceil
import random
import networkx as nx


def edge(a,b):
    return tuple(sorted((a,b)))


def graph_edges(N, edges):
    if type(N) is not int or N < 1 or N>4096:
        raise ValueError("Vertex count must be an integer in 1..4096 for this adapter.")
    out=[]
    for e in edges:
        if not isinstance(e,(list,tuple)) or len(e)!=2 or any(type(v) is not int or v<0 or v>=N for v in e) or e[0]==e[1]:
            raise ValueError("Invalid edge endpoint or loop.")
        out.append(edge(*e))
    if len(out)!=len(set(out)):
        raise ValueError("Repeated undirected edge.")
    return set(out)


def inflation(n,r):
    if type(n) is not int or type(r) is not int or n<4 or r<1:
        raise ValueError("This cycle-inflation adapter requires integer n>=4 and r>=1.")
    N=n*r
    fibres={edge(r*i+a,r*i+b) for i in range(n) for a,b in combinations(range(r),2)}
    joins={edge(r*i+a,r*((i+1)%n)+b) for i in range(n) for a in range(r) for b in range(r)}
    return N, fibres|joins, joins


def triangle_count(N, edges):
    adj=[set() for _ in range(N)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    return sum(len(adj[a]&adj[b]) for a,b in edges)//3


def proper_coloring(N, edges, colors, k):
    return (len(colors)==N and all(type(c) is int and 0<=c<k for c in colors)
            and all(colors[a]!=colors[b] for a,b in edges))


def verify_rotation(N, edges, rotation):
    """Check a cellular orientable genus-zero embedding, component by component."""
    edges=graph_edges(N,edges)
    if {int(v) for v in rotation} != set(range(N)):
        raise ValueError("Rotation must include every vertex, including isolates.")
    rot={int(k):v for k,v in rotation.items()}
    adjacency=[set() for _ in range(N)]
    for a,b in edges:adjacency[a].add(b);adjacency[b].add(a)
    for v in range(N):
        if len(rot[v])!=len(set(rot[v])) or set(rot[v])!=adjacency[v]:
            raise ValueError("Rotation does not have exactly the graph's neighbors.")
    visited=set();components=[]
    for start in range(N):
        if start in visited:continue
        comp=set();todo=[start]
        while todo:
            v=todo.pop()
            if v in comp:continue
            comp.add(v);todo.extend(adjacency[v]-comp)
        visited|=comp
        darts={(a,b) for a in comp for b in adjacency[a]}
        left=set(darts);faces=0
        while left:
            first=next(iter(left));current=first;orbit=set()
            while current not in orbit:
                if current not in darts:raise ValueError("Invalid face orbit")
                orbit.add(current)
                a,b=current
                ring=rot[b]
                current=(b,ring[(ring.index(a)-1)%len(ring)])
            if current!=first:raise ValueError("Face traversal failed to close at its start")
            if not orbit<=left:raise ValueError("Face orbit overlap")
            left-=orbit;faces+=1
        if not darts:faces=1
        chi=len(comp)-len(darts)//2+faces
        if chi!=2:raise ValueError("Rotation has positive genus, not a planar embedding.")
        components.append({"vertices":len(comp),"edges":len(darts)//2,"faces":faces,"Euler_characteristic":chi})
    return components


def planar_certificate(N, edges):
    G=nx.Graph();G.add_nodes_from(range(N));G.add_edges_from(sorted(edges))
    ok,embedding=nx.check_planarity(G)
    if not ok:return {"planar":False,"method":"NetworkX exact graph planarity algorithm"}
    rotation={str(k):list(v) for k,v in embedding.get_data().items()}
    components=verify_rotation(N,edges,rotation)
    return {"planar":True,"rotation":rotation,"independently_checked_components":components}


def forest_layers(n):
    """Three forests of C_n[K2]. Explicit for n>=5; finite certificate at n=4."""
    N,E,_=inflation(n,2)
    if n>=5:
        rails_a={edge(2*i,2*((i+1)%n)) for i in range(n)}
        rails_b={edge(2*i+1,2*((i+1)%n)+1) for i in range(n)}
        cross={edge(2*i+a,2*((i+1)%n)+(1-a)) for i in range(n) for a in [0,1]}
        A=(rails_a|rails_b)-{edge(0,2),edge(3,5)}
        B=cross-{edge(4,7),edge(6,2*((3+1)%n)+1)}
        layers=[A,B,E-A-B]
    else:
        # Search only for a witness, never infer impossibility from failure.
        rng=random.Random(20260907)
        for _ in range(2000):
            order=list(sorted(E));rng.shuffle(order);layers=[set(),set(),set()]
            forests=[nx.Graph() for _ in range(3)]
            for F in forests:F.add_nodes_from(range(N))
            for a,b in order:
                options=[j for j in range(3) if not nx.has_path(forests[j],a,b)]
                if not options:break
                j=min(options,key=lambda j:len(layers[j]))
                layers[j].add(edge(a,b));forests[j].add_edge(a,b)
            else:break
        else:raise RuntimeError("No forest witness found in bounded search.")
    assert set.union(*layers)==E and sum(map(len,layers))==len(E)
    for layer in layers:
        F=nx.Graph();F.add_nodes_from(range(N));F.add_edges_from(layer)
        assert nx.is_forest(F)
    return layers


def three_planar_layers(n):
    # Closed 2-blowup of C_n[K2]. Internal clone edges assigned once to layer 0.
    forests=forest_layers(n)
    layers=[]
    for j,F in enumerate(forests):
        edges={edge(2*a+i,2*b+k) for a,b in F for i in [0,1] for k in [0,1]}
        if j==0:edges|={edge(2*v,2*v+1) for v in range(2*n)}
        layers.append(edges)
    N,E,_=inflation(n,4)
    assert set.union(*layers)==E and sum(map(len,layers))==len(E)
    certificates=[planar_certificate(N,F) for F in layers]
    assert all(c["planar"] for c in certificates)
    return {"layers":[[list(e) for e in sorted(F)] for F in layers],"embeddings":certificates,
            "construction":"closed 2-blowup of three explicitly checked forests of C_n[K2]"}


def full_ten_coloring():
    assigned=[[] for _ in range(7)]
    for color in range(7):
        for fibre in [(color+j)%7 for j in [0,2,4]]:assigned[fibre].append(color)
    for i in range(7):assigned[i].append(7+(i%2 if i<6 else 2))
    return [color for row in assigned for color in row]


def nine_after_join_deletion(missing):
    """Canonical missing join is (fibre6,slot0)-(fibre0,slot0).

    A four-vertex color class uses fibres 0,2,4,6; eight remaining color
    classes are independent triples of the base cycle. Multiplicities are
    (1,2,1,1,1,1,1). Rotate fibres and permute within fibres to any join edge.
    """
    a,b=missing
    fa,fb=a//4,b//4
    if (fa+1)%7==fb:prev,following=a,b
    elif (fb+1)%7==fa:prev,following=b,a
    else:raise ValueError("Not a join edge")
    colors=[None]*28
    occupied=[0]*7
    for i in [0,2,4,6]:colors[4*i]=0;occupied[i]=1
    color=1
    for j,multiplicity in enumerate([1,2,1,1,1,1,1]):
        for _ in range(multiplicity):
            for i in [(j+k)%7 for k in [0,2,4]]:
                colors[4*i+occupied[i]]=color;occupied[i]+=1
            color+=1
    assert occupied==[4]*7 and color==9
    output=[None]*28
    for i in range(7):
        target_fibre=(following//4+i)%7
        slots=list(range(4))
        special=following%4 if i==0 else prev%4 if i==6 else None
        if special is not None:slots[0],slots[special]=slots[special],slots[0]
        for j in range(4):output[4*target_fibre+slots[j]]=colors[4*i+j]
    return output


def screen(p):
    N=p["num_vertices"]
    if "edges_part1" in p or "edges_part2" in p:
        A=graph_edges(N,p["edges_part1"]);B=graph_edges(N,p["edges_part2"])
        if A&B:raise ValueError("The proposed planar parts must be disjoint.")
        E=A|B;parts=[planar_certificate(N,F) for F in [A,B]]
    else:
        E=graph_edges(N,p["edges"]);parts=None
    report={"vertices":N,"edges":len(E),"arithmetic":"exact graph incidence and counts",
            "source_target":"https://epoch.ai/frontiermath/open-problems/earth-moon",
            "official_epoch_verifier_run":False}
    rejects=[]
    report["whole_graph_density"]={"ceiling":6*N-12 if N>=3 else None,
                                   "passes_necessary_bound":len(E)<=6*N-12 if N>=3 else True}
    if N>=3 and len(E)>6*N-12:rejects.append("whole-graph Euler density")
    if "triangle_free_subgraph" in p:
        J=graph_edges(N,p["triangle_free_subgraph"])
        if not J<=E or triangle_count(N,J):raise ValueError("Proposed triangle-free subgraph is invalid.")
        report["triangle_free_subgraph"]={"edges":len(J),"triangles":0,"ceiling":4*N-8 if N>=3 else None,
                                          "excess":len(J)-(4*N-8) if N>=3 else None}
        if N>=3 and len(J)>4*N-8:rejects.append("triangle-free subgraph density")
    if parts is not None:
        report["supplied_planar_parts"]=parts
        if not all(z["planar"] for z in parts):rejects.append("a supplied layer is nonplanar")
    if "coloring" in p:
        k=p["chromatic_number"]
        if type(k) is not int or k<1:raise ValueError("Invalid claimed chromatic number")
        ok=proper_coloring(N,E,p["coloring"],k)
        report["proper_coloring"]={"colors":k,"verified":ok,"logical_role":"upper bound only"}
        if not ok:rejects.append("invalid proper coloring")
        if k<10 or k>12:rejects.append("claimed chromatic number outside target range")
    report["rejections"]=rejects
    report["status"]="rejected_for_stated_candidate" if rejects else "necessary_checks_passed_target_unresolved"
    report["scope"]="Passing density or a supplied proper coloring never proves the required chromatic lower bound. This screen does not solve arbitrary chromatic-number instances."
    return report


def main_certificate():
    N,E,J=inflation(7,4)
    colors=full_ten_coloring()
    assert proper_coloring(N,E,colors,10)
    # Exhaust all subsets of the seven fibres for the independence bound.
    independent=[]
    for mask in range(1<<7):
        S={i for i in range(7) if mask>>i&1}
        if all(not(i in S and (i+1)%7 in S) for i in range(7)):independent.append(sorted(S))
    alpha=max(map(len,independent));assert alpha==3
    deletions=[]
    for missing in sorted(J):
        nine=nine_after_join_deletion(missing)
        assert proper_coloring(N,E-{missing},nine,9)
        deletions.append({"deleted_join_edge":list(missing),"nine_coloring":nine})
    p={"num_vertices":N,"edges":[list(e) for e in sorted(E)],"triangle_free_subgraph":[list(e) for e in sorted(J)],
       "coloring":colors,"chromatic_number":10}
    return {"schema":"compound-eye-earth-moon-certificate-v1","candidate":p,"screen":screen(p),
            "independence_certificate":{"fibre_sizes":[4]*7,"all_independent_fibre_subsets":independent,
                                        "maximum_size":3,"chromatic_lower_bound":ceil(N/alpha)},
            "thickness_upper_certificate":three_planar_layers(7),
            "join_deletion_nine_colorings":deletions,
            "consequence":"Every biplanar subgraph of C7[K4] is 9-colorable: biplanarity requires omitting a join edge, and all 112 such one-edge deletions have explicit proper 9-colorings.",
            "novelty_status":"derived and verified here; no historical-priority claim",
            "epoch_target_solved":False}
