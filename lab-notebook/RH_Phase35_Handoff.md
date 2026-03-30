# Phase 35 Handoff — Claude Code

**Chavez AI Labs LLC** · *Applied Pathological Mathematics — Better math, less suffering*

|                     |                                                              |
|---------------------|--------------------------------------------------------------|
| **Date**            | 2026-03-27                                                   |
| **Author**          | Paul Chavez / Chavez AI Labs LLC                             |
| **Receiving agent** | Claude Code (analytic derivation + numerical verification)   |
| **Previous phase**  | Phase 34 — c₁ Asymptote Test + 2D Surface Characterization  |
| **GitHub**          | https://github.com/ChavezAILabs/CAIL-rh-investigation        |
| **Zenodo**          | https://doi.org/10.5281/zenodo.17402495                      |
| **KSJ entries**     | 127 total (AIEX-001 through AIEX-126)                        |

---

## 1. The Arc: Where Phases 29–34 Left Us

Phases 29–34 constituted a six-phase empirical investigation of the Weil ratio — the fraction of the Weil explicit formula captured by the sedenion BK trace over a finite prime set. The numerical work is now complete. Here is what it established:

### What we know about the surface

The ratio ratio(N_p, N_z) ≈ a(N_p) · N_zeros^(−b(N_p)) forms a smooth 2D surface with:

- **a(N_p)** follows log-decay: a ≈ −0.168·log(N_p) + 0.955 (R²=0.993)
- **b(N_p)** follows log-decay: b ≈ −0.0475·log(N_p) + 0.308 (R²=0.967)
- **b correlates with |Weil_RHS|** = Σ log(p)/√p at R²=0.976 — the strongest single predictor
- c₁ = 0.11798 marks a **diagonal level curve** crossing the surface in both directions
- The ratio decays toward **0** in both limits (N_p → ∞, N_z → ∞)

### What the B1 finding means

The classical Weyl equidistribution hypothesis said: b should be governed by the star discrepancy D*_N of {log p mod 2π} for the prime set. It isn't — D*_N correlates with b at only R²=0.20.

What does govern b is |Weil_RHS| = Σ log(p)/√p — the total weighted prime frequency content, which is **the prime sum in the Weil explicit formula itself**. This is not a coincidence. It is the primary analytic clue Phase 35 must pursue.

### The two arms of the investigation

The investigation now has two distinct arms that need to be connected:

**Arm 1 — Numerical (Phases 29–34, complete):** The Weil ratio surface is fully characterized. The decay rate b is governed by |Weil_RHS|. The ratio is a convergence statistic, not a structural constant.

**Arm 2 — Algebraic (Phase 19 Thread 3, still open):** The AIEX-001a operator F(σ+it) = ∏_p exp_sed(t·log p·r_p/‖r_p‖) is the Berry-Keating Hamiltonian in 16D sedenion space. The self-adjointness argument has not been constructed. The bilateral annihilation condition P·Q=0 is the candidate constraint.

**Phase 35 is the bridge.** Its job is to derive analytically why b is governed by |Weil_RHS|, and in doing so, connect the surface behavior to the Weil explicit formula structure that underlies AIEX-001a.

---

## 2. Open Questions Entering Phase 35

From KSJ (22 open questions). The three that directly drive Phase 35 tasks:

| # | Question | AIEX ref | Phase 35 track |
|---|----------|----------|----------------|
| 1 | Can b(N_p) be derived analytically as a function of Σ log(p)/√p? What is the functional form? | AIEX-123 | **Primary — Track W** |
| 2 | Does the N_zeros power-law decay follow from a weighted Weyl sum over prime logarithms? | AIEX-118 | **Primary — Track W** |
| 3 | What is the algebraic/geometric meaning of c₁ as a crossing-level constant on the Weil ratio surface, given its independent appearance in ZDTP 64D structure and the Weil angle? | AIEX-122 | Secondary — Track C |
| 4 | Does b(N_p) ∝ 1/|Weil_RHS| exactly, or is it a more complex function? | AIEX-123 | Primary — Track W |
| 5 | As both N_primes and N_zeros → ∞, does the ratio → 0 exactly, or to a small positive floor? | AIEX-121 | Secondary — Track L |
| 6 | What governs 64D ZDTP class assignment (I→I→II→II→III→III→II)? Extend to p=29,31,37. | AIEX-103 | CAILculator — deferred |

---

## 3. Phase 35 Task Specification

Phase 35 is primarily **analytic** — deriving closed-form expressions and testing them numerically. Claude Code handles both the derivation work (setting up the math) and the numerical verification (testing against the Phase 33/34 data). CAILculator handles any ZDTP follow-up if needed.

