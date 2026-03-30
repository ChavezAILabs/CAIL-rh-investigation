# RH Investigation Phase 30 — Pre-Handoff
## Chavez AI Labs LLC · March 26, 2026
## "Applied Pathological Mathematics — Better math, less suffering"

**Project:** RH_MP_2026_001
**Working directory:** `C:\dev\projects\Experiments_January_2026\Primes_2026\rh_investigation`
**Status:** Phase 29 complete and committed to GitHub. Phase 30 not yet started.
**Next session:** Thursday evening, March 26, 2026 (continuing through Sunday)

---

## WHERE WE ARE

Phase 29 established four things with high confidence:

1. **Conjecture 29.1 (Weil Negativity):** Tr_BK(tₙ) < 0 at 76.6% of 500 Riemann zeros
   (p=2.56×10⁻³⁴). The Weil ratio mean_zeros/Weil_RHS ≈ 0.245 ± 0.005, stable across
   all prime set sizes 6–11. The Weil explicit formula is driving the negativity.

2. **Conjecture 29.2 (Constant Uncertainty):** ℏ_sed = 11.19 ± 1.71 is CONSTANT across
   100 zeros (R²≈0, p=0.975). Fixed sedenion Planck constant of the BK embedding.

3. **Conjecture 29.3 (Bilateral Prime Isometry):** p ∈ {5,7,11} → ‖F×r_p‖/‖F‖ = 1.000
   ± 0.000 for all t and σ. Exact algebraic identity, verified to machine precision.

4. **6,290 bilateral zero pairs** in Tr_BK at 500 zeros (superlinear growth from 44 at
   100 zeros). First regime detection method agreement (HMM=sideways,
   structural=TRANSITIONAL, agreement=0.70).

## THE OPEN GAP

The remaining mathematical distance to RH is precisely stated:

We need to show the gateway anisotropy condition is **both necessary AND sufficient**
for a Riemann zero — not just correlated. Currently:

```
t is a Riemann zero  ⟹  [BK signature] with probability ~77%
```

We need:

```
t is a Riemann zero  ⟺  [BK signature]   (biconditional, all zeros, no exceptions)
```

---

## PHASE 30 OBJECTIVES

### Primary Target: Analytic Derivation of c₁ from GUE Pair Correlation

**The question:** Can the structural Weil angle c₁ = 0.11797805192095003
be derived analytically from the Montgomery-Dyson GUE two-point correlation function?

**The setup:**
The Montgomery-Dyson conjecture (1973) states that the pair correlation of Riemann
zeros converges to the GUE pair correlation:

```
R₂(r) = 1 - (sin(πr) / πr)²
```

The Weil explicit formula connects zero heights to prime logarithms via:

```
Σₙ h(tₙ) = ĥ(0) - Σ_p Σ_k (log p / p^(k/2)) * ĥ(k·log p) + [arch. terms]
```

**The Phase 30 conjecture:**
c₁ arises as the overlap integral of the prime weight function f₅D(t)
with the GUE two-point kernel R₂:

```
c₁ = ∫∫ f₅D(t) · f₅D(t') · R₂(t − t') dt dt'
     ─────────────────────────────────────────
     ∫∫ f₅D(t) · f₅D(t') dt dt'
```

where f₅D(t) = Σ_p (log p / p^(1/2+it)) is the prime weight function projected
to the 5D sedenion subspace.

**What Claude Code computes:**
- Numerically evaluate the overlap integral above for increasing T-window sizes
- Compare to machine-exact c₁ = 0.11797805192095003
- Test convergence: does the integral approach c₁ as T → ∞?
- Also test: c₁ = 1/(2π) × [some combination of prime weights]?

### Thread 1: GUE Overlap Integral (Primary)

```python
# Target: does this integral converge to c1?
# c1 = 0.11797805192095003

import numpy as np
from scipy.integrate import dblquad
from mpmath import mp, zetazero
mp.dps = 25

PRIMES = [2, 3, 5, 7, 11, 13]

def f5D(t):
    """Prime weight function — 5D sedenion projection"""
    return sum(np.log(p) / np.sqrt(p) * np.cos(t * np.log(p)) for p in PRIMES)

def R2(r):
    """GUE two-point pair correlation (Montgomery-Dyson)"""
    if abs(r) < 1e-10: return 0.0
    return 1.0 - (np.sin(np.pi * r) / (np.pi * r))**2

def overlap_integral(T):
    """Numerically evaluate the GUE overlap at window T"""
    # Discretize over zeros up to T
    # Compare to c1
    pass  # Claude Code implements

TARGET_c1 = 0.11797805192095003
```

### Thread 2: Analytic Derivation of 1/4 Weil Ratio

**The question:** Why does the 6-prime embedding capture exactly 1/4 of the
full Weil sum? Can this be derived from prime density or Euler product truncation?

