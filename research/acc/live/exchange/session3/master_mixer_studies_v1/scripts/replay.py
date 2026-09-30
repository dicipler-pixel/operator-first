# SCRIPT: ACC_REPLAY_SHIM  free reduction for letters 0=x 1=X 2=y 3=Y (inverse = c^1), as whitehead.py expects
def free_reduce(w):
    o=[]
    for c in w:
        if o and o[-1]==(c^1): o.pop()
        else: o.append(c)
    return o