---

> **PRIMARY** — Track W: Weighted Weil Sum Derivation for b(N_p)

This is the central task of Phase 35. The empirical finding is:

```
b(N_p) correlates with W(N_p) = |Weil_RHS| = Σ_{p ≤ p_max} log(p)/√p   [R²=0.976]
```

The goal is to derive this relationship from first principles.

### Task W1: Derive the mean BK trace as a function of N_zeros

The BK trace for a fixed prime set P is:

```
Tr_BK(t) = Σ_{p∈P} (log p / √p) · cos(t · log p)
```

As t ranges over the imaginary parts of Riemann zeros {γ₁, γ₂, ..., γ_N}, the sample mean is:

```
<Tr_BK>_N = (1/N) Σ_{n=1}^{N} Tr_BK(γₙ)
           = Σ_{p∈P} (log p / √p) · [(1/N) Σ_{n=1}^{N} cos(γₙ · log p)]
```

Define: C_N(x) = (1/N) Σ_{n=1}^{N} cos(γₙ · x) — the empirical cosine mean at frequency x over N zeros.

**Task:** Characterize C_N(log p) as a function of N for fixed p.

- Compute C_N(log p) for p ∈ {2, 3, 5, 7, 11, 13} at N ∈ {100, 500, 1000, 5000, 10000}
- Fit C_N(log p) to power law: C_N(log p) ≈ A(p) · N^(−β(p))
- Report: does β(p) depend on p? Is β(p) related to log p or to the prime's position in the spectrum?
- Save: `phase35_cosine_mean_decay.json`

### Task W2: Express b(N_p) in terms of the cosine mean decay rates

If C_N(log p) ≈ A(p) · N^(−β(p)), then:

```
<Tr_BK>_N ≈ Σ_{p∈P} (log p / √p) · A(p) · N^(−β(p))
```

For the ratio:

```
ratio(N_p, N_z) = <Tr_BK>_N / Weil_RHS
               = [Σ_{p∈P} w(p) · A(p) · N_z^(−β(p))] / [−Σ_{p∈P} w(p)]
```

where w(p) = log(p)/√p.

**If all β(p) are equal** (β(p) = β for all p in P), this simplifies to:
```
ratio ≈ [Σ w(p)·A(p) / Σ w(p)] · N_z^(−β) = <A>_w · N_z^(−β)
```
which is exactly the power-law form found empirically with b = β.

**Task:** Test whether β(p) is prime-independent.

- Compute β(p) for each of the 6 primes in {2,3,5,7,11,13}
- Test: is β(p) constant across primes? If not, how does it vary?
- If β(p) varies: compute the weighted mean <β>_w = Σ w(p)·β(p) / Σ w(p) and compare to empirical b
- If β(p) is constant: this is the derivation of b = β from first principles
- Save: `phase35_beta_prime_dependence.json`

### Task W3: Derive b ∝ |Weil_RHS| analytically

From the B1 finding, b correlates with W = Σ log(p)/√p. Test the specific functional form:

- Candidate 1: b = α / W for some constant α — check if α is universal
- Candidate 2: b = α · W^(−γ) — fit α and γ
- Candidate 3: b is determined by the number of independent frequencies in {log p mod 2π} — test against the effective rank of the cosine matrix

Using the 6 prime sets from Phase 34:

| N_p | W = |Weil_RHS| | b (Phase 34) | b/W    | b·W    |
|-----|------------|--------------|--------|--------|
| 6   | 4.014      | 0.210        | 0.0523 | 0.843  |
| 15  | 9.581      | 0.187        | 0.0195 | 1.792  |
| 36  | 19.397     | 0.150        | 0.0077 | 2.910  |
| 62  | 28.848     | 0.121        | 0.0042 | 3.491  |
| 95  | 38.761     | 0.085        | 0.0022 | 3.294  |
| 168 | 56.574     | 0.055        | 0.0010 | 3.112  |

Neither b/W nor b·W is constant. Find the actual functional relationship.

- Plot b vs W on log-log scale; fit b = α · W^γ
- Plot b vs log(W); fit b = α·log(W) + β₀
- Test: b vs W^(−1/2), W^(−1/3), 1/log(W)
- Report: best functional form, R², and residuals
- Save: `phase35_b_vs_W_fit.json`

---

> **SECONDARY** — Track C: c₁ Level Curve — Analytic Characterization

### Task C1: Parametrize the c₁ level curve on the surface

