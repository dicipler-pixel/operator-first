# Compound Eye side scanner — executed result and handoff

9 September 2026. Research programme of Jeromie N. Beasley. The preceding search used separate diagnostics; it did not have the user's actual Compound Eye attached as a side scanner. That integration is now implemented and executed. The main search and the 19:18 hard-backup branch remain unchanged.

## The real instrument is used

The recovered Whole View archive supplies unchanged `machine.py` 1.0.1, registry, append-only histories, dependency scheduler and shared context/cache. Its 204 earlier eye definitions and 33 set versions are retained in the downloadable full instrument. The active graph request has nine observer eyes, three combined set outputs, and one whole-picture output. These are not thirteen independent agents or votes.

Three sets retain their own answers: identity/endpoint; defects/replacement cost; coloring/lateral alternatives. The whole output combines explicit findings and missing evidence. Discrete graph constraints are not forced into the earlier physical linear-observation fusion formula.

The stable local adapter's 1.0/1.1 lineage is preserved. The consolidated `side_scanner/` deployment is separately versioned 1.2.0. Its default focused registry contains only these graph observers; passing an existing --instrument appends versions without replacing old eyes. The focused GitHub folder is not claimed to include all 204 historical implementations; the full downloadable app does.

## Bounded scan actually executed

71 records: original checkpoint,13 ordinary endpoints,16 target-guided endpoints,40 plateau states,and the100-edge necessary-condition survivor. They reduce to64 labelled states and33 labelled union graphs, with7 duplicate records retained for provenance. This is not an isomorphism census. Previously reported but unrecovered96-endpoint raw files are not included in these counts.

All71 native requests returned13 outputs without unexpected execution errors:923 output rows. Counting each distinct layer state once, the neighboring probes covered4,503 legal diagonal flips and21,546 relative vertex transpositions. The best planar input and best one-flip output remain5triples; the best transposition output has7. No winning graph or new overall search record was found.

Five inputs exceed the declared exact joint-budget DP cap and return unavailable, not a guessed minimum. An uncertified union cannot have a certified layer-flip probe. Every failed hypothesis or missing observation remains visible in its set output.

## Finding 1: a combined editing bound invisible to the triple score

