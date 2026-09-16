"""Independent replay of ordinary AC moves (ac-r2-v1, moves 0-13).
Written from the move definitions; shares no code with the C search engines.
Letters: 0=x 1=x^-1 2=y 3=y^-1 ; inverse = XOR 1. Target = (x, y) = ([0],[2]).
NOT the pinned SAIR verifier. See README.md 'Replay authority'."""
TARGET = ((0,), (2,))
MOVE_CLASS = {0:"inverse",1:"inverse",2:"multiply",3:"multiply",4:"multiply",5:"multiply",
              **{m:"conjugate" for m in range(6,14)}}

def free_reduce(w):
    o=[]
    for c in w:
        if o and o[-1]==(c^1): o.pop()
        else: o.append(c)
    return o

def invert(w): return [c^1 for c in reversed(w)]

def cyclic_reduce(w):
    w=free_reduce(w)
    i,j=0,len(w)
    while j-i>=2 and w[i]==(w[j-1]^1): i+=1; j-=1
    return w[i:j]

def apply_move(r0,r1,m):
    """Returns (r0,r1) after move m. Raises ValueError on an unknown move."""
    if m==0: return invert(r0), r1
    if m==1: return r0, invert(r1)
    if m==2: return free_reduce(r0+r1), r1
    if m==3: return free_reduce(r0+invert(r1)), r1
    if m==4: return r0, free_reduce(r1+r0)
    if m==5: return r0, free_reduce(r1+invert(r0))
    if 6<=m<=9:
        g=m-6;  return free_reduce([g]+r0+[g^1]), r1
    if 10<=m<=13:
        g=m-10; return r0, free_reduce([g]+r1+[g^1])
    raise ValueError(f"unknown move {m}")

def replay(r0,r1,moves):
    """Apply a whole move list. Returns (r0,r1,ok) with ok = landed on TARGET."""
    a,b=list(r0),list(r1)
    for m in moves: a,b=apply_move(a,b,m)
    return a,b,(tuple(a),tuple(b))==TARGET

def expsum(w):
    """Abelianization channel: (exponent sum in x, exponent sum in y)."""
    ex=sum(1 if c==0 else -1 if c==1 else 0 for c in w)
    ey=sum(1 if c==2 else -1 if c==3 else 0 for c in w)
    return ex,ey

def penultimate_proximity(r0,r1):
    """0 if either relator is a bare generator letter, else min |len-1| over relators."""
    if len(r0)==1 or len(r1)==1: return 0
    return min(abs(len(r0)-1), abs(len(r1)-1))
