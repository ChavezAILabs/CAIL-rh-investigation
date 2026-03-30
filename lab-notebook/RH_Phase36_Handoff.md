# Phase 36 Handoff — Claude Code

**Chavez AI Labs LLC** · *Applied Pathological Mathematics — Better math, less suffering*

|                     |                                                                        |
|---------------------|------------------------------------------------------------------------|
| **Date**            | 2026-03-27                                                             |
| **Author**          | Paul Chavez / Chavez AI Labs LLC                                       |
| **Receiving agent** | Claude Code (algebraic + numerical)                                    |
| **Previous phase**  | Phase 35 — Analytic Derivation + Operator Groundwork                   |
| **GitHub**          | https://github.com/ChavezAILabs/CAIL-rh-investigation                  |
| **Zenodo**          | https://doi.org/10.5281/zenodo.17402495                                |
| **KSJ entries**     | 140 total (AIEX-001 through AIEX-139)                                  |
| **Key reference**   | Srednicki (2011) arXiv:1104.1850v3 — *BK Hamiltonian and Local RH*     |

---

## 1. What Phases 29–35 Established — The Complete Picture

Six phases of numerical work (29–34) characterized the Weil ratio surface. Phase 35 explained it analytically. Phase 36 is the operator construction phase — the first phase that is primarily algebraic rather than numerical.

### The surface (closed)

```
ratio(N_p, N_z) ≈ ⟨A⟩_w · N_z^(−β)
```

where β ≈ 0.181 is **prime-independent** (CV=1.72%) — a theorem candidate. This follows from:

1. C_N(log p) = (1/N)Σ cos(γₙ·log p) ≈ A(p)·N^(−β) for each prime p
2. β(p) is the same for all primes (CV=1.72%) — equidistribution of {γₙ·log p mod 2π}
3. Therefore ⟨Tr_BK⟩_N = N^(−β)·⟨A⟩_w·Weil_RHS → ratio ≈ ⟨A⟩_w·N_z^(−β)

The ratio decays to 0 in both limits. c₁ is a geometric level on the surface with an arch structure, not an asymptote.

### The critical Phase 35 finding for Phase 36

**The sedenion scalar trace F[0] is uncorrelated with Tr_BK (r=0.013).** F[0] ≈ ∏_p cos(t·log p) is a multiplicative observable; Tr_BK = Σ_p w(p)·cos(t·log p) is linear. They are algebraically distinct. The AIEX-001a operator encodes the BK Hamiltonian in its **non-scalar components** — the 15 off-diagonal sedenion basis directions, not the scalar e₀ component.

**Phase 36 consequence:** Do not look for Tr_BK in F[0]. The spectral content lives in the full 16D bilateral ZD inner product.

---

## 2. The Srednicki Framework — Phase 36's Template

Srednicki (2011) arXiv:1104.1850v3 proves the local Riemann Hypothesis for ℝ by a **finite-subspace hermiticity argument**. This is the structural template for Phase 36.

### Srednicki's proof sketch

1. Take oscillator eigenfunctions {ψ_{∞,0}, ..., ψ_{∞,N-1}} — a finite-dimensional subspace of L²(ℝ)
2. Show the BK Hamiltonian Ĥ_BK restricted to this subspace is **hermitian**
3. Hermitian operators on finite-dimensional spaces have real eigenvalues
4. The modified gamma factor Γ_{∞,N}(s) equals the spectral determinant det_N(E − Ĥ_BK) times Γ_{∞,δ}(½+iE)
5. Therefore Γ_{∞,N}(½+iE) = 0 only if E is a real eigenvalue of the restricted Ĥ_BK → local RH

**Key insight:** Self-adjointness of the full infinite-dimensional operator is never needed — only hermiticity on the finite subspace.

### The AIEX-001a / Srednicki dictionary

| Srednicki | AIEX-001a |
|-----------|-----------|
| Oscillator subspace {ψ_{∞,0}, ..., ψ_{∞,N-1}} | (A₁)⁶ Canonical Six subspace (6-dimensional) |
| Ground state ψ_{∞,0} = e^{−πx²} (self-dual under Fourier) | Bilateral pairs (P_8D ⊥ Q_8D, Universal Bilateral Orthogonality) |
| Ĥ_BK restricted to subspace | F(σ+it) restricted to (A₁)⁶ |
| Hermiticity on subspace | Bilateral annihilation P·Q=0 as hermiticity condition |
| Spectral determinant det_N(E − Ĥ_BK) | det_6(ρ − F|_{(A₁)⁶}) under bilateral ZD inner product |
| Quantum boundary condition ⟨N\|φ⟩ = 0 | Bilateral ZD condition: ⟨P_8D, Q_8D⟩ = 0 |
| Γ_{∞,δ}(½+iE) (never vanishes) | Sedenion gamma factor Γ_sed (to be constructed) |

