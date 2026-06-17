# RH Investigation — Phase 77 Results: Encoding Reconciliation & the Signed Gateway Channel
**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Date:** June 12, 2026
**Phase:** 77 (Q-14 + Q-15)
**Tag:** #phase-77-encoding · #phase-77-convergence
**Execution:** Claude Fable 5, in-shell (Phase 77 mandate, June 11, 2026)
**Branch:** `phase-77-archaeology`

---

## Executive Summary

**Q-14 (encoding reconciliation): CLOSED.** The Gateway Linear Law (Phase 76) applied to the recovered Phase 73 baseline vector reproduces every recorded Phase 73 observable — mean magnitude 35.38, convergence 0.4274 (exact to 4 dp), B/A ratio 3.66 — and a live June 12 run confirms the current v2.1.4 server returns the identical values on the historical input. The law's asymptotics also explain the recorded Phase 73 invariants in closed form: μ ≈ 2.5γₙ is exactly (3√17+3)/6 = 2.5616, the "fixed 57% std/mean" is the law asymptote 0.6096, and the convergence descent 0.4274→0.3950 is approach to the law asymptote 0.3904. The sole law-incompatible record is the Phase 75 Q-2/Q-4 magnitude table, now formally quarantined by an **infeasibility certificate**: at σ=½ the law forces |M_g| ≥ √16.25 = 4.0311 for *any* 16D input, but Phase 75 published 2.565–2.570 at t=±20. Cross-phase magnitude comparisons must therefore cite Phase 76+ runs only.

**Q-15 (convergence/bilateral-annihilation γₙ probe): CLOSED — negative for all existing ZDTP channels, with a constructive discovery.** Dense sweeps (19,001 points, t ∈ [10,105], γ₁–γ₃₁) show no γₙ signature in the convergence channel or in the nonlinear bilateral sandwich residuals. But the **explicit-formula positive control** — the scalar −Σₚ (log p/√p)cos(t·log p) built from the *same six prime oscillators* — detects the zeros decisively (z = 6.36). The negative is therefore **architectural, not information-theoretic**: the signal is present in the encoding and is destroyed downstream. Pinpointing where: the **signed gateway scalar c_S2** (which the server computes and exposes at 32D lift slot 0) carries a significant γₙ value signature (z = +3.72, p = 0.0004, Bonferroni-surviving), and the magnitude law |M|² = ‖x‖² + 4c² + 16(2σ)² **squares c, erasing the sign coherence that carries the signal**. The instrument detects the zeros, then discards the detection before reporting. Reading the signed lift scalar directly — the proposed **Signed Gateway Channel** — turns the CAILculator into a genuine (weak, 6-prime) zero detector.

**Q-17 (Signed Gateway Channel characterization): CLOSED same-day.** Scale test: the c_S2 signature strengthens to z = 4.92 over γ₁–γ₁₀₁. The **Detector Encoding** exploits the disjoint supports of u₂ and u₆ to realize the full 6-prime explicit-formula detector *exactly* as the sum of two signed instrument readings — c_S2 + c_S6 = −2·Σ(log p/√p)cos(t·log p), residual 1.8×10⁻¹⁵, live-validated at γ₁. Detector performance over 101 zeros: **z = 8.42, ROC AUC 0.87 (δ=0.5), peak precision 0.83 vs 0.43 chance at ε=0.5**. See §2A.

Environment re-verified June 12: 8,061 jobs · 0 errors · 1 sorry (by design) · stack at commit `e1f170e` intact.

---

## 1. Q-14 — Encoding Reconciliation

### 1.1 Provenance recovery

No Phase 73–75 generator script or result JSON exists in the repo (newest pre-76 results are `RH_Phase70_*.json`). The Phase 73–75 baseline input is preserved verbatim in `CAILculator_Phase73_Runs_AB.md` (May 5, 2026), Run B (γ₁ = 14.1347, σ ∈ {0.3, 0.5, 0.7}):

```
[σ, 14.1347, σ+0.0019, -0.8651, 0.3546, -0.935, 0.6283, 0.778,
 0.1288, -0.9917, 0.4154, -0.9097, 0.7071, 0.7071, 0.0, 0.0]
```

Two encoding-convention differences vs the Phase 76 Documented Encoding: position 2 was **σ + 0.0019** (now σ − ½ + 0.0019), and positions 3–13 were a **fixed "standard prime encoding template"** held constant across γₙ (the Run A protocol recomputed only positions 0–5 per zero).

