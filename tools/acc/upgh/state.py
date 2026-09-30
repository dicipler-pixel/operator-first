"""M, the memory register: harness state is a fold over the ledger.

fold(events) keeps what a future decision can read: our best checked path per
row, open work, parked misses and what reopens them, heat per strategy family,
and stop. Anything the fold drops cannot change a later decision. That is the
operational stand-in for V/N_inf, and it is only an analogy [H]. When two
attempts look identical to the fold but lead to different outcomes, the fold
is too coarse. `upgh split` then promotes the separating knob into the family
signature for that row. That is the S1 repair.
"""
from __future__ import annotations

import collections
import hashlib
import json

from ledger import canon, parse_iso

# Strategy coordinates that define the scoring complement. Changing one of these is a switch (Phi fired).
PHI_COORDS = ("method", "seed", "pool", "capture", "representation", "board_filter")
# Everything under strategy["knobs"] is heat: effort inside one family. It is never a switch
# unless `split` has promoted that knob for the row.
ROLES = ("builder", "checker", "advisor", "memory")


def family(strategy: dict, refined=()) -> str:
    core = {c: strategy.get(c) for c in PHI_COORDS}
    knobs = strategy.get("knobs") or {}
    core["refined"] = {k: knobs.get(k) for k in sorted(refined)}
    return "f-" + hashlib.sha256(canon(core)).hexdigest()[:10]


def phi_changes(before: dict, after: dict, refined=()) -> list[str]:
    changed = [c for c in PHI_COORDS if before.get(c) != after.get(c)]
    kb, ka = before.get("knobs") or {}, after.get("knobs") or {}
    changed += ["knobs." + k for k in sorted(refined) if kb.get(k) != ka.get(k)]
    return changed


def wake_key(event: dict) -> str:
    return hashlib.sha256(canon(event)).hexdigest()[:16]


class State:
    def __init__(self):
        self.last_seq = 0
        self.setup = None
        self.best = {}                 # cid -> path.best data (+seq)
        self.invalid = []              # path.invalid data
        self.known_invalid = set()     # "cid:sha16" of paths already rejected, never re-checked by harvest
        self.disagree = []             # path.disagree data
        self.boards = {}               # problem -> board.snapshot data (+seq)
        self.prev_boards = {}          # problem -> the snapshot before that
        self.history = None            # history.snapshot data
        self.tasks = {}                # tid -> {"contract", "status", "claim", "result", "closed"}
        self.parked = {}               # tid -> miss.parked data (+ "reopened_by": [...])
        self.heat = collections.Counter()      # (row, family) -> misses since last switch/wake
        self.switches = collections.Counter()  # row -> accepted switches
        self.row_strategy = {}         # row -> strategy after the latest switch
        self.refined = collections.defaultdict(set)  # row -> knobs promoted to Phi coords
        self.stopped = False
        self.stop_reason = None
        self.last_harvest = None
        self.wake_keys = set()
        self.plans = []
        self.refusals = []
        self.splits = []

    # -- helpers -------------------------------------------------------------------
    def open_tasks(self, role=None):
        return [t for t in self.tasks.values()
                if t["status"] in ("queued", "claimed")
                and (role is None or t["contract"]["role"] == role)]

    def busy_rows(self):
        rows = set()
        for t in self.open_tasks():
            rows.update(t["contract"].get("rows", []))
        return rows

    def strategy_for(self, row, default):
        return self.row_strategy.get(row, default)

    def family_for(self, row, strategy):
        return family(strategy, self.refined.get(row, ()))

    def held(self):
        return (self.history or {}).get("best", {})

    # -- fold ----------------------------------------------------------------------
    def apply(self, e: dict):
        self.last_seq = e["seq"]
        kind, d = e["kind"], e["data"]
        if kind == "setup":
            self.setup = d
        elif kind == "path.best":
            self.best[d["cid"]] = {**d, "seq": e["seq"], "at": e["at"]}
        elif kind == "path.invalid":
            self.invalid.append({**d, "seq": e["seq"]})
            self.known_invalid.add("%s:%s" % (d["cid"], d["moves_sha"][:16]))
        elif kind == "path.disagree":
            self.disagree.append({**d, "seq": e["seq"]})
        elif kind == "board.snapshot":
            if d["problem"] in self.boards:
                self.prev_boards[d["problem"]] = self.boards[d["problem"]]
            self.boards[d["problem"]] = {**d, "seq": e["seq"]}
        elif kind == "history.snapshot":
            self.history = {**d, "seq": e["seq"]}
        elif kind == "harvest":
            self.last_harvest = {**d, "seq": e["seq"], "at": e["at"]}
            self.known_invalid.update(d.get("invalid_keys", []))
        elif kind == "task.opened":
            self.tasks[d["task"]] = {"contract": d, "status": "queued", "claim": None,
                                     "result": None, "closed": None, "opened_seq": e["seq"]}
        elif kind == "task.claimed":
            t = self.tasks[d["task"]]
            t["status"], t["claim"] = "claimed", d
        elif kind == "task.result":
            self.tasks[d["task"]]["result"] = d
        elif kind in ("task.closed", "task.interrupted"):
            t = self.tasks[d["task"]]
            t["status"] = "closed" if kind == "task.closed" else "interrupted"
            t["closed"] = {**d, "seq": e["seq"]}
            for row, fam in d.get("heat", []):
                self.heat[(row, fam)] += 1
        elif kind == "miss.parked":
            self.parked[d["task"]] = {**d, "seq": e["seq"], "reopened_by": []}
        elif kind == "wake":
            self.wake_keys.add(d["key"])
            for tid in d.get("matched", []):
                p = self.parked.get(tid)
                if p is not None:
                    p["reopened_by"].append(d["key"])
                    self.heat.pop((p["row"], p["family"]), None)
        elif kind == "switch":
            self.switches[d["row"]] += 1
            self.row_strategy[d["row"]] = d["after"]
        elif kind == "task.voided":
            t = self.tasks[d["task"]]
            t["status"] = "voided"
            for row, fam in d.get("heat", []):
                self.heat[(row, fam)] -= 1
                if self.heat[(row, fam)] <= 0:
                    del self.heat[(row, fam)]
            self.parked.pop(d["task"], None)
        elif kind == "memory.imported":
            # negative memory from outside the ledger (team files): these families are already spent here
            for row in d["rows"]:
                for fam in d["families"]:
                    self.heat[(row, fam)] += d["heat"]
        elif kind == "witness.split":
            self.refined[d["row"]].add(d["knob"])
            self.splits.append({**d, "seq": e["seq"]})
        elif kind == "plan.written":
            self.plans.append({**d, "seq": e["seq"], "at": e["at"]})
        elif kind == "refusal":
            self.refusals.append({**d, "seq": e["seq"], "at": e["at"]})
        elif kind == "stop":
            self.stopped, self.stop_reason = True, d.get("reason")
        elif kind == "resume":
            self.stopped, self.stop_reason = False, None

    def board_age(self, problem, now):
        b = self.boards.get(problem)
        return None if b is None else now - b["pulled_at"]

    def history_age(self, now):
        return None if self.history is None else now - self.history["pulled_at"]


def fold(events) -> State:
    s = State()
    for e in events:
        s.apply(e)
    return s


def contract_json(contract) -> str:
    return json.dumps(contract, indent=2, ensure_ascii=False)


def at_epoch(event) -> float:
    return parse_iso(event["at"])
