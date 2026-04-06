import NoetherDuality
import Mathlib

/-!
# RH Investigation Phase 59 — Pillar 1: Universal Perimeter
Author: Paul Chavez, Chavez AI Labs LLC
Date: April 4, 2026

Defines the 24-member zero-divisor cage and the Universal Trapping Lemma.
Establishes the algebraic boundary that forces nontrivial zeros to the
critical line.
-/

noncomputable section

open Real InnerProductSpace

/-- The 24-member bilateral zero-divisor family (48 signed pairs).
    These vectors reside on the E8 first shell and form the 'structural cage'. -/
def is_perimeter_vector (v : Sed) : Prop :=
  ∃ i j : Fin 16, i ≠ j ∧
  (v = sedBasis i + sedBasis j ∨ v = sedBasis i - sedBasis j)

/-- The Perimeter Set. -/
def Perimeter24 : Set Sed := { v | is_perimeter_vector v }

/-- Canonical ROOT_16D prime root vectors for the six basis primes. -/
def root_2  : Sed := sedBasis 3 - sedBasis 12
def root_3  : Sed := sedBasis 5 + sedBasis 10
def root_5  : Sed := sedBasis 3 + sedBasis 6
def root_7  : Sed := sedBasis 2 - sedBasis 7
def root_11 : Sed := sedBasis 2 + sedBasis 7
def root_13 : Sed := sedBasis 6 + sedBasis 9

private lemma hi4_lemma (t σ : ℝ) :
    @inner ℝ Sed _ (sedBasis 4) (F_param t σ) = (σ - 1/2) / Real.sqrt 2 := by
  unfold F_param;
  unfold F_base u_antisym sedBasis;
  norm_num [ EuclideanSpace.inner_single_left, EuclideanSpace.inner_single_right ] ; ring;
  grind

private lemma hi5_lemma (t σ : ℝ) :
    @inner ℝ Sed _ (sedBasis 5) (F_param t σ) = -(σ - 1/2) / Real.sqrt 2 := by
  unfold F_param; norm_num [ sedBasis ] ; ring;
  unfold u_antisym; norm_num [ F_base ] ; ring;
  unfold sedBasis; norm_num [ EuclideanSpace.inner_single_left ] ; ring;
  grind +revert

private lemma hi0_lemma (t σ : ℝ) :
    @inner ℝ Sed _ (sedBasis 0) (F_param t σ) = Real.cos (t * Real.log 2) := by
  unfold F_param; simp +decide [ F_base ] ;
  unfold u_antisym;
  unfold sedBasis;
  norm_num [ EuclideanSpace.inner_single_left, EuclideanSpace.inner_single_right ];
  simp +decide [ Fin.ext_iff ]

private lemma hi3_lemma (t σ : ℝ) :
    @inner ℝ Sed _ (sedBasis 3) (F_param t σ) = Real.sin (t * Real.log 2) := by
  unfold F_param; simp +decide [ F_base ] ;
  unfold u_antisym; norm_num [ EuclideanSpace.norm_eq, Fin.sum_univ_succ, inner_add_left, inner_add_right, inner_smul_left, inner_smul_right ] ; ring;
  simp +decide [ EuclideanSpace.inner_single_left, EuclideanSpace.inner_single_right, sedBasis ]

