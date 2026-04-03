import RHForcingArgument

/-! Helper lemmas for MirrorSymmetry: coordinate computations of
    `sed_comm u_antisym (F_base t)` at indices 0, 4, 5. -/

noncomputable section

set_option maxHeartbeats 800000 in
/-- The commutator `[u_antisym, F_base t]` has zero `e₀` component. -/
lemma sed_comm_u_F_base_coord0 (t : ℝ) :
    (sed_comm u_antisym (F_base t)) (0 : Fin 16) = 0 := by
  -- By definition of sed_comm, we know that its 0th component is given by the difference of the products of the 0th components of u_antisym and F_base t. Using the multiplication table, we can see that these products are both zero.
  simp [sed_comm, instMulSed, sedMulTarget, sedMulSign];
  -- By definition of multiplication in Sed, we can expand both products.
  have h_expand : ∀ x y : Sed, (x * y).ofLp 0 = ∑ i : Fin 16, ∑ j : Fin 16, (if sedMulTarget i j = 0 then sedMulSign i j * x i * y j else 0) := by
    exact?;
  rw [ h_expand, h_expand ];
  simp +decide [ u_antisym, F_base, sedMulTarget, sedMulSign ];
  simp +decide [ Fin.sum_univ_succ, Fin.sum_univ_zero, sedBasis ]

set_option maxHeartbeats 800000 in
/-- The commutator `[u_antisym, F_base t]` has zero `e₄` component. -/
lemma sed_comm_u_F_base_coord4 (t : ℝ) :
    (sed_comm u_antisym (F_base t)) (4 : Fin 16) = 0 := by
  unfold sed_comm u_antisym F_base; simp +decide [ instMulSed, sedMulTarget, sedMulSign ];
  erw [ show ( ( Real.sqrt 2 ) ⁻¹ • ( sedBasis 4 - sedBasis 5 ) * ( Real.cos ( t * Real.log 2 ) • sedBasis 0 + Real.sin ( t * Real.log 2 ) • sedBasis 3 + Real.sin ( t * Real.log 3 ) • sedBasis 6 ) ) = ( EuclideanSpace.equiv ( Fin 16 ) ℝ ).symm ( fun k => ∑ i : Fin 16, ∑ j : Fin 16, if sedMulTarget i j = k then sedMulSign i j * ( ( Real.sqrt 2 ) ⁻¹ • ( sedBasis 4 - sedBasis 5 ) ) i * ( Real.cos ( t * Real.log 2 ) • sedBasis 0 + Real.sin ( t * Real.log 2 ) • sedBasis 3 + Real.sin ( t * Real.log 3 ) • sedBasis 6 ) j else 0 ) from rfl ];
  erw [ show ( ( Real.cos ( t * Real.log 2 ) • sedBasis 0 + Real.sin ( t * Real.log 2 ) • sedBasis 3 + Real.sin ( t * Real.log 3 ) • sedBasis 6 ) * ( Real.sqrt 2 ) ⁻¹ • ( sedBasis 4 - sedBasis 5 ) ) = ( EuclideanSpace.equiv ( Fin 16 ) ℝ ).symm ( fun k => ∑ i : Fin 16, ∑ j : Fin 16, if sedMulTarget i j = k then sedMulSign i j * ( Real.cos ( t * Real.log 2 ) • sedBasis 0 + Real.sin ( t * Real.log 2 ) • sedBasis 3 + Real.sin ( t * Real.log 3 ) • sedBasis 6 ) i * ( ( Real.sqrt 2 ) ⁻¹ • ( sedBasis 4 - sedBasis 5 ) ) j else 0 ) from rfl ];
  simp +decide [ Fin.sum_univ_succ, Fin.sum_univ_zero, sedMulTarget, sedMulSign, sedBasis ] ; ring!;

set_option maxHeartbeats 800000 in
/-- The commutator `[u_antisym, F_base t]` has zero `e₅` component. -/
lemma sed_comm_u_F_base_coord5 (t : ℝ) :
    (sed_comm u_antisym (F_base t)) (5 : Fin 16) = 0 := by
  unfold sed_comm u_antisym F_base; norm_num [ Fin.sum_univ_succ, Finset.sum_range_succ, Finset.sum_range_zero, Pi.smul_apply, Pi.add_apply ] ; ring;
  -- By definition of multiplication in the sedenion algebra, we can expand the product.
  have h_mul : ∀ (x y : Sed), (x * y) = (EuclideanSpace.equiv (Fin 16) ℝ).symm (fun k => ∑ i : Fin 16, ∑ j : Fin 16, if sedMulTarget i j = k then sedMulSign i j * x i * y j else 0) := by
    bound;
  rw [ h_mul, h_mul ];
  simp +decide [ Fin.sum_univ_succ, Fin.sum_univ_zero, Finset.sum_range_succ, Finset.sum_range_zero, Pi.smul_apply, Pi.add_apply, Pi.sub_apply, sedBasis ] ; ring!

end