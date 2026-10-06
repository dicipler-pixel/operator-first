# Owner authorization: UPG-H submits (6 Oct 2026, 15:04Z)

The owner wrote: "i submitted those 5 … you can submit for me im going to work please stay busy long big problems for you and the team tell everyone updates every 30 to 40 mins and try to get the submissions in yoursef every 40 mins or so"

What changes from now on:

- **UPG-H submits.** It uses only `python3 tools/acc/sair_api.py send FILE --yes`. That command pulls fresh boards and history, keeps only unsolved, beat or tie lines that have not been sent, and logs to submit_log.jsonl.
- **When.** About every 40 minutes, and only when verified candidate lines exist. Limits: 40 submissions per day, and 360 GETs per read window with a reserve of 40.
- **Team updates.** A short hub update every 30–40 minutes. Members report to the hub on the same cadence.

Unchanged: never touch 09839, 02257, 09311, 06403, 04718, 05378 or their twins; pin a0fd6e6f.
