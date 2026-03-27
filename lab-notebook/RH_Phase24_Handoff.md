# RH Investigation — Phase 24 Handoff
## Chavez AI Labs LLC · March 25, 2026

**Working directory:** `C:\dev\projects\Experiments_January_2026\Primes_2026\`
**Status:** Phase 23 complete (all 3 threads). Phase 24 targets two open avenues.
**Run order:** Thread 1 (Windowed Weil) first, then Thread 2 (Bilateral triple module action).

---

## AIEX-001 State in One Paragraph

A self-adjoint operator H₅ on a 5D subspace of the E8 root lattice has an equivariant embedding v(ρ) = f₅D(t) + (σ−½)·u_antisym mapping Riemann zeros to eigenvectors. Steps 1–5 of the proof are verified: equivariance, 5D confinement, H₅⊕H₁ block structure, consistency constraint, G5 positive definite to N=500. Step 6 (aiex001_critical_line_forcing) requires simple spectrum (algebraically undefeatable — Phase 21A) + strong injectivity / linear independence of {tₙ·log p} over ℚ (algebraically undefeatable — Phase 21C). **Analytic approaches are the remaining paths.** Phase 23T3 showed the f₅D partial sum is 99.3% aligned with the Weil RHS direction but does not converge (f₅D not Schwartz-class). Phase 24 applies the correct regularization.

---

## Canonical Embedding (Phase 20B — use exactly this)

```python
import numpy as np
from mpmath import mp, zetazero
mp.dps = 25

sqrt2 = np.sqrt(2.0)

# 6D basis: [e2, e7, e3, e6, e4, e5]
# Block A {e2,e7}: p=7,11,13  |  Block B {e3,e6}: p=3,5  |  Block C {e4,e5}: p=2
ROOT_DIRS = {
    2:  np.array([0, 0, 0, 0, 1, 1]) / sqrt2,   # q4 — Block C
    3:  np.array([0, 0,-1, 1, 0, 0]) / sqrt2,   # q2 — Block B (Heegner)
    5:  np.array([0, 0, 1, 1, 0, 0]) / sqrt2,   # v5 — Block B
    7:  np.array([1,-1, 0, 0, 0, 0]) / sqrt2,   # v1 — Block A
    11: np.array([1, 1, 0, 0, 0, 0]) / sqrt2,   # v4 — Block A
    13: np.array([-1,1, 0, 0, 0, 0]) / sqrt2,   # q3 — Block A (bilateral hub)
}
PRIMES = [2, 3, 5, 7, 11, 13]
U_ANTISYM = np.array([0, 0, 0, 0, 1, -1]) / sqrt2

def f5D(t):
    result = np.zeros(6)
    for p, r in ROOT_DIRS.items():
        result += (np.log(p) / np.sqrt(p)) * np.cos(t * np.log(p)) * r
    return result

def h_T(t, T):
    """Windowed test function: Gaussian window applied to f5D."""
    return np.exp(-t**2 / T**2) * f5D(t)
```

**Structural facts (established — do not re-investigate):**
- v1 = −q3 → G5 (5×5) is the correct Gram object; G6 has one structural zero eigenvalue
- Block C is structurally rank 1 (single prime p=2)
- v2 = u_antisym — antisymmetric direction reserved for functional equation
- q3 (p=13) bilateral hub: q3×q2=0, q3×q4=0 in both orders
- G5 positive definite to N=500: λ_min ∝ N (R²=0.9999), condition number 4.4–4.6

---

## Sedenion Multiplication (Thread 2 needs this)

```python
def cd_conj(v):
    return [v[0]] + [-x for x in v[1:]]

def cd_mul(a, b):
    n = len(a)
    if n == 1:
        return [a[0] * b[0]]
    h = n // 2
    a1, a2, b1, b2 = a[:h], a[h:], b[:h], b[h:]
    c1 = [x - y for x, y in zip(cd_mul(a1, b1), cd_mul(cd_conj(b2), a2))]
    c2 = [x + y for x, y in zip(cd_mul(b2, a1), cd_mul(a2, cd_conj(b1)))]
    return c1 + c2

