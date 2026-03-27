# Phase 23 Pre-Handoff — Claude Code Briefing
## RH Investigation · Chavez AI Labs LLC · March 24, 2026

**Prepared by:** Claude (claude.ai session)
**For:** Claude Code
**Status:** Ready to execute
**Priority:** Algebraic closure (Avenue 4) + GUE norm comparison + λ_min trajectory extension

---

## Investigation Context

This is Phase 23 of an open science Riemann Hypothesis investigation using the Chavez Transform, ZDTP, and the sedenion bilateral zero divisor structure (AIEX-001 framework). The full history is in the roadmap and prior phase results. This briefing covers only what Claude Code needs to execute Phase 23.

**The AIEX-001 argument in one paragraph:** A self-adjoint operator H₅ on a 5D subspace of the sedenion E8 root lattice has an equivariant embedding v(ρ) = f₅D(t) + (σ−½)·u_antisym that maps Riemann zeros to eigenvectors. Steps 1–5 of the proof are verified. Step 6 (aiex001_critical_line_forcing) requires two assumptions: simple spectrum (not derivable from algebra — Phase 21A) and strong injectivity / linear independence of {tₙ·log p} over ℚ (not derivable from algebra — Phase 21C). Phase 22 established that G5 (the 5×5 Gram matrix of zero images) is positive definite with λ_min=10.46 and condition number 4.40 — better than random controls. This rules out the "systematic collapse" failure mode for strong injectivity. Phase 23 pursues remaining open avenues.

---

## The Embedding (Use Exactly This — Phase 20B Definition)

```python
import numpy as np
from mpmath import mp, zetazero
mp.dps = 25

# 6D basis: [e2, e7, e3, e6, e4, e5]
PRIMES = [2, 3, 5, 7, 11, 13]
ROOT_DIRS = {
    2:  np.array([0,0,0,0,1,1])/np.sqrt(2),   # q4 — Block C
    3:  np.array([0,0,-1,1,0,0])/np.sqrt(2),  # q2 — Block B (Heegner)
    5:  np.array([0,0,1,1,0,0])/np.sqrt(2),   # v5 — Block B
    7:  np.array([1,-1,0,0,0,0])/np.sqrt(2),  # v1 — Block A
    11: np.array([1,1,0,0,0,0])/np.sqrt(2),   # v4 — Block A
    13: np.array([-1,1,0,0,0,0])/np.sqrt(2),  # q3 — Block A (bilateral hub)
}
U_ANTISYM = np.array([0,0,0,0,1,-1])/np.sqrt(2)  # (e4-e5)/sqrt(2)

def f5D(t):
    result = np.zeros(6)
    for p, r in ROOT_DIRS.items():
        result += (np.log(p)/np.sqrt(p)) * np.cos(t * np.log(p)) * r
    return result

def v_rho(sigma, t):
    return f5D(t) + (sigma - 0.5) * U_ANTISYM
```

**Structural facts established in prior phases:**
- v1 = −q3 → G6 has rank 5 (structural, not a defect)
- G5 = F.T @ F (5×5 after projecting out v1/q3 redundancy) is the correct PD object
- Block C is structurally rank 1 (single prime p=2)
- v2 = u_antisym — the antisymmetric direction is reserved for the functional equation
- q3 (p=13) is a bilateral hub: q3×q2=0 and q3×q4=0 in sedenion algebra

---

## Phase 23 Targets — Three Threads

---

### Thread 1: Algebraic Closure of the 6-Root Set (Avenue 4)

**The question:** The 6-prime root set {v1, v4, q3, q2, v5, q4} is NOT closed under sedenion multiplication — q2×q4 = 2×(e6−e9), which exits the set. What is the minimal set of roots closed under sedenion multiplication containing all 6 prime roots?

**Why it matters:** If the algebraic closure corresponds to a recognizable set of primes or root system, it might reveal a universal structure across all L-functions, not just the Riemann zeta function.

**Script target: `rh_phase23_thread1.py`**

Computations:

1. **Closure generation** — starting from the 6 prime roots, iteratively compute all pairwise sedenion products and add any new unit-norm vectors (normalized products) to the set. Continue until no new vectors are generated. Report the minimal closed set.

2. **Product table** — build the complete multiplication table for the 6 prime roots (36 products). Record: scalar part, vector part, norm², and whether the product is in the (A₁)⁶ root family, E8 first shell, or elsewhere.

3. **New vectors characterization** — for each vector generated in the closure but not in the original 6-root set: what is its norm? Does it lie in the 5D fixed subspace? What bilateral zero divisor pairs does it participate in? Does it correspond to a prime or prime power?

4. **Root system identification** — does the closed set form a recognizable root system (D₄, E₆, E₇, E₈, or other)? Check: is it closed under negation? Under Weyl reflections? What is its rank?

5. **Prime correspondence** — if the closure contains more than 6 directions, attempt to assign the new directions to primes p=17, 19, 23 (the next detected primes from Phase 17A). Do the new directions match the cross-block directions used in the Phase 20C 9-prime formula?

