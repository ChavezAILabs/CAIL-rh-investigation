/- C-020 hypothesis-use audit (Phase 78 verification batch, Task 3).
   Scratch copy of ba_asymptote_sq from GatewayLinearLaw.lean with the
   `hK : 0 ≤ K` hypothesis DELETED from the signature (proof body left
   otherwise identical, `hK` references removed). If this still elaborates,
   the hypothesis is decorative.
   Result: FAILS -- error: failed to prove positivity/nonnegativity/nonzeroness
   at the `t^2+K ≠ 0` step. hK is load-bearing, not decorative. -/
import Mathlib.Analysis.InnerProductSpace.EuclideanDist

noncomputable section

theorem ba_asymptote_sq_no_hK (K : ℝ) :
    Filter.Tendsto (fun t : ℝ => (17 * t ^ 2 + K) / (t ^ 2 + K))
      Filter.atTop (nhds 17) := by
  have h_inf : Filter.Tendsto (fun t : ℝ => t ^ 2 + K) Filter.atTop Filter.atTop := by
    rw [Filter.tendsto_atTop]
    intro b
    rw [Filter.eventually_atTop]
    refine ⟨max 1 (Real.sqrt (b - K)), fun t ht => ?_⟩
    have h1 : 1 ≤ t := le_trans (le_max_left _ _) ht
    have h2 : Real.sqrt (b - K) ≤ t := le_trans (le_max_right _ _) ht
    by_cases hbK : b ≤ K
    · linarith [sq_nonneg t]
    · have hpos : 0 < b - K := by linarith [not_le.mp hbK]
      have hsq : Real.sqrt (b - K) ^ 2 = b - K := Real.sq_sqrt (le_of_lt hpos)
      nlinarith [Real.sqrt_nonneg (b - K), sq_nonneg (t - Real.sqrt (b - K)),
                 mul_nonneg (Real.sqrt_nonneg (b - K)) (by linarith : (0:ℝ) ≤ t - Real.sqrt (b - K)),
                 h2, hsq]
  have h_inv : Filter.Tendsto (fun t : ℝ => (t ^ 2 + K)⁻¹) Filter.atTop (nhds 0) :=
    tendsto_inv_atTop_zero.comp h_inf
  have h_corr : Filter.Tendsto (fun t : ℝ => 16 * K * (t ^ 2 + K)⁻¹)
      Filter.atTop (nhds 0) := by
    have hc : Filter.Tendsto (fun _ : ℝ => (16 * K : ℝ)) Filter.atTop (nhds (16 * K)) :=
      tendsto_const_nhds
    have h := hc.mul h_inv
    simp only [mul_zero] at h
    exact h
  have h_main : Filter.Tendsto (fun t : ℝ => 17 - 16 * K * (t ^ 2 + K)⁻¹)
      Filter.atTop (nhds 17) := by
    have h17 : Filter.Tendsto (fun _ : ℝ => (17 : ℝ)) Filter.atTop (nhds 17) :=
      tendsto_const_nhds
    have h := h17.sub h_corr
    simp only [sub_zero] at h
    exact h
  apply h_main.congr'
  filter_upwards [Filter.eventually_gt_atTop 0] with t ht
  have hd : t ^ 2 + K ≠ 0 := by positivity
  field_simp [hd]; ring

end
