from replay import *
import sys
row=sys.argv[1]; idx=int(sys.argv[2])
for r, CH, S0, route, S in rows():
    if r==row: print(st(S[idx]))