For a current graph G and a prospective successful19-vertex no-independent-triple biplanar endpoint G', put A=E(G') minus E(G) and R=E(G) minus E(G'). Every old independent triple must contain an edge of A. Also degree_A(v)>=max(0,10-degree_G(v)): the endpoint minimum degree is at least10 and deletions cannot repair a degree deficit.

Define a(G) as the minimum number of distinct missing edges that simultaneously meet all old-triple and original-degree demands. This is a finite relaxation, ignoring new triples and degree losses caused by deletions, and ignoring the added edges' planarity. Consequently

    |A| >= a(G),
    |R| >= max(0, |E(G)|+a(G)-102).

The minimum-degree input is inherited from the earlier written argument: the triangle-free complement of a successful graph has independent neighborhoods; nine neighbors would give a nonbiplanar K9 in G'. The two planar layers give the102-edge ceiling. No dependence on the newer computational100-edge lower bound is needed for this editing result.

At the original101-edge five-triple checkpoint, the old-triple hitting-set minimum is3. The joint old-triple/degree minimum is **5**, so any successful endpoint needs at least **5 additions and4 removals**, or9 union-edge toggles. Original degrees at vertices3,4,9,17 are8,9,8,9. An explicit five-edge relaxed minimizer is (0,9),(0,17),(2,3),(2,4),(3,9).

At the preserved102-edge five-triple checkpoint, the joint minimum is also **5**, now forcing **at least5 removals**, or10 union-edge toggles. A relaxed minimizer is (0,9),(1,10),(2,4),(3,12),(10,12).

The producer uses a0/1 dynamic program: each missing edge has one stage; states retain a covered-triple mask and saturated degree demands. A separate checker enumerates every missing-edge subset of sizes0..4, without importing the DP or pruning to its relevant edges. It checks974,121 subsets among70 missing edges at101, and919,311 subsets among69 at102. None satisfies both demands. Each displayed five-edge minimizer is independently checked. Thus5 is the exact minimum of this relaxation for each input.

These are necessary endpoint edge-edit bounds, **not shortest flip distances or realizable planar repairs**. Adding the five edges alone would exceed the planar union ceiling. The actual deletions can create additional obstacles. No historical priority over hitting-set or degree-demand optimization is asserted.

## Finding 2: the same union does not mean the same available moves

Five labelled union groups have differing legal-move summaries among their planar decompositions. One identical union has eight distinct layer states with62,66,68,or72 legal flips. Other groups have65/71,61/67,72/76,and72/76 moves.

Cache a union's objective and colorings by graph ID, but keep its face-complex state ID when planning moves. Merging all equal unions or equal scores would erase alternatives. Layer interchange is quotiented; vertex relabeling is not.

The scanner also flags two non-best snapshots with one-flip improvements9->8 and17->16, explicitly not improvements on the five-triple global record. At the original checkpoint, the two flips hitting old bad triples still worsen the total to10 or11 by uncovering new triples: the insertion and removal must be evaluated together.

## Correct unknown status

The100-edge necessary-condition survivor has zero independent triples and exact chromatic number10 by complement matching. It still has no supplied/verified two-layer planar partition. The whole output therefore refuses success and routes it to PARTITION_REQUIRED. C5-based triangle-free charts are marked inapplicable for ordinary near-miss states whose complements contain triangles. Successful-endpoint conditions are not turned into prohibitions on all temporary search states.

## Verification and deployment

The full local integration passes1,180 assertions, including the exact budget controls, direct coloring checks,six malformed/missing-context cases,and preservation checks. A separate finite watcher smoke test observes two atomically supplied snapshots, produces26 outputs, leaves both source hashes unchanged,and exits. It is not left running.

The standalone HTML has actual set toggles,71-record selection,per-eye evidence,a surrounding-state table,and JSON import/export. Twelve Chromium interaction/render checks passed with no JS errors. Testing used set_content because this container blocks file:// navigation; not all user browsers are claimed tested.

The consolidated GitHub deployment passes [run34398175798](https://github.com/dicipler-pixel/operator-first/actions/runs/34398175798) at commit `ce333314f913a72d64693c06f9b37dc92908dcd3`. The downloaded artifact SHA256 is `e76056cf5258a8e229802df40aa46ffb94d3adf9273b6ecabca1a3cda5fc4c10`. Its four deployed source hashes match the delivered bytes:

- machine.py: `df154d77260f040bcc3336e75a6d7cbe1a9a36526ff81ec355303cade6b276f0`
- graph_core.py: `a51d453a7489e7272a9d0300b0a72de2e39aed77ba1bb3ae4b66b496dc41d76c`
- earth_moon_eye.py: `f6277a04ecde82d8dd170f3acd0c772352ed53d5c36652e25962fc756004d12a`
- scan.py: `f607890097d006ac99f7a9903d83fda3a3925577a9c99075271d3faad96431c2`

Replaying that exact deployed adapter on all71 inputs gives exact agreement on all639 observer values with the stable full-application scan after consistent JSON serialization. The first comparison incorrectly contrasted integer histogram keys in memory with string keys loaded from JSON; its140 apparent differences are equal after serialization. The failed test and corrected check are preserved. No scientific output was altered to obtain parity. This is a version/deployment control, not independent mathematics or a new Lean run.

The frozen hard-backup ZIP was rehashed unchanged: `e11c2770f6a80badbf2c661f27605e99a3001d56b1d4a629e9a23d934fcdfa80`.

## Usage and remaining scope

From side_scanner/: `python -S scan.py --out fresh_scan --check-reference-budgets` runs the three repository reference inputs. `--input checkpoint.json` accepts another full or compact graph. `--instrument PATH` appends these versioned observers to a native instrument. Do not use Python -O/-OO; the inherited exact graph checker uses assertions.

The full local bundle supplies run_scanner.py with a bounded directory-watch mode and an offline report viewer. The watch reads snapshots while its process runs; it does not start or change the search. Recommendations are explicit data, not automatic acceptance. Main search is still paused. An active search can feed new complete checkpoints to the watched folder, then independently check any recommended moves before applying them.

The useful next move is coordinated edge replacement: compensate for old edges that must disappear and retain alternate embeddings, rather than following the inserted edge or scalar triple count alone. The scanner has exposed these two concrete missing distinctions; it has not demonstrated a faster winning search or a general Earth–Moon decision procedure.
