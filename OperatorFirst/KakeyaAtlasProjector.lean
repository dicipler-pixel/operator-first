import OperatorFirst.KakeyaAtlasFamily

/-! Exact rational rank-one projector for the initial g3 forcing kernel at q=2.
No numerical eigenvalue tolerance and no assumption of the claimed kernel. -/
open scoped BigOperators
namespace OperatorFirst.KakeyaAtlasProjector
abbrev Vec := Fin 7 → ℚ
def dot (x y : Vec) : ℚ := ∑ i, x i*y i
def mode : Vec := ![-1,-1,1,-1,2,-1,-2]
def project (v : Vec) : Vec := fun i => mode i * dot mode v / 13
def target (v : Vec) : ℚ := -v 0
def targetVector : Vec := ![-1,0,0,0,0,0,0]
def constraints (v : Vec) : Fin 7 → ℚ :=
  let w := KakeyaAtlasFamily.witness 2 v
  ![w 0,w 1,w 2,w 3,w 6,w 7,w 4+w 5]

theorem mode_norm_sq : dot mode mode = 13 := by norm_num [dot,mode,Fin.sum_univ_succ]

theorem target_is_dot (v : Vec) : target v = dot targetVector v := by
  norm_num [target,dot,targetVector,Fin.sum_univ_succ]

theorem dot_mode_project (v : Vec) : dot mode (project v) = dot mode v := by
  simp [dot,project,mode,Fin.sum_univ_succ]
  ring

theorem project_idempotent (v : Vec) : project (project v) = project v := by
  funext i
  simp only [project, dot_mode_project]

theorem project_symmetric (u v : Vec) : dot u (project v) = dot (project u) v := by
  simp [dot,project,mode,Fin.sum_univ_succ]
  ring

theorem project_mode : project mode = mode := by
  funext i
  simp [project,mode_norm_sq]

theorem mode_is_kernel : constraints mode = 0 := by
  funext i
  fin_cases i <;> norm_num [constraints,KakeyaAtlasFamily.witness,mode]

theorem kernel_is_mode_line (v : Vec) (h : constraints v = 0) :
    v = fun i => v 2 * mode i := by
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  have h2 := congrFun h 2
  have h3 := congrFun h 3
  have h4 := congrFun h 4
  have h5 := congrFun h 5
  have h6 := congrFun h 6
  norm_num [constraints,KakeyaAtlasFamily.witness] at h0 h1 h2 h3 h4 h5 h6
  funext i
  fin_cases i <;> norm_num [mode] <;> linarith

theorem projected_vector_is_kernel (v : Vec) : constraints (project v) = 0 := by
  funext i
  fin_cases i <;> norm_num [constraints,KakeyaAtlasFamily.witness,project,mode] <;> ring

theorem projector_fixes_kernel (v : Vec) (h : constraints v = 0) : project v = v := by
  have hv := kernel_is_mode_line v h
  conv_rhs => rw [hv]
  funext i
  simp only [project]
  have hd : dot mode v = 13 * v 2 := by
    rw [hv]
    norm_num [dot,mode,Fin.sum_univ_succ]
    ring
  rw [hd]
  ring

theorem target_mode_nonzero : target mode = 1 := by norm_num [target,mode]

theorem projector_target_value : dot targetVector (project targetVector) = 1/13 := by
  norm_num [dot,project,mode,targetVector,Fin.sum_univ_succ]

theorem projector_target_positive : 0 < dot targetVector (project targetVector) := by
  rw [projector_target_value]
  norm_num

theorem exact_first_witness :
    KakeyaAtlasFamily.witness 2 mode = ![0,0,0,0,1,-1,0,0] := by
  funext i
  fin_cases i <;> norm_num [KakeyaAtlasFamily.witness,mode]

theorem kernel_line_iff (v : Vec) : constraints v = 0 ↔ ∃ a : ℚ, v = fun i => a*mode i := by
  constructor
  · intro h
    exact ⟨v 2,kernel_is_mode_line v h⟩
  · rintro ⟨a,rfl⟩
    funext i
    fin_cases i <;> norm_num [constraints,KakeyaAtlasFamily.witness,mode] <;> ring

end OperatorFirst.KakeyaAtlasProjector

#print axioms OperatorFirst.KakeyaAtlasProjector.mode_norm_sq
#print axioms OperatorFirst.KakeyaAtlasProjector.target_is_dot
#print axioms OperatorFirst.KakeyaAtlasProjector.dot_mode_project
#print axioms OperatorFirst.KakeyaAtlasProjector.project_idempotent
#print axioms OperatorFirst.KakeyaAtlasProjector.project_symmetric
#print axioms OperatorFirst.KakeyaAtlasProjector.project_mode
#print axioms OperatorFirst.KakeyaAtlasProjector.mode_is_kernel
#print axioms OperatorFirst.KakeyaAtlasProjector.kernel_is_mode_line
#print axioms OperatorFirst.KakeyaAtlasProjector.projected_vector_is_kernel
#print axioms OperatorFirst.KakeyaAtlasProjector.projector_fixes_kernel
#print axioms OperatorFirst.KakeyaAtlasProjector.target_mode_nonzero
#print axioms OperatorFirst.KakeyaAtlasProjector.projector_target_value
#print axioms OperatorFirst.KakeyaAtlasProjector.projector_target_positive
#print axioms OperatorFirst.KakeyaAtlasProjector.exact_first_witness
#print axioms OperatorFirst.KakeyaAtlasProjector.kernel_line_iff
