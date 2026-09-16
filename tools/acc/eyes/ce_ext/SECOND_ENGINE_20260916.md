# Second engine — the cross-check, and what it corrects

`engine2.py`. Deliberately independent of `ac_shared_ball_v1.c`: different language,
different state representation (immutable tuples of letters, not two packed `uint64`),
different hashing (Python's own dict, not a hand-rolled open-addressing table), different
traversal bookkeeping. No shared code, no shared data structure. The only thing in common
is the definition of the fourteen moves — which is the thing being cross-checked.

It also asks a question the C engine never asked. That engine reported component **sizes**.
Equal sizes are equally consistent with one graph under two names and with two distinct
graphs that happen to match. This enumerates the component as a **set**.

## Result

`ac-00945` and `ac-05233`, cap 26:

    engine 1 (C)       386,320   CLOSED     386,320   CLOSED
    engine 2 (Python)  386,320   closed     386,320   closed

    set intersection            0
    length profile  (len r0,len r1)  identical, class by class
    degree sequence                  identical
    target (x,y) in component        False for both

## What this settles

**1. The closures now have their second engine.** Two independent implementations agree on
the count, on closure, and on the target's absence. The audit's condition for the word
*theorem* — `(cap, component_size, engine_id, second_engine?)` — is met for this closure:

> no path to `(x,y)` exists inside the enumerated component at total-length cap 26,
> component size 386,320, confirmed by two independent engines.

**2. "One graph, five names" was wrong.** The intersection is **zero**. These are two
*disjoint* components. My earlier claim that the five R7 rows closing at exactly 7,159,020
was "independent confirmation of the transport map, one problem with five identifiers" used
the wrong mechanism. They are not one graph.

**3. The transport map survives, in its correct form.** Identical length profile and
identical degree sequence over 386,320 states is what a symmetry relation produces: the
symmetry carries component A bijectively onto component B, preserving relator lengths and
branching, while the states themselves are different tuples. So the right statement is
**isomorphic and disjoint**, not identical. Equal component size is evidence *for* the
transport relation — just not by the route I claimed.

This is also why the earlier duel showed nothing: `ac-00945` and `ac-05233` sit in isomorphic
components, so no search can distinguish them, which is exactly the measured outcome. The
retraction in `DUEL_RESULT_20260916.md` stands, and now has a mechanism.

## What is still not established

Isomorphism is inferred from two invariants (length profile, degree sequence) over a
386,320-state graph, not exhibited. Exhibiting it means producing the symmetry element and
checking it maps A onto B pointwise. That is the next step if the transport claim is ever
to carry weight, and until then it remains a strong hypothesis rather than a result.