**Sedenion multiplication:** Use the Cayley-Dickson construction. The 16D representations of the 6 prime roots are:

```
v1 = e2 - e7   (positions 2,7 in 0-indexed 16D)
v4 = e2 + e7
q3 = e6 + e9
q2 = e5 + e10
v5 = e3 + e6
q4 = e3 - e12
```

Use the sedenion_mul function from Phase 21B/21C (Cayley-Dickson recursive definition).

**Expected output:** A table of closure vectors, their norms, their 5D subspace membership, and whether they correspond to recognizable mathematical objects.

---

### Thread 2: λ_min(G5) Trajectory Extension to N=500

**The question:** Does the smallest eigenvalue of G5 continue growing monotonically, or does it plateau? Does the condition number stabilize? At what rate does λ_min grow relative to N?

**From Phase 22:** λ_min grew from 0.69 (N=10) to 10.46 (N=100). Condition number stabilized around 4–5 for N≥50.

**Script target: `rh_phase23_thread2.py`**

Computations:

1. **Extended trajectory** — compute λ_min(G5) and condition number at N = 100, 150, 200, 250, 300, 400, 500. Use mpmath.zetazero for zeros n=1..500 at dps=25.

2. **Growth rate analysis** — fit λ_min(N) to candidate growth models:
   - Linear: λ_min ∝ N
   - Square root: λ_min ∝ √N (expected for random matrices by Marchenko-Pastur)
   - Logarithmic: λ_min ∝ log(N)
   Report best fit and R².

3. **Random matrix comparison** — generate 10 random control matrices at each N (uniform t-values on [14, t_N_zeros]). Compare λ_min trajectory: do zeros track random closely, exceed random, or fall below?

4. **Block trajectories** — separately track λ_min for G_A (3×3), G_B (2×2) as N grows. Which block's λ_min grows fastest? Block B (Heegner channel) vs Block A (high-pass cluster).

5. **GUE comparison for diagonal norms** — generate GUE-distributed spacings (Wigner surmise: P(s) = (π/2)s·exp(−πs²/4)) and compute ‖f₅D(tₙ)‖² from them. Apply Chavez Transform. Does the GUE control score ~73–75% (same as Riemann zeros) or ~93% (same as uniform random)? This determines whether the 73.8% norm symmetry score is a GUE signature or specific to the Riemann zeros.

**Key result to look for:** If λ_min(G5) ∝ √N (Marchenko-Pastur scaling), that would mean the zero images behave like a random matrix ensemble — consistent with GUE and supporting strong injectivity analytically. If λ_min grows faster than √N, the zeros are "more injective" than random.

---

### Thread 3: Weil Explicit Formula Vector Identity Verification

**The question:** The f₅D formula is the k=1 terms of the Weil explicit formula with a vector-valued test function. Can the Weil identity be used to derive a constraint on the zero images?

**The Weil explicit formula (k=1 terms):**
```
Σ_ρ h(Im(ρ)) ≈ −Σ_p (log p / √p) · ĥ(log p) + [archimedean terms]
```

With h(t) = f₅D(t) (vector-valued), the left side becomes Σ_n f₅D(tₙ) and the right side is the Euler product sum. The archimedean terms are constants.

**Script target: `rh_phase23_thread3.py`**

Computations:

1. **Partial sum convergence** — compute Σ_{n=1}^{N} f₅D(tₙ) for N = 10, 50, 100, 200, 500. Does this sum converge? In what direction? Compare the direction of the partial sum against each prime root direction.

2. **Euler product right-hand side** — compute the k=1..5 Euler product terms: −Σ_p Σ_{k=1}^{5} (log p / p^{k/2}) · r_p · cos(0 · k log p) [at t=0]. This is the "DC component" of the Weil formula. Compare against the partial sum direction.

3. **Residual analysis** — for each N, compute the residual vector: Σ_{n=1}^{N} f₅D(tₙ) − [Euler product approximation]. Does the residual shrink as N grows? This tests whether the vector-valued Weil identity is numerically satisfied.

4. **Per-component Weil check** — decompose the Weil identity block by block (Block A, B, C separately). Does the identity hold block by block, or does it require cross-block cancellation?

5. **Connection to positivity** — the Weil positivity criterion states: Σ_{n} h(tₙ) · h̄(tₙ) ≥ 0 for suitable test functions h if and only if RH holds. With h = f₅D (vector-valued), compute Σ_n ‖f₅D(tₙ)‖² and compare to the Weil bound. Is the positivity criterion satisfied?

**Why this matters:** If the vector-valued Weil identity is satisfied numerically (residual → 0 as N → ∞), that connects the AIEX-001 embedding to a proven theorem in analytic number theory. The positivity check is a direct test of whether the embedding is consistent with RH being true.

---

## Output Requirements

