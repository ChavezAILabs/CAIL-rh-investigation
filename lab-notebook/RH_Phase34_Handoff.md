# Phase 34 Handoff — Claude Code

**Chavez AI Labs LLC** · *Applied Pathological Mathematics — Better math, less suffering*

|                     |                                                              |
|---------------------|--------------------------------------------------------------|
| **Date**            | 2026-03-27                                                   |
| **Author**          | Paul Chavez / Chavez AI Labs LLC                             |
| **Receiving agent** | Claude Code (pure Python computation)                        |
| **Previous phase**  | Phase 33 — Weil Ratio Double-Dependence Characterization     |
| **GitHub**          | https://github.com/ChavezAILabs/CAIL-rh-investigation        |
| **Zenodo**          | https://doi.org/10.5281/zenodo.17402495                      |
| **KSJ entries**     | 121 total (AIEX-001 through AIEX-120)                        |

---

## 1. What Phase 33 Established

Phase 33 characterized the full double dependence of the Weil ratio on N_primes and N_zeros, mapping the (N_primes, N_zeros) surface and locating c₁ on it.

### 1.1 Power-Law Decay in N_zeros

The Weil ratio decays as a power law in N_zeros across all prime sets tested (R²≈0.999):

```
ratio ≈ a(N_p) · N_zeros^(−b(N_p))
```

Decay exponent b **decreases with N_primes** — larger prime sets converge more slowly as N_zeros grows:

| Prime set | a     | b     | Best R²  |
|-----------|-------|-------|----------|
| 6 primes  | 0.648 | 0.211 | 0.9985   |
| 36 primes | —     | 0.147 | 0.9981   |
| 62 primes | 0.247 | 0.120 | 0.9989   |

### 1.2 The c₁ Level Curve

c₁ = 0.11798 is **not** a fixed prime threshold — it locates a diagonal level curve on the (N_primes, N_zeros) surface running from upper-right to lower-left in (log N_primes, log N_zeros) space:

| N_zeros | Crossing p_max | Crossing N_primes |
|---------|---------------|-------------------|
| 100     | > 400         | > 78              |
| 500     | ≈ 306         | ≈ 62–63           |
| 1000    | < 199         | < 46              |

Exact crossing at N_zeros=500: **p_max = 306.06**, when p=307 enters the prime set.

### 1.3 The Remarkable c₁ Asymptote (AIEX-116 — Unconfirmed)

**The most important Phase 33 finding, requiring Phase 34 verification:**

The 1/√N_zeros model for the **6-prime set** gives a finite asymptote:

```
c∞ = 0.1197  ≈  c₁ = 0.11798   (difference: 0.0017)
```

If exact, this means: **lim_{N_zeros→∞} ratio(6 primes, N_zeros) = c₁ = sin(θ_W)**

This is currently fit only to N_zeros ≤ 1000. Phase 34 must test whether the asymptote holds at much larger N_zeros. This is the primary goal.

### 1.4 Verified Baselines (do not recompute)

| N_zeros | N_primes | Ratio (verified) |
|---------|----------|-----------------|
| 100     | 6        | 0.247931        |
| 500     | 6        | 0.173349        |
| 500     | 36       | 0.136356        |
| 500     | 62       | 0.118099 ≈ c₁   |
| 500     | 168      | 0.082508        |

---

## 2. Open Questions Entering Phase 34

Live KSJ open questions, ordered by relevance to Phase 34 tasks.

