"""Hourly independent eye recording, mixed only after the hour closes.

Jeromie's rule, which this file exists to enforce:

    Each hour records independently. They are only mixed together afterward
    to see for effect.

event_log_v1 guarantees that every eye leaves a record. It does NOT guarantee
that the record is the eye's OWN. On 2026-09-14 twelve gate readings were
appended at seq 2420-2431 with timestamps spanning ten milliseconds --
20:59:12.377 to .387. That is one author writing twelve records in one loop.
Every eye left a record and not one of them was an independent observation.
This file makes that failure structurally impossible to repeat silently.

Four properties, each with a test that tries to break it:

  HOUR-BUCKETED    every reading carries the UTC hour it observed in. An eye
                   reads its own hour; hours are the unit of independence.

  ONE PER HOUR     a second reading from the same (eye, item, hour) is
                   REFUSED. You cannot revise a reading after seeing how it
                   landed, because there is no second slot to revise into.

  MIX ONLY CLOSED  an hour cannot be mixed until it is over. The mix therefore
                   cannot exist while any reading in it is still being made,
                   so no reading in a mixed hour was influenced by the mix.
                   This is the whole point and it is checked, not promised.

  BATCHING VISIBLE co-authored readings are NOT rejected and NOT deleted --
                   they are measured. The mix reports how far apart in wall
                   time the readings of an hour were actually written, so a
                   ten-millisecond block is visible as what it is. Mixing may
                   change what influences a decision; it may never erase what
                   an eye saw, or how it came to say it.

An eye must declare what it read. `read=` is hashed into the record, so two
eyes claiming independence while consuming byte-identical input are visible
as such. Passing another eye's reading as input is refused outright.

    python3 tools/acc/eye_hour_v1.py --item <id>            # show hours
    python3 tools/acc/eye_hour_v1.py --item <id> --mix      # mix closed hours
"""

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from event_log_v1 import EventLog, EYE_STATES, canonical, sha256  # noqa: E402

READING_STATES = {"observed", "silent", "contradicted"}
EXCUSED_STATES = {"blocked", "failed", "disabled"}


def hour_of(ts):
    """The UTC hour bucket a timestamp falls in, as '2026-09-14T20Z'."""
    if isinstance(ts, str):
        ts = _dt.datetime.fromisoformat(ts)
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=_dt.timezone.utc)
    ts = ts.astimezone(_dt.timezone.utc)
    return f"{ts:%Y-%m-%dT%H}Z"


def now_hour():
    return hour_of(_dt.datetime.now(_dt.timezone.utc))


def _foreign_eye(value, mine):
    """Find another eye's reading smuggled in as this eye's input."""
    if isinstance(value, dict):
        eid = value.get("eye_id")
        if isinstance(eid, str) and eid != mine:
            return eid
        for v in value.values():
            found = _foreign_eye(v, mine)
            if found:
                return found
    elif isinstance(value, (list, tuple)):
        for v in value:
            found = _foreign_eye(v, mine)
            if found:
                return found
    return None


