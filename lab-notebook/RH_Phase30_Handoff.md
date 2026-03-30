# RH Investigation Phase 30 — Official Handoff
## Chavez AI Labs LLC · March 26, 2026
## "Applied Pathological Mathematics — Better math, less suffering"

**Project:** RH_MP_2026_001
**Working directory:** `C:\dev\projects\Experiments_January_2026\Primes_2026`
**Phase 29 status:** Complete and committed to GitHub.
**Phase 30 status:** Ready to run.

---

## CONTEXT: WHERE PHASE 29 LEFT US

Phase 29 established three conjectures with high confidence:

| Conjecture | Result | Confidence |
|---|---|---|
| 29.1 Weil Negativity | Tr_BK(tₙ) < 0 at 76.6% of 500 zeros | p = 2.56×10⁻³⁴ |
| 29.2 Constant Uncertainty | ℏ_sed = 11.19 ± 1.71 (slope ≈ 0) | R² ≈ 0, p = 0.975 |
| 29.3 Bilateral Prime Isometry | ‖F×r_p‖/‖F‖ = 1.000 ± 0.000 for p ∈ {5,7,11} | Algebraic identity |

The Weil ratio mean_Tr_BK / Weil_RHS ≈ 0.245–0.250 is stable across prime sets of size 6–11.

**Machine-exact constants (Phase 24):**

| Constant | Value | Meaning |
|---|---|---|
| c₁ | 0.11797805192095003 | sin(Weil angle) — structural residual ratio |
| c₃ | 0.9930162029216528 | cos(Weil angle) — projection fraction |
| Weil angle | 6.784° | Angle between S(N) and Weil RHS direction |
| ℏ_sed | 11.19 ± 1.71 | Sedenion Planck constant |
| Weil ratio | 0.245 ± 0.005 | mean Tr_BK / Weil_RHS |

Note: c₁² + c₃² = 1.000 (sin/cos of same angle). 12% Weil angle is STRUCTURAL (Phase 24T1).

---

## PHASE 30 OBJECTIVES

**Primary question:** Is there an analytic handle on c₁ = 0.11797805192095003?

Two threads:
1. **Thread 1:** Does c₁ arise from the GUE two-point pair correlation overlap integral of f₅D?
2. **Thread 2:** Does the Weil ratio converge to an analytic constant (1/4?) as the prime set grows?

Phase 30 is explicitly speculative. A null result on both threads is a valid and informative outcome.

---

## STEP 1: RUN THE PYTHON SCRIPT (Claude Code)

**Script:** `rh_phase30.py`
**Output:** `phase30_results.json`
**Dependencies:** numpy, scipy, json (no mpmath needed if `rh_zeros.json` cache exists)
**Runtime estimate:** 5–15 minutes (dominated by the T=500 grid computation)

```bash
cd C:\dev\projects\Experiments_January_2026\Primes_2026
python rh_phase30.py
```

The script produces `phase30_results.json` and prints a full console summary.

### Thread 1: GUE Overlap Integral

Tests whether the structural Weil angle c₁ can be derived from the Montgomery-Dyson
GUE two-point pair correlation function:

```
R₂(r) = 1 − (sin(πr) / πr)²
```

**Formula tested:**
```
c₁_hat = ∫∫ f₅D(t)·f₅D(t')·R₂_norm(t,t') dt dt'
          ─────────────────────────────────────────
          ∫∫ f₅D(t)·f₅D(t') dt dt'
```

where f₅D(t) = Σ_p (log p / √p)·cos(t·log p) and R₂ is evaluated with local zero
density normalization: r_norm = |t − t'| × density(mean(t,t')).

**Sub-methods:**
- **1A (Grid):** Continuous double integral on [0,T]×[0,T] for T ∈ {50, 100, 200, 500}
- **1B (Zeros):** Discrete sum using actual Riemann zeros as integration nodes
- **1C (Alternatives):** R₂ evaluated at c₁, r that solves R₂(r)=c₁, diagonal suppression

**Mathematical note recorded in script:** R₂(k) = 1 exactly for all non-zero integers k
(since sin(kπ) = 0). Thus the GUE suppression in the zero-based version is purely a
diagonal (i=j) effect. As N → ∞, c₁_hat → 1 − diagonal_fraction → 1. The script
reports whether this is what we observe.

### Thread 2: Weil Ratio Convergence

Tests whether mean_Tr_BK(zeros) / Weil_RHS converges to an analytic constant
as the prime set grows from p ≤ 13 through p ≤ 151 (9 prime sets, 6–36 primes).

```python
# Weil ratio for prime set P:
ratio(P) = mean_{n=1..100} Tr_BK(tₙ, P) / Weil_RHS(P)
         = mean_{n=1..100} Σ_{p∈P} (log p/√p)·cos(tₙ·log p)
           ───────────────────────────────────────────────────
           -Σ_{p∈P} log p / √p
```

