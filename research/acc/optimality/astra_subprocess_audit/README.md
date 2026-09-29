# Optional subprocess audit for the unchanged raw beam runner

`run_beam_raw.py` does not check the return code of `acc_beam` or `acc_window`.
A failed beam can therefore be recorded as `nopath`. Session 1 reported this
failure after a CPU change caused SIGILL; Astra separately detected a truncated
T8 file before resuming and rebuilt it before searching.

This opt-in hook preserves the original runner, binaries, arguments, beam
settings and successful outputs. It records each beam/window return code and
raw stdout/stderr, then rejects nonzero exits. A zero-exit beam must also print
explicit AC and SAC result lines. Failures stop the runner before the current
row is appended, so its ordinary checkpoint resume retries that row.

From the repository root, add these two variables to the original launch:

```bash
export PYTHONPATH="$PWD/research/acc/optimality/astra_subprocess_audit${PYTHONPATH:+:$PYTHONPATH}"
export ASTRA_SUBPROCESS_AUDIT_DIR="$PWD/work/astra_subprocess_audit"
```

Then run the same `nohup env BEAM_H=1 ... python3 .../run_beam_raw.py ...`
command from the orders. Enable these variables only for the raw runner.
The hook is inactive unless `ASTRA_SUBPROCESS_AUDIT_DIR` is set.

Check the guard without launching a search:

```bash
python3 research/acc/optimality/astra_subprocess_audit/check_guard.py
```

The four checks cover a nonzero beam exit even when it prints NONE, an empty
zero-exit beam, a valid explicit negative, and a failed window process.
They also check raw-log and return-code receipts. These are reliability checks,
not a validation of the beam's completeness or an optimality claim.

Before resuming after a machine change, rebuild the native binaries and verify
the finish table's complete expected hash. The audit is additional protection;
it does not make a corrupt table trustworthy merely because a process exits zero.