### 1.2 Template archaeology (negative, recorded honestly)

Grid search of positions 3–13 against ±cos/sin(γₙ·ln p) for n = 1..4, p ∈ {2,3,5,7,11,13}, with and without 1/√2 scaling (tolerance 2.5×10⁻⁴ matching the 4-dp record):

- pos12 = pos13 = **1/√2** (identified; residual 7×10⁻⁶).
- Positions 3–11: **UNIDENTIFIED** under any candidate. The nearest non-match: (pos8, pos9) ≈ cos/sin(t·ln 13) at t ≈ 14.1357 (not 14.1347; residual ~3×10⁻³).
- All four (cos,sin)-type pairs (4,5), (6,7), (8,9), (10,11) are unit-norm, confirming oscillator structure, but their generating formulas are not reproducible from the documented families.

**Consequence:** the old template is not regenerable; the Phase 76 Documented Encoding is the only reproducible standard. This retroactively justifies the Phase 76 encoding-freeze rule.

### 1.3 The Linear Law reproduces every recorded Phase 73 observable

Applying c_g = −2⟪x, P_g+Q_g⟫, |M_g|² = ‖x‖² + 4(c_g² + 4(2σ)²) to the recovered σ=0.5 vector:

| Observable | Law (replica) | Recorded (2026-04-29) | Source |
|---|---|---|---|
| Mean 256D magnitude at γ₁ | **35.3833** | 35.38 | AIEX-587 |
| Convergence at γ₁ | **0.4274** | 0.4274 | AIEX-586 |
| B/A ratio at γ₁ | **3.6591** | 3.66 | Phase 73 Run A doc |
| std/mean at γ₁ | **0.5726** | "~57%" | Q-10 |

And the law's F(s)-input asymptotics (Class B |M| → √17·t, Class A |M| → t) give closed forms for the recorded invariants:

| Invariant | Law closed form | Recorded |
|---|---|---|
| Mean magnitude growth | (3√17+3)/6 · γₙ = **2.5616·γₙ** | "μ ≈ 2.5γₙ" (AIEX-621, Q-9) |
| std/mean asymptote | **0.6096** | "0.57–0.62 fixed" (Q-10) |
| Convergence asymptote | **0.3904** | descent 0.4274→0.3950, γ₁–γ₄ (AIEX-586) |

Q-9 and Q-10, closed empirically in Phase 73, are now **derived** results.

### 1.4 Live instrument-continuity run (June 12, 2026)

The verbatim historical vector was transmitted to the current CAILculator v2.1.4 server (RHI profile, gateway=all). Server returned: mean magnitude **35.38331177450292**, convergence **0.4273964226844107**, B/A **3.6591** — identical to the April 29 v2.0.3 record and matching the law replica to ~10⁻¹² on all six gateway magnitudes. All six bilateral verifications passed (PQ = QP = 0 at 10⁻¹⁵). Raw record: `results/phase77_q14_live_continuity_run.json`.

**The Phase 73 magnitude channel is retroactively law-consistent across two server versions.**

### 1.5 Infeasibility certificate for the Phase 75 Q-2/Q-4 table

Under the v2.1.4 law at σ = ½: |M_g|² = ‖x‖² + 4c_g² + 16 ≥ σ² + 16 = 16.25, hence

> **|M_g| ≥ 4.0311 for every 16D input with position 0 = ½.**

Phase 75 (v2.0.4) published S3 = 2.570, S4 = S5 = 2.565, S6 = 2.570 at t = ±20 — all below the floor, hence unreachable by *any* input under the current law. Additionally, the law's documented-encoding predictions at t = 1 and t = 20 match no published Phase 75 magnitude under any uniform rescaling.

**Verdict:** the Phase 75 Q-2/Q-4 magnitude tables came from a structurally different v2.0.4 pipeline (or post-processing) and are **quarantined for cross-phase comparison**. The Phase 75 *Lean* results (`critical_line_convergence` etc.) are entirely unaffected — they are independent of CAILculator.

### 1.6 The "phantom σ=½ pairing collapse" as explicit functional conditions

Under the law, |M_i| = |M_j| ⟺ ⟪x, u_i−u_j⟫·⟪x, u_i+u_j⟫ = 0 (u_g = P_g+Q_g). The three pairings Phase 75 reported at σ=½ require, e.g.:

