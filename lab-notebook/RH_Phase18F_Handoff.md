# Phase 18F Handoff — 2-Adic Tower: chi8 Companion Test
## Chavez AI Labs LLC · March 23, 2026

---

## Redesign Note

Phase 18F was originally planned as a chi16 computation. **There are no real primitive Dirichlet characters of conductor 16.** This is a mathematical theorem, not a computation error:

> **Proof:** (Z/16Z)* ≅ Z/2 × Z/4. Any real (order-2) character χ mod 16 satisfies χ(9) = χ(3)² = 1 (since χ(3) ∈ {±1}). The kernel of (Z/16Z)* → (Z/8Z)* is {1, 9}, so χ(9) = 1 means χ is induced from mod 8. Therefore every real character of modulus 16 has conductor dividing 8. ∎

The 2-adic tower for real primitive characters terminates at chi8. Phase 18F is redesigned to answer the same underlying question — "is chi8's Q2 elevation a conductor-8 property or character-specific?" — via a cleaner test.

---

## Redesigned Objective

Test the **chi8 companion**: the other real primitive character of conductor 8.

| L-function | Conrey label | Mean Q2 ratio | Source |
|---|---|---|---|
| chi4 | dirichlet_char(4, 3) | 0.158 | Phase 18A |
| chi8a | dirichlet_char(8, 5) | 0.298 | Phase 18A |
| **chi8b** | **dirichlet_char(8, 7)** | **???** | **Phase 18F** |

There are exactly two real primitive characters of conductor 8 (both are Kronecker symbols for fundamental discriminants ±8). chi8a and chi8b have the same conductor but different chi-value patterns at primes.

**Key question:** Does chi8b also show Q2 ≈ 0.298?

- **Yes (both elevated):** Q2 elevation is a **conductor-8 property** — structural, shared by all real primitive characters of that conductor. The 2-adic tower effect is real but terminates at chi8.
- **No (only chi8a elevated):** Q2 elevation is **character-specific** — tied to chi8a's chi-value pattern at specific primes, not to conductor 8 as such.

---

## Script

**File:** `rh_phase18f_prep.py`

**Run:**
```
cd C:\dev\projects\Experiments_January_2026\Primes_2026
python rh_phase18f_prep.py
```

**Dependencies:** `python-flint` (v0.8.0), standard library. Already installed.

**Estimated runtime:** ~3–5 minutes. chi4 and chi8a load from cache. chi8b requires fresh zero computation (~1,500 zeros to t≈2500).

**Output files:**
- `p18f_results.json` — complete results
- `zeros_chi8b_phase18f.json` — chi8b zero cache

---

## What the Script Does

### 1. Tower-Termination Verification
Scans all valid Conrey indices mod 16 and confirms no real primitive character of conductor 16 exists. Printed to console and recorded in JSON. Confirms the mathematical theorem is consistent with python-flint's character library.

### 2. Character Properties
Reports chi4, chi8a, chi8b properties:
- Conductor, order, real/primitive status
- Chi values at p = 2, 3, 5, 7, 11, 13, 17, 19, 23
- Ramified primes (p=2 for all three)

**Expected chi8b values:** chi8b = dirichlet_char(8,7) should be the Kronecker symbol (8/·) or (−8/·) — whichever chi8a is NOT. The two characters differ in their values at odd primes; chi8b(3) may differ in sign from chi8a(3)=-1.

### 3. Zero Computation
- **chi4:** loaded from `zeros_chi4_2k.json` (2,092 zeros)
- **chi8a:** loaded from `zeros_chi8_phase18a.json` (1,500 zeros)
- **chi8b:** computed fresh, cached to `zeros_chi8b_phase18f.json`

### 4. SNR Analysis
Q2, Q4, P2 projections for all three. Reference: zeta 10k zeros. Identical pipeline to Phase 18A.

### 5. Companion Summary
Mean Q2 (and Q4) chi/zeta ratio over unramified primes. Conclusion: conductor-8 property or character-specific.

Also includes chi8a consistency check vs Phase 18A (should reproduce ≈ 0.298, confirming pipeline stability).

---

## Interpretation Guide

### chi8a Consistency Check
The script re-runs chi8a through the pipeline (from its cached zeros). The mean Q2 ratio should reproduce the Phase 18A value of 0.298 ± small statistical variation (N=1500 vs the Phase 18A run). If it deviates significantly (>0.05), flag — this would suggest N-dependence.

### chi8b Result Interpretation

**Outcome A — Both elevated (chi8b ≈ chi8a ≈ 0.298):**
- Conductor-8 property confirmed
- The Q2 elevation tracks conductor 8 as a whole, not individual character values
- Paper contribution: "Both real primitive characters of conductor 8 show Q2 elevation ≈ 0.298; the effect is a structural property of conductor 8 in the 2-adic tower"
- Follow-up question: what is special about conductor 8 (= 2³) specifically vs conductor 4 (= 2²)?

**Outcome B — Only chi8a elevated (chi8b ≈ chi4 ≈ 0.158):**
- Character-specific result
- The Q2 elevation is determined by chi8a's specific chi-value pattern, not by conductor
- Need to identify which prime values drive the difference (compare chi8a vs chi8b chi-values at each unramified prime)
- Paper contribution: "chi8a uniquely shows Q2 elevation among conductor-8 characters; effect is not a conductor property"

**Outcome C — Both suppressed (both ≈ chi4 ≈ 0.158):**
- Phase 18A chi8a result (0.298) may be N-dependent (N=1500 may be too small)
- Run at larger N to confirm or revise Phase 18A
- Less likely given Phase 18A used the same N=1500

### Route B Check
In all outcomes, verify p=2 suppression in chi8b (chi8b(2)=0, so p=2 ramified). This extends Route B confirmation to both conductor-8 characters and provides a third data point for the suppression pattern: chi4, chi8a, chi8b all suppress p=2.

### Q4 Tower
Q4 (ultra-low-pass) may track Q2's pattern or diverge. If Q4 shows a stronger conductor-8 property than Q2, it suggests low-frequency arithmetic content is more conductor-sensitive than broadband content.

---

## Key Context

### What Changed from chi16 Plan
The chi16 test would have confirmed/denied 2-adic monotonicity by testing a higher conductor. Since chi16 doesn't exist (real), the companion test substitutes by directly testing whether the chi8 effect is:
- Universal within conductor 8 (both chi8a and chi8b elevated) → conductor property
- Specific to chi8a → character property, not conductor-driven

This is actually a stronger test than chi16 would have been, because chi16 would have tested a *different* conductor level, while the companion test holds conductor fixed and varies the character.

### Mathematical Finding for Paper
The non-existence of real primitive characters of conductor 16 is a standalone mathematical observation worth noting in the paper's Phase 18F section:

> "The 2-adic tower of real primitive Dirichlet characters terminates at chi8 (conductor 8 = 2³). No real primitive character of conductor 2^k for k ≥ 4 exists. This follows from the structure of (Z/2^k Z)* ≅ Z/2 × Z/2^(k-2) for k ≥ 3, where all quadratic (order-2) characters are induced from the mod-8 quotient."

---

## After Running

Record results in `RH_Phase18F_Results.md` with:
1. Tower-termination theorem: confirmed/noted
2. chi8b character: Conrey index, chi values at all survey primes
3. Companion table: chi4 / chi8a / chi8b Q2 and Q4 mean ratios
4. Route B: p=2 suppression in chi8b
5. Conclusion: Outcome A/B/C and interpretation
6. Decision: proceed to Thread 1 (45-direction E8 root system classification)

Update `RH_Investigation_Roadmap.md` Phase 18F section with results.