| # | Question | Track | AIEX ref |
|---|----------|-------|----------|
| 1 | Is c∞(6 primes) = c₁ exact or coincidental? Needs N_zeros > 1000 verification and analytic derivation from 6-prime Euler product. | **Primary** | AIEX-116 |
| 2 | Does b(N_p) follow a known prime-density law (e.g. b ∝ 1/log(N_p))? If so, full surface has closed form. | **Primary** | AIEX-118 |
| 3 | Can the N_zeros power-law decay be derived from Weyl equidistribution of {log p mod 2π}? Exponent b should be expressible in terms of the prime set discrepancy. | **Primary** | AIEX-118 |
| 4 | Does p=307 have any special role in the sedenion/E8/bilateral structure, or is it incidental at the N_zeros=500 threshold? | Secondary | AIEX-120 |
| 5 | What governs 64D ZDTP class assignment (I→I→II→II→III→III→II)? Slot index mod 4 or mod 8? Extend to p=29, 31, 37. | CAILculator | AIEX-103 |
| 6 | Does bilateral annihilation P·Q=0 provide a self-adjointness argument for AIEX-001? (Phase 19 Thread 3 — operator construction) | Phase 35 setup | AIEX-051 |
| 7 | N_zeros-dependence analytic form: is there a series convergence theorem that explains the power-law rate? | Phase 35 setup | AIEX-111 |

---

## 3. Phase 34 Task Specification for Claude Code

**Phase 34 has two missions:**
1. **Confirm or refute the c₁ asymptote hypothesis** (AIEX-116) — the most consequential open question in the investigation
2. **Fit the full 2D surface analytically** (AIEX-118) — characterize a(N_p) and b(N_p) as functions of N_p, setting up Phase 35's analytic derivation

Claude Code handles all pure Python computation and JSON output. CAILculator MCP (Claude Desktop) handles ZDTP. Do not mix.

---

> **PRIMARY** — Track E: Extended N_zeros Scan (c₁ Asymptote Test)

### Task E1: High-N_zeros scan for the 6-prime set

Extend the 6-prime ratio computation to much larger N_zeros to test whether c∞ = c₁ = 0.11798 exactly.

- Prime set: {2, 3, 5, 7, 11, 13} (6 primes, p_max=13) — fixed throughout
- Compute ratio at N_zeros ∈ {1000, 2000, 3000, 5000, 7500, 10000}
- Use all available zeros from `rh_zeros.json` (1000 zeros). For N_zeros > 1000: extend using `mpmath.zetazero(n)` for n=1001 through n=10000, dps=25
- For each N_zeros: report ratio, (ratio − c₁), and running power-law fit parameters a and b
- Report: does the fitted asymptote c∞ converge toward c₁, away from it, or remain stable at ~0.1197?
- Decision gate: if |c∞ − c₁| < 0.0005 at N_zeros=10000, flag as "strong candidate for exactness"
- Save: `phase34_c1_asymptote_test.json`

### Task E2: Asymptote test for 36-prime and 62-prime sets

The 6-prime asymptote is the headline, but check whether other prime sets also show finite asymptotes — or converge to zero.

- 36-prime set (p_max=151): compute ratio at N_zeros ∈ {1000, 2000, 5000, 10000}
- 62-prime set (p_max=300): same N_zeros values
- For each: fit power law and report extrapolated c∞
- Report: do 36-prime and 62-prime asymptotes also approach known constants, or do they approach 0?
- Save: `phase34_asymptote_comparison.json`

---

> **PRIMARY** — Track S: 2D Surface Fit

### Task S1: Characterize a(N_p) and b(N_p)

Phase 33 established that ratio ≈ a(N_p) · N_zeros^(−b(N_p)) with both a and b decreasing functions of N_p. Phase 34 must fit these functional forms.

- Use Phase 33 power-law fits as input: (N_p=6, a=0.648, b=0.211), (N_p=36, b=0.147), (N_p=62, a=0.247, b=0.120)
- Add 3 new prime sets: N_p=15 (p_max=47), N_p=95 (p_max=499), N_p=168 (p_max=1000)
- For each new prime set: compute ratio at N_zeros ∈ {100, 200, 500, 1000} and fit power law to get a and b
- Compile full table: (N_p, p_max, a, b) for all 6 prime sets
- Fit a(N_p) vs N_p: test models — power law, log decay, 1/√N_p, linear in log(N_p)
- Fit b(N_p) vs N_p: same candidate models; note that b(62)=0.120 ≈ 1/log(62)≈0.236... (likely not exact — check)
- Report: best-fit functional forms for a(N_p) and b(N_p) with R² values
- Save: `phase34_surface_parameters.json`

