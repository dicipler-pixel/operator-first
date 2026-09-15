from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, KeepTogether, HRFlowable)

INK   = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#5a5a5a")
RULE  = colors.HexColor("#c8c8c8")
BAND  = colors.HexColor("#eef1f4")
ACC   = colors.HexColor("#8a3324")

ss = getSampleStyleSheet()
def S(name, **kw):
    base = kw.pop("parent", ss["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

TITLE   = S("TITLE", fontName="Times-Bold", fontSize=23, leading=27, textColor=INK, spaceAfter=6)
SUBT    = S("SUBT", fontName="Times-Italic", fontSize=12.5, leading=16, textColor=MUTED, spaceAfter=20)
H1      = S("H1", fontName="Times-Bold", fontSize=15, leading=19, textColor=INK, spaceBefore=18, spaceAfter=7)
H2      = S("H2", fontName="Times-Bold", fontSize=11.5, leading=15, textColor=ACC, spaceBefore=12, spaceAfter=4)
BODY    = S("BODY", fontName="Times-Roman", fontSize=10.4, leading=14.6, textColor=INK,
            alignment=TA_JUSTIFY, spaceAfter=7)
LEAD    = S("LEAD", parent=BODY, fontSize=11.2, leading=15.8, spaceAfter=9)
BULLET  = S("BULLET", parent=BODY, leftIndent=15, bulletIndent=4, spaceAfter=4)
CODE    = S("CODE", fontName="Courier", fontSize=8.1, leading=10.4, textColor=INK,
            leftIndent=10, spaceBefore=4, spaceAfter=8)
QUOTE   = S("QUOTE", fontName="Times-Italic", fontSize=10.6, leading=14.8, textColor=INK,
            leftIndent=18, rightIndent=14, spaceBefore=6, spaceAfter=8)
CAP     = S("CAP", fontName="Times-Italic", fontSize=8.7, leading=11.5, textColor=MUTED, spaceAfter=12)
FOOT    = S("FOOT", fontName="Times-Roman", fontSize=8.6, leading=11.5, textColor=MUTED)

def rule(sp=8):
    return [Spacer(1, sp/2), HRFlowable(width="100%", thickness=0.6, color=RULE), Spacer(1, sp)]

def tbl(data, widths, head=True, align=None, size=8.8):
    t = Table(data, colWidths=widths, hAlign="LEFT")
    st = [("FONT",(0,0),(-1,-1),"Times-Roman",size),
          ("TEXTCOLOR",(0,0),(-1,-1),INK),
          ("VALIGN",(0,0),(-1,-1),"TOP"),
          ("TOPPADDING",(0,0),(-1,-1),3.5),
          ("BOTTOMPADDING",(0,0),(-1,-1),3.5),
          ("LEFTPADDING",(0,0),(-1,-1),6),
          ("LINEBELOW",(0,0),(-1,-2),0.25,RULE)]
    if head:
        st += [("FONT",(0,0),(-1,0),"Times-Bold",size),
               ("BACKGROUND",(0,0),(-1,0),BAND),
               ("LINEBELOW",(0,0),(-1,0),0.7,MUTED)]
    if align:
        for col,a in align.items(): st.append(("ALIGN",(col,0),(col,-1),a))
    t.setStyle(TableStyle(st))
    return t

def pagenum(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 8.5)
    canvas.setFillColor(MUTED)
    if doc.page > 1:
        canvas.drawCentredString(LETTER[0]/2, 0.55*inch, str(doc.page))
        canvas.setFont("Times-Italic", 7.6)
        canvas.drawString(0.95*inch, LETTER[1]-0.62*inch,
                          "An Application Method for Solving Tough Problems")
        canvas.drawRightString(LETTER[0]-0.95*inch, LETTER[1]-0.62*inch, "Beasley")
        canvas.setStrokeColor(RULE); canvas.setLineWidth(0.4)
        canvas.line(0.95*inch, LETTER[1]-0.72*inch, LETTER[0]-0.95*inch, LETTER[1]-0.72*inch)
    canvas.restoreState()

story = []
A = story.append

# ---------------------------------------------------------------- title page
A(Spacer(1, 1.15*inch))
A(Paragraph("An Application Method for Solving Tough Problems "
            "and Recording Their Solutions for Pure Understanding", TITLE))
A(Paragraph("A working method, and the day of Andrews&ndash;Curtis search that produced it", SUBT))
A(HRFlowable(width="38%", thickness=1.1, color=ACC, hAlign="LEFT"))
A(Spacer(1, 16))
A(Paragraph("<b>Jeromie N. Beasley</b><br/>"
            "<font size=9.4 color='#5a5a5a'>Logic, theory, planning and research direction. "
            "Mathematical assistance by AI, credited as assistance.</font>", BODY))
A(Spacer(1, 4))
A(Paragraph("<font size=9.4 color='#5a5a5a'>Edition 1 &middot; 15 September 2026 &middot; "
            "operator-first research programme</font>", BODY))
A(Spacer(1, 26))

A(Paragraph("Abstract", H2))
A(Paragraph(
  "This document sets out a method for attacking problems that resist direct assault, and for "
  "recording what is learned so that the record is worth more than the answer. The method is not "
  "described in the abstract: it is derived from a single day's work on the Andrews&ndash;Curtis "
  "search problem, in which 182 challenges were measured exhaustively, 94 graph components "
  "enumerated, one exact theorem proved, three claims retracted, two certificates produced for "
  "problems that direct search could not solve, and every step written into an append-only "
  "hash-chained ledger that now holds 2,463 events.", LEAD))
A(Paragraph(
  "The central claims are procedural. Measure complete populations rather than samples, because "
  "a sample that mixes incomparable cases produces confident nonsense. When a pattern appears, "
  "hunt for its mechanism instead of collecting more instances of it, because a mechanism "
  "predicts and a pattern only summarises. Prefer methods that can prove a negative. Record "
  "failures with the same care as results, and never rewrite a record: supersede it. Each rule "
  "below is paired with the specific error that taught it.", BODY))
A(Spacer(1, 18))
story.extend(rule(6)[1:])
A(Paragraph("Contents", H2))
toc = [["1.", "The problem this method is for"],
       ["2.", "Seven rules, and the error behind each"],
       ["3.", "The record: what an append-only ledger is for"],
       ["4.", "Worked application: Andrews\u2013Curtis, 15 September 2026"],
       ["5.", "What was proved, what was measured, what was withdrawn"],
       ["6.", "Limits of this account"]]
A(tbl(toc, [0.35*inch, 5.0*inch], head=False, size=9.6))
A(PageBreak())

# ------------------------------------------------------------------- part 1
A(Paragraph("1.&nbsp;&nbsp;The problem this method is for", H1))
A(Paragraph(
  "Some problems yield to effort. You push, and the thing moves. This method is not for those.", BODY))
A(Paragraph(
  "It is for problems where effort alone produces a confident wrong answer: where the search "
  "space is too large to exhaust, where every measurement is expensive, where patterns appear in "
  "the data that are artefacts of how the data was gathered, and where the person doing the work "
  "is also the person checking it. Under those conditions the ordinary failure is not "
  "getting stuck. It is getting a result, believing it, and building on it.", BODY))
A(Paragraph(
  "The method that follows is therefore mostly defensive. Its rules are about what to measure, "
  "what to trust, and what to write down &mdash; and its value is that each rule has a scar "
  "behind it. None of them is offered as a principle derived from first thought. Every one is "
  "the residue of a specific mistake, made and caught during the work described in section 4.", BODY))

A(Paragraph("Why &ldquo;for pure understanding&rdquo;", H2))
A(Paragraph(
  "A solution that cannot be replayed is a rumour. A solution that can be replayed but whose "
  "false starts have been deleted is a lie of omission: it makes the path look inevitable and "
  "teaches the reader nothing about how to walk it. The recording half of this method exists so "
  "that a reader &mdash; including the author, six months later &mdash; can reconstruct not only "
  "what was concluded but what was believed at each point and why it changed.", BODY))
A(Paragraph(
  "That is what is meant by pure understanding here: the record is kept for comprehension, not "
  "for credit. It is optimised so that the wrong turns remain legible.", BODY))

# ------------------------------------------------------------------- part 2
A(Paragraph("2.&nbsp;&nbsp;Seven rules, and the error behind each", H1))

A(Paragraph("Rule 1 &mdash; Measure a complete population, never a convenient sample", H2))
A(Paragraph(
  "A sample is only as good as the comparability of what it contains. If the units differ in a "
  "way that matters and the sampling mixes them, every aggregate statistic is meaningless while "
  "still looking perfectly ordinary.", BODY))
A(Paragraph(
  "<b>The error.</b> An early claim held that component sizes in the search graph were quantised "
  "&mdash; that they took only a few values pool-wide. The evidence was 19 challenges showing 7 "
  "values. It was false, and a uniform random census refuted it: 30 closed components, 30 "
  "distinct sizes. The cause was that the sampling script sorted by length before sharding, so "
  "the original 19 were concentrated in two narrow profiles.", BODY))
A(Paragraph(
  "<b>The deeper cause, found later.</b> The refuting census was itself comparing incomparable "
  "things. Challenges of different initial length live in <i>different graphs</i>; their "
  "component sizes carry no information about one another. Both the claim and its refutation "
  "were measuring an artefact. The fix was to fix the profile &mdash; measure every challenge of "
  "one exact length &mdash; at which point the pattern reappeared, legitimately, and replicated "
  "on a second profile.", BODY))

A(Paragraph("Rule 2 &mdash; When a pattern appears, hunt the mechanism, not more instances", H2))
A(Paragraph(
  "More instances of a pattern raise confidence without raising understanding, and confidence "
  "without understanding is precisely the failure mode of rule 1. A mechanism, by contrast, "
  "makes a prediction about cases not yet seen.", BODY))
A(Paragraph(
  "<b>The near miss.</b> Five component sizes in one profile shared a common factor of 36. That "
  "invites a law. Testing the factor against the wider set of 42 measured components killed it "
  "immediately &mdash; but the same test revealed that <i>all</i> 42 were divisible by 4, with "
  "greatest common divisor exactly 4. Rather than collect more, the question became: why 4?", BODY))
A(Paragraph(
  "The answer was a two-line symmetry argument, given in full in section 5, that explains every "
  "measurement and predicts all future ones. Fifty-two components have been measured since it "
  "was written. All 94 comply.", BODY))

A(Paragraph("Rule 3 &mdash; Prefer a method that can prove a negative", H2))
A(Paragraph(
  "A search that fails to find something has found nothing. An exhaustive enumeration that "
  "fails to contain something has proved it is absent. The difference is not one of degree.", BODY))
A(Paragraph(
  "<b>The application.</b> Two methods were available for grouping related problems: search for "
  "a transformation between them, or enumerate the component containing one and check whether "
  "the other is in it. These turn out to define the same relation. But the first can only ever "
  "prove that two problems <i>are</i> related; the second, when the enumeration completes, also "
  "proves that two problems are <i>not</i> &mdash; which is the fact that lets you stop trying.", BODY))

A(Paragraph("Rule 4 &mdash; A negative result from an unvalidated instrument is not a result", H2))
A(Paragraph(
  "<b>The error.</b> A test was written to determine whether two problems shared a component. It "
  "called the official verification library with the wrong number of arguments, inside a "
  "<font face='Courier' size='8.6'>try/except Exception: continue</font>. Every call raised, "
  "every exception was swallowed, the search frontier was empty at every depth, and the script "
  "reported &ldquo;not reachable&rdquo; &mdash; a negative result from a search that never ran.", BODY))
A(Paragraph(
  "It was caught only because a breadth-first search reporting one state at depth eight is "
  "visibly broken. Had the numbers looked plausible, a false claim would have been published. "
  "The rewrite asserts that the move function produces successors <i>before</i> trusting any "
  "negative answer.", BODY))

A(Paragraph("Rule 5 &mdash; Cross-validate against something you did not build", H2))
A(Paragraph(
  "Self-consistency is cheap. Two independent implementations agreeing is evidence; one "
  "implementation agreeing with itself is not.", BODY))
A(Paragraph(
  "<b>The application.</b> A collaborator's search pass reported an eight-move ball of "
  "24,587,144 states around the solved endpoint. Because the move set is closed under inverses, "
  "the same object could be computed here by an unrelated implementation running in the opposite "
  "direction. It returned 24,583,188 &mdash; agreement to 99.98%, with the residual 3,956 states "
  "accounted for exactly by this implementation's 64-letter representation limit. The "
  "collaborator's claim of no truncation was corroborated from outside, and a hard limit of the "
  "local engine was quantified in the same stroke.", BODY))

A(Paragraph("Rule 6 &mdash; Supersede, never rewrite", H2))
A(Paragraph(
  "A record that can be edited is a record of what you currently believe. A record that can only "
  "be appended to is a record of what you believed and when. Only the second can be audited, and "
  "only the second teaches anything.", BODY))
A(Paragraph(
  "In practice: when a claim is withdrawn, the withdrawal is a new entry naming the old one and "
  "stating what broke it. The original stays exactly as written. This applies to commit messages "
  "and to the event ledger alike, and it is enforced mechanically &mdash; the ledger is a hash "
  "chain, so editing any entry breaks every later link.", BODY))

A(Paragraph("Rule 7 &mdash; Instrument gaps are findable before they bite", H2))
A(Paragraph(
  "The most expensive failures are not wrong answers but unasked questions, and those come from "
  "instruments that cannot express the question.", BODY))
A(Paragraph(
  "<b>The application.</b> The search engine had the target hard-coded. It could therefore answer "
  "only &ldquo;is the solution in this component?&rdquo; and never &ldquo;are these two problems "
  "in the same component?&rdquo; &mdash; so the component structure was invisible, and remained "
  "invisible for as long as nobody looked at the instrument rather than through it. Making the "
  "target a parameter took twenty minutes and immediately produced results the previous engine "
  "could not have expressed.", BODY))

A(PageBreak())

# ------------------------------------------------------------------- part 3
A(Paragraph("3.&nbsp;&nbsp;The record: what an append-only ledger is for", H1))
A(Paragraph(
  "The recording half of the method is a single append-only event stream. Every input, state, "
  "observation, failure, decision and relationship is written to it once and never rewritten. "
  "Reports are derived from it; they never replace it. At the time of writing it holds 2,463 "
  "events.", BODY))
A(Paragraph("Four properties, each with a test that tries to break it", H2))
A(tbl([
  ["Property", "What it guarantees", "How it is enforced"],
  ["Tamper-evident", "editing or deleting any entry is detectable",
   "every event carries the digest of the previous one; verification names the first break"],
  ["Torn-write safe", "a process killed mid-append cannot corrupt data",
   "one line, written under an exclusive lock and fsynced; a short final line fails its own digest and is reported, not parsed"],
  ["Concurrent safe", "two writers interleave records, never bytes",
   "appends take an exclusive lock covering read-tail and write together"],
  ["Exactly typed", "silent numeric corruption is impossible",
   "integers beyond 2^53 are rejected recursively over the whole event, not one field"],
], [1.05*inch, 1.75*inch, 3.0*inch]))
A(Paragraph(
  "A separate external count pin guards the one attack the hash chain cannot see: truncating the "
  "tail. A chain missing its last five entries verifies perfectly. The pin fires.", CAP))

A(Paragraph("The rule that makes it worth keeping", H2))
A(Paragraph(
  "&ldquo;All eyes on&rdquo; means every instrument leaves a record. Mixing may change what "
  "influences a decision; it may never erase what an instrument saw, or failed to see.", QUOTE))
A(Paragraph(
  "The practical form of this is that instruments which contribute nothing are retained at "
  "weight zero <i>with a stated reason</i>, rather than dropped. An instrument that cannot read "
  "a given question files that it cannot, and keeps its place. A silent gap &mdash; an "
  "instrument that claims to have read while producing nothing &mdash; is the one thing the "
  "design forbids, and the integrity check that enforces this caught the author violating it "
  "within an hour of it being written.", BODY))

A(Paragraph("Independence of observation", H2))
A(Paragraph(
  "A later refinement: each hour records independently, and hours are mixed only after they "
  "close. Twelve observations written by one process inside ten milliseconds are not twelve "
  "independent observations, however scrupulously each is labelled. The enforcement is "
  "structural &mdash; one reading per instrument per hour, so there is no second slot to revise "
  "into after seeing how the first landed, and an hour cannot be mixed until it is over, so the "
  "mixed result cannot exist while any reading in it is still being made.", BODY))
A(Paragraph(
  "Co-authored readings are not rejected. They are measured: the mix reports the wall-clock "
  "spread and names any instruments that consumed byte-identical input. Erasure is the failure "
  "mode being avoided; visibility is the remedy.", BODY))

A(PageBreak())

# ------------------------------------------------------------------- part 4
A(Paragraph("4.&nbsp;&nbsp;Worked application: Andrews&ndash;Curtis, 15 September 2026", H1))
A(Paragraph(
  "The Andrews&ndash;Curtis problem asks whether a balanced presentation of the trivial group "
  "can be reduced to the standard one by a fixed set of moves. Concretely, one is given a pair "
  "of words and a set of fourteen legal operations, and asked for a sequence taking the pair to "
  "the trivial pair. The search space is unbounded; the standard approach bounds it by capping "
  "the total length a presentation may reach, and searching that finite graph.", BODY))

A(Paragraph("4.1&nbsp;&nbsp;A reading that changed everything", H2))
A(Paragraph(
  "Exhausting a capped search without finding the target had been recorded as &ldquo;no solution "
  "within budget&rdquo;. Checking the problem set rather than assuming it showed that every one "
  "of the 10,115 targets is the same pair, of total length 2 &mdash; and every cap is at least "
  "17. The target is therefore <i>always</i> inside the capped graph. So:", BODY))
A(Paragraph(
  "An exhausted search does not mean the target is far away. It proves the start and the target "
  "lie in <b>different connected components</b>. What blocks progress is connectivity, not "
  "distance.", QUOTE))
A(Paragraph(
  "This cost one query against the problem file and changed every previous result from a bound "
  "into a disconnection theorem.", CAP))

A(Paragraph("4.2&nbsp;&nbsp;What the instrument could not see", H2))
A(Paragraph(
  "A breadth-first search from a start only ever sees that start's component. Measuring the "
  "component around the <i>solution</i> instead &mdash; the same engine, a different seed &mdash; "
  "showed two radically different objects at the same cap:", BODY))
A(tbl([
  ["Component at cap 47", "States", "Levels", "Branching"],
  ["start of one challenge", "2,464,344 (closed)", "51", "1.33"],
  ["the solved presentation", "> 40,000,000 (budget)", "8+", "~8.6"],
], [1.9*inch, 1.5*inch, 0.8*inch, 0.85*inch], align={1:"RIGHT",2:"RIGHT",3:"RIGHT"}))
A(Paragraph(
  "Provably disjoint. The start is not distant from the solution; it sits in a small closed "
  "pocket while the solution occupies a region holding twenty-four million states within eight "
  "levels.", CAP))

A(Paragraph("4.3&nbsp;&nbsp;Complete profiles", H2))
A(Paragraph(
  "Applying rule 1, ten lengths were measured exhaustively &mdash; every challenge of that "
  "length, no sampling &mdash; giving 182 challenges, 416 search records and 94 fully enumerated "
  "components.", BODY))
A(tbl([
  ["Length", "Cap", "Challenges", "Closed", "Distinct sizes"],
  ["14", "22", "14", "6", "2"],
  ["15", "23", "92", "39", "10"],
  ["37", "45", "30", "8", "4"],
  ["39", "47", "28", "12", "5"],
], [0.85*inch, 0.7*inch, 1.1*inch, 0.85*inch, 1.15*inch],
  align={0:"RIGHT",1:"RIGHT",2:"RIGHT",3:"RIGHT",4:"RIGHT"}))
A(Paragraph(
  "Few sizes over many closed components, replicated on profiles sharing no graph. Whether "
  "equal sizes are equal components is a separate question, settled by search in 4.4 and 5.2. "
  "Lengths 9, 11, 12, 13, 38 and 40 were also completed and are omitted here for size.", CAP))

A(Paragraph("4.4&nbsp;&nbsp;The correction that mattered most", H2))
A(Paragraph(
  "In the length-37 and length-39 profiles, every collision of equal size tested as a distinct "
  "component &mdash; eighteen exhaustive searches, all disjoint. Including one decisive pair "
  "agreeing on both size <i>and</i> depth and still proving distinct.", BODY))
A(Paragraph(
  "Then length 14 produced the opposite. Four challenges reporting identical size were shown to "
  "be <b>one component seen from four roots</b>, the depth spread being nothing but different "
  "basepoints. The deflationary explanation refuted twice was the correct one here.", BODY))
A(Paragraph(
  "And in the same profile, two other pairs:", BODY))
A(Paragraph(
  "one pair: same size, same depth, and the <b>same</b> component.<br/>"
  "another pair: same size, same depth, and <b>different</b> components.", QUOTE))
A(Paragraph(
  "No measurement the instrument reports distinguishes these two cases. Only a search decides. "
  "The tool had been built specifically to detect this outcome, and it did &mdash; which is the "
  "argument for building instruments that can contradict you.", BODY))

A(PageBreak())

# ------------------------------------------------------------------- part 5
A(Paragraph("5.&nbsp;&nbsp;What was proved, what was measured, what was withdrawn", H1))

A(Paragraph("5.1&nbsp;&nbsp;Proved", H2))
A(Paragraph("<b>Theorem.</b> Let <i>G</i> be a connected component of the length-capped "
            "Andrews&ndash;Curtis move graph, and suppose <i>G</i> contains a presentation of "
            "the trivial group. Then 4 divides |<i>G</i>|.", BODY))
A(Paragraph(
  "<i>Proof.</i> Two of the fourteen moves invert the first and second word respectively. Each "
  "is an involution; they act on different coordinates, so they commute and generate a group of "
  "order four. Both are moves, so <i>G</i> is closed under them, and both preserve word length, "
  "so the cap can never block them. A fixed point requires a word equal to its own inverse, "
  "hence of order two; free groups are torsion-free, so that word is empty. But an empty word "
  "leaves a presentation on two generators with one relator, whose abelianisation has rank at "
  "least one and is therefore nontrivial &mdash; impossible, since the moves preserve the "
  "presented group and <i>G</i> contains a trivial-group presentation. So no non-identity "
  "element fixes any state: the action is free, orbits have size exactly four, and 4 divides "
  "|<i>G</i>|. &#9632;", BODY))
A(Paragraph(
  "Status: written from a mechanism when 42 components were known; 52 further components have "
  "been measured since, none available as data at the time of proof. All 94 comply, with "
  "greatest common divisor exactly 4. A single closed component of size not divisible by four "
  "refutes it.", CAP))

A(Paragraph("5.2&nbsp;&nbsp;The transfer result", H2))
A(Paragraph(
  "Problems in the same component share a solution. A certificate for any member transfers to "
  "every other along the connecting path, and that path is bounded by the cap for free. Grouping "
  "two complete profiles:", BODY))
A(tbl([
  ["Profile", "Challenges", "Groups", "Multi-member", "Coverage", "Redundancy removed"],
  ["length 14", "14", "8", "3", "9/14 = 64%", "42.9%"],
  ["length 15", "92", "54", "20", "58/92 = 63%", "41.3%"],
], [0.85*inch, 0.85*inch, 0.62*inch, 0.95*inch, 0.95*inch, 1.2*inch],
  align={1:"RIGHT",2:"RIGHT",3:"RIGHT",4:"RIGHT",5:"RIGHT"}))
A(Paragraph(
  "Sixty-three and sixty-four percent, on profiles sharing no graph. Twelve of the twenty "
  "length-15 groups were found from <i>incomplete</i> enumerations, where positive hits remain "
  "valid though misses do not &mdash; a method restricted to completed searches would have "
  "missed most of them.", CAP))
A(Paragraph(
  "<b>The payoff, verified.</b> One length-14 challenge had a 25-move solution and shared a "
  "component with two challenges that direct search could not solve at all. Concatenating the "
  "transfer path with the known solution:", BODY))
A(Paragraph(
  "transfer 28 + solution 25 = 53 moves &nbsp;&mdash;&nbsp; officially verified<br/>"
  "transfer 33 + solution 25 = 58 moves &nbsp;&mdash;&nbsp; officially verified", CODE))
A(Paragraph(
  "Both accepted by the official verifier on the full concatenated sequence. These are solutions "
  "to problems that direct search could not produce, obtained purely from structure. They are "
  "certificates, not <i>short</i> certificates &mdash; transfer buys existence, and shortening "
  "is a separate problem that can now start from something rather than nothing.", BODY))

A(Paragraph("5.3&nbsp;&nbsp;Withdrawn", H2))
A(Paragraph(
  "Recorded here because the method requires it, and because a list of retractions is the "
  "honest measure of how much a day's confidence was worth.", BODY))
A(tbl([
  ["Claim", "Why it failed"],
  ["Component sizes are quantised pool-wide",
   "refuted by unbiased census; the original sample was concentrated by a sort"],
  ["Solutions require little headroom",
   "generalised from training instances half the size, with solutions less than half as long"],
  ["Length-8 certificates are worthless",
   "assumed without evidence that every team holds them"],
  ["Seven conditional theorems in a proof library",
   "searched for one name, missed two others; actual count was 41"],
  ["Equal component size implies distinct components",
   "true in two profiles, false in a third; four equal-size components were one"],
  ["A profile-wide common factor of 36",
   "did not survive the wider set; caught before being claimed"],
], [2.15*inch, 3.65*inch]))

A(PageBreak())

# ------------------------------------------------------------------- part 6
A(Paragraph("6.&nbsp;&nbsp;Limits of this account", H1))
A(Paragraph(
  "Stating these is part of the method, not an apology for it.", BODY))
A(Paragraph(
  "<b>The measurements are of small components at modest headroom.</b> Of the 416 search "
  "records, 313 stopped on budget: those components exceed forty million states and nothing is "
  "known about them. Every structural statement here concerns the part of the graph that closes.", BULLET, bulletText="\u2022"))
A(Paragraph(
  "<b>The transfer result needs a seed.</b> Grouping is cheap and general; converting a group "
  "into certificates requires that the group already contain one solved member. Length 15 "
  "produced twenty groups and no certificates, because it contained no solved member to "
  "transfer from.", BULLET, bulletText="\u2022"))
A(Paragraph(
  "<b>Nothing here is a competition submission.</b> No result has been priced, submitted or "
  "accepted. The two transfer certificates are almost certainly far from optimal length.", BULLET, bulletText="\u2022"))
A(Paragraph(
  "<b>The generality of the method is untested.</b> It was derived from one problem over one "
  "day. The rules are stated as general because they read as general, not because they have been "
  "shown to transfer &mdash; which is exactly the inference rule 1 warns against, applied to "
  "this document itself.", BULLET, bulletText="\u2022"))

A(Spacer(1, 14))
story.extend(rule(6)[1:])
A(Paragraph("Provenance", H2))
A(Paragraph(
  "Every number in this document is drawn from committed artefacts in the operator-first "
  "repository: raw search records, component groupings, certificate files with move lists, and "
  "the event ledger. Thirty commits were made on the day described. The searches are search "
  "tools only &mdash; every certificate is re-verified by the official competition verifier, "
  "never by a re-implementation.", FOOT))
A(Spacer(1, 8))
A(Paragraph(
  "Author: Jeromie N. Beasley &mdash; logic, theories, planning and research direction. "
  "Mathematical assistance was provided by AI systems and is credited as assistance, not "
  "authorship of the research programme. Licensing follows the repository's mixed policy: "
  "original code and formal proofs under MIT, original scholarly prose under CC BY 4.0.", FOOT))
A(Spacer(1, 8))
A(Paragraph(
  "No part of this document uses the root-conjugacy, donor-restoration, coordinate-transport, "
  "divisibility, period or companion-restoration ideas of Robert Sneiderman (ACC-P000002), so no "
  "such citation is claimed. The divisibility result of section 5.1 concerns a component's "
  "vertex count and the order of a symmetry group, and is unrelated.", FOOT))

doc = SimpleDocTemplate(
    "papers/method/An_Application_Method_for_Solving_Tough_Problems_v1.pdf",
    pagesize=LETTER, leftMargin=0.95*inch, rightMargin=0.95*inch,
    topMargin=0.85*inch, bottomMargin=0.85*inch,
    title="An Application Method for Solving Tough Problems and Recording Their Solutions for Pure Understanding",
    author="Jeromie N. Beasley", subject="Research method and worked application")
doc.build(story, onFirstPage=pagenum, onLaterPages=pagenum)
print("built")
