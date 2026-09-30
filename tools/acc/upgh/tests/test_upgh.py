"""UPG-H v2 tests. Run: python3 -m unittest discover -s tools/acc/upgh/tests -v

Tests that need the pinned official verifier skip when it is not set up
(`python3 tools/acc/upgh/upgh.py setup`). Every harness test runs in a
temporary repository and never touches research/acc/upgh or the network.
"""
import copy
import gzip
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import diagnostics  # noqa: E402
import kernel  # noqa: E402
from harness import Harness, Refused  # noqa: E402
from ledger import Ledger, LedgerError, sha256_file  # noqa: E402
from state import family, phi_changes  # noqa: E402

CFG = json.loads((HERE / "config.json").read_text())
PROBE = Harness(state_dir=tempfile.mkdtemp())
PINNED = not PROBE.checker.pin_problems()
needs_pins = unittest.skipUnless(PINNED, "official verifier not set up; run `upgh setup`")

# real, officially accepted lines from ACC_SUBMIT_NEW14_20260927.txt
AC313 = [7, 7, 12, 2, 5, 12, 6, 2, 6, 2, 6, 8, 6, 2, 0, 3, 9, 4, 11, 13, 11, 6, 0, 6, 4, 7, 7, 3, 3, 5, 5, 5, 5]
AC1373 = [1, 7, 9, 4, 8, 6, 11, 2, 5, 12, 10, 8, 5, 10, 13, 11, 12, 2, 6, 5, 5, 1, 4, 10, 3, 5, 5, 5, 5, 10]
T0 = 1_790_000_000.0


class Env:
    """A throwaway repository with a harness, a fake clock and fake boards."""

    def __init__(self, methods=None):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = self.tmp / "repo"
        self.repo.mkdir()
        cfg = copy.deepcopy(CFG)
        cfg["harvest"]["globs"] = ["inbox/**/*.txt", "inbox/**/*.jsonl"]
        if methods:
            cfg["methods"].update(methods)
        self.cfg_path = self.tmp / "config.json"
        self.cfg_path.write_text(json.dumps(cfg))
        self.h = Harness(config_path=self.cfg_path, state_dir=self.repo / "state", repo=self.repo)
        self.t = [T0]
        self.h.now = lambda: self.t[0]

    def file(self, rel, text):
        p = self.repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def boards(self, ac=None, sac=None, held=None, at=None, history_at=None):
        at = self.t[0] if at is None else at
        events = []
        for problem, rows in (("ac", ac or {}), ("stable_ac", sac or {})):
            items = [{"challengeId": c, "currentBestLength": r, "kTeams": k, "status": "open"}
                     for c, (r, k) in rows.items()]
            p = self.repo / "state" / "cache" / ("%s_%d.json.gz" % (problem, at))
            p.parent.mkdir(parents=True, exist_ok=True)
            with gzip.open(p, "wt") as fh:
                json.dump({"pulledAt": at, "data": {"items": items}}, fh)
            events.append(("board.snapshot", {"problem": problem, "file": str(p.relative_to(self.repo)),
                                              "sha256": sha256_file(p), "pulled_at": at, "rows": len(items)}, "C"))
        events.append(("history.snapshot", {"file": "none", "sha256": "0" * 64,
                                            "pulled_at": at if history_at is None else history_at,
                                            "best": held or {}}, "C"))
        self.h.ledger.append_many(events)

    def result(self, rel, obj):
        p = self.file(rel, json.dumps(obj))
        return {"path": str(p.relative_to(self.repo)), "sha256": sha256_file(p)}


class LedgerTests(unittest.TestCase):
    def test_chain_tamper_and_torn_tail(self):
        led = Ledger(Path(tempfile.mkdtemp()) / "l.jsonl")
        led.append("a", {"x": 1}, "V")
        led.append_many([("b", {"y": 2}, "H"), ("c", {}, "C")])
        self.assertEqual([e["seq"] for e in led.events()], [1, 2, 3])
        with self.assertRaises(LedgerError):
            led.append("d", {}, "maybe")          # grades are closed
        raw = led.path.read_text()
        led.path.write_text(raw.replace('"y": 2', '"y": 3'))
        with self.assertRaises(LedgerError):
            led.events()                          # an edited line breaks the chain
        led.path.write_text(raw + '{"seq": 4, "half')
        with self.assertRaises(LedgerError):
            led.events()                          # a torn write fails closed
        torn = led.repair_tail()
        self.assertTrue(Path(torn).read_text().startswith('{"seq": 4'))
        self.assertEqual(len(led.events()), 3)    # kept bytes aside, chain intact