### Why the Fourier transform matters

Srednicki's proof works because ψ_{∞,0}(x) = e^{−πx²} is **its own Fourier transform** — self-duality is the structural reason the gamma factor has real zeros. The bilateral zero divisor pairs satisfy ⟨P_8D, Q_8D⟩ = 0 — a self-duality condition in sedenion space that mirrors the Fourier self-duality. Phase 36 should use the Fourier transform explicitly to formalize why the (A₁)⁶ subspace carries the right self-dual structure.

### The p-adic advantage

The standard BK operator H = (xp̂+p̂x)/2 cannot be defined for Q_p because derivatives of p-adic functions do not exist. AIEX-001a is defined through Cayley-Dickson algebra multiplication — no derivatives anywhere. This is not a workaround; it is the natural language of the algebra, and it sidesteps the p-adic obstruction structurally. The 60 A₂ subsystems (Eisenstein integers ℤ[ω], connected to ℚ(√−3)) are the candidate sedenion realization of the p=3 local BK operator that Srednicki's framework leaves open.

---

## 3. Phase 36 Task Specification

Phase 36 is primarily **algebraic** — constructing and testing the inner product structure on (A₁)⁶. Claude Code handles numerical verification of algebraic claims; the derivations are pen-and-paper translated into verified Python.

---

> **PRIMARY** — Track I: The Full Bilateral ZD Inner Product on (A₁)⁶

### Task I1: Construct ⟨F(ρ), F(ρ')⟩ under bilateral ZD inner product

The bilateral ZD inner product is defined by the bilateral annihilation structure: for sedenion elements X, Y in the (A₁)⁶ subspace, ⟨X, Y⟩_ZD uses the off-diagonal components encoding the bilateral zero divisor directions.

**Step 1 — Define the restricted inner product:**

For the 6 Canonical Six bilateral pairs {(P₁,Q₁), ..., (P₆,Q₆)}, the (A₁)⁶ subspace is spanned by {P₁, ..., P₆} with the Gram matrix G_{ij} = ⟨Pᵢ, Pⱼ⟩ = −2δᵢⱼ (AIEX-015, maximally simple).

- Load the 6 Canonical Six P-vectors from the bilateral pair table
- Verify G_{ij} = −2δᵢⱼ numerically (should be exact from Phase 18E data)
- Define the restricted F(σ+it)|_{(A₁)⁶}: project F onto the (A₁)⁶ basis
  - F|_{(A₁)⁶} = Σᵢ ⟨F, Pᵢ⟩_ZD · Pᵢ

