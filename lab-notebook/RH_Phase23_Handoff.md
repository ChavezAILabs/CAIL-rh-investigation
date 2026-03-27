# RH Investigation — Working Handoff Document
## Chavez AI Labs LLC · March 24, 2026

**Prepared for:** New session or collaborator
**Working directory:** `C:\dev\projects\Experiments_January_2026\Primes_2026\`
**GitHub repo:** `CAIL-rh-investigation/` (subdirectory, separate git repo)
**Status:** Phase 22 complete. Phase 23 scripted, not yet written.

---

## What This Project Is

An open science empirical investigation into the Riemann Hypothesis using two novel tools:

- **Chavez Transform** — uses Cayley-Dickson sedenion zero divisor structure to analyze sequences across hypercomplex dimensions. Lean 4 verified.
- **ZDTP (Zero Divisor Transmission Protocol)** — lossless 16D→32D→64D transmission with six canonical gateway analyses.

The algebraic foundation is the **Canonical Six** — six framework-independent bilateral zero divisor patterns in 16D sedenion space (companion paper v1.3, Zenodo DOI: 10.5281/zenodo.17402495).

The central conjecture under investigation is **AIEX-001**: a Hilbert-Pólya operator H₅ in a 5D subspace of the E8 root lattice whose eigenvalues are the imaginary parts of the Riemann nontrivial zeros.

---

## AIEX-001 In One Page

**The embedding** (Phase 20B — canonical reference):

```python
import numpy as np
from mpmath import mp, zetazero
mp.dps = 25

sqrt2 = np.sqrt(2.0)

# 6D basis: [e2, e7, e3, e6, e4, e5]
# Block A {e2,e7}: primes p=7,11,13
# Block B {e3,e6}: primes p=3,5  (Heegner channel)
# Block C {e4,e5}: prime  p=2   (rank-1, single direction)

ROOT_DIRS = {
    2:  np.array([0, 0, 0, 0, 1, 1]) / sqrt2,   # q4 — Block C
    3:  np.array([0, 0,-1, 1, 0, 0]) / sqrt2,   # q2 — Block B (Heegner)
    5:  np.array([0, 0, 1, 1, 0, 0]) / sqrt2,   # v5 — Block B
    7:  np.array([1,-1, 0, 0, 0, 0]) / sqrt2,   # v1 — Block A
    11: np.array([1, 1, 0, 0, 0, 0]) / sqrt2,   # v4 — Block A
    13: np.array([-1,1, 0, 0, 0, 0]) / sqrt2,   # q3 — Block A (bilateral hub)
}
U_ANTISYM = np.array([0, 0, 0, 0, 1, -1]) / sqrt2  # (e4-e5)/sqrt2

def f5D(t):
    """Phase 20B embedding: maps Riemann zero imaginary part to 6D vector."""
    result = np.zeros(6)
    for p, r in ROOT_DIRS.items():
        result += (np.log(p) / np.sqrt(p)) * np.cos(t * np.log(p)) * r
    return result

def v_rho(sigma, t):
    """Full embedding: v(rho) = f5D(t) + (sigma-0.5)*u_antisym."""
    return f5D(t) + (sigma - 0.5) * U_ANTISYM
```

**Structural facts** (established, do not re-investigate):
- `v1 = −q3` (antipodal) → 6 roots span only **5D**, not 6D
- `v2 = u_antisym` → the antisymmetric direction is **reserved** for the functional equation
- Block C is structurally **rank 1** (single prime p=2, direction q4=(e4+e5)/√2)
- **G5** (5×5 Gram matrix via P5 projection) is the correct positive-definiteness object; G6 (6×6) has one structural zero eigenvalue

```python
# P5 projection: 6D -> 5D, combining e4/e5 into single (e4+e5)/sqrt2 direction
P5 = np.zeros((5, 6))
P5[0, 0] = 1.0; P5[1, 1] = 1.0; P5[2, 2] = 1.0; P5[3, 3] = 1.0
P5[4, 4] = 1.0 / sqrt2; P5[4, 5] = 1.0 / sqrt2

def gram_G5(F):
    F5 = F @ P5.T   # N×5
    return F5.T @ F5  # 5×5