class HourlyEyes:
    def __init__(self, log_dir="ledger/events"):
        self.log = EventLog(log_dir)

    # ---------------------------------------------------------------- reading

    def readings(self, item_id=None):
        """Every hour-bucketed eye reading, oldest first."""
        out = []
        # read() yields (lineno, record_or_None, raw); None means a torn line,
        # which is reported by verify() and never parsed as data here.
        for _n, rec, _raw in self.log.read():
            if rec is None or rec.get("kind") != "eye-reading":
                continue
            b = rec.get("body") or {}
            if "hour" not in b:
                continue                      # pre-hour records; not mixable
            if item_id and b.get("item_id") != item_id:
                continue
            out.append({"seq": rec["seq"], "ts": rec["ts"], **b})
        return out

    def taken(self, eye_id, item_id, hour):
        return any(r["eye_id"] == eye_id and r["hour"] == hour
                   for r in self.readings(item_id))

    # ---------------------------------------------------------------- writing

    def record(self, eye_id, item_id, state, read, output=None, reason=None,
               hour=None, run_id="default"):
        if state not in EYE_STATES:
            raise ValueError(f"eye state must be one of {sorted(EYE_STATES)}")
        if state in READING_STATES and output is None and state == "observed":
            raise ValueError("an 'observed' reading must carry an output")
        if state in EXCUSED_STATES and not reason:
            raise ValueError(
                f"state {state!r} must carry a reason. An eye that cannot read "
                "files blocked/failed WITH a reason and keeps its place.")

        foreign = _foreign_eye(read, eye_id)
        if foreign:
            raise ValueError(
                f"{eye_id!r} was handed {foreign!r}'s reading as input. Each hour "
                "records independently; an eye reads the data, not another eye.")

        hour = hour or now_hour()
        if hour > now_hour():
            raise ValueError(f"hour {hour} has not happened yet")
        if self.taken(eye_id, item_id, hour):
            raise ValueError(
                f"{eye_id!r} already recorded on {item_id!r} for hour {hour}. "
                "One reading per eye per hour: there is no second slot to "
                "revise into after seeing how the first landed.")

        return self.log.append("eye-reading", {
            "claim_id": item_id, "item_id": item_id, "eye_id": eye_id,
            "state": state, "output": output, "reason": reason,
            "basis": "hourly", "hour": hour,
            "input_digest": sha256(canonical(read)),
        }, run_id=run_id)

    # ----------------------------------------------------------------- mixing

    def hours(self, item_id):
        seen = {}
        for r in self.readings(item_id):
            seen.setdefault(r["hour"], []).append(r)
        return dict(sorted(seen.items()))

    def mix(self, item_id, hour):
        """Mix one CLOSED hour. Refuses an hour that is still running."""
        if hour >= now_hour():
            raise ValueError(
                f"hour {hour} is still open (now {now_hour()}). An hour is mixed "
                "only after it closes, so that no reading in it can have been "
                "influenced by the mix.")
        rows = self.hours(item_id).get(hour, [])
        if not rows:
            return {"item_id": item_id, "hour": hour, "readings": 0}

        stamps = sorted(_dt.datetime.fromisoformat(r["ts"]) for r in rows)
        spread_ms = (stamps[-1] - stamps[0]).total_seconds() * 1000.0
        digests = {}
        for r in rows:
            digests.setdefault(r["input_digest"], []).append(r["eye_id"])
        shared = {d: e for d, e in digests.items() if len(e) > 1}

        return {
            "item_id": item_id, "hour": hour, "readings": len(rows),
            "eyes": sorted(r["eye_id"] for r in rows),
            "read": sorted(r["eye_id"] for r in rows if r["state"] in READING_STATES),
            "excused": sorted(r["eye_id"] for r in rows if r["state"] in EXCUSED_STATES),
            # Batching is measured, never erased. A ten-millisecond spread
            # across many eyes is one author in a loop, not many observers.
            "wall_spread_ms": round(spread_ms, 3),
            "co_authored": spread_ms < 1000.0 and len(rows) > 2,
            "shared_input_digests": shared,
        }

    def mix_all(self, item_id):
        return [self.mix(item_id, h) for h in self.hours(item_id)
                if h < now_hour()]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--item", required=True)
    p.add_argument("--mix", action="store_true", help="mix every closed hour")
    p.add_argument("--dir", default="ledger/events")
    a = p.parse_args(argv)

    he = HourlyEyes(a.dir)
    hours = he.hours(a.item)
    if not hours:
        print(f"no hour-bucketed readings on {a.item!r}")
        print("(readings filed before eye_hour_v1 carry no hour and are not mixable)")
        return 0

    print(f"item: {a.item}")
    for h, rows in hours.items():
        tag = "OPEN" if h >= now_hour() else "closed"
        print(f"  {h}  {len(rows):>3} readings  [{tag}]")

    if a.mix:
        print()
        for m in he.mix_all(a.item):
            print(f"hour {m['hour']}: {m['readings']} readings, "
                  f"{len(m['read'])} read / {len(m['excused'])} excused")
            print(f"  wall spread {m['wall_spread_ms']} ms"
                  + ("   <-- CO-AUTHORED: written as one batch, not observed "
                     "independently" if m["co_authored"] else ""))
            for d, eyes in m["shared_input_digests"].items():
                print(f"  shared input {d[:12]}: {', '.join(eyes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