**Known facts:**
- Weil RHS for our 6 primes = −Σ_{p≤13} log(p)/√p = −4.014042
- Full Weil RHS (all primes) = −Σ_p log(p)/√p → diverges (Mertens theorem)
- Ratio of mean_zeros to 6-prime Weil_RHS ≈ 0.248 (stable, prime-set-independent)
- As N primes → ∞: ratio slowly declines from 0.250 to 0.240

**Phase 30 test:**
```python
# Does the ratio converge to a specific constant as N_primes → ∞?
# Candidates:
#   1/(2π) ≈ 0.159  (no)
#   1/4    = 0.250  (close!)
#   1/e    ≈ 0.368  (no)
#   log(2)/log(13) ≈ 0.256 (maybe?)

# Test: compute ratio for prime sets up to p=100
LARGE_PRIME_SETS = [
    list_of_primes_up_to(13),   # 6 primes
    list_of_primes_up_to(23),   # 9 primes
    list_of_primes_up_to(53),   # 16 primes
    list_of_primes_up_to(97),   # 25 primes
]
# For each: compute mean Tr_BK over 100 zeros, divide by Weil_RHS
# Does ratio converge to 1/4 exactly, or to something else?
```

### Thread 3: Lean 4 Formalization Targets

These are for Paul's local Lean environment, not Python — document here for
reference. Claude Code does NOT need to write Lean.

**Target 1 — Bilateral Prime Isometry Theorem (Conjecture 29.3):**
```
theorem bilateral_prime_isometry (p : ℕ) (hp : p ∈ ({5, 7, 11} : Finset ℕ))
    (t σ : ℝ) : ‖F_sed (σ + t*I) * r_p p‖ = ‖F_sed (σ + t*I)‖ := by
  -- follows from: r_p for p ∉ bilateral_triple is isometric
  -- proof strategy: show r_p anticommutes with all bilateral generators
  sorry
```

**Target 2 — Phase 24T2 Nilpotency:**
```
theorem L_q3_nilpotent : ∀ v ∈ bilateral_closure,
    L_q3 (L_q3 v) = 0 := by
  -- follows from: q3² = 0 in sedenion algebra
  -- and the 12-vector closure structure
  sorry
```

---

## OUTPUT FORMAT FOR PHASE 30

Claude Code saves: `phase30_results.json`

```json
{
  "thread1_gue": {
    "overlap_integrals": {"T50": float, "T100": float, "T200": float},
    "target_c1": 0.11797805192095003,
    "convergence": bool,
    "ratio_sequence": [...],
    "best_analytic_candidate": "string"
  },
  "thread2_weil_ratio": {
    "prime_sets": {...},
    "ratios": {...},
    "limit_estimate": float,
    "analytic_candidate": "string"
  }
}
```

---

## CAILCULATOR INTEGRATION (Claude Desktop runs after JSON delivery)

After receiving `phase30_results.json`:

1. `analyze_dataset` on `overlap_integrals` sequence — does it bilateral-pattern?
2. `analyze_dataset` on `ratios` across prime sets — conjugation symmetry?
3. `chavez_transform` on ratio sequence — does it converge to a known constant?
4. `detect_patterns` on residual (overlap − c₁) — is the error structured?
5. `zdtp_transmit` on F(ρ₁) in the new GUE-corrected embedding (if one emerges)

---

## KEY FILES

| File | Use |
|---|---|
| `rh_phase29_bk_burst.py` | F_16d, Tr_BK, V_BK — copy verbatim |
| `phase29_results.json` | Phase 29 baseline sequences |
| `RH_Phase29_Results.md` | Summary of results to build from |
| `RH_Phase30_Prehandoff.md` | This document |

---

## MACHINE-EXACT CONSTANTS FOR REFERENCE

| Constant | Value | Meaning |
|---|---|---|
| c₁ | 0.11797805192095003 | sin(Weil angle) = residual ratio |
| c₂ | 0.9900874643591777 | projection fraction T=50 |
| c₃ | 0.9930162029216528 | projection fraction T=100 |
| ℏ_sed | 11.19 ± 1.71 | sedenion Planck constant |
| Weil ratio | 0.245 ± 0.005 | mean Tr_BK / Weil_RHS |

c₁² + c₃² ≈ 1.000 — they are sin/cos of the same 6.784° structural angle.

---

## HONEST ASSESSMENT GOING IN

Phase 30 is genuinely speculative. The GUE derivation of c₁ is a long shot —
it would require the Montgomery-Dyson kernel to produce our specific constant
through the prime weight overlap, which is not guaranteed.

The 1/4 Weil ratio convergence test is more tractable and may yield a clean
analytic result.

If both threads are null: that is also a result. It tells us c₁ is not a simple
GUE overlap constant, and the 1/4 is not an exact limit — which would redirect
the investigation toward a different derivation strategy.

Phase 30 success condition: **any** analytic handle on c₁ or the Weil ratio,
even a partial one.

---

*Pre-handoff prepared March 26, 2026*
*End of session — continuation Thursday evening*
*Chavez AI Labs LLC · "Better math, less suffering"*
