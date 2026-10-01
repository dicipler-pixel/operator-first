"""Commuting-pair cleanup (UPG-H song-4 rule, own implementation): a move m and a later inverse(m) cancel when every move between them
commutes with m (neither writes a relator the other reads or writes). Repeats until no pair is left. Only moves 0..13 are touched;
moves above 13 (Stable moves) are barriers that no pair crosses. Always re-verify the result with the official verifier.
Moves (ac-r2-v1): 0 inv r0 | 1 inv r1 | 2,3 r0 *= r1^(+-1) | 4,5 r1 *= r0^(+-1) | 6-9 conj r0 | 10-13 conj r1."""
INV = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)
def rw(m):
    if m in (0, 6, 7, 8, 9): return {0}, {0}
    if m in (1, 10, 11, 12, 13): return {1}, {1}
    if m in (2, 3): return {0, 1}, {0}
    return {0, 1}, {1}           # 4, 5
def commute(a, b):
    ra, wa = rw(a); rb, wb = rw(b)
    return not (wa & (rb | wb)) and not (wb & ra)
def clean(path):
    p = list(path); tail = []
    while p and p[-1] > 13: tail.insert(0, p.pop())
    changed = True
    while changed:
        changed = False
        for i in range(len(p)):
            if p[i] > 13: continue
            for j in range(i + 1, len(p)):
                if p[j] > 13: break          # Stable/other moves are barriers
                if p[j] == INV[p[i]]:
                    p = p[:i] + p[i + 1:j] + p[j + 1:]; changed = True; break
                if not commute(p[i], p[j]): break
            if changed: break
    return p + tail
if __name__ == '__main__':
    import json, sys
    print(json.dumps(clean(json.loads(sys.argv[1]))))
