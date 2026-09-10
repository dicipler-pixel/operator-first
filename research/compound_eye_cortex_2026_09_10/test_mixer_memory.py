#!/usr/bin/env python3
from pathlib import Path
import json
import tempfile
import mixer_memory as mm

checks = 0
refused = 0

def req(x, msg="control failed"):
    global checks
    if not x:
        raise AssertionError(msg)
    checks += 1

obs = [
    {"eye":"eye.a@1.0.0","channel":"speed","value":0.60,"units":"c","scope":"model-A","lineage":"impl-A","scale":"fine"},
    {"eye":"eye.b@1.0.0","channel":"speed","value":0.62,"units":"c","scope":"model-A","lineage":"impl-B","scale":"fine"},
    {"eye":"eye.c@1.0.0","channel":"phase","value":1.0,"units":"rad","scope":"model-A","lineage":"shared","scale":"fine"},
    {"eye":"eye.d@1.0.0","channel":"phase","value":-1.0,"units":"rad","scope":"model-A","lineage":"shared","scale":"coarse"},
]
trial = mm.make_mix_trial(
    "mix-001", "q-light",
    ["eye.a@1.0.0","eye.b@1.0.0","eye.c@1.0.0","eye.d@1.0.0","eye.e@1.0.0"],
    ["eye.a@1.0.0"], obs,
    routing_reasons={"eye.a@1.0.0":"velocity view","eye.c@1.0.0":"phase check"},
    parameters={"coupling":0.4})
req(trial["schema"] == mm.MIX_SCHEMA)
req(trial["no_output_eyes"] == ["eye.e@1.0.0"])
req(len(trial["composite"]["source_rows"]) == len(obs))
by = {g["channel"]:g for g in trial["composite"]["groups"]}
req(by["speed"]["recommended_view"] == "SUMMARY_PLUS_SOURCES")
req(by["phase"]["recommended_view"] == "OVERLAY_ONLY")
req(set(by["phase"]["distortion_flags"]) == {"SIGN_CANCELLATION","SHARED_LINEAGE","MIXED_SCALE"})
req(abs(by["phase"]["cancellation_fraction"] - 1.0) < 1e-15)
req(by["speed"]["independent_lineages"] == 2)
req(by["speed"]["source_rows_sha256"] == mm.digest(by["speed"]["source_rows"]))

ledger = {
    "schema":mm.LEDGER_SCHEMA,
    "rows":[
        {"eye":"eye.a@1.0.0","execution_status":"ok","surfaced":True,"reason":None,"value_sha256":"a"*64},
        {"eye":"eye.c@1.0.0","execution_status":"ok","surfaced":False,"reason":None,"value_sha256":"c"*64},
        {"eye":"eye.z@1.0.0","execution_status":"not_attempted","surfaced":False,"reason":"not selected","value_sha256":None},
    ],
}
replay = mm.replay_epiphany(ledger,[trial],["eye.c@1.0.0","eye.z@1.0.0"],["phase"])
classes = {r["eye"]:r["miss_class"] for r in replay["ledger_replay"]}
req(classes["eye.c@1.0.0"] == "SEEN_BUT_NOT_SURFACED")
req(classes["eye.z@1.0.0"] == "NOT_ATTEMPTED_EARLIER")
modes = set(replay["trial_replay"][0]["failure_modes"])
req("SEEN_BUT_NOT_SURFACED" in modes)
req("FUSION_SIGN_CANCELLATION" in modes and "FUSION_SHARED_LINEAGE" in modes and "FUSION_MIXED_SCALE" in modes)
req(any(a["mode"] == "FUSION_SIGN_CANCELLATION" for a in replay["learning_actions"]))

with tempfile.TemporaryDirectory() as td:
    p = Path(td)/"mix_history.jsonl"
    a = mm.append_mix_trial(p, trial)
    b = mm.append_mix_trial(p, mm.make_mix_trial("mix-002","q-light",["eye.a@1.0.0"],["eye.a@1.0.0"],[obs[0]]))
    rows = mm.verify_mix_log(p)
    req(len(rows) == 2 and rows[0]["event_sha256"] == a["event_sha256"] and rows[1]["event_sha256"] == b["event_sha256"])
    text = p.read_text()
    p.write_text(text.replace('0.6','0.7',1))
    try:
        mm.verify_mix_log(p)
    except ValueError:
        refused += 1
    else:
        raise AssertionError("tampered mixer log accepted")

bad = [
    lambda:mm.make_mix_trial("x","q",["a"],["b"],[]),
    lambda:mm.make_mix_trial("x","q",["a"],[],[{"eye":"b","channel":"x","value":1,"units":"u","scope":"s","lineage":"l"}]),
    lambda:mm.combine_observations([{"eye":"a","channel":"x","value":float('nan'),"units":"u","scope":"s","lineage":"l"}]),
    lambda:mm.replay_epiphany({"schema":"wrong"},[],[],[]),
]
for fn in bad:
    try:
        fn()
    except ValueError:
        refused += 1
    else:
        raise AssertionError("invalid mixer input accepted")
req(refused == 5)

out = {
    "status":"PASS",
    "positive_controls":checks,
    "refused_or_tampered_controls":refused,
    "phase_distortion_flags":by["phase"]["distortion_flags"],
    "epiphany_failure_modes":sorted(modes),
    "scope":"Meta-layer mixer/replay controls only; no scientific theorem is certified by this test.",
}
Path('mixer_memory_test_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