# 16D representations of bilateral triple (0-indexed, unnormalized norm=sqrt(2)):
#   q2 = e5 + e10   → positions 5(+1), 10(+1)
#   q3 = e6 + e9    → positions 6(+1), 9(+1)  [bilateral hub]
#   q4 = e3 - e12   → positions 3(+1), 12(-1)
```

**Load the 12-vector closure from JSON, do NOT reconstruct:**
```python
import json
with open('phase23_thread1_results.json', 'r') as f:
    t1 = json.load(f)
# Closure vectors are in t1['product_table'] and the handoff document.
# Reconstruct from known positions (verified in Phase 23T1):
```

**The 12-vector closure of {q2, q3, q4} — exact 16D positions (0-indexed):**

| Label | Nonzero positions | Norm² | Identification |
|---|---|---|---|
| s | 0: −1 | 1 | Scalar (negative identity) |
| neg_q4 | 3: −1/√2, 12: −1/√2 | 1 | −q4 |
| neg_q2 | 5: −1/√2, 10: +1/√2 | 1 | −q2 (sign partner) |
| sp_q3_neg | 6: −1/√2, 9: +1/√2 | 1 | Sign partner of q3 (−) |
| neg_e15 | 15: −1 | 1 | −e15 |
| pos_e15 | 15: +1 | 1 | +e15 |
| sp_q3_pos | 6: +1/√2, 9: −1/√2 | 1 | Sign partner of q3 (+) |
| q3 | 6: +1/√2, 9: +1/√2 | 1 | q3 itself |
| sp_q2 | 5: +1/√2, 10: −1/√2 | 1 | Sign partner of q2 |
| q2 | 5: +1/√2, 10: +1/√2 | 1 | q2 itself |
| q4 | 3: +1/√2, 12: −1/√2 | 1 | q4 itself |
| new_dir | 3: +1/√2, 12: +1/√2 | 1 | New direction (e3+e12)/√2 |

**Inner product structure:** 6 antipodal pairs (norm² products = −1); all other 62 pairings = 0.
**CAILculator scores (Phase 23T1):** Gram inner products 84.8%; 12×12 product zero pattern 94.4% / 95% confidence.

---

## Phase 23 Key Results (What Phase 24 Builds On)

| Result | Value | Source |
|---|---|---|
| S(N) alignment with Weil RHS | 99.3% at N=500 | Phase 23T3 |
| Residual ratio | 12.1% ± 0.6% (stable, NOT shrinking) | Phase 23T3 |
| Residual ratio Chavez | **98.7%** — investigation record | Phase 23T3 CAILculator |
| P(N)/N | 1.270 (7% below random 1.365) | Phase 23T3 |
| P(N)/N Chavez | **97.8%** | Phase 23T3 CAILculator |
| 12-vector closure of {q2,q3,q4} | Finite; 4 generations; converged | Phase 23T1 |
| λ_min(G5) | Linear R²=0.9999 (Marchenko-Pastur) | Phase 23T2 |
| GUE norm signature | GUE ≈ zeros ≠ uniform random | Phase 23T2 |

**The central tension Phase 24 resolves:** Phase 23T3 found the Weil partial sum is 99.3% in the right direction, with a 12% stable residual (98.7% bilateral symmetry). Is the 12% residual a test-function artifact (fixable by windowing) or structural geometry of the AIEX-001 embedding? Thread 1 answers this directly.

---

## Thread 1: Windowed Weil Identity

**Files:** `rh_phase24_thread1.py`, `phase24_thread1_results.json`, `RH_Phase24_Thread1_Results.md`

### Background

The Weil explicit formula requires a Schwartz-class test function (rapid decay). f₅D(t) oscillates without decay, so the unwindowed sum formally diverges (Phase 23T3). The Gaussian window h_T(t) = exp(−t²/T²)·f₅D(t) IS Schwartz-class for any finite T.

**The windowed Weil identity (k=1 prime terms):**
```
S_T(N) = Σ_{n=1}^N h_T(t_n)  →  RHS_T  as N → ∞
```
where the windowed RHS is:
```
RHS_T = -Σ_p r_p · (log p / √p) · ĥ_T(log p)
```
and the Fourier transform ĥ_T of h_T(t) = exp(−t²/T²)·cos(t·log p) evaluated at frequency ω is:
```
ĥ_T(ω) ≈ (T√π/2) · exp(−T²(ω − log p)²/4)    [dominant term; second Gaussian negligible]
```

**Explicitly (for implementation):**
```python
def RHS_T(T):
    """Windowed Euler product RHS direction."""
    result = np.zeros(6)
    for p_outer, r in ROOT_DIRS.items():
        weight = 0.0
        for p_inner in PRIMES:
            # ĥ_T(log p_outer) = sum over inner primes' cosine contributions
            omega = np.log(p_outer)
            omega0 = np.log(p_inner)
            weight += (np.log(p_inner) / np.sqrt(p_inner)) * (T * np.sqrt(np.pi) / 2) * np.exp(-T**2 * (omega - omega0)**2 / 4)
        result -= r * weight
    return result