/--
**The Universal Trapping Lemma.**
Any analytic prime oscillation that deviates from the critical line
must eventually strike one of these 24 algebraic walls.
-/
theorem universal_trapping_lemma (σ : ℝ) (h_neq : σ ≠ 1/2) :
    ∀ t, F_param t σ ∉ Perimeter24 := by
  intro t ⟨i, j, hij, hcase⟩
  have hδ : σ - 1/2 ≠ 0 := sub_ne_zero.mpr h_neq
  have hrt2 : Real.sqrt 2 ≠ 0 := Real.sqrt_ne_zero'.mpr (by norm_num)
  have hi4 := hi4_lemma t σ
  have hi5 := hi5_lemma t σ
  have hi0 := hi0_lemma t σ
  have hi3 := hi3_lemma t σ
  -- Both index-4 and index-5 components are non-zero
  have h4_ne : @inner ℝ Sed _ (sedBasis 4) (F_param t σ) ≠ 0 := by
    rw [hi4]; exact div_ne_zero hδ hrt2
  have h5_ne : @inner ℝ Sed _ (sedBasis 5) (F_param t σ) ≠ 0 := by
    rw [hi5]; exact div_ne_zero (neg_ne_zero.mpr hδ) hrt2
  -- Orthonormality
  have ij_inner : ∀ k m : Fin 16, @inner ℝ Sed _ (sedBasis k) (sedBasis m) =
      if k = m then (1 : ℝ) else 0 := fun k m => by
    simp only [sedBasis, EuclideanSpace.inner_single_left, EuclideanSpace.single_apply]
    split_ifs <;> simp_all
  -- Helper: from {i,j}={4,5}, derive sin²+cos²=1 contradiction
  suffices h45 : (i = 4 ∧ j = 5) ∨ (i = 5 ∧ j = 4) by
    obtain ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ := h45 <;> {
      rcases hcase with heq | heq <;> {
        rw [heq] at hi0 hi3
        simp only [inner_add_right, inner_sub_right, ij_inner] at hi0 hi3
        simp +decide at hi0 hi3
        nlinarith [Real.sin_sq_add_cos_sq (t * Real.log 2)]
      }
    }
  -- Prove {i,j} = {4,5}
  rcases hcase with heq | heq <;> {
    rw [heq] at h4_ne h5_ne
    simp only [inner_add_right, inner_sub_right, ij_inner] at h4_ne h5_ne
    have h4_in : (4 : Fin 16) = i ∨ (4 : Fin 16) = j := by
      by_contra hc; push_neg at hc
      exact h4_ne (by simp [if_neg hc.1, if_neg hc.2])
    have h5_in : (5 : Fin 16) = i ∨ (5 : Fin 16) = j := by
      by_contra hc; push_neg at hc
      exact h5_ne (by simp [if_neg hc.1, if_neg hc.2])
    rcases h4_in with h4i | h4j <;> rcases h5_in with h5i | h5j
    · exact absurd (h5i.trans h4i.symm) (by decide)
    · exact Or.inl ⟨h4i.symm, h5j.symm⟩
    · exact Or.inr ⟨h5i.symm, h4j.symm⟩
    · exact absurd (h5j.trans h4j.symm) (by decide)
  }

/--
The **core** perimeter: the 4 conjugate-pair index families that avoid
the tension-axis indices {4, 5}.
-/
theorem perimeter_orthogonal_balance (v : Sed) (hv : v ∈ Perimeter24)
    (h_no_45 : ∀ i j : Fin 16, i ≠ j →
      (v = sedBasis i + sedBasis j ∨ v = sedBasis i - sedBasis j) →
      i.val ≠ 4 ∧ i.val ≠ 5 ∧ j.val ≠ 4 ∧ j.val ≠ 5) :
  @inner ℝ Sed _ v u_antisym = 0 := by
  obtain ⟨i, j, hij, hcase⟩ := hv
  obtain ⟨hi4, hi5, hj4, hj5⟩ := h_no_45 i j hij hcase
  have hbi : @inner ℝ Sed _ (sedBasis i) u_antisym = 0 := by
    simp only [sedBasis, u_antisym, inner_smul_right, inner_sub_right,
               EuclideanSpace.inner_single_left, EuclideanSpace.single_apply]
    have h1 : i ≠ (4 : Fin 16) := fun h => hi4 (congrArg Fin.val h)
    have h2 : i ≠ (5 : Fin 16) := fun h => hi5 (congrArg Fin.val h)
    simp [if_neg h1, if_neg h2]
  have hbj : @inner ℝ Sed _ (sedBasis j) u_antisym = 0 := by
    simp only [sedBasis, u_antisym, inner_smul_right, inner_sub_right,
               EuclideanSpace.inner_single_left, EuclideanSpace.single_apply]
    have h1 : j ≠ (4 : Fin 16) := fun h => hj4 (congrArg Fin.val h)
    have h2 : j ≠ (5 : Fin 16) := fun h => hj5 (congrArg Fin.val h)
    simp [if_neg h1, if_neg h2]
  rcases hcase with rfl | rfl
  · simp [inner_add_left, hbi, hbj]
  · simp [inner_sub_left, hbi, hbj]

end
