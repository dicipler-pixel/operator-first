#!/usr/bin/env python3
"""UPG-H v2 (Claude edition): memory-first harness for the SAIR Andrews-Curtis work.

Hold the ledger. Spend a switch only to change what scores. Check every clock on
its own. Write Z or refuse.

  upgh setup [--t9]              pin the official verifier, compile tools, (build T9)
  upgh doctor                    plain-language health check, labelled S1-S4
  upgh status                    one screen: clocks, paths, tasks, heat, last plan
  upgh board                     pull live boards + full submission history (read-only)
  upgh harvest [FILE...]         write every path found in files to the ledger (checked twice)
  upgh plan [--queue]            write the lines that score now (and queue them); never sends them
  upgh cycle                     harvest, import boards, refresh only if needed, plan, queue (no send)
  upgh import-boards             adopt boards the team's sair_api.py already pulled (0 API calls)
  upgh history                   refresh our submission history (usually 1 API call)
  upgh next [--role R] [--runner code]   claim the next task (prints contract path + token)
  upgh run [--max-tasks N]       code runner: claim and execute beam tasks, no model needed
  upgh accept TASK TOKEN RESULT.json     hand in a worker result
  upgh heartbeat TASK TOKEN      extend a lease
  upgh open CONTRACT.json        queue an explicit task
  upgh recover                   mark expired leases interrupted
  upgh wake '{"event": ...}'     new evidence: reopen matching parked misses
  upgh split ROW KNOB LEFT RIGHT promote a knob that separated two outcomes (S1 repair)
  upgh recall ROW                what the ledger knows about one row
  upgh stop REASON | upgh resume
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import Harness, Refused  # noqa: E402
from ledger import LedgerError  # noqa: E402


def _load(text_or_path):
    p = Path(text_or_path)
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return json.loads(text_or_path)


def _age(s):
    if s is None:
        return "never"
    s = int(s)
    return "%ds" % s if s < 120 else "%dm" % (s // 60) if s < 7200 else "%.1fh" % (s / 3600)


def show_status(st):
    print("ledger: %d lines   stopped: %s%s   pins: %s" % (
        st["ledger_lines"], st["stopped"], " (%s)" % st["stop_reason"] if st["stopped"] else "",
        "ok" if st["pins_ok"] else "BROKEN"))
    print("clocks: " + "   ".join("%s %s%s" % (k, _age(v["age_s"]), "" if v["ok"] else "!")
                                  for k, v in st["clocks"].items()))
    print("best checked paths: AC %(AC)d, SAC %(SAC)d" % st["best_paths"])
    print("tasks: %s   parked misses: %d   switches: %s   splits: %d" % (
        st["tasks"] or "none", st["parked_misses"], st["switches"] or "none", st["splits"]))
    if st["hot_families"]:
        rows = sorted({h["row"] for h in st["hot_families"]})
        print("hot rows (a spent family; advisor territory): %d, e.g. %s" % (len(rows), ", ".join(rows[:6])))
    if st["last_plan"]:
        lp = st["last_plan"]
        print("last plan %s: %d scoring lines, ~%s points, file %s" % (
            lp["at"], lp["scoring"], lp["points"], (lp["file"] or {}).get("path")))
    for r in st["recent_refusals"]:
        print("refused %s %s [%s]: %s" % (r["at"], r["action"], r["species"], r["reason"][:120]))


def show_doctor(findings):
    mark = {"ok": "ok  ", "info": "info", "warn": "WARN", "error": "FAIL"}
    for f in findings:
        print("%s [%s] %s" % (mark[f["level"]], f["species"], f["text"]))


def show_plan(p):
    for line in p["lines"]:
        print("%-8s %s  ours %d  live %s  k %s  ~%.3g pt" % (line["verdict"], line["cid"], line["length"],
                                                           line["record"], line["k"], line["points"]))
    print("scoring lines: %d   ~%s points   unobservable: %d" % (p["scoring"], p["points"], p["unobservable"]))
    if p["behind_by_1_to_3"]:
        print("closest behind: " + ", ".join("%(cid)s %(length)d/%(record)d" % b for b in p["behind_by_1_to_3"][:12]))
    if p["file"]:
        print("wrote %s  (official CLI: %d lines ok)" % (p["file"]["path"], p["official_cli"]["lines"]))
        print("nothing was sent. Sending goes through the team tool, which re-checks the board within 5 min:\n"
              "  python3 tools/acc/sair_api.py send %s --lean          (dry run)\n"
              "  python3 tools/acc/sair_api.py send %s --lean --yes    (uses 1 of 40 daily submissions)"
              % (p["file"]["path"], p["file"]["path"]))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="upgh", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--state", help="state directory (default: research/acc/upgh)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("setup")
    p.add_argument("--t9", action="store_true", help="also build T9.tab (4.5 GB, about 3 minutes)")
    p = sub.add_parser("doctor")
    p.add_argument("--repair-tail", action="store_true")
    p = sub.add_parser("recover")
    p.add_argument("--abandon", nargs="*", default=[], help="claimed task ids to end now (operator)")
    for name in ("status", "board", "resume", "cycle", "import-boards", "history"):
        sub.add_parser(name)
    p = sub.add_parser("plan")
    p.add_argument("--queue", action="store_true", help="also copy the lines into research/acc/live/queue")
    p = sub.add_parser("harvest")
    p.add_argument("files", nargs="*")
    p = sub.add_parser("next")
    p.add_argument("--role", choices=("builder", "checker", "advisor", "memory"))
    p.add_argument("--runner", choices=("code", "agent"))
    p = sub.add_parser("run")
    p.add_argument("--max-tasks", type=int, default=1)
    p = sub.add_parser("execute")
    p.add_argument("task")
    p.add_argument("token")
    p = sub.add_parser("accept")
    p.add_argument("task")
    p.add_argument("token")
    p.add_argument("result")
    p = sub.add_parser("heartbeat")
    p.add_argument("task")
    p.add_argument("token")
    p = sub.add_parser("open")
    p.add_argument("contract")
    p = sub.add_parser("wake")
    p.add_argument("event")
    p = sub.add_parser("split")
    for name in ("row", "knob", "left", "right"):
        p.add_argument(name)
    p = sub.add_parser("void")
    p.add_argument("--reason", required=True)
    p.add_argument("tasks", nargs="+")
    p = sub.add_parser("negative")
    p.add_argument("--source", required=True, help="repo file that records the failed work")
    p.add_argument("--reason", required=True)
    p.add_argument("--methods", nargs="*", help="only these ladder methods are spent (default: all)")
    p.add_argument("rows", nargs="+")
    p = sub.add_parser("recall")
    p.add_argument("row")
    p = sub.add_parser("stop")
    p.add_argument("reason", nargs="+")
    args = ap.parse_args(argv)

    h = Harness(state_dir=args.state)
    try:
        if args.cmd == "setup":
            out = h.setup(build_t9=args.t9)
        elif args.cmd == "doctor":
            if args.repair_tail:
                print("moved torn tail to %s" % h.ledger.repair_tail())
            out = h.doctor()
            if not args.json:
                return show_doctor(out) or (1 if any(f["level"] == "error" for f in out) else 0)
        elif args.cmd == "status":
            out = h.status()
            if not args.json:
                return show_status(out) or 0
        elif args.cmd == "board":
            out = h.board()
        elif args.cmd == "harvest":
            out = h.harvest(args.files or None)
        elif args.cmd == "plan":
            out = h.plan()
            if args.queue:
                out["queue"] = h.queue(out)
            if not args.json:
                show_plan(out)
                if args.queue:
                    print("queue: %s" % out["queue"])
                return 0
        elif args.cmd == "cycle":
            out = h.cycle()
        elif args.cmd == "import-boards":
            out = {"imported": h.import_boards()}
        elif args.cmd == "history":
            out = h.history()
        elif args.cmd == "next":
            out = h.next(role=args.role, runner=args.runner) or {"task": None, "note": "nothing runnable"}
        elif args.cmd == "run":
            out = h.run(max_tasks=args.max_tasks)
        elif args.cmd == "execute":
            out = h.execute(args.task, args.token)
        elif args.cmd == "accept":
            out = h.accept(args.task, args.token, _load(args.result))
        elif args.cmd == "heartbeat":
            out = h.heartbeat(args.task, args.token)
        elif args.cmd == "open":
            out = {"task": h.open(_load(args.contract))}
        elif args.cmd == "recover":
            out = {"interrupted": h.recover(abandon=args.abandon)}
        elif args.cmd == "wake":
            out = h.wake(_load(args.event))
        elif args.cmd == "split":
            out = h.split({"row": args.row, "knob": args.knob, "left": args.left, "right": args.right})
        elif args.cmd == "void":
            out = {"voided": h.void(args.tasks, args.reason)}
        elif args.cmd == "negative":
            out = h.negative(args.rows, args.source, args.reason, methods=args.methods)
        elif args.cmd == "recall":
            out = h.recall(args.row)
        elif args.cmd == "stop":
            out = h.stop(" ".join(args.reason))
        elif args.cmd == "resume":
            out = h.resume()
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    except Refused as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (ValueError, LedgerError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
