"""tail_for_id.py OUT K [K ...] -> full tail (moves from echo state K to (x,y)): reverse of the C-recorded src->x path, then the route tail."""
import sys, json, struct
INV = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12}
def tails(out, ids):
    sm = json.load(open(out + '.srcmap.json')); meta = open(out + '.meta', 'rb'); res = {}
    for k in ids:
        meta.seek(7 * k); sr, dp, pa = struct.unpack('<HBI', meta.read(7))
        fwd = [(pa >> (4 * j)) & 15 for j in range(dp)]      # moves src -> x
        b, ri, i = sm['sources'][sr]
        res[k] = [INV[m] for m in reversed(fwd)] + sm['routes'][ri][i:]
    return res
if __name__ == '__main__':
    print(json.dumps(tails(sys.argv[1], [int(a) for a in sys.argv[2:]])))
