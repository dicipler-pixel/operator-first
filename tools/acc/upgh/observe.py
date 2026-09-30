"""R, the observation: what code can see about a row, and the verdict that follows.

A verdict is a pure function of R. When R lacks a bit that the verdict needs,
the verdict is "unobservable". The harness then refuses; it does not guess.
(The map's rule: a distinction R cannot see lives in N_inf and will leak.)

Clocks are reported one by one and never averaged. The common-clock check
passes only when each clock needed for an action is fresh on its own terms.
"""
from __future__ import annotations

SCORING = ("unsolved", "beat", "tie")
BOARD_OF = {"AC": "ac", "SAC": "stable_ac"}


def track_of(cid):
    return "SAC" if cid.startswith("sac-") else "AC"


def observe(cid, best, board_rows, held, clocks) -> dict:
    """best: path.best data or None. board_rows: problem -> {cid: {record, k}}.
    held: {cid: our accepted length}. clocks: output of clock_report()."""
    problem = BOARD_OF[track_of(cid)]
    rows = board_rows.get(problem)
    row = rows.get(cid) if rows is not None else None
    return {
        "cid": cid,
        "written": best is not None,                         # Z line exists (grade V)
        "official_ok": bool(best and best.get("official", {}).get("ok")),
        "agree": bool(best and best.get("agree")),
        "length": best["length"] if best else None,
        "board_seen": row is not None,
        "board_fresh": clocks.get("board_" + problem, {}).get("ok", False),
        "history_fresh": clocks.get("history", {}).get("ok", False),
        "record": row["record"] if row else None,
        "k": row["k"] if row else None,
        "held_len": held.get(cid),
    }


def verdict(R) -> tuple[str, list]:
    """Returns (verdict, missing_bits)."""
    missing = [b for b in ("written", "official_ok", "agree", "board_seen",
                           "board_fresh", "history_fresh") if not R[b]]
    if not R["written"]:
        return "unobservable", missing
    if R["written"] and not R["official_ok"]:
        return "invalid", missing
    if missing:
        return "unobservable", missing
    L, rec, held = R["length"], R["record"], R["held_len"]
    if rec is not None and L > rec:
        return "above", []          # behind the live record, whatever we hold
    if held is not None and held <= L:
        return "held", []
    if rec is None:
        return "unsolved", []
    if L < rec:
        return "beat", []
    if L == rec:
        return "tie", []
    return "above", []


def points(v, k) -> float:
    """[C] from tools/acc/HANDOFF_SAIR_ACC.md: beat or first solve = 1.0; tie = 2^(1-k) with us counted in k."""
    if v in ("unsolved", "beat"):
        return 1.0
    if v == "tie":
        return 2.0 ** (1 - ((k or 0) + 1))
    return 0.0


def clock_report(state, cfg, now, extra=None) -> dict:
    """Each clock on its own terms. ok=False when stale or never ticked."""
    c = cfg["clocks"]
    out = {}
    for problem in ("ac", "stable_ac"):
        age = state.board_age(problem, now)
        out["board_" + problem] = {"age_s": age, "max_age_s": c["board_max_age_s"],
                                   "ok": age is not None and 0 <= age <= c["board_max_age_s"]}
    age = state.history_age(now)
    out["history"] = {"age_s": age, "max_age_s": c["history_max_age_s"],
                      "ok": age is not None and 0 <= age <= c["history_max_age_s"]}
    # the board and our history must describe one present, not two
    times = [state.boards[p]["pulled_at"] for p in ("ac", "stable_ac") if p in state.boards]
    if state.history:
        times.append(state.history["pulled_at"])
    skew = (max(times) - min(times)) if len(times) == 3 else None
    out["board_history_skew"] = {"age_s": skew, "max_age_s": c["pair_max_skew_s"],
                                 "ok": skew is not None and skew <= c["pair_max_skew_s"]}
    if extra:
        out.update(extra)
    return out


def common_clock(report, needed) -> list[str]:
    return ["%s (%s)" % (name, _fmt(report.get(name))) for name in needed
            if not report.get(name, {}).get("ok")]


def _fmt(clock):
    if not clock or clock.get("age_s") is None:
        return "never ticked"
    return "age %ds > %ds" % (clock["age_s"], clock["max_age_s"])