```

**The AIEX-001 proof chain:**

| Step | Claim | Status |
|---|---|---|
| 1 | v(ρ) is equivariant under s→1−s ↔ s_α4 Weyl reflection | ✓ Verified (Phase 20B) |
| 2 | Critical-line zeros → v⁻=0 (purely 5D) | ✓ Theorem, no assumptions (Phase 19T3) |
| 3 | H₅⊕H₁ block structure forced by equivariance | ✓ Verified (Phase 19T3) |
| 4 | At most ONE zero can be off critical line | ✓ Consistency constraint (Phase 19T3) |
| 5 | G5 positive definite (N=100) | ✓ λ_min=10.46, cond=4.40 (Phase 22) |
| 6 | **aiex001_critical_line_forcing** | ✗ **MISSING — requires GSH or Schanuel** |

**The two unresolved assumptions** (algebraically undefeatable — Phase 21):
1. **Simple spectrum of H₅** — not derivable; degenerate H₅=I₅ satisfies all constraints (Phase 21A)
2. **Strong injectivity** / linear independence of {tₙ·log p} over ℚ — not derivable from algebra (Phase 21C); equivalent to Grand Simplicity Hypothesis + Schanuel's Conjecture

---

## Sedenion Multiplication (Thread 1 needs this)

```python
def cd_conj(v):
    """Cayley-Dickson conjugate: negate all non-scalar components."""
    return [v[0]] + [-x for x in v[1:]]

def cd_mul(a, b):
    """Recursive Cayley-Dickson multiplication (any 2^n dimension)."""
    n = len(a)
    if n == 1:
        return [a[0] * b[0]]
    h = n // 2
    a1, a2, b1, b2 = a[:h], a[h:], b[:h], b[h:]
    # (a1,a2)*(b1,b2) = (a1*b1 - conj(b2)*a2,  b2*a1 + a2*conj(b1))
    c1 = [x - y for x, y in zip(cd_mul(a1, b1), cd_mul(cd_conj(b2), a2))]
    c2 = [x + y for x, y in zip(cd_mul(b2, a1), cd_mul(a2, cd_conj(b1)))]
    return c1 + c2

