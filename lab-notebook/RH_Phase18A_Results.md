# RH Phase 18A Results — chi3/zeta Q2 Anomaly: Conductor Survey

**Date:** March 14, 2026
**Researcher:** Paul Chavez, Chavez AI Labs LLC
**Status:** COMPLETE
**Files:** `rh_phase18a_conductor_survey.py`, `p18a_conductor_results.json`
**Zero caches:** `zeros_chi5_phase18a.json` (1500), `zeros_chi7_phase18a.json` (1500), `zeros_chi8_phase18a.json` (1500)

---

## Background

Phase 17 found an unexpected result for the Q2 projection (q2 = e5+e10, 8D image (0,0,-1,0,0,+1,0,0)):

| L-function | Q2 chi/zeta (unramified primes) | Route B prediction |
|---|---|---|
| chi3 (conductor 3) | **0.90–1.05** (anomalous ≈ 1.0) | unspecified |
| chi4 (conductor 4) | **~0.23** | unspecified |

Route B explains which primes are suppressed (those where chi(p) = 0, i.e., ramified primes) but says nothing about the SNR ratio for unramified primes. The chi3/Q2 ≈ 1.0 was outside Route B's scope.

**Candidate hypothesis:** q2 has nonzero components at E8 coordinates 3 and 6. Chi3 has conductor 3. The sedenion basis index 3 may encode the prime 3 directly — giving chi3 a structural alignment with the q2 direction that other L-functions lack.

**Phase 18A test:** Compute Q2, Q4, and P2 log-prime DFT SNR profiles for chi5, chi7, chi8 (new conductors) and compare chi/zeta ratios using the full 10k zeta zeros as reference denominator (matching Phase 17 methodology).

---

## Characters Tested

| Name | Conductor | Order | Ramified prime | chi at p=2,3,5,7,11,13,17,19,23 |
|---|---|---|---|---|
| chi3 | 3 | 2 | p=3 | −1,0,−1,+1,−1,+1,+1,−1,+1 |
| chi4 | 4 | 2 | p=2 | 0,−1,+1,−1,−1,+1,+1,−1,−1 |
| chi5 | 5 | 2 | p=5 | −1,−1,0,−1,+1,−1,−1,+1,−1 |
| chi7 | 7 | 2 | p=7 | +1,−1,−1,0,+1,−1,−1,−1,+1 |
| chi8 | 8 | 2 | p=2 | 0,−1,−1,+1,−1,−1,+1,−1,+1 |

All confirmed real, primitive. Zeta zeros: 10,000 (full Phase 10B dataset). Each chi-function: 1,499 gaps (cached).

---

## Q2 SNR Profiles

Q2 direction = (0,0,−1,0,0,+1,0,0).
Zeta reference from full 10k zeros. Asterisk (*) = ramified prime (chi(p)=0).

| L-function | p=2 | p=3 | p=5 | p=7 | p=11 | p=13 | p=17 | p=19 | p=23 |
|---|---|---|---|---|---|---|---|---|---|
| **zeta (10k)** | 418.7 | 1143.0 | 1761.7 | 1757.8 | 1357.0 | 1151.9 | 841.6 | 726.6 | 549.1 |
| chi3 | 577.7 | **0.2*** | 2290.3 | 2253.7 | 1601.2 | 1237.0 | 853.4 | 755.7 | 575.2 |
| chi4 | **0.1*** | 193.9 | 283.7 | 288.3 | 230.9 | 178.5 | 123.6 | 107.2 | 81.9 |
| chi5 | 43.0 | 131.0 | **0.1*** | 193.1 | 159.5 | 128.8 | 97.7 | 91.5 | 63.4 |
| chi7 | 60.1 | 155.3 | 275.5 | **0.2*** | 223.2 | 190.3 | 140.5 | 118.4 | 84.2 |
| chi8 | **0.1*** | 275.1 | 468.0 | 498.5 | 401.9 | 348.8 | 273.1 | 242.2 | 186.1 |

---

## chi/zeta Q2 Ratios

Denominator = full 10k zeta SNR (matching Phase 17).