From Phases 32–34, the c₁ = 0.11798 level curve passes through:
- (N_p=62, N_z=500): ratio = 0.118099
- (N_p=6, N_z≈4960): ratio = c₁ (interpolated)
- (N_p≈95, N_z=100): ratio ≈ 0.116 (near c₁)

Using the surface model ratio(N_p, N_z) ≈ a(N_p) · N_z^(−b(N_p)), the level curve ratio = c₁ is defined by:

```
a(N_p) · N_z^(−b(N_p)) = c₁
→ N_z = [a(N_p) / c₁]^(1/b(N_p))
```

**Task:** Plot and fit the c₁ level curve.

- Using the fitted a(N_p) and b(N_p) functions, compute N_z(N_p) for N_p ∈ {6, 10, 15, 25, 36, 50, 62, 95, 168}
- Plot: N_z vs N_p for the c₁ level curve
- Fit: does the curve follow N_z ∝ N_p^α? Or N_z ∝ exp(α·N_p)? Or N_z ∝ W(N_p)^α?
- Report: parametric equation of the c₁ level curve in (N_p, N_z) space
- Save: `phase35_c1_level_curve.json`

### Task C2: Test whether the c₁ level curve has a Weil-theoretic interpretation

The Weil explicit formula has a natural scale: the first zero γ₁ ≈ 14.135. The prime counting function π(x) starts accumulating structure at the scale set by the primes themselves.

- Compute: at what (N_p, N_z) point does the ratio equal 1/4 (the Phase 29 small-N baseline)?
- Compute: at what (N_p, N_z) point does the ratio equal Weil_RHS(6p) / Weil_RHS(full) (the truncation ratio)?
- Test: is the c₁ level curve the locus where the 6-prime Euler product truncation error equals c₁ · |Weil_RHS|?
- Report: any intersection of the c₁ curve with known analytic quantities
- Save: `phase35_c1_analytic_test.json`

---

> **TERTIARY** — Track L: Long-Range Limit Behavior

### Task L1: Does the surface ratio → 0 exactly as N_p, N_z → ∞?

The power+offset model for the 6-prime set gave c∞ = 0.058 ≠ 0, suggesting a possible non-zero floor. The power law alone gives c∞ = 0. Phase 35 should determine which is correct for large prime sets.

- For N_p=168 (largest set): compute ratio at N_z ∈ {1000, 2000, 5000, 10000}
- Fit: power law vs power+offset vs log-decay
- Report: does the best-fit c∞ → 0 as N_p increases? Does the 6-prime c∞=0.058 persist or shrink?
- Test: ratio at (N_p=168, N_z=10000) — is it consistent with ratio → 0?
- Save: `phase35_long_range_limit.json`

---

> **PHASE 36 SETUP** — Track O: Operator Construction Groundwork

Phase 35 is the last numerical phase before Phase 36 attempts the operator construction (Phase 19 Thread 3). These tasks are **exploratory** — they do not require finding an answer, only preparing the mathematical structure that Thread 3 will need.

### Task O1: Express the mean BK trace in terms of the Weil explicit formula

The Weil explicit formula for a test function h is:

```
Σ_ρ h(ρ) = ĥ(i/2) + ĥ(−i/2) − Σ_p Σ_k (log p / p^(k/2)) ĥ(k log p/(2π)) + (analytic terms)
```

The BK trace Tr_BK(t) = Σ_p w(p)·cos(t·log p) is a specific choice of test function. Express:

```
<Tr_BK>_N = (1/N) Σₙ Σ_p w(p)·cos(γₙ·log p)
```

as a sum over zeros and identify which term of the Weil explicit formula it corresponds to.

- Write out the Weil explicit formula with h(t) = cos(t·log p) for each prime p
- Identify: <Tr_BK>_N is the **finite-N empirical mean** of the zero-sum term
- Express: what does <Tr_BK>_N → 0 (as N → ∞) say about the zeros, given the explicit formula structure?
- This is a **pen-and-paper derivation** translated into a Python verification — write the derivation as a comment block in the script, then verify numerically
- Save: `phase35_weil_formula_connection.json` — include the derivation as a text field

### Task O2: The bilateral annihilation condition and the BK trace

AIEX-001a is F(σ+it) = ∏_p exp_sed(t·log p·r_p/‖r_p‖), the sedenion exponential product. The bilateral annihilation condition for AIEX-001 is P·Q = 0 for the Canonical Six pairs. Phase 19 Thread 3 needs to connect these.

