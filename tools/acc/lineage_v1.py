#!/usr/bin/env python3
# SCRIPT: lineage
"""lineage v1 — chronological build lineage and capability regression matrix,
DERIVED from the repository and the event ledger, never hand-maintained.

A hand-typed lineage launders an assertion into a reviewer-facing fact. This one
cannot, because every row cites where it came from: the frozen instrument's own
manifest and release notes, the import-validation record, and the append-only
event stream. Where two eyes disagree about a build, BOTH are printed with the
contradiction named -- the matrix never silently picks a winner.

    python3 tools/acc/lineage_v1.py --write   # regenerate the markdown
    python3 tools/acc/lineage_v1.py --check   # fail if the checked-in copy is stale
"""
import json, os, re, subprocess, sys, argparse, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT  = os.path.join(ROOT, "tools", "acc", "LINEAGE_v1.md")

def read(p, default=""):
    try:
        with open(os.path.join(ROOT, p), encoding="utf-8") as f: return f.read()
    except OSError: return default

def git(*a):
    try:
        return subprocess.run(["git"]+list(a), cwd=ROOT, capture_output=True,
                              text=True, timeout=30).stdout.strip()
    except Exception: return ""

def manifest_releases():
    try:
        m = json.loads(read("tools/compound-eye/UNIVERSAL_MANIFEST.json"))
        return m.get("release"), m.get("source_releases", []), m.get("scope","")
    except Exception: return None, [], ""

def versions_seen():
    """Every build string the frozen instrument mentions -- the instrument is the
    source of truth for its own lineage."""
    out = subprocess.run(
        ["grep","-rhoE",r"(Universal|Canonical|UPG|Eye Mixer)[ _-]?[0-9]+\.[0-9]+(\.[0-9]+)?",
         os.path.join(ROOT,"tools","compound-eye")],
        capture_output=True, text=True)
    vs = sorted(set(x.strip() for x in out.stdout.splitlines() if x.strip()))
    def key(v):
        nums = [int(n) for n in re.findall(r"\d+", v)]
        return (v.split()[0], nums)
    return sorted(vs, key=key)

def hashes_from_import_validation():
    txt = read("tools/acc/MIXER_5_1_IMPORT_VALIDATION.md")
    rows = []
    for m in re.finditer(r"\|\s*(\S+\.(?:html|zip))\s*\|\s*`([0-9a-f]{64})`", txt):
        rows.append((m.group(1), m.group(2)))
    return rows

def ledger_capability_claims():
    """Capability observations about builds, with their contradictions intact."""
    claims, contras = [], []
    p = os.path.join(ROOT, "ledger", "events", "stream_v1.jsonl")
    if not os.path.exists(p): return claims, contras
    for line in open(p, encoding="utf-8"):
        try: e = json.loads(line)
        except Exception: continue
        b = e.get("body", {})
        if e.get("kind") == "eye-reading" and isinstance(b.get("output"), dict) \
           and "pre-ledger" in str(b["output"].get("about","")):
            claims.append({"seq": e.get("seq"), "eye": b.get("eye_id"),
                           "state": b.get("state"), "value": b["output"].get("value",""),
                           "basis": b["output"].get("basis","")})
        if e.get("kind") == "eye-reading" and str(b.get("eye_id","")).startswith("contradiction:"):
            contras.append({"seq": e.get("seq"), "id": b.get("eye_id"),
                            "body": b.get("output", {})})
    return claims, contras

def recorder_properties():
    """Properties the recorder claims, paired with the test that tries to break
    each one. Derived from the test files actually present."""
    props = [
        ("tamper-evident",  "hash chain; editing any event breaks every later link",
         "test_event_log_v1.py", "tamper"),
        ("torn-write safe", "one fsynced line under flock; a kill mid-append leaves a short line",
         "test_event_log_v1.py", "torn"),
        ("concurrent safe", "appends take flock(LOCK_EX); writers interleave records not bytes",
         "test_event_log_v1.py", "concurren"),
        ("exactly typed",   "unsafe integers rejected recursively over the whole event",
         "test_event_log_v1.py", "unsafe"),
    ]
    rows = []
    for name, how, testfile, needle in props:
        txt = read(f"tools/acc/{testfile}")
        n = len(re.findall(needle, txt, re.I))
        rows.append((name, how, testfile if n else "—", n))
    return rows