Analytic candidates tested: 1/4, 1/e, 1/(2π), log 2/π, 1/π, γ (Euler), √2−1, (√5−1)/2.
Limit extrapolation via linear fits in 1/log(p_max) and 1/n_primes.

---

## STEP 2: CAILCULATOR ANALYSIS (Claude Desktop)

Load `phase30_results.json` and run the following in order.

### 2.1 Thread 1 — GUE Overlap Sequences

**Goal:** Does c₁_hat converge to c₁ = 0.11797805192095003?

**a) Zero-based c₁_hat sequence (N = 50, 100, 200, 500):**
```json
Input: [thread1_gue_overlap.zero_based_1B.N50.c1_hat,
        thread1_gue_overlap.zero_based_1B.N100.c1_hat,
        thread1_gue_overlap.zero_based_1B.N200.c1_hat,
        thread1_gue_overlap.zero_based_1B.N500.c1_hat]
```
→ `analyze_dataset` — Chavez transform, conjugation symmetry, persistence
→ `detect_patterns` — is this sequence structured or converging?

**b) Grid-based c₁_hat sequence (T = 50, 100, 200, 500):**
```json
Input: [thread1_gue_overlap.grid_based_1A.T50.c1_hat,
        thread1_gue_overlap.grid_based_1A.T100.c1_hat,
        thread1_gue_overlap.grid_based_1A.T200.c1_hat,
        thread1_gue_overlap.grid_based_1A.T500.c1_hat]
```
→ `analyze_dataset` + `detect_patterns`

**c) Alternative 1C values:**
```json
Input: [thread1_gue_overlap.alternative_1C.R2_at_c1,
        thread1_gue_overlap.alternative_1C.r_solving_R2_eq_c1,
        thread1_gue_overlap.alternative_1C.diagonal_fraction_N100,
        thread1_gue_overlap.alternative_1C.c1_pred_diagonal_suppression]
```
→ `analyze_dataset` — do any of these match c₁?

### 2.2 Thread 2 — Weil Ratio Sequence

**Goal:** Does the ratio converge to 1/4 or another analytic constant?

**a) Ratio sequence across prime sets (9 values):**
```json
Input: thread2_weil_ratio.ratio_sequence
       (p_max: 13, 23, 29, 37, 53, 71, 97, 127, 151)
```
→ `analyze_dataset` — Chavez transform, CV, conjugation symmetry
→ `chavez_transform` specifically — what does the dimensional reduction reveal?

**b) Weil_RHS sequence (9 values, all negative):**
```json
Input: thread2_weil_ratio.weil_rhs_sequence
```
→ `analyze_dataset` — how fast does |Weil_RHS| grow? Logarithmic?

**c) Per-prime-set Tr_BK distributions:**
For each of the 9 prime sets, run:
```json
Input: thread2_weil_ratio.prime_sets.[label].tr_zeros_100
```
→ `chavez_transform` — does the CV remain ≈ 0.146 as prime set grows?
→ `analyze_dataset` with conjugation_symmetry — does GUE separation persist?

### 2.3 Combined ZDTP Analysis

**d) ZDTP on the ratio sequence as a "dataset":**
```json
Input: thread2_weil_ratio.ratio_sequence  (9 values)
```
→ `zdtp_transmit` — 16D→32D→64D — is the ratio sequence algebraically special?

**e) ZDTP on the c₁_hat grid sequence (4 values):**
```json
Input: [c1_hat values at T50, T100, T200, T500]
```
→ `zdtp_transmit` — bilateral zero confidence?

---

## EXPECTED OUTCOMES

### Thread 1 (GUE Overlap)

**Pre-run smoke test reveals two distinct behaviors:**

- **Grid method (1A):** c₁_hat ≈ 34.7 at T=50 (not near 0.118). Cause: the denominator
  (∫f dt)² ≈ 0 because f₅D is a sum of cosines whose integral over [0,T] is bounded
  (O(1)) while the numerator grows as O(T²). The formula as written is numerically
  ill-conditioned for oscillating functions with near-zero integral mean. Results will
  show large c₁_hat values diverging with T — a clear null.

- **Zero-based method (1B):** c₁_hat ≈ 0.996 at N=100 (not near 0.118). Cause: R₂(k)=1
  exactly for all non-zero integers k (since sin(kπ)=0), so the only GUE suppression is
  on the diagonal (i=j, R₂=0). The diagonal contributes only ~2% of the total sum; the
  remaining 98% has R₂≈1. As N→∞, c₁_hat → 1 − (diagonal fraction) → 1. A clean null.

**Conclusion from Thread 1:** c₁ does NOT arise from the GUE two-point overlap
integral in this formulation. The formula is sensitive to the near-zero-mean property
of f₅D. A well-conditioned reformulation would use the L² norm ∫f²dt as the
denominator (capturing the power fraction), but that is a different formula.

**What this tells us:** c₁ = sin(Weil angle) is set by the Euler product amplitude
structure of f₅D relative to the Weil RHS direction — a geometric property of the
AIEX-001a embedding, not a pair-correlation constant.

