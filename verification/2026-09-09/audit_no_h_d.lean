/- C-017 fix, hypothesis-use audit (standing check item 1).
   Scratch copy of chavez_transform_integrable with h_d DELETED from the
   signature. Result: FAILS -- unknown identifier `h_d` at the K_bound call
   site. h_d is load-bearing. -/
import ChavezTransform_genuine

open scoped Real MeasureTheory
open MeasureTheory
noncomputable section

lemma K_realToSed_continuous (P Q : Sed) (α d : ℝ) :
    Continuous (fun x : ℝ => K P Q (realToSed x) α d) := by
  have heq : (fun x : ℝ => K P Q (realToSed x) α d)
      = fun x => 2 * x^2 * (‖P‖^2 + ‖Q‖^2) * Real.exp (-α * x^2) * (1 + x^2) ^ (-d / 2) := by
    funext x; unfold K; rw [K_Z_realToSed, norm_realToSed_sq]
  rw [heq]
  have hrpow : Continuous (fun x : ℝ => (1 + x^2) ^ (-d / 2)) := by
    apply Continuous.rpow_const (by fun_prop)
    intro x; left; positivity
  fun_prop

-- h_d DELETED
theorem chavez_transform_integrable_no_hd
    (f : ℝ → ℝ) (P Q : Sed) (α d a b : ℝ)
    (h_integrable : IntervalIntegrable f MeasureTheory.volume a b)
    (h_alpha      : 0 < α) :
    IntegrableOn (fun x => f x * K P Q (realToSed x) α d) (Set.Ioc a b) volume := by
  unfold IntegrableOn
  apply Integrable.mono' (g := fun x => stability_constant P Q α * |f x|)
  · exact (h_integrable.norm.1).const_mul _
  · exact h_integrable.1.aestronglyMeasurable.mul
      (K_realToSed_continuous P Q α d).aestronglyMeasurable
  · filter_upwards [ae_restrict_mem measurableSet_Ioc] with x _
    rw [Real.norm_eq_abs, abs_mul]
    have hK_nn := K_nonneg P Q (realToSed x) α d
    rw [abs_of_nonneg hK_nn]
    have hKbound := K_bound P Q α d x h_alpha h_d
    nlinarith [abs_nonneg (f x)]

end