- S1=S2 ⟺ (x₁+x₁₄−x₅−x₁₀)·(x₁+x₁₄+2x₃+2x₁₂+x₅+x₁₀) = 0
- S4=S5 ⟺ (x₃−x₁₂−x₅−x₁₀)·(2x₁−2x₁₄+x₃−x₁₂+x₅+x₁₀) = 0

Neither the recovered Phase 73 vector nor the documented encoding satisfies any of the 15 pair conditions identically; on the critical line they vanish only at isolated t (zero-crossing counts in the results JSON). σ does not appear in any condition — reconfirming Q-5's negative closure (pairing is an encoding condition, not a Re(s)=½ characterization). The t ≈ 18–22 "collapse" is the Class A scalars' zero crossings (computed: S2 at t=20.06; S3 at 20.33; S6 at 20.54), set by prime logs — γ₄ = 21.022 is not among them.

**Q-14: CLOSED.**

---

## 2. Q-15 — Convergence/Bilateral-Annihilation γₙ Probe

### 2.1 Design

Documented encoding, σ = ½, t ∈ [10, 105], Δt = 0.005 (19,001 points), zeros γ₁–γ₃₁ in range. Channels:

- **conv(t)** — convergence score (law-determined; control).
- **Sandwich residuals** r_g(t) = ‖(x·P_g)·(Q_g·x)‖/‖x‖² and the opposite orientation — bilinear in x, genuinely outside the scalar-contraction law. Computed via the Cayley-Dickson structure tensor (replica validated against the live server at 10⁻⁹ in Phase 76 and re-validated live in §2.4).
- **Gateway scalars** c_g(t) for Class A (bounded oscillators; Class B are t-dominated).
- **Weighted-encoding variants** (prime blocks scaled by log p/√p).
- **Positive control:** −Σₚ (log p/√p)cos(t·log p) — the optimal explicit-formula zero detector constructible from the same six oscillators.

Tests: **T1** — mean channel value at the zeros vs 5,000 Monte Carlo draws of 31 uniform t (two-sided). **T2** — mean distance from zeros to nearest channel minimum, with the minima held *fixed* and query points randomized (randomizing the minima themselves fakes proximity, because prime-log oscillator minima are quasi-regular — a null-model correction applied during this work and documented in the script).

### 2.2 Results

| Channel | T1 z | T1 p | T2 p(close) | Verdict |
|---|---|---|---|---|
| conv (law control) | 0.31 | 0.70 | 0.98 | no signature |
| sandwich residuals (6 gateways, 2 orientations, class means) | \|z\| ≤ 1.44 | ≥ 0.135 | ≥ 0.07 | no signature |
| weighted-encoding conv / sandwich | −0.09 / −1.41 | 0.98 / 0.15 | 0.99 / 0.52 | no signature |
| **c_S2 (signed gateway scalar)** | **+3.72** | **0.0004** | 0.998 | **VALUE SIGNATURE** |
| c_S6 / c_S3 | 2.05 / 1.87 | 0.041 / 0.060 | — | marginal, consistent |
| **explicit-formula control** | **+6.36** | **< 0.0002** | **< 0.0005** (maxima) | decisive (as theory predicts) |

c_S2's p = 0.0004 survives Bonferroni correction across all 21 channels tested (0.0004 × 21 = 0.0084).

### 2.3 The mechanism — and why the magnitude channel is blind

The signature strength tracks the **number of cosine terms** in each gateway functional:

- c_S2 = −2(cos(t·ln2) + cos(t·ln13) + sin(t·ln3) + cos(t·ln11)) — **3 cosines** → z = 3.72
- c_S6, c_S3 — 1 cosine each → z ≈ 2.0, 1.9
- explicit-formula control — all 6 cosines, optimally weighted → z = 6.36

At Riemann zeros, Σₚ cos(γ·ln p) is systematically negative (the k=1 von Mangoldt explicit formula), so c_S2 is systematically *positive-high* at zeros. The magnitude law |M|² = ‖x‖² + 4c² + 16(2σ)² is **even in c** — squaring destroys exactly the sign coherence that carries the signal. This single fact explains the entire Q-15 landscape: signal present in c (linear), absent in |M| and conv (even in c), absent in the sandwich residuals (norm-type, also even).

### 2.4 Live confirmation (June 12, 2026)

Documented-encoding vector at t = γ₁ = 14.134725141734695, gateway S2, RHI profile: server 32D lift slot 0 = **2.828631554103408** vs replica prediction 2.8286315541034086 (agreement 10⁻¹⁵), positive-high at γ₁ exactly as the signature predicts. The signed scalar is already a first-class server observable — no instrument change is needed to read it.