| L-function | p=2 | p=3 | p=5 | p=7 | p=11 | p=13 | p=17 | p=19 | p=23 | Mean (unramified) |
|---|---|---|---|---|---|---|---|---|---|---|
| chi3 | **1.38** | 0.00* | **1.30** | **1.28** | **1.18** | **1.07** | **1.01** | **1.04** | **1.05** | **1.165** |
| chi4 | 0.00* | 0.17 | 0.16 | 0.16 | 0.17 | 0.15 | 0.15 | 0.15 | 0.15 | 0.158 |
| chi5 | 0.10 | 0.11 | 0.00* | 0.11 | 0.12 | 0.11 | 0.12 | 0.13 | 0.12 | 0.114 |
| chi7 | 0.14 | 0.14 | 0.16 | 0.00* | 0.16 | 0.17 | 0.17 | 0.16 | 0.15 | 0.156 |
| chi8 | 0.00* | 0.24 | 0.27 | 0.28 | 0.30 | 0.30 | 0.32 | 0.33 | 0.34 | 0.298 |

---

## Anomaly Test Result

**CONDUCTOR-SPECIFIC: chi3/Q2 ≈ 1.0 is unique to conductor 3.**

| L-function | Mean Q2 ratio (unramified) | Anomaly present? |
|---|---|---|
| chi3 (conductor 3) | **1.165** | YES — ≈ 1.0 |
| chi4 (conductor 4) | 0.158 | No |
| chi5 (conductor 5) | 0.114 | No |
| chi7 (conductor 7) | 0.156 | No |
| chi8 (conductor 8) | 0.298 | No |

Threshold: 0.7 < ratio < 1.3 = anomalous. Only chi3 passes.

---

## Route B Suppression — All 5 L-Functions Confirmed

| L-function | Ramified prime | chi/zeta Q2 at suppressed prime |
|---|---|---|
| chi3 | p=3 | 0.000 |
| chi4 | p=2 | 0.000 |
| chi5 | p=5 | 0.000 |
| chi7 | p=7 | 0.000 |
| chi8 | p=2 | 0.000 |

All 5 L-functions confirm Route B suppression. Ramified prime suppression is universal.

---

## Q4 and P2 Profiles (supplementary)

### Q4 chi/zeta ratios

| L-function | p=2 | p=3 | p=5 | p=7 | Mean (unramified, low-p) | Notes |
|---|---|---|---|---|---|---|
| chi3 | 0.13 | 0.00* | 0.11 | 0.09 | ~0.11 | Normal |
| chi4 | 0.00* | 0.04 | 0.04 | 0.04 | ~0.04 | Normal |
| chi5 | 0.14 | 0.14 | 0.00* | 0.15 | ~0.14 | Normal |
| chi7 | 0.07 | 0.07 | 0.08 | 0.00* | ~0.07 | Normal |
| chi8 | 0.00* | 0.18 | 0.19 | 0.21 | ~0.19 | Normal |

No Q4 anomaly. The chi3/Q2 ≈ 1.0 is specific to the Q2 direction.

### P2 chi/zeta ratios

| L-function | Mean (unramified, p=5..23) | Notes |
|---|---|---|
| chi3 | ~0.5 | Elevated at p=11,13 (anomalous spikes) |
| chi4 | ~0.18 | Normal |
| chi5 | ~0.09 | Normal |
| chi7 | ~0.03 | Normal |
| chi8 | ~0.23 | Normal |

P2 shows a weaker chi3 elevation at p=11,13, distinct from the uniform Q2 elevation. Not the primary signal.

---

## Interpretation

### Primary finding: sedenion basis index encodes prime arithmetic

Q2 = e5+e10 in sedenion notation, with 8D E8 image q2 = (0,0,−1,0,0,+1,0,0).
The nonzero components appear at **positions 3 and 6** in the 8D vector (0-indexed).

Chi3 has conductor 3. Its Euler product is:
```
L(chi3, s) = prod_{p ≠ 3} 1/(1 - chi3(p)·p^{-s})
```
where chi3(3) = 0 (ramified), and chi3(p) = Legendre symbol (p/3) for p ≠ 3.

