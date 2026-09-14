"""Attacks on hourly independent eye recording. Each one tries to break a
property eye_hour_v1 claims. A test that cannot fail proves nothing, so every
attack below is run against a real ledger in a temp dir and must be REPELLED.

Written after the failure it exists to prevent: on 2026-09-14 twelve eye
readings were appended inside ten milliseconds by one author in one loop.
Attack 4 is that exact event, replayed, and it is not repelled -- it is
MEASURED. Co-authorship is not forbidden; hiding it is.
"""
import datetime as _dt
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eye_hour_v1 import HourlyEyes, now_hour, hour_of  # noqa: E402

PASS, FAIL = [], []


def repelled(name, fn, expect):
    try:
        fn()
    except ValueError as e:
        if expect.lower() in str(e).lower():
            PASS.append(name); print(f"  REPELLED  {name}"); return
        FAIL.append((name, f"wrong reason: {e}"))
        print(f"  LEAKED    {name}: wrong reason: {e}"); return
    FAIL.append((name, "attack succeeded"))
    print(f"  BREACHED  {name}: the attack succeeded")


def held(name, cond, detail=""):
    (PASS if cond else FAIL).append(name if cond else (name, detail))
    print(f"  {'OK       ' if cond else 'BROKEN   '} {name}{'' if cond else ': ' + detail}")


def main():
    tmp = tempfile.mkdtemp()
    he = HourlyEyes(tmp)
    ITEM = "test:item"
    prev = hour_of(_dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(hours=2))

    print("attacks on eye_hour_v1\n")

    # 1. Two readings from one eye in one hour: revising after seeing the mix.
    he.record("eye-a", ITEM, "observed", read={"x": 1}, output={"v": 1}, hour=prev)
    repelled("1. second reading from the same eye in the same hour",
             lambda: he.record("eye-a", ITEM, "observed", read={"x": 2},
                               output={"v": 999}, hour=prev),
             "one reading per eye per hour")

    # 2. Mixing an hour that is still running.
    he.record("eye-b", ITEM, "observed", read={"x": 3}, output={"v": 3})
    repelled("2. mixing the current, still-open hour",
             lambda: he.mix(ITEM, now_hour()), "still open")

    # 3. Feeding one eye another eye's reading as its input.
    repelled("3. an eye handed another eye's reading as input",
             lambda: he.record("eye-c", ITEM, "observed",
                               read={"prior": {"eye_id": "eye-a", "output": {"v": 1}}},
                               output={"v": 1}, hour=prev),
             "records independently")

    # 4. The 2026-09-14 failure replayed: many eyes, one loop, one instant.
    #    NOT repelled. Measured.
    tmp2 = tempfile.mkdtemp()
    batch = HourlyEyes(tmp2)
    for i in range(8):
        batch.record(f"batch-eye-{i}", ITEM, "observed",
                     read={"same": "input"}, output={"i": i}, hour=prev)
    m = batch.mix(ITEM, prev)
    held("4. a co-authored batch is recorded, not rejected", m["readings"] == 8)
    held("4a. and is FLAGGED as co-authored", m["co_authored"] is True,
         f"wall_spread_ms={m['wall_spread_ms']}")
    held("4b. and its shared input digest is named",
         len(m["shared_input_digests"]) == 1
         and len(next(iter(m["shared_input_digests"].values()))) == 8,
         str(m["shared_input_digests"]))

    # 5. An excused state with no reason: the silent gap the design forbids.
    repelled("5. 'blocked' filed with no reason",
             lambda: he.record("eye-d", ITEM, "blocked", read={}, hour=prev),
             "must carry a reason")

    # 6. 'observed' with nothing observed.
    repelled("6. 'observed' filed with no output",
             lambda: he.record("eye-e", ITEM, "observed", read={}, hour=prev),
             "must carry an output")

    # 7. Recording into an hour that has not happened.
    future = hour_of(_dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(hours=3))
    repelled("7. recording into a future hour",
             lambda: he.record("eye-f", ITEM, "observed", read={}, output={"v": 0},
                               hour=future),
             "has not happened yet")

    # 8. The blocked eye keeps its place: excused, weight zero, never dropped.
    he.record("eye-g", ITEM, "blocked", read={},
              reason="no input it can see this hour", hour=prev)
    mix = he.mix(ITEM, prev)
    held("8. a blocked eye stays on the roster in the mix",
         "eye-g" in mix["eyes"] and "eye-g" in mix["excused"])

    # 9. The chain still verifies after every attack.
    seen, problems = he.log.verify()
    held("9. hash chain intact after all attacks", not problems, str(problems))

    print(f"\n{len(PASS)} held, {len(FAIL)} broken")
    for f in FAIL:
        print("  BROKEN:", f)
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