### 2.5 Verdicts and the constructive proposal

- **Q-15 as posed: NEGATIVE.** Neither the convergence channel nor the bilateral-annihilation (sandwich-residual) channel carries a γₙ signature, under the documented or weighted encodings. Phase 76's Q-6 resolution (no γₙ lock in magnitude dips) extends to all norm-type channels.
- **The negative is architectural, not information-theoretic.** The same six oscillators detect zeros decisively when read as a signed, weighted linear functional.
- **Proposed new observable (Q-17 candidate): the Signed Gateway Channel** — read c_g from the 32D lift directly (already exposed), optionally with explicit-formula weights in the encoding. Predicted detector strength at the c_S2 level (z ≈ 3.7) unweighted, z ≈ 6.4 weighted. This is the first ZDTP observable with demonstrated zero-detection capability, and it is a *proved-formula* observable (c_g = −2⟪x, u_g⟫, Phase 76 Lean: `gateway_pairing_iff` infrastructure).

**Q-15: CLOSED (negative as posed; constructive discovery logged).**

---

## 2A. Q-17 — The Signed Gateway Channel as a Zero Detector (June 12, 2026)

Q-17 (proposed in §2.5) was executed same-day. Three results:

### 2A.1 Scale test (γ₁–γ₁₀₁)

Extending the sweep to t ∈ [10, 240] (46,001 points, 101 zeros): the c_S2 signature **strengthens with sample size** — z = 3.62 at 31 zeros → **z = 4.92 at 101 zeros** (p < 0.0002). Growth is sub-√N (√N prediction 6.53), consistent with a fixed 6-prime resolution against rising zero density — the expected behavior of a genuine but truncation-limited signal, not an artifact.

### 2A.2 The Detector Encoding — exact realization of the explicit-formula detector

The supports of u₂ = e₃+e₁₂+e₅+e₁₀ and u₆ = e₂−e₁₃+e₆+e₉ are disjoint. Placing w_p·cos(t·ln p), w_p = log p/√p, in those slots (p = 2,3,11,13 → u₂ slots; p = 5,7 → u₆ slots; pos2 = 0; pos0 = σ, pos1 = t retained) yields the **exact identity**:

> **c_S2(D(t)) + c_S6(D(t)) = −2·Σₚ (log p/√p)·cos(t·log p)** (sweep residual 1.8×10⁻¹⁵)

— the full 6-prime k=1 von Mangoldt explicit-formula detector, realized as the **sum of two signed readings of the unmodified instrument**. Live-validated June 12: pattern 2 returned 3.1204551984921403 and pattern 6 returned 2.102194713548072 at γ₁ (both exact; sum 5.2226499…). This is a deliberate, documented deviation from the Documented F(s) Encoding (purpose-built detector input). Detector statistic at 101 zeros: **z = 8.42**.

### 2A.3 Detector performance (γ₁–γ₁₀₁, honest baselines)

| Metric | c_S2 (documented) | Detector (c_S2+c_S6) | Chance baseline |
|---|---|---|---|
| ROC AUC, δ=0.25 | 0.673 | **0.810** | 0.500 |
| ROC AUC, δ=0.5 | 0.694 | **0.866** | 0.500 |
| Peak precision @ ε=0.5 | 0.718 | **0.831** | 0.433 |
| Peak F1 @ ε=0.5 | 0.656 | **0.719** | — |
| Peak precision @ ε=1.0 | 0.847 | 0.974 | 0.875 (≈ mean gap 2.28) |

The ε=0.5 figures are the meaningful ones (ε=1.0 baseline is near-saturated at this zero density and is reported only for completeness). A high-γ documented-encoding spot check (γ₁₀₀, pattern 2: server −1.1533297669142253 = replica to 10⁻¹⁵) is recorded with a *negative* reading — the signature is statistical, not pointwise, and the record keeps that honest.

### 2A.4 Candidate Lean lemma (not yet implemented)

The detector identity is pure algebra over the Gateway Linear Law and is formalizable with standard axioms over the `GatewayLinearLaw.lean` infrastructure:

```
theorem detector_channel_identity (t : ℝ) :
    gatewayScalar (D t) 2 + gatewayScalar (D t) 6
      = -2 * ∑ p ∈ {2,3,5,7,11,13}, (Real.log p / Real.sqrt p) * Real.cos (t * Real.log p)
```

