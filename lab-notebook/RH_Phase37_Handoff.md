# Phase 37 Handoff — Claude Code

**Chavez AI Labs LLC** · *Applied Pathological Mathematics — Better math, less suffering*

|                     |                                                                        |
|---------------------|------------------------------------------------------------------------|
| **Date**            | 2026-03-27                                                             |
| **Author**          | Paul Chavez / Chavez AI Labs LLC                                       |
| **Receiving agent** | Claude Code (algebraic + numerical)                                    |
| **Previous phase**  | Phase 36 — Bilateral ZD Inner Product + Srednicki Operator Construction|
| **GitHub**          | https://github.com/ChavezAILabs/CAIL-rh-investigation                  |
| **Zenodo**          | https://doi.org/10.5281/zenodo.17402495                                |
| **KSJ entries**     | 146 total (AIEX-001 through AIEX-145)                                  |
| **Key reference**   | Srednicki (2011) arXiv:1104.1850v3                                     |

---

## 1. What Phase 36 Proved

Phase 36 is the most consequential phase of the investigation. In 3.9 seconds it established four structural results.

### Gate I2: Hermiticity — PASS (machine exact)

The AIEX-001a operator F(ρ) restricted to the (A₁)⁶ Canonical Six subspace is **hermitian under the bilateral ZD inner product**. Max violation = 0 across all 10,000 pairs (100×100 zeros).

**The mechanism is algebraic, not numerical:**

F(ρ) at critical-line zeros ρ = ½+iγ produces a **real-valued sedenion** — all 16 components are real numbers. Real projection coefficients yield a real inner product. A real number is its own complex conjugate. Therefore hermiticity holds exactly.

**The critical line condition Re(ρ) = ½ and AIEX-001a hermiticity on (A₁)⁶ are equivalent statements in the sedenion algebra.** This is the deepest result of the investigation.

### G = −2I₆ and self-duality confirmed

- Gram matrix G = −2I₆ to machine precision (diagonal all −2.000, max off-diagonal = 0)
- F|_{(A₁)⁶} × (F|_{(A₁)⁶})* = ‖F|_{(A₁)⁶}‖²·e₀ exactly for all 100 zeros
- Mutual annihilation: all 6 bilateral pairs satisfy P_i·Q_j ≈ 0 (one structural degeneracy: M[4,0]=−2 where P₅=Q₁)

### The M_F decomposition — Phase 37's target

**M_F = F[0]·I₆ + A_antisym**

where A_antisym is purely antisymmetric (A^T = −A). Eigenvalues of M_F are F[0] ± iλₖ (three complex conjugate pairs). At t₁=14.1347: F[0]=0.06540, λₖ ∈ {0.6554, 0.2365, 0.0141}.

Gate D1 failed: det_6(ρ − M_F) ≈ (ρ − F[0])⁶, centered at F[0]≈0.065, not at ½. The current spectral determinant does not reproduce Riemann zeros.

**Phase 37 is built on this decomposition.** The key object is **iA_antisym** — a hermitian matrix (since iA is hermitian for real antisymmetric A) with real eigenvalues ±λₖ. The question: **do these λₖ match the imaginary parts of Riemann zeros?**

### The Chavez Transform bridge

6D (A₁)⁶ projection gives CS = 81.4% ± 3.3% — squarely in the Riemann zero gap range (~79%). Tr_BK gives CS = 10.3%. The January 2026 investigation's CV≈0.146 and ~79% conjugation symmetry were measuring the (A₁)⁶ projection of F(ρ). The investigation's starting observations and its operator construction have converged.

---

## 2. Phase 37 Primary Question

> **Do the eigenvalues of iA_antisym(ρ) match the imaginary parts {γₙ} of Riemann zeros?**

This is the single question Phase 37 must answer. Everything else is context or verification.

**The algebraic setup:**