### Thread 2 (Weil Ratio)

**Pre-run smoke test (100 zeros):**

| p_max | n_primes | ratio | diff from 1/4 |
|---|---|---|---|
| 13 | 6 | 0.2479 | −0.0021 |
| 23 | 9 | 0.2467 | −0.0033 |
| 53 | 16 | 0.2189 | −0.0311 |
| 97 | 25 | 0.1970 | −0.0530 |
| 127 | 31 | 0.1834 | −0.0666 |
| 151 | 36 | 0.1736 | −0.0764 |

**The ratio is decreasing and NOT converging to 1/4.** It is heading toward 0.

**Mathematical explanation (confirmed):** By partial summation from PNT,
Σ_{p≤P} log p/√p ~ 2√P (grows as √P), while the numerator Σ_{p≤P} (log p)²/p ~ (log P)²/2
grows only logarithmically. So ratio ~ (log P)² / (N × 4√P) → 0 as P → ∞.

**The stability observed in Phase 29 (0.240–0.250 across 6–11 primes) is a finite-size
plateau, not a universal constant.** The 0.248 value is specific to the 6-prime
AIEX-001a embedding, not a limit of a convergent series.

**What this tells us:** The Weil ratio 0.248 is a property of the 6-prime Euler product
truncation — it encodes how much of the Weil RHS is captured by the first 6 primes in
the AIEX-001a embedding. It is NOT a fundamental constant like 1/4 or 1/e.

**CAILculator focus for Thread 2:** The ratio sequence [0.248, 0.247, 0.219, 0.197,
0.183, 0.174, ...] may still have algebraic structure (e.g., Chavez symmetry, bilateral
zero patterns). The sequence is not random — it decays in a way controlled by PNT.

---

## OUTPUT FORMAT

`phase30_results.json` schema:

```json
{
  "metadata": {
    "phase": 30,
    "date": "2026-03-26",
    "target_c1": 0.11797805192095003,
    "weil_angle_degrees": 6.784
  },
  "thread1_gue_overlap": {
    "grid_based_1A":    {"T50": {...}, "T100": {...}, "T200": {...}, "T500": {...}},
    "zero_based_1B":    {"N50": {...}, "N100": {...}, "N200": {...}, "N500": {...}},
    "alternative_1C":   {...},
    "converging_to_c1": bool,
    "grid_c1_range":    [min, max],
    "zero_c1_range":    [min, max]
  },
  "thread2_weil_ratio": {
    "prime_sets":         {"p13": {...}, "p23": {...}, ..., "p151": {...}},
    "ratio_sequence":     [float × 9],
    "weil_rhs_sequence":  [float × 9],
    "analytic_fits":      {"vs_inv_log_pmax": {...}, "vs_inv_n_primes": {...}},
    "monotone_decreasing": bool
  }
}
```

---

## KEY FILES

| File | Purpose |
|---|---|
| `rh_phase29_bk_burst.py` | Phase 29 engine — sedenion functions copied verbatim |
| `phase29_results.json` | Phase 29 baseline (ratio 0.245, ℏ_sed, etc.) |
| `rh_zeros.json` | 1,000 zero cache (script uses first 500) |
| `rh_phase30.py` | **This phase's computation script** |
| `phase30_results.json` | **Output — feed to CAILculator** |

---

## SUCCESS CONDITION

Phase 30 succeeds if ANY of the following:

1. c₁_hat converges toward 0.118 from either method (Thread 1 positive result)
2. The Weil ratio converges to an identifiable analytic constant (Thread 2 positive result)
3. A null result with clear explanation of WHY the formula doesn't work (guides redirection)
4. The CAILculator finds unexpected structure in either sequence (bilateral confidence, high CV, etc.)

The paper (target April 1, 2026) benefits from either a positive result or a clearly-argued
null — both sharpen the analytic description of c₁ and the Weil ratio.

---

## LEAN 4 TARGETS (Paul's local environment — not Claude Code)

Document for reference only. Do not implement in Python.

**Target 1 — Bilateral Prime Isometry (Conjecture 29.3):**
```
theorem bilateral_prime_isometry (p : ℕ) (hp : p ∈ ({5, 7, 11} : Finset ℕ))
    (t σ : ℝ) : ‖F_sed (σ + t*I) * r_p p‖ = ‖F_sed (σ + t*I)‖
```
Proof strategy: r_p for p ∉ bilateral_triple is isometric — show r_p anticommutes
with all bilateral generators {q₂, q₃, q₄}.

**Target 2 — L_q3 Nilpotency (Phase 24T2):**
```
theorem L_q3_nilpotent : ∀ v ∈ bilateral_closure, L_q3 (L_q3 v) = 0
```
Follows from q₃² = 0 in sedenion algebra and the 12-vector closure structure.

---

*Phase 30 Handoff — March 26, 2026*
*Chavez AI Labs LLC · "Better math, less suffering"*