The zero-detection *statistics* are number-theoretic (explicit-formula truncation) and are not a Lean target. Implementation deferred pending Paul's call on whether to grow the stack (would be an 18th-file or GatewayLinearLaw addition; current verified baseline 8,061 jobs untouched).

**Q-17: CLOSED (characterized).** The Signed Gateway Channel is the first ZDTP observable with demonstrated, quantified zero-detection capability — AUC 0.87, detector z = 8.42 — and it is exactly the explicit-formula truncation, proved by construction and validated live.

---

---

## 3. `ba_asymptote_sq` — Lean Theorem (June 17, 2026)

**Proved and verified by Claude Sonnet 4.6, in-shell, June 17, 2026.**

This is the algebraic closure of Q-8: the B/A = √17 asymptote is a proved limit, not a numerically observed one. Added as the 4th theorem to `GatewayLinearLaw.lean`.

```lean
theorem ba_asymptote_sq (K : ℝ) (hK : 0 ≤ K) :
    Filter.Tendsto (fun t : ℝ => (17 * t ^ 2 + K) / (t ^ 2 + K))
      Filter.atTop (nhds 17)
```

**Interpretation:** Class B gateways (S1/S4/S5) have u_g supported on the pos1=t slot, giving c_B ≈ −2t for large t. Class A gateways (S2/S3/S6) have bounded c_A = O(1). With K = 16σ² ≥ 0 and ‖x‖² ≈ t² for large t: |M_B|² ≈ 17t² + K and |M_A|² ≈ t² + K, whence the ratio B²/A² → 17 and B/A → √17.

**Proof route:** Factor (17t²+K)/(t²+K) = 17 − 16K/(t²+K), then:
1. Show (t²+K) → +∞ via `Real.sqrt` witness in `Filter.eventually_atTop`
2. Compose `tendsto_inv_atTop_zero` for the inverse
3. Multiply correction by constant via `Tendsto.mul`
4. Subtract from constant 17 via `Tendsto.sub`
5. Close with `congr'` + `field_simp` + `ring`

**Notable obstacles:** (a) `Filter.tendsto_atTop.mpr` does not accept `refine ⟨...⟩` directly — requires `rw [Filter.tendsto_atTop]` then `rw [Filter.eventually_atTop]` first; (b) `le_or_lt` is not in scope via the EuclideanDist import chain in Mathlib v4.28.0 — replaced with `by_cases hbK : b ≤ K` (uses Classical.em). See CLAUDE.md notes 17, 18 for analogous patterns.

**Axiom footprint:** `[propext, Classical.choice, Quot.sound]` — standard only. ✓

**Build verification:** 8,061 jobs · 0 errors · 1 sorry (unchanged) · `ba_asymptote_sq` axiom audit clean.

**Q-8 status:** CLOSED. The architectural B/A = √17 ratio is now doubly attested — empirically observed over γ₁–γ₃₁ (converging from above, γ₁₂ local minimum 4.067) and proved as a limit theorem. The E₈/Fano argument explains the *class partition* (why Class B gateways carry the t-slot); the ratio itself is arithmetic: (t-slot weight)² + (three bounded oscillators)² : (four bounded oscillators)² as t → ∞.

---

## 4. Run B — Bilateral Magnitude Symmetry Scan (June 17, 2026)

**Execution:** Claude Sonnet 4.6, in-shell, analytical via Gateway Linear Law (no live MCP calls needed — the law is proved exact).  
**Script:** `scripts/phase77_runB_bilateral_scan.py`  
**Results:** `results/phase77_runB_results.json`

### 4.1 Protocol

Documented F(s) Encoding. For each σ ∈ {0.10, 0.15, ..., 0.90} (17 values, Δσ=0.05) and each of γ₁/γ₂/γ₃, transmit two vectors (t = +γ and t = −γ) and record:

> **bilateral_diff_g(σ, γ) = |M_g(σ, +γ)| − |M_g(σ, −γ)|**

for all six gateways. Computation is analytical via |M_g|² = ‖x‖² + 4*(c_g² + 4*(2σ)²) and c_g = −2⟪x, u_g⟫ (proved Gateway Linear Law, accurate to machine precision).

### 4.2 Full Results: Run B-1 (γ₁ = 14.134725141734695)