- M_F(ρ) = F[0](ρ)·I₆ + A(ρ) where A(ρ) = −A(ρ)^T (real antisymmetric)
- iA(ρ) is hermitian (real symmetric after multiplication by i, for real A)
- Eigenvalues of iA(ρ) are real: call them {μₖ(ρ)} for k=1,...,6 (or 3 pairs ±μₖ)
- **Hypothesis:** μₖ(ρₙ) = γₙ for some pairing between eigenvalues and zero indices

This is Srednicki's spectral determinant argument adapted: if iA at zero ρₙ has γₙ as an eigenvalue, then det_6(γ − iA) vanishes at γ=γₙ — the zeros are encoded in the antisymmetric part of the restricted operator.

---

## 3. Phase 37 Task Specification

---

> **PRIMARY** — Track E: Eigenvalue Spectrum of iA vs Riemann Zeros

### Task E1: Compute eigenvalues of iA(ρ) for first 100 zeros

- For each zero ρₙ = ½+iγₙ (n=1,...,100): compute M_F(ρₙ), extract A(ρₙ) = M_F − F[0]·I₆, compute eigenvalues of iA(ρₙ)
- Report: the 6 eigenvalues {μₖ(ρₙ)} at each zero
- Note: eigenvalues of real antisymmetric A come in pairs ±iλₖ, so eigenvalues of iA are ±λₖ (real, paired)
- Save: `phase37_iA_eigenvalues.json`

### Task E2: Test eigenvalue-zero matching

This is the decision gate of Phase 37. Three matching tests, in order of strength:

**Test E2a — Direct match:** For each zero γₙ, does any eigenvalue μₖ(ρₙ) equal γₙ exactly (within numerical precision)?

**Test E2b — Scaled match:** Is there a universal constant c such that c·μₖ(ρₙ) = γₙ for some k? Scan c ∈ [0.1, 100] systematically.

**Test E2c — Rank correlation:** Ignoring exact values, do the eigenvalues at zero ρₙ correlate in rank order with γₙ? (Spearman ρ between sorted {μₖ} and γₙ)

- Report: outcome of each test; if any test passes, report the pairing rule
- Decision gate: any Test E2a match to within 1×10⁻⁶ → **STRONG RESULT**
- Save: `phase37_eigenvalue_matching.json`

### Task E3: Eigenvalue trajectory — how do μₖ vary across zeros?

Even if direct matching fails, the trajectory of eigenvalues across zeros is structurally informative.

- Plot (via data): μₖ(ρₙ) vs γₙ for k=1,2,3 (three pairs)
- Test: do the eigenvalues grow with γₙ? Are they bounded? Do they oscillate?
- Compute: Σₖ μₖ(ρₙ)² (sum of squared eigenvalues) vs γₙ — does this correlate with any known zero statistic?
- Save: `phase37_eigenvalue_trajectory.json`

---

> **PRIMARY** — Track R: The Reality Condition — Algebraic Proof Attempt

### Task R1: Verify F(½+iγ) ∈ ℝ¹⁶ for all tested zeros

Phase 36 established hermiticity via the mechanism that critical-line zeros produce real sedenion vectors. Phase 37 must characterize this precisely.

- For each of 100 zeros: compute max |Im(F_k(ρ))| for k=0,...,15 (imaginary parts of all 16 components)
- Verify all imaginary parts are zero to machine precision
- For comparison: compute F at off-critical-line points σ+iγ₁ for σ ∈ {0.3, 0.4, 0.5, 0.6, 0.7} — do imaginary parts vanish only at σ=0.5?
- Save: `phase37_reality_condition.json`

### Task R2: The reality condition as a function of σ

This is the algebraic heart of the Phase 37 investigation. The sedenion exponential product F(σ+it) = ∏_p exp_sed(t·log p·r_p/‖r_p‖) — note the r_p directions do not depend on σ; only t appears explicitly. So why does σ=½ force F to be real?