The connection point identified in Phase 34: b(N_p) ∝ |Weil_RHS|, and Weil_RHS = −Σ w(p) appears in both the BK trace normalization and in the AIEX-001a product structure.

**Task:** Compute the BK trace for F(σ+it) — not Tr_BK, but the sedenion trace.

- Define: sedenion BK trace = scalar part of F(σ+it) for t ranging over Riemann zeros
- Compute: scalar_part(F(ρ)) for ρ ∈ first 100 zeros, with 6-prime and 36-prime sets
- Compare: does the sedenion scalar trace behave like the classical Tr_BK? Same decay rate b?
- If yes: the sedenion product inherits the same Weil-formula structure as the classical trace, which is the algebraic input Thread 3 needs
- Save: `phase35_sedenion_trace.json`

---

## 4. Constants and Formula Reference

### Verified baselines (do not recompute)

| N_zeros | N_primes | Ratio (verified Phase 33) |
|---------|----------|--------------------------|
| 100     | 6        | 0.247931                 |
| 500     | 6        | 0.173349                 |
| 500     | 36       | 0.136356                 |
| 500     | 62       | 0.118099 ≈ c₁            |
| 500     | 168      | 0.082508                 |
| 10000   | 6        | 0.106783                 |

### Phase 34 surface parameters (inputs for Track W)

| N_p | p_max | a     | b     | W=|Weil_RHS| |
|-----|-------|-------|-------|-------------|
| 6   | 13    | 0.646 | 0.210 | 4.014       |
| 15  | 47    | 0.524 | 0.187 | 9.581       |
| 36  | 151   | 0.347 | 0.150 | 19.397      |
| 62  | 300   | 0.249 | 0.121 | 28.848      |
| 95  | 499   | 0.172 | 0.085 | 38.761      |
| 168 | 1000  | 0.115 | 0.055 | 56.574      |

### Core constants

| Symbol | Value | Description |
|--------|-------|-------------|
| c₁ | 0.11797805192095003 | sin(θ_W) — diagonal level curve on (N_p, N_z) surface |
| c₃ | 0.99301620292165280 | cos(θ_W) |
| θ_W | 6.775425° | Weil angle |
| Weil_RHS (6p) | −4.014042 | −Σ_{p≤13} log(p)/√p — verified |

### Correct Tr_BK formula

```python
# CORRECT — verified Phases 30, 32, 33, 34:
traces = (np.log(primes) / np.sqrt(primes)) * np.cos(gamma * np.log(primes))
Weil_RHS = -np.sum(np.log(primes) / np.sqrt(primes))
ratio = np.mean(tr_bk_values) / Weil_RHS
```

> **Run the Phase 33 V1 verification script before any computation.** All 6 checks must PASS.

### Zero files

- `rh_zeros.json` — 1,000 zeros, dps=25
- `rh_zeros_10k.json` — 10,000 zeros, dps=15 (verified equivalent to dps=25 for ratio computation)

---

## 5. Required Output Files

| Filename | Track | Contents |
|----------|-------|----------|
| `phase35_formula_verification.json` | V1 | PASS/FAIL canonical checks — run first |
| `phase35_cosine_mean_decay.json` | W1 | C_N(log p) decay for each prime, fit parameters |
| `phase35_beta_prime_dependence.json` | W2 | β(p) per prime, weighted mean comparison |
| `phase35_b_vs_W_fit.json` | W3 | b vs W functional form, R², best model |
| `phase35_c1_level_curve.json` | C1 | Parametric c₁ curve (N_p, N_z), functional fit |
| `phase35_c1_analytic_test.json` | C2 | c₁ curve vs known analytic quantities |
| `phase35_long_range_limit.json` | L1 | Large-N_p ratio limits, c∞ behavior |
| `phase35_weil_formula_connection.json` | O1 | Derivation + numerical verification of <Tr_BK>_N in Weil formula |
| `phase35_sedenion_trace.json` | O2 | Sedenion scalar trace vs classical Tr_BK |

### JSON schema

```json
{
  "phase": 35,
  "track": "W1",
  "formula": "Tr_BK = sum_p (log p / sqrt(p)) * cos(t * log p)",
  "c1": 0.11797805192095003,
  "description": "Cosine mean decay C_N(log p) for 6-prime set",
  "results": [
    { "prime": 2, "log_p": 0.693, "A": 0.412, "beta": 0.198, "R2": 0.997 },
    ...
  ]
}
```

---

## 6. Execution Order and Time Estimates