| σ | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| 0.10 | −6.2442 | −0.5805 | −1.6154 | −8.2011 | −6.1124 | −2.7407 |
| 0.15 | −6.2435 | −0.5796 | −1.6127 | −8.2001 | −6.1118 | −2.6232 |
| 0.20 | −6.2424 | −0.5783 | −1.6088 | −8.1988 | −6.1108 | −2.5033 |
| 0.25 | −6.2411 | −0.5767 | −1.6039 | −8.1971 | −6.1095 | −2.3812 |
| 0.30 | −6.2395 | −0.5746 | −1.5978 | −8.1949 | −6.1080 | −2.2572 |
| 0.35 | −6.2376 | −0.5722 | −1.5907 | −8.1924 | −6.1061 | −2.1317 |
| 0.40 | −6.2354 | −0.5695 | −1.5826 | −8.1895 | −6.1040 | −2.0049 |
| 0.45 | −6.2328 | −0.5664 | −1.5736 | −8.1861 | −6.1016 | −1.8772 |
| **0.50** | **−6.2300** | **−0.5631** | **−1.5636** | **−8.1824** | **−6.0989** | **−1.7490** |
| 0.55 | −6.2269 | −0.5594 | −1.5528 | −8.1783 | −6.0959 | −1.6205 |
| 0.60 | −6.2235 | −0.5555 | −1.5413 | −8.1738 | −6.0926 | −1.4921 |
| 0.65 | −6.2198 | −0.5513 | −1.5289 | −8.1689 | −6.0891 | −1.3641 |
| 0.70 | −6.2158 | −0.5469 | −1.5160 | −8.1637 | −6.0853 | −1.2368 |
| 0.75 | −6.2115 | −0.5423 | −1.5024 | −8.1580 | −6.0812 | −1.1104 |
| 0.80 | −6.2069 | −0.5375 | −1.4882 | −8.1520 | −6.0768 | −0.9852 |
| 0.85 | −6.2020 | −0.5325 | −1.4736 | −8.1456 | −6.0721 | −0.8615 |
| 0.90 | −6.1969 | −0.5273 | −1.4585 | −8.1388 | −6.0672 | −0.7395 |

### 4.3 Full Results: Run B-2 (γ₂ = 21.022039638771555)

| σ | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| 0.10 | −10.0206 | +0.4015 | +0.6441 | +3.4942 | +7.6575 | −0.5087 |
| 0.20 | −10.0194 | +0.4007 | +0.6428 | +3.4938 | +7.6565 | −0.4652 |
| 0.30 | −10.0173 | +0.3993 | +0.6406 | +3.4930 | +7.6547 | −0.4208 |
| 0.40 | −10.0142 | +0.3974 | +0.6375 | +3.4920 | +7.6522 | −0.3757 |
| **0.50** | **−10.0103** | **+0.3950** | **+0.6336** | **+3.4906** | **+7.6490** | **−0.3302** |
| 0.60 | −10.0056 | +0.3920 | +0.6289 | +3.4890 | +7.6451 | −0.2845 |
| 0.70 | −9.9999 | +0.3887 | +0.6234 | +3.4870 | +7.6404 | −0.2389 |
| 0.80 | −9.9934 | +0.3849 | +0.6173 | +3.4847 | +7.6350 | −0.1937 |
| 0.90 | −9.9861 | +0.3807 | +0.6106 | +3.4822 | +7.6289 | −0.1489 |

(Full 17-row table in `results/phase77_runB_results.json`.)

### 4.4 Full Results: Run B-3 (γ₃ = 25.010857580145688)

| σ | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| 0.10 | +2.3733 | −0.5898 | +0.4186 | −1.4822 | −7.4624 | +2.0954 |
| 0.20 | +2.3730 | −0.5889 | +0.4180 | −1.4821 | −7.4618 | +1.9276 |
| 0.30 | +2.3727 | −0.5875 | +0.4169 | −1.4819 | −7.4607 | +1.7572 |
| 0.40 | +2.3722 | −0.5855 | +0.4155 | −1.4816 | −7.4592 | +1.5849 |
| **0.50** | **+2.3715** | **−0.5829** | **+0.4136** | **−1.4812** | **−7.4572** | **+1.4114** |
| 0.60 | +2.3707 | −0.5797 | +0.4114 | −1.4807 | −7.4549 | +1.2371 |
| 0.70 | +2.3698 | −0.5761 | +0.4088 | −1.4801 | −7.4521 | +1.0629 |
| 0.80 | +2.3687 | −0.5719 | +0.4059 | −1.4794 | −7.4488 | +0.8892 |
| 0.90 | +2.3675 | −0.5674 | +0.4026 | −1.4786 | −7.4451 | +0.7167 |

