import SectionIntegrality

/- Deliberately false: at u=0 the section y-coordinate is 3/2, not zero. -/
example : DiophantineEye.sectionY 0 = 0 := by
  norm_num [DiophantineEye.sectionY]