class DiagnosticsTests(unittest.TestCase):
    def test_phi_zero_does_not_mean_no_switch(self):
        d = diagnostics.phi_is_not_f()
        self.assertEqual(d["phi"], 0)             # diag(0,1) is normal
        self.assertAlmostEqual(d["f_norm2"], 0.5)  # but it moves the (1,1) projector

    def test_predictive_quotient_finite_test(self):
        L = [[0, 1, 0], [0, 0, 1], [0, 0, 0]]     # shift
        R = [[1, 0, 0]]                           # read the first coordinate
        self.assertEqual(diagnostics.observability(L, R), 3)
        # same present reading, different future: not the same state
        self.assertFalse(diagnostics.twins(L, R, [1, 0, 0], [1, 1, 0]))
        R2 = [[0, 0, 1]]                          # a readout that never sees coordinates 1-2 later
        self.assertEqual(diagnostics.observability(L, R2), 1)
        self.assertTrue(diagnostics.twins(L, R2, [1, 0, 5], [7, 3, 5]))


class StopGateTests(unittest.TestCase):
    def test_hook_blocks_search_and_submit_only(self):
        import subprocess
        gate = HERE / "stop_gate.py"
        cases = {"python3 tools/acc/upgh/upgh.py run": 2, "python3 tools/acc/sair_api.py submit F --yes": 2,
                 "bin/acc_beam T9 1 2": 2, "python3 tools/acc/upgh/upgh.py harvest": 0,
                 "python3 tools/acc/upgh/upgh.py resume": 0, "git commit -m ledger": 0}
        for command, code in cases.items():
            p = subprocess.run([sys.executable, str(gate)], input=json.dumps({"tool_input": {"command": command}}),
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, code, command)


class StateTests(unittest.TestCase):
    def test_knobs_are_heat_not_a_switch(self):
        a = CFG["default_strategy"]
        b = {**a, "knobs": {**a["knobs"], "W": 999}}
        self.assertEqual(phi_changes(a, b), [])
        self.assertEqual(family(a), family(b))
        self.assertEqual(phi_changes(a, b, refined={"W"}), ["knobs.W"])   # after an S1 split
        self.assertEqual(phi_changes(a, {**a, "method": "splice"}), ["method"])


@needs_pins
class KernelTests(unittest.TestCase):
    def test_independent_kernel_matches_official_golden_vectors(self):
        data = PROBE.sair_dir / "competition/tools/verifier/data"
        g = json.loads((data / "golden_vectors.json").read_text())
        specs = {"ac-r2-v1": kernel.Spec.load(data / "move_spec.json"),
                 "sac-r8-v1": kernel.Spec.load(data / "stable_move_spec.json")}
        for v in g["verify_vectors"]:
            ch = g["challenges"][v["challenge_id"]]
            if v.get("move_spec_version", ch["move_spec_version"]) != ch["move_spec_version"]:
                continue   # spec mismatch is checked before replay; not a kernel question
            r = kernel.replay(ch["initial_relators"], v["moves"], specs[ch["move_spec_version"]],
                              v.get("limits", g["default_limits"]))
            for key in ("ok", "code", "length", "work", "move_index", "reason"):
                if key in v["expected"]:
                    self.assertEqual(r.get(key), v["expected"][key], (v["name"], key))

    def test_exact_start(self):
        # gate 4: a route valid for one start is not valid for another row
        rs = PROBE.checker.check([("ac-00313", AC313), ("ac-01373", AC313), ("sac-00313", AC313 + [16, 15])])
        self.assertEqual([r["ok"] for r in rs], [True, False, True])
        self.assertTrue(all(r["agree"] for r in rs))