def build(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    rel, srcs, scope = manifest_releases()
    vs = versions_seen()
    hs = hashes_from_import_validation()
    claims, contras = ledger_capability_claims()
    props = recorder_properties()

    L = []
    w = L.append
    w("# Compound Eye — build lineage and regression matrix")
    w("")
    w("**GENERATED — do not hand-edit.** Regenerate with")
    w("`python3 tools/acc/lineage_v1.py --write`; CI may assert freshness with `--check`.")
    w("")
    w("A hand-typed lineage launders an assertion into a fact. Every row below names")
    w("where it came from. Where two eyes disagree about a build, both are printed and")
    w("the contradiction is named; this table never silently picks a winner.")
    w("")
    w("## 1. Chronological lineage")
    w("")
    w(f"Frozen instrument manifest reports release **{rel}**, built from source releases "
      f"**{', '.join(srcs) if srcs else '—'}**.")
    w(f"Manifest scope, in its own words: *{scope}*")
    w("")
    w("| build | evidence it exists |")
    w("|---|---|")
    for v in vs:
        w(f"| `{v}` | string present in the frozen instrument tree |")
    w("")
    if hs:
        w("Content hashes recorded at import validation (the package itself is a private")
        w("working instrument and is deliberately not committed):")
        w("")
        w("| artifact | sha256 |")
        w("|---|---|")
        for n, h in hs: w(f"| `{n}` | `{h}` |")
        w("")
    w("## 2. Capability regression matrix")
    w("")
    w("Rows are capability claims about the pre-ledger builds, taken verbatim from the")
    w("event stream. `state` is the eye's own recorded state — a contradicted eye keeps")
    w("its observation, it is not deleted.")
    w("")
    if claims:
        w("| seq | eye | state | claim | basis |")
        w("|---|---|---|---|---|")
        for c in claims:
            w(f"| {c['seq']} | `{c['eye']}` | {c['state']} | {c['value'][:120]} | {c['basis'][:120]} |")
    else:
        w("*(no capability claims found in the ledger)*")
    w("")
    if contras:
        w("### Open contradictions")
        w("")
        for c in contras:
            b = c["body"] or {}
            w(f"- **{c['id']}** (seq {c['seq']}) — disagreement on *{b.get('disagree_on','?')}*; "
              f"resolved: **{b.get('resolved')}**")
            for side in ("side_a","side_b"):
                s = b.get(side) or {}
                if s: w(f"  - `{s.get('eye')}` (seq {s.get('seq')}): {str(s.get('value'))[:160]}")
            if b.get("note"): w(f"  - note: {b['note'][:300]}")
        w("")
    w("## 3. Recorder property matrix")
    w("")
    w("Each property is paired with the test that tries to break it. A property with no")
    w("test is worth nothing, so the count of matching test references is shown.")
    w("")
    w("| property | how it is enforced | test file | references |")
    w("|---|---|---|---|")
    for name, how, tf, n in props:
        w(f"| {name} | {how} | `{tf}` | {n} |")
    w("")
    w("## 4. Provenance of this file")
    w("")
    # Deliberately NO repo HEAD and NO event count here. Both change on every
    # commit, so embedding them would make --check fail perpetually -- a freshness
    # gate that can never be satisfied is worse than no gate. The event count is
    # pinned separately in ledger/events/COUNT_FLOOR, which is its proper home.
    w("- sources read: `tools/compound-eye/UNIVERSAL_MANIFEST.json`, the frozen instrument tree,")
    w("  `tools/acc/MIXER_5_1_IMPORT_VALIDATION.md`, `ledger/events/stream_v1.jsonl`")
    w("- the frozen instrument is READ ONLY here; nothing under `tools/compound-eye/` is written")
    text = "\n".join(L) + "\n"

    if a.check:
        cur = read("tools/acc/LINEAGE_v1.md")
        if cur.strip() != text.strip():
            print("lineage: LINEAGE_v1.md is stale — run tools/acc/lineage_v1.py --write")
            return 1
        print("lineage: up to date"); return 0
    if a.write:
        with open(OUT, "w", encoding="utf-8") as f: f.write(text)
        print(f"lineage: wrote {os.path.relpath(OUT, ROOT)} ({len(text)} bytes)")
        return 0
    sys.stdout.write(text); return 0

if __name__ == "__main__":
    raise SystemExit(build())
