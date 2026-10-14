"""Closest-approach pass for pilot keys that ran before the driver logged it: direct mode only, same W/D, min total length of the
kept beam (sampled every 10 depths) on M. usage: closest_pass.py W D REP [REP ...]"""
import sys, os, importlib.util, time, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("fs", HERE + "/firstsolve.py"); fs = importlib.util.module_from_spec(spec); spec.loader.exec_module(fs)
W, D = sys.argv[1], sys.argv[2]
for rep in sys.argv[3:]:
    t0 = time.time()
    S0 = tuple(fs.SR.w2s(r) for r in fs.SR.CH[rep]["initial_relators"]); M, _ = fs.CT.descend(S0)
    out = fs.beam(M[0], M[1], W, D)
    line = "- %s closest-approach pass (key rep %s, direct only, W %s, D %s): %s; closest total length on M %s (start %d), %ds\n" % (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%MZ"), rep, W, D, "ROAD %d" % len(out) if out else "no road", fs.beam.closest, fs.total(M), time.time() - t0)
    open(fs.R + "research/acc/live/sweeps/cov/FINDINGS_unsolved.md", "a").write(line); print(line, end="", flush=True)
