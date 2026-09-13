#!/usr/bin/env python3
# SCRIPT: acc_senses
"""acc_senses v1 — more senses for the Compound Eye: touch, taste, smell, sound.

Eyes see radiation (length, the Smith disk).  This adds, per replayed state (official verifier only):
  touch  — what the state feels under contact: how many of the 12 pair moves push length down
           (touch_pressure), leave it flat (touch_flat), and the deepest single push (touch_max_drop).
  taste  — the chemistry of the words: x_fraction of all letters, alternation rate (letter-type
           switches per letter) of each relator, and exponent sums of x and y in each relator.
  smell  — what lingers: leaky integrators (decay 0.7 per step) of cancellations, of growth, and of
           consecutive conjugations, so an event is still smelled several steps later.
  sound  — a WAV rendering of the run: pitch follows total length (lower length = higher pitch),
           each cancellation adds a click scaled by letters cancelled, growth adds a low thud.
Everything is telemetry; nothing here is an invariant, distance or proof.  Python 3 stdlib only.
"""
import argparse, json, math, os, struct, sys, wave
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import acc_run_decoder_v2 as D

VERSION = "acc_senses v1"; DECAY = 0.7
PAIRS = ((2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13))

def touch(core, s):
    L = sum(len(w) for w in s); ds = [sum(len(w) for w in core.apply_move(s, m)) - L for p in PAIRS for m in p]
    return {"touch_pressure": sum(1 for d in ds if d < 0), "touch_flat": sum(1 for d in ds if d == 0), "touch_max_drop": -min(ds)}

def taste(s):
    letters = [abs(g) for w in s for g in w]; n = len(letters) or 1
    def alt(w): return (sum(1 for a, b in zip(w, w[1:]) if abs(a) != abs(b)) / (len(w) - 1)) if len(w) > 1 else 0.0
    return {"taste_x_fraction": sum(1 for g in letters if g == 1) / n, "taste_alt_r0": alt(s[0]), "taste_alt_r1": alt(s[1]),
            "taste_expx_r0": sum(1 if g == 1 else -1 if g == -1 else 0 for g in s[0]), "taste_expy_r0": sum(1 if g == 2 else -1 if g == -2 else 0 for g in s[0]),
            "taste_expx_r1": sum(1 if g == 1 else -1 if g == -1 else 0 for g in s[1]), "taste_expy_r1": sum(1 if g == 2 else -1 if g == -2 else 0 for g in s[1])}

def sonify(steps, path, sr=22050, dur=0.08):
    L0 = steps[0]["total_length"]; frames = []
    for k, r in enumerate(steps):
        f = 220.0 * 2 ** ((L0 - r["total_length"]) / 12.0); n = int(sr * dur)
        canc, growth = r.get("cancellations", 0), max(0, r.get("delta_total", 0))
        for i in range(n):
            t = i / sr; env = min(1.0, i / 200) * min(1.0, (n - i) / 400)
            v = 0.35 * env * math.sin(2 * math.pi * f * t)
            if canc and i < 600: v += 0.4 * min(1.0, canc / 6) * (1 - i / 600) * math.sin(2 * math.pi * 3000 * t)  # click
            if growth and i < 1500: v += 0.4 * (1 - i / 1500) * math.sin(2 * math.pi * 60 * t)              # thud
            frames.append(max(-1, min(1, v)))
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", int(v * 32767)) for v in frames))
    return len(frames) / sr

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--sair", default="/home/user/saircompetition/andrews-curtis")
    ap.add_argument("--out-dir", default=os.path.join(HERE, "senses_v1")); ap.add_argument("--sound", default="ms-train-0160,ms-train-0066,ms-train-0342")
    a = ap.parse_args(); core, stable_core, specs = D.load_verifier(a.sair); limits, _ = D.load_manifest(a.sair)
    os.makedirs(os.path.join(a.out_dir, "recipes"), exist_ok=True); os.makedirs(os.path.join(a.out_dir, "sound"), exist_ok=True)
    summ = {"version": VERSION, "runs": 0, "steps": 0, "growth_steps": 0, "growth_with_pressure_available": 0, "sounds": {}}
    for c, moves in D.load_training(a.sair, "ac-r2-v1"):
        cid = c["challenge_id"]; steps, err = D.replay(core, stable_core, "ac-r2-v1", c["initial_relators"], moves)
        if err: print("REPLAY ERROR", cid, err); sys.exit(2)
        state = tuple(tuple(w) for w in c["initial_relators"]); rows = []; lc = lg = lj = 0.0
        for k, r in enumerate(steps):
            if k: state = core.apply_move(state, moves[k - 1])
            row = {}; row.update(touch(core, state)); row.update(taste(state))
            lc = DECAY * lc + r["cancellations"]; lg = DECAY * lg + max(0, r["delta_total"]); lj = DECAY * lj + (1 if r["move_class"] == "conjugate" else 0)
            row.update({"smell_linger_canc": lc, "smell_linger_growth": lg, "smell_linger_conj": lj}); rows.append(row)
            if k and r["delta_total"] > 0:
                summ["growth_steps"] += 1
                if rows[k - 1]["touch_pressure"] > 0: summ["growth_with_pressure_available"] += 1
        rec = D.run_record(c, moves, "ac-r2-v1", "training", steps, None, specs.get("ac-r2-v1").verify(c, moves, "ac-r2-v1", limits))
        ds = D.mixer_dataset(rec); units = {"touch": "count", "taste_x": "fraction", "taste_alt": "switches per letter", "taste_exp": "exponent sum", "smell": "lingering letters"}
        for key in rows[0]:
            u = "count" if key.startswith("touch") else "fraction" if key == "taste_x_fraction" else "switches per letter" if key.startswith("taste_alt") else "exponent sum" if key.startswith("taste_exp") else "lingering units"
            ds["traces"].append({"id": key, "label": key.replace("_", " "), "unit": u, "source": VERSION + " (official verifier replay)", "values": [row[key] for row in rows], "defaultRoute": "y", "defaultEnabled": key in ("touch_pressure", "smell_linger_canc")})
        ds["id"] += "__senses"; ds["title"] += " — senses v1"; ds["description"] = (ds.get("description", "") + " Touch/taste/smell channels; telemetry only.")
        rp = {"schema": "compound-eye-mixer-recipe-v1", "engine_version": "1.0.0", "dataset": ds, "settings": D.recipe_settings(ds, "rms"), "baseline": None,
              "meaning": "A reproducible visual composition; weights, centering and smoothing are chosen display operations, not automatically physical laws."}
        with open(os.path.join(a.out_dir, "recipes", f"{cid}__training__senses_recipe.json"), "w") as f: json.dump(rp, f, separators=(",", ":"))
        summ["runs"] += 1; summ["steps"] += len(rows) - 1
        if cid in a.sound.split(","):
            summ["sounds"][cid] = round(sonify(steps, os.path.join(a.out_dir, "sound", f"{cid}.wav")), 2)
    json.dump(summ, open(os.path.join(a.out_dir, "SUMMARY.json"), "w"), indent=1); print(json.dumps(summ, indent=1))

if __name__ == "__main__": main()