**For each thread:**
- Script: `rh_phase23_thread{1,2,3}.py`
- JSON: `phase23_thread{1,2,3}_results.json`
- MD summary: `RH_Phase23_Thread{1,2,3}_Results.md` (following standard investigation format)

**MD format standard** (match prior phases):
- Header with status, script, output
- Headline result in bold
- Numbered sections with tables
- Summary table at end
- Open questions for next phase
- Footer: date, Chavez AI Labs LLC, "Better math, less suffering"

**JSON standard:**
- Top-level keys: experiment, date, results
- All numpy types converted to Python native (float, int, bool)
- No infinity or NaN values — replace with None or string "inf"

---

## Phase 22 Results Summary (What Thread 2 and 3 Build On)

| Result | Value | Source |
|---|---|---|
| G5 eigenvalues | [10.459, 17.381, 22.843, 26.453, 46.022] | Phase 22 script |
| G5 condition number | 4.40 (zeros) vs 5.20 (random) | Phase 22 script |
| λ_min at N=10 | 0.692 | Phase 22 script |
| λ_min at N=100 | 10.459 | Phase 22 script |
| Block A cond | 1.79 (PD=True) | Phase 22 script |
| Block B cond | 1.35 (PD=True) | Phase 22 script |
| Block C rank | 1 (structural) | Phase 22 script |
| Diagonal norm Chavez (zeros) | 73.8% | Phase 22 CAILculator |
| Diagonal norm Chavez (random) | 92.9% | Phase 22 CAILculator |
| Signed inner product Chavez (zeros) | 62.6% | Phase 22 CAILculator |
| Signed inner product Chavez (random) | 63.8% | Phase 22 CAILculator |

---

## Phase 21 Closed Avenues (Do NOT Re-investigate)

| Avenue | Status | Reason |
|---|---|---|
| Simple spectrum from bilateral algebra | CLOSED | Degenerate H5 constructible — Phase 21A |
| Linear independence from block structure | CLOSED | Module map ill-defined (32/36 products escape 5D) — Phase 21C |
| q3 hub → eigenvalue coupling | CLOSED | Requires module map — Phase 21B+21C |

---

## Remaining Open Avenues (Phase 23 and Beyond)

| Avenue | Thread | Status |
|---|---|---|
| Algebraic closure of 6-root set | Thread 1 | NEW |
| λ_min trajectory + GUE comparison | Thread 2 | EXTENSION of Phase 22 |
| Weil explicit formula vector identity | Thread 3 | NEW |
| W(E8) Weyl group symmetries | Future | Not yet attempted |
| H₅ uniqueness via Euler product | Future | Not yet attempted |
| Zero-free region via Chavez/ZDTP | Future | Not yet attempted |

---

## Files Available in Investigation Directory

The following files from prior phases are available for reference:

- `rh_phase20b.py` — v(ρ) embedding definition (canonical reference)
- `rh_phase21b.py` — sedenion multiplication + bilateral zero divisor computation
- `rh_phase21c.py` — fixed-subspace closure test
- `rh_phase22.py` — G5 Gram matrix construction
- `phase22_results.json` — all sequences including cailculator_sequences
- `phase21b_results.json` — triple product identity results
- `RH_Phase22_Results.md` — full Phase 22 results

**Working directory:** `C:\dev\projects\Experiments_January_2026\Primes_2026\`

---

## Sequencing Recommendation

Run threads in this order:

1. **Thread 2 first** (λ_min extension) — straightforward extension of Phase 22, clean numerical computation, produces clear result quickly
2. **Thread 1 second** (algebraic closure) — requires sedenion multiplication but the code exists from Phase 21B; moderate complexity
3. **Thread 3 last** (Weil identity) — most exploratory, requires careful interpretation; should be informed by Thread 2 results

---

## What "Success" Looks Like for Phase 23

**Thread 1 success:** The closure produces a recognizable root system (e.g., D4, E6, or a specific 9-root set matching the primes 17, 19, 23 from Phase 20C). This would suggest the algebraic structure is selecting a universal prime set.

**Thread 2 success:** λ_min(G5) ∝ √N (Marchenko-Pastur) with zeros tracking or exceeding random. GUE-distributed spacings score ~73% on diagonal norm Chavez (same as Riemann zeros), confirming the inversion is a GUE signature. This would connect G5 positive definiteness to the GUE ensemble analytically.

**Thread 3 success:** The vector-valued Weil residual shrinks as N grows, and the positivity criterion Σ_n ‖f₅D(tₙ)‖² satisfies the Weil bound. This would connect the AIEX-001 embedding to a proven theorem.

**Null results are also valuable** — if Thread 1 finds no recognizable root system, if Thread 2 shows λ_min growing slower than √N, or if Thread 3 shows the Weil residual does not converge, these close additional avenues cleanly. The investigation goal is exhaustion of all algebraic and analytic approaches, not just positive results.

---

*Phase 23 Pre-Handoff prepared March 24, 2026*
*Chavez AI Labs LLC · Applied Pathological Mathematics · "Better math, less suffering"*
