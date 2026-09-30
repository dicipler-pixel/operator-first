# UPG-H v0 — Harness Map

**Purpose.** A runtime that uses the same typed objects the papers use for projectors, memory, connection energy, and clocks. It is a control loop, not a theory of everything.

**Sources (do not fuse).**  
- *Universal Projector Geometry* — workspace \(\Pi\), redistribution \(F\), rigidity, persistence.  
- *Light Keeps the Ledger* — metric register vs contour/ledger register.  
- *The Dirac Time of the Gigantefermion* — predictive quotient \(V/N_\infty\), common clock, path ledger.  
- *Non-Normality Is Connection Energy* — \(\mathcal{E}_{\mathrm{sc}}(H)=\mathcal{E}_{\mathrm{conn}}(D)\).  
Electron / Gigantefermion ontology stays **[H]** and is **not** in the kernel.

---

## 1. Picture

A cat in free space has no floor. Balance is internal.

Tennis-racket axes (body frame):

| Axis | Role | Object |
|---|---|---|
| Max inertia | hard to disturb | ledger / memory \(M\), contour \(Z\) |
| Min inertia | cheap local work | metric \(g\), current projector \(\Pi\) |
| Intermediate | unstable on purpose | switch \(\Phi=F\) |
| Space-fixed \(L\) | one general direction | flow \(\dot\tau\) |

Ride the intermediate axis and you flail. Cross it once, keep \(M\) and \(\dot\tau\), and attitude changes.  
Normal \(H\) means the obstruction field is parallel: no switch. Non-normal means the connection is storing energy: that energy *is* the switch.

---

## 2. Typed objects (do not collapse)

### 2.1 Workspace \(\Pi\)
Finite-rank projector. What the job is allowed to see and edit *now*.

### 2.2 Anchor / memory \(M\) (Dirac Time)
Continuation \(L\), readout \(R\):
\[
N_\infty=\{v:RL^nv=0\ \forall n\ge 0\},\qquad
M=V/N_\infty.
\]
Two presents that agree on \(R\) but disagree on later observations are **not** the same state.  
Present closes (no memory needed) iff \(RL=AR\) for some linear \(A\).  
Finite test: agreement on the first \(\dim V\) future observations decides all of them.

**Ops form.** Identity of a candidate is not \((\mathrm{start},|w|)\). Identity is the coarsest invariant that splits known record families (cost per generator/relation, corridor, edit-class). Local search stays inside one cell of \(M\).

### 2.3 Metric register \(g\) (Light)
Intrinsic pairing on projector tangents:
\[
Q(A,B)=\mathrm{Tr}(\Pi A^\dagger B)=g-\tfrac{i}{2}\Omega.
\]
Licence of a contour can fail before \(g\) dies. Degenerate \(g\) is not “no information”; it is “do not trust local geometry.”

### 2.4 Ledger register \(Z\) (Light / UPG winding)
Contour / integer / silence window. Survives amplitude collapse when the contour remains admissible.
\[
Z_f=\frac{1}{2\pi i}\oint_\Gamma f(z)\,\mathrm{Tr}\,(zI-H)^{-1}\,dz.
\]
**Ops form of \(Z\).** The thing that scores, written down: length \(\le\) record on an unheld row; cost per relation use \(=1\); JSON line with record fields; heartbeat; resume step. Prose is not \(Z\).

### 2.5 Switch \(\Phi\) (Non-normal note + UPG \(F\))
Working operator \(H=D+A\).
\[
\Phi=\mathcal{E}_{\mathrm{sc}}(H)=\|[H,H^\dagger]\|_F^2=\mathcal{E}_{\mathrm{conn}}(D).
\]
\(H\) normal \(\iff\) \(D\) parallel \(\iff\) \(\Phi=0\).

Legal proposal channel:
\[
F(\Omega,\Pi)=(I-\Pi)\Omega\Pi+\Pi\Omega(I-\Pi).
\]
Complementary blocks only. Trace-free.  
**Ops rule.** \(\Phi\) counts as fired only if the scoring complement changes: new family seed, foreign-pool merge, new capture schema, new board filter. Wider beam / restart / window on the same seed is \(\Phi=0\) even if the process is hot.

