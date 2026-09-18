# Compound Eye HARNESS v2 — calibration record

## Verified path calibration

- Exact replay: **PASS**
- Moves: **23**
- Peak total relator length: **20**
- Floor total relator length: **13**
- Ledger-fiber holonomy events: **9**
- Gross shear moves: **8**
- Net shear current: **[0, 0]**
- Net-zero / gross-nonzero shear cancellation: **True**

Largest future-move-profile turns:
[
  {
    "from_length": 20,
    "incoming_move": 0,
    "step": 20,
    "to_length": 20,
    "turn": 1.088321288793649
  },
  {
    "from_length": 19,
    "incoming_move": 5,
    "step": 19,
    "to_length": 20,
    "turn": 0.9845558694400194
  },
  {
    "from_length": 18,
    "incoming_move": 3,
    "step": 6,
    "to_length": 19,
    "turn": 0.6813652537338378
  },
  {
    "from_length": 18,
    "incoming_move": 4,
    "step": 11,
    "to_length": 15,
    "turn": 0.6616763431509892
  },
  {
    "from_length": 19,
    "incoming_move": 3,
    "step": 9,
    "to_length": 18,
    "turn": 0.5504469974542467
  }
]

## Exact cap-14 component calibration

- Component states: **180**
- Distinct crossing children: **1440**
- Boundary edges: **1440**
- Lowest exit length: **15**
- Lowest exits: **16**
- Count-only histogram classes: **1**
- Ordered 14-label channel classes: **16**
- Exact one-hot channel-matrix rank: **7**
- First retention level separating all lowest exits: **labelled_14_channel**

Collision ladder:
[
  {
    "collisions": 15,
    "level": "scalar_total_length",
    "unique_classes": 1
  },
  {
    "collisions": 15,
    "level": "boundary_histogram",
    "unique_classes": 1
  },
  {
    "collisions": 0,
    "level": "labelled_14_channel",
    "unique_classes": 16
  },
  {
    "collisions": 8,
    "level": "exponent_ledger",
    "unique_classes": 8
  },
  {
    "collisions": 13,
    "level": "cyclic_support",
    "unique_classes": 3
  },
  {
    "collisions": 0,
    "level": "magnus2",
    "unique_classes": 16
  },
  {
    "collisions": 0,
    "level": "magnus3",
    "unique_classes": 16
  }
]

## Meaning

The old degree/count eye is correctly retained as a flat reading, not discarded.
The labelled move-response eye recovers the orientation that the count compressed
away. On this boundary it separates all 16 candidates before Magnus escalation.

This does **not** prove any exit is productive. It gives the HARNESS a cheaper,
higher-resolution screen for deciding which candidates deserve path/deep-eye work.
