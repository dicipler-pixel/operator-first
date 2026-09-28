# sac-02257: two long roads between the same states (2026-09-28 22:29 UTC)

The successful route is in `inbox/20260928T2227Z_codex_sac-02257.txt`, accepted by the pinned `stable_core.verify` at 47 moves (certificate sha256:1e002f3ebf92539c4a0e634aebba2a97b2aa70c896729ba431708d6e018f3d99). The prior yx2 route in `sweeps/codex_stable_yx2_20260928.jsonl` is official-valid at 48 moves. Both consist of rank-two moves to (y,x) plus [15,15]. The yx route is saved in `sweeps/codex_stable_yx_alt_20260928.jsonl`.

Replaying every move with the pinned rank-two core gives identical states at old/new indices (0,0), (5,5), (6,6), (7,7), (8,8), (9,9), then (35,34), (36,35), (37,36), (38,37), (44,43), (45,44), (46,45). From state 9 to the next shared state, the old road uses **26** moves and the new road **25**. Both roads peak at total relator length 37.

- Shared start state at index 9: `(XyyXyXYYXYXyxxxx, xxYYY)`, relator lengths (16,5).
- Shared end state at old index 35 / new index 34: `(yXYxYxYYxYx, xYxYxYYxYxYY)`, lengths (11,12).
- Old 26-move segment: `[6,6,11,11,3,8,2,7,3,9,2,10,3,8,4,3,11,4,7,8,1,5,11,2,12,12]`.
- New 25-move segment: `[8,8,8,3,11,11,3,8,2,7,3,9,2,10,3,8,4,3,6,1,5,13,2,9,9]`.

The exact radius-3+4 window tool checks spans <=8 and the radius-5+5 variant spans <=11; neither can see this 26-move replacement. The original radius-6+7 window checks spans <=14 but timed out at 180s without a splice, and even a completed pass would not cover this pair of endpoints. The complete ceiling-16 reverse map cannot see either shared state (their total lengths are 21 and 23). This is a concrete long-route junction: retain several different valid roads, index exact states along each, and splice at a repeated state even when it lies far apart in the two paths. It does not prove 47 is globally shortest.

To reproduce: replay the two raw `sac` arrays without their final two moves from the manifest start and compare state 9 and states 35/34 using `verifier.core.apply_move`, then official-verify the 47-move route with `stable_core`. Only Session 2 sends to SAIR.
