# Collision pass at the wall — the ladder does not thin the population

The staged architecture escalates to Magnus/Fox **only on cells where a cheaper recorded
view merges states**. So the number that sizes the deep-eye budget is not the component
size; it is how many states sit in cells of size > 1 at each ladder level.

Measured on the full `ac-02842` cap-19 component, **23,609,984 states**, every state's
signature computed from the same proposals the enumerator already generates:

| ladder level | classes | states in collision cells | largest cell |
|---|---:|---:|---:|
| scalar total length | 7 | 23,609,984 (**100%**) | 17,862,272 |
| R/D/S/U histogram | 14 | 23,609,984 (**100%**) | 11,788,096 |
| **labelled 14-channel** | **734** | 23,609,984 (**100%**) | 420,128 |
| exponent ledger | 1,032 | 23,609,984 (**100%**) | 218,746 |

**Every state is in a collision cell at every level.** The labelled channel — the eye that
separated 16 of 16 on the boundary calibration — yields **734 classes for 23.6 million
states**: a mean cell of 32,166 and a largest cell of 420,128.

## What this does and does not overturn

**It does not overturn the calibration.** The 16/16 separation on the lowest exits is real;
it was independently reproduced in C, record for record. The labelled eye genuinely beats
the count eye there, and the principle behind it — keep the labels, the histogram threw the
orientation away — is sound.

**It does overturn extrapolating that to the interior at scale.** On a 16-element boundary
sample the labelled channel looks like a perfect discriminator. On 23.6M interior states it
compresses by a factor of 32,000. A separation measured at n=16 carries no information about
n=23,609,984, and this is the measurement that shows the gap rather than assuming either way.

Consequently, **if escalation is triggered by "the cell has more than one member", the
escalation population at the wall is the entire component** — which is the outcome the
staged design exists to avoid.

## The design's own answer, and why I could not test it

The design doc says boundary filtering "is the right place to spend expensive response
measurements", and the run order escalates on *boundary* cells, not interior ones. That is a
materially different and much smaller population, and the numbers above do **not** test it.

I could not measure the cap-19 boundary. At cap 18 the component is 106,800 with a boundary
of 805,660 (≈7.5x). Scaling that ratio to a 23.6M component puts the cap-19 boundary near
1.8×10^8 distinct children, past this enumerator's table. So the fair version of the test —
does the ladder thin a *boundary* population at the wall — is open, and the honest statement
is that the interior result above should not be read as settling it.

## What the number does settle

The Census layer is affordable at the wall (121 s for 23.6M states, ~195k states/s). The
**Collision layer's trigger rule is not** — "more than one member" selects everything. A
usable trigger needs either a finer signature than the four levels tested, or a threshold on
cell size, or restriction to the boundary. Which of those is right is a design decision the
measurement now forces rather than defers.

Reproduce with:

    census 19 YXXYx YYYYXyyyx collide
