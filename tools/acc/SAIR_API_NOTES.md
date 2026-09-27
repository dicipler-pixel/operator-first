# SAIR API notes (for pulling our submissions and the live board)

Checked 2026-09-27. Sources searched:
- The official repo `SAIRcompetition/Andrews-Curtis` at a0fd6e6. It has **no API docs**. The README only says "SAIR hosts registration, teams, submissions, and leaderboards".
- The web. Only Terry Tao's post (https://terrytao.wordpress.com/2026/09/11/sair-competition-andrew-curtis-challenge/) turned up, and it has nothing on the API.
- sair.foundation and api.sair.foundation. **Blocked from this Claude container**, so I can't open them. To let Claude call them, add `api.sair.foundation` under the environment's Network access settings.

## 1. CONFIRMED: our team's submissions

```
GET https://api.sair.foundation/api/public/v1/competitions/acc/submissions/mine?limit=20
```
- It needs you to be logged in. It works in the browser tab where you're signed into SAIR.
- The response is `{"ok":true,"data":{"items":[...],"totalCount":N,"nextCursor":"..."}}`.
- Each item has `submissionId, status, receivedAt, solutionCount, results:[{challenge_id, ok, length, problem}], errorMessage`.
- For more pages, `nextCursor` is the key. The query param name is **unconfirmed**. Try `&cursor=<nextCursor>`.

## 2. NOT CONFIRMED: the board / records by other teams

We have the board's JSON shape (you pasted it), but not the exact URL:
```
{"ok":true,"data":{"problem":"ac","competitionId":"acc","contractVersion":"acc-discovery-txt-v2",
 "totalCount":10115,"items":[{"problem","challengeId","status","currentBestLength","kTeams"}]}}
```
My best guesses. They are **untested**, so don't trust them until you've seen one work:
```
https://api.sair.foundation/api/public/v1/competitions/acc/challenges?problem=ac
https://api.sair.foundation/api/public/v1/competitions/acc/leaderboard
```
Records by other teams show up as `currentBestLength` dropping, or as `kTeams` going up, between two snapshots.

## 3. How to get the exact URL yourself (2 minutes)

1. Open the ACC leaderboard / challenges page on competition.sair.foundation while logged in.
2. Press F12 (or right-click → Inspect), open the **Network** tab, and tick **Fetch/XHR**.
3. Reload the page. Click the request whose Response starts with `{"ok":true`.
4. Right-click it → **Copy → Copy URL**. That URL is the "actual wording". Paste the **URL only** to Claude.
5. Do the same on the "My submissions" page for the submissions URL.

**Never paste "Copy as cURL" output, cookies, or `Authorization:` headers** into chat, ReqBin or anywhere else. They contain your login token.

## 4. What to send Claude
- The copied URL (no headers).
- Or the JSON response body. Save it with Response → right-click → "Save as" / copy, then paste or upload it.

From the board JSON, Claude can list every row where another team has a record we don't match.
