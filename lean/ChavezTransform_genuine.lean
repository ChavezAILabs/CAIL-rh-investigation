/-
ChavezTransform_genuine.lean
Chavez AI Labs LLC — Applied Pathological Mathematics
April 2026

Formal verification of a scalar-channel restriction of the Chavez Transform,
using genuine sedenion multiplication (see Scope note below -- this file does
NOT verify the transform's zero-divisor structure, which is its actual
subject; see CORRECTIONS.md C-018).
Supersedes ChavezTransform_Specification_aristotle.lean (UUID 0bfec79d), where
CD4_mul was defined as the zero function, making all theorems vacuous.

Authors:
  Paul Chavez — Chavez AI Labs LLC (@aztecsungod)
    Mathematical design, proof architecture, session direction

AI Contributors:
  Claude Code (Anthropic) — four-step proof architecture, file construction,
    error diagnosis and repair across multiple build iterations
  Gemini CLI (Google) — build completion via multi-AI relay handoff
  Aristotle / Harmonic Math — final stack verification, axiom footprint
    confirmation: [propext, Classical.choice, Quot.sound]

Multi-AI Workflow:
  Claude Desktop (Anthropic) — strategy, session prompts, KSJ curation
  Claude Code — Lean scaffolding and iterative build
  Gemini CLI — relay completion at Claude Code context limit
  Aristotle — final independent verification (Harmonic Math platform)

Design:
  - Sed := EuclideanSpace ℝ (Fin 16) with instMulSed (genuine 16×16 table)
  - realToSed x = x • sedBasis 0  (embeds ℝ ↪ Sed via the scalar channel e₀)
  - e₀ identity: P * sedBasis 0 = P and sedBasis 0 * P = P  (table rows/cols 0)
  - K_Z P Q (realToSed x) = 2 * x² * (‖P‖² + ‖Q‖²)  (exact, no sorries)
  - stability_constant P Q α = 2 * (‖P‖² + ‖Q‖²) / (α * Real.exp 1)
  - Domain: parametric (a, b]  (matches IntervalIntegrable)

