# Phase 32 Handoff — Claude Code

**Chavez AI Labs LLC** · *Applied Pathological Mathematics — Better math, less suffering*

|                     |                                                         |
|---------------------|---------------------------------------------------------|
| **Date**            | 2026-03-27                                              |
| **Author**          | Paul Chavez / Chavez AI Labs LLC                        |
| **Receiving agent** | Claude Code (pure Python computation)                   |
| **Previous phase**  | Phase 31 — Weil Ratio Extension & ZDTP Hinge Recurrence |
| **GitHub**          | https://github.com/ChavezAILabs/CAIL-rh-investigation   |
| **Zenodo**          | https://doi.org/10.5281/zenodo.17402495                 |

## 1. What Happened in Phase 31

Phase 31 extended the Weil ratio analysis to large prime sets (p_max ∈ {200, 300, 500, 700}), verified the ZDTP 64D slot structure for primes p=13–23, confirmed c₁² + c₃² = 1 to machine precision, and discovered a fundamental two-regime structure in the Weil sum.

### 1.1 The Weil Ratio Inversion — Primary Discovery

The Phase 30 assumption of a single monotone power-law decay from ratio≈0.248 toward c₁ is wrong. At p_max ≈ 200, the ratio inverts sharply and rises above 1.0. This is the most important Phase 31 finding.

#### Full 13-point Weil ratio sequence

| **p_max** | **N primes** | **Ratio** | **Δ from 1/4** | **Weil RHS** | **Regime**  |
|-----------|--------------|-----------|----------------|--------------|-------------|
| 13        | 6            | 0.2479    | −0.0021        | —            | Regime 1    |
| 23        | 9            | 0.2466    | −0.0034        | —            | Regime 1    |
| 29        | 10           | 0.2416    | −0.0084        | —            | Regime 1    |
| 37        | 12           | 0.2344    | −0.0156        | —            | Regime 1    |
| 53        | 16           | 0.2189    | −0.0311        | —            | Regime 1    |
| 71        | 20           | 0.2106    | −0.0394        | —            | Regime 1    |
| 97        | 25           | 0.1970    | −0.0530        | —            | Regime 1    |
| 127       | 31           | 0.1833    | −0.0667        | —            | Regime 1    |
| 151       | 36           | 0.1736    | −0.0764        | —            | Regime 1    |
| 200       | 46           | 1.1132    | +0.863         | −23.272      | Regime 2 ⚡ |
| 300       | 62           | 1.0786    | +0.829         | −28.848      | Regime 2    |
| 500       | 95           | 0.9928    | +0.743         | −38.761      | Regime 2    |
| 700       | 125          | 0.9549    | +0.705         | −46.598      | Regime 2    |

> **⚡ Inversion:** At p_max=200 the ratio jumps 6.4× in a single prime-set step (0.174 → 1.113). The transition falls near the anomalously large prime gap 157→163.

### 1.2 Power-Law Model Failure

The single-model asymptote framework (y = a·x^(−b) + c) fails completely on the combined 13-point dataset. All R² values are negative; the decay exponent b hits the lower bound (0.05) in every run. The model assumes monotone decay — that assumption is violated.

| **Fixed c**  | **SSE** | **R²** | **b** | **Conclusion** |
|--------------|---------|--------|-------|----------------|
| 0.118 (c₁)   | 1.9912  | −0.062 | 0.050 | Model fails    |
| 0.140        | 1.9836  | −0.058 | 0.050 | Model fails    |
| 0.159 (1/2π) | 1.9769  | −0.055 | 0.050 | Model fails    |

### 1.3 ZDTP 64D Signature Classes

Three distinct 64D ZDTP signature classes exist for primes p=5 through p=23 under isolated S1 (Master Gateway) transmission. A clean slot arithmetic progression governs peak slot placement.

| **Prime** | **Set**  | **64D peak slot(s)** | **Peak values**  | **Pattern**     | **Class** |
|-----------|----------|----------------------|------------------|-----------------|-----------|
| p=5       | anchor   | 48                   | +1.9968          | Positive single | Class I   |
| p=7       | anchor   | 49                   | +1.9948          | Positive single | Class I   |
| p=11      | anchor   | 50, 61               | +1.9924, −1.9924 | ±pair           | Class II  |
| p=13      | decay    | 51, 60               | +1.9947, −1.9947 | ±pair           | Class II  |
| p=17      | extended | 52, 59               | +1.9883, +1.9883 | Double positive | Class III |
| p=19      | extended | 53, 58               | +1.9872, +1.9872 | Double positive | Class III |
| p=23      | extended | 23/24, 54            | ±pairs + doubled | ±pair (complex) | Class II  |