### Task S2: Full surface reconstruction and residuals

With fitted a(N_p) and b(N_p), reconstruct the surface and check residuals.

- Compute predicted ratio for all (N_p, N_zeros) pairs from Phase 33's 6×4 grid
- Compute residuals: predicted vs actual
- Report: max residual, mean absolute residual, any systematic pattern
- Identify: does the surface have a clean closed-form approximation, or are there corrections needed?
- Save: `phase34_surface_residuals.json`

---

> **SECONDARY** — Track B: b(N_p) Analytic Probe

### Task B1: Test the Weyl equidistribution hypothesis for b(N_p)

The decay exponent b should be expressible in terms of the discrepancy of {log p mod 2π} for the prime set if the decay follows Weyl equidistribution. This is the analytic grounding question for Phase 35.

- For each of the 6 prime sets: compute the **discrepancy** of {log p mod 2π} using the standard L² discrepancy formula
- Compute the **star discrepancy** D*_N for each set
- Test: does b correlate with D*_N, 1/D*_N, or log(D*_N)?
- Test: does b correlate with known prime-set statistics: log(p_max), π(p_max), sum of log(p)/√p (Weil_RHS magnitude)?
- Report: strongest correlation found; flag if R² > 0.95 for any single predictor
- Save: `phase34_b_predictor_analysis.json`

---

> **TERTIARY** — Track P: Phase 35 Setup — Analytic Groundwork

### Task P1: Exact value probe for c₁ in the 6-prime Euler product

This task searches for an analytic expression connecting c₁ to the 6-prime Euler product structure — the algebraic setup Phase 35 will need.

- Compute: Σ_{p∈{2,3,5,7,11,13}} log(p)/√p = |Weil_RHS| = 4.014042...
- Compute: Σ log(p)/p, Σ log(p)/p², Σ (log p)²/√p for the 6-prime set
- Compute: the 6-prime Mertens constant analogue: Π_{p≤13} (1 − 1/p)^{−1}
- Test: does c₁ = sin(arctan(Σ log(p)/√p / Σ...))? Explore all natural trigonometric combinations of these sums
- Test: is c₁ = (Σ log(p)/√p)^{−1} · (some integer or half-integer)? Or expressible as a ratio of two of these sums?
- This is exploratory — report all combinations tested and closest matches within 0.005 of c₁
- Save: `phase34_c1_euler_probe.json`

### Task P2: Weil explicit formula — 6-prime truncation error

Characterize how the 6-prime BK trace relates to the full Weil explicit formula — what fraction of the formula is captured, and does that fraction converge to c₁?

- The full Weil explicit formula: Σ_ρ h(ρ) = Σ_p Σ_k (log p / p^{k/2}) · ĥ(k log p) + (analytic terms)
- The 6-prime BK trace approximates the prime sum with k=1 and ĥ(x) = cos(t·x)
- Compute: ratio of 6-prime BK trace to 12-prime, 24-prime, 48-prime BK traces at N_zeros=500
- Does the ratio of (6-prime BK trace / full BK trace) converge to c₁²? Or to c₁?
- Save: `phase34_weil_truncation.json`

---

## 4. Constants and Formula Reference

### Core constants (do not re-derive)

| Symbol | Value | Description |
|--------|-------|-------------|
| c₁ | 0.11797805192095003 | sin(θ_W) — c₁ asymptote hypothesis for 6-prime set |
| c₃ | 0.99301620292165280 | cos(θ_W) |
| θ_W | 6.775425° | Weil angle |
| c∞(6p, Phase 33) | 0.1197 | Fitted asymptote for 6-prime set at N_zeros≤1000 — **UNCONFIRMED** |
| Weil_RHS (6p) | −4.014042 | −Σ_{p≤13} log(p)/√p — verified |

