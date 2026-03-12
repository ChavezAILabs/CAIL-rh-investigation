# RH Phase 14C -- Color Group Spectral Survey: RESULTS

**Date:** 2026-03-09
**Status: COMPLETE**
**Verdict: COLOR GROUP MEMBERSHIP DOES NOT PREDICT SPECTRAL SIMILARITY — mathematical form does**

---

## SNR at Log-Prime Frequencies: All Five P-Vectors

| Prime | P1 (CG1) | P2 (CG2) | P3 (CG3) | P4 (CG1) | P5 (CG2) | SR (13A) |
|---|---|---|---|---|---|---|
| 2 | 750 | **1585** | **1585** | 572 | 504 | 0.84 |
| 3 | 917 | **1493** | **1493** | 979 | 1458 | 7.6 |
| 5 | 680 | 606 | 606 | 1182 | **2404** | 76 |
| 7 | 464 | 181 | 181 | 1128 | **2510** | 140 |
| 11 | 232 | **0.90** | **0.90** | 881 | 2076 | 231 |
| 13 | 172 | 7.8 | 7.8 | 764 | 1818 | 246 |
| 17 | 111 | 47 | 47 | 591 | 1396 | 206 |
| 19 | 95 | 63 | 63 | 527 | 1231 | 212 |
| 23 | 71 | 97 | 97 | 415 | 964 | 185 |

Signal primes per P-vector (SNR > 2.0 AND > 1.5× max control):
- **P1**: all 9 primes [2,3,5,7,11,13,17,19,23]
- **P2**: 8 primes [2,3,5,7,13,17,19,23] — p=11 absent (SNR=0.90)
- **P3**: 8 primes [same as P2 — spectral isometry]
- **P4**: all 9 primes
- **P5**: all 9 primes

---

## Color Group Spectral Similarity (Pairwise SNR Profile Correlations)

|  | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| **P1** | 1.000 | 0.897* | 0.897 | 0.566 | 0.045 |
| **P2** | 0.897 | 1.000 | 1.000* | 0.145 | **-0.400** |
| **P3** | 0.897 | 1.000* | 1.000 | 0.145 | -0.400 |
| **P4** | 0.566* | 0.145 | 0.145 | 1.000 | 0.849 |
| **P5** | 0.045 | **-0.400** | -0.400 | 0.849* | 1.000 |

*Within-group pairs (CG1: P1/P4; CG2: P2/P5; CG3: P3 only)

### Within-group similarities
- CG1: r(P1, P4) = **0.566** — moderate
- CG2: r(P2, P5) = **−0.400** — **anti-correlated**

### Cross-group pair outperforming within-group
- r(P1, P2) = **0.897** — stronger than either within-group pair
- r(P1, P3) = 0.897 — P1 is spectrally closer to P2/P3 (different group) than to P4 (same group)

**The Color Group hypothesis is violated.** CG2 contains internally anti-correlated
members (P2 and P5), while cross-group pairs can be strongly correlated.

---

## What Predicts Spectral Profile?

Mathematical form, not Color Group membership:

| Feature | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| Form | g1*g2/s | -(g1²+g2²)/(2s) | (g1²+g2²)/(2s) | g2*(s+1)/s | (g1-g2)+g1/s |
| Symmetric in g1,g2? | Yes | Yes | Yes | **No** | **No** |
| Magnitude or difference? | Magnitude | Magnitude | Magnitude | Magnitude | **Difference** |
| Spectral profile | Smooth low-pass | Notch at p=11 | Same as P2 | Steep low-pass | Steep low-pass |

- **P1, P2, P3** are all symmetric magnitude-sensitive functions → similar profiles (high r)
- **P4** = g2*(s+1)/s ≈ g2 for large s — mostly raw g2, low-pass but steep
- **P5** = (g1−g2) + g1/s — dominated by gap difference; asymmetric, different physics

The P5 high SNR values (2510 at p=7) likely reflect that the gap *difference* g1−g2 is
modulated more strongly by short-period BK oscillations (large log p) than the raw gaps.
P5 is essentially a high-pass filter like the spacing ratio, but linear rather than scale-free.

---

## P2/P3 Antipodal Pair

SNR profiles identical to machine precision for all 9 primes (ratio = 1.0000000000 each).
The Weyl reflection α₄ (v2 ↔ v3) is a perfect spectral isometry — confirmed redundantly
here across all five P-vectors in the Color Group context.

---

## P1 as a Bridge

P1 (CG1) has r=0.897 with P2/P3 (CG2/CG3) and only r=0.566 with P4 (its own Color Group).
P1 = g1*g2/(g1+g2) is the harmonic mean of the gap pair. Like P2, it is symmetric and
magnitude-sensitive. Despite the algebraic Color Group separation, spectral behavior is
governed by these analytic properties.

**P1 detects all 9 primes** including p=11 (SNR=232) where P2 goes dark. P1 occupies
the intermediate regime — not as low-pass as P2, not as high-pass as SR. It acts as a
spectral bridge across the p=11 crossover.

---

## Files

| File | Purpose |
|---|---|
| `rh_phase14c_prep.py` | Analysis script |
| `p14c_results.json` | Full results JSON |
| `RH_Phase14C_Results.md` | This document |

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