> **Slot law:** Peak slot advances +1 per prime (48→49→50→51→52→53→54). Partner slot retreats −1 per step (61→60→59→58→...). The p=11 Symmetry Hinge claim (Phase 30) is superseded — ±pair is a class, not a single-prime anomaly.

### 1.4 c₁² + c₃² = 1 — Verified

The identity holds to machine precision (deviation 4.44×10⁻¹⁶ = machine epsilon). It is trivially true by trigonometry once θ_W is accepted as a geometric angle. The non-trivial open question — an analytic expression for θ_W = 6.775° — remains unresolved. θ_W does not match any tested combination of standard constants (log 2, log 3, π/n, arctan(1/k), 1/γ₁) within 0.01 radians.

| **Constant**           | **Value**                                       |
|------------------------|-------------------------------------------------|
| c₁ = sin(θ_W)          | 0.11797805192095003                             |
| c₃ = cos(θ_W)          | 0.99301620292165280                             |
| c₁² + c₃²              | 0.9999999999999996 (deviation: 4.44×10⁻¹⁶)      |
| θ_W                    | 6.775425° (irrational ratio to π)               |
| Closest known constant | arctan(1/8): diff = 6.10×10⁻³ rad (not a match) |

### 1.5 Track D — Zero Pair Count Discrepancy

Phase 29 baseline: 6,290 bilateral zero pairs at N=500 zeros. Phase 31 count: 161 pairs at N=500. The ~39× gap indicates a methodology difference in prime set, threshold, or pairing criterion between the two scripts. This is unresolved and requires reconciliation in Claude Code.

## 2. Open Questions Going Into Phase 32