### Correct Tr_BK formula

```python
# CORRECT — verified Phases 30, 32, 33:
traces = (np.log(primes) / np.sqrt(primes)) * np.cos(gamma * np.log(primes))
Weil_RHS = -np.sum(np.log(primes) / np.sqrt(primes))
ratio = np.mean(tr_bk_values) / Weil_RHS
```

> **Run the Track V1 verification script first.** It is in `rh_phase33.py` and takes <5 seconds. If any check fails, stop and report before proceeding.

### Zero generation for N_zeros > 1000

**`rh_zeros_10k.json` already exists with all 10,000 zeros at dps=15 — no extended computation needed.**

```python
import json
with open("rh_zeros_10k.json") as f:
    zeros_10k = json.load(f)  # list of 10,000 floats
# Slice to desired N_zeros:
zeros = zeros_10k[:N_zeros]
```

The dps=15 precision is sufficient for ratio computation — verify with the V1 check that N_zeros=1000 from `rh_zeros_10k.json` gives ratio within 0.0001 of `rh_zeros.json` (dps=25) before proceeding. This is a one-line sanity check, not a blocker.

### Phase 33 power-law parameters (inputs for Track S)

| N_p | p_max | a     | b     | Source  |
|-----|-------|-------|-------|---------|
| 6   | 13    | 0.648 | 0.211 | Phase 33 |
| 36  | 151   | —     | 0.147 | Phase 33 |
| 62  | 300   | 0.247 | 0.120 | Phase 33 |

---

## 5. Required Output Files

| Filename | Track | Contents |
|----------|-------|----------|
| `phase34_formula_verification.json` | V1 | PASS/FAIL all 6 canonical checks — run first |
| `phase34_c1_asymptote_test.json` | E1 | 6-prime ratio at N_zeros={1000→10000}, fitted c∞ |
| `phase34_asymptote_comparison.json` | E2 | 36-prime and 62-prime asymptotes |
| `phase34_surface_parameters.json` | S1 | (N_p, a, b) table for 6 prime sets; fits for a(N_p), b(N_p) |
| `phase34_surface_residuals.json` | S2 | Reconstructed surface vs Phase 33 actuals |
| `phase34_b_predictor_analysis.json` | B1 | Discrepancy and prime-set statistics vs b |
| `phase34_c1_euler_probe.json` | P1 | Euler product combinations tested vs c₁ |
| `phase34_weil_truncation.json` | P2 | 6-prime trace fraction of full Weil sum |

### JSON schema

```json
{
  "phase": 34,
  "track": "E1",
  "formula": "Tr_BK = sum_p (log p / sqrt(p)) * cos(t * log p)",
  "c1": 0.11797805192095003,
  "prime_set": [2, 3, 5, 7, 11, 13],
  "points": [
    { "N_zeros": 1000, "ratio": 0.152656, "vs_c1": 0.034678, "fit_c_inf": 0.1197 },
    ...
  ],
  "final_fit": { "a": 0.648, "b": 0.211, "c_inf": 0.1197, "R2": 0.9985 }
}
```

---

## 6. Known Constraints

> **Verified working:** `numpy`, `scipy`, `mpmath` — `pip install numpy scipy mpmath`

> **Do not modify:** The Tr_BK formula. The c₁ value. The zero indexing (zetazero(1) = first non-trivial zero ≈ 14.135).

**Computation time estimates (revised — rh_zeros_10k.json pre-exists):**
- Formula verification (V1): < 5 seconds
- Tasks E1/E2 (ratio at all N_zeros up to 10,000): < 5 minutes total — zeros already computed
- Tasks S1/S2/B1 (fits and correlations): < 5 minutes
- Tasks P1/P2 (Euler product probes): < 10 minutes
- **Total estimated runtime: < 30 minutes**