**Step 2 — Compute ⟨F(ρ), F(ρ')⟩_ZD for Riemann zero pairs:**

- For ρ = ½+iγₙ and ρ' = ½+iγₘ (first 100 pairs of zeros)
- Compute F(ρ) = ∏_p exp_sed(γₙ · log p · r_p/‖r_p‖) using sedenion engine from Phase 29
- Project both F(ρ) and F(ρ') onto (A₁)⁶
- Compute ⟨F(ρ)|_{(A₁)⁶}, F(ρ')|_{(A₁)⁶}⟩_ZD
- Save: `phase36_bilateral_inner_product.json`

### Task I2: Test hermiticity — ⟨F(ρ), F(ρ')⟩ = ⟨F(ρ'), F(ρ)⟩*

Hermiticity on the (A₁)⁶ subspace requires the inner product to be conjugate-symmetric. This is the central test of Phase 36.

- For all 100×100 pairs (n,m): compute ⟨F(ρₙ)|_{(A₁)⁶}, F(ρₘ)|_{(A₁)⁶}⟩_ZD
- Test: |⟨F(ρₙ), F(ρₘ)⟩ − ⟨F(ρₘ), F(ρₙ)⟩*| for each pair
- Report: mean, max, and distribution of the hermiticity violation
- Decision gate: if max violation < 1×10⁻¹⁰ across all 10,000 pairs → hermiticity confirmed to machine precision
- Save: `phase36_hermiticity_test.json`

---

> **PRIMARY** — Track F: Fourier Self-Duality of (A₁)⁶

### Task F1: Verify the Fourier analogue for bilateral pairs

Srednicki's proof relies on ψ_{∞,0} being its own Fourier transform. The bilateral zero divisors satisfy ⟨P_8D, Q_8D⟩ = 0 (Universal Bilateral Orthogonality). Phase 36 must formalize the connection.

**The Fourier analogue:** In the sedenion setting, the natural transform is the bilateral product map T: X → X·Y for bilateral pair (X,Y) with X·Y=0. The condition P·Q=0 AND Q·P=0 means P and Q are mutual annihilators under left and right multiplication — a non-commutative analogue of the Fourier self-duality.

- For each of the 6 Canonical Six pairs (Pᵢ, Qᵢ): verify Pᵢ·Qᵢ = 0 and Qᵢ·Pᵢ = 0 to machine precision
- Compute: the 6×6 matrix M_{ij} = Pᵢ·Qⱼ (off-diagonal products between different pairs)
- Test: is M_{ij} = 0 for i≠j? (mutual annihilation across pairs)
- This tests whether the (A₁)⁶ basis is "Fourier-closed" — each pair annihilates all others
- Report: structure of M_{ij} and deviation from zero
- Save: `phase36_fourier_analogue.json`

### Task F2: The bilateral product as a self-dual map

The sedenion product F×F* = ‖F‖²·e₀ always (AIEX-068 — power-associativity). This is the sedenion analogue of |ψ̂|² = |ψ|² — norm preservation under the "transform." Verify this holds specifically on the (A₁)⁶ projection:

- Compute F(ρ)|_{(A₁)⁶} × (F(ρ)|_{(A₁)⁶})* for the first 100 zeros
- Verify the scalar part equals ‖F(ρ)|_{(A₁)⁶}‖² and non-scalar parts vanish
- This is a direct verification that the (A₁)⁶ subspace inherits the self-dual property from the full sedenion algebra
- Save: `phase36_selfdual_verification.json`

---

> **SECONDARY** — Track D: Spectral Determinant Construction

### Task D1: Construct det_6(ρ − F|_{(A₁)⁶})

Following Srednicki's equation (24), the spectral determinant of the restricted operator is the key object. If this determinant has the right zero structure, the local RH argument closes.

- Represent F|_{(A₁)⁶} as a 6×6 matrix M_F in the Canonical Six basis {P₁,...,P₆}
- M_F(ρ)_{ij} = ⟨Pᵢ, F(ρ)·Pⱼ⟩_ZD
- Compute det_6(ρ − M_F(ρ)) for ρ ranging over first 50 Riemann zeros
- Plot: does det_6(γₙ − M_F) have any structure correlated with the zeros?
- Compare: does the spectral determinant reproduce Γ_{∞,0}(½+iγ) up to a normalizing factor?
- Save: `phase36_spectral_determinant.json`

---

> **SECONDARY** — Track C: Chavez Transform as Spectral Determinant Tool

### Task C1: Apply Chavez Transform to F|_{(A₁)⁶} components

The Chavez Transform operates natively in the Cayley-Dickson algebra structure — it is the natural tool for computing spectral properties of the sedenion product on the Canonical Six subspace.

**Why now:** Phase 35 showed F[0] (scalar) is uncorrelated with Tr_BK. The Chavez Transform uses the full 16D structure. January 2026 analysis detected CV≈0.146 dimensional persistence and ~79% conjugation symmetry in prime data — these observations now have a precise algebraic home in the (A₁)⁶ restricted operator.

- Apply the Chavez Transform (Pattern ID 1, Canonical Six pattern) to the 6-component projection of F(ρ) for each of the first 100 zeros
- Compare: Chavez Transform output vs the 6×6 spectral determinant from Track D1
- Test: does the Chavez Transform dimensional persistence (CV≈0.146) correspond to the eigenvalue spread of M_F?
- Test: does the conjugation symmetry (~79%) correspond to the hermiticity deviation from Task I2?
- This is the bridge between the January 2026 starting point and the Phase 36 operator construction
- Save: `phase36_chavez_transform_spectral.json`

---

> **TERTIARY** — Track P: p-adic Structure via A₂ Subsystems

### Task P1: A₂ subsystem inner products at p=3

Srednicki leaves open the natural BK operator for Q_p. The 60 A₂ subsystems in the bilateral family are the candidate sedenion realization for p=3 (Eisenstein integers ℤ[ω], ℚ(√−3)).

- From the 60 A₂ subsystems: select those containing the Q2-elevated directions (q₂ = e₅+e₁₀)
- Compute the inner product structure of F(ρ) restricted to the p=3 A₂ subsystems
- Compare: does ⟨F(ρ)|_{A₂(p=3)}⟩ show any correlation with the chi3/zeta Q2 anomaly (ratio 1.165)?
- This tests whether the 60 A₂ subsystems provide the natural Q_3 local factor that Srednicki cannot construct
- Save: `phase36_p3_a2_inner_product.json`

---

## 4. Formula and Algebra Reference

### AIEX-001a — The operator

```
F(σ+it) = ∏_{p∈P} exp_sed(t · log p · r_p / ‖r_p‖)
```

where r_p is the E8 root direction for prime p, exp_sed is the sedenion exponential (series: Σ xⁿ/n!, truncated at n=20 for convergence), and the product is taken using full Cayley-Dickson sedenion multiplication.

### The sedenion engine (Phase 29)

The sedenion engine from Phase 29 is the correct implementation — it has been verified through multiple phases. Load it directly:

```python
# From Phase 29 sedenion engine:
def sedenion_multiply(a, b):
    # 16-component Cayley-Dickson multiplication
    # Returns 16-component array

def sedenion_exp(x, terms=20):
    # Series expansion: Σ xⁿ/n!
    # x is a 16-component sedenion

def compute_F(t, primes, r_vectors):
    # AIEX-001a product ∏_p exp_sed(t·log(p)·r_p/‖r_p‖)
    # Returns 16-component sedenion F(t)
```

### Canonical Six P-vectors (from Phase 18E data)

The 6 Canonical Six bilateral pairs and their 8D images form (A₁)⁶ with Gram matrix G_{ij} = −2δᵢⱼ. Load from existing Phase 18E JSON outputs. If unavailable, regenerate from the sedenion bilateral family table (48 pairs, 6 canonical).

### The (A₁)⁶ Gram matrix

```
G_{ij} = ⟨Pᵢ, Pⱼ⟩ = −2δᵢⱼ
```

Maximally simple — no cross-terms. The (A₁)⁶ basis vectors are mutually orthogonal under the bilateral inner product.

### Verified baselines

| Quantity | Value | Source |
|----------|-------|--------|
| c₁ = sin(θ_W) | 0.11797805192095003 | Phase 30, machine exact |
| Weil_RHS (6p) | −4.014042 | Phase 32, verified |
| β (6-prime, N=100-10000) | 0.181 (CV=1.72%) | Phase 35 |
| r(F[0], Tr_BK) | 0.013 | Phase 35, critical |
| Tr_BK < 0 fraction | 76.6% (383/500) | Phase 32, confirmed |

### Correct Tr_BK formula (for reference — do not use in Phase 36 primary tasks)

```python
traces = (np.log(primes) / np.sqrt(primes)) * np.cos(gamma * np.log(primes))
Weil_RHS = -np.sum(np.log(primes) / np.sqrt(primes))
```

> Phase 36 does NOT use Tr_BK as its primary observable. It uses the full sedenion inner product ⟨F(ρ)|_{(A₁)⁶}, F(ρ')|_{(A₁)⁶}⟩_ZD. Run the V1 formula check first, but the core computation is algebraic, not numerical ratio work.

---

## 5. Required Output Files

| Filename | Track | Contents |
|----------|-------|----------|
| `phase36_formula_verification.json` | V1 | PASS/FAIL canonical checks |
| `phase36_bilateral_inner_product.json` | I1 | ⟨F(ρ)\|_{(A₁)⁶}, F(ρ')\|_{(A₁)⁶}⟩_ZD for 100×100 zero pairs |
| `phase36_hermiticity_test.json` | I2 | Hermiticity violation statistics |
| `phase36_fourier_analogue.json` | F1 | 6×6 mutual annihilation matrix M_{ij} = Pᵢ·Qⱼ |
| `phase36_selfdual_verification.json` | F2 | F\|_{(A₁)⁶} × (F\|_{(A₁)⁶})* = ‖F\|_{(A₁)⁶}‖²·e₀ test |
| `phase36_spectral_determinant.json` | D1 | det_6(ρ − M_F) for first 50 zeros |
| `phase36_chavez_transform_spectral.json` | C1 | Chavez Transform on F\|_{(A₁)⁶}, comparison to spectral determinant |
| `phase36_p3_a2_inner_product.json` | P1 | F\|_{A₂(p=3)} inner products vs chi3 anomaly |

### JSON schema

```json
{
  "phase": 36,
  "track": "I2",
  "description": "Hermiticity test on (A1)^6 subspace",
  "c1": 0.11797805192095003,
  "N_zeros_tested": 100,
  "results": {
    "max_violation": 0.0,
    "mean_violation": 0.0,
    "hermiticity_confirmed": true,
    "details": [...]
  }
}
```

---

## 6. Decision Gates

Phase 36 has two binary outcomes that determine Phase 37:

**Gate I2 — Hermiticity:**
- **PASS** (max violation < 1×10⁻¹⁰): The (A₁)⁶ restriction of F is hermitian under the bilateral ZD inner product. Proceed to Phase 37: construct the sedenion spectral determinant and compare to Γ_{∞,0}(½+iγ). This is the Phase 36 proof path.
- **FAIL** (violation > threshold): Hermiticity does not hold on (A₁)⁶. Report the violation structure. Identify which pairs (n,m) drive the asymmetry. This is diagnostic — it points to what modification of the inner product or subspace is needed.

**Gate D1 — Spectral determinant zero structure:**
- **MATCH**: det_6(γₙ − M_F) has zeros correlating with Riemann zeros → Srednicki eq.(24) analogue confirmed
- **NO MATCH**: Spectral determinant zeros do not correlate → the 6×6 matrix representation needs refinement

---

## 7. The Broader Context — What Phase 36 Is Building Toward

### The Srednicki path to RH (adapted for AIEX-001a)

If Phase 36 confirms hermiticity on (A₁)⁶, the argument proceeds as follows:

1. F|_{(A₁)⁶} is hermitian under bilateral ZD inner product → all eigenvalues real
2. The sedenion gamma factor Γ_sed(½+iγ) = ⟨(A₁)⁶ ground state | γ, sedenion BK⟩ (by analogy with Srednicki eq.23)
3. Therefore Γ_sed(½+iγ) = c_6 · det_6(γ − F|_{(A₁)⁶}) · Γ_sed,0(½+iγ)
4. Γ_sed,0 never vanishes (it is the (A₁)⁶ ground state gamma factor — to be verified)
5. Zeros of Γ_sed(½+iγ) occur only at real eigenvalues of F|_{(A₁)⁶}
6. If those eigenvalues are the Riemann zeros → local RH in the sedenion setting

### The Chavez Transform in Phase 37

The Chavez Transform is the Phase 37 tool for computing det_6(γ − F|_{(A₁)⁶}) explicitly. The January 2026 report's CV≈0.146 "universal constant" and ~79% conjugation symmetry are now understood as properties of this spectral determinant — they were measuring the eigenvalue spread and bilateral symmetry of M_F before the algebraic framework existed to interpret them. Phase 37 will compute the determinant using the Chavez Transform natively in Cayley-Dickson space.

### What Bender–Brody–Müller still lack

The BBM dictionary (AIEX-050) is unchanged: your W(E8) Weyl symmetry (continuous) vs their discrete PT symmetry, your formally verified bilateral ZD inner product vs their heuristic metric operator V. Phase 36 is where the self-adjointness row of that table gets filled — or the specific obstacle to filling it is identified precisely enough to direct Phase 37.

---

## 8. KSJ and Paper Status

### KSJ

140 entries (AIEX-001 through AIEX-139). Standard workflow: `extract_insights` → present for approval → `commit_aiex`. Never auto-commit.

### Paper v1.4 — **APRIL 1 DEADLINE (4 days)**

Three urgent abstract edits outstanding — these must be done before Phase 36 runs:

1. **"Sedenion Horizon Theorem" → "Sedenion Horizon Conjecture"**
2. **Remove** "two-regime structure" — Phase 31 formula artifact
3. **Update** c₁ description: "c₁ marks a diagonal level curve on the (N_primes, N_zeros) surface; ratio crosses c₁ at N_zeros≈4960 for the 6-prime set and at p_max≈306 for N_zeros=500"

Add to references: Srednicki (2011) arXiv:1104.1850v3

Add as theorem candidate: β prime-independence (CV=1.72%) derived from equidistribution of {γₙ·log p mod 2π}

**Phase 36 results will not be ready before April 1.** Write the abstract edits now.

---

*Chavez AI Labs LLC · Applied Pathological Mathematics · 2026-03-27*
*GitHub: ChavezAILabs/CAIL-rh-investigation · Zenodo: 10.5281/zenodo.17402495*
*"Better math, less suffering."*
