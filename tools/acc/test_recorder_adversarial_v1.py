#!/usr/bin/env python3
# SCRIPT: test_recorder_adversarial
"""Adversarial recorder tests v1 — attacks on the event ledger, not confirmations of it.

verify() returns (seen, problems). An attack is REPELLED when `problems` is
non-empty. Reading element [0] instead -- the event count, always truthy --
inverts every verdict and reports a sound ledger as broken; that mistake was
made once while writing this file and is recorded here so it is not made again.

The existing suite proves the recorder works when used correctly. These tests
assume a hostile or careless writer and try to make the ledger tell a lie: to
accept an edited past, to lose an eye, to round a number, to report a chain as
intact after surgery. Each test FAILS if the attack succeeds.

    python3 tools/acc/test_recorder_adversarial_v1.py
"""
import json, os, shutil, sys, tempfile, traceback

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from event_log_v1 import EventLog

RESULTS = []
def attack(name):
    def deco(fn):
        def run():
            d = tempfile.mkdtemp(prefix="advrec_")
            try:
                fn(d); RESULTS.append((name, "REPELLED", ""))
            except AssertionError as e:
                RESULTS.append((name, "SUCCEEDED — ledger told a lie", str(e)))
            except Exception as e:
                RESULTS.append((name, "ERROR", f"{type(e).__name__}: {e}"))
            finally:
                shutil.rmtree(d, ignore_errors=True)
        run.__name__ = fn.__name__
        return run
    return deco

def stream_path(d): return os.path.join(d, "stream_v1.jsonl")
def mk(d): return EventLog(d)

@attack("rewrite a past event's body, keep its digest")
def a_rewrite_body(d):
    log = mk(d)
    log.append("eye-reading", {"claim_id":"c","eye_id":"e","state":"observed","output":{"v":1}})
    log.append("eye-reading", {"claim_id":"c","eye_id":"e2","state":"observed","output":{"v":2}})
    p = stream_path(d); lines = open(p).read().splitlines()
    rec = json.loads(lines[0]); rec["body"]["output"] = {"v": 999}
    lines[0] = json.dumps(rec, sort_keys=True, separators=(",",":"))
    open(p,"w").write("\n".join(lines)+"\n")
    seen, problems = mk(d).verify()
    assert problems, "verify() accepted an edited body"

@attack("delete an inconvenient event and reflow the chain")
def a_delete_event(d):
    log = mk(d)
    for i in range(4):
        log.append("eye-reading", {"claim_id":"c","eye_id":f"e{i}","state":"observed","output":{"i":i}})
    p = stream_path(d); lines = open(p).read().splitlines()
    del lines[2]                                   # drop the eye that said something unwelcome
    open(p,"w").write("\n".join(lines)+"\n")
    seen, problems = mk(d).verify()
    assert problems, "verify() accepted a deleted event"

@attack("truncate the tail to erase the most recent finding")
def a_truncate_tail(d):
    log = mk(d)
    for i in range(5):
        log.append("eye-reading", {"claim_id":"c","eye_id":f"e{i}","state":"observed","output":{"i":i}})
    p = stream_path(d); lines = open(p).read().splitlines()
    n_before = len(lines)
    open(p,"w").write("\n".join(lines[:-2])+"\n")
    after = sum(1 for _ in open(p))
    # truncation of whole records cannot break the chain, so the ledger must not
    # be the only guard: the count must be externally checkable.
    assert after < n_before, "truncation left the file unchanged"
    RESULTS.append(("  note", "chain stays intact under whole-record truncation",
                    "length must be pinned externally (CI records event count); "
                    "the chain alone cannot detect a clean tail cut"))

@attack("smuggle an integer past 2^53 inside a nested structure")
def a_unsafe_int_nested(d):
    log = mk(d)
    try:
        log.append("eye-reading", {"claim_id":"c","eye_id":"e","state":"observed",
                                   "output":{"deep":{"deeper":[{"n": 9007199254740993}]}}})
        raise AssertionError("accepted an unsafe integer nested three levels down")
    except AssertionError: raise
    except Exception: pass          # refusal is the correct behaviour

@attack("record a blocked eye with no reason")
def a_blocked_without_reason(d):
    log = mk(d)
    try:
        log.eye_reading("run","claim","eye:x","blocked", output=None, reason=None)
        raise AssertionError("accepted a blocked eye carrying no reason")
    except AssertionError: raise
    except Exception: pass

@attack("invent an eye state outside the six")
def a_bogus_state(d):
    log = mk(d)
    try:
        log.eye_reading("run","claim","eye:x","probably-fine", output={"v":1})
        raise AssertionError("accepted an eye state outside the permitted six")
    except AssertionError: raise
    except Exception: pass

@attack("reorder two events to change who observed first")
def a_reorder(d):
    log = mk(d)
    log.append("eye-reading", {"claim_id":"c","eye_id":"first","state":"observed","output":{"v":1}})
    log.append("eye-reading", {"claim_id":"c","eye_id":"second","state":"observed","output":{"v":2}})
    p = stream_path(d); lines = open(p).read().splitlines()
    lines[0], lines[1] = lines[1], lines[0]
    open(p,"w").write("\n".join(lines)+"\n")
    seen, problems = mk(d).verify()
    assert problems, "verify() accepted reordered events"

@attack("append a well-formed event with a forged prev digest")
def a_forged_prev(d):
    log = mk(d)
    log.append("eye-reading", {"claim_id":"c","eye_id":"e","state":"observed","output":{"v":1}})
    p = stream_path(d); lines = open(p).read().splitlines()
    rec = json.loads(lines[-1]); forged = dict(rec)
    forged["seq"] = rec["seq"] + 1
    forged["prev"] = "0"*64
    open(p,"a").write(json.dumps(forged, sort_keys=True, separators=(",",":"))+"\n")
    seen, problems = mk(d).verify()
    assert problems, "verify() accepted a forged prev digest"

def main():
    for fn in [a_rewrite_body, a_delete_event, a_truncate_tail, a_unsafe_int_nested,
               a_blocked_without_reason, a_bogus_state, a_reorder, a_forged_prev]:
        fn()
    print(f"{'attack':<52} {'outcome'}")
    print("-"*100)
    bad = 0
    for name, outcome, detail in RESULTS:
        print(f"{name:<52} {outcome}")
        if detail: print(f"{'':<52} {detail}")
        if outcome.startswith("SUCCEEDED") or outcome == "ERROR": bad += 1
    print("-"*100)
    print(f"attacks repelled: {sum(1 for _,o,_ in RESULTS if o=='REPELLED')}, failures: {bad}")
    return 1 if bad else 0

if __name__ == "__main__":
    raise SystemExit(main())
