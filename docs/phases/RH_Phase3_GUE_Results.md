# RH Phase 3 — GUE Level Repulsion Test Results
**Experiment ID:** RH_GUE_2026_001  
**Date:** 2026-03-04  
**Researcher:** Paul Chavez, Chavez AI Labs

---

## Decision Table (Final)

| Sequence | Chavez Symmetry | Δ from Baseline | Trials |
|---|---|---|---|
| **Actual Riemann zero gaps (n=99)** | **83.4%** | baseline | — |
| Poisson Exp(mean=2.25) seed=1 | 79.0% | −4.4 pts | |
| Poisson Exp(mean=2.25) seed=2 | 81.5% | −1.9 pts | |
| Poisson Exp(mean=2.25) seed=3 | 79.8% | −3.7 pts | |
| **Poisson Mean** | **80.1%** | **−3.3 pts** | 3 trials |
| GUE Wigner surmise seed=1 | 80.7% | −2.7 pts | |
| GUE Wigner surmise seed=2 | 78.0% | −5.4 pts | |
| GUE Wigner surmise seed=3 | 79.5% | −3.9 pts | |
| **GUE Wigner Mean** | **79.4%** | **−4.0 pts** | 3 trials |
| Sophie Germain primes (reference) | 88.5% | +5.1 pts | prior work |

---

## Key Finding: GUE Does NOT Score Higher Than Poisson

**The target outcome was:** GUE ≈ actual zeros >> Poisson (confirming GUE level repulsion fingerprint)  
**The actual outcome:** GUE (79.4%) ≈ Poisson (80.1%) << actual zeros (83.4%)

GUE and Poisson are separated by only **−0.7 points** (Poisson actually scores marginally higher than GUE). The Chavez conjugation symmetry measure **cannot distinguish GUE from Poisson gap distributions**. This definitively rules out the hypothesis that the 83.4% signal is detecting GUE level repulsion specifically.

---

## What the Signal IS Detecting

The structural difference between sequences is stark in the gap statistics:

| Sequence | Min gap | Gaps < 0.1 | Gaps < 0.5 |
|---|---|---|---|
| Actual zeros | 0.7158 | 0 | 0 |
| GUE (all trials, n=297) | 0.1493 | 0 | 4 |
| Poisson (all trials, n=297) | 0.0003 | 13 | 58 |

GUE has level repulsion (near-zero gaps suppressed), Poisson freely produces near-zero gaps. Both score ~79–80%. The actual zeros have a **minimum gap of 0.716** — far above both synthetic minimums — and zero gaps below 0.5. The actual gaps are tightly bounded below.

**Conclusion: The 83.4% signal is detecting the lower-bounded, compact support of the actual Riemann zero gap distribution, not GUE-specific correlations.** The first 99 zeros are in a low-height regime (zeros #1–99, imaginary parts 14–237) where the local density formula gives larger-than-average mean gaps, and the gaps have a higher floor than either GUE or Poisson resampling produces at scale. The Chavez bilateral symmetry measure is sensitive to this lower bound: sequences without near-zero gaps have more "balanced" bilateral structure because the extremes on both sides of the midpoint are similarly large.

---

## Revised Hierarchy Position

The 83.4% is not a GUE eigenvalue spacing fingerprint. It is a gap distribution compactness signal — reflecting the bounded-below character of actual zero gaps in the low-height regime. This is a real structural property of the zeros, but not the one sought.

```
CHAVEZ CONJUGATION SYMMETRY — REVISED INTERPRETATION
─────────────────────────────────────────────────────
SG primes                          88.5%  ← compact, prime-repulsion bounded below
Actual zero gaps (low regime)      83.4%  ← compact, bounded below ~0.7
GUE Wigner (synthetic, n=99)       79.4%  ← some near-zero gaps (min 0.15)
Poisson Exp(mean=2.25, n=99)       80.1%  ← many near-zero gaps (min 0.0003)
─────────────────────────────────────────────────────
What the measure detects: lower-bound compactness, not sequential correlations,
not GUE-specific eigenvalue repulsion
```

---

## What This Changes for the Roadmap

**Phase 1–3 net result:** The Chavez conjugation symmetry on Riemann zero gaps detects a real structural property — lower-bound compactness — but this is not the GUE algebraic structure AIEX-001 sought. The measure is not sensitive to:
- Gap ordering (Phase 2b finding)
- GUE vs. Poisson distributional differences (Phase 3 finding)

**What remains live:**
1. The scale stability (86.2% at n=249) is a real property of the zero gap lower bound across the spectrum.
2. ZDTP gateway ordering (S1 monotone descent) distinguishes smooth from noisy sequences — a weak but real signal.
3. The annihilation topology work (AT-1/AT-2) is independent and should proceed.

**Reframe for subsequent experiments:**  
To test GUE structure algebraically, the right approach is not Chavez symmetry on gap values but rather:
- **Pair correlation function** r(α): test whether the two-point correlation of zero gaps matches GUE Montgomery-Dyson. This is ordering-dependent and GUE-specific.
- **Nearest-neighbor spacing distribution**: compare actual zero spacings against Wigner P(s) vs. Poisson — a standard RMT test.
- **Number variance and spectral rigidity**: long-range statistics that specifically distinguish GUE from GOE and Poisson.

These are classical RMT tests. Applying the Chavez Transform to their *outputs* (rather than raw gaps) may give a more meaningful fingerprint.

---

## Immediate Next Steps

- [ ] Update CLAUDE.md: Chavez symmetry = lower-bound compactness signal, not GUE-specific
- [ ] Proceed to AT-1 (annihilation topology) — independent of this result
- [ ] Consider: Apply Chavez Transform to pair correlation r(α) or spacing ratio r_n = min(g_n, g_{n+1}) / max(g_n, g_{n+1}) — a GUE-specific statistic that Chavez might fingerprint successfully
- [ ] Close RH Phase 3; open Phase 4 as annihilation topology bridge
