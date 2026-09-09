/- C-020 hypothesis-use audit (Phase 78 verification batch, Task 3).
   Scratch copy of Fbase_nondegeneracy from SpectralIdentification.lean with the
   `hs : 0 < s.re ∧ s.re < 1` hypothesis DELETED from the signature. If this still
   elaborates, the hypothesis is decorative in the canonical lemma.
   Result: compiles clean, exit 0. hs is confirmed decorative. -/
import SedenionicHamiltonian

noncomputable section

lemma Fbase_nondegeneracy_no_hs (s : ℂ)
    (h : ∀ t : ℝ, t ≠ 0 → sed_comm (sedenion_Hamiltonian s) (F_base t) = 0) :
    sedenion_Hamiltonian s = 0 := by
  have hcomm : ∀ t : ℝ, t ≠ 0 →
      (s.re - 1 / 2) • sed_comm u_antisym (F_base t) = 0 := by
    intro t ht
    have ht_comm := h t ht
    rw [sedenion_Hamiltonian, sed_comm_smul_left] at ht_comm
    exact ht_comm
  have hwitness : sed_comm u_antisym (F_base 1) ≠ 0 :=
    sed_comm_u_Fbase_nonzero 1 one_ne_zero
  have hscalar : s.re - 1 / 2 = 0 := by
    have h1 := hcomm 1 one_ne_zero
    rcases smul_eq_zero.mp h1 with hc | hv
    · exact hc
    · exact absurd hv hwitness
  rw [sedenion_Hamiltonian, hscalar, zero_smul]

end