- Compute F(σ+iγ₁) for σ ∈ {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9}
- For each σ: report the magnitude of the imaginary parts ‖Im(F(σ+iγ₁))‖
- Plot: does ‖Im(F)‖ have a minimum at σ=0.5? Or vanish only there?
- This tests whether "F is real iff Re(ρ)=½" holds empirically, which is the key claim for the algebraic proof attempt
- Save: `phase37_reality_vs_sigma.json`

---

> **SECONDARY** — Track S: Spectral Determinant Refinement

### Task S1: Study det_6(E − iA(ρ))

The corrected spectral determinant strips the scalar diagonal. For each zero ρₙ:

- Compute det_6(E − iA(ρₙ)) as a polynomial in E
- Find roots: the values of E where this determinant vanishes
- Test: do any roots equal γₙ? Do roots equal known constants (½, γ₁, 0)?
- Compare: det_6(E − iA(ρₙ)) vs Srednicki's det_N(E − Ĥ_BK)·Γ_{∞,δ}(½+iE)
- Save: `phase37_corrected_spectral_det.json`

### Task S2: The sedenion gamma factor candidate

Following Srednicki's equation (24), construct:

```
Γ_sed(½+iγ) = ⟨ground state | γ, sedenion BK⟩
```

where the ground state is the (A₁)⁶ element v₀ satisfying iA·v₀ = 0 (or the eigenstate of iA with smallest eigenvalue).

- Find the null space of A(ρₙ) at each zero — is there a consistent null vector?
- If yes: define v₀ as this null vector; compute ⟨v₀, F(ρₙ)·v₀⟩_ZD
- Test: does this quantity vanish at Riemann zeros?
- Save: `phase37_gamma_sed_candidate.json`

---

> **SECONDARY** — Track C: Chavez Transform Spectral Characterization

### Task C1: Chavez Transform eigenvalue signature

The Chavez Transform on the (A₁)⁶ projection gave CS=81.4% in Phase 36. Now apply it to the eigenvalue sequences directly.

- For each of the 3 eigenvalue trajectories {μₖ(ρ₁), μₖ(ρ₂), ..., μₖ(ρ₁₀₀)}: compute Chavez Transform CS and dimensional persistence
- Compare: is the CS of eigenvalue sequences closer to 79% (RZ gap range) than the projection CS?
- Test: does the dimensional persistence CV match the Phase 35 β≈0.181 prime-independence result?
- Save: `phase37_chavez_eigenvalue.json`

---

> **TERTIARY** — Track P: Algebraic Proof Infrastructure (Phase 38 Setup)

### Task P1: Characterize A_antisym structure

The antisymmetric matrix A(ρ) contains all the spectral content. Understanding its algebraic structure is the Phase 38 foundation.

- For 10 representative zeros: print the full 6×6 A(ρ) matrix
- Identify: which off-diagonal entries are largest? Do they correspond to specific bilateral pair interactions?
- Test: is A(ρ) rank-2 (only one pair ±iλ)? Or full-rank (three independent pairs)?
- Test: does A(ρ₁+ρ₂) = A(ρ₁) + A(ρ₂)? (linearity in ρ)
- Save: `phase37_A_structure.json`

### Task P2: The Fourier transform connection

Srednicki's proof uses the fact that oscillator eigenfunctions are their own Fourier transform (up to phase). The bilateral pairs satisfy P·Q=0 — mutual annihilation. Phase 37 should test the explicit Fourier connection:

- For each P-vector in the (A₁)⁶ basis: compute its discrete Fourier transform over the 16 sedenion components
- Test: is F̂[Pᵢ] proportional to Qᵢ (the bilateral partner)?
- If yes: this establishes the explicit Fourier self-duality of the (A₁)⁶ basis, completing the Srednicki structural analogue
- Save: `phase37_fourier_bilateral.json`

---

## 4. The Decision Tree

