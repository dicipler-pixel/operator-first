import ElementalFoundations
example : ElementalFoundations.transmission 1 (1/10) =
    ElementalFoundations.transmission (-1) (1/10) := by
  norm_num [ElementalFoundations.transmission, ElementalFoundations.denominator,
    ElementalFoundations.characteristic]
