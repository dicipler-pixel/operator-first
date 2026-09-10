#!/usr/bin/env python3
"""Closed-sphere face operations and certificate core.

Extracted without mathematical changes from EM19_QUADFLIP_03.py (SHA256
023d0fd19be4bd526c5e43c0f035f0af823262e91089c493471ae635e419a526).
This is the reusable verification core, not the original full annealer.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict, deque
from functools import lru_cache
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import sys
import time

N = 19
Edge = tuple[int, int]
Face = tuple[int, int, int]

def edge(a: int, b: int) -> Edge:
    return (a, b) if a < b else (b, a)

def fedges(f: Face) -> tuple[Edge, Edge, Edge]:
    a, b, c = f
    return (edge(a,b), edge(b,c), edge(c,a))

class Triangulation:
    """Unoriented face complex; independent verification constructs orientation."""
    def __init__(self, n: int, faces: list[Face]):
        self.n = n
        self.faces = [tuple(sorted(f)) for f in faces]
        self.inc: dict[Edge, list[int]] = {}
        for i, f in enumerate(self.faces):
            for e in fedges(f):
                self.inc.setdefault(e, []).append(i)
        self.edge_list = sorted(self.inc)

    @classmethod
    def stacked(cls, n: int, seed: int) -> Triangulation:
        if n < 4:
            raise ValueError('A closed simplicial sphere starts with K4: n >= 4.')
        rng = random.Random(seed)
        order = list(range(n)); rng.shuffle(order)
        faces = sorted(itertools.combinations(order[:4],3))
        faces = [tuple(sorted(f)) for f in faces]
        for v in order[4:]:
            i = rng.randrange(len(faces))
            a,b,c = faces[i]
            faces[i] = tuple(sorted((v,a,b)))
            faces.extend([tuple(sorted((v,b,c))), tuple(sorted((v,c,a)))])
        return cls(n, faces)

    def proposal(self, k: int):
        """Return a legal flip without mutating. Invalid proposals are self-loops."""
        old = self.edge_list[k]
        i,j = self.inc[old]
        f,g = self.faces[i], self.faces[j]
        u,v = old
        a = next(x for x in f if x != u and x != v)
        b = next(x for x in g if x != u and x != v)
        new = edge(a,b)
        if a == b or new in self.inc:
            return None
        return (k, old, new, i, j, f, g)

    def apply(self, rec) -> None:
        k, old, new, i, j, f, g = rec
        u,v = old; a,b = new
        for ix, ff in ((i,f),(j,g)):
            for e in fedges(ff):
                self.inc[e].remove(ix)
                if not self.inc[e]: del self.inc[e]
        self.faces[i] = tuple(sorted((u,a,b)))
        self.faces[j] = tuple(sorted((v,a,b)))
        for ix in (i,j):
            for e in fedges(self.faces[ix]):
                self.inc.setdefault(e, []).append(ix)
        self.edge_list[k] = new

    def undo(self, rec) -> None:
        k, old, new, i, j, f, g = rec
        for ix in (i,j):
            for e in fedges(self.faces[ix]):
                self.inc[e].remove(ix)
                if not self.inc[e]: del self.inc[e]
        self.faces[i],self.faces[j] = f,g
        for ix,ff in ((i,f),(j,g)):
            for e in fedges(ff):
                self.inc.setdefault(e, []).append(ix)
        self.edge_list[k] = old

    def as_dict(self) -> dict:
        return {'edges': [list(e) for e in sorted(self.inc)],
                'faces': [list(f) for f in sorted(self.faces)]}


def complement(n: int, union: set[Edge]) -> list[int]:
    h = [((1<<n)-1) ^ (1<<v) for v in range(n)]
    for a,b in union:
        h[a] &= ~(1<<b); h[b] &= ~(1<<a)
    return h


def triples_slow(n: int, union: set[Edge]) -> list[tuple[int,int,int]]:
    return [(a,b,c) for a,b,c in itertools.combinations(range(n),3)
            if (a,b) not in union and (a,c) not in union and (b,c) not in union]


def triangles_fast(h: list[int]) -> int:
    total = 0
    for a,mask in enumerate(h):
        neighbors = mask >> (a+1) << (a+1)
        while neighbors:
            bit = neighbors & -neighbors; neighbors ^= bit
            b = bit.bit_length()-1
            total += (h[a] & h[b]).bit_count()
    return total//3


def graph_key(layers: list[Triangulation]) -> tuple:
    """Includes faces/layer assignment, not just union, for finite repair states."""
    data = [tuple(sorted(t.faces)) for t in layers]
    # Exact tuple equality prevents any hash-collision-based identification.
    # Layer interchange is a valid symmetry; vertex relabeling is NOT done here.
    return tuple(sorted(data))


def snapshot(layers: list[Triangulation], meta: dict | None = None) -> dict:
    n = layers[0].n
    es = [set(t.inc) for t in layers]
    union = es[0] | es[1]
    missing = triples_slow(n,union)
    return {'format':'EM19-QUADFLIP-03','n':n,
            'status':'candidate_lower_bound' if not missing else 'near_miss',
            'independent_triples':len(missing),'remaining_triples':[list(x) for x in missing],
            'overlap':len(es[0]&es[1]),'union_edges':len(union),
            'layers':[t.as_dict() for t in layers],
            'partition':[[list(e) for e in sorted(es[0])],
                         [list(e) for e in sorted(es[1]-es[0])]],
            'metadata':meta or {}}


def connected(adj: dict[int,set[int]], vertices: set[int]) -> bool:
    if not vertices: return False
    todo = [next(iter(vertices))]; seen=set(todo)
    while todo:
        v=todo.pop()
        for w in adj.get(v,set()):
            if w not in seen: seen.add(w); todo.append(w)
    return seen==vertices


def verify_layer(n: int, data: dict) -> dict:
    """From scratch: closed connected orientable simplicial surface with chi=2.

    Checks vertex links, not only Euler/edge counts. This is a spherical
    embedding certificate, using the standard classification of surfaces.
    No dependence on the flip engine's adjacency maps or cached counts.
    """
    def require(condition, message):
        if not condition: raise ValueError(message)
    raw_edges = data['edges']; raw_faces = data['faces']
    require(all(len(e)==2 for e in raw_edges),'invalid edge shape')
    require(all(len(f)==3 for f in raw_faces),'invalid face shape')
    require(all(isinstance(v,int) and not isinstance(v,bool) and 0<=v<n
                for e in raw_edges for v in e),'invalid edge vertex')
    require(all(isinstance(v,int) and not isinstance(v,bool) and 0<=v<n
                for f in raw_faces for v in f),'invalid face vertex')
    es = {edge(*e) for e in raw_edges}
    fs = [tuple(sorted(f)) for f in raw_faces]
    require(all(a!=b for a,b in es),'edge loop')
    require(all(len(set(f))==3 for f in fs),'degenerate face')
    require(len(es)==len(raw_edges),'duplicate edge')
    require(len(set(fs))==len(fs),'duplicate face')
    require(len(es)==3*n-6 and len(fs)==2*n-4,'wrong counts')
    inc = defaultdict(list); adj=defaultdict(set)
    for i,f in enumerate(fs):
        for e in itertools.combinations(f,2): inc[e].append(i)
    require(set(inc)==es,'face edges disagree with supplied edges')
    require(all(len(ids)==2 for ids in inc.values()),'an edge lacks two faces')
    for a,b in es: adj[a].add(b);adj[b].add(a)
    require(connected(adj,set(range(n))),'disconnected graph or missing vertex')
    for v in range(n):
        link=defaultdict(set)
        for f in fs:
            if v in f:
                a,b=[x for x in f if x!=v]
                link[a].add(b);link[b].add(a)
        require(set(link)==adj[v],'invalid vertex link support')
        require(all(len(z)==2 for z in link.values()),'vertex link not 2-regular')
        require(connected(link,set(link)),'disconnected vertex link')
    def direction(f,e):
        a,b,c=f
        return 1 if e in ((a,b),(b,c),(c,a)) else -1
    signs={0:1}; todo=[0]
    while todo:
        i=todo.pop()
        for e in itertools.combinations(fs[i],2):
            f0,f1=inc[e]; j=f1 if f0==i else f0
            expected=-signs[i]*direction(fs[i],e)*direction(fs[j],e)
            if j in signs: require(signs[j]==expected,'nonorientable face complex')
            else: signs[j]=expected;todo.append(j)
    require(len(signs)==len(fs),'disconnected dual')
    require(n-len(es)+len(fs)==2,'wrong Euler characteristic')
    return {'vertices':n,'edges':len(es),'faces':len(fs),'spherical_embedding':True}


def maximum_matching_dp(h: list[int]) -> list[Edge]:
    """Exact matching on <=19 vertices by vertex-subset DP; no blossom library."""
    @lru_cache(None)
    def solve(mask: int):
        if not mask: return ()
        bit=mask&-mask; v=bit.bit_length()-1; rest=mask^bit
        best=solve(rest)
        choices=h[v]&rest
        while choices:
            b=choices&-choices;choices^=b; w=b.bit_length()-1
            candidate=((v,w),)+solve(rest^b)
            if len(candidate)>len(best): best=candidate
        return best
    return list(solve((1<<len(h))-1))


def verify(data: dict) -> dict:
    n=data['n']
    if not isinstance(n,int) or n<4: raise ValueError('invalid n')
    if len(data['layers'])!=2: raise ValueError('two layers required')
    reports=[verify_layer(n,t) for t in data['layers']]
    es=[{edge(*e) for e in t['edges']} for t in data['layers']]
    union=es[0]|es[1]; ts=triples_slow(n,union)
    stats={'independent_triples':len(ts),'overlap':len(es[0]&es[1]),'union_edges':len(union)}
    for k,v in stats.items():
        if data.get(k)!=v: raise ValueError('cached value mismatch: '+k)
    if data.get('remaining_triples')!=[list(x) for x in ts]:
        raise ValueError('remaining-triples list mismatch')
    if 'partition' in data:
        pp=[{edge(*e) for e in p} for p in data['partition']]
        if len(pp)!=2 or pp[0]&pp[1] or pp[0]|pp[1]!=union:
            raise ValueError('not a disjoint partition of the union')
        if not pp[0]<=es[0] or not pp[1]<=es[1]:
            raise ValueError('partition not contained in certified layers')
    if stats['union_edges'] != 6*n-12-stats['overlap']:
        raise ValueError('inclusion-exclusion failure')
    result={'verified':True,'layers':reports,**stats,
            'zero_triples':not ts,'remaining_triples':[list(t) for t in ts]}
    if not ts:
        matching=maximum_matching_dp(complement(n,union))
        colors=[list(e) for e in matching]
        used={v for e in matching for v in e}
        colors.extend([[v] for v in range(n) if v not in used])
        result.update({'chromatic_number':n-len(matching),'maximum_complement_matching':matching,
                       'proper_color_classes':colors,'lower_bound_from_alpha':(n+1)//2})
    else:
        result['warning']='Near miss only. No >=10-chromatic conclusion.'
    return result


