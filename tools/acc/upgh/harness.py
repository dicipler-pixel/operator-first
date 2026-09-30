"""UPG-H v2 controller. Code decides dispatch; models advise; the pinned verifier certifies.

One step of the loop (map §3), as implemented:
  1  Pi       a task contract names rows, strategy, limits and the only directory it may write
  2  licence  pins intact, not stopped, board fresh enough for the action -> else refuse (ledger line)
  3  M        fold the ledger; is this row+family already hot or parked?
  4  Phi      a switch counts only when a scoring-complement coordinate changes
  5  execute  code runner or agent, with lease + heartbeat
  6  harvest  every path in the artifacts, checked by official verifier + independent kernel
  7  Z        path.best / miss.parked / task.closed lines, fsynced
  8  grade    V for checked replay, C for SAIR data, H for model text
  9  clocks   board, history, skew and lease are checked one by one before any plan
"""
from __future__ import annotations

import contextlib
import fcntl
import json
import os
import re
import secrets
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import harvest as harvest_mod  # noqa: E402
import observe  # noqa: E402
import sources  # noqa: E402
from checker import Checker, PinError, moves_sha  # noqa: E402
from ledger import Ledger, sha256_bytes, sha256_file, canon  # noqa: E402
from state import PHI_COORDS, ROLES, fold, family, phi_changes, wake_key  # noqa: E402

REPO = HERE.parents[2]
KINDS = {"builder": ("ran", "blocked"), "checker": ("review", "blocked"),
         "advisor": ("proposal", "blocked"), "memory": ("context", "blocked")}
NEVER = ["submit to SAIR", "git push", "edit or delete ledger lines", "write outside artifacts_dir",
         "start background jobs that outlive the lease"]


class Refused(Exception):
    """A fail-closed refusal. Its ledger line is already written."""


