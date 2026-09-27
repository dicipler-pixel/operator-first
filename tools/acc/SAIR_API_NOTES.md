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