@needs_pins
class HarnessTests(unittest.TestCase):
    def test_harvest_writes_z_once_and_keeps_only_improvements(self):
        e = Env()
        e.file("inbox/a.txt", "ac-00313: %s\nac-01373: [1, 2, 3]\n" % AC313)
        e.file("inbox/b.jsonl", json.dumps({"id": "ac-00313", "ac": AC313, "sac": AC313 + [16, 15]}) + "\n")
        s = e.h.harvest()
        self.assertEqual((s["improved"], s["invalid"], s["disagree"]), (2, 1, 0))
        st = e.h.state()
        self.assertEqual(st.best["sac-00313"]["length"], 35)
        self.assertEqual(e.h.harvest()["checked"], 0)   # nothing new: nothing re-checked, nothing re-written

    def test_sac_is_derived_from_checked_ac_paths_only(self):
        e = Env()
        e.file("inbox/a.txt", "ac-00313: %s\nac-01373: [1, 2, 3]\n" % AC313)
        e.h.harvest()
        st = e.h.state()
        self.assertEqual(st.best["sac-00313"]["moves"], AC313 + [16, 15])
        self.assertEqual(st.best["sac-00313"]["source"]["kind"], "derived")
        self.assertNotIn("sac-01373", st.best)              # an invalid AC path derives nothing

    def test_scoring_needs_every_bit_of_R(self):
        e = Env()
        e.file("inbox/a.txt", "ac-00313: %s\nac-01373: %s\n" % (AC313, AC1373))
        e.h.harvest()
        e.boards(ac={"ac-00313": (33, 3), "ac-01373": (29, 2)}, sac={}, held={})
        rows = {r["R"]["cid"]: r["verdict"] for r in e.h.rows_report()[0] if r["R"]["cid"].startswith("ac-")}
        self.assertEqual(rows, {"ac-00313": "tie", "ac-01373": "above"})   # gate 11: valid is not scoring
        e.boards(ac={"ac-00313": (33, 3)}, sac={}, held={"ac-00313": 33})
        self.assertEqual({r["R"]["cid"]: r["verdict"] for r in e.h.rows_report()[0]}["ac-00313"], "held")
        e.t[0] += 3600                                                   # board goes stale
        v = {r["R"]["cid"]: (r["verdict"], r["missing"]) for r in e.h.rows_report()[0]}
        self.assertEqual(v["ac-00313"][0], "unobservable")
        self.assertIn("board_fresh", v["ac-00313"][1])

    def test_plan_refuses_on_disagreeing_clocks_then_writes_checked_file(self):
        e = Env()
        e.file("inbox/a.txt", "ac-00313: %s\n" % AC313)
        e.h.harvest()
        e.boards(ac={"ac-00313": (33, 3)}, sac={}, held={}, history_at=T0 - 2000)
        with self.assertRaises(Refused):           # S3: board and history describe two presents
            e.h.plan()
        self.assertEqual(e.h.state().refusals[-1]["species"], "S3")
        e.boards(ac={"ac-00313": (33, 3)}, sac={}, held={})
        p = e.h.plan()
        self.assertEqual([l["cid"] for l in p["lines"]], ["ac-00313"])
        self.assertTrue(p["official_cli"]["ok"])
        self.assertIn("ac-00313: [7, 7, 12", (e.repo / p["file"]["path"]).read_text())

    def test_builder_miss_parks_heats_and_calls_the_advisor(self):
        e = Env()
        e.file("inbox/a.txt", "ac-01373: %s\n" % AC1373)
        e.h.harvest()
        e.boards(ac={"ac-01373": (29, 2)}, sac={}, held={})
        for n in range(3):
            c = e.h.next(role="builder")
            self.assertEqual(json.loads((e.repo / c["contract"]).read_text())["rows"], ["ac-01373"])
            art = e.result("state/artifacts/%s/out.jsonl" % c["task"], {"id": "ac-01373", "ac": AC1373})
            out = e.h.accept(c["task"], c["token"], {"kind": "ran", "summary": "beam, no gain",
                                                     "prediction": "null", "artifacts": [art],
                                                     "coverage": {"W": 1000}})
            self.assertEqual(out["outcome"], "miss")
        st = e.h.state()
        self.assertEqual(len(st.parked), 3)
        self.assertIn("not an impossibility", next(iter(st.parked.values()))["scope"])   # gate 6
        self.assertEqual([t["contract"]["role"] for t in st.open_tasks()], ["advisor"])
        # the flailing guard: code will not pick the hot row again, and a person must force it
        self.assertEqual(e.h.next(role="builder"), None)
        with self.assertRaises(Refused):
            e.h.open({"role": "builder", "rows": ["ac-01373"], "strategy": CFG["default_strategy"]})

    def test_phi_gate_refuses_cosmetic_switch_and_accepts_a_real_one(self):
        e = Env()
        e.boards(ac={"ac-01373": (29, 2)}, sac={}, held={})
        for strategy, expect in ((dict(CFG["default_strategy"], knobs={"W": 5}), "refused"),
                                 (dict(CFG["default_strategy"], method="splice", pool="beam-pool"), "proposal")):
            tid = e.h.open({"role": "advisor", "rows": ["ac-01373"]})
            c = e.h.next(role="advisor")
            self.assertEqual(c["task"], tid)
            out = e.h.accept(tid, c["token"], {
                "kind": "proposal", "summary": "try it", "strategy": strategy, "ledger_refs": [1],
                "disputed_assumption": "the start seed is the bottleneck",
                "discriminating_test": {"observe": "best length", "outcomes": {"<=29": "keep", ">29": "drop"}}})
            self.assertEqual(out["outcome"], expect)
        st = e.h.state()
        self.assertEqual(st.switches["ac-01373"], 1)
        queued = [t["contract"] for t in st.open_tasks("builder")]
        self.assertEqual(queued[0]["strategy"]["method"], "splice")
        self.assertEqual(queued[0]["runner"], "agent")       # no code runner for splice: an agent runs it

    def test_stop_dominates_and_writing_z_still_works(self):
        e = Env()
        e.file("inbox/a.txt", "ac-01373: %s\n" % AC1373)
        e.h.harvest()
        e.boards(ac={"ac-01373": (29, 2)}, sac={}, held={})
        c = e.h.next(role="builder")
        e.h.stop("user stop")
        with self.assertRaises(Refused):
            e.h.next()                                   # gate 9
        self.assertTrue((e.repo / "state" / "STOP").exists())
        art = e.result("state/artifacts/%s/out.jsonl" % c["task"], {"id": "ac-01373", "ac": AC1373})
        out = e.h.accept(c["task"], c["token"], {"kind": "ran", "summary": "x", "prediction": "null",
                                                 "artifacts": [art]})
        self.assertEqual(out["opened"], [])              # recorded, nothing dispatched
        e.h.harvest()                                    # Z may still be written
        self.assertTrue(e.h.state().stopped)             # a restart is a fold: still stopped
        e.h.resume()
        self.assertFalse(e.h.state().stopped)

    def test_lost_lease_is_interrupted_not_a_miss_and_harvest_recovers_the_path(self):
        e = Env()
        e.file("inbox/a.txt", "ac-01373: %s\n" % (AC1373 + [0, 0]))   # 32 moves; [0, 0] cancels
        e.h.harvest()
        e.boards(ac={"ac-01373": (29, 2)}, sac={}, held={})
        c = e.h.next(role="builder")
        # the worker found a better path, wrote it, then died before `accept` (gates 7 and 8)
        e.file("inbox/%s.jsonl" % c["task"], json.dumps({"id": "ac-01373", "ac": AC1373}) + "\n")
        e.t[0] += CFG["clocks"]["lease_s"] + 1
        self.assertEqual(e.h.recover(), [c["task"]])
        st = e.h.state()
        self.assertEqual(st.tasks[c["task"]]["status"], "interrupted")
        self.assertEqual(len(st.parked), 0)              # not a miss
        with self.assertRaises(ValueError):
            e.h.accept(c["task"], c["token"], {"kind": "blocked", "summary": "late"})   # fenced
        self.assertEqual(e.h.harvest()["improved"], 2)   # S4 repair: the orphaned path (and its +[16,15] twin)
        self.assertEqual(e.h.state().best["ac-01373"]["length"], 30)

    def test_wake_reopens_once(self):
        e = Env()
        e.file("inbox/a.txt", "ac-01373: %s\n" % AC1373)
        e.h.harvest()
        e.boards(ac={"ac-01373": (29, 2)}, sac={}, held={})
        c = e.h.next(role="builder")
        art = e.result("state/artifacts/%s/out.jsonl" % c["task"], {"id": "ac-01373", "ac": AC1373})
        e.h.accept(c["task"], c["token"], {"kind": "ran", "summary": "x", "prediction": "null",
                                           "artifacts": [art], "reopen_when": {"event": "reducer_fixed",
                                                                                "row": "ac-01373"}})
        first = e.h.wake({"event": "reducer_fixed", "row": "ac-01373"})
        again = e.h.wake({"event": "reducer_fixed", "row": "ac-01373"})
        other = e.h.wake({"event": "reducer_fixed", "row": "ac-00001"})
        self.assertEqual((len(first["reopened"]), again["reopened"], other["reopened"]), (1, [], []))
        reopened = e.h.state().tasks[first["reopened"][0]]["contract"]
        self.assertEqual(reopened["reopened_from"], c["task"])

    def test_split_needs_a_real_witness(self):
        e = Env()
        e.file("inbox/a.txt", "ac-01373: %s\n" % AC1373)
        e.h.harvest()
        e.boards(ac={"ac-01373": (29, 2)}, sac={}, held={})
        tids = []
        for knobs in ({"W": 10}, {"W": 20}):
            s = dict(CFG["default_strategy"], knobs=dict(CFG["default_strategy"]["knobs"], **knobs))
            tid = e.h.open({"role": "builder", "rows": ["ac-01373"], "strategy": s})
            c = e.h.next(role="builder")
            art = e.result("state/artifacts/%s/out.jsonl" % tid, {"id": "ac-01373", "ac": AC1373})
            e.h.accept(tid, c["token"], {"kind": "ran", "summary": "x", "prediction": "null", "artifacts": [art]})
            tids.append(tid)
        with self.assertRaises(Refused):   # both missed: equal outcomes separate nothing
            e.h.split({"row": "ac-01373", "knob": "W", "left": tids[0], "right": tids[1]})

    def test_split_on_witnessed_twins_refines_the_family(self):
        e = Env()
        e.file("inbox/a.txt", "ac-00313: %s\n" % (AC313 + [0, 0]))
        e.h.harvest()
        e.boards(ac={"ac-00313": (33, 3)}, sac={}, held={})
        tids = []
        for w, path in ((10, AC313 + [0, 0]), (20, AC313)):       # W=10 misses, W=20 finds the tie
            s = dict(CFG["default_strategy"], knobs=dict(CFG["default_strategy"]["knobs"], W=w))
            tid = e.h.open({"role": "builder", "rows": ["ac-00313"], "strategy": s})
            c = e.h.next(role="builder")
            art = e.result("state/artifacts/%s/out.jsonl" % tid, {"id": "ac-00313", "ac": path})
            e.h.accept(tid, c["token"], {"kind": "ran", "summary": "x", "prediction": "p", "artifacts": [art]})
            tids.append(tid)
        st = e.h.state()
        self.assertEqual([st.tasks[t]["closed"]["outcome"] for t in tids], ["miss", "hit"])
        self.assertTrue(any("twins on ac-00313" in f["text"] for f in e.h.doctor()))
        e.h.split({"row": "ac-00313", "knob": "W", "left": tids[1], "right": tids[0]})
        st = e.h.state()
        a = dict(CFG["default_strategy"], knobs=dict(CFG["default_strategy"]["knobs"], W=10))
        b = dict(CFG["default_strategy"], knobs=dict(CFG["default_strategy"]["knobs"], W=20))
        self.assertNotEqual(st.family_for("ac-00313", a), st.family_for("ac-00313", b))   # W now separates
        self.assertEqual(st.family_for("ac-01373", a), st.family_for("ac-01373", b))       # only on that row

    def test_rows_claimed_by_other_lanes_are_skipped(self):
        e = Env()
        e.file("inbox/a.txt", "ac-01373: %s\nac-00313: %s\n" % (AC1373, AC313 + [0, 0]))
        e.h.harvest()
        e.boards(ac={"ac-01373": (29, 2), "ac-00313": (33, 3)}, sac={}, held={})
        e.file("research/acc/live/WORKING_other.md", "Row: sac-01373, bounded probe\n")
        e.t[0] = __import__("time").time()          # the claim file is fresh
        e.boards(ac={"ac-01373": (29, 2), "ac-00313": (33, 3)}, sac={}, held={})
        c = e.h.next(role="builder")
        self.assertEqual(json.loads((e.repo / c["contract"]).read_text())["rows"], ["ac-00313"])
        self.assertIn("t00001: ac-00313", (e.repo / "research/acc/live/WORKING_upgh.md").read_text())
        with self.assertRaises(Refused):
            e.h.open({"role": "builder", "rows": ["ac-01373"], "strategy": CFG["default_strategy"]})

    def test_artifacts_are_fenced_to_the_workspace(self):
        e = Env()
        e.file("inbox/a.txt", "ac-01373: %s\n" % AC1373)
        e.h.harvest()
        e.boards(ac={"ac-01373": (29, 2)}, sac={}, held={})
        c = e.h.next(role="builder")
        outside = e.result("inbox/elsewhere.jsonl", {"id": "ac-01373", "ac": AC1373})
        with self.assertRaises(ValueError):
            e.h.accept(c["task"], c["token"], {"kind": "ran", "summary": "x", "prediction": "p",
                                               "artifacts": [outside]})
        inside = e.result("state/artifacts/%s/o.jsonl" % c["task"], {"id": "ac-01373", "ac": AC1373})
        with self.assertRaises(ValueError):
            e.h.accept(c["task"], c["token"], {"kind": "ran", "summary": "x", "prediction": "p",
                                               "artifacts": [dict(inside, sha256="0" * 64)]})
        with self.assertRaises(ValueError):   # no artifacts means it did not run
            e.h.accept(c["task"], c["token"], {"kind": "ran", "summary": "x", "prediction": "p", "artifacts": []})

    def test_bad_tool_output_opens_a_checker_task(self):
        e = Env()
        e.file("inbox/a.txt", "ac-01373: %s\n" % AC1373)
        e.h.harvest()
        e.boards(ac={"ac-01373": (29, 2)}, sac={}, held={})
        c = e.h.next(role="builder")
        art = e.result("state/artifacts/%s/out.jsonl" % c["task"], {"id": "ac-01373", "ac": AC313})
        out = e.h.accept(c["task"], c["token"], {"kind": "ran", "summary": "x", "prediction": "p",
                                                 "artifacts": [art]})
        self.assertTrue(any(o.endswith(":checker") for o in out["opened"]))

    def test_kernel_disagreement_is_refused_and_escalated(self):
        e = Env()
        real = e.h.checker.kernel_verdict
        e.h.checker.kernel_verdict = lambda cid, moves: {"ok": False, "code": "E_NOT_TARGET"}
        try:
            e.file("inbox/a.txt", "ac-00313: %s\n" % AC313)
            s = e.h.harvest()
        finally:
            e.h.checker.kernel_verdict = real
        st = e.h.state()
        self.assertEqual((s["disagree"], s["improved"]), (1, 0))
        self.assertNotIn("ac-00313", st.best)            # never admitted
        self.assertEqual(st.open_tasks()[0]["contract"]["role"], "checker")
        self.assertTrue(any(f["species"] == "S1" and f["level"] == "error" for f in e.h.doctor()))

    def test_code_runner_executes_a_method_and_harvests_its_output(self):
        line = json.dumps({"id": "ac-00313", "ac": AC313})
        e = Env(methods={"fake": {"runner": "code", "wall_seconds": 30, "needs": [],
                                  "command": ["{python}", "-c",
                                              "import sys; open(sys.argv[1], 'w').write(sys.argv[2] + '\\n')",
                                              "{out}", line]}})
        cfg = json.loads(e.cfg_path.read_text())
        cfg["default_strategy"]["method"] = "fake"
        e.cfg_path.write_text(json.dumps(cfg))
        e.h = Harness(config_path=e.cfg_path, state_dir=e.repo / "state", repo=e.repo)
        e.h.now = lambda: e.t[0]
        e.file("inbox/a.txt", "ac-00313: %s\n" % (AC313 + [0, 0]))   # our old best: 35
        e.h.harvest()
        e.boards(ac={"ac-00313": (33, 3)}, sac={}, held={})
        done = e.h.run(max_tasks=1)
        self.assertEqual(done[0]["outcome"], "hit")
        self.assertEqual(e.h.state().best["ac-00313"]["length"], 33)


if __name__ == "__main__":
    unittest.main()