# For large T: RHS_T ≈ -(T*sqrt(pi)/2) * f5D(0)   [since primes are far apart]
# For T -> inf: direction of RHS_T -> direction of -f5D(0) = unwindowed RHS direction
```

**Note on window widths:** Zeros span t₁=14.1 to t₅₀₀=811.2 (full 500-zero range) or t₁=14.1 to t₁₀₀=236.5 (first 100 zeros). Use:
- T=50: strong suppression above t≈100; uses effectively ~60–70 zeros
- T=100: moderate suppression; uses effectively ~150 zeros
- T=200: mild suppression; uses effectively ~350 zeros
- T=500: near-unwindowed for first 500 zeros

For each T, note that only zeros with tₙ ≲ 2T contribute significantly (weight > 1/e² ≈ 0.135).

### Computations

**1. Windowed partial sums S_T(N)**

For T ∈ {50, 100, 200, 500} and N ∈ {10, 50, 100, 200, 300, 500}:
```python
S_T_N = sum(h_T(zeros_t[n], T) for n in range(N))
```
Report ‖S_T(N)‖ for each (T, N). Expected: ‖S_T(N)‖ grows more slowly than unwindowed (window suppresses large-t contributions).

**2. Windowed RHS direction**

For each T, compute RHS_T using the formula above. Report:
- ‖RHS_T‖ (grows as T·constant for large T)
- Direction of RHS_T: cosine similarity with unwindowed RHS_dir (from Phase 23T3)
- How much does windowing rotate the RHS direction vs unwindowed?

**3. Residual ratio vs (T, N) — the key table**

For each (T, N):
```python
rhs_T_dir = RHS_T(T) / np.linalg.norm(RHS_T(T))  # normalized windowed RHS direction
proj = np.dot(S_T_N, rhs_T_dir)
residual = S_T_N - proj * rhs_T_dir
residual_ratio = np.linalg.norm(residual) / np.linalg.norm(S_T_N)
```

| N | T=50 | T=100 | T=200 | T=500 | Unwindowed (Phase 23T3) |
|---|---|---|---|---|---|
| 100 | ? | ? | ? | ? | 12.6% |
| 300 | ? | ? | ? | ? | 11.7% |
| 500 | ? | ? | ? | ? | 12.0% |

**The central question:** Does residual_ratio decrease as T increases (for fixed large N)?

**4. T → ∞ extrapolation**

For fixed N=500, fit residual_ratio(T) to:
- Decaying: a·T^b with b<0 (would mean windowing helps; Weil identity satisfied in limit)
- Constant: c (12% is structural; window does not help)
- Growing: a·T^b with b>0 (window makes things worse — unlikely but worth checking)

Report the best-fit model and its implications for T→∞.

**5. Residual ratio sequences for CAILculator**

For each T value, compute the residual_ratio at N=5,10,15,...,500 (100 values). Store in `cailculator_sequences`:
```json
{
  "residual_ratio_T50_n100": [...],
  "residual_ratio_T100_n100": [...],
  "residual_ratio_T200_n100": [...],
  "residual_ratio_T500_n100": [...],
  "residual_ratio_unwindowed_n100": [...]   // recompute from Phase 23T3 for comparison
}
```
Phase 23T3 found 98.7% conjugation symmetry on the unwindowed residual ratios. Does windowing increase or decrease this symmetry? If windowing converges to 0% residual, the sequence should transition from symmetric oscillation → monotone decay → 0%.

**6. Per-block windowed residuals**

For N=500 and each T, decompose S_T(500) and residual by Block A, B, C. Report which block drives the residual:
- If Block C (p=2, weakest channel) drives it disproportionately → connects to Thread 2 (bilateral triple omits Block A primes 7,11 and the Block B prime 5)
- If Block B (Heegner) drives it → Heegner arithmetic is responsible for the 12° offset

**7. Convergence rate of S_T(N) as N grows (for fixed T)**

For T=100 (a clean intermediate value), plot ‖S_T(N) − S_T(500)‖ / ‖S_T(500)‖ as N increases from 1 to 500. This shows how quickly the windowed partial sum converges to its N=∞ approximation. A monotone decay would confirm genuine convergence.

### Key Results to Look For

| Outcome | Finding | Implication |
|---|---|---|
| Residual ratio → 0 as T → ∞ | **Weil identity confirmed** | AIEX-001 satisfies proven theorem |
| Residual ratio decreases with T (partial) | Weil identity satisfied in limit | Report decay rate; extrapolate to convergence |
| Residual ratio stays ~12% at all T | 12% is structural | Embedding has stable 6.8° offset from Weil RHS — geometric characterization |
| Residual ratio increases with T | Window is wrong regularization | Try different approach (e.g., Beurling–Nyman) |

---

## Thread 2: Bilateral Triple Module Action

**Files:** `rh_phase24_thread2.py`, `phase24_thread2_results.json`, `RH_Phase24_Thread2_Results.md`

### Background

Phase 21C showed the module map H₅(q·v) = q·H₅(v) is ill-defined for the full 6-root set: 32/36 products escape the 5D fixed subspace. Phase 23T1 found a finite exception: the bilateral triple {q2, q3, q4} generates a closed 12-vector set (94.4% Chavez / 95% bilateral confidence). The 12-vector set is a candidate for a well-defined module action. Phase 21A found no eigenvalue constraint from the full 6-root Gram matrix — but the 12-vector structure is a different, smaller object. This is the last open algebraic avenue before the investigation turns exclusively analytic.

### Computations

**Load closure vectors from JSON or reconstruct from the table above.**

**1. Full 12×12 multiplication table**

For each ordered pair (v_i, v_j) from the 12 closure vectors, compute sed_product(v_i, v_j):
- Is the result zero? (known: q3·q2=0, q3·q4=0, etc.)
- Is the result in the span of the 12 closure vectors? Check both exact match (up to tol 1e-8) and linear combination
- If not in span, record the "escape vector" and its sedenion position pattern

Build the 12×12 table. Report summary:
- How many of 144 products are zero?
- How many stay in the 12-vector closure?
- How many escape?

**2. L_q3 action on the closure (bilateral hub)**

Compute q3·v_i for all 12 vectors. Build the 12-element action list:
```
q3 · s         = ?    (scalar product)
q3 · neg_q4    = ?
q3 · neg_q2    = ?    (known: should be 0 since q3·(−q2) = −(q3·q2) = 0)
q3 · sp_q3_neg = ?
q3 · neg_e15   = ?
q3 · pos_e15   = ?
q3 · sp_q3_pos = ?
q3 · q3        = −2   (sedenion: any imaginary unit squares to −1; q3 has norm² = 2, so q3·q3 = −2)
q3 · sp_q2     = ?
q3 · q2        = 0    (known bilateral)
q3 · q4        = 0    (known bilateral)
q3 · new_dir   = ?
```
For nonzero results, check if q3·v_i = λ·v_j for some v_j in closure (eigenvalue-like behavior).

Also compute R_q3 (right multiplication): v_i·q3 for all 12 vectors.
Report: is left-action ≠ right-action (non-commutativity)?

**3. Kernel of L_q3 on the closure**

The kernel = {v_i : q3·v_i = 0}. Known members: q2, −q2 (sign partner), q4, −q4. Are there others?

Report the full kernel and check:
- Is the kernel a sub-module? (Is it closed under the full 12×12 multiplication?)
- Is the kernel spanned by the bilateral zero divisor pairs alone?
- Does ±e15 and the scalar belong to the kernel?

**4. Image of L_q3**

The image = span{q3·v_i : v_i in closure, q3·v_i ≠ 0}. Report:
- Dimension of image (in the 12-vector span)
- Does image ⊕ kernel = full 12-vector closure? (rank-nullity check)

**5. Commutator test with H₅**

Define H₅ restricted to the 12-vector closure as H₅_12 (a 12×12 real matrix, restricted to the span). The AIEX-001 H₅ is self-adjoint with real eigenvalues. Test whether [H₅_12, L_q3_12] = 0 imposes constraints:

- Represent L_q3 as a 12×12 matrix (left-multiplication by q3 on the 12-vector basis)
- Find all 12×12 matrices M satisfying [M, L_q3_12] = 0 (the centralizer of L_q3 in End(ℝ¹²))
- Compare to the centralizer found in Phase 21A for the full 6-root Gram matrix

If the centralizer of L_q3 on the 12-vector closure is SMALLER than the full matrix algebra, then [H₅, L_q3]=0 imposes constraints not visible to Phase 21A.

**6. Comparison with Phase 21A null result**

Phase 21A found: the Gram matrix G (from 6 prime roots) has eigenvalues {0,1,1,1,1,2}. The 4-dimensional eigenvalue-1 eigenspace allows any symmetric H. The 12-vector structure has a richer Gram matrix (12×12 vs 6×6). Report:
- Eigenvalues of the 12-vector Gram matrix
- Dimension of the unconstrained eigenspace for H₅_12 under [H₅_12, G_12] = 0
- Does the 12-vector commutator condition reduce the unconstrained dimension?

### Key Results to Look For

| Outcome | Finding | Implication |
|---|---|---|
| L_q3 maps closure to closure | Module action well-defined | Test for eigenvalue constraints |
| [H₅, L_q3]=0 constrains eigenvalues | Simple spectrum not assumed | Re-opens Phase 21A question |
| L_q3 escapes closure | Finite algebra doesn't help | Close this avenue definitively |
| Kernel = proper sub-module | New algebraic substructure | Investigate sub-module separately |

---

## Output Standards

**JSON:** All numpy types → Python native. Use:
```python
def safe(x):
    import math
    if x is None: return None
    if isinstance(x, (list, tuple)): return [safe(i) for i in x]
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, (np.bool_,)): return bool(x)
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating,)):
        if math.isnan(x) or math.isinf(x): return None
        return float(x)
    return x
