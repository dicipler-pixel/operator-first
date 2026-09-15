# ACC representation-rescue experiment

Date: 2026-09-15
Branch: `acc-representation-rescue-2026-09-15`

## Why this exists

SauersML/group-approximation reported on 2026-09-14 that, in its stable-AC fake-surface certification pipeline, a default presentation solved 2,952,729 complexity-6 cases, alternate spanning-tree presentations rescued 14,426 additional cases, and a bounded product-search/backtracking stage rescued the remaining 178 trivial cases. That external result is **search inspiration only** here.

Relevant upstream commits:

- `SauersML/group-approximation@c23a75e269f9c7ee1b2559718eb223c2a6fa1a5b` — complexity-6 exhaustive stable-AC certificate run.
- `SauersML/group-approximation@9b35cbe844ca78319fca53bf51f5cac460f62fea` — corrected fake-surface census and independent certificate checker through complexity five.

## What this branch tests

`representation_rescue.py` separates two ideas that must not be conflated:

1. **Representation eye.** Measure whether equivalent relator views expose a very different eliminability signal. This is an observation/routing feature, not a certificate.
2. **Ordinary-AC unstick search.** Run a bounded search using only relator inversion, relator multiplication, relator conjugation by one generator letter, and relator swap. The target is a state where a generator occurs exactly once in a relator.

The search objective is deliberately different from shortest total relator length. A state can be slightly longer but structurally easier if it creates a unique occurrence that enables elimination.

## Hard boundary

This branch does **not** claim:

- that SauersML's stable-AC certificates are ordinary-AC SAIR paths;
- that changing a spanning tree is an ordinary-AC move;
- that finding a unique generator occurrence solves a challenge instance;
- that the internal Python replay is the official SAIR verifier;
- any new leaderboard result.

Every score-changing candidate still needs literal replay under the frozen official SAIR grammar and then comparison against current authenticated pricing.

## Usage

Self-test:

```bash
python experiments/acc/representation_rescue.py --self-test
```

Run on a literal rank-two state:

```json
{
  "rels": [[1, 2, -1, 2], [1, 1, -2]],
  "max_depth": 6,
  "max_states": 50000,
  "length_cap": 40
}
```

```bash
python experiments/acc/representation_rescue.py input.json
```

Signed integers encode free-group letters: `1=x`, `-1=x^-1`, `2=y`, `-2=y^-1`.

## Next experiment

Feed the current hard ordinary-AC frontier states and stalled SAIR challenge states through this instrument. Record, per state:

- baseline total/max relator length;
- baseline unique-occurrence count;
- best equivalent-view unique-occurrence count;
- whether bounded ordinary-AC search reaches an eliminable state;
- states explored and depth;
- exact emitted path;
- official replay result;
- whether the path improves, ties, or merely changes routing information.

Only the last two items can justify promotion as challenge progress.