### 2.6 Flow \(\dot\tau\) (Dirac Time common clock)
\[
R^\dagger HR-i\hbar R^\dagger\dot R=\dot\tau\,H_0+a(t)I.
\]
Many internal rhythms become one time only if gaps co-scale. Geometry cannot fix the second.

**Ops clocks (declare separately; never average):**
- search
- container idle
- per-call (hard cap + persist)
- pool merge
- send
- board eligibility

If two disagree, split the job or stop.

### 2.7 Grade ledger
Every claim carries one of: `[T]` theorem/identity, `[V]` numerical gate, `[C]` cited fact, `[L]` Lean-backed finite line, `[H]` reading/hypothesis.  
`[H]` cannot authorize a tool call or a submission.

---

## 3. Runtime loop (one step)

```
1. Ingest task → Π
2. Licence test on Γ / board / row-held
      fail → refuse, write grade, stop
3. Read M: is this present a known twin of a different future?
4. Compute Φ
      Φ ≈ 0 → answer from current Π (local metric / cached tools)
      Φ > 0 → emit only F-legal moves
5. Execute tools with per-call cap + heartbeat + persist
6. Update M from what future observations can still see; drop N∞
7. Write Z (integer / constraint / file line), not the narrative
8. Grade the move
9. Common-clock check; if clocks disagree, split or stop
```

Flailing = large \(\Phi\) with no \(F\) channel.  
Frozen = \(\Phi=0\) on the wrong \(\Pi\).  
Balance = \(M\) held, one real \(F\), \(\dot\tau\) unchanged.

---

## 4. Refusal / fail-closed

Refuse when:

- contour / board licence is closed
- proposed move is not \(F\)-supported (same-family cosmetics sold as a switch)
- clocks disagree and no split is declared
- claim grade is `[H]` but the act is a submission or a kernel write
- observation \(R\) cannot tell hit from miss, live from dead, valid from scoring

Silence is a legal output. Guessing is not.

---

## 5. Observation \(R\) (must be able to see)

A live lane and a dead lane must differ in \(R\).  
A hit and a non-hit must differ in \(R\).  
A valid route and a scoring route must differ in \(R\).

Minimum bits:

- heartbeat
- cap-file / JSON write with record fields
- length \(\le\) record
- row not already held
- family / cost invariant
- which clock is running

If \(R\) lacks a bit, that distinction lives in \(N_\infty\) and will leak.

---

## 6. Failure species (from the first ACC set)

Use these names when annotating new misses.

**S1 Present twins, future strangers**  
Same start / length class / relation-use count / “our best,” different future. Fix \(M\) and \(R\).

**S2 Switch without leaving the family**  
Tools moved, scoring complement did not. Do not count as \(\Phi>0\).

**S3 Several clocks sold as one time**  
Search vs container vs send vs board vs session pool. Fail common-clock.

**S4 \(Z\) not written**  
Constructor or search found the object; the ledger line was never minted.

One knob per batch: licence/\(R\), \(\Phi\) gate, or what may enter \(M\). Do not retune all three at once.

---

## 7. What is in / out of the kernel

**In:** \(\Pi\), \(M=V/N_\infty\), \(g\) vs \(Z\), \(\Phi=\mathcal{E}_{\mathrm{sc}}=\mathcal{E}_{\mathrm{conn}}\), \(F\), \(\dot\tau\), grades, refusal.

**Out of kernel ([H] only):** electron as knot of memory, Gigantefermion, “universe uses this harness,” any physical assignment of light/matter beyond the finite algebra.

Lean companions are optional verifiers for finite identities, not the runtime.

---

## 8. Pass-around questions (for suggestions)

1. Is family-as-\(M\) the right coarsening, or is there a cheaper invariant that already splits record families?  
2. Is “\(\Phi\) fires iff scoring complement changes” too strict for exploratory nights?  
3. Which clocks must be first-class in your stack (idle reclaim, batch send, shared pool)?  
4. Should merge of foreign pools be automatic on a short cadence, or an explicit \(F\)?  
5. What is the smallest \(R\) your watcher can actually implement tonight?  
6. Where does this map overclaim relative to the papers (especially `[H]` leakage)?

---

## 9. One-line spec

**Hold the ledger and the predictive quotient. Spend connection energy only to change the complementary sector that scores. Never treat disagreeing clocks as one time. Write \(Z\) or refuse.**
