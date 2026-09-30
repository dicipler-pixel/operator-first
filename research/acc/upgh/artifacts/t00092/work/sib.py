from lib import *
import re,json
def ms(c):
    a,b=st(c)[0]
    for r0,r1 in ((a,b),(b,a)):
        m=re.fullmatch(r'(Y+)X(y+)x',S(r1))
        if m and len(m.group(1))==len(m.group(2))+1: return len(m.group(2)),S(r0)
    return None
tgt={'YYYYYxYXX','YYYYXXYYYx','YYYYxYXX','YYYYxxYX','YYYXYYxx','YYYXXYYx'}
for c in CH:
    r=ms(c)
    if r and r[1] in tgt: print(c,r)