### 4.5 Key Findings

**FINDING 1 (ANOMALY vs handoff prediction): Bilateral differences are NONZERO at σ=½ for ALL gateways at ALL three γ values.**

The Run B handoff predicted |M_g(½+iγ)| − |M_g(½−iγ)| = 0 "exactly (proved, Q-4)." The data refutes this for the Documented F(s) Encoding at all γ values tested:

| Gateway | γ₁ | γ₂ | γ₃ |
|---|---|---|---|
| S1 | −6.2300 | −10.0103 | +2.3715 |
| S2 | −0.5631 | +0.3950 | −0.5829 |
| S3 | −1.5636 | +0.6336 | +0.4136 |
| S4 | −8.1824 | +3.4906 | −1.4812 |
| S5 | −6.0989 | +7.6490 | −7.4572 |
| S6 | −1.7490 | −0.3302 | +1.4114 |

**FINDING 2: Theoretical explanation — time-reversal asymmetry of gateway scalars.**

The norm symmetry IS preserved: ‖x(+γ)‖² = ‖x(−γ)‖² exactly (= 203.7955... at σ=0.5, γ=γ₁; difference 0.00×10⁰ to full double precision). All components squared, so sign flips on odd-indexed components cancel. However:

c_g(+t) ≠ c_g(−t) because the gateway sums u_g have support on *odd-indexed* components:
- pos1 = t (sign flips: S1, S4, S5)
- pos4,5 = sin(t·ln3)/√2, sin(t·ln3) (S2 partial, S3 partial)
- pos7,9,11,13 = sin/√2 terms (S3, S5, S6 partial)

At γ₁, σ=0.5:
- S1: c(+t) = −26.66, c(−t) = +29.88 → large bilateral asymmetry from the t-slot
- S4: c(+t) = −26.15, c(−t) = +30.38 → similar
- S5: c(+t) = −27.05, c(−t) = +30.20 → similar
- S2: c(+t) = +2.83, c(−t) = +3.54 → small asymmetry (sin(t·ln3) component only)

Since |M|² = ‖x‖² + 4*(c² + const), and ‖x‖² is symmetric, the bilateral difference is driven purely by c² asymmetry: **|M(+t)|² − |M(−t)|² = 4*(c(+t)² − c(−t)²) = 16·a_g·b_g** where a_g = inner(x_even, u_g) and b_g = inner(x_odd, u_g).

**FINDING 3: The Q-4 "proved" claim in the handoff misapplied `pairing_sigma_independent`.**

The proved theorem `pairing_sigma_independent` states: for fixed input x, the *cross-gateway* magnitude difference |M_g(x,σ₁)| − |M_h(x,σ₁)| equals |M_g(x,σ₂)| − |M_h(x,σ₂)|. This is about different gateways at the same input, not bilateral (±t) pairs at the same gateway. The Phase 75 Q-4 magnitude tables are already quarantined (§1.5 infeasibility certificate). The sedenion norm equality ‖F(+t)‖ = ‖F(−t)‖ holds (confirmed above), but it does not imply ZDTP gateway magnitude equality.

**FINDING 4: γ-dependence is STRONG — curve shapes are NOT γ-independent.**

Signs and magnitudes change substantially across γ₁/γ₂/γ₃:
- S2 flips from negative (γ₁,γ₃) to positive (γ₂)
- S3 flips from negative (γ₁) to positive (γ₂,γ₃)
- S4, S5 change by factors of 4–5 and flip sign
- S6 flips from negative (γ₁,γ₂) to positive (γ₃)

The only gateway without a sign flip is S1, which is t-dominated in all three cases.

**FINDING 5: S6 bilateral diff is uniquely σ-sensitive.**

S6 is the only gateway where c_g contains pos2 = σ−0.5+0.0019 (an explicit σ-linear term). Slope of S6 bilateral diff per unit σ: 2.50 (γ₁), 0.45 (γ₂), −1.72 (γ₃). The slope is γ-dependent because b_S6 (the odd/sin component of c_S6) changes with γ. S1–S5 slopes are much smaller (range 0.047–0.17 per unit σ at γ₁).

S6 extrapolated zero-crossing: σ ≈ 1.20 (γ₁), σ ≈ 1.23 (γ₂), σ ≈ 1.32 (γ₃) — all outside the critical strip 0 < Re(s) < 1.