# 16D sedenion representations of the 6 prime roots (0-indexed, unnormalized, norm=sqrt(2)):
#   v1  = e2 - e7     → positions 2(+1), 7(-1)
#   v4  = e2 + e7     → positions 2(+1), 7(+1)
#   q3  = e6 + e9     → positions 6(+1), 9(+1)
#   q2  = e5 + e10    → positions 5(+1), 10(+1)
#   v5  = e3 + e6     → positions 3(+1), 6(+1)
#   q4  = e3 - e12    → positions 3(+1), 12(-1)
```

**Known products** (from Phase 21B):
- `q3 × q2 = 0` and `q2 × q3 = 0` (bilateral zero divisors)
- `q3 × q4 = 0` and `q4 × q3 = 0` (bilateral zero divisors)
- `q2 × q4 = 2×(e6−e9)` — this exits the 6-root set and is the seed for algebraic closure

---

## Phase 22 Results (What Phase 23 Builds On)

| Result | Value | Significance |
|---|---|---|
| G5 PD | TRUE, λ_min=10.459, cond=4.40 | Zero images span full 5D; better cond than random (5.20) |
| λ_min trajectory N=10→100 | 0.69→10.46, monotone | Stable; no degeneracy trend |
| Block A | rank 2/2, cond=1.79, PD=True | p=7,11,13 span 2D subspace fully |
| Block B | rank 2/2, cond=1.35, PD=True | p=3,5 (Heegner) span 2D subspace fully |
| Block C | rank 1/2, structural | q4 is single direction — expected |
| Diagonal norm Chavez | zeros 73.8%, random 92.9% | GUE clustering breaks symmetric distribution |
| ZDTP signed inner products | zeros 62.6% ≈ random 63.8% | NULL — sorted pairwise ≠ sequential GUE |
| Inner product mean bias | +0.089 (zeros) vs ~0 (random) | Slight positive alignment — GUE clustering |

5D spanning rules out the "systematic collapse" failure mode. Only the "specific Diophantine coincidence" failure mode (addressed by GSH+Schanuel) remains.

---

## Phase 23 — Three Threads to Implement

Run in this order: **Thread 2 → Thread 1 → Thread 3**

---

### Thread 2 — λ_min(G5) Trajectory to N=500 + GUE Norm Comparison

**Files:** `rh_phase23_thread2.py`, `phase23_thread2_results.json`, `RH_Phase23_Thread2_Results.md`

**Computations:**

1. **Fetch zeros n=1..500** via `mpmath.zetazero` at dps=25

2. **Extended trajectory** — λ_min(G5) and condition number at N = 100, 150, 200, 250, 300, 400, 500

3. **Growth rate fitting** — fit λ_min(N) to three models, report best fit + R²:
   - Linear: `λ_min = a·N`
   - Square root: `λ_min = a·√N`  ← Marchenko-Pastur expectation for random matrices
   - Logarithmic: `λ_min = a·log(N) + b`

4. **Random controls** — 10 seeds (uniform t ∈ [14, t_N]) at each N; compare λ_min and cond

5. **Block trajectories** — track the smaller eigenvalue of the 2×2 G_A block and 2×2 G_B block at each N

6. **GUE norm comparison** — the open question from Phase 22: does a GUE-distributed spacing sequence score ~73% (like zeros) or ~93% (like uniform random)?
   - GUE Wigner surmise (β=2): P(s) = (32/π²)·s²·exp(−4s²/π), mode at s=√(π)/2≈0.886
   - Use rejection sampling; generate N=100 normalized spacings
   - Scale to span same t-range as actual zeros [14.135, 236.524]
   - Compute ‖f₅D(tₙ)‖², sort, apply Chavez conjugation symmetry
   - Repeat for 10 GUE seeds; report mean ± std

**Key result:** If λ_min ∝ √N → zeros behave like random matrix ensemble (GUE-consistent). If GUE control scores ~73% → norm inversion confirmed as GUE signature.

---

### Thread 1 — Algebraic Closure of the 6-Root Set

**Files:** `rh_phase23_thread1.py`, `phase23_thread1_results.json`, `RH_Phase23_Thread1_Results.md`

Find the minimal set of sedenion unit vectors closed under multiplication that contains all 6 prime roots.

**Computations:**

1. **Closure generation** — iterative algorithm:
   - Start: 6 prime roots as 16D vectors (normalized to ‖v‖=1)
   - Compute all pairwise products (both orders) → 36 products
   - For each nonzero product: normalize, check if already in set
   - If new: add to set, expand the product table
   - Terminate when no new vectors appear
   - Report: final size, generations to stabilization

2. **Product table** — for all 36 initial root×root products, record:
   - Scalar part (position 0), vector part (positions 1–15), norm²
   - Classification: zero / in original set / in bilateral family / new

3. **New vector characterization** — for each closure vector not in the original 6:
   - Which sedenion positions are nonzero?
   - Does it lie in the 5D fixed subspace {v[4]=v[5]}?
   - Is it in the Phase 18D bilateral family (E8 first shell)?
   - What bilateral zero divisor partners does it have?

4. **Root system identification** — does the closed set form D₄, E₆, E₇, E₈, or other?
   Check: closed under negation? What is its rank? What are the inner products?

5. **Prime correspondence** — do any new closure directions match the cross-block directions used for p=17,19,23 in the Phase 20C 9-prime formula?

**Seed vector:** q2×q4 = 2×(e6−e9), i.e., positions 6(+1), 9(−1) — this is generation 2.

---

### Thread 3 — Weil Explicit Formula Vector Identity

**Files:** `rh_phase23_thread3.py`, `phase23_thread3_results.json`, `RH_Phase23_Thread3_Results.md`

Test whether the vector-valued Weil explicit formula is numerically satisfied by the f₅D embedding.

The f₅D formula is the k=1 prime terms of the Weil explicit formula with a vector-valued test function. The identity:

```
Σ_{n=1}^N f₅D(tₙ)  →  -Σ_p (log p / √p) · r_p · [archimedean terms]  as N→∞
```

**Computations:**

1. **Partial sums** — `S(N) = Σ_{n=1}^N f₅D(tₙ)` for N = 10, 50, 100, 200, 500
   Report: direction, norm, block breakdown (S_A, S_B, S_C)

2. **Euler product DC component** — compute the right-hand side "DC" term:
   ```
   RHS_k = -Σ_p r_p · log(p) · Σ_{j=1}^k p^(-j/2)
   ```
   for k=1,2,3,4,5. Compare direction and magnitude to S(N).

3. **Residual analysis** — `residual(N) = S(N) − scaled_RHS`. Does ‖residual(N)‖/‖S(N)‖ shrink as N grows?

4. **Per-block Weil check** — compute S_A(N), S_B(N), S_C(N) separately. Does convergence differ by block?

5. **Positivity criterion** — compute `P(N) = Σ_{n=1}^N ‖f₅D(tₙ)‖²` for N=10..500. Does P(N)/N converge, and to what? Compare to E[‖f₅D‖²] under GUE.

**Note:** S(N) is expected to oscillate (zeros come in conjugate pairs; f₅D involves cosines). The key question is whether the running mean S(N)/N converges toward the Euler product RHS.

---

## Output Standards

**JSON:** All numpy types → Python native (float/int/bool); no `inf`/`NaN` → use `None`

**Sequences ≥50 elements:** Save in `cailculator_sequences` JSON key for CAILculator MCP handoff in Claude Desktop. Do NOT compute Chavez locally for these — defer to MCP.

**MD format** (match prior phases exactly):
```
# Phase 23 Thread N Results — [Title]
## Chavez AI Labs LLC · [Date]
**Status:** COMPLETE
**Script:** `rh_phase23_threadN.py`
**Output:** `phase23_threadN_results.json`
---
## Headline
[bold finding]
---
## Section 1: ...
[numbered sections with tables]
---
## Summary Table
| Result | Finding | Significance |
---
## Open Questions for Phase 24
---
*Phase 23 Thread N completed [date]*
*Chavez AI Labs LLC · Applied Pathological Mathematics · "Better math, less suffering"*
```

---

## Closed Avenues (Do NOT Re-investigate)

| Avenue | Phase | Reason |
|---|---|---|
| Simple spectrum from bilateral algebra | 21A | Degenerate H₅=I₅ satisfies all constraints |
| Module map H₅(q₃×v) = q₃×H₅(v) | 21C | ILL-DEFINED — products escape 5D subspace |
| Bilateral → embedding zeros | 21C | 0/105 zero products among f₅D(tᵢ)·f₅D(tⱼ) |
| Chavez on sorted pairwise inner products | 22 | NULL — sorted pairwise ≠ sequential GUE |
| Route C (GUE universality) | 16 | ELIMINATED — χ₃/χ₄/ζ have different prime content |

---

## Key File Inventory

### Scripts (reference for sedenion code)
| File | What to reuse |
|---|---|
| `rh_phase17b_prep.py` | `cd_mul`, `cd_conj` (canonical sedenion multiplication) |
| `rh_phase20b.py` | `f5D` embedding — canonical reference |
| `rh_phase21b.py` | sedenion products of root vectors |
| `rh_phase21c.py` | Fixed-subspace tests |
| `rh_phase22.py` | `gram_G5`, `P5`, `safe()` JSON helper, `conjugation_symmetry` |

### Results
| File | Contents |
|---|---|
| `phase22_results.json` | G5 results; `cailculator_sequences.*` (7 sequences) |
| `phase21b_results.json` | Triple product identity; bilateral zero divisor table |
| `RH_Phase22_Results.md` | Full Phase 22 results including ZDTP null result |
| `RH_Phase23_Prehandoff.md` | Claude Desktop Phase 23 briefing (additional context) |

### GitHub repo (`CAIL-rh-investigation/`)
**Phase 22 not yet committed** — add: `rh_phase22.py`, `phase22_results.json`, `RH_Phase22_Results.md` to scripts/, results/, docs/phases/; update README phases table.

---

## Broader Context

- **Researcher:** Paul Chavez, Chavez AI Labs LLC
- **CAILculator MCP** — available in Claude Desktop only (not Claude Code). Scripts prepare `cailculator_sequences` JSON keys for MCP handoff.
- **Chavez conjugation symmetry formula:** `1 − mean(|x[i]−x[n−1−i]| for i in range(n//2))` on sequence normalized to [0,1]
- **Route B** = Euler product arithmetic mechanism (confirmed Phase 16); **Route C** = GUE universality (eliminated Phase 16)
- **Block B = Heegner channel** — {e₃,e₆} subspace corresponds to L-functions of ℚ(√−3) and ℚ(√−2)
- **q₃ (p=13) is the bilateral hub** — the only root that annihilates both q₂ (p=3) and q₄ (p=2)
- **Paper target:** April 1, 2026 — Sophie Germain's 250th birthday; Phase 20A (consolidation) still queued
- Null results are as valued as positive ones. The investigation goal is systematic exhaustion of algebraic and analytic approaches.

---

*Phase 23 Handoff prepared March 24, 2026*
*Chavez AI Labs LLC · Applied Pathological Mathematics · "Better math, less suffering"*