The position-3 component of q2 appears to align with conductor 3 in a way that no other tested conductor shares. The chi3 zeros carry Q2 SNR at the same level as zeta zeros (ratio ≈ 1.0–1.4 across all unramified primes), while chi4, chi5, chi7, chi8 all return ratios ≈ 0.1–0.3.

### What this is not

- Not a data quantity effect: Phase 17 chi3 result was N=1893; Phase 18A uses N=1499 for chi3, same range — the anomaly persists.
- Not a generic real-primitive-character property: chi4 (also real primitive, conductor 4) has ratio 0.158. The anomaly is not about the character type.
- Not a low-conductor effect: chi5 (conductor 5) has ratio 0.114, lower than chi4. The anomaly does not simply increase with decreasing conductor.
- Not shared with chi8 despite same ramification: chi8 (conductor 8, ramified at p=2 like chi4) has ratio 0.298 — elevated versus chi4 and chi5 but far below chi3's 1.165.

### Open questions after Phase 18A

1. **Sedenion index correspondence**: Does the sedenion basis position 3 (in e5, the 5th sedenion basis element via e5+e10) correspond to the prime 3 by some arithmetic rule? The Q2 direction uses e5+e10; in the 16D sedenion numbering, e5 has index 5 and e10 has index 10. Position 3 in the 8D reduction is the 4th coordinate (0-indexed). More work needed to understand the exact mapping.

2. **Chi8 elevation**: Chi8 shows Q2 ratios of 0.24–0.34, notably higher than chi4, chi5, chi7 (all 0.11–0.16). Chi8 has conductor 8 = 2³. This may warrant a follow-up with higher conductor characters.

3. **Functional equation structure**: Chi3 is special among real primitive characters — it is the minimal-conductor odd character. Its functional equation has a specific gamma factor. Does this functional equation structure, combined with the E8 geometry of q2, force the SNR ratio to 1?

4. **Q-vector index theorem (conjecture)**: If the sedenion basis index of the Q-vector encodes the prime p directly, then Q(e_p + e_{16-p}) should show chi_p/zeta ≈ 1.0 for conductor-p characters. This is testable: q2 = e5+e10 → prime 5 candidate would be q2 by this encoding. But chi5/Q2 ≈ 0.114, not 1.0 — so the simple "index = prime" reading is wrong. The specific encoding rule remains open.

---

## AIEX-001 Implications

The chi3/Q2 ≈ 1.0 anomaly suggests that the Q2 direction in E8 space is not merely a spectral filter but encodes specific arithmetic structure from the conductor of an L-function. If AIEX-001 postulates a Hilbert-Pólya operator H with eigenvectors in the bilateral zero divisor root space, the Q-vector directions must carry arithmetic labels beyond their geometric role. The conductor-3 / q2-direction alignment may be a clue about how the operator H distinguishes L-functions by their arithmetic.

---

## Summary Table

| Finding | Result |
|---|---|
| chi3/zeta Q2 anomaly reproduced | YES (mean ratio 1.165) |
| Anomaly conductor-specific | YES — only chi3 out of 5 tested |
| chi4, chi5, chi7, chi8 Q2 ratio | ~0.11–0.30 (normal range) |
| Route B ramified prime suppression | Confirmed for all 5 L-functions |
| Q4 anomaly for chi3 | NO — Q4 shows normal ratios |
| P2 anomaly for chi3 | Partial (elevated at p=11,13 only) |
| chi8 Q2 elevation (conductor 8) | Moderate (0.298) — worth follow-up |

**Phase 18A conclusion:** The chi3/zeta Q2 ≈ 1.0 anomaly is conductor-specific to conductor 3. The q2 = e5+e10 sedenion direction has a structural relationship with conductor-3 L-functions that is not shared by conductors 4, 5, 7, or 8. The exact arithmetic mechanism — and whether it generalizes to other prime-indexed conductors with corresponding Q-vector directions — is an open question for future phases.