**Recommended execution order:**
1. Formula verification (V1) + dps=15 sanity check — always first
2. Task E1 (6-prime asymptote test up to N_zeros=10,000) — primary goal
3. Tasks S1, S2, B1 — surface characterization
4. Tasks E2, P1, P2 — secondary and Phase 35 groundwork

---

## 7. Phase 35 Preview — What This Phase Is Building Toward

Phase 34 is computational groundwork for Phase 35, which is the **analytic derivation phase**. The goal of Phase 35 is to explain *why* the surface looks the way it does.

### Phase 35 target questions (not tasks for Phase 34)

**Q1: Can the N_zeros power-law decay be derived from Weyl equidistribution?**

The BK trace Tr_BK(t) = Σ_p (log p/√p) · cos(t log p) is a trigonometric sum over prime logarithms. As t ranges over the imaginary parts of Riemann zeros, the mean of cos(t log p) over N zeros converges to zero — this is a consequence of the equidistribution of Riemann zeros (the GUE hypothesis / Montgomery's conjecture). The rate of convergence — the power-law exponent b — should be expressible in terms of the discrepancy of the sequence {log p mod 2π} for the prime set. Phase 34 Task B1 tests this empirically; Phase 35 derives it.

**Q2: If c∞(6 primes) = c₁ exactly, what is the proof?**

The 6-prime set {2,3,5,7,11,13} is the baseline for the entire investigation. If the Weil ratio for this specific set converges to sin(θ_W) as N_zeros → ∞, there must be a reason rooted in the algebra — either the 6-prime Euler product truncation captures exactly a sin(θ_W) fraction of the full Weil sum in the equidistributed limit, or the (A₁)⁶ geometry of the Canonical Six imposes this constraint. Phase 34 Task P1 probes the Euler product structure; Phase 34 Task P2 probes the truncation fraction. Phase 35 assembles the proof attempt.

**Q3: The full 2D surface as a known special function**

If b(N_p) ∝ 1/log(N_p) and a(N_p) ∝ N_p^{−α}, the surface becomes:
```
ratio(N_p, N_z) ≈ C · N_p^{−α} · N_z^{−1/log(N_p)}
```
This is a doubly-indexed product that may be recognizable as an Euler product approximation, a Dirichlet series truncation, or a known function from analytic number theory. If it is, the investigation has a direct connection from the numerical surface to the full Weil explicit formula — which is the heart of AIEX-001a.

### Connecting back to Bender–Brody–Müller and AIEX-001a

The Weil ratio characterization (Phases 29–34) is the empirical arm of the investigation. The operator construction (Phase 19 Thread 3, the BBM comparison) is the algebraic arm. They connect at the following point: if c₁ = sin(θ_W) is the N_zeros → ∞ limit of the 6-prime embedding ratio, it means the (A₁)⁶ Canonical Six subspace captures exactly a c₁-fraction of the Weil explicit formula in the spectral limit. That fraction — sin(θ_W) — is the same constant that appears in the Weil angle geometry and the Berry-Keating Hamiltonian identification (AIEX-071). Phase 35 is where these two arms potentially meet.

---

## 8. Broader Context

### KSJ status

121 entries (AIEX-001 through AIEX-120). Standard workflow: `extract_insights` → present for approval → `commit_aiex`. Never auto-commit.

### Paper v1.4 status (April 1 deadline)

Two abstract additions required from Phase 33 (action items from KSJ):

1. **Add:** c₁ locates a level curve on the (N_primes, N_zeros) surface; crossing p_max is N_zeros-dependent
2. **Add footnote candidate:** 6-prime asymptote c∞ ≈ c₁ (Phase 33 fit, confirmation pending Phase 34)

If Phase 34 Task E1 confirms c∞ = c₁ before April 1, the footnote becomes a finding and belongs in the abstract itself.

---

*Chavez AI Labs LLC · Applied Pathological Mathematics · 2026-03-27*
*GitHub: ChavezAILabs/CAIL-rh-investigation · Zenodo: 10.5281/zenodo.17402495*