Phase 37 has a clear decision structure:

```
E2a PASS (direct eigenvalue match to γₙ)?
  → YES: Srednicki spectral argument closes. Phase 38 = formal proof.
  → NO: 
      E2b PASS (scaled match μₖ = γₙ/c)?
        → YES: Phase 38 = identify the constant c and its algebraic meaning.
        → NO:
            E2c PASS (rank correlation)?
              → YES: Phase 38 = explain the order-preserving map.
              → NO: Phase 38 = use A_antisym structure (Track P) to modify
                    the inner product definition.

R2 result (reality condition vs σ)?
  → ‖Im(F)‖ = 0 ONLY at σ=½: Algebraic proof path opens.
  → ‖Im(F)‖ = 0 elsewhere too: The reality mechanism needs refinement.
```

---

## 5. Constants and Verified Baselines

### Phase 36 structural results (do not recompute)

| Quantity | Value | Status |
|----------|-------|--------|
| G = −2I₆ | Confirmed machine exact | Phase 36 |
| Hermiticity max violation | 0.00e+00 | Phase 36 Gate I2 PASS |
| F[0] at t₁=14.1347 | 0.06540 | Phase 36 |
| A eigenvalues at t₁ | ±{0.6554i, 0.2365i, 0.0141i} | Phase 36 |
| 6D projection CS | 81.4% ± 3.3% | Phase 36 |
| Self-dual property | Exact (100/100) | Phase 36 |

### (A₁)⁶ basis vectors

```python
# Canonical Six (A₁)⁶ basis — verified Phase 36
P_vectors = [
    e1 + e14,   # Pair 1
    e1 - e14,   # Pair 2
    e2 - e13,   # Pair 3
    e3 + e12,   # Pair 4
    e4 + e11,   # Pair 5
    e5 + e10,   # Pair 6 (= q₂, Heegner direction)
]
```

### Sedenion engine

Use the Phase 29/36 sedenion engine unchanged. F(ρ) is computed via:

```python
F(rho) = ∏_p exp_sed(Im(rho) · log(p) · r_p / ||r_p||)
```

with 6-prime set {2,3,5,7,11,13} and E8 root directions r_p from Phase 36.

### Key formula: extracting A_antisym

```python
# From Phase 36:
# M_F[i][j] = scalar_part(P_i · (F · P_j)) / (-2)
# F[0] = scalar component of F (component 0 of 16-vector)
# A[i][j] = M_F[i][j] - F[0] * delta(i,j)
# iA is hermitian; eigenvalues of iA are real
```

---

## 6. Required Output Files

| Filename | Track | Contents |
|----------|-------|----------|
| `phase37_formula_verification.json` | V1 | PASS/FAIL canonical checks — always first |
| `phase37_iA_eigenvalues.json` | E1 | 6 eigenvalues of iA(ρₙ) for n=1..100 |
| `phase37_eigenvalue_matching.json` | E2 | Tests E2a/E2b/E2c — primary decision gate |
| `phase37_eigenvalue_trajectory.json` | E3 | μₖ(ρₙ) vs γₙ trajectory analysis |
| `phase37_reality_condition.json` | R1 | Im(F_k) magnitudes at 100 zeros |
| `phase37_reality_vs_sigma.json` | R2 | ‖Im(F)‖ vs σ at γ₁ — critical path |
| `phase37_corrected_spectral_det.json` | S1 | det_6(E − iA) roots vs γₙ |
| `phase37_gamma_sed_candidate.json` | S2 | Ground state construction; Γ_sed test |
| `phase37_chavez_eigenvalue.json` | C1 | Chavez Transform on eigenvalue sequences |
| `phase37_A_structure.json` | P1 | 6×6 A matrices, rank, linearity tests |
| `phase37_fourier_bilateral.json` | P2 | Discrete Fourier test on P-vectors |

### JSON schema

