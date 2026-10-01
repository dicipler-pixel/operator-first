# SAIR API — how to pull the live board (updated 2026-09-27)

Source: two public competitor repos that use the API in working code
(github.com/nahomar/andrews-curtis-solver `solver/sair.py`,
github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE `src/harness/submit.py`).
Official docs (blocked from Claude's machine): https://docs.sair.foundation/docs/endpoints/competitions/acc/
and https://docs.sair.foundation/llms.txt

Base: `https://api.sair.foundation/api/public/v1/competitions/acc`

| What | Method + path |
|---|---|
| **Full AC board (all 10,115 records)** | `GET /discoveries/snapshot?problem=ac` |
| **Full Stable AC board** | `GET /discoveries/snapshot?problem=stable_ac` |
| Team leaderboard | `GET /leaderboard?problem=ac&limit=100` |
| Our submissions | `GET /submissions/mine` |
| Our team / can we submit | `GET /me` |
| Submission rules | `GET /submission-spec` (limits: maxSolutions, maxBodyBytes, dailySubmissions) |
| **Submit** | `POST /submissions` body `{"payload":{"text":"ac-00001: [..]\n..."},"meta":{"description":"..."}}` → 202 + `data.submissionId`; uses daily quota; never retry a POST |
| One submission | `GET /submissions/{id}` → `data.status` queued/…/complete/failed, `data.results[]` |

Our client: `tools/acc/sair_api.py` (check / boards / mine / plan / submit / status).

Headers needed:
- `Authorization: Bearer YOUR_SAIR_API_KEY`  (make a key on the SAIR site under API)
- `Accept: application/json`
- A browser-like `User-Agent` (Cloudflare blocks non-browser agents with error 1010), e.g.
  `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36`

Snapshot reply shape: `{"ok":true,"data":{"problem":"ac","contractVersion":"acc-discovery-txt-v2",
"totalCount":10115,"items":[{"challengeId","status","currentBestLength","kTeams"}, ...]}}`

## ReqBin steps
1. Method **GET**, URL: `https://api.sair.foundation/api/public/v1/competitions/acc/discoveries/snapshot?problem=ac`
2. **Auth** tab → **Bearer Token** → paste your SAIR API key.
3. **Headers** tab → add `User-Agent` with the browser string above, and `Accept: application/json`.
4. **Send**. Save/copy the whole JSON reply and upload it to Claude. Repeat with `problem=stable_ac`.

Safety: ReqBin sees your key. Make a separate key for this, never paste the key into chat,
and delete/revoke it on the SAIR site when done.

## curl alternative (your own computer, key stays local)
```
curl -H "Authorization: Bearer $SAIR_API_KEY" -H "Accept: application/json" \
     -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36" \
     "https://api.sair.foundation/api/public/v1/competitions/acc/discoveries/snapshot?problem=ac" -o board_ac.json
```

## Official endpoint map and scoring rules (owner paste, 1 Oct 2026 ~03:00Z)
Endpoints: competition detail, submission spec, my participation, submit, list/get/download my submissions, leaderboard, my standing, team scoring
challenges, challenge progress (paginated: pageIndex + pageSize + signed snapshotId; `include=initialRelators`; `challengeId=` selects one), complete
challenge snapshot (`/discoveries/snapshot?problem=ac|stable_ac`, no pagination). **There is no Proof Track / Contributor Network endpoint**; that is website only.
- **Scoring:** only teams holding the current shortest verified solution score. With base V and k teams tied at the shortest length, **each gets V * 2^(1-k)**
  (k counts all tied teams, us included): 1 team -> 1, 2 -> 0.5 each, 3 -> 0.25. So joining a record held by m teams pays 2^-m.
  A shorter solution replaces the minimum. **Equal or longer resubmissions by the same team do not create another tie.**
- **Ranking:** exact descending score, then the earliest scoring event at which the team reached its current total, then team ID. Display scores are rounded strings
  (round-half-even, 4 dp); don't sort by them.
- Results: per-solution codes E_UNKNOWN_CHALLENGE (also training IDs), E_PATH_TOO_LONG, E_BAD_MOVE_ID, E_MOVE_NOT_APPLICABLE (move_index, move, reason),
  E_NOT_TARGET (final_shape). An accepted batch consumes quota whatever the outcome. 409 ACC_FREEZE_CONFLICT: re-read the spec before resubmitting. 503 ACC_NOT_READY: retry reads later.
- Stable AC move ids run 0-256 (rank cap 8); AC 0-13. Moves must be integer JSON literals.

## Read budget, 1 Oct (UPG-H, 09:27Z)
- A full `mine` pull costs one read per 20 submissions, so 169 submissions cost 9 reads. Pull it only after 00:00Z, or when it is really needed.
- At the 40-read reserve, `boards`, `mine` and `upgh board` are refused, so `upgh plan` refuses too (stale clocks, S3, by design).
- Until the reset, use `tools/acc/upgh/offline_send_file.py`: scout SEND rows plus queue lines, minus rows we hold, with 0 reads. Then send with `send FILE --lean --yes`, an essential read path of about 4-5 reads per send.