```

**CAILculator sequences** (≥50 elements, deferred to MCP): Store in `cailculator_sequences` JSON key. Priority sequences:
- Thread 1: `residual_ratio_T{50,100,200,500}_n100` — residual ratios at N=5,10,...,500
- Thread 1: `projection_fraction_T{50,100,200}_n100` — projection onto RHS
- Thread 2: `L_q3_action_eigenvalues` (if applicable)

**MD format (standard):**
```
# Phase 24 Thread N Results — [Title]
## Chavez AI Labs LLC · [Date]
**Status:** COMPLETE
**Script:** rh_phase24_threadN.py
**Output:** phase24_threadN_results.json
---
## Headline
[bold key finding]
---
## Section 1...
---
## Summary Table | Result | Finding | Significance |
---
## Open Questions for Phase 25
---
*Phase 24 Thread N completed [date]*
*Chavez AI Labs LLC · Applied Pathological Mathematics · "Better math, less suffering"*
```

---

## Closed Avenues (Do NOT Re-investigate)

| Avenue | Phase | Reason |
|---|---|---|
| Simple spectrum from bilateral algebra | 21A | Degenerate H₅=I₅ satisfies all constraints |
| Linear independence from block structure | 21C | Module map ill-defined (32/36 products escape 5D) |
| Full 6-root algebraic closure | 23T1 | Diverges exponentially (6→878+ in 3 iterations) |
| Weil identity (non-windowed f₅D) | 23T3 | Formally diverges; direction correct, window needed |
| Chavez on sorted pairwise inner products | 22 | Null — sorted pairwise ≠ sequential GUE structure |
| Route C (GUE universality) | 16 | Eliminated — χ₃/χ₄/ζ have different prime content |

---

## Key File Inventory

| File | What to reuse |
|---|---|
| `rh_phase20b.py` | f5D embedding — canonical reference |
| `rh_phase21b.py` | cd_mul, cd_conj — sedenion multiplication |
| `rh_phase23_thread3.py` | S(N), RHS_dir, residual computation (reuse directly) |
| `rh_phase23_thread1_minimal.py` | 12-vector closure code |
| `rh_phase22.py` | gram_G5, P5 projection, safe() JSON helper |
| `phase23_thread1_results.json` | 12-vector closure vectors (exact positions) |
| `phase23_thread3_results.json` | S(N) partial sums, residual ratios, cailculator_sequences |
| `rh_zeros.json` | First 500 zeros (cached, dps=25) — use if available; otherwise re-fetch via mpmath |

---

## Broader Context

- **Researcher:** Paul Chavez, Chavez AI Labs LLC
- **CAILculator MCP** — available in Claude Desktop only. Scripts prepare `cailculator_sequences` for MCP handoff.
- **Chavez conjugation symmetry formula:** `1 − mean(|x[i]−x[n−1−i]|)` for i in range(n//2), on sequence normalized to [0,1]
- **Investigation records (Phase 23):** Residual ratio 98.7% (unwindowed), P(N)/N convergence 97.8%, bilateral triple 94.4% / 95% bilateral confidence
- **The open gap:** Simple spectrum + linear independence of {tₙ·log p} over ℚ. Both algebraically undefeatable. Analytic route (windowed Weil) is the primary remaining path.
- **Paper target:** April 1, 2026 — Sophie Germain's 250th birthday. Phase 20A (consolidation) still queued.
- Null results are as valued as positive ones. Each closed avenue tightens the characterization.

---

## What Success Looks Like

**Thread 1 (strong):** Residual ratio shrinks toward zero as T → ∞. Weil identity confirmed in windowed sense. AIEX-001 connects to a proven theorem. *This would be the investigation's most significant analytic result.*

**Thread 1 (partial):** Residual ratio decreases with T but extrapolation to T→∞ gives c > 0. Provides decay rate and a lower bound on the structural offset.

**Thread 1 (null):** Residual ratio stays ~12% regardless of T (98.7% symmetry maintained). The 6.8° offset between the AIEX-001 partial sum and the Weil RHS is structural — a new geometric characterization of the embedding.

**Thread 2 (strong):** L_q3 maps closure to itself; [H₅, L_q3]=0 reduces the unconstrained eigenspace below Phase 21A's 4-dimensional residual. Simple spectrum becomes derivable (or more constrained) from within the 12-vector module.

**Thread 2 (null):** L_q3 escapes the 12-vector closure. The bilateral triple finite algebra doesn't constrain H₅. Close definitively; document which products escape and why. The investigation proceeds exclusively via analytic methods.

---

*Phase 24 Handoff prepared March 25, 2026*
*Chavez AI Labs LLC · Applied Pathological Mathematics · "Better math, less suffering"*