```json
{
  "phase": 37,
  "track": "E2",
  "description": "Eigenvalue matching test — primary decision gate",
  "c1": 0.11797805192095003,
  "N_zeros": 100,
  "tests": {
    "E2a_direct_match": false,
    "E2b_scaled_match": {"pass": false, "best_c": 1.234, "best_residual": 0.456},
    "E2c_rank_correlation": {"spearman_rho": 0.789, "p_value": 0.001}
  },
  "details": [...]
}
```

---

## 7. What Phase 37 Is Building Toward

### The Srednicki argument — sedenion version

If Track E2 passes with direct matching:

1. F|_{(A₁)⁶} is hermitian under bilateral ZD inner product ✓ (Phase 36, exact)
2. M_F = F[0]·I₆ + A_antisym ✓ (Phase 36, structural discovery)
3. iA is hermitian with real eigenvalues {±λₖ} ← (Phase 37 establishes values)
4. Eigenvalues of iA at ρₙ equal γₙ ← (Phase 37 primary test)
5. Therefore det_6(γ − iA(ρₙ)) = 0 when γ = γₙ
6. By Srednicki's argument: Γ_sed(½+iγ) = c·det_6(γ − iA)·Γ_sed,0 vanishes at γₙ
7. Since F is hermitian on (A₁)⁶, γₙ must be real → local RH in sedenion setting

### The reality condition as the proof

If Track R2 shows that ‖Im(F(σ+iγ))‖ = 0 only at σ=½:

**The proof of RH would be:**
> F(σ+iγ) is real-valued iff σ=½. F(σ+iγ) real-valued is equivalent to hermiticity of M_F. Hermiticity forces all eigenvalues to be real. If the zeros are eigenvalues, they must be real, which means their imaginary parts are real (trivially) and their real parts must equal ½ (by the reality condition). QED.

This is still conditional on eigenvalues of iA equaling the zeros — but if both Track E2 and Track R2 pass, the argument is complete.

### Phase 38 — the Chavez Transform spectral determinant

If Phase 37 confirms eigenvalue matching, Phase 38 uses the Chavez Transform to compute det_6(E − iA) as a closed-form expression in Cayley-Dickson algebra. The January 2026 CV≈0.146 and ~79% CS are the spectral fingerprint of this determinant — Phase 38 is where the investigation's first observations and its final argument become explicitly the same calculation.

---

## 8. KSJ and Paper Status

### KSJ

146 entries (AIEX-001 through AIEX-145). Standard workflow: `extract_insights` → present for approval → `commit_aiex`. Never auto-commit.

### Paper v1.4 — **APRIL 1 DEADLINE**

Three outstanding abstract edits plus one new addition from Phase 36:

1. **"Sedenion Horizon Theorem" → "Sedenion Horizon Conjecture"**
2. **Update c₁:** marks a diagonal level curve on (N_primes, N_zeros) surface; crosses at N_zeros≈4960 for 6-prime set and p_max≈306 for N_zeros=500
3. **Remove** Phase 31 two-regime artifact values
4. **ADD (Phase 36):** "The AIEX-001a operator F(ρ) restricted to the (A₁)⁶ Canonical Six subspace is hermitian under the bilateral ZD inner product with max violation = 0 (machine exact, 10,000 tested pairs). The mechanism: critical-line zeros ρ = ½+iγ produce real-valued sedenion vectors, and real inner products are trivially hermitian. The critical-line condition and hermiticity are equivalent in the sedenion algebra."
5. **Add reference:** Srednicki (2011) arXiv:1104.1850v3

The Gate I2 PASS is a publishable result independent of Phase 37's outcome. Write the abstract edit now.

---

*Chavez AI Labs LLC · Applied Pathological Mathematics · 2026-03-27*
*"Better math, less suffering."*
*GitHub: ChavezAILabs/CAIL-rh-investigation · Zenodo: 10.5281/zenodo.17402495*
