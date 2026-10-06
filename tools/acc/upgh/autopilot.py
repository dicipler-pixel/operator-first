#!/usr/bin/env python3
"""Autopilot: the team's cheapest scorers, run unattended on the owner's PC (no model, no API calls, no ledger writes).

Each round: git pull -> height web -> Stable web -> recognition web (-> twist web every --twist-every rounds) -> plan_offline on
everything they wrote -> ACC_SUBMIT_OWNER_PC_<UTC>.txt with only the lines that score against the newest board in the repo ->
git commit + push of the outputs (so UPG-H sees them at its check-in). A new round starts only when new roads arrived (the webs are
a fixed point of what we already hold), checked every --poll minutes.

Needs: Python 3.9+, git, this repo checked out on branch claude/gallant-bardeen-0pgpae. Nothing to compile. The pinned official
verifier (github.com/SAIRcompetition/Andrews-Curtis @ the commit in config.json, about 23 MB) is cloned on first run.

usage:  python3 tools/acc/upgh/autopilot.py                 # loop forever (Ctrl+C to stop)
        python3 tools/acc/upgh/autopilot.py --once          # one round
        python3 tools/acc/upgh/autopilot.py --no-push       # keep results local
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PY = sys.executable
BRANCH = "claude/gallant-bardeen-0pgpae"
CFG = json.loads((HERE / "config.json").read_text())
CACHE = Path(os.environ.get("UPGH_CACHE") or CFG.get("cache_dir", "~/.cache/upgh")).expanduser()
SAIR = Path(os.environ.get("SAIR_REPO") or CACHE / "sair").expanduser()
INBOX = REPO / "research/acc/live/inbox"


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%MZ")


def log(msg):
    print("[%s] %s" % (utc(), msg), flush=True)


def run(cmd, timeout=None, quiet=False):
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=timeout)
    if not quiet and p.returncode != 0:
        log("command failed (%d): %s\n%s" % (p.returncode, " ".join(map(str, cmd)), (p.stdout + p.stderr)[-800:]))
    return p


def ensure_verifier():
    sair = CFG["sair"]
    if not (SAIR / ".git").is_dir():
        SAIR.parent.mkdir(parents=True, exist_ok=True)
        log("cloning the official verifier into %s" % SAIR)
        subprocess.run(["git", "clone", "-q", sair["url"], str(SAIR)], check=True)
    head = subprocess.run(["git", "-C", str(SAIR), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if head != sair["commit"]:
        subprocess.run(["git", "-C", str(SAIR), "fetch", "-q", "origin"], check=False)
        subprocess.run(["git", "-C", str(SAIR), "checkout", "-q", sair["commit"]], check=True)
    os.environ["SAIR_REPO"] = str(SAIR)
    os.environ["SAIR"] = str(SAIR)


def roads_signature():
    """Changes when any road source the webs read changes (inbox, queue, sweeps, ledger)."""
    h = hashlib.sha256()
    pats = ["research/acc/live/inbox/*.txt", "research/acc/live/queue/**/*.txt", "research/acc/live/sweeps/**/*.txt",
            "research/acc/upgh/ledger.jsonl"]
    for pat in pats:
        for f in sorted(glob.glob(str(REPO / pat), recursive=True)):
            if "/pc_" in f.replace("\\", "/"):
                continue
            st = os.stat(f)
            h.update(("%s %d %d" % (f, st.st_size, int(st.st_mtime))).encode())
    return h.hexdigest()


def git_pull():
    p = run(["git", "pull", "-q", "--no-edit", "origin", BRANCH], quiet=True)
    if p.returncode != 0:
        log("git pull failed (working offline this round): %s" % (p.stdout + p.stderr).strip()[-300:])


def web(script, out, extra=(), timeout=3600):
    t = time.time()
    p = run([PY, str(HERE / script), *extra, "--out", str(out)], timeout=timeout)
    lines = [l for l in p.stdout.splitlines() if "RECORD" in l or "AT/UNDER" in l or "FIRST" in l or "TIE" in l or "BEAT" in l]
    log("%s done in %.0fs%s" % (script, time.time() - t, (": " + "; ".join(lines[:6])) if lines else ""))
    return out if out.exists() else None


def plan(files, stamp):
    """plan_offline on every web output; keep only scoring lines (TIE / BEAT / first solve)."""
    keep = {}
    for f in files:
        tmp = REPO / ("research/acc/live/inbox/pc_plan_%s_%s" % (stamp, f.name))
        p = run([PY, str(REPO / "tools/acc/plan_offline.py"), str(f), "--sair", str(SAIR), "--out", str(tmp)], timeout=1200)
        if tmp.exists():
            for line in tmp.read_text().splitlines():
                if line.startswith(("ac-", "sac-")):
                    cid, path = line.split(":", 1)
                    path = path.strip().replace(" ", "")
                    if cid not in keep or path.count(",") < keep[cid].count(","):
                        keep[cid] = path
            tmp.unlink()
        for l in p.stdout.splitlines():
            if "TIE" in l or "BEAT" in l or "UNSOLVED" in l:
                log("  " + l.strip())
    return keep


def push(paths, msg):
    run(["git", "add", *map(str, paths)], quiet=True)
    if run(["git", "diff", "--cached", "--quiet"], quiet=True).returncode == 0:
        return
    run(["git", "commit", "-q", "-m", msg + " [skip ci]"])
    for i in range(4):
        if run(["git", "push", "-q", "origin", "HEAD:" + BRANCH], quiet=True).returncode == 0:
            log("pushed: " + msg)
            return
        git_pull()
        time.sleep(2 ** (i + 1))
    log("push failed; results stay local in the repo folder")


def one_round(n, args):
    stamp = utc()
    INBOX.mkdir(parents=True, exist_ok=True)
    outs = [web("height_web.py", INBOX / ("pc_height_%s.txt" % stamp)),
            web("stable_web.py", INBOX / ("pc_stable_%s.txt" % stamp)),
            web("recognition_web.py", INBOX / ("pc_recognition_%s.txt" % stamp), ["--deadline-min", str(args.recog_min)])]
    if args.twist_every and n % args.twist_every == 0:
        outs.append(web("twist_web.py", INBOX / ("pc_twist_%s.txt" % stamp), ["--rows", "all"], timeout=4 * 3600))
    outs = [o for o in outs if o]
    keep = plan(outs, stamp)
    written = list(outs)
    if keep:
        owner = REPO / ("ACC_SUBMIT_OWNER_PC_%s.txt" % stamp)
        owner.write_text("".join("%s: %s\n" % (c, keep[c]) for c in sorted(keep)))
        written.append(owner)
        log("SCORING LINES: %d -> %s (UPG-H re-checks them against the live board before you submit)" % (len(keep), owner.name))
    else:
        log("no scoring lines this round")
    if args.push and written:
        push(written, "autopilot (owner PC): round %d, %d road files, %d scoring lines" % (n, len(outs), len(keep)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--no-push", dest="push", action="store_false")
    ap.add_argument("--poll", type=float, default=30, help="minutes between checks for new roads")
    ap.add_argument("--twist-every", type=int, default=3, help="run the (slow, ~25 min) twist web every N rounds; 0 = never")
    ap.add_argument("--recog-min", type=float, default=30, help="time cap for the recognition web, minutes")
    args = ap.parse_args()
    ensure_verifier()
    n, last = 0, None
    while True:
        git_pull()
        sig = roads_signature()
        if sig != last:
            n += 1
            log("round %d: new roads since the last round, running the webs" % n)
            one_round(n, args)
            last = roads_signature()
        else:
            log("no new roads; next check in %.0f min" % args.poll)
        if args.once:
            break
        time.sleep(args.poll * 60)


if __name__ == "__main__":
    main()
