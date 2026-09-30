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

## Optional recovery from a known shortening failure

Astra caught `acc_window` exiting 3 with `FATAL walk to s_j failed` on both
ac-03068 routes. The raw beam routes AC51/SAC53 passed the pinned official
verifiers, but neither shortening completed. The cause remains unresolved.

With `ASTRA_VERIFIED_WINDOW_FALLBACK=1`, only this exact reconstruction error
may retain the original window input. The hook requires the pinned SAIR checkout,
replays the literal input using official `core.verify` and manifest limits, and
requires arrival at `(x,y)`. It rejects failed output containing `FINALPATH`.
It preserves the actual nonzero exit and a `verified_input_fallback` explanation
in the audit receipt; the unchanged runner then uses its existing input-path
fallback. No shortened path or optimality is claimed. The local literal-input
check is not a board certificate: final AC/SAC paths still require verification
against their actual manifest challenge before inboxing.

This option never permits failed beam executions, other window errors, or invalid
input paths. Without it all nonzero exits still stop the runner. Five additional
checks cover a valid input, an invalid input, another exit code, failed output
containing FINALPATH, and the required opt-in. The original four guard checks
continue to pass. Inspect audit receipts for every fallback when checkpointing.
