# RH Phase 17 — CAILculator Handoff
## Q-Vector Access: Multi-Channel Embedding
**Date:** March 12, 2026
**Researcher:** Paul Chavez, Chavez AI Labs LLC
**Status:** Prep scripts complete; awaiting CAILculator MCP analysis

---

## Background

All prior phases (7–16) accessed P-vector geometry exclusively. The Canonical Six bilateral zero divisors each have a P-vector (proven to lie on the E8 first shell, forming a single Weyl orbit) and a Q-vector. Phase 15C established that **framework-independence lives in the Q-vector**: the canonical/non-canonical distinction is invisible to P-vector projections because all framework-dependent patterns share P-vectors with Canonical Six patterns.

Phase 17 opens the Q-vector for the first time.

**The Q-vector 8D images** (derived from 16D sedenion structure; sign rule: e_{8+k} → pos k with sign −1):

| Pattern | P (16D) | Q (16D) | 8D image | Status |
|---------|---------|---------|----------|--------|
| 1 | e₁+e₁₄ | e₃+e₁₂ | q₁ = v₂ = (0,0,0,+1,−1,0,0,0) | Already tested as P2 |
| 2 | e₃+e₁₂ | e₅+e₁₀ | **q₂ = (0,0,−1,0,0,+1,0,0)** | **NEW** |
| 3 | e₄+e₁₁ | e₆+e₉  | q₃ = −v₁ = (0,−1,0,0,0,0,+1,0) | Isometry: same DFT as v₁ |
| 4 | e₁−e₁₄ | e₃−e₁₂ | **q₄ = (0,0,0,+1,+1,0,0,0)** | **NEW** |
| 5 | e₁−e₁₄ | e₅+e₁₀ | q₂ (same as Pattern 2) | NEW |
| 6 | e₂−e₁₃ | e₆+e₉  | q₃ (same as Pattern 3) | — |

Two genuinely new directions: **q₂** and **q₄**.

**Algebraic note on q₄:** The q₄ projection of embed_pair(g₁,g₂) equals H/2 + A, where H = 2g₁g₂/(g₁+g₂) is the harmonic mean and A = (g₁+g₂)/2 is the arithmetic mean. This is the *positive complement* of the P2 projection (P2 = H/2 − A ≤ 0), and q₄ + P2 = H (harmonic mean of the gap pair).

---

## Phase 17A Results (prep script: `rh_phase17a_prep.py`)

### To run:
```
python rh_phase17a_prep.py
```
Output file: `p17a_results.json`

### What the script computes:
- **17A-i**: Log-prime DFT SNR for q₂ projection of embed_pair on ζ gap pairs (10k zeros)
- **17A-ii**: Log-prime DFT SNR for q₄ projection of embed_pair on ζ gap pairs
- **17A-iii**: q₃ = −v₁ isometry verification (analytic theorem, deviation should be < 10⁻¹⁰)

### CAILculator analysis protocol:

Run Chavez Transform on the Q-vector sequences. The JSON file `p17a_results.json` contains:
- `q2_sequence_500`: first 500 values of q₂·embed_pair(gₙ, gₙ₊₁)
- `q4_sequence_500`: first 500 values of q₄·embed_pair(gₙ, gₙ₊₁)

**For each sequence, run detect_patterns with:**
- alpha=1.0, dimension_param=2, pattern_id=1
- dimensions_tested=[1,2,3,4,5]

**Compare to P2 reference** (from Phase 14B, CLAUDE.md):
- P2 symmetry: 88.5% (for gaps), ~82–84% (for spacing ratios)
- P2 CV: 0.146

**Key questions for CAILculator:**
1. Do q₂ and q₄ sequences give Chavez CV ≈ 0.146 (same universal CV as all other datasets)?
2. Is q₄ symmetry higher than q₂ symmetry? (q₄ = H/2+A is "smooth"; q₂ is asymmetric)
3. Does the dimensional persistence differ between q₂ and q₄?

---

## Phase 17B Results (prep script: `rh_phase17b_prep.py`)

### To run:
```
python rh_phase17b_prep.py
```
Output file: `p17b_results.json`

### Sub-experiment 17B-i: L-function comparative Q-projection

