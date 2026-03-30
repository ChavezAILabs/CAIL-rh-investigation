# Phase 32 Results — RH Investigation
**Chavez AI Labs LLC | Applied Pathological Mathematics**
*Paul Chavez | 2026-03-27*
*GitHub: [CAIL-rh-investigation](https://github.com/ChavezAILabs/CAIL-rh-investigation)*

---

## Overview

Phase 32 was designed to characterize the two-regime Weil ratio structure discovered in Phase 31 — specifically to identify the regime boundary near p_max≈200 and extend the Regime 2 trajectory to p_max=1000.

**Primary finding: The Phase 31 "two-regime inversion" does not exist.**

A formula bug in Phase 31's `bilateral_trace` function (missing `1/√p` weight) produced artificially inflated ratios. When the correct Berry-Keating formula is applied, the Weil ratio decreases monotonically through the entire range p_max=13→1000. There is no inversion, no regime boundary, and no "Regime 2."

---

## The Phase 31 Formula Bug

### What Happened

Phase 30 (verified) computed:
```
Tr_BK(t_n) = Σ_p (log p / √p) · cos(t_n · log p)
```

Phase 31's `bilateral_trace` function **dropped the `1/√p` weight**:
```python
# Phase 31 (WRONG):
traces = np.log(primes) * np.cos(gamma * np.log(primes))

# Phase 32 (CORRECT — matches Phase 30 and handoff spec):
traces = (np.log(primes) / np.sqrt(primes)) * np.cos(gamma * np.log(primes))
```

### Verification

| N_zeros | Phase 32 ratio (correct formula, 6 primes) | Expected |
|---------|-------------------------------------------|----------|
| 100     | **0.247931**                              | Phase 30: 0.2479 ✓ |
| 200     | 0.209744                                  | — |
| 500     | 0.173349                                  | — |

| N_zeros | Phase 31 ratio (wrong formula, 6 primes) |
|---------|------------------------------------------|
| 100     | 0.653767 (2.64× too high)               |
| 500     | 0.455093 (2.63× too high)               |

The wrong formula produces ratios ~2.6× too high for small prime sets. For large prime sets (p_max≥200), the distortion is even larger — the wrong formula gives ratios above 1.0, creating the apparent "inversion."

### Phase 31 Values Now Invalidated

| p_max | Phase 31 (INVALID) | Phase 32 (correct) |
|-------|--------------------|--------------------|
| 200   | 1.1132             | **0.1286**         |
| 300   | 1.0786             | **0.1181**         |
| 500   | 0.9928             | **0.1027**         |
| 700   | 0.9549             | **0.0938**         |

The "Weil ratio inversion at p_max≈200" does not exist. The correct ratios are in the range 0.09–0.13, continuing the monotone declining trend.

---

## Track A1 — Regime Boundary Fine-Scan

**Finding: No regime boundary. No inversion. Monotone decline throughout.**

| p_max | N_primes | Ratio    | New primes |
|-------|----------|----------|------------|
| 151   | 36       | 0.136356 | [Phase 30 anchor, N=500 zeros] |
| 155   | 36       | 0.136356 | (no new primes) |
| 157   | 37       | 0.135351 | +p=157 |
| 160   | 37       | 0.135351 | (no new primes) |
| 163   | 38       | 0.134410 | +p=163 |
| 165   | 38       | 0.134410 | (no new primes) |
| 170   | 39       | 0.133569 | +p=167 |
| 175   | 40       | 0.132647 | +p=173 |
| 180   | 41       | 0.131940 | +p=179 |
| 190   | 42       | 0.131197 | +p=181 |
| 200   | 46       | 0.128631 | +p={191,193,197,199} |

The ratio decreases smoothly and monotonically. Each new prime contributes a small incremental decline (~0.001 per prime step). The gap 157→163 is visible but not anomalous — it produces the same ~0.001 step as adjacent primes.

**Prime gap hypothesis: REJECTED.** The gap 157→163 does not trigger any regime change. The ratio at p_max=157 is 0.135, and at p_max=163 is 0.134 — both well within the monotone decline.

---

## Track A2 — Extended Trajectory (p_max 200→1000)

**Finding: Continuous monotone decline. R²=0.9994 for log-decay model.**

| p_max | N_primes | Ratio    | vs c₁    |
|-------|----------|----------|----------|
| 200   | 46       | 0.128631 | +0.0107  |
| 250   | 53       | 0.124688 | +0.0067  |
| **300**   | **62**   | **0.118099** | **+0.0001** ← passes through c₁ |
| 400   | 78       | 0.109811 | −0.0082  |
| 500   | 95       | 0.102727 | −0.0153  |
| 600   | 109      | 0.098117 | −0.0199  |
| 700   | 125      | 0.093847 | −0.0241  |
| 800   | 139      | 0.089668 | −0.0283  |
| 900   | 154      | 0.086297 | −0.0317  |
| 1000  | 168      | 0.082508 | −0.0355  |

**Key finding:** The ratio passes through c₁=0.118 at approximately p_max=300 (62 primes), then continues declining. c₁ is a **crossing point**, not a floor.

**Log-decay model** (y = a·log(N) + b): R²=0.9994 — excellent fit.
- Formula: ratio ≈ −0.0356·log(N_primes) + 0.265
- At N_primes=168 (p_max=1000): predicted 0.0832, actual 0.0825 ✓

The ratio is heading toward 0 as the prime set grows, consistent with the BK trace mean converging to 0 by prime number equidistribution.

---

## Track A3 — Separate Regime Fitting

### Regime 1 (Phase 30 p_max grid, recomputed at N=500 zeros)

| N_primes | Phase 30 (N=100) | Phase 32 (N=500) |
|----------|------------------|------------------|
| 6        | 0.2479           | 0.1733           |
| 9        | 0.2466           | 0.1716           |
| 10       | 0.2416           | 0.1699           |
| 12       | 0.2344           | 0.1670           |
| 16       | 0.2189           | 0.1614           |
| 20       | 0.2106           | 0.1558           |
| 25       | 0.1970           | 0.1496           |
| 31       | 0.1833           | 0.1427           |
| 36       | 0.1736           | 0.1364           |

The Phase 30 baseline used N=100 zeros; Phase 32 uses N=500. With more zeros, the mean BK trace converges to a lower value (the oscillating cos terms cancel more). **The ratio is N_zeros-dependent** — it decays as N_zeros increases, in addition to decaying as N_primes increases.

**Fixed-c power-law fit (N=500 data):**
- c=c₁=0.118: a=0.1463, b=0.4773, R²=0.868 ← **best fixed-c** (same winner as Phase 30)
- c=1/2π=0.159: R²=0.279
- c=1/4=0.250: R²=−52.5 (fails completely)

c₁ remains the best fixed-c candidate for the Regime 1 power-law fit, even after correcting the N_zeros count.

### Regime 2 (corrected)

Since there is no genuine "Regime 2" (the inversion was a bug), this section fits the corrected p_max=200→700 data:

**Log-decay model** (4 corrected points): R²=0.9996, formula: ratio ≈ −0.0350·log(N) + 0.2625.
Extrapolated at N~170 primes (p_max=1000): 0.083 — consistent with A2.

---

## Track D1 — Bilateral Zero Pair Count Reconciliation

**Conclusion: Definitional difference, not a script error.**

| Statistic | Value |
|-----------|-------|
| Tr_BK < 0 at N=500 | 383/500 = 76.6% ← **exactly matches Phase 29 BK burst** ✓ |
| Tr_BK range | [−3.54, +1.48] |
| Tr_BK mean | −0.696 |

### The 6,290 vs 161 Discrepancy

| Count | Source | Methodology |
|-------|--------|-------------|
| 6,290 | CAILculator (Phase 29) | Sedenion bilateral zero confidence at 95% threshold in v(ρ) embedding space |
| 161   | Python rh_phase31.py (Phase 31) | \|Tr_BK(γᵢ) + Tr_BK(γⱼ)\| < 0.01 |
| 469   | Python rh_phase32.py (Phase 32) | Same criterion but with correct formula (scaled differently) |

The two definitions are **fundamentally different**:
- CAILculator counts sedenion-space algebraic bilateral zero pairs in the AIEX-001a product F(ρ)
- Python counts pairs of zeros where the BK traces nearly cancel (scalar proximity)

**Threshold probe (Phase 32 formula):**
- threshold=0.01 → 469 pairs
- threshold=0.10 → 4,687 pairs (closest to 6,290, diff=1,603)
- threshold=0.50 → 23,277 pairs

No single threshold in the Python criterion reproduces 6,290. The CAILculator metric is qualitatively different.

**Recommendation:** Retire the "superlinear growth from 44 to 6,290" claim from the paper unless the CAILculator criterion is explicitly defined and reproducible in Python. The two counts should be reported as distinct statistics measuring different objects.

---

## Summary of Phase 32 Findings

| Finding | Status | Impact |
|---------|--------|--------|
| Phase 31 "inversion" (ratio=1.113) | **FORMULA ARTIFACT** | Phase 31 extension values invalidated |
| Phase 31 formula bug | **CONFIRMED** | bilateral_trace missing 1/√p weight |
| Phase 30 formula verification | **CONFIRMED** | N=100, 6 primes → 0.2479 ✓ |
| No regime boundary / no inversion | **CONFIRMED** | Monotone decline throughout |
| c₁=0.118 is a crossing point at p_max≈300 | **NEW FINDING** | Not a floor |
| Ratio converges toward 0 | **NEW FINDING** | log(N) model, R²=0.9994 |
| Track D: 161 vs 6,290 definitional | **RESOLVED** | Different objects, not a bug |

---

## Implications for the Canonical Six v1.4 Paper (April 1 Deadline)

The abstract revision from Phase 32 roadmap must be updated to reflect:

1. **"Sedenion Horizon Theorem" → "Sedenion Horizon Conjecture"** ← unchanged from Phase 31 recommendation
2. **The "two-regime structure" finding does NOT exist** — this was a Phase 31 formula artifact
3. **"c₁ as floor" → "c₁ as crossing point"** — the ratio passes through c₁ at p_max≈300 but continues declining toward 0
4. **Phase 31 extension ratios (1.1132, etc.) must be removed** or explicitly labeled as computed with wrong formula

The Sedenion Horizon Conjecture remains mathematically interesting (c₁ IS special in the Regime 1 power-law fit) but the claim that the ratio converges TO c₁ is not supported by Phase 32 data.

---

## Reproducibility

**Script:** `rh_phase32.py`
**Outputs:**
- `phase32_boundary_scan.json` — Track A1 fine-scan
- `phase32_weil_full.json` — Track A2 full sequence
- `phase32_regime_fits.json` — Track A3 fits
- `phase32_track_d_reconciliation.txt` — Track D1 reconciliation

```bash
pip install numpy scipy
python rh_phase32.py
```

**Zeros:** `rh_zeros.json` (1,000 zeros, mpmath dps=25); 500 used.

---

## Citation

Chavez, P. (2026). *Phase 32: Two-Regime Weil Characterization — RH Investigation.*
Chavez AI Labs LLC. GitHub: https://github.com/ChavezAILabs/CAIL-rh-investigation

---

*Chavez AI Labs LLC — Applied Pathological Mathematics: Better math, less suffering.*