class Harness:
    def __init__(self, config_path=None, state_dir=None, repo=None):
        self.repo = Path(repo or REPO).resolve()
        self.config_path = Path(config_path or HERE / "config.json")
        self.cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.state_dir = Path(state_dir or self.repo / self.cfg["state_dir"]).resolve()
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.cache = Path(os.environ.get("UPGH_CACHE") or self.cfg["cache_dir"]).expanduser()
        self.sair_dir = Path(os.environ.get("SAIR_REPO") or self.cache / "sair").expanduser()
        self.ledger = Ledger(self.state_dir / "ledger.jsonl")
        self._checker = None
        self.now = time.time  # tests may replace

    # -- plumbing ----------------------------------------------------------------
    def _rel(self, path) -> str:
        try:
            return Path(path).resolve().relative_to(self.repo).as_posix()
        except ValueError:
            return str(path)

    @contextlib.contextmanager
    def control(self):
        with open(self.state_dir / "controller.lock", "a+b") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)

    def state(self):
        return fold(self.ledger.events())

    @property
    def checker(self) -> Checker:
        if self._checker is None:
            self._checker = Checker(self.sair_dir, self.cfg["sair"]["pins"], self.cfg["sair"]["commit"])
        return self._checker

    def _refuse(self, action, species, reason):
        self.ledger.append("refusal", {"action": action, "species": species, "reason": reason}, "V")
        raise Refused("%s refused [%s]: %s" % (action, species, reason))

    def _licence(self, action, st, *, allow_stopped=False):
        if st.stopped and not allow_stopped:
            self._refuse(action, "stop", "harness is stopped (%s); `upgh resume` is a human decision"
                         % st.stop_reason)
        problems = self.checker.pin_problems()
        if problems:
            self._refuse(action, "licence", "; ".join(problems))

    def _stop_file(self):
        return self.state_dir / "STOP"

    def _next_tid(self, st, offset=0):
        return "t%05d" % (len(st.tasks) + 1 + offset)

    def _boards(self, st):
        out = {}
        for problem, snap in st.boards.items():
            path = self.repo / snap["file"]
            if path.is_file() and sha256_file(path) == snap["sha256"]:
                out[problem] = sources.load_board(path)
        return out

    def _clocks(self, st):
        return observe.clock_report(st, self.cfg, self.now())

    # -- setup -------------------------------------------------------------------
    def setup(self, build_t9=False, compile_tools=True):
        """Clone and pin the official verifier, compile search tools, check T9. Idempotent."""
        sair = self.cfg["sair"]
        log = []
        if not self.sair_dir.is_dir():
            self.sair_dir.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "clone", "-q", sair["url"], str(self.sair_dir)], check=True)
            log.append("cloned " + sair["url"])
        head = subprocess.run(["git", "-C", str(self.sair_dir), "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
        if head != sair["commit"]:
            subprocess.run(["git", "-C", str(self.sair_dir), "checkout", "-q", sair["commit"]], check=True)
            log.append("checked out " + sair["commit"][:7])
        problems = self.checker.pin_problems()
        bindir = self.cache / "bin"
        if compile_tools:
            bindir.mkdir(parents=True, exist_ok=True)
            for tool in ("acc_beam", "acc_window", "acc_capped"):
                src = self.repo / "research/acc/optimality" / (tool + ".c")
                stamp = bindir / (tool + ".src.sha256")
                have = stamp.read_text().strip() if stamp.exists() else None
                if not (bindir / tool).exists() or have != sha256_file(src):
                    tmp = bindir / (tool + ".new")
                    subprocess.run(["gcc", "-O3", "-march=native", "-Wno-misleading-indentation", "-o",
                                    str(tmp), str(src), "-lm"], check=True)
                    os.replace(tmp, bindir / tool)   # a running lane keeps the old inode
                    stamp.write_text(sha256_file(src) + "\n")
                    log.append("compiled %s from source %s" % (tool, sha256_file(src)[:12]))
        t9 = self.cache / "T9.tab"
        if build_t9 and not t9.exists():
            subprocess.run(["bash", str(self.repo / "tools/acc/build_T9.sh"), str(self.cache)],
                           check=True, cwd=self.repo)
            log.append("built T9.tab")
        t9_state = "missing (run `upgh setup --t9`, about 3 minutes, 4.5 GB)"
        if t9.exists():
            t9_state = "present (%d bytes)" % t9.stat().st_size
            if build_t9 or not self.cfg.get("skip_t9_hash"):
                t9_state += ", sha256 %s" % ("ok" if sha256_file(t9) == self.cfg["t9_sha256"] else "MISMATCH")
        entry = {"sair_commit": sair["commit"], "sair_dir": str(self.sair_dir), "pins_ok": not problems,
                 "problems": problems, "config_sha256": sha256_file(self.config_path),
                 "kernel": "upgh.kernel (independent, from published move tables)", "t9": t9_state}
        st = self.state()
        if st.setup != entry:
            self.ledger.append("setup", entry, "V")
        return {"log": log, **entry}

    # -- evidence ------------------------------------------------------------------
    def _check_paths(self, st, found, source, all_paths=False):
        """found: list of (cid, moves, where). Returns (events, improved, invalid, disagree, unique, checked).
        Harvest checks only paths that could change the fold; task output is checked in full."""
        unique = {}
        for cid, moves, where in found:
            key = (cid, moves_sha(moves))
            if key not in unique:
                unique[key] = (cid, moves, where)
        # only paths that could change the fold: shorter than our best, or first for the row
        todo = [(c, m, w) for (c, sha), (c, m, w) in unique.items()
                if all_paths or ("%s:%s" % (c, sha[:16]) not in st.known_invalid
                                 and (c not in st.best or len(m) < st.best[c]["length"]))]
        todo.sort(key=lambda x: (x[0], len(x[1])))
        receipts = self.checker.check([(c, m) for c, m, _ in todo]) if todo else []
        events, improved, invalid, disagree = [], {}, [], []
        best_len = {c: b["length"] for c, b in st.best.items()}
        for (cid, moves, where), r in zip(todo, receipts):
            src = {**source, "where": where}
            if not r["agree"]:
                d = {"cid": cid, "moves": moves, "source": src, "official": r["official"], "kernel": r["kernel"]}
                disagree.append(d)
                events.append(("path.disagree", d, "V"))
            elif not r["ok"]:
                invalid.append({"cid": cid, "length": len(moves), "moves_sha": r["moves_sha"],
                                "source": src, "code": r["official"].get("code")})
            elif cid not in best_len or len(moves) < best_len[cid]:
                prev = best_len.get(cid)
                best_len[cid] = len(moves)
                improved[cid] = {"cid": cid, "track": r["track"], "moves": moves, "length": len(moves),
                                 "moves_sha": r["moves_sha"], "prev_length": prev, "source": src,
                                 "official": r["official"], "kernel": r["kernel"], "agree": True}
        events += [("path.best", d, "V") for d in improved.values()]
        return events, improved, invalid, disagree, len(unique), len(todo)

    def harvest(self, files=None):
        """Scan configured files (or the given ones) and write Z for anything new and better."""
        with self.control():
            st = self.state()
            self._licence("harvest", st, allow_stopped=True)  # writing Z is allowed while stopped
            h = self.cfg["harvest"]
            paths = [Path(f).resolve() for f in files] if files else harvest_mod.scan(
                self.repo, h["globs"], h["exclude"])
            if not files:   # outputs of runs still in progress, or of lanes that died mid-run (S4)
                paths += sorted((self.cache / "running").glob("*/out.jsonl"))
            found = []
            for p in paths:
                rel = self._rel(p)
                found += [(c, m, "%s:%s" % (rel, w)) for c, m, w in harvest_mod.extract(p)]
            events, improved, invalid, disagree, n_unique, n_checked = self._check_paths(
                st, found, {"kind": "harvest"})
            # exact construction from checked AC paths only: P gives the Stable AC path P + [16, 15]
            ac_best = {c: b["moves"] for c, b in st.best.items() if c.startswith("ac-")}
            ac_best.update({c: d["moves"] for c, d in improved.items() if c.startswith("ac-")})
            sac_len = {c: b["length"] for c, b in st.best.items() if c.startswith("sac-")}
            sac_len.update({c: d["length"] for c, d in improved.items() if c.startswith("sac-")})
            derived = [("sac-" + c.split("-")[1], m + [16, 15], "derived: %s + [16,15]" % c)
                       for c, m in ac_best.items() if len(m) + 2 < sac_len.get("sac-" + c.split("-")[1], 10 ** 9)]
            if derived:
                ev2, imp2, inv2, dis2, _, n2 = self._check_paths(st, derived, {"kind": "derived"})
                events += ev2
                improved.update(imp2)
                invalid += inv2
                disagree += dis2
                n_checked += n2
            stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(self.now()))
            art = self.state_dir / "harvests" / ("harvest_%s.json" % stamp)
            art.parent.mkdir(parents=True, exist_ok=True)
            art.write_text(json.dumps({"files": [self._rel(p) for p in paths], "invalid": invalid,
                                       "improved": sorted(improved)}, indent=1) + "\n", encoding="utf-8")
            summary = {"files": len(paths), "found": len(found), "unique": n_unique, "checked": n_checked,
                       "improved": len(improved), "invalid": len(invalid), "disagree": len(disagree),
                       "invalid_keys": sorted("%s:%s" % (d["cid"], d["moves_sha"][:16]) for d in invalid),
                       "newest_mtime": harvest_mod.newest_mtime(paths), "at_epoch": self.now(),
                       "report": {"path": self._rel(art), "sha256": sha256_file(art)}}
            events.append(("harvest", summary, "V"))
            events += self._wake_events(st, [{"event": "new_path", "row": c} for c in sorted(improved)],
                                        offset=0, exclude_task=None)
            events += self._disagree_tasks(st, disagree, offset=self._pending_offset(events))
            self.ledger.append_many(events)
            return {k: v for k, v in summary.items() if k != "invalid_keys"}

    def _pending_offset(self, events):
        return sum(1 for k, _, _ in events if k == "task.opened")

    def _disagree_tasks(self, st, disagree, offset):
        if not disagree:
            return []
        tid = self._next_tid(st, offset)
        rows = sorted({d["cid"] for d in disagree})
        contract = {"task": tid, "role": "checker", "rows": rows,
                    "why": "official verifier and independent kernel disagree (S1: one present, two readings)",
                    "items": disagree[:20], "limits": {"wall_seconds": 900},
                    "workspace": self._workspace(tid)}
        return [("task.opened", contract, "V")]

    # -- SAIR data -------------------------------------------------------------------
    def board(self):
        """Pull both boards and our full history (read-only). Emits board_changed wakes for parked rows."""
        with self.control():
            st = self.state()
            cache = self.state_dir / "cache"
            snaps = sources.pull_boards(cache / "boards")
            prev = st.history if (st.history and st.history.get("max_submission_id") is not None
                                  and self.now() - st.history["pulled_at"] < 86400) else None
            hist = sources.pull_history(cache / "history", previous=prev)
            for s in snaps:
                s["file"] = self._rel(Path(s["file"]))
            hist["file"] = self._rel(Path(hist["file"]))
            events = [("board.snapshot", s, "C") for s in snaps] + [("history.snapshot", hist, "C")]
            # rows whose record moved, for rows that have parked misses
            wakes = []
            parked_rows = {p["row"] for p in st.parked.values()}
            if parked_rows:
                old = self._boards(st)
                for s in snaps:
                    new = sources.load_board(self.repo / s["file"])
                    for cid in parked_rows & set(new):
                        before = old.get(s["problem"], {}).get(cid)
                        if before is not None and before != new[cid]:
                            wakes.append({"event": "board_changed", "row": cid})
            events += self._wake_events(st, wakes, offset=0, exclude_task=None)
            self.ledger.append_many(events)
            return {"boards": snaps, "history": {k: v for k, v in hist.items() if k != "best"},
                    "wakes": len(wakes)}

    def import_boards(self):
        """Adopt boards the team's sair_api.py already pulled. Zero API calls."""
        with self.control():
            st = self.state()
            live = self.repo / "research/acc/live/boards"
            events = []
            for problem in ("ac", "stable_ac"):
                snap = sources.newest_live_board(live, problem)
                cur = st.boards.get(problem)
                if snap and (cur is None or snap["pulled_at"] > cur["pulled_at"]):
                    snap["file"] = self._rel(Path(snap["file"]))
                    events.append(("board.snapshot", snap, "C"))
            self.ledger.append_many(events)
            return [e[1]["problem"] for e in events]

    def history(self):
        """Refresh only our submission history (usually one API call)."""
        with self.control():
            st = self.state()
            prev = st.history if (st.history and st.history.get("max_submission_id") is not None
                                  and self.now() - st.history["pulled_at"] < 86400) else None
            hist = sources.pull_history(self.state_dir / "cache" / "history", previous=prev)
            hist["file"] = self._rel(Path(hist["file"]))
            self.ledger.append("history.snapshot", hist, "C")
            return {k: v for k, v in hist.items() if k not in ("best", "today_ids")}

    def queue(self, plan_result):
        """Copy plan lines into the team's send queue (research/acc/live/queue). Sending is a separate,
        human-authorised step: `sair_api.py send-queue` re-checks the live board and drops anything sent."""
        if not plan_result.get("file"):
            return {"queued": 0}
        qdir = self.repo / "research/acc/live/queue"
        qdir.mkdir(parents=True, exist_ok=True)
        waiting = {}
        for f in qdir.glob("*.txt"):
            for cid, moves, _ in harvest_mod.extract(f):
                waiting[cid] = min(len(moves), waiting.get(cid, 10 ** 9))
        keep = []
        for cid, moves, _ in harvest_mod.extract(self.repo / plan_result["file"]["path"]):
            if waiting.get(cid, 10 ** 9) > len(moves):
                keep.append("%s: [%s]" % (cid, ", ".join(map(str, moves))))
        if not keep:
            return {"queued": 0}
        out = qdir / ("upgh_%s.txt" % time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(self.now())))
        out.write_text("\n".join(keep) + "\n", encoding="utf-8")
        self.ledger.append("queue.written", {"file": self._rel(out), "sha256": sha256_file(out),
                                             "lines": len(keep), "plan": plan_result["file"]}, "V")
        return {"queued": len(keep), "file": self._rel(out)}

    def cycle(self):
        """One cycle: harvest, refresh board/history only when something new needs deciding, plan,
        queue. It does not send."""
        out = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now()))}
        out["harvest"] = {k: self.harvest()[k] for k in ("improved", "invalid", "disagree")}
        out["imported_boards"] = self.import_boards()
        st = self.state()
        new_since_plan = any(b["seq"] > (st.plans[-1]["seq"] if st.plans else 0) for b in st.best.values())
        if new_since_plan:
            clocks = self._clocks(st)
            if not (clocks["board_ac"]["ok"] and clocks["board_stable_ac"]["ok"]):
                out["board"] = {"pulled": [s["problem"] for s in self.board()["boards"]]}
            elif not clocks["history"]["ok"] or not clocks["board_history_skew"]["ok"]:
                out["history"] = self.history()
            try:
                p = self.plan()
                out["plan"] = {"scoring": p["scoring"], "points": p["points"]}
                out["queue"] = self.queue(p)
            except Refused as exc:
                out["plan"] = {"refused": str(exc)}
        else:
            out["plan"] = "skipped: no new best path since the last plan (no API calls spent)"
        qdir = self.repo / "research/acc/live/queue"
        out["queue_lines_waiting"] = sum(1 for f in qdir.glob("*.txt") for _ in harvest_mod.extract(f)) \
            if qdir.is_dir() else 0
        return out

    # -- plan --------------------------------------------------------------------------
    def rows_report(self, st=None):
        st = st or self.state()
        boards, held, clocks = self._boards(st), st.held(), self._clocks(st)
        out = []
        for cid in sorted(st.best):
            R = observe.observe(cid, st.best[cid], boards, held, clocks)
            v, missing = observe.verdict(R)
            out.append({"R": R, "verdict": v, "missing": missing,
                        "points": observe.points(v, R["k"])})
        return out, clocks

    def plan(self):
        """Write the lines that score right now. Never sends them."""
        with self.control():
            st = self.state()
            self._licence("plan", st, allow_stopped=True)
            clocks = self._clocks(st)
            stale = observe.common_clock(clocks, ("board_ac", "board_stable_ac", "history",
                                                  "board_history_skew"))
            if stale:
                self._refuse("plan", "S3", "clocks disagree or are stale: %s; run `upgh board`"
                             % ", ".join(stale))
            report, _ = self.rows_report(st)
            unobservable = [r for r in report if r["verdict"] == "unobservable"]
            scoring = [r for r in report if r["verdict"] in observe.SCORING]
            order = {"unsolved": 0, "beat": 1, "tie": 2}
            scoring.sort(key=lambda r: (order[r["verdict"]], -((r["R"]["record"] or 0) - r["R"]["length"]),
                                        r["R"]["k"] or 0, r["R"]["cid"]))
            behind = sorted((r for r in report if r["verdict"] == "above"),
                            key=lambda r: (r["R"]["length"] - r["R"]["record"], r["R"]["k"]))
            result = {"scoring": len(scoring), "unobservable": len(unobservable),
                      "points": round(sum(r["points"] for r in scoring), 4),
                      "lines": [{**{k: r["R"][k] for k in ("cid", "length", "record", "k", "held_len")},
                                 "verdict": r["verdict"], "points": r["points"]} for r in scoring],
                      "behind_by_1_to_3": [{k: r["R"][k] for k in ("cid", "length", "record", "k")}
                                           for r in behind if r["R"]["length"] - r["R"]["record"] <= 3][:40],
                      "file": None}
            if not scoring:
                self.ledger.append("plan.written", {**result, "boards": {p: b["sha256"] for p, b in st.boards.items()},
                                                    "history": st.history["sha256"]}, "V")
                return result
            stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(self.now()))
            path = self.state_dir / "plans" / ("SEND_%s.txt" % stamp)
            path.parent.mkdir(parents=True, exist_ok=True)
            text = "".join("%s: [%s]\n" % (r["R"]["cid"], ", ".join(map(str, st.best[r["R"]["cid"]]["moves"])))
                           for r in scoring[:500])
            path.write_text(text, encoding="utf-8")
            gate = self._official_cli(path)
            if not gate["ok"]:
                path.rename(path.with_suffix(".REFUSED.txt"))
                self._refuse("plan", "V", "official CLI rejected the plan file: %s" % gate["detail"])
            result["file"] = {"path": self._rel(path), "sha256": sha256_file(path)}
            result["official_cli"] = gate
            self.ledger.append("plan.written", {**result, "boards": {p: b["sha256"] for p, b in st.boards.items()},
                                                "history": st.history["sha256"],
                                                "clocks": {k: round(v["age_s"] or 0) for k, v in clocks.items()}},
                               "V")
            return result

    def _official_cli(self, path):
        proc = subprocess.run([sys.executable, "-m", "verifier", "--manifest",
                               "competition/tools/verifier/data/manifest.json", "--submission", str(path)],
                              cwd=self.sair_dir, capture_output=True, text=True,
                              env={**os.environ, "PYTHONPATH": str(self.sair_dir / "competition/tools"),
                                   "PYTHONDONTWRITEBYTECODE": "1"})
        try:
            verdict = json.loads(proc.stdout)
        except ValueError:
            return {"ok": False, "detail": "no JSON (exit %s): %s" % (proc.returncode, proc.stderr[-300:])}
        results = verdict.get("results", [])
        bad = [r for r in results if not r.get("ok")]
        return {"ok": proc.returncode == 0 and verdict.get("accepted") is True and not bad,
                "accepted": verdict.get("accepted"), "lines": len(results),
                "detail": bad[:5] or verdict.get("code")}

    # -- tasks -----------------------------------------------------------------------------
    def _workspace(self, tid):
        art = self.state_dir / "artifacts" / tid
        return {"artifacts_dir": self._rel(art), "never": NEVER}

    def _row_context(self, st, cid, boards):
        ch = self.checker.challenge(cid) or {}
        problem = observe.BOARD_OF[observe.track_of(cid)]
        row = boards.get(problem, {}).get(cid, {})
        best = st.best.get(cid)
        prior = [{"task": p["task"], "family": p["family"], "knobs": (p.get("strategy") or {}).get("knobs"),
                  "coverage": p.get("coverage"), "reopen_when": p.get("reopen_when")}
                 for p in st.parked.values() if p["row"] == cid][-5:]
        return {"start": ch.get("initial_relators"), "record": row.get("record"), "k": row.get("k"),
                "our_best": best["length"] if best else None, "our_best_moves": best["moves"] if best else None,
                "held": st.held().get(cid), "prior_misses": prior,
                "refined_knobs": sorted(st.refined.get(cid, ()))}

    def _builder_contract(self, st, tid, rows, strategy, why, boards, extra=None):
        method = self.cfg["methods"].get(strategy["method"], {})
        wall = method.get("wall_seconds", 900)
        fams = {r: st.family_for(r, strategy) for r in rows}
        c = {"task": tid, "role": "builder", "why": why, "rows": rows, "strategy": strategy, "family": fams,
             "runner": method.get("runner", "agent"),
             "prediction": "null: no row gets a path <= its live record within these limits; "
                           "a hit is any checked path that ties or beats a record we do not already hold",
             "limits": {"wall_seconds": wall, "lease_s": self.cfg["clocks"]["lease_s"]},
             "workspace": self._workspace(tid),
             "context": {r: self._row_context(st, r, boards) for r in rows}}
        if extra:
            c.update(extra)
        return c

    def external_claims(self):
        """Row numbers named in other lanes' research/acc/live/WORKING_*.md files committed recently.
        The team's convention: a lane writes the rows it is on. Twins (ac/sac) count as claimed together."""
        live = self.repo / "research/acc/live"
        limit = self.cfg["clocks"].get("claims_max_age_s", 21600)
        claimed = {}
        for f in sorted(live.glob("WORKING_*.md")):
            if f.name == "WORKING_upgh.md":
                continue
            t = subprocess.run(["git", "-C", str(self.repo), "log", "-1", "--format=%ct", "--", str(f)],
                               capture_output=True, text=True).stdout.strip()
            when = float(t) if t else f.stat().st_mtime
            if self.now() - when > limit:
                continue
            for num in set(re.findall(r"\b(?:ac|sac)-(\d{5})\b", f.read_text(encoding="utf-8", errors="replace"))):
                claimed.setdefault(num, f.name)
        return claimed

    def _write_working(self):
        st = self.state()
        lines = ["# Active harness lanes: UPG-H v2 (Claude edition)", "",
                 "Written by tools/acc/upgh on every claim and result. Rows below are being searched now; "
                 "other lanes please skip them. The harness skips rows named in any WORKING_*.md committed "
                 "in the last %d hours." % (self.cfg["clocks"].get("claims_max_age_s", 21600) // 3600), ""]
        open_tasks = [t for t in st.tasks.values() if t["status"] == "claimed" and t["contract"]["role"] == "builder"]
        for t in sorted(open_tasks, key=lambda t: t["contract"]["task"]):
            c = t["contract"]
            lines.append("- %s: %s (method %s, seed %s)" % (c["task"], ", ".join(c["rows"]), c["strategy"]["method"],
                                                           (c["strategy"].get("knobs") or {}).get("SEED")))
        if not open_tasks:
            lines.append("- (no rows claimed right now)")
        text = "\n".join(lines) + "\n"
        path = self.repo / "research/acc/live/WORKING_upgh.md"
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def _select_rows(self, st, boards, strategy):
        g = self.cfg["gates"]
        held, busy = st.held(), st.busy_rows()
        claimed = self.external_claims()
        cands = []
        for problem in ("ac", "stable_ac"):
            for cid, row in boards.get(problem, {}).items():
                rec, best = row["record"], st.best.get(cid)
                if cid in busy or cid.split("-")[1] in claimed:
                    continue
                if rec is None and not g["include_unsolved"]:
                    continue
                if rec is not None and g.get("max_k") is not None and row["k"] > g["max_k"]:
                    continue
                if best is None:
                    # a new target: other teams hold it, we have no path yet; short records only
                    if rec is None or rec > g.get("nopath_record_max", 0):
                        continue
                    L = None
                    gap, value = 2, 2.0 ** (-row["k"])
                elif rec is None:
                    L = best["length"]
                    gap, value = 1, 1.0
                else:
                    L = best["length"]
                    ours_at_rec = held.get(cid, 10 ** 9) <= rec or L <= rec
                    gap = L - (rec - 1 if ours_at_rec else rec)
                    # a beat is worth 1.0 minus the tie we already have; a new tie is worth 2^-k
                    value = 1.0 - 2.0 ** (1 - row["k"]) if ours_at_rec else 2.0 ** (-row["k"])
                    if ours_at_rec:
                        value *= g.get("beat_prior", 1.0)   # [H] beats by one have been rare; ties land more often
                category = "new" if best is None else "near"
                if best is not None and rec is not None and g["gap_max"] < gap <= g.get("shorten_gap_max", 0) \
                        and rec <= g.get("nopath_record_max", 0):
                    category = "new"          # a new target's first road: keep shortening it toward the record
                    value = 2.0 ** (-row["k"])
                elif not 1 <= gap <= g["gap_max"]:
                    continue
                chosen = self._rung(st, cid, best, strategy)
                if chosen is None:
                    continue  # every rung is hot or spent: advisor territory now
                fam = st.family_for(cid, chosen)
                cands.append({"cid": cid, "gap": gap, "k": row["k"], "record": rec, "value": round(value, 4),
                              "tries": st.heat[(cid, fam)], "strategy": chosen, "category": category})
        # breadth first: every target gets one attempt before any gets a second
        cands.sort(key=lambda c: (c["tries"], c["gap"], -c["value"], c["record"] or 0, c["cid"]))
        return cands

    def _rung(self, st, cid, best, default):
        """The strategy code uses on this row: an advisor's switch if there was one, else the first ladder
        rung that applies (needs a best path?), is not hot, and is not a spent deterministic run."""
        if cid in st.row_strategy:
            s = st.row_strategy[cid]
            return None if st.heat[(cid, st.family_for(cid, s))] >= self.cfg["gates"]["heat_before_advisor"] else s
        for rung in self.cfg.get("ladder") or [default]:
            method = self.cfg["methods"].get(rung["method"], {})
            if method.get("needs_best") and best is None:
                continue
            if method.get("needs_nobest") and best is not None:
                continue
            if method.get("sac_only") and not cid.startswith("sac-"):
                continue
            if method.get("needs_ac_twin") and ("ac-" + cid.split("-")[1]) not in st.best:
                continue
            if st.heat[(cid, st.family_for(cid, rung))] >= self.cfg["gates"]["heat_before_advisor"]:
                continue
            if "SEED" not in (rung.get("knobs") or {}) and self._exact_repeats(st, [cid], rung):
                continue  # deterministic and already run here
            return rung
        return None

    def next(self, role=None, runner=None):
        """Claim the next task: queued work first (advisor/checker/reopened), else code picks rows.
        runner="code" limits the claim to builder work the code runner can execute."""
        with self.control():
            self._recover_locked()
            st = self.state()
            self._licence("next", st)
            queued = [t for t in st.tasks.values() if t["status"] == "queued"
                      and (role is None or t["contract"]["role"] == role)
                      and (runner is None or t["contract"].get("runner") == runner)]
            events = []
            if queued:
                contract = min(queued, key=lambda t: t["opened_seq"])["contract"]
            elif role not in (None, "builder"):
                return None
            else:
                clocks = self._clocks(st)
                ages = [clocks[k]["age_s"] for k in ("board_ac", "board_stable_ac")]
                limit = self.cfg["clocks"]["select_board_max_age_s"]
                if any(a is None or a > limit for a in ages):
                    self._refuse("next", "S3", "board older than %ds (or never pulled): choosing rows on a stale "
                                 "board is Phi=0 on the wrong Pi; run `upgh board`" % limit)
                boards = self._boards(st)
                strategy = self.cfg["default_strategy"]
                cands = self._select_rows(st, boards, strategy)
                if runner == "code":   # a code lane must not claim a row whose strategy needs an agent
                    cands = [c for c in cands
                             if self.cfg["methods"].get(c["strategy"]["method"], {}).get("runner") == "code"]
                if not cands:
                    return None
                # alternate near-record rows and new targets (rows other teams hold, no path of ours yet)
                last = next((t["contract"].get("category") for t in sorted(
                    st.tasks.values(), key=lambda t: t["opened_seq"], reverse=True)
                    if t["contract"].get("category")), None)
                want = "new" if last == "near" else "near"
                pick = [c for c in cands if c["category"] == want] or cands
                cands = pick + [c for c in cands if c not in pick]
                tid = self._next_tid(st)
                strategy = cands[0]["strategy"]
                same = [c["cid"] for c in cands if canon(c["strategy"]) == canon(strategy)]
                rows = []
                for cid in same:   # a row and its AC/SAC twin share one beam run
                    num = cid.split("-")[1]
                    for r in [cid] + [x for x in same if x != cid and x.split("-")[1] == num]:
                        if r not in rows:
                            rows.append(r)
                    per_task = self.cfg["methods"].get(strategy["method"], {}).get(
                        "rows_per_task", self.cfg["gates"]["rows_per_task"])
                    if len({r.split("-")[1] for r in rows}) >= per_task:
                        break
                strategy = self._rotate_seed(st, rows, strategy)
                while self._exact_repeats(st, rows, strategy) and "SEED" in (strategy.get("knobs") or {}):
                    strategy = {**strategy, "knobs": {**strategy["knobs"], "SEED": strategy["knobs"]["SEED"] + 1}}
                why = "code choice (metric g): " + "; ".join(
                    "%s gap %d, k=%d, record %s, worth %.3g" % (c["cid"], c["gap"], c["k"], c["record"] or "none",
                                                               c["value"])
                    for c in cands if c["cid"] in rows)
                contract = self._builder_contract(st, tid, rows, strategy, why, boards,
                                                  {"category": cands[0]["category"]})
                events.append(("task.opened", contract, "V"))
            token = secrets.token_hex(12)
            until = self.now() + self.cfg["clocks"]["lease_s"]
            events.append(("task.claimed", {"task": contract["task"], "token_sha": sha256_bytes(token.encode()),
                                            "until": until}, "V"))
            self.ledger.append_many(events)
            path = self._write_contract(contract)
            self._write_lease(contract["task"], until)
            self._write_working()
            return {"task": contract["task"], "role": contract["role"], "token": token,
                    "contract": self._rel(path), "runner": contract.get("runner", "agent"),
                    "agent": self.cfg["roles"][contract["role"]]["claude_agent"]}

    def _rotate_seed(self, st, rows, strategy):
        """Heat, not a switch: each attempt in one family gets a fresh noise seed, new for every row in
        the task, so no run is an exact (deterministic) repeat of an earlier one."""
        knobs = dict(strategy.get("knobs") or {})
        if "SEED" not in knobs:
            return strategy
        tries = 0
        for row in rows:
            fam = st.family_for(row, strategy)
            tries = max(tries, sum(1 for t in st.tasks.values() if t["contract"]["role"] == "builder"
                                   and t["contract"].get("family", {}).get(row) == fam))
        knobs["SEED"] = int(knobs["SEED"]) + tries
        return {**strategy, "knobs": knobs}

    @staticmethod
    def _twins(rows):
        return {"%s-%s" % (p, r.split("-")[1]) for r in rows for p in ("ac", "sac")}

    def _exact_repeats(self, st, rows, strategy):
        """Earlier builder tasks with the same strategy and knobs on any of these rows or their AC/SAC
        twins (one beam run serves both twins)."""
        want = self._twins(rows)
        return sorted({t["contract"]["task"] for t in st.tasks.values()
                       if t["contract"]["role"] == "builder" and t["status"] in ("closed", "claimed")
                       and canon(t["contract"]["strategy"]) == canon(strategy)
                       and want & self._twins(t["contract"]["rows"])})

    def _write_contract(self, contract):
        path = self.state_dir / "tasks" / (contract["task"] + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path

    def _lease_file(self, tid):
        return self.state_dir / "leases" / (tid + ".json")

    def _write_lease(self, tid, until):
        path = self._lease_file(tid)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"until": until, "beat": self.now()}), encoding="utf-8")

    def _lease_until(self, task):
        until = task["claim"]["until"] if task.get("claim") else 0
        try:
            until = max(until, json.loads(self._lease_file(task["contract"]["task"]).read_text())["until"])
        except (OSError, ValueError, KeyError):
            pass
        return until

    def open(self, contract):
        """Queue an explicit task (from a person or an agent). The same gates apply."""
        with self.control():
            st = self.state()
            self._licence("open", st)
            role = contract.get("role")
            if role not in ROLES:
                raise ValueError("role must be one of %s" % (ROLES,))
            rows = contract.get("rows")
            if not isinstance(rows, list) or not rows or not all(isinstance(r, str) for r in rows):
                raise ValueError("rows must be a nonempty list of challenge ids")
            unknown = [r for r in rows if self.checker.challenge(r) is None]
            if unknown:
                raise ValueError("unknown challenge ids: %s" % unknown)
            tid = self._next_tid(st)
            boards = self._boards(st)
            if role == "builder":
                strategy = contract.get("strategy") or self.cfg["default_strategy"]
                missing = [c for c in PHI_COORDS if not strategy.get(c)]
                if missing:
                    raise ValueError("strategy lacks %s" % missing)
                hot = [r for r in rows if st.heat[(r, st.family_for(r, strategy))]
                       >= self.cfg["gates"]["heat_before_advisor"]]
                claimed = self.external_claims()
                taken = sorted({r for r in rows if r.split("-")[1] in claimed})
                if taken and not contract.get("force_claim"):
                    self._refuse("open", "claim", "rows claimed by another lane: %s (%s); a person may set "
                                 "force_claim" % (taken, ", ".join(sorted({claimed[r.split('-')[1]] for r in taken}))))
                repeats = self._exact_repeats(st, rows, strategy)
                if repeats and not contract.get("force_heat"):
                    self._refuse("open", "S2", "exact repeat of %s: same rows, same strategy and knobs; a "
                                 "deterministic rerun adds heat and no information" % ", ".join(repeats))
                if hot and not contract.get("force_heat"):
                    self._refuse("open", "S2", "family already hot on %s; change a scoring coordinate "
                                 "(%s) or ask the advisor; a person may set force_heat" % (hot, ", ".join(PHI_COORDS)))
                full = self._builder_contract(st, tid, rows, strategy, contract.get("why", "opened explicitly"),
                                              boards, {"force_heat": bool(contract.get("force_heat"))})
            else:
                full = {"task": tid, "role": role, "rows": rows, "why": contract.get("why", "opened explicitly"),
                        "limits": {"wall_seconds": 900}, "workspace": self._workspace(tid),
                        "context": {r: self._row_context(st, r, boards) for r in rows}}
                if role == "advisor":
                    full.update(self._advisor_fields(st, rows[0]))
            self.ledger.append("task.opened", full, "V")
            self._write_contract(full)
            return tid

    def _advisor_fields(self, st, row):
        cur = st.strategy_for(row, self.cfg["default_strategy"])
        return {"current_strategy": cur, "current_family": st.family_for(row, cur),
                "phi_coords": list(PHI_COORDS), "refined_knobs": sorted(st.refined.get(row, ())),
                "switches_used": st.switches[row], "switches_max": self.cfg["gates"]["max_switches_per_row"],
                "known_methods": {k: v.get("about", "") for k, v in self.cfg["methods"].items()}}

    def heartbeat(self, tid, token):
        st = self.state()
        task = self._claimed(st, tid, token)
        until = self.now() + self.cfg["clocks"]["lease_s"]
        self._write_lease(tid, until)
        return {"task": tid, "until": until, "stopped": st.stopped}

    def _claimed(self, st, tid, token):
        task = st.tasks.get(tid)
        if task is None:
            raise ValueError("unknown task " + tid)
        if task["status"] != "claimed":
            raise ValueError("task %s is %s, not claimed" % (tid, task["status"]))
        if sha256_bytes(token.encode()) != task["claim"]["token_sha"]:
            raise ValueError("wrong lease token for " + tid)
        return task

    def recover(self, abandon=()):
        """Mark expired leases interrupted. `abandon` lets a person end named claimed tasks now
        (for example after restarting workers); they are recorded as interrupted, never as misses."""
        with self.control():
            st = self.state()
            events = [("task.interrupted", {"task": tid, "reason": "abandoned by operator before its lease "
                                                                  "expired; not a miss, not a hit"}, "V")
                      for tid in abandon if st.tasks.get(tid, {}).get("status") == "claimed"]
            self.ledger.append_many(events)
            return [e[1]["task"] for e in events] + self._recover_locked()

    def _recover_locked(self):
        st = self.state()
        now, events = self.now(), []
        for task in st.tasks.values():
            if task["status"] == "claimed" and self._lease_until(task) < now:
                events.append(("task.interrupted", {"task": task["contract"]["task"],
                                                    "reason": "lease expired without a result; "
                                                              "not a miss, not a hit"}, "V"))
        self.ledger.append_many(events)
        return [e[1]["task"] for e in events]

    # -- results -------------------------------------------------------------------------------
    def _validate(self, st, task, result):
        c = task["contract"]
        role = c["role"]
        if not isinstance(result, dict):
            raise ValueError("result must be a JSON object")
        if result.get("task") not in (None, c["task"]):
            raise ValueError("result names task %r, lease is for %s" % (result.get("task"), c["task"]))
        kind = result.get("kind")
        if kind not in KINDS[role]:
            raise ValueError("%s may return %s, not %r" % (role, KINDS[role], kind))
        if not isinstance(result.get("summary"), str) or not result["summary"].strip():
            raise ValueError("summary is required")
        if len(result["summary"]) > 4000:
            raise ValueError("summary over 4000 characters")
        arts = result.get("artifacts", [])
        if not isinstance(arts, list):
            raise ValueError("artifacts must be a list")
        root = (self.repo / c["workspace"]["artifacts_dir"]).resolve() if role == "builder" else self.repo
        for a in arts:
            if not isinstance(a, dict) or not isinstance(a.get("path"), str) or not isinstance(a.get("sha256"), str):
                raise ValueError("each artifact is {path, sha256}")
            p = (self.repo / a["path"]).resolve()
            if not p.is_relative_to(root):
                raise ValueError("artifact outside %s: %s" % (self._rel(root), a["path"]))
            if not p.is_file():
                raise ValueError("artifact missing: " + a["path"])
            if p.stat().st_size > self.cfg["gates"]["max_artifact_bytes"]:
                raise ValueError("artifact over size cap: " + a["path"])
            if sha256_file(p) != a["sha256"]:
                raise ValueError("artifact hash mismatch: " + a["path"])
        refs = result.get("ledger_refs", [])
        if not isinstance(refs, list) or not all(type(x) is int and 1 <= x <= st.last_seq for x in refs):
            raise ValueError("ledger_refs must be existing ledger seq numbers")
        if role == "builder" and kind == "ran":
            if not arts:
                raise ValueError("a run without artifacts is not a run; return kind 'blocked'")
            if not isinstance(result.get("prediction"), str) or not result["prediction"].strip():
                raise ValueError("state the prediction you made before running")
            rw = result.get("reopen_when")
            if rw is not None and not (isinstance(rw, dict) and isinstance(rw.get("event"), str)
                                       and all(isinstance(v, (str, int)) for v in rw.values())):
                raise ValueError("reopen_when must be a flat {event: ..., key: value} object")
        if role == "advisor" and kind == "proposal":
            s = result.get("strategy")
            if not isinstance(s, dict) or any(not isinstance(s.get(k), str) or not s.get(k) for k in PHI_COORDS):
                raise ValueError("strategy must give every coordinate: %s" % (PHI_COORDS,))
            if s.get("knobs") is not None and not isinstance(s["knobs"], dict):
                raise ValueError("strategy.knobs must be an object")
            t = result.get("discriminating_test")
            if not isinstance(t, dict) or not isinstance(t.get("outcomes"), dict) or len(t["outcomes"]) < 2:
                raise ValueError("discriminating_test needs outcomes with at least two different meanings")
            if not isinstance(result.get("disputed_assumption"), str):
                raise ValueError("name the disputed assumption")
            if not refs and not arts:
                raise ValueError("a proposal cites ledger_refs or artifacts")
        if role == "checker" and kind == "review":
            if result.get("verdict") not in ("accept", "repair", "escalate"):
                raise ValueError("verdict is accept, repair or escalate")
            if not refs and not arts:
                raise ValueError("a review cites ledger_refs or artifacts")
        if role == "memory" and kind == "context" and not refs:
            raise ValueError("context must cite ledger_refs")

    def accept(self, tid, token, result):
        with self.control():
            st = self.state()
            task = self._claimed(st, tid, token)
            self._validate(st, task, result)
            self._licence("accept", st, allow_stopped=True)
            events = [("task.result", {"task": tid, "result": result, "after_stop": st.stopped}, "H")]
            role = task["contract"]["role"]
            handler = {"builder": self._on_builder, "advisor": self._on_advisor,
                       "checker": self._on_checker, "memory": self._on_memory}[role]
            events += handler(st, task, result)
            if st.stopped:  # record everything, dispatch nothing
                events = [e for e in events if e[0] != "task.opened"]
            self.ledger.append_many(events)
            self._write_working()
            closed = next((d for k, d, _ in events if k == "task.closed"), {})
            opened = [d["task"] + ":" + d["role"] for k, d, _ in events if k == "task.opened"]
            return {"task": tid, "outcome": closed.get("outcome"), "rows": closed.get("rows"), "opened": opened}

    def _on_builder(self, st, task, result):
        c = task["contract"]
        tid = c["task"]
        if result["kind"] == "blocked":
            return [("task.closed", {"task": tid, "outcome": "blocked", "detail": result["summary"][:500]}, "V")]
        found = []
        for a in result["artifacts"]:
            p = self.repo / a["path"]
            found += [(cid, m, "%s:%s" % (a["path"], w)) for cid, m, w in harvest_mod.extract(p)]
        events, improved, invalid, disagree, _, _ = self._check_paths(st, found, {"kind": "task", "task": tid},
                                                                      all_paths=True)
        events += [("path.invalid", d, "V") for d in invalid[:50]]
        boards, clocks = self._boards(st), self._clocks(st)
        held = st.held()
        rows_out, heat, parked = {}, [], []
        strategy = c["strategy"]
        for row in c["rows"]:
            best = improved.get(row) or st.best.get(row)
            R = observe.observe(row, best, boards, held, clocks)
            v, missing = observe.verdict(R)
            if row in improved and v in observe.SCORING:
                outcome = "hit"
            elif row in improved:
                outcome = "improved"
            else:
                outcome = "miss"
            rows_out[row] = {"outcome": outcome, "verdict": v, "length": R["length"], "record": R["record"],
                             "prev_length": (improved.get(row) or {}).get("prev_length")}
            if outcome == "miss":
                fam = c["family"][row]
                heat.append([row, fam])
                reopen = result.get("reopen_when") or {"event": "new_path", "row": row}
                parked.append(("miss.parked", {"task": tid, "row": row, "family": fam, "strategy": strategy,
                                               "coverage": result.get("coverage"), "summary": result["summary"][:500],
                                               "reopen_when": reopen,
                                               "scope": "bounded miss inside the stated limits; not an impossibility"},
                               "V"))
        overall = ("hit" if any(r["outcome"] == "hit" for r in rows_out.values()) else
                   "improved" if any(r["outcome"] == "improved" for r in rows_out.values()) else "miss")
        others = sorted(set(improved) - set(c["rows"]))
        events.append(("task.closed", {"task": tid, "outcome": overall, "rows": rows_out, "heat": heat,
                                       "also_improved": others, "invalid_paths": len(invalid),
                                       "disagreements": len(disagree)}, "V"))
        events += parked
        offset = 0
        # triggers: hot family -> advisor; invalid or disagreeing output -> checker
        for row, fam in heat:
            if st.heat[(row, fam)] + 1 >= self.cfg["gates"]["heat_before_advisor"] and not any(
                    t["contract"]["role"] == "advisor" and row in t["contract"]["rows"] for t in st.open_tasks()):
                if st.switches[row] >= self.cfg["gates"]["max_switches_per_row"]:
                    continue
                atid = self._next_tid(st, offset)
                offset += 1
                boards_ctx = boards
                events.append(("task.opened", {
                    "task": atid, "role": "advisor", "rows": [row],
                    "why": "family %s has %d bounded misses on %s without a hit (flailing guard)"
                           % (fam, st.heat[(row, fam)] + 1, row),
                    "limits": {"wall_seconds": 900}, "workspace": self._workspace(atid),
                    "context": {row: self._row_context(st, row, boards_ctx)},
                    **self._advisor_fields(st, row)}, "V"))
        if invalid or disagree:
            ctid = self._next_tid(st, offset)
            offset += 1
            events.append(("task.opened", {
                "task": ctid, "role": "checker", "rows": sorted({d["cid"] for d in invalid + disagree}),
                "why": "task %s produced %d path(s) the official verifier rejects and %d disagreement(s); "
                       "find the tool defect (start, generator map, orientation, rank, composition)"
                       % (tid, len(invalid), len(disagree)),
                "items": (disagree + invalid)[:20], "source_task": tid,
                "limits": {"wall_seconds": 900}, "workspace": self._workspace(ctid)}, "V"))
        events += self._wake_events(st, [{"event": "new_path", "row": r} for r in sorted(improved)],
                                    offset=offset, exclude_task=tid)
        return events

    def _on_advisor(self, st, task, result):
        c = task["contract"]
        tid, row = c["task"], c["rows"][0]
        if result["kind"] == "blocked":
            ev = [("task.closed", {"task": tid, "outcome": "blocked", "detail": result["summary"][:500]}, "V")]
            if isinstance(result.get("reopen_when"), dict):
                cur = st.strategy_for(row, self.cfg["default_strategy"])
                ev.append(("miss.parked", {"task": tid, "row": row, "family": st.family_for(row, cur),
                                           "strategy": cur, "reopen_when": result["reopen_when"],
                                           "summary": result["summary"][:500], "scope": "advisor blocked"}, "V"))
            return ev
        before = st.strategy_for(row, self.cfg["default_strategy"])
        after = dict(result["strategy"])
        after.setdefault("knobs", before.get("knobs", {}))
        changed = phi_changes(before, after, st.refined.get(row, ()))
        if not changed:
            return [("switch.refused", {"task": tid, "row": row, "before": before, "after": after,
                                        "species": "S2", "reason": "no scoring-complement coordinate changed "
                                                                   "(knob changes are heat, not a switch)"}, "V"),
                    ("task.closed", {"task": tid, "outcome": "refused", "detail": "S2"}, "V")]
        if st.switches[row] >= self.cfg["gates"]["max_switches_per_row"]:
            return [("switch.refused", {"task": tid, "row": row, "before": before, "after": after,
                                        "species": "budget", "reason": "switch budget for this row is spent"}, "V"),
                    ("task.closed", {"task": tid, "outcome": "refused", "detail": "switch budget"}, "V")]
        btid = self._next_tid(st)
        why = "switch by advisor %s: %s changed; test: %s" % (
            tid, ", ".join(changed), json.dumps(result["discriminating_test"])[:300])
        contract = self._builder_contract(st, btid, [row], after, why, self._boards(st),
                                          {"discriminating_test": result["discriminating_test"],
                                           "disputed_assumption": result["disputed_assumption"]})
        return [("switch", {"task": tid, "row": row, "before": before, "after": after, "changed": changed,
                            "discriminating_test": result["discriminating_test"],
                            "evidence": {"ledger_refs": result.get("ledger_refs", []),
                                         "artifacts": result.get("artifacts", [])}}, "V"),
                ("task.closed", {"task": tid, "outcome": "proposal", "changed": changed}, "V"),
                ("task.opened", contract, "V")]

    def _on_checker(self, st, task, result):
        c = task["contract"]
        tid = c["task"]
        if result["kind"] == "blocked":
            return [("task.closed", {"task": tid, "outcome": "blocked", "detail": result["summary"][:500]}, "V")]
        verdict = result["verdict"]
        events = [("task.closed", {"task": tid, "outcome": "review", "verdict": verdict}, "V")]
        row = c["rows"][0]
        if verdict == "repair":
            repairs = sum(1 for t in st.tasks.values() if t["contract"]["role"] == "builder"
                          and t["contract"].get("repair_of") and row in t["contract"]["rows"])
            if repairs < self.cfg["gates"]["max_repairs"]:
                strategy = st.strategy_for(row, self.cfg["default_strategy"])
                events.append(("task.opened", self._builder_contract(
                    st, self._next_tid(st), [row], strategy, "repair requested by checker %s" % tid,
                    self._boards(st), {"repair_of": tid, "review": result}), "V"))
        elif verdict == "escalate":
            atid = self._next_tid(st)
            events.append(("task.opened", {"task": atid, "role": "advisor", "rows": [row],
                                           "why": "checker %s escalated: %s" % (tid, result["summary"][:300]),
                                           "limits": {"wall_seconds": 900}, "workspace": self._workspace(atid),
                                           "context": {row: self._row_context(st, row, self._boards(st))},
                                           **self._advisor_fields(st, row)}, "V"))
        return events

    def _on_memory(self, st, task, result):
        return [("task.closed", {"task": task["contract"]["task"], "outcome": result["kind"],
                                 "suggested_wakes": result.get("suggested_wakes", [])}, "V")]

    # -- reopening -------------------------------------------------------------------------------
    def _wake_events(self, st, wakes, offset, exclude_task):
        """Match exact events against parked reopen_when. Duplicate events do nothing.
        While stopped nothing is reopened and no wake is recorded, so the wake can still fire after resume."""
        if st.stopped:
            return []
        events, seen = [], set(st.wake_keys)
        boards = None
        for ev in wakes:
            key = wake_key(ev)
            if key in seen:
                continue
            seen.add(key)
            matched = [tid for tid, p in st.parked.items()
                       if tid != exclude_task and isinstance(p.get("reopen_when"), dict)
                       and all(ev.get(k) == v for k, v in p["reopen_when"].items())]
            if not matched:
                continue
            events.append(("wake", {"key": key, "event": ev, "matched": matched}, "C"))
            boards = boards if boards is not None else self._boards(st)
            for ptid in matched:
                p = st.parked[ptid]
                tid = self._next_tid(st, offset)
                offset += 1
                contract = self._builder_contract(st, tid, [p["row"]], p["strategy"],
                                                  "reopened: %s matched parked %s" % (json.dumps(ev), ptid),
                                                  boards, {"reopened_from": ptid, "trigger": ev})
                events.append(("task.opened", contract, "V"))
        return events

    def wake(self, event):
        if not isinstance(event, dict) or not isinstance(event.get("event"), str):
            raise ValueError("a wake is {event: name, ...flat keys}")
        if not all(isinstance(v, (str, int)) for v in event.values()):
            raise ValueError("wake values must be strings or integers (exact matching only)")
        with self.control():
            st = self.state()
            self._licence("wake", st)
            events = self._wake_events(st, [event], 0, None)
            self.ledger.append_many(events)
            opened = [d["task"] for k, d, _ in events if k == "task.opened"]
            return {"key": wake_key(event), "reopened": opened, "duplicate": wake_key(event) in st.wake_keys}

    def split(self, witness):
        """S1 repair: two closed builder tasks, same row and family, different outcomes, one differing knob."""
        with self.control():
            st = self.state()
            row, knob = witness.get("row"), witness.get("knob")
            left, right = st.tasks.get(witness.get("left")), st.tasks.get(witness.get("right"))
            problems = []
            for name, t in (("left", left), ("right", right)):
                if t is None or t["contract"]["role"] != "builder" or t["status"] != "closed":
                    problems.append(name + " is not a closed builder task")
                elif row not in t["contract"]["rows"]:
                    problems.append("%s did not work on %s" % (name, row))
            if not problems:
                fl, fr = left["contract"]["family"][row], right["contract"]["family"][row]
                kl = (left["contract"]["strategy"].get("knobs") or {}).get(knob)
                kr = (right["contract"]["strategy"].get("knobs") or {}).get(knob)
                ol = left["closed"]["rows"][row]["outcome"]
                orr = right["closed"]["rows"][row]["outcome"]
                if fl != fr:
                    problems.append("families differ; this is already a switch, not a twin")
                if kl == kr:
                    problems.append("knob %r has the same value in both" % knob)
                if ol == orr:
                    problems.append("outcomes are equal (%s); nothing to separate" % ol)
            if problems:
                self._refuse("split", "S1", "; ".join(problems))
            data = {"row": row, "knob": knob, "left": witness["left"], "right": witness["right"],
                    "values": [kl, kr], "outcomes": [ol, orr],
                    "scope": "empirical witness: the knob separated outcomes once; it is now a family coordinate "
                             "for this row"}
            self.ledger.append("witness.split", data, "V")
            return data

    def negative(self, rows, source, reason, methods=None):
        """Import negative memory recorded outside the ledger (for example a team note that every tool
        stalled on these rows). Every ladder family becomes hot on them, so code stops choosing them; an
        advisor switch or a wake (new path, board change) can still reopen them."""
        with self.control():
            st = self.state()
            src = self.repo / source
            if not src.is_file():
                raise ValueError("source file not found: " + source)
            unknown = [r for r in rows if self.checker.challenge(r) is None]
            if unknown:
                raise ValueError("unknown challenge ids: %s" % unknown)
            rungs = (self.cfg.get("ladder") or []) + [self.cfg["default_strategy"],
                                                     dict(self.cfg["default_strategy"], method="beam")]
            if methods:
                rungs = [r for r in rungs if r["method"] in methods]
                if not rungs:
                    raise ValueError("no ladder rung uses %s" % (methods,))
            fams = sorted({family(r, ()) for r in rungs})
            data = {"rows": sorted(set(rows)), "families": fams, "heat": self.cfg["gates"]["heat_before_advisor"],
                    "source": {"path": self._rel(src), "sha256": sha256_file(src)}, "reason": reason}
            self.ledger.append("memory.imported", data, "C")
            return {k: v for k, v in data.items() if k != "families"}

    def void(self, tasks, reason):
        """Withdraw closed builder results that were not real searches (for example a tool that never ran).
        Appends a correction; the original lines stay in the ledger. Heat and parked misses are removed."""
        with self.control():
            st = self.state()
            events = []
            for tid in tasks:
                t = st.tasks.get(tid)
                if t is None or t["status"] != "closed" or t["contract"]["role"] != "builder":
                    raise ValueError("%s is not a closed builder task" % tid)
                events.append(("task.voided", {"task": tid, "reason": reason,
                                               "heat": t["closed"].get("heat", [])}, "V"))
            self.ledger.append_many(events)
            return [e[1]["task"] for e in events]

    # -- stop -----------------------------------------------------------------------------------------
    def stop(self, reason):
        with self.control():
            self.ledger.append("stop", {"reason": reason}, "V")
            self._stop_file().write_text(reason + "\n", encoding="utf-8")
            return {"stopped": True, "reason": reason}

    def resume(self, reason="resumed by a person"):
        with self.control():
            self.ledger.append("resume", {"reason": reason}, "V")
            with contextlib.suppress(FileNotFoundError):
                self._stop_file().unlink()
            return {"stopped": False}

    # -- the code runner ---------------------------------------------------------------------------------
    def run(self, max_tasks=1):
        """Claim and execute builder tasks whose method has a code runner. No model is involved."""
        done = []
        for _ in range(max_tasks):
            if self.state().stopped:
                break
            claim = self.next(role="builder", runner="code")
            if claim is None:
                break
            done.append(self.execute(claim["task"], claim["token"]))
        return done

    def execute(self, tid, token):
        st = self.state()
        task = self._claimed(st, tid, token)
        c = task["contract"]
        method = self.cfg["methods"][c["strategy"]["method"]]
        missing = [n for n in method.get("needs", []) if not (self.cache / n).exists()]
        if missing:
            return self.accept(tid, token, {"task": tid, "kind": "blocked",
                                            "summary": "missing %s in %s; run `upgh setup --t9`" % (missing, self.cache)})
        final_art = self.repo / c["workspace"]["artifacts_dir"]
        work = self.cache / "work" / tid
        art = self.cache / "running" / tid          # live outputs stay out of the repo until the run ends
        art.mkdir(parents=True, exist_ok=True)
        work.mkdir(parents=True, exist_ok=True)
        targets = []
        for row in c["rows"]:
            ctx = c["context"][row]
            ac = "ac-" + row.split("-")[1]
            if any(t["id"] == ac for t in targets):
                continue
            record = ctx["record"] if ctx["record"] is not None else (ctx["our_best"] or 100)
            targets.append({"id": ac, "record": record, "k": ctx["k"] or 0})
        (art / "targets.json").write_text(json.dumps(targets) + "\n", encoding="utf-8")
        jobs = {}
        for row in c["rows"]:
            ac = "ac-" + row.split("-")[1]
            best = st.best.get(ac)
            if best and ac not in jobs:
                jobs[ac] = best["moves"]
        (art / "jobs.json").write_text(json.dumps(jobs) + "\n", encoding="utf-8")
        knobs = c["strategy"].get("knobs") or {}
        subst = {"{python}": sys.executable, "{manifest}": str(self.sair_dir / "competition/tools/verifier/data/manifest.json"),
                 "{bin}": str(self.cache / "bin"), "{t9}": str(self.cache / "T9.tab"), "{work}": str(work),
                 "{out}": str(art / "out.jsonl"), "{targets}": str(art / "targets.json"),
                 "{jobs}": str(art / "jobs.json"), "{sair}": str(self.sair_dir)}

        def fill(text):
            for k, v in subst.items():
                text = text.replace(k, v)
            return re.sub(r"\{knob:(\w+)\}", lambda m: str(knobs[m.group(1)]), text)
        command = [fill(x) for x in method["command"]]
        env = {**os.environ, **{k: fill(v) for k, v in method.get("env", {}).items()}}
        wall = c["limits"]["wall_seconds"]
        beat_every = self.cfg["clocks"]["heartbeat_s"]
        t0 = time.monotonic()
        reason = "finished"
        with open(art / "stdout.log", "wb") as out, open(art / "stderr.log", "wb") as err:
            proc = subprocess.Popen(command, cwd=self.repo, env=env, stdout=out, stderr=err,
                                    stdin=subprocess.DEVNULL, start_new_session=True)
            last_beat = 0.0
            while proc.poll() is None:
                time.sleep(1)
                elapsed = time.monotonic() - t0
                if elapsed - last_beat >= beat_every:
                    self.heartbeat(tid, token)
                    last_beat = elapsed
                if self._stop_file().exists():
                    reason = "stopped"
                elif elapsed > wall:
                    reason = "wall_limit"
                if reason != "finished":
                    with contextlib.suppress(ProcessLookupError):
                        os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
                    break
        for name in ("stdout.log", "stderr.log"):
            p = art / name
            if p.stat().st_size > 262144:
                data = p.read_bytes()[-262144:]
                p.write_bytes(b"[truncated to last 256 KiB]\n" + data)
        wall_s = round(time.monotonic() - t0, 1)
        provenance = {}
        for n in method.get("needs", []):
            if n.startswith("bin/"):
                stamp = self.cache / (n + ".src.sha256")
                provenance[n] = {"binary_sha256": sha256_file(self.cache / n),
                                 "source_sha256": stamp.read_text().strip() if stamp.exists() else None}
        final_art.mkdir(parents=True, exist_ok=True)
        for name in ("out.jsonl", "targets.json", "jobs.json", "stdout.log", "stderr.log"):
            if (art / name).exists():
                shutil.copyfile(art / name, final_art / name)
        arts = [{"path": self._rel(p), "sha256": sha256_file(p)}
                for p in (final_art / "out.jsonl", final_art / "targets.json", final_art / "stdout.log",
                          final_art / "stderr.log") if p.exists()]
        if reason == "finished" and proc.returncode != 0:
            return self.accept(tid, token, {"task": tid, "kind": "blocked", "artifacts": arts,
                                            "summary": "%s exited %s after %ss: a tool error is not a miss; see "
                                                       "stderr.log" % (c["strategy"]["method"], proc.returncode, wall_s)})
        result = {"task": tid, "kind": "ran",
                  "summary": "%s on %s: exit %s after %ss (%s)" % (c["strategy"]["method"], ",".join(c["rows"]),
                                                                  proc.returncode, wall_s, reason),
                  "prediction": c["prediction"], "artifacts": arts,
                  "coverage": {"rows": [t["id"] for t in targets], "wall_s": wall_s, "exit": proc.returncode,
                               "ended_by": reason, "knobs": knobs, "binaries": provenance,
                               "note": "a wall limit or stop is a scoped miss, never an impossibility claim"}}
        return self.accept(tid, token, result)

    # -- memory and reporting ---------------------------------------------------------------------------------
    def recall(self, row):
        """Everything the ledger knows about one row, compact. Code retrieval; no model needed."""
        num = row.split("-")[1] if "-" in row else row
        cids = {"ac-" + num, "sac-" + num}
        out = []
        for e in self.ledger.events():
            d = e["data"]
            rows = d.get("rows")
            touched = (d.get("cid") in cids or d.get("row") in cids
                       or (isinstance(rows, (list, dict)) and bool(cids & set(rows))))
            if not touched:
                continue
            item = {"seq": e["seq"], "at": e["at"], "kind": e["kind"], "grade": e["grade"]}
            if e["kind"] == "path.best":
                item.update(cid=d["cid"], length=d["length"], prev=d.get("prev_length"), source=d["source"])
            elif e["kind"] == "task.opened":
                item.update(task=d["task"], role=d["role"], why=d.get("why"),
                            family=d.get("family"), knobs=(d.get("strategy") or {}).get("knobs"))
            elif e["kind"] == "task.closed":
                item.update(task=d["task"], outcome=d.get("outcome"),
                            rows={k: v for k, v in (d.get("rows") or {}).items() if k in cids})
            else:
                item["data"] = {k: v for k, v in d.items() if k not in ("moves", "context", "items")}
            out.append(item)
        return out

    def status(self):
        st = self.state()
        clocks = self._clocks(st)
        tasks = {}
        for t in st.tasks.values():
            key = "%s/%s" % (t["contract"]["role"], t["status"])
            tasks[key] = tasks.get(key, 0) + 1
        g = self.cfg["gates"]["heat_before_advisor"]
        last_plan = st.plans[-1] if st.plans else None
        return {"ledger_lines": st.last_seq, "stopped": st.stopped, "stop_reason": st.stop_reason,
                "pins_ok": not self.checker.pin_problems(),
                "clocks": {k: {"age_s": None if v["age_s"] is None else round(v["age_s"]), "ok": v["ok"]}
                           for k, v in clocks.items()},
                "best_paths": {"AC": sum(1 for c in st.best if c.startswith("ac-")),
                               "SAC": sum(1 for c in st.best if c.startswith("sac-"))},
                "tasks": tasks, "parked_misses": len(st.parked),
                "hot_families": [{"row": r, "family": f, "heat": n} for (r, f), n in st.heat.items() if n >= g],
                "switches": dict(st.switches), "splits": len(st.splits),
                "last_plan": None if not last_plan else {"at": last_plan["at"], "scoring": last_plan["scoring"],
                                                         "points": last_plan["points"], "file": last_plan["file"]},
                "recent_refusals": [{k: r[k] for k in ("at", "action", "species", "reason")} for r in st.refusals[-5:]]}

    def doctor(self):
        """Plain-language findings, labelled with the map's failure species."""
        findings = []

        def add(level, species, text):
            findings.append({"level": level, "species": species, "text": text})
        try:
            st = self.state()
        except Exception as exc:  # the ledger chain itself is broken
            return [{"level": "error", "species": "Z", "text": "ledger unreadable: %s" % exc}]
        add("ok", "Z", "ledger chain verified: %d lines" % st.last_seq)
        problems = self.checker.pin_problems()
        add("error" if problems else "ok", "licence",
            "; ".join(problems) if problems else "official verifier pinned at %s" % self.cfg["sair"]["commit"][:7])
        for name in ("bin/acc_beam", "bin/acc_window", "bin/acc_capped", "T9.tab"):
            if not (self.cache / name).exists():
                add("warn", "tools", "%s missing in %s (code runner blocked): `upgh setup --t9`" % (name, self.cache))
            elif name.startswith("bin/"):
                stamp = self.cache / (name + ".src.sha256")
                src = self.repo / "research/acc/optimality" / (name[4:] + ".c")
                if src.is_file() and (not stamp.exists() or stamp.read_text().strip() != sha256_file(src)):
                    add("error", "tools", "%s was not built from the current %s; results would carry the wrong "
                        "method label: run `upgh setup`" % (name, self._rel(src)))
        if st.stopped != self._stop_file().exists():
            add("warn", "stop", "STOP file and ledger disagree; the ledger wins (stopped=%s)" % st.stopped)
        if st.stopped:
            add("info", "stop", "stopped: %s" % st.stop_reason)
        # S3: clocks, one by one
        clocks = self._clocks(st)
        for name, clock in clocks.items():
            if not clock["ok"]:
                add("warn", "S3", "clock %s: %s" % (name, observe._fmt(clock)))
        now = self.now()
        for t in st.tasks.values():
            if t["status"] == "claimed" and self._lease_until(t) < now:
                add("warn", "S3", "task %s lease expired; `upgh recover` marks it interrupted" % t["contract"]["task"])
        git = subprocess.run(["git", "-C", str(self.repo), "status", "--porcelain", "--", self._rel(self.state_dir)],
                             capture_output=True, text=True)
        if git.stdout.strip():
            add("warn", "S3", "container clock: ledger/state has uncommitted changes; commit and push before the "
                              "container is reclaimed")
        # S4: found but not written
        h = self.cfg["harvest"]
        files = harvest_mod.scan(self.repo, h["globs"], h["exclude"])
        last = st.last_harvest["at_epoch"] if st.last_harvest else 0
        newer = [f for f in files if os.path.getmtime(f) > last]
        if not st.last_harvest:
            add("warn", "S4", "never harvested: %d files may hold unwritten paths; run `upgh harvest`" % len(files))
        elif newer:
            add("warn", "S4", "%d file(s) changed since the last harvest, e.g. %s; run `upgh harvest`"
                % (len(newer), ", ".join(self._rel(f) for f in newer[:3])))
        if st.boards and st.history:
            report, _ = self.rows_report(st)
            scoring = [r for r in report if r["verdict"] in observe.SCORING]
            planned = set()
            if st.plans and st.plans[-1].get("lines"):
                planned = {(l["cid"], l["length"]) for l in st.plans[-1]["lines"]}
            unplanned = [r for r in scoring if (r["R"]["cid"], r["R"]["length"]) not in planned]
            if unplanned:
                add("warn", "S4", "%d scoring path(s) are not in the latest plan (e.g. %s); run `upgh plan`"
                    % (len(unplanned), ", ".join(r["R"]["cid"] for r in unplanned[:5])))
        # S2 and flailing
        g = self.cfg["gates"]["heat_before_advisor"]
        hot_rows = sorted({row for (row, fam), n in st.heat.items() if n >= g
                           and not any(t["contract"]["role"] == "advisor" and row in t["contract"]["rows"]
                                       for t in st.open_tasks())})
        if hot_rows:
            add("info", "S2", "%d row(s) have a spent family and no advisor task (code skips them): %s%s"
                % (len(hot_rows), ", ".join(hot_rows[:8]), " ..." if len(hot_rows) > 8 else ""))
        for p in st.parked.values():
            rw = p.get("reopen_when") or {}
            b = st.best.get(rw.get("row"))
            if rw.get("event") == "new_path" and b and b["seq"] > p["seq"] and not p["reopened_by"]:
                add("warn", "S4", "parked %s waits for a new path on %s, and one exists (line %d); "
                    "`upgh wake '{\"event\": \"new_path\", \"row\": \"%s\"}'`" % (p["task"], rw["row"], b["seq"], rw["row"]))
        refused = sum(1 for r in st.refusals if r["species"] == "S2")
        if refused:
            add("info", "S2", "%d switch(es) refused as same-family cosmetics" % refused)
        # S1: disagreement and twins
        for d in st.disagree:
            add("error", "S1", "official and kernel disagree on %s (%s vs %s)"
                % (d["cid"], d["official"].get("code") or "ok", d["kernel"].get("code") or "ok"))
        by = {}
        for t in st.tasks.values():
            c = t["contract"]
            if c["role"] == "builder" and t["status"] == "closed" and t.get("closed", {}).get("rows"):
                for row, out in t["closed"]["rows"].items():
                    by.setdefault((row, c["family"][row]), []).append((c["task"], out["outcome"],
                                                                       c["strategy"].get("knobs") or {}))
        for (row, fam), runs in by.items():
            outs = {o for _, o, _ in runs}
            if "hit" in outs and "miss" in outs:
                hit = next(r for r in runs if r[1] == "hit")
                miss = next(r for r in runs if r[1] == "miss")
                diff = sorted(k for k in set(hit[2]) | set(miss[2]) if hit[2].get(k) != miss[2].get(k))
                add("warn", "S1", "twins on %s (%s): %s hit, %s missed; separating knob candidates %s -> "
                    "`upgh split %s KNOB %s %s`" % (row, fam, hit[0], miss[0], diff, row, hit[0], miss[0]))
        # frozen: work on rows that can no longer score
        if st.boards:
            boards, held = self._boards(st), st.held()
            for t in st.open_tasks("builder"):
                for row in t["contract"]["rows"]:
                    b = boards.get(observe.BOARD_OF[observe.track_of(row)], {}).get(row)
                    if b and b["record"] is not None and held.get(row, 10 ** 9) < b["record"]:
                        add("info", "frozen", "task %s works on %s, which we already hold below the record"
                            % (t["contract"]["task"], row))
        return findings