**FINDING 6: Architecture confirmed — the bilateral asymmetry is NOT a critical-line probe.**

The Run B bilateral difference carries no special feature at σ=½ under the Documented F(s) Encoding. The bilateral structure was designed for the Signed Gateway Channel (Run A/Q-17), where c_g carries the γₙ signature in its sign. The magnitude law (even in c) erases this, and the bilateral difference is a structural artifact of the encoding's t-slot, not a probe of Re(s)=½.

### 4.6 Resolution of the Q-4 Discrepancy

Phase 75 Q-4 was measured with a structurally different pipeline (v2.0.4 encoding — now quarantined). Any bilateral equality observed there was either an artifact of that pipeline or referred to a different quantity (possibly the sedenion norm, which IS time-reversal symmetric). Under the current Documented F(s) Encoding + Gateway Linear Law (v2.1.4), bilateral magnitude equality at σ=½ is not a theorem and not observed.

The correct structural symmetry that IS preserved is:
1. **‖F(+t, σ)‖ = ‖F(−t, σ)‖** — sedenion norm symmetric in t (proved from F_base structure)
2. **`pairing_sigma_independent`** — cross-gateway magnitude differences are σ-free for fixed input
3. **`gateway_magSq_sub`** — the bilateral difference formula |M_g|²−|M_h|² = 16⟪x,u_g−u_h⟫⟪x,u_g+u_h⟫

None of these implies bilateral (±t) equality at σ=½ for individual gateway magnitudes. Run B is complete and properly demarcates the boundary of what the proved structural symmetries guarantee.

---

## 5. Artifacts

| Artifact | Path |
|---|---|
| Q-14 reconciliation script | `scripts/phase77_q14_reconciliation.py` |
| Q-14 results JSON | `results/phase77_q14_reconciliation.json` |
| Q-14 live continuity record | `results/phase77_q14_live_continuity_run.json` |
| Q-15 probe script | `scripts/phase77_q15_convergence_probe.py` |
| Q-15 results JSON | `results/phase77_q15_results.json` |
| Q-17 detector script | `scripts/phase77_q17_signed_channel.py` |
| Q-17 results JSON | `results/phase77_q17_results.json` |
| Q-17 live validation | `results/phase77_q17_live_validation.json` |
| **Run B scan script** | **`scripts/phase77_runB_bilateral_scan.py`** |
| **Run B results JSON** | **`results/phase77_runB_results.json`** |

Build baseline re-verified June 12, 2026 (cached replay) + `ba_asymptote_sq` added June 17: **8,061 jobs · 0 errors · 1 sorry** (`spectral_implies_zeta_zero`, by design) · 1 non-standard axiom (`riemann_critical_line`). Stack files unchanged since Phase 76 (`GatewayLinearLaw.lean` updated with 4th theorem).

**KSJ record (through June 12):** AIEX-731 through AIEX-738 (Q-14/Q-15) + AIEX-739 through AIEX-743 (Q-17). Phase 77 continuation (June 17: `ba_asymptote_sq` + Run B) — KSJ extraction pending Paul's review.

## 6. Phase 77 Remaining Queue

- **Q-16:** sedenion orthogonality theorem in Lean (e₀-transparency of the Canonical Six; needs Cayley-Dickson tensor infrastructure — Phase 78 scope)
- **`detector_channel_identity`:** Lean lemma (Paul's call on stack growth — GatewayLinearLaw addition vs 18th file)
- **v1.4 abstract:** gates Berry/Keating + Tao outreach; key highlights: `critical_line_convergence` (centerpiece), `ba_asymptote_sq` (Q-8 algebraic closure), Signed Gateway Channel / Detector Encoding (Q-17, z=8.42, AUC 0.87)
- ~~`ba_asymptote_sq`~~ **PROVED June 17** (§3): Lean theorem, standard axioms, build clean ✓
- ~~Run B~~ **COMPLETE June 17** (§4): bilateral equality refuted for Documented Encoding; structural explanation in terms of c_g time-reversal asymmetry; Q-4 discrepancy resolved
- ~~Q-17~~ **CLOSED June 12** (§2A): Detector Encoding z=8.42, AUC 0.87
- ~~Q-14, Q-15~~ **CLOSED June 12** (§1, §2)

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering*
*Phase 77 · June 12/17, 2026 · github.com/ChavezAILabs/CAIL-rh-investigation*