The script applies q₂ and q₄ projections to ζ zeros (10k), chi₄ zeros (2k), and chi₃ zeros (2k), then computes log-prime DFT SNR profiles.

**Decision criteria (Route B test for Q-vectors):**

| Outcome | Interpretation |
|---------|---------------|
| chi₄ p=2 ratio ≈ 0.003 (same as Phase 16B) | Q-vectors encode Euler product identically to P-vectors |
| chi₄ p=2 ratio differs significantly | Q-vectors carry *different* arithmetic information |
| chi₄ p=2 ratio ≈ 1.0 (not suppressed) | Q-vectors do NOT encode ramification |

Phase 16B established (P-vector / spacing ratio):
- p=2 in chi₄: 353× suppressed (chi₄/ζ ratio = 0.003)
- p=3 in chi₃: 736× suppressed (chi₃/ζ ratio = 0.001)

### Sub-experiment 17B-ii: Sedenion bilateral zero divisor verification

Implements the Cayley-Dickson CD4 multiplication and verifies P*Q = Q*P = 0 for all 6 patterns computationally (re-verification of Lean 4 proof to machine precision).

**Three-gap sedenion statistic (new):**
For x_n = g_n·P₁ + g_{n+1}·Q₁, the sedenion product x_n · x_{n+1} has:
```
scalar_part(x_n · x_{n+1}) = −2 · g_{n+1} · (g_n + g_{n+2})
```
This follows analytically from P₁² = Q₁² = −2·e₀ and P₁·Q₁ = 0 (bilateral condition).

The three-gap statistic `s_n = g_{n+1}·(g_n + g_{n+2})` captures how the n-th gap relates to the sum of its neighbors. For GUE, three-gap correlations are governed by the 3-point form factor (non-trivial); for Poisson (independent), s_n factorizes.

**For CAILculator analysis** — compute Chavez Transform on the three-gap statistic sequence extracted from `p17b_results.json`.

---

## Theoretical Significance

### If Q-vectors detect the same primes as P-vectors:
The arithmetic encoding (Route B) runs through both the P-vector geometry (E8 Weyl orbit, already characterized) and the Q-vector geometry (new directions q₂, q₄). This would mean the *full bilateral zero divisor structure* — not just the P-component — is reading the Euler product. Important for AIEX-001: the operator H should then be built from the complete zero divisor pairs, not just the P-projections.

### If Q-vectors detect different primes or with different suppression ratios:
The two components of each bilateral zero divisor pair are encoding *different* aspects of the L-function arithmetic. This would be the first evidence that P and Q carry distinguishable arithmetic information — a fundamentally new finding about the sedenion structure.

### If Q-vectors give null signal:
Framework-independence (Q-vector property, Phase 15C) does not manifest in the log-prime DFT via the embed_pair kernel. Phase 18 must design a different probe — direct sedenion multiplication (beyond embed_pair), or the multi-channel embedding route.

---

## Connection to AIEX-001

The sedenion product statistic in 17B-ii demonstrates that bilateral zero divisor structure naturally generates three-gap correlations: `s_n = g_{n+1}·(g_n + g_{n+2})`. This is a *nonlinear* functional of the gap sequence that emerges directly from the algebraic condition P·Q = 0.

If this statistic discriminates actual ζ zeros from GUE/Poisson (Act/GUE variance ratio ≠ 1), it would be the first *nonlinear* algebraic probe of the RH zero structure — beyond the linear projections used in Phases 7–16.

The Act/GUE variance ratio is expected to track the `~0.65` seen in all P-vector projections (Phases 10–12). Any deviation would signal that the three-gap structure differs from two-gap structure in a way the bilateral product captures but single projections miss.

---

## Files

| File | Description |
|------|-------------|
| `rh_phase17a_prep.py` | Q-vector DFT survey (ζ zeros) |
| `rh_phase17b_prep.py` | L-function comparison + sedenion verification |
| `p17a_results.json` | Phase 17A results (generated by script) |
| `p17b_results.json` | Phase 17B results (generated by script) |
| `RH_Phase17_Handoff.md` | This document |

---

*Chavez AI Labs LLC · Applied Pathological Mathematics*
*"Better math, less suffering"*
