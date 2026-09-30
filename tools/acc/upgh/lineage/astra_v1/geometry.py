"""Optional finite matrix diagnostics. These never certify or prune ACC states.

normality_energy and projector mixing are independent measurements. The factor
one eighth matches the cited connection-energy paper only under its additional
block-graph hypotheses; this module makes no claim those hold for agent traces.
"""
def mul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def adjoint(a):
    return [[complex(x).conjugate() for x in col] for col in zip(*a)]

def add(a,b,sign=1):
    return [[x+sign*y for x,y in zip(row,col)] for row,col in zip(a,b)]

def norm2(a):
    return sum(abs(x)**2 for row in a for x in row)

def diagnostics(operator,projector,tolerance=1e-10):
    n=len(operator)
    if not 1 <= n <= 64 or len(projector)!=n or any(len(r)!=n for r in operator+projector):
        raise ValueError('Supply equally sized square matrices of size 1..64.')
    if norm2(add(projector,adjoint(projector),-1))>tolerance or norm2(add(mul(projector,projector),projector,-1))>tolerance:
        raise ValueError('Pi must be an orthogonal projector within numerical tolerance.')
    identity=[[int(i==j) for j in range(n)] for i in range(n)]
    complement=add(identity,projector,-1)
    f=add(mul(mul(complement,operator),projector),mul(mul(projector,operator),complement))
    hstar=adjoint(operator)
    commutator=add(mul(operator,hstar),mul(hstar,operator),-1)
    return {'projector_mixing_squared':norm2(f),'commutator_squared':norm2(commutator),
            'normality_energy_one_eighth':norm2(commutator)/8,
            'grade':'V','scope':'finite numerical matrices only','authorizes_scoring':False}