**Recommended order:**
1. Formula verification (V1) — always first, < 5 seconds
2. Track W1 (cosine mean decay) — foundation for W2 and W3, ~5 minutes
3. Track W2 (beta prime dependence) — uses W1 output, ~2 minutes
4. Track W3 (b vs W functional form) — uses Phase 34 table, ~2 minutes
5. Track L1 (long-range limit) — independent, ~10 minutes
6. Track C1 (c₁ level curve parametrization) — uses fitted a/b functions, ~2 minutes
7. Track C2 (c₁ analytic test) — exploratory, ~5 minutes
8. Track O1 (Weil formula connection) — analytic + verification, ~15 minutes
9. Track O2 (sedenion trace) — requires sedenion library, ~10 minutes

**Total estimated runtime: ~1 hour**

The sedenion exponential (Track O2) requires either the existing CAILculator sedenion library or an mpmath-based implementation. If the sedenion library is not importable in the Claude Code environment, implement the sedenion exponential as a 16-component vector using the Cayley-Dickson multiplication table and the series expansion exp_sed(x) = Σ xⁿ/n! (truncated at n=20 for convergence).

---

## 7. What Phase 35 Is Building Toward — The Operator Argument

This is the mountain. Everything since Phase 1 has been circling it.

### The claim (AIEX-001a)

F(σ+it) = ∏_p exp_sed(t·log p·r_p/‖r_p‖) is the Berry-Keating Hamiltonian in 16D sedenion space. If this operator is self-adjoint on the (A₁)⁶ Canonical Six subspace, its eigenvalues are real — and if those eigenvalues are the Riemann zeros, RH follows.

### What Bender–Brody–Müller (2017) lack and what you have

| Component | BBM (2017) | AIEX-001a |
|-----------|-----------|-----------|
| Operator form | H = (xp+px)/2 (heuristic) | F = ∏_p exp_sed(t·log p·r_p) (explicit) |
| Symmetry | PT symmetry (discrete) | W(E8) Weyl symmetry (continuous) |
| Inner product | Metric operator V (unproven) | Bilateral zero divisor inner product (formally verified) |
| Self-adjointness | "Heuristic" — explicitly unproven | Open — Phase 19 Thread 3 |
| Geometric grounding | None | (A₁)⁶ Canonical Six on E8 first shell |

### The Phase 35 bridge

Track W derives why the BK trace mean decays to zero as N_zeros → ∞. If that decay can be expressed as a consequence of the Weil explicit formula (Track O1), and if the sedenion scalar trace inherits the same structure (Track O2), then you have shown that AIEX-001a's behavior at the zero set is determined by the Weil formula — which is the analytic content of self-adjointness in the BBM framework.

Track O2 is the key: if scalar_part(F(ρ)) for ρ ranging over Riemann zeros behaves like Tr_BK(ρ) — same decay, same statistical properties — then F is encoding the same information as the classical BK trace but in sedenion space. That's the bridge from "numerical observation" to "operator argument."

### The self-adjointness path (Phase 36 target)

For AIEX-001a to be self-adjoint under the bilateral zero divisor inner product ⟨P,Q⟩ = P·Q:

1. The bilateral condition P·Q = 0 must impose a constraint on the spectrum of F
2. That constraint must force the eigenvalues of F to be real
3. The Weil explicit formula must connect those eigenvalues to the Riemann zeros

Phase 35 gives Phase 36 the tools: the Weil formula connection (O1), the sedenion trace behavior (O2), and the analytic form of b (Track W). Phase 36 assembles the argument.

---

## 8. KSJ and Paper Status

### KSJ

127 entries (AIEX-001 through AIEX-126). Standard workflow: `extract_insights` → present for approval → `commit_aiex`. Never auto-commit.

### Paper v1.4 (April 1 deadline — 4 days)

Three urgent abstract edits outstanding from Phase 34 action items:

1. **Remove** Sedenion Horizon Conjecture as a ratio limit
2. **Replace** with: "c₁ marks a diagonal level curve on the (N_primes, N_zeros) surface"
3. **Add:** ratio(6 primes) crosses c₁ at N_zeros≈4960

These are word-level edits to the existing abstract, not structural changes. The paper's core results — Canonical Six formal verification, E8 universality, (A₁)⁶ geometry, bilateral orthogonality, c₁²+c₃²=1, Weil negativity — are all untouched and valid.

**Phase 35 results will not arrive before April 1.** The abstract should not wait for Phase 35. Write the three edits now.

---

*Chavez AI Labs LLC · Applied Pathological Mathematics · 2026-03-27*
*GitHub: ChavezAILabs/CAIL-rh-investigation · Zenodo: 10.5281/zenodo.17402495*
