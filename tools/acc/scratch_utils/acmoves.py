# Official ac-r2-v1 moves on letter strings (x,X,y,Y), free reduction only.
def red(w):
    o=[]
    for c in w:
        if o and o[-1]==c.swapcase(): o.pop()
        else: o.append(c)
    return ''.join(o)
def inv(w): return w.swapcase()[::-1]
G=['x','X','y','Y']
def move(R,m):
    a,b=R
    if m==0: return (inv(a),b)
    if m==1: return (a,inv(b))
    if m==2: return (red(a+b),b)
    if m==3: return (red(a+inv(b)),b)
    if m==4: return (a,red(b+a))
    if m==5: return (a,red(b+inv(a)))
    if 6<=m<=9: g=G[m-6]; return (red(g+a+g.swapcase()),b)
    g=G[m-10]; return (a,red(g+b+g.swapcase()))
def run(R,p,show=False):
    for i,m in enumerate(p):
        R=move(R,m)
        if show: print(f"{i+1:3d} m{m:2d} {len(R[0])+len(R[1]):3d}  {R[0]:<30s} {R[1]}")
    return R