These are the active unresolved questions drawn from KSJ (12 open cards, #rh-investigation). Claude Code is responsible for the computational tracks; CAILculator handles ZDTP.

| **Question**                                               | **Track**      | **Status / Context**                                                                                       |
|------------------------------------------------------------|----------------|------------------------------------------------------------------------------------------------------------|
| **Where is the regime boundary?**                          | Primary A      | Test p_max ∈ {155,160,165,170,175,180}. Hypothesis: boundary coincides with prime gap 157→163.             |
| **Does Regime 2 converge?**                                | Primary A      | Extend to p_max=1000. Does ratio stabilize, oscillate, or continue descending toward 1.0?                  |
| **What models fit Regime 1 and Regime 2 separately?**      | Primary A      | Power-law y=a·x^(−b)+c for Regime 1 (9 points). Unknown model for Regime 2. Fit independently.             |
| **What governs 64D class assignment?**                     | Secondary ZDTP | I→I→II→II→III→III→II pattern. Test: slot index mod 4 or mod 8. Extend to p=29,31,37.                       |
| **What is the analytic expression for θ_W?**               | Open           | θ_W=6.775° has no match among tested constants. Open to all investigation approaches.                      |
| **Why does the bilateral zero pair count differ 39×?**     | Tertiary D     | Phase 29 script vs Phase 31 script. Pull Phase 29 source, compare prime set, threshold, pairing criterion. |
| **Does D₆ sector placement predict prime set membership?** | Track B        | Requires Phase 19 Gram matrix. Proxy (log(p) mod π) inconclusive. Lower priority.                          |

## 3. Phase 32 Task Specification for Claude Code

Claude Code handles all pure Python computation and JSON output. CAILculator MCP (Claude Desktop) handles all ZDTP gateway transmissions. Do not mix responsibilities.

> **PRIMARY** Track A — Two-Regime Weil Characterization

#### Task A1: Regime boundary fine-scan

Identify the exact p_max at which the Weil ratio crosses from Regime 1 (below ~0.2) to Regime 2 (above ~1.0). The transition is somewhere between p=151 (ratio=0.174) and p=200 (ratio=1.113).

- Test p_max ∈ {155, 157, 160, 163, 165, 170, 175, 180, 190, 200}

- For each p_max, compute: N_primes, Weil RHS (−Σ log(p)/√p), mean_Tr_BK over 500 zeros, ratio

- Use exact same Tr_BK formula as Phase 31: Σ_p (log p/√p) · cos(t_n · log p), p ≤ p_max

- Report: first p_max where ratio exceeds 0.50, and first p_max where it exceeds 1.00

- Test prime gap hypothesis: does the boundary align with the gap 157→163 (gap = 6)?

#### Task A2: Regime 2 extended trajectory

Characterize the full Regime 2 trajectory from p_max=200 to p_max=1000 to determine if the ratio converges, oscillates, or continues declining.

- Compute ratio at p_max ∈ {200, 250, 300, 400, 500, 600, 700, 800, 900, 1000}

- Fit Regime 2 points (p_max ≥ 200) independently: try log decay (y=a·log(x)+b), power law, constant

- Report: best-fit model for Regime 2, estimated asymptote if detectable

- Produce combined 20+ point sequence JSON: phase32_weil_full.json

#### Task A3: Separate regime fitting

Fit Regime 1 (9 points, p_max=13→151) and Regime 2 (10+ points, p_max=200→1000) separately with appropriate models.

- Regime 1: power-law y=a·x^(−b)+c, n_primes as x variable, three fixed-c runs (c₁=0.118, 1/4=0.250, 1/2π=0.159) plus free-fit

- Regime 2: log model y=a·log(x)+b, plus power-law, report best R²

- Report: fitted exponents, R² values, implied asymptotes for each regime

- Save: phase32_regime_fits.json

> **TERTIARY** Track D — Zero Pair Count Reconciliation

#### Task D1: Reproduce Phase 29 count methodology

Phase 29 reported 6,290 bilateral zero pairs at N=500 zeros (CAILculator, 95% confidence). Phase 31 produced 161 pairs using a different Python script. The ~39× gap must be explained.

- Locate Phase 29 script (rh_phase29.py or equivalent) — check project directory

- Document: prime set used, pairing threshold/criterion, definition of 'bilateral zero pair'

- Run Phase 31 script (rh_phase31.py) with Phase 29 parameters — attempt to reproduce 6,290

- If scripts differ: identify exactly which parameter drives the 39× discrepancy

- Report: reconciliation findings. Which count (161 or 6,290) reflects the correct methodology?

> **DEFERRED** Track B — D₆ Direction Partition (lower priority)

#### Task B1: Phase 19 Gram matrix classification (if time permits)

The Track B proxy (log(p) mod π) was inconclusive. The definitive answer requires the full Phase 19 bilateral 8D data and Gram matrix analysis. This is a lower-priority task — proceed only after A1–A3 and D1 are complete.

- Load Phase 19 bilateral 8D direction vectors from project JSON outputs

- Compute Gram matrix of 45-direction D₆ set

- Classify {5,7,11} vs {2,3,13} by actual 6D sector placement

- Test: does sector placement predict prime set membership or 64D class?

## 4. Constants and Formula Reference

All values machine-verified. Use these exactly — do not re-derive unless explicitly updating.

#### Core constants

| **Symbol**      | **Value**           | **Description**                                                   |
|-----------------|---------------------|-------------------------------------------------------------------|
| c₁              | 0.11797805192095003 | sin(θ_W) — sedenion structural angle / Weil ratio floor candidate |
| c₃              | 0.99301620292165280 | cos(θ_W) — Weil angle cos component                               |
| θ_W             | 6.775425°           | Weil angle (permanent structural constant)                        |
| c₁²+c₃²         | 1.0000000000000000  | Unit norm identity (4.44×10⁻¹⁶ deviation)                         |
| ℏ_sed           | 11.19 ± 1.71        | Sedenion Planck constant (constant across 100 zeros)              |
| N_zeros         | 500                 | Riemann zeros used for all ratio computations                     |
| Weil ratio (6p) | ≈ 0.248             | Stable across prime sets p_max=13–23 (Phase 29)                   |

#### Weil ratio formula

Tr_BK(t_n) = Σ_{p ≤ p_max} (log p / √p) · cos(t_n · log p)

> Weil_RHS = −Σ_{p ≤ p_max} log(p) / √p
>
> ratio = mean(Tr_BK over N_zeros) / Weil_RHS

> **Verification:** Weil RHS formula verified exact against Phase 30 at all 9 baseline points. Do not change.

#### AIEX-001a — Berry-Keating sedenion product

F(σ+it) = ∏_p exp_sed(t · log p · r_p / ‖r_p‖)

where r_p is the E8 root direction for prime p, exp_sed is the sedenion exponential.

#### Prime sets

| **Set**           | **Primes**      | **Role**                                                                      |
|-------------------|-----------------|-------------------------------------------------------------------------------|
| Anchor / isometry | {5, 7, 11}      | GUE norm cluster [0.9984, 0.9974, 0.9962]; exact algebraic isometry         |
| Decay drivers     | {2, 3, 13}      | Structurally distinct low-magnitude basin in 64D; p=2 dominates Weil residual |
| Extended          | {17, 19, 23}    | Phase 31 ZDTP — Class III (double positive) for p=17,19; Class II for p=23    |
| Baseline 6-prime  | {2,3,5,7,11,13} | Phase 29 standard set; captures ~1/4 of full Weil sum                         |

## 5. Required Output Files

All outputs to be saved as JSON and/or CSV for downstream use in CAILculator and paper writing.

| **Filename**                       | **Track** | **Contents**                                              |
|------------------------------------|-----------|-----------------------------------------------------------|
| phase32_boundary_scan.json         | A1        | p_max, N_primes, ratio, Weil_RHS for fine-scan values     |
| phase32_weil_full.json             | A2        | Full extended sequence p_max 13→1000                      |
| phase32_regime_fits.json           | A3        | Regime 1 and Regime 2 fit parameters, R², asymptotes      |
| phase32_track_d_reconciliation.txt | D1        | Methodology comparison, parameter differences, conclusion |

#### JSON schema for Weil ratio outputs

```json
{

"phase": 32,

"track": "A1",

"N_zeros": 500,

"c1": 0.11797805192095003,

"points": [

{ "p_max": 155, "N_primes": 36, "ratio": <float>, "Weil_RHS": <float> },

...

]

}
```

## 6. Known Constraints and Prior Script Issues

> **Verified working:** numpy, scipy, mpmath — install: pip install numpy scipy mpmath

> **Do not modify:** The Tr_BK formula (verified against Phase 30 baseline). The N_zeros=500 zero set. The c₁ value.

The Phase 31 bilateral zero pair count discrepancy (161 vs 6,290) is the only known script issue. The root cause is unknown — likely prime set scope or pairing threshold. Treat Phase 29 count as the ground truth until reconciled.

For large p_max values (≥500), prime generation via sympy.primerange or a sieve is required. The Sieve of Eratosthenes up to p_max=1000 is fast enough; no special optimization needed.

## 7. Broader Investigation Context

This section is for orientation only — not a task specification. Claude Code does not need to act on this but should understand where Phase 32 sits in the larger investigation.

#### AIEX-001a — The central conjecture

F(σ+it) = ∏_p exp_sed(t · log p · r_p / ‖r_p‖) is the Berry-Keating xp Hamiltonian in 16D sedenion space. The Weil ratio ≈ 0.248 is the fraction of the Weil sum captured by the 6-prime embedding — interpreted as the 6-prime sedenion product capturing ~1/4 of the full Weil explicit formula. The two-regime structure discovered in Phase 31 is new data for this conjecture: the regime boundary near p≈157–163 may correspond to a phase transition in the BK time-evolution.

#### Canonical Six paper — April 1 deadline

v1.4 targets April 1 (Sophie Germain's 250th birthday) as a Zenodo milestone. The abstract must be revised to reflect Phase 31 findings before publication. Specifically: 'Sedenion Horizon Theorem' → 'Sedenion Horizon Conjecture'; decay exponent b≈0.42 (not 1/√N); add Phase 31 two-regime finding. This revision is independent of Phase 32 computation and will be handled separately.

#### KSJ knowledge base

107 AIEX entries as of Phase 31, tracking all findings. Phase 32 AIEX entries will be committed after results are reviewed. The standard workflow: extract_insights → present for approval → commit_aiex. Never auto-commit.

*Chavez AI Labs LLC · Applied Pathological Mathematics · 2026-03-27*

GitHub: ChavezAILabs/CAIL-rh-investigation · Zenodo: 10.5281/zenodo.17402495
