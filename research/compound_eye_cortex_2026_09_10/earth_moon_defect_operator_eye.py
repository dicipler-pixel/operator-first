#!/usr/bin/env python3
"""Generic label-preserving defect / legal-generator eye.

The eye is deliberately finite and exact:
- defects retain their labels;
- legal triangulation flips retain planarity by construction;
- the one-step move/defect operator is kept as signed support;
- rational sparse elimination tests whether the desired local correction lies
  in the linear span of the one-step effects;
- two-step enumeration measures whether setup moves unlock defects and at what
  collateral defect count.

This is a diagnostic eye, not a global existence/non-existence proof.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
import hashlib
import json


def edge(a, b):
    return (a, b) if a < b else (b, a)


def canon_face(face):
    return tuple(sorted(map(int, face)))


def canon_faces(faces):
    return tuple(sorted(canon_face(f) for f in faces))


def edges_from_faces(faces):
    out = set()
    for f in faces:
        a, b, c = map(int, f)
        out.add(edge(a, b)); out.add(edge(a, c)); out.add(edge(b, c))
    return out


def all_triples(n):
    return list(combinations(range(n), 3))


def independent_triples(n, union_edges):
    ans = []
    for a, b, c in combinations(range(n), 3):
        if edge(a, b) not in union_edges and edge(a, c) not in union_edges and edge(b, c) not in union_edges:
            ans.append((a, b, c))
    return ans


def legal_flips(faces):
    """All ordinary diagonal flips in a closed triangular complex."""
    fs = [canon_face(f) for f in faces]
    e2faces = defaultdict(list)
    for i, f in enumerate(fs):
        for a, b in combinations(f, 2):
            e2faces[edge(a, b)].append((i, f))
    E = edges_from_faces(fs)
    ans = []
    for old in sorted(e2faces):
        pair = e2faces[old]
        if len(pair) != 2:
            continue
        (i, f1), (j, f2) = pair
        a = next(x for x in f1 if x not in old)
        b = next(x for x in f2 if x not in old)
        new = edge(a, b)
        if a == b or new in E:
            continue
        ans.append({"old": old, "new": new, "face_indices": (i, j), "opposites": (a, b)})
    return ans


def apply_flip(faces, flip):
    fs = [canon_face(f) for f in faces]
    i, j = flip["face_indices"]
    u, v = flip["old"]
    a, b = flip["opposites"]
    fs[i] = canon_face((a, b, u))
    fs[j] = canon_face((a, b, v))
    return fs


def state_observables(n, layers):
    E = [edges_from_faces(layer) for layer in layers]
    U = set().union(*E)
    overlap = sum(len(E[i] & E[j]) for i in range(len(E)) for j in range(i + 1, len(E)))
    bad = independent_triples(n, U)
    return {
        "layer_edge_counts": [len(x) for x in E],
        "union_edges": len(U),
        "pairwise_overlap_sum": overlap,
        "defects": bad,
        "defect_count": len(bad),
    }


def signed_effect(base_defects, new_defects, index):
    v = {}
    for t in base_defects - new_defects:
        v[index[t]] = -1
    for t in new_defects - base_defects:
        v[index[t]] = 1
    return v


def sparse_rank(vectors):
    """Exact rational rank of sparse coordinate vectors."""
    basis = {}
    for raw in vectors:
        w = {int(k): Fraction(v) for k, v in raw.items() if v}
        for p in sorted(basis):
            if p not in w:
                continue
            factor = w[p]
            bp = basis[p]
            for k, bv in bp.items():
                nv = w.get(k, Fraction(0)) - factor * bv
                if nv:
                    w[k] = nv
                elif k in w:
                    del w[k]
        if not w:
            continue
        p = min(w)
        pivot = w[p]
        basis[p] = {k: v / pivot for k, v in w.items()}
    return len(basis)


def analyze_one_step(n, layers):
    base = state_observables(n, layers)
    base_defects = set(base["defects"])
    triples = all_triples(n)
    index = {t: i for i, t in enumerate(triples)}
    moves = []
    effects = []

    for li, layer in enumerate(layers):
        for fl in legal_flips(layer):
            new_layers = [list(map(canon_face, x)) for x in layers]
            new_layers[li] = apply_flip(new_layers[li], fl)
            obs = state_observables(n, new_layers)
            new_defects = set(obs["defects"])
            destroyed = sorted(base_defects - new_defects)
            created = sorted(new_defects - base_defects)
            effect = signed_effect(base_defects, new_defects, index)
            effects.append(effect)
            moves.append({
                "layer": li,
                "old": list(fl["old"]),
                "new": list(fl["new"]),
                "defect_count_after": obs["defect_count"],
                "destroyed": [list(t) for t in destroyed],
                "created": [list(t) for t in created],
                "union_edges_after": obs["union_edges"],
                "pairwise_overlap_sum_after": obs["pairwise_overlap_sum"],
                "signed_support_size": len(effect),
            })

    target = {index[t]: -1 for t in base_defects}
    r = sparse_rank(effects)
    r_aug = sparse_rank([*effects, target])

    per_defect = []
    for t in sorted(base_defects):
        destroyers = [i for i, effect in enumerate(effects) if effect.get(index[t], 0) == -1]
        per_defect.append({"triple": list(t), "one_step_destroyer_count": len(destroyers), "destroying_move_indices": destroyers})

    counts = Counter(m["defect_count_after"] for m in moves)
    improving = sum(1 for m in moves if m["defect_count_after"] < base["defect_count"])
    neutral = sum(1 for m in moves if m["defect_count_after"] == base["defect_count"])
    destructive_moves = [{"move_index": i, **m} for i, m in enumerate(moves) if m["destroyed"]]

    return {
        "base": {**base, "defects": [list(t) for t in base["defects"]], "triple_coordinate_count": len(triples)},
        "legal_flip_counts_by_layer": [len(legal_flips(layer)) for layer in layers],
        "legal_flip_count": len(moves),
        "one_step_min_defect_count": min((m["defect_count_after"] for m in moves), default=base["defect_count"]),
        "one_step_improving_moves": improving,
        "one_step_neutral_moves": neutral,
        "one_step_count_histogram": {str(k): counts[k] for k in sorted(counts)},
        "per_initial_defect": per_defect,
        "moves_destroying_initial_defects": destructive_moves,
        "linearized_move_defect_operator": {
            "shape": [len(triples), len(moves)],
            "exact_rank": r,
            "augmented_rank_with_desired_minus_defect": r_aug,
            "desired_minus_defect_in_linear_span": r_aug == r,
            "interpretation_scope": "one-step effects frozen at this base state only",
        },
    }


def analyze_two_step(n, layers):
    base = state_observables(n, layers)
    base_defects = set(base["defects"])
    total = 0
    nonreverse = 0
    min_all = None
    min_nonreverse = None
    support_hashes = set()
    unique_states = set()
    cheapest_remove = {t: None for t in base_defects}

    for li, layer in enumerate(layers):
        for f1 in legal_flips(layer):
            mid = [list(map(canon_face, x)) for x in layers]
            mid[li] = apply_flip(mid[li], f1)
            for lj, layer2 in enumerate(mid):
                for f2 in legal_flips(layer2):
                    total += 1
                    is_reverse = (lj == li and tuple(f2["old"]) == tuple(f1["new"]) and tuple(f2["new"]) == tuple(f1["old"]))
                    fin = [list(map(canon_face, x)) for x in mid]
                    fin[lj] = apply_flip(fin[lj], f2)
                    obs = state_observables(n, fin)
                    c = obs["defect_count"]
                    min_all = c if min_all is None else min(min_all, c)
                    if is_reverse:
                        continue
                    nonreverse += 1
                    min_nonreverse = c if min_nonreverse is None else min(min_nonreverse, c)
                    ds = tuple(sorted(obs["defects"]))
                    support_hashes.add(hashlib.sha256(repr(ds).encode()).hexdigest())
                    state_key = repr(tuple(canon_faces(x) for x in fin))
                    unique_states.add(hashlib.sha256(state_key.encode()).hexdigest())
                    dset = set(obs["defects"])
                    for t in base_defects:
                        if t in dset:
                            continue
                        prev = cheapest_remove[t]
                        candidate = {
                            "triple": list(t),
                            "defect_count_after": c,
                            "union_edges_after": obs["union_edges"],
                            "pairwise_overlap_sum_after": obs["pairwise_overlap_sum"],
                            "step1": {"layer": li, "old": list(f1["old"]), "new": list(f1["new"])},
                            "step2": {"layer": lj, "old": list(f2["old"]), "new": list(f2["new"])},
                            "defects_after": [list(x) for x in sorted(dset)],
                        }
                        if prev is None or c < prev["defect_count_after"]:
                            cheapest_remove[t] = candidate

    return {
        "two_step_sequences_including_immediate_reverse": total,
        "two_step_nonreverse_sequences": nonreverse,
        "two_step_unique_nonreverse_states": len(unique_states),
        "two_step_unique_defect_supports": len(support_hashes),
        "two_step_min_defect_count_including_reverse": min_all,
        "two_step_min_defect_count_nonreverse": min_nonreverse,
        "two_step_improves_base": min_nonreverse is not None and min_nonreverse < base["defect_count"],
        "cheapest_two_step_removal_of_each_initial_defect": [cheapest_remove[t] for t in sorted(base_defects)],
        "scope": "exhaustive ordered two-flip enumeration from the supplied base state; not a global radius proof",
    }


def audit(payload, source=None):
    n = int(payload["n"])
    layers = payload["faces"]
    if len(layers) != 2:
        raise ValueError("This control expects exactly two triangulation layers.")
    one = analyze_one_step(n, layers)
    two = analyze_two_step(n, layers)
    source = dict(source or {})
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return {
        "schema": "compound-eye-defect-generator-audit-v1",
        "status": "PASS",
        "source": {**source, "payload_sha256": hashlib.sha256(canonical).hexdigest()},
        "claim_grade": {
            "exact": ["base defect labels and counts", "legal one-flip census", "signed one-step defect effects", "exact rational rank / augmented-rank test", "ordered two-flip enumeration from this base state"],
            "not_claimed": ["global nonexistence", "radius-three exhaustion", "independence of search lineage", "a theorem about all biplanar 19-vertex graphs"],
        },
        "one_step": one,
        "two_step": two,
        "mixer_lessons": [
            "LABEL_LOSS: the scalar defect count hides which triples are locally addressable.",
            "SIGN_COLLATERAL: a move can destroy target defects while creating more elsewhere.",
            "MIXED_SCALE: one-flip, two-flip, macro/permutation, and exact-completion evidence must remain separate.",
            "SHARED_LINEAGE: many explored states from one grammar are not independent conceptual evidence.",
            "LOCAL_LINEAR_OBSTRUCTION: if augmented rank rises, the desired correction is outside the frozen one-step effect span.",
        ],
    }


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("input_json")
    p.add_argument("--out", default="earth_moon_defect_operator_eye_results.json")
    p.add_argument("--source-branch", default="")
    p.add_argument("--source-blob-sha", default="")
    args = p.parse_args()
    with open(args.input_json, "r", encoding="utf-8") as f:
        payload = json.load(f)
    result = audit(payload, {"input": args.input_json, "source_branch": args.source_branch, "source_blob_sha": args.source_blob_sha})
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True); f.write("\n")
    op = result["one_step"]["linearized_move_defect_operator"]
    print(json.dumps({"status": result["status"], "defects": result["one_step"]["base"]["defects"], "legal_flips": result["one_step"]["legal_flip_count"], "one_step_min": result["one_step"]["one_step_min_defect_count"], "rank": op["exact_rank"], "augmented_rank": op["augmented_rank_with_desired_minus_defect"], "two_step_min_nonreverse": result["two_step"]["two_step_min_defect_count_nonreverse"]}, indent=2))


if __name__ == "__main__":
    main()
