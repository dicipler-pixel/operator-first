# Chill plan (Oct 6): save model time, keep scoring

## What happened
- **Oct 1 (high burn, high return):** about 46 accepted lines (28 sent by UPG-H, 18 by the owner), 5 beats, rank 9.
  - The cost was a week of Claude usage in one day: 15-minute sweeps, 60-second inbox monitors that woke the coordinator, a Fable subagent (~170k tokens for one job, then the weekly limit), song and paper games (many turns each), and 3–4 Claude sessions writing notes to each other.
- **Oct 2–4 (UPG-H offline):** Astra (GPT) coordinated, with Team 1 (Grokboto/SuperGrok) and Team 2 (Sol/DeepSeek). Colab and local runs: about 8 meet-in-the-middle windows (300 s, ~10M states, ~2 GB sqlite each), plus one 16-second Colab run.
  - **Every one ended INCOMPLETE on its timer, with no candidate.** Two owner submissions (#3052 with 11 lines, #3231 with 4).

## Why Colab and the bots were not productive
1. Each scope was bigger than its time cap, so every run timed out. An INCOMPLETE run teaches nothing; it is not even a scoped miss.
2. 2 GB checkpoints were saved and never resumed.
3. Orders, leases and receipts cost more than the compute did.
4. Window searches inside held roads: Kernel showed (Oct 1) that a tie on those rows needs a road at least 5 moves away from every held road. Windows stay inside that tube.

## What paid, per unit of model time (all of it is plain CPU scripts, 1–8 min each)
- Global height / Stable / recognition / twist webs: about 30 ties and a beat.
- Session 2's fixpoint loop on CONSTRUCTED roads: 2 beat pairs.
- Lost-submission audits: free ties.

## The plan
- **A. CPU is free; model time is the budget.** Every job is a script that runs to a natural end and writes a `LINES_*.txt`. No model watches a running job.
- **B. One Claude coordinator (UPG-H), 1–2 check-ins a day,** or when the owner pings. Each check-in: collect the LINES files, run `plan_offline` on a fresh board, paste the scoring lines to the owner. Target: at most ~10 tool calls. No monitors, no 15-minute routines, no subagents unless the owner approves one specific job.
- **C. Park the Claude worker sessions** (session 1, session 2, Fable). Their best lanes become scripts in the autopilot below.
- **D. Non-Claude members** (Astra, Grok/SuperGrok, Sol, DeepSeek, Gemini) use other quotas. Keep ONE coordinator for them. Rule: a scope must be sized to FINISH inside its cap, or run unattended for hours; no 300-second timeouts.
- **E. Autopilot on the owner's PC or Colab (no model):** `git pull`, then height web, Stable web, recognition web, twist web and the fixpoint loop on constructed roads, then `plan_offline`, then an `ACC_SUBMIT_OWNER_*.txt` file. At most one read-only board pull per day.

## Decisions (owner, Oct 6 00:20Z)
- The autopilot runs on the **owner's PC**.
- The **owner coordinates the non-Claude members** directly.
- The **Claude worker sessions** (session 1, session 2, Git/session 3, Fable) **finish their current task, post the results, then park**.
- UPG-H checks in **twice a day** (07:52 and 19:52 Central): it collects lines, runs plan_offline on a fresh board and hands the owner the submission in chat.

## Autopilot on the owner's PC (no model, no API, no Lean, nothing to compile)
1. **Repo:** reuse the existing clone of `operator-first` if there is one (`git pull` only fetches what is new). Otherwise make a small one:
   `git clone --depth 1 --single-branch --branch claude/gallant-bardeen-0pgpae https://github.com/dicipler-pixel/operator-first.git`
2. **Verifier:** if a folder of the official SAIR Andrews-Curtis repo is already on file, point at it so nothing downloads: `SAIR_REPO=<that folder>`. On Windows, `set SAIR_REPO=<that folder>`. Otherwise the first run clones it once, about 23 MB, and pins the commit.
3. **Run:** `python3 tools/acc/upgh/autopilot.py` (on Windows, `py tools\acc\upgh\autopilot.py`). It loops, re-running the webs only when new roads arrive, and pushes `ACC_SUBMIT_OWNER_PC_*.txt` plus its road files. `--once` runs a single round; `--no-push` keeps everything local.
4. **Lean / mathlib is never used by the autopilot.** Never run lake or mathlib builds for the ACC work; they re-download the library.