Key Results:
  - chavez_transform_integrable (2026-09-09, replaces the vacuous
    chavez_transform_convergence -- see CORRECTIONS.md C-017): the
    transform's integrand f(x)*K(P,Q,realToSed x,α,d) is genuinely
    IntegrableOn (a,b] whenever f is interval-integrable and α,d > 0.
    This is where "the integral converges" actually has content, unlike
    the old theorem's `∃ C, |C[f]| ≤ C`, which holds for any real number
    regardless of hypotheses. h_bounded was dropped from the old
    signature -- confirmed unnecessary by the standing hypothesis-use
    check (integrability of f, not boundedness, is what the proof needs;
    K's boundedness alone supplies the rest). The other three hypotheses
    were independently confirmed load-bearing by the same check.
  - chavez_transform_stability: |C[f]| ≤ stability_constant P Q α * L1_norm f a b
  - K_Z_realToSed: exact closed form of K_Z on the embedded line (not a
    "pattern invariance" result -- see Scope note)

Scope (corrected 2026-09-09 -- see CORRECTIONS.md C-018):
  Both theorems above are about chavez_transform_1d, whose integration
  variable enters ONLY through realToSed x = x . sedBasis 0 -- the e0 scalar
  channel. Because e0 is the multiplicative identity, P * (x.e0) = x.P for
  EVERY P, so sedenion multiplication reduces exactly to scalar
  multiplication on this subspace (K_Z_realToSed makes this literal:
  K_Z P Q (realToSed x) = 2x^2(||P||^2+||Q||^2), no P,Q product survives).
  The zero-divisor structure -- the actual subject of the Chavez Transform,
  and the reason to use a non-associative Cayley-Dickson algebra at all --
  is invisible on this line and is NOT exercised by anything proved here.
  "Both theorems unconditional on P*Q=0" is true but is a symptom of this,
  not a strength: the zero-divisor condition never mattered because the
  product never appeared. K_Z_realToSed's formula is pattern-independent
  because the multiplication degenerated, not because distinct Canonical
  Six patterns were shown equivalent -- "pattern invariance formally proved
  as theorem" (the previous framing) does not follow from it.
  What IS proved: a correct, non-trivial, sharp-constant bound on this
  scalar-channel restriction -- genuinely useful, but a different and much
  simpler object than "the Chavez Transform...formally verified" as
  described elsewhere in this repo. A genuine formalization of the full
  transform needs the integral over an actual multi-dimensional sedenion
  domain where P.x and x.Q differ, which needs a bound like
  sed_norm_mul_le (or equivalent) that does not yet exist in this stack.

Axiom footprint (both theorems):
  [propext, Classical.choice, Quot.sound]
  No riemann_critical_line. No sorryAx. No non-standard axioms.

GitHub: https://github.com/ChavezAILabs/CAIL-rh-investigation
Zenodo: https://doi.org/10.5281/zenodo.17402495
-/

import Mathlib
import RHForcingArgument

set_option maxHeartbeats 800000

open scoped Real MeasureTheory
open MeasureTheory

noncomputable section

-- ============================================================
-- §1  COMPONENT ACCESS: (P * Q) k = ∑ i j, ...
-- ============================================================

/-- The k-th component of a sedenion product equals the bilinear sum over the table.
    Proved by definitional equality (same as the exact? answer in sed_mul_smul_right). -/
private lemma mul_apply (P Q : Sed) (k : Fin 16) :
    (P * Q) k = ∑ i : Fin 16, ∑ j : Fin 16,
      if sedMulTarget i j = k then sedMulSign i j * P i * Q j else 0 :=
  Real.ext_cauchy rfl

-- ============================================================
-- §2  TABLE FACTS  (decidable on closed ∀-propositions)
-- ============================================================

-- Universal form avoids "free variable" error from decide.
private lemma sedMulTarget_col0 : ∀ i : Fin 16, sedMulTarget i (0 : Fin 16) = i := by decide
private lemma sedMulSign_col0   : ∀ i : Fin 16, sedMulSign i (0 : Fin 16) = 1 := by intro i; fin_cases i <;> rfl
private lemma sedMulTarget_row0 : ∀ j : Fin 16, sedMulTarget (0 : Fin 16) j = j := by decide
private lemma sedMulSign_row0   : ∀ j : Fin 16, sedMulSign (0 : Fin 16) j = 1 := by intro j; fin_cases j <;> rfl

-- ============================================================
-- §3  e₀ IS A TWO-SIDED IDENTITY
-- ============================================================

/-- Right identity: P * e₀ = P. -/
lemma sed_mul_sedBasis0 (P : Sed) : P * sedBasis 0 = P := by
  ext k
  rw [mul_apply]
  simp only [sedBasis, EuclideanSpace.single_apply, mul_ite, mul_one, mul_zero]
  -- Goal: ∑ i, ∑ j, if sedMulTarget i j = k
  --         then (if j = 0 then sedMulSign i j * P i else 0) else 0 = P k
  -- Collapse j-sum: only j = 0 contributes (inner if is 0 for j ≠ 0)
  have hj_sum : ∀ i : Fin 16, ∑ j : Fin 16,
      (if sedMulTarget i j = k then (if j = (0 : Fin 16) then sedMulSign i j * P i else 0)
        else 0) =
      if sedMulTarget i 0 = k then sedMulSign i 0 * P i else 0 := fun i => by
    apply Finset.sum_eq_single (0 : Fin 16)
    · intro j _ hj
      simp [hj]
    · simp
  simp_rw [hj_sum, sedMulTarget_col0, sedMulSign_col0, one_mul]
  simp [Finset.sum_ite_eq', Finset.mem_univ]

/-- Left identity: e₀ * Q = Q. -/
lemma sedBasis0_mul_sed (Q : Sed) : sedBasis 0 * Q = Q := by
  ext k
  rw [mul_apply]
  simp only [sedBasis, EuclideanSpace.single_apply, ite_mul, one_mul, zero_mul, mul_ite,
             mul_zero, mul_one]
  -- Goal: ∑ i, ∑ j, if sedMulTarget i j = k
  --         then (if i = 0 then sedMulSign i j * Q j else 0) else 0 = Q k
  -- Collapse i-sum via sum_comm then sum_eq_single
  rw [Finset.sum_comm]
  have hi_sum : ∀ j : Fin 16, ∑ i : Fin 16,
      (if sedMulTarget i j = k then (if i = (0 : Fin 16) then sedMulSign i j * Q j else 0)
        else 0) =
      if sedMulTarget 0 j = k then sedMulSign 0 j * Q j else 0 := fun j => by
    apply Finset.sum_eq_single (0 : Fin 16)
    · intro i _ hi
      simp [hi]
    · simp
  simp_rw [hi_sum, sedMulTarget_row0, sedMulSign_row0, one_mul]
  simp [Finset.sum_ite_eq', Finset.mem_univ]

-- ============================================================
-- §4  realToSed AND ITS ALGEBRAIC PROPERTIES
-- ============================================================

/-- Embed ℝ into Sed via the scalar channel: x ↦ x · e₀. -/
def realToSed (x : ℝ) : Sed := x • sedBasis 0

lemma sed_mul_realToSed (P : Sed) (x : ℝ) : P * realToSed x = x • P := by
  unfold realToSed
  rw [sed_mul_smul_right, sed_mul_sedBasis0]

lemma realToSed_mul_sed (x : ℝ) (Q : Sed) : realToSed x * Q = x • Q := by
  unfold realToSed
  rw [sed_mul_smul_left, sedBasis0_mul_sed]

lemma norm_sedBasis0 : ‖sedBasis 0‖ = 1 := by
  simp [sedBasis, EuclideanSpace.norm_single]

lemma norm_realToSed (x : ℝ) : ‖realToSed x‖ = |x| := by
  simp [realToSed, norm_smul, norm_sedBasis0]

-- ============================================================
-- §5  KERNEL DEFINITIONS
-- ============================================================

/-- The bilateral sedenion kernel: K_Z(P,Q,x) = ‖Px‖² + ‖xQ‖² + ‖Qx‖² + ‖xP‖². -/
def K_Z (P Q x : Sed) : ℝ :=
  ‖P * x‖^2 + ‖x * Q‖^2 + ‖Q * x‖^2 + ‖x * P‖^2

/-- Full kernel with Gaussian and power-law weights. -/
def K (P Q x : Sed) (α d : ℝ) : ℝ :=
  K_Z P Q x * Real.exp (-α * ‖x‖^2) * (1 + ‖x‖^2) ^ (-d / 2)

-- ============================================================
-- §6  EXACT K_Z FORMULA FOR 1D EMBEDDING
-- ============================================================

/-- When x is embedded via realToSed, K_Z simplifies exactly to 2x²(‖P‖²+‖Q‖²). -/
lemma K_Z_realToSed (P Q : Sed) (x : ℝ) :
    K_Z P Q (realToSed x) = 2 * x^2 * (‖P‖^2 + ‖Q‖^2) := by
  unfold K_Z
  rw [sed_mul_realToSed, realToSed_mul_sed, sed_mul_realToSed, realToSed_mul_sed]
  simp only [norm_smul, Real.norm_eq_abs]
  nlinarith [sq_abs x, sq_nonneg ‖P‖, sq_nonneg ‖Q‖, norm_nonneg P, norm_nonneg Q]

/-- ‖realToSed x‖² = x² -/
lemma norm_realToSed_sq (x : ℝ) : ‖realToSed x‖^2 = x^2 := by
  rw [norm_realToSed, sq_abs]

-- ============================================================
-- §7  HELPER BOUNDS
-- ============================================================

/-- Gaussian decay: exp(-α‖v‖²) ≤ 1 for α > 0. -/
lemma exp_decay_le_one (v : Sed) (α : ℝ) (hα : 0 < α) :
    Real.exp (-α * ‖v‖^2) ≤ 1 :=
  Real.exp_le_one_iff.mpr (mul_nonpos_of_nonpos_of_nonneg
    (neg_nonpos.mpr hα.le) (sq_nonneg _))

/-- Power-law decay: (1 + ‖v‖²)^(-d/2) ≤ 1 for d > 0. -/
lemma rpow_decay_le_one (v : Sed) (d : ℝ) (hd : 0 < d) :
    (1 + ‖v‖^2) ^ (-d / 2) ≤ 1 :=
  le_trans
    (Real.rpow_le_rpow_of_exponent_le (by nlinarith [sq_nonneg ‖v‖])
      (div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr hd.le) zero_le_two))
    (by norm_num)

/-- Core scalar bound: t · exp(-t) ≤ 1 / exp(1) for all t ∈ ℝ. -/
lemma mul_exp_neg_le (t : ℝ) : t * Real.exp (-t) ≤ 1 / Real.exp 1 := by
  have hstep : t ≤ Real.exp (t - 1) := by
    have := Real.add_one_le_exp (t - 1)
    linarith
  calc t * Real.exp (-t)
      ≤ Real.exp (t - 1) * Real.exp (-t) :=
          mul_le_mul_of_nonneg_right hstep (Real.exp_nonneg _)
    _ = Real.exp (-1) := by
          rw [← Real.exp_add]
          ring_nf
    _ = 1 / Real.exp 1 := by
          rw [Real.exp_neg]; ring

/-- Optimal Gaussian bound: x² · exp(-αx²) ≤ 1 / (α · exp 1) for α > 0. -/
lemma sq_mul_exp_neg (x α : ℝ) (hα : 0 < α) :
    x^2 * Real.exp (-α * x^2) ≤ 1 / (α * Real.exp 1) := by
  have hαe : 0 < α * Real.exp 1 := mul_pos hα (Real.exp_pos 1)
  rw [le_div_iff₀ hαe]
  have key : α * x^2 * Real.exp (-(α * x^2)) ≤ 1 / Real.exp 1 :=
    mul_exp_neg_le (α * x^2)
  calc x^2 * Real.exp (-α * x^2) * (α * Real.exp 1)
      = (α * x^2 * Real.exp (-(α * x^2))) * Real.exp 1 := by ring_nf
    _ ≤ (1 / Real.exp 1) * Real.exp 1 :=
          mul_le_mul_of_nonneg_right key (Real.exp_pos 1).le
    _ = 1 := by field_simp [Real.exp_ne_zero]

-- ============================================================
-- §8  THE TRANSFORM, NORM, AND STABILITY CONSTANT
-- ============================================================

/-- L¹ norm of f on (a, b]. -/
def L1_norm (f : ℝ → ℝ) (a b : ℝ) : ℝ :=
  ∫ x in Set.Ioc a b, |f x|

/-- Stability constant: 2(‖P‖² + ‖Q‖²) / (α · e). -/
def stability_constant (P Q : Sed) (α : ℝ) : ℝ :=
  2 * (‖P‖^2 + ‖Q‖^2) / (α * Real.exp 1)

/-- The Chavez Transform on (a, b]: C[f](P,Q,α,d) = ∫ₐᵇ f(x) K(P,Q,x̃,α,d) dx. -/
def chavez_transform_1d (f : ℝ → ℝ) (P Q : Sed) (α d a b : ℝ) : ℝ :=
  ∫ x in Set.Ioc a b, f x * K P Q (realToSed x) α d

-- ============================================================
-- §9  KERNEL IS NONNEG AND BOUNDED
-- ============================================================

lemma K_Z_nonneg (P Q x : Sed) : 0 ≤ K_Z P Q x := by
  unfold K_Z; positivity

lemma K_nonneg (P Q x : Sed) (α d : ℝ) : 0 ≤ K P Q x α d := by
  unfold K K_Z
  apply mul_nonneg
  · apply mul_nonneg
    · positivity
    · exact Real.exp_nonneg _
  · exact Real.rpow_nonneg (by positivity) _

/-- Pointwise kernel bound: K P Q (realToSed x) α d ≤ stability_constant P Q α. -/
lemma K_bound (P Q : Sed) (α d x : ℝ) (hα : 0 < α) (hd : 0 < d) :
    K P Q (realToSed x) α d ≤ stability_constant P Q α := by
  unfold K stability_constant
  have hKZ : K_Z P Q (realToSed x) = 2 * x^2 * (‖P‖^2 + ‖Q‖^2) :=
    K_Z_realToSed P Q x
  have hnorm_sq : ‖realToSed x‖^2 = x^2 := norm_realToSed_sq x
  rw [hKZ, hnorm_sq]
  have hrpow : (1 + x^2) ^ (-d / 2) ≤ 1 :=
    calc (1 + x^2) ^ (-d / 2)
        ≤ (1 + x^2) ^ (0 : ℝ) :=
              Real.rpow_le_rpow_of_exponent_le (by nlinarith [sq_nonneg x])
                (div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr hd.le) zero_le_two)
      _ = 1 := Real.rpow_zero _
  have hexp_bound : x^2 * Real.exp (-α * x^2) ≤ 1 / (α * Real.exp 1) :=
    sq_mul_exp_neg x α hα
  calc 2 * x^2 * (‖P‖^2 + ‖Q‖^2) * Real.exp (-α * x^2) * (1 + x^2) ^ (-d / 2)
      ≤ 2 * x^2 * (‖P‖^2 + ‖Q‖^2) * Real.exp (-α * x^2) * 1 := by
            apply mul_le_mul_of_nonneg_left hrpow; positivity
    _ = 2 * (‖P‖^2 + ‖Q‖^2) * (x^2 * Real.exp (-α * x^2)) := by ring
    _ ≤ 2 * (‖P‖^2 + ‖Q‖^2) * (1 / (α * Real.exp 1)) := by
            apply mul_le_mul_of_nonneg_left hexp_bound; positivity
    _ = 2 * (‖P‖^2 + ‖Q‖^2) / (α * Real.exp 1) := by ring

-- ============================================================
-- §10  MAIN THEOREMS
-- ============================================================

/-- `K P Q (realToSed x) α d`, as a function of `x : ℝ`, is continuous.
    Substitutes the exact 1D formulas (`K_Z_realToSed`, `norm_realToSed_sq`) to
    reduce to elementary real-analysis continuity: a polynomial times `exp`
    times an `rpow` with strictly positive base `1 + x^2`, so the rpow's
    continuity holds regardless of the sign of its exponent `-d/2`. -/
lemma K_realToSed_continuous (P Q : Sed) (α d : ℝ) :
    Continuous (fun x : ℝ => K P Q (realToSed x) α d) := by
  have heq : (fun x : ℝ => K P Q (realToSed x) α d)
      = fun x => 2 * x ^ 2 * (‖P‖ ^ 2 + ‖Q‖ ^ 2) * Real.exp (-α * x ^ 2)
          * (1 + x ^ 2) ^ (-d / 2) := by
    funext x
    unfold K
    rw [K_Z_realToSed, norm_realToSed_sq]
  rw [heq]
  have hrpow : Continuous (fun x : ℝ => (1 + x ^ 2) ^ (-d / 2)) := by
    apply Continuous.rpow_const (by fun_prop)
    intro x; left; positivity
  fun_prop

/-- **Theorem 1: Convergence (integrability), corrected 2026-09-09.**
    The Chavez Transform's integrand is genuinely integrable on `(a, b]`
    whenever `f` is interval-integrable and `α, d > 0` -- this is what "the
    transform converges" should mean, and it is where the hypotheses
    actually do work. Replaces `chavez_transform_convergence`, whose
    conclusion `∃ C, |C[f]| ≤ C` was true unconditionally (see
    CORRECTIONS.md C-017) and used none of its four hypotheses.

    Proof: `f * K(...)` is dominated a.e. by the integrable majorant
    `stability_constant P Q α * |f|` (integrable via `h_integrable.norm`,
    the same expression `chavez_transform_stability` uses for its own
    dominating function) and is itself a.e.-strongly-measurable (`f` from
    `h_integrable`, `K(...)` from `K_realToSed_continuous`), so
    `Integrable.mono'` applies. -/
theorem chavez_transform_integrable
    (f : ℝ → ℝ) (P Q : Sed) (α d a b : ℝ)
    (h_integrable : IntervalIntegrable f MeasureTheory.volume a b)
    (h_alpha      : 0 < α)
    (h_d          : 0 < d) :
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

/-- **Theorem 2: Stability.**
    |C[f]| ≤ stability_constant(P,Q,α) · ‖f‖₁. -/
theorem chavez_transform_stability
    (f : ℝ → ℝ) (P Q : Sed) (α d a b : ℝ)
    (h_integrable : IntervalIntegrable f MeasureTheory.volume a b)
    (h_alpha      : 0 < α)
    (h_d          : 0 < d) :
    |chavez_transform_1d f P Q α d a b| ≤
      stability_constant P Q α * L1_norm f a b := by
  unfold chavez_transform_1d L1_norm
  -- Convert |·| to ‖·‖ so norm_integral_le_integral_norm applies
  rw [← Real.norm_eq_abs]
  -- Step 1: ‖∫ f·K‖ ≤ ∫ ‖f·K‖
  refine le_trans (MeasureTheory.norm_integral_le_integral_norm _) ?_
  simp only [Real.norm_eq_abs, abs_mul]
  -- Step 2: ∫ |f|·|K| ≤ stability_constant · ∫ |f|
  rw [← integral_const_mul]
  apply integral_mono_of_nonneg
  · -- Integrand nonneg
    exact Filter.Eventually.of_forall (fun x => by positivity)
  · -- RHS integrable: stability_constant * |f| on (a, b]
    exact (h_integrable.norm.1).const_mul _
  · -- Pointwise: |f x| · |K(...)| ≤ stability_constant · |f x|
    filter_upwards [ae_restrict_mem measurableSet_Ioc] with x _
    have hK_nn : 0 ≤ K P Q (realToSed x) α d := K_nonneg P Q (realToSed x) α d
    rw [abs_of_nonneg hK_nn]
    have hKbound := K_bound P Q α d x h_alpha h_d
    have hsc_nn : 0 ≤ stability_constant P Q α := by
      unfold stability_constant; positivity
    nlinarith [abs_nonneg (f x)]

end  -- noncomputable section
