"""Driver for the compiled bidirectional corridor engine."""
import json, subprocess, sys, os
SAIR="/home/user/saircompetition/andrews-curtis"
ENG=os.path.join(os.path.dirname(os.path.abspath(__file__)),"corridor64bi2")
DIG={1:0,-1:1,2:2,-2:3}          # engine packs 2 bits: 0=x 1=X 2=y 3=Y
_MAN=None
def manifest():
    global _MAN
    if _MAN is None:
        _MAN={c["challenge_id"]:c for c in json.load(
            open(f"{SAIR}/competition/tools/verifier/data/manifest.json"))["challenges"]}
    return _MAN
def digits(word): return [DIG[c] for c in word]
def run(challenge_id, cap, budget, timeout=900):
    ch=manifest()[challenge_id]
    r0,r1=ch["initial_relators"]; t0,t1=ch["target_relators"]
    argv=[ENG,str(cap),str(budget),
          str(len(r0)),*map(str,digits(r0)), str(len(r1)),*map(str,digits(r1)),
          str(len(t0)),*map(str,digits(t0)), str(len(t1)),*map(str,digits(t1))]
    p=subprocess.run(argv,capture_output=True,text=True,timeout=timeout)
    out=p.stdout.strip().splitlines()
    head=out[0] if out else "NO_OUTPUT"
    moves=None
    for l in out:
        if l.startswith("MOVES"):
            moves=[int(x) for x in l.split()[1:]]
    return {"challenge_id":challenge_id,"cap":cap,"budget":budget,
            "verdict":head.split()[0] if head else "NO_OUTPUT","head":head,"moves":moves}
