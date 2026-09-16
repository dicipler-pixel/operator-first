"""Eyes derived from the RTOE Master Index Lagrangian seed.

    L_eps(w, wdot) = 1/2 R_eps(w) ||wdot||^2 - V(w)
    R_eps(w)       = 1 / (sigma_min(A_intr(w))^2 + eps)

The transferable content is R_eps: a resistance that blows up as the smallest
singular value collapses, so motion through a degenerate region is expensive.
The AC analogue is exact and cheap -- at a given cap, a state where few of the
fourteen moves are legal is pinched, and sigma_min's role is played by the
legal-move fraction.

These are ADDITIVE. mh_eyes_v1.py is unchanged. Per the Master Index every
reading below carries a status label, and per Atlas B70 each eye answers ONE
question and is named for it.

Status labels (Master Index): PROVED, LEAN-CERTIFIED, COMPUTED, MEASURED,
HYPOTHESIS, REMEMBERED/NOT-RECOVERED, FAILED/DIVERTED.

CALIBRATION RESULT -- READ BEFORE USING
---------------------------------------
CORRIDOR_RESISTANCE is FAILED/DIVERTED as a discriminator. Measured over the
radius-3 ball of every root at its own start cap:

    root  cap  |ball|  meanR  medR   maxR   pinches(R>20)
    G6     20      55   5.34  5.42   5.42   0
    G8     24      55   5.34  5.42   5.42   0
    G10    28      55   5.34  5.42   5.42   0
    R6     20      54   5.42  5.42   5.42   0
    R7     22      54   5.42  5.42   5.42   0

Solvable controls and hard roots are indistinguishable -- same median, same
max, no pinches anywhere, ball sizes 54 against 55. At step 0 every one of
the five reads R=5.415 exactly (6 of 14 moves legal). The eye has no power to
separate a solvable root from a hard one and must NOT be used for target
selection. Contrast EXPONENT_PAIR, which separates them before any move.

It is retained because one reading did survive:

PINCH_PROFILE is MEASURED and real. Both verified Gordon paths pass through
R=46.711 at step 1 -- only 2 of 14 moves legal -- immediately after the donor
fire, then open out to R~1.0 for the remainder. That bottleneck is a genuine
structural feature of the control paths. Whether it generalises is untested.

RELATIONAL_ACTION and POTENTIAL_V are COMPUTED but uncalibrated as
discriminators; q=6 gives action 491.02 and q=8 gives 503.07, which is not a
separation. Do not promote them on this evidence.
"""
import sys
sys.path.insert(0,'/home/user/saircompetition/andrews-curtis/competition/tools')
from verifier import core

EPS = 1e-3

def legal_moves(s, cap):
    """Which of the 14 moves keep total length within cap."""
    out=[]
    for m in range(14):
        t=core.apply_move(s,m)
        if t is None: continue
        if sum(len(w) for w in t) <= cap: out.append(m)
    return out

def eye_corridor_resistance(s, cap):
    """CORRIDOR_RESISTANCE  [COMPUTED]

    R = 1/(f^2 + eps) with f the fraction of legal moves. The sigma_min
    analogue: f -> 0 is a pinch, where the corridor admits almost no motion
    and R diverges. One question: how constrained is motion HERE.
    """
    L=legal_moves(s,cap); f=len(L)/14.0
    return {"status":"COMPUTED","legal":len(L),"frac":round(f,4),
            "R":round(1.0/(f*f+EPS),3),"moves":L}

def eye_relational_action(path_states, cap):
    """RELATIONAL_ACTION  [COMPUTED]

    Discrete kinetic term sum R(s_t) * (delta total)^2 along a path. Weights
    a length change by how pinched the state was when it was made, so a jump
    taken in a tight region costs more than the same jump in an open one.
    One question: what did this path cost, resistance-weighted.
    """
    tot=lambda s: sum(len(w) for w in s)
    acc=0.0; terms=[]
    for i in range(1,len(path_states)):
        R=eye_corridor_resistance(path_states[i-1],cap)["R"]
        d=tot(path_states[i])-tot(path_states[i-1])
        term=R*d*d; acc+=term; terms.append(round(term,2))
    return {"status":"COMPUTED","action":round(acc,2),"terms":terms}

def eye_potential(s):
    """POTENTIAL_V  [COMPUTED]

    V = total length - 2, zero exactly at the target (x,y). The Lagrangian's
    V(w). One question: how far from the endpoint in the crude measure --
    deliberately crude, since Atlas B52 warns a magnitude threshold
    misclassifies where an endpoint test does not.
    """
    return {"status":"COMPUTED","V":sum(len(w) for w in s)-2}

def eye_pinch_profile(path_states, cap):
    """PINCH_PROFILE  [MEASURED]

    Where along a path the resistance spikes. Returns the argmax and the
    series. One question: which step was the bottleneck.
    """
    Rs=[eye_corridor_resistance(s,cap)["R"] for s in path_states]
    mx=max(Rs)
    return {"status":"MEASURED","max_R":mx,"at":Rs.index(mx),"series":Rs}
